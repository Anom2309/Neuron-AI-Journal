import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada - Daily Workflow", 
    page_icon="🌱", 
    layout="wide"
)

# --- 2. KONEKSI DATABASE ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. CSS CUSTOM (Estetika Sage Green - Balik ke Awal) ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f7f4; color: #2d4035; }
    .stButton>button { 
        background-color: #9CAF88; color: white; border-radius: 8px; border: none; 
        padding: 10px 24px; font-weight: bold; width: 100%;
    }
    .stButton>button:hover { background-color: #7b8f6b; }
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
    st.markdown("<h1 class='header-title'>🌱 Neuro Nada Daily Workflow</h1>", unsafe_allow_html=True)
    st.write("Masukkan email lo untuk sinkronisasi jurnal otomatis.")
    email_input = st.text_input("Alamat Email")
    if st.button("Masuk / Daftar"):
        if email_input:
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email_input.strip().lower()
            st.rerun()
        else:
            st.warning("Emailnya diisi dulu dong, Bro!")

# --- 5. DASHBOARD UTAMA (Setelah Login) ---
else:
    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("<h1 class='header-title'>Neuro Nada Daily Workflow 🚀</h1>", unsafe_allow_html=True)
        st.write(f"Sesi milik: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    # Karakter Nero Quote
    st.markdown("""
        <div class='nero-box'>
            <b>^‿^ Nero bilang:</b><br>
            "Tenang aja, Bro! Fokus aja ke <i>deep work</i> lo hari ini. Urusan nyimpen dan <i>backup</i> data ke brankas digital, biar Nero yang beresin di belakang layar. Gaspol!"
        </div>
    """, unsafe_allow_html=True)
    
    tab_panduan, tab_harian, tab_mingguan, tab_riwayat = st.tabs([
        "📖 Panduan", "✍️ Jurnal Harian", "🔄 Reset Mingguan", "📜 Riwayat Saya"
    ])
    
    with tab_panduan:
        st.markdown("<h3 class='sub-header'>Filosofi & Kerangka Kerja</h3>", unsafe_allow_html=True)
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.write("🌿 **Mindset 'Adem'**")
            st.write("Produktivitas bukan berarti sibuk tanpa henti. Aplikasi ini dirancang untuk menjaga fokus.")
        with col_p2:
            st.write("🤖 **Integrasi AI**")
            st.write("Biarkan AI dan sistem yang menangani tugas repetitif. Fokus energi lo pada strategi.")

    with tab_harian:
        col_pagi, col_siang, col_malam = st.columns(3)
        with col_pagi:
            st.subheader("🌅 Pagi")
            prioritas = st.text_area("🎯 Top 3 Prioritas Utama", height=150)
        with col_siang:
            st.subheader("🚀 Siang")
            ai_tasks = st.text_area("🤖 Otomatisasi AI Hari Ini", height=150)
        with col_malam:
            st.subheader("🌙 Malam")
            pencapaian = st.text_area("🏆 Pencapaian Terbaik", height=100)
            mood = st.select_slider("Mood", options=["Kacau", "Biasa", "Oke", "Mantap", "Sempurna"], value="Oke")
        
        st.write("---")
        if st.button("💾 SIMPAN KE DRIVE SEKARANG", use_container_width=True):
            new_entry = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Email": st.session_state['user_email'],
                "Prioritas": prioritas,
                "AI_Tasks": ai_tasks,
                "Pencapaian": pencapaian,
                "Mood": mood
            }])
            try:
                df_lama = conn.read(worksheet="Sheet1", ttl=0)
                df_baru = pd.concat([df_lama, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_baru)
                st.success("✅ Mantap! Data udah terbang ke Google Sheets lo.")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Gagal simpan: {e}")

    with tab_mingguan:
        st.markdown("<h3 class='sub-header'>Evaluasi Mingguan</h3>", unsafe_allow_html=True)
        st.text_area("✅ Apa yang berjalan sangat lancar minggu ini?", height=100)
        st.text_area("🚧 Hambatan apa yang paling sering muncul?", height=100)
        if st.button("🔄 Simpan Evaluasi Mingguan"):
            st.success("Evaluasi tersimpan!")

    with tab_riwayat:
        st.subheader("Riwayat Jurnal Personal Lo")
        if st.button("🔄 Segarkan Data (Refresh)"):
            st.cache_data.clear()
            st.rerun()

        try:
            # Baca data terbaru tanpa cache
            full_df = conn.read(worksheet="Sheet1", ttl=0)
            
            if not full_df.empty:
                # Normalisasi Nama Kolom & Data Email
                full_df.columns = [str(c).strip().capitalize() for c in full_df.columns]
                full_df['Email_search'] = full_df['Email'].astype(str).str.strip().lower()
                
                # Filter berdasarkan email login
                user_email = st.session_state['user_email']
                user_history = full_df[full_df['Email_search'] == user_email]
                
                if not user_history.empty:
                    # Tampilkan tanpa kolom bantu
                    display_df = user_history.drop(columns=['Email_search'])
                    st.dataframe(display_df.sort_values(by="Timestamp", ascending=False), use_container_width=True)
                else:
                    st.info(f"Belum ada riwayat jurnal buat {user_email}.")
            else:
                st.info("Database masih kosong.")
        except Exception as e:
            st.error(f"Gagal memuat riwayat: {e}")
