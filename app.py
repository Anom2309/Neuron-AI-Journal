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
# Pastikan URL Spreadsheet lo sudah ada di Secrets Streamlit Cloud
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. CSS CUSTOM (Estetika Sage Green) ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f7f4; color: #2d4035; }
    .stButton>button { 
        background-color: #9CAF88; 
        color: white; 
        border-radius: 8px; 
        border: none; 
        padding: 10px 24px; 
        font-weight: bold; 
        width: 100%;
    }
    .stButton>button:hover { background-color: #7b8f6b; }
    .nero-box { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #ffb703; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
        margin-bottom: 25px; 
        font-size: 1.1em;
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
    st.write("Masukkan email untuk sinkronisasi data 30 hari lo.")
    email_input = st.text_input("Alamat Email")
    if st.button("Masuk"):
        if email_input:
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email_input
            st.rerun()
        else:
            st.warning("Emailnya diisi dulu ya, Bro!")

# --- 5. DASHBOARD UTAMA ---
else:
    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown(f"<h1 class='header-title'>Neuro Nada Daily Workflow 🚀</h1>", unsafe_allow_html=True)
        st.write(f"User aktif: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    # Karakter Nero Quote
    st.markdown("""
        <div class='nero-box'>
            <b>^‿^ Nero bilang:</b> "Tenang aja, Bro! Fokus aja ke <i>deep work</i> lo hari ini. Urusan nyimpen dan <i>backup</i> data ke brankas digital, biar Nero yang beresin di belakang layar. Gaspol!"
        </div>
    """, unsafe_allow_html=True)
    
    # Navigasi Tab
    tab_panduan, tab_harian, tab_mingguan, tab_riwayat = st.tabs(["📖 Panduan", "✍️ Jurnal Harian", "🔄 Reset Mingguan", "📜 Riwayat Saya"])
    
    with tab_panduan:
        st.markdown("<h3 class='sub-header'>Filosofi & Kerangka Kerja</h3>", unsafe_allow_html=True)
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.write("🌿 **Mindset 'Adem'**")
            st.write("Aplikasi ini dirancang untuk menurunkan ketegangan pikiran dan menjaga fokus melalui ketenangan visual.")
            st.write("🤖 **Integrasi AI**")
            st.write("Fokuskan energi pada strategi krusial. Biarkan AI menangani tugas repetitif.")
        with col_p2:
            st.write("✨ **Tentang Nero**")
            st.write("Nero adalah personifikasi neuron otak lo yang ceria, siap nemenin progres harian lo.")

    with tab_harian:
        col_pagi, col_siang, col_malam = st.columns(3)
        with col_pagi:
            st.subheader("🌅 Pagi")
            prioritas = st.text_area("Top 3 Prioritas Utama", height=150)
        with col_siang:
            st.subheader("🚀 Siang")
            ai_tasks = st.text_area("Otomatisasi AI hari ini", height=150)
        with col_malam:
            st.subheader("🌙 Malam")
            pencapaian = st.text_area("Pencapaian terbaik", height=100)
            mood = st.select_slider("Mood", options=["Kacau", "Biasa", "Oke", "Mantap", "Sempurna"], value="Oke")
        
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
                df_lama = conn.read(worksheet="Sheet1")
                df_baru = pd.concat([df_lama, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_baru)
                st.success("✅ Berhasil disimpan ke Google Sheets!")
            except:
                st.error("Cek koneksi atau Secrets URL lo, Bro!")

    with tab_mingguan:
        st.markdown("<h3 class='sub-header'>Evaluasi Mingguan</h3>", unsafe_allow_html=True)
        eval_lancar = st.text_area("Apa yang berjalan sangat lancar minggu ini?")
        eval_hambat = st.text_area("Hambatan apa yang paling sering muncul?")
        if st.button("🔄 Simpan Evaluasi"):
            st.success("Evaluasi mingguan tersimpan!")

    with tab_riwayat:
        st.subheader("Jurnal lama lo")
        try:
            # Kita paksa baca ulang data terbaru dari Sheets
            full_df = conn.read(worksheet="Sheet1", ttl=0) # ttl=0 artinya jangan pakai cache, baca asli!
            
            # Pastikan email dibandingkan dengan benar (case-insensitive & tanpa spasi)
            user_email_now = st.session_state['user_email'].strip().lower()
            full_df['Email'] = full_df['Email'].astype(str).str.strip().lower()
            
            user_history = full_df[full_df['Email'] == user_email_now]
            
            if not user_history.empty:
                st.dataframe(user_history.sort_values(by="Timestamp", ascending=False), use_container_width=True)
            else:
                st.info(f"Data untuk {user_email_now} belum ada di Sheets. Coba simpan data baru dulu, Bro!")
        except Exception as e:
            st.error(f"Gagal narik data: {e}")
