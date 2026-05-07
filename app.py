import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Daily Workflow - Neuron AI", page_icon="🌱", layout="centered")
conn = st.connection("gsheets", type=GSheetsConnection)

# CSS Custom (Estetika Sage Green)
st.markdown("""
    <style>
    .stApp { background-color: #f0f7f4; color: #2d4035; }
    .stButton>button { background-color: #9CAF88; color: white; border-radius: 8px; font-weight: bold; width: 100%; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #7b8f6b; }
    .nero-box { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ffb703; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = ""

if not st.session_state['logged_in']:
    st.title("🌱 Neuron AI Login")
    email_input = st.text_input("Alamat Email", key="login_email_input")
    if st.button("Masuk / Daftar", key="login_button"):
        if email_input:
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email_input.strip().lower()
            st.rerun()
        else:
            st.warning("Isi email dulu dong, Bro!")

# --- 3. DASHBOARD UTAMA ---
else:
    cols = st.columns([4, 1])
    with cols[0]:
        st.title("Neuron Ai Daily Workflow Book 🚀")
        st.write(f"Sesi milik: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout", key="main_logout_btn"):
            st.session_state.clear()
            st.rerun()

    st.markdown("<div class='nero-box'><b>^‿^ Nero:</b> Satu langkah kecil hari ini adalah fondasi masa depan!</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🌅 Pagi", "🚀 Siang", "🌙 Malam", "📜 Riwayat"])
    
    with tab1:
        st.subheader("Top 3 Prioritas")
        d1 = st.text_input("Prioritas 1", key="p1_input")
        d2 = st.text_input("Prioritas 2", key="p2_input")
        d3 = st.text_input("Prioritas 3", key="p3_input")
        
    with tab2:
        st.subheader("Otomatisasi AI")
        ai_tasks = st.text_area("Ide otomatisasi...", height=150, key="ai_area")
        
    with tab3:
        st.subheader("Refleksi Malam")
        achieve = st.text_input("Pencapaian hari ini", key="achieve_input")
        mood_val = st.slider("Mood (1-5)", 1, 5, 3, key="mood_slider")
        
        if st.button("Simpan Jurnal Hari Ini", key="save_journal_btn"):
            new_entry = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Email": st.session_state['user_email'],
                "Prioritas": f"{d1} | {d2} | {d3}",
                "AI_Tasks": ai_tasks,
                "Pencapaian": achieve,
                "Mood": mood_val
            }])
            try:
                df_lama = conn.read(worksheet="Sheet1", ttl=0)
                df_baru = pd.concat([df_lama, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_baru)
                st.success("✅ Berhasil Simpan ke Sheets!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Gagal simpan: {e}")

    with tab4:
        st.subheader("Riwayat Jurnal Personal Lo")
        if st.button("🔄 Refresh Data", key="refresh_riwayat_btn"):
            st.cache_data.clear()
            st.rerun()
            
        try:
            # Ambil data mentah
            df_full = conn.read(worksheet="Sheet1", ttl=0)
            
            if df_full is not None and not df_full.empty:
                # 1. Bersihkan nama kolom (kecilkan & hapus spasi)
                df_full.columns = [str(c).strip().lower() for c in df_full.columns]
                
                # 2. Cari kolom yang mengandung kata 'email'
                email_cols = [c for c in df_full.columns if 'email' in c]
                
                if email_cols:
                    target_col = email_cols[0]
                    user_ref = str(st.session_state['user_email']).strip().lower()
                    
                    # 3. FILTER AMAN: Gunakan .str.strip().str.lower()
                    # Ini obat buat error 'Series object has no attribute lower'
                    mask = df_full[target_col].astype(str).str.strip().str.lower() == user_ref
                    user_df = df_full[mask].copy()
                    
                    if not user_df.empty:
                        # Rapiin judul kolom pas tampil
                        user_df.columns = [str(c).capitalize() for c in user_df.columns]
                        st.dataframe(user_df.sort_values(by=user_df.columns[0], ascending=False), use_container_width=True)
                    else:
                        st.info("Belum ada data untuk email ini.")
                else:
                    st.warning("Kolom Email tidak ditemukan. Menampilkan semua data:")
                    st.dataframe(df_full)
            else:
                st.info("Sheets masih kosong.")
        except Exception as e:
            st.error(f"Gagal memuat riwayat: {e}")
