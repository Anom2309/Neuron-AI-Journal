import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Daily Workflow - Neuron AI", page_icon="🌱", layout="centered")
conn = st.connection("gsheets", type=GSheetsConnection)

# CSS Custom (Sage Green & Nero Style)
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
    email_input = st.text_input("Alamat Email", key="login_field")
    if st.button("Masuk / Daftar", key="login_btn"):
        if email_input:
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email_input.strip().lower()
            st.rerun()
        else:
            st.warning("Bro, isi emailnya dulu dong!")

# --- 3. DASHBOARD UTAMA ---
else:
    cols = st.columns([4, 1])
    with cols[0]:
        st.title("Daily Workflow Book 🚀")
        st.write(f"Sesi milik: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout", key="logout_top"):
            st.session_state.clear()
            st.rerun()

    st.markdown("<div class='nero-box'><b>^‿^ Nero bilang:</b><br>\"Satu langkah kecil hari ini, fondasi besar buat masa depan! Yuk, kita sikat, Bro!\"</div>", unsafe_allow_html=True)
    
    # Tab Navigasi Sesuai Request (Pagi, Siang, Malam, Riwayat)
    tab1, tab2, tab3, tab4 = st.tabs(["🌅 Pagi (Persiapan)", "🚀 Siang (Eksekusi)", "🌙 Malam (Refleksi)", "📜 Riwayat Saya"])
    
    with tab1:
        st.subheader("Top 3 Prioritas Utama Hari Ini")
        st.write("Fokuskan pikiran. Apa yang paling penting?")
        st.checkbox("Prioritas 1", key="chk_p1")
        det1 = st.text_input("Detail Prioritas 1", label_visibility="collapsed", key="in_p1")
        st.checkbox("Prioritas 2", key="chk_p2")
        det2 = st.text_input("Detail Prioritas 2", label_visibility="collapsed", key="in_p2")
        st.checkbox("Prioritas 3", key="chk_p3")
        det3 = st.text_input("Detail Prioritas 3", label_visibility="collapsed", key="in_p3")
        
    with tab2:
        st.subheader("Otomatisasi & Delegasi AI")
        st.write("Bagian mana dari tugas hari ini yang bisa diserahkan ke prompt atau sistem otomatisasi?")
        ai_tasks = st.text_area("Catat ide otomatisasi di sini...", height=150, key="in_ai")
        
    with tab3:
        st.subheader("Evaluasi Diri & Mood")
        st.write("Pencapaian Terbaik Hari Ini:")
        achieve = st.text_input("Hal yang bikin lo bangga hari ini", label_visibility="collapsed", key="in_achieve")
        
        st.write("Tingkat Kepuasan Hari Ini:")
        mood = st.slider("Gimana hari lo?", 1, 5, 3, key="in_mood")
        
        st.write("---")
        # INI TOMBOL SIMPANNYA, BRO! SUDAH BALIK LAGI
        if st.button("Simpan Jurnal Hari Ini", key="btn_save_final"):
            new_entry = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Email": st.session_state['user_email'],
                "Prioritas": f"1. {det1} | 2. {det2} | 3. {det3}",
                "AI_Tasks": ai_tasks,
                "Pencapaian": achieve,
                "Mood": mood
            }])
            try:
                df_lama = conn.read(worksheet="Sheet1", ttl=0)
                df_baru = pd.concat([df_lama, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_baru)
                st.success("Mantap! Data jurnal hari ini berhasil disimpan ke Google Sheets. Istirahat yang cukup, Bro!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Gagal simpan: {e}")

    with tab4:
        st.subheader("Riwayat Jurnal Personal Lo")
        if st.button("🔄 Segarkan Data", key="btn_refresh"):
            st.cache_data.clear()
            st.rerun()
            
        try:
            df_full = conn.read(worksheet="Sheet1", ttl=0)
            if df_full is not None and not df_full.empty:
                # Normalisasi Kolom & Filter (OBAT ERROR .lower())
                df_full.columns = [str(c).strip().lower() for c in df_full.columns]
                user_email = str(st.session_state['user_email']).strip().lower()
                
                if 'email' in df_full.columns:
                    mask = df_full['email'].astype(str).str.strip().str.lower() == user_email
                    user_df = df_full[mask].copy()
                    
                    if not user_df.empty:
                        user_df.columns = [str(c).capitalize() for c in user_df.columns]
                        st.dataframe(user_df.sort_values(by="Timestamp", ascending=False), use_container_width=True)
                    else:
                        st.info("Belum ada riwayat untuk email lo.")
                else:
                    st.warning("Kolom 'Email' tidak ditemukan di Sheets.")
            else:
                st.info("Database masih kosong.")
        except Exception as e:
            st.error(f"Gagal memuat: {e}")
