import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px # Untuk grafik yang lebih cantik

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada - Daily Journal", 
    page_icon="🌱", 
    layout="wide"
)

# --- 2. KONEKSI DATABASE (Google Sheets) ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. CSS CUSTOM (Kembali ke Estetika Pertama: Soft Sage Green) ---
st.markdown("""
    <style>
    /* Background Adem */
    .stApp { background-color: #f0f7f4; color: #2d4035; }
    
    /* Tombol Utama */
    .stButton>button { 
        background-color: #9CAF88; 
        color: white; 
        border-radius: 12px; 
        border: none; 
        padding: 12px 24px; 
        font-weight: bold; 
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #7b8f6b; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    
    /* Nero Card Style */
    .nero-card { 
        background-color: white; 
        padding: 25px; 
        border-radius: 20px; 
        border-left: 8px solid #ffb703; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
        margin-bottom: 30px;
    }
    
    /* Header Styles */
    .header-text { color: #1D3557; font-family: 'Poppins', sans-serif; font-weight: 700; }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown("<h1 class='header-text'>🌱 Neuro Nada Daily Journal</h1>", unsafe_allow_html=True)
    st.write("Masuk untuk sinkronisasi jurnal dan analisis progres lo.")
    email_input = st.text_input("Email lo:")
    if st.button("Gas Masuk"):
        if email_input:
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email_input
            st.rerun()
else:
    # Sidebar untuk Navigasi
    st.sidebar.markdown(f"### 👤 {st.session_state['user_email']}")
    menu = st.sidebar.radio("Navigasi", ["✍️ Tulis Jurnal", "📊 Ringkasan & Analisis", "📖 Panduan Nero"])
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

    # DASHBOARD UTAMA
    if menu == "✍️ Tulis Jurnal":
        st.markdown("<h1 class='header-text'>Catat Progres Hari Ini 🚀</h1>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class='nero-card'>
                <b>^‿^ Nero:</b> "Setiap baris yang lo tulis adalah investasi buat masa depan. Fokus ke <i>deep work</i>, sisanya biar Nero yang jaga."
            </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            prioritas = st.text_area("🎯 3 Prioritas Utama & Action Items", height=150, placeholder="Apa yang harus selesai hari ini?")
            ai_tasks = st.text_area("🤖 Delegasi AI", height=100, placeholder="Tugas apa yang lo serahin ke AI hari ini?")
        with col_b:
            pencapaian = st.text_area("🏆 Pencapaian Terbaik", height=150, placeholder="Hal apa yang bikin lo bangga hari ini?")
            mood_val = st.select_slider("🌈 Mood Hari Ini", options=["Kacau", "Biasa", "Oke", "Mantap", "Sempurna"], value="Oke")

        if st.button("💾 SIMPAN KE DRIVE"):
            new_entry = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Email": st.session_state['user_email'],
                "Prioritas": prioritas,
                "AI_Tasks": ai_tasks,
                "Pencapaian": pencapaian,
                "Mood": mood_val
            }])
            try:
                df_lama = conn.read(worksheet="Sheet1")
                df_baru = pd.concat([df_lama, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_baru)
                st.success("✅ Tersimpan! Data lo udah aman di Google Sheets.")
            except:
                st.error("Gagal koneksi. Cek Secrets URL lo, Bro!")

    elif menu == "📊 Ringkasan & Analisis":
        st.markdown("<h1 class='header-text'>Ringkasan Neuro Nada lo 📊</h1>", unsafe_allow_html=True)
        
        try:
            df = conn.read(worksheet="Sheet1")
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            user_df = df[df['Email'] == st.session_state['user_email']].sort_values('Timestamp', ascending=False)
            
            if not user_df.empty:
                # Perhitungan Periode
                now = datetime.now()
                df_week = user_df[user_df['Timestamp'] > (now - timedelta(days=7))]
                df_month = user_df[user_df['Timestamp'] > (now - timedelta(days=30))]
                df_year = user_df[user_df['Timestamp'] > (now - timedelta(days=365))]

                # Tampilan Metrik Ringkasan
                m1, m2, m3 = st.columns(3)
                m1.metric("Minggu Ini", f"{len(df_week)} Jurnal")
                m2.metric("Bulan Ini", f"{len(df_month)} Jurnal")
                m3.metric("Tahun Ini", f"{len(df_year)} Jurnal")

                st.write("---")
                
                # Visualisasi Mood
                st.subheader("📈 Tren Mood & Produktivitas")
                mood_map = {"Kacau": 1, "Biasa": 2, "Oke": 3, "Mantap": 4, "Sempurna": 5}
                user_df['Mood_Score'] = user_df['Mood'].map(mood_map)
                
                fig = px.line(user_df, x='Timestamp', y='Mood_Score', title='Fluktuasi Mood lo', 
                              markers=True, color_discrete_sequence=['#9CAF88'])
                fig.update_layout(yaxis=dict(tickvals=[1,2,3,4,5], ticktext=["Kacau", "Biasa", "Oke", "Mantap", "Sempurna"]))
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("📜 Riwayat Jurnal Lengkap")
                st.dataframe(user_df[['Timestamp', 'Prioritas', 'AI_Tasks', 'Pencapaian', 'Mood']], use_container_width=True)
                
            else:
                st.info("Belum ada data untuk dianalisis. Mulai menjurnal hari ini, Bro!")
        except:
            st.error("Gagal memuat data dari Spreadsheet.")

    elif menu == "📖 Panduan Nero":
        st.markdown("<h2 class='header-text'>Filosofi Neuro Nada</h2>", unsafe_allow_html=True)
        st.write("Selamat datang di ekosistem produktivitas yang mengutamakan ketenangan.")
        col1, col2 = st.columns(2)
        with col1:
            st.info("💡 **Tips Mingguan:** Cek tab Analisis setiap hari Minggu malam untuk kalibrasi sistem lo.")
        with col2:
            st.success("🤖 **Tips AI:** Jangan serahin semua ke AI. Pakai AI buat tugas administratif, simpan otak lo buat tugas kreatif.")
