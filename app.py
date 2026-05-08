import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Konfigurasi Halaman & Tema
st.set_page_config(page_title="Daily Workflow - Neuron AI", page_icon="🌱", layout="centered")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LINK GOOGLE SHEETS LO (PASTI TEMBUS) ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/14bqio8DdbK2YcpG5ACikzuj_rlEP7tdVtWWHbXcbLGA/edit"

st.markdown("""
    <style>
    .stApp { background-color: #f0f7f4; color: #2d4035; }
    .stButton>button { background-color: #9CAF88; color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #7b8f6b; }
    .nero-box { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ffb703; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 25px; font-size: 1.1em; }
    .premium-card { background: linear-gradient(135deg, #1D3557 0%, #457B9D 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 2. Sistem Autentikasi
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = ""

if not st.session_state['logged_in']:
    st.title("🌱 Selamat Datang di Neuron AI")
    email_input = st.text_input("Alamat Email", key="in_login_mail")
    if st.button("Masuk / Daftar", key="btn_login"):
        if email_input:
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email_input.strip().lower()
            st.rerun()
        else:
            st.warning("Bro, isi emailnya dulu dong!")

else:
    user_email = st.session_state['user_email']
    is_premium = False
    
    # --- JURUS SAKTI KHUSUS OWNER (ADMIN BYPASS) ---
    if user_email == "sedichachmad@gmail.com":
        is_premium = True
    else:
        try:
            # Pake SHEET_URL langsung di sini
            df_db = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)
            if df_db is not None and not df_db.empty:
                col_email = [c for c in df_db.columns if 'email' in str(c).lower()]
                col_status = [c for c in df_db.columns if 'status' in str(c).lower()]
                
                if col_email and col_status:
                    mask = df_db[col_email[0]].astype(str).str.strip().str.lower() == user_email
                    user_info = df_db[mask]
                    
                    if not user_info.empty:
                        status_list = user_info[col_status[0]].astype(str).str.strip().str.lower().tolist()
                        if 'premium' in status_list:
                            is_premium = True
        except Exception as e:
            pass 
    
    # Header Utama
    cols = st.columns([4, 1])
    with cols[0]:
        st.title("Daily Workflow Book 🚀")
        tag_status = "👑 OWNER" if user_email == "sedichachmad@gmail.com" else ("🟡 PREMIUM" if is_premium else "⚪ FREE")
        st.write(f"Sesi milik: **{user_email}** | {tag_status}")
    with cols[1]:
        if st.button("Logout", key="btn_logout"):
            st.session_state.clear()
            st.rerun()

    # BANNER JUALAN 
    if not is_premium:
        st.markdown(f"""
            <div class='premium-card'>
                <h3>🔒 Upgrade Neuron AI Premium</h3>
                <p>Buka akses <b>Riwayat Tanpa Batas</b> dan <b>Grafik Mood Analytics</b>.</p>
                <a href='https://wa.me/628XXXXXXXXXXX?text=Halo+Achmad,+gw+mau+upgrade+Neuron+AI+buat+email+{user_email}' style='color: #1D3557; font-weight: bold; text-decoration: none; background: white; padding: 10px 20px; border-radius: 8px;'>Upgrade via WhatsApp</a>
            </div>
        """, unsafe_allow_html=True)
    else:
        if user_email == "sedichachmad@gmail.com":
            st.markdown("<div class='nero-box'><b>^‿^ Nero bilang:</b><br>\"Selamat datang kembali, Master! Semua sistem Premium sudah kebuka buat lo!\"</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='nero-box'><b>^‿^ Nero bilang:</b><br>\"Mode Premium Aktif! Yuk, kita sikat hari ini, Bro!\"</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌅 Pagi", "🚀 Siang", "🌙 Malam", "📜 Riwayat", "📊 Analytics"])
    
    with tab1:
        st.subheader("Top 3 Prioritas")
        d1 = st.text_input("Detail 1", key="d1")
        d2 = st.text_input("Detail 2", key="d2")
        d3 = st.text_input("Detail 3", key="d3")
        
    with tab2:
        st.subheader("Otomatisasi AI")
        ai_tasks = st.text_area("Ide otomatisasi...", height=150, key="ai")
        
    with tab3:
        st.subheader("Refleksi")
        achieve = st.text_input("Pencapaian", key="achieve")
        mood_val = st.slider("Mood (1-5)", 1, 5, 3, key="mood")
        
        if st.button("Simpan Jurnal Hari Ini", key="btn_save_jurnal"):
            new_entry = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Email": user_email,
                "Prioritas": f"{d1} | {d2} | {d3}",
                "AI_Tasks": ai_tasks,
                "Pencapaian": achieve,
                "Mood": mood_val,
                "Status": "Premium" if is_premium else "Free"
            }])
            try:
                # Pakai SHEET_URL langsung saat simpan
                df_lama = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)
                df_baru = pd.concat([df_lama, new_entry], ignore_index=True)
                conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=df_baru)
                st.success("✅ Berhasil Simpan!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Gagal simpan: {e}")

    with tab4:
        st.subheader("Riwayat Jurnal Lo")
        if st.button("🔄 Paksa Muat Ulang", key="btn_refresh"):
            st.cache_data.clear()
            st.rerun()
            
        try:
            # Pakai SHEET_URL di riwayat
            df_full = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)
            if df_full is not None and not df_full.empty:
                target_col = [c for c in df_full.columns if 'email' in str(c).lower()]
                if target_col:
                    col_key = target_col[0]
                    mask = df_full[col_key].astype(str).str.strip().str.lower() == user_email
                    user_df = df_full[mask].copy()
                    
                    if not user_df.empty:
                        if not is_premium:
                            st.warning("🔒 Akun Gratis hanya menampilkan 3 data terakhir.")
                            st.dataframe(user_df.sort_values(by=user_df.columns[0], ascending=False).head(3), use_container_width=True)
                        else:
                            st.dataframe(user_df.sort_values(by=user_df.columns[0], ascending=False), use_container_width=True)
                    else:
                        st.info(f"Belum ada data buat {user_email}. Coba Simpan dulu, Bro.")
                else:
                    st.warning("Kolom Email nggak spesifik, nampilin semua data:")
                    st.dataframe(df_full)
            else:
                st.info("Sheets masih kosong.")
        except Exception as e:
            st.error(f"Lagi sibuk: {e}")

    with tab5:
        st.subheader("📊 Neuron Analytics")
        if is_premium:
            st.write("Tren produktivitas dan kepuasan lo berdasarkan input jurnal:")
            try:
                # Pakai SHEET_URL di analytics
                df_chart = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)
                col_em = [c for c in df_chart.columns if 'email' in str(c).lower()]
                if col_em:
                    mask = df_chart[col_em[0]].astype(str).str.strip().str.lower() == user_email
                    user_data = df_chart[mask].copy()
                    
                    if not user_data.empty:
                        col_mood = [c for c in user_data.columns if 'mood' in str(c).lower()]
                        col_time = [c for c in user_data.columns if 'timestamp' in str(c).lower()]
                        
                        if col_mood and col_time:
                            user_data[col_mood[0]] = pd.to_numeric(user_data[col_mood[0]], errors='coerce')
                            chart_data = user_data.set_index(col_time[0])[col_mood[0]]
                            st.line_chart(chart_data)
                            st.caption("Puncak grafik menunjukkan kondisi *flow state* terbaik lo.")
                        else:
                            st.info("Belum cukup data untuk menggambar grafik.")
            except Exception as e:
                st.error("Gagal muat grafik.")
        else:
            st.error("🔒 Fitur Analytics Terkunci")
            st.write("Fitur ini eksklusif untuk member Premium.")
