import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada - Daily Journal", 
    page_icon="🌱", 
    layout="wide"
)

# --- 2. KONEKSI DATABASE (Google Sheets) ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. CSS CUSTOM ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f7f4; color: #2d4035; }
    .stButton>button { 
        background-color: #9CAF88; color: white; border-radius: 8px; border: none; 
        padding: 10px 24px; font-weight: bold; width: 100%;
    }
    .nero-box { 
        background-color: white; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #ffb703; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 25px; 
    }
    .header-title { color: #1D3557; font-family: sans-serif; font-weight: 700; }
    .sub-header { color: #9CAF88; font-weight: bold; border-bottom: 2px solid #9CAF88; padding-bottom: 10px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_email'] = ""

if not st.session_state['logged_in']:
    st.markdown("<h1 class='header-title'>🌱 Neuro Nada Daily Journal</h1>", unsafe_allow_html=True)
    email_input = st.text_input("Masukkan Email lo untuk sinkronisasi:")
    if st.button("Masuk"):
        if email_input:
            # Kita simpan email dalam format huruf kecil & tanpa spasi
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email_input.strip().lower()
            st.rerun()
        else:
            st.warning("Isi email dulu, Bro!")

else:
    # Header & Logout
    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown(f"<h1 class='header-title'>Neuro Nada Daily Workflow 🚀</h1>", unsafe_allow_html=True)
        st.write(f"User: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown("<div class='nero-box'><b>^‿^ Nero:</b> Fokus aja, urusan backup biar Nero yang urus!</div>", unsafe_allow_html=True)
    
    tab_panduan, tab_harian, tab_riwayat = st.tabs(["📖 Panduan", "✍️ Jurnal Harian", "📜 Riwayat Saya"])

    with tab_harian:
        col1, col2, col3 = st.columns(3)
        with col1: prioritas = st.text_area("🎯 3 Prioritas Utama", height=150)
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
                # Paksa baca data tanpa cache (ttl=0)
                df_lama = conn.read(worksheet="Sheet1", ttl=0)
                df_baru = pd.concat([df_lama, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_baru)
                st.success("✅ Mantap! Data sudah masuk ke Sheets.")
                st.cache_data.clear() # Bersihkan memori aplikasi
            except Exception as e:
                st.error(f"Gagal Simpan: {e}")

    with tab_riwayat:
        st.subheader("Jurnal lama lo")
        if st.button("🔄 Segarkan Data (Refresh)"):
            st.cache_data.clear()
            st.rerun()
            
        try:
            # PAKSA BACA DATA TERBARU (ttl=0)
            full_df = conn.read(worksheet="Sheet1", ttl=0)
            
            # Bersihkan data email di Sheets (biar nggak ada spasi/beda huruf gede-kecil)
            full_df['Email'] = full_df['Email'].astype(str).str.strip().lower()
            current_user = st.session_state['user_email']
            
            user_history = full_df[full_df['Email'] == current_user]
            
            if not user_history.empty:
                st.dataframe(user_history.sort_values(by="Timestamp", ascending=False), use_container_width=True)
            else:
                st.info(f"Belum ada data buat {current_user}. Coba simpan satu dulu!")
        except Exception as e:
            st.write("Belum ada data atau koneksi sibuk. Coba klik Refresh di atas.")
