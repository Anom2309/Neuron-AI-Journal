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
    }
    .sub-header { color: #9CAF88; font-weight: bold; border-bottom: 2px solid #9CAF88; padding-bottom: 10px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_email'] = ""

if not st.session_state['logged_in']:
    st.markdown("<h1>🌱 Neuro Nada Journal</h1>", unsafe_allow_html=True)
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
        st.markdown(f"<h1>Neuro Nada Daily Workflow 🚀</h1>", unsafe_allow_html=True)
        st.write(f"User aktif: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown("""
        <div class='nero-box'>
            <b>^‿^ Nero:</b> "Data lo bakal langsung masuk ke spreadsheet <b>14bqio8D...</b> secara otomatis!"
        </div>
    """, unsafe_allow_html=True)

    # Tabs Konten
    tab1, tab2 = st.tabs(["✍️ Tulis Jurnal", "📜 Riwayat Saya"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("🌅 Persiapan & Eksekusi")
            prioritas = st.text_area("Top 3 Prioritas & Action Items", height=100)
            ai_tasks = st.text_area("Ide Otomatisasi AI hari ini", height=100)
        with col_b:
            st.subheader("🌙 Refleksi")
            pencapaian = st.text_area("Pencapaian terbaik hari ini", height=100)
            mood = st.select_slider("Gimana perasaan lo hari ini?", 
                                    options=["Kacau", "Biasa", "Oke", "Mantap", "Sempurna"])

        if st.button("💾 SIMPAN KE DRIVE SEKARANG"):
            # Data baru yang akan dikirim
            new_entry = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Email": st.session_state['user_email'],
                "Prioritas": prioritas,
                "AI_Tasks": ai_tasks,
                "Pencapaian": pencapaian,
                "Mood": mood
            }])

            try:
                # Membaca data lama, menggabungkan, lalu update
                df_lama = conn.read(worksheet="Sheet1")
                df_baru = pd.concat([df_lama, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_baru)
                st.success("✅ Berhasil! Data sudah tersimpan permanen di Google Sheets lo.")
            except Exception as e:
                st.error("Gagal nyambung ke Sheets. Cek apakah link di Secrets sudah benar.")

    with tab2:
        st.subheader("Jurnal yang Pernah Lo Tulis")
        try:
            full_df = conn.read(worksheet="Sheet1")
            # Filter hanya data milik user yang sedang login
            user_history = full_df[full_df['Email'] == st.session_state['user_email']]
            if not user_history.empty:
                st.dataframe(user_history.sort_values(by="Timestamp", ascending=False))
            else:
                st.info("Belum ada riwayat jurnal buat email ini.")
        except:
            st.write("Belum ada data di spreadsheet.")
