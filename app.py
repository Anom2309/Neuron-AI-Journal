import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Neuro Nada - Daily Journal", page_icon="🌱", layout="wide")

# --- 2. KONEKSI DATABASE ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. CSS CUSTOM ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f7f4; color: #2d4035; }
    .stButton>button { background-color: #9CAF88; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .nero-box { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ffb703; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_email'] = ""

if not st.session_state['logged_in']:
    st.title("🌱 Neuro Nada Login")
    email_input = st.text_input("Masukkan Email lo:")
    if st.button("Masuk"):
        if email_input:
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email_input.strip().lower()
            st.rerun()
        else:
            st.warning("Isi email dulu, Bro!")
else:
    cols = st.columns([4, 1])
    with cols[0]:
        st.title("Neuro Nada Daily Workflow 🚀")
        st.write(f"User aktif: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    tab_harian, tab_riwayat = st.tabs(["✍️ Jurnal Harian", "📜 Riwayat Saya"])

    with tab_harian:
        col1, col2, col3 = st.columns(3)
        with col1: prioritas = st.text_area("🎯 Prioritas", height=150)
        with col2: ai_tasks = st.text_area("🤖 Otomatisasi AI", height=150)
        with col3: 
            pencapaian = st.text_area("🏆 Pencapaian", height=100)
            mood = st.select_slider("Mood", options=["Kacau", "Biasa", "Oke", "Mantap", "Sempurna"], value="Oke")
        
        if st.button("💾 SIMPAN KE DRIVE SEKARANG"):
            new_entry = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Email": st.session_state['user_email'],
                "Prioritas": prioritas,
                "AI_Tasks": ai_tasks,
                "Pencapaian": pencapaian,
                "Mood": mood
            }])
            try:
                # Ambil data lama tanpa cache
                df_lama = conn.read(worksheet="Sheet1", ttl=0)
                df_baru = pd.concat([df_lama, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_baru)
                st.success("✅ Berhasil Simpan!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Gagal Simpan: {e}")

    with tab_riwayat:
        st.subheader("Semua Riwayat Jurnal")
        # TOMBOL REFRESH MANUAL
        if st.button("🔄 Tarik Data Terbaru"):
            st.cache_data.clear()
            st.rerun()

        try:
            # KITA TAMPILIN SEMUA DATA TANPA FILTER EMAIL DULU
            # BIAR KETAHUAN DATANYA KE-READ APA ENGGAK
            raw_data = conn.read(worksheet="Sheet1", ttl=0)
            
            if raw_data is not None and not raw_data.empty:
                # Tampilkan semuanya
                st.dataframe(raw_data.sort_values(by=raw_data.columns[0], ascending=False), use_container_width=True)
                st.info("Catatan: Saat ini filter email dimatikan untuk memastikan koneksi lancar.")
            else:
                st.warning("Data di Sheets terdeteksi kosong oleh aplikasi. Cek nama Sheet lo (harus 'Sheet1').")
        except Exception as e:
            st.error(f"Error pembacaan: {e}")
