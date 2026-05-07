import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Neuro Nada - Daily Workflow", page_icon="🌱", layout="wide")

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
    cols = st.columns([4, 1])
    with cols[0]:
        st.title("Neuro Nada Daily Workflow 🚀")
        st.write(f"Sesi Aktif: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    tab_harian, tab_riwayat, tab_debug = st.tabs(["✍️ Jurnal", "📜 Riwayat", "🔍 Mode Detektif"])

    with tab_harian:
        col1, col2, col3 = st.columns(3)
        with col1: prioritas = st.text_area("🎯 Prioritas", height=150)
        with col2: ai_tasks = st.text_area("🤖 Delegasi AI", height=150)
        with col3: 
            pencapaian = st.text_area("🏆 Pencapaian", height=100)
            mood = st.select_slider("Mood", options=["Kacau", "Biasa", "Oke", "Mantap", "Sempurna"], value="Oke")
        
        if st.button("💾 SIMPAN KE DRIVE"):
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
                st.success("✅ Berhasil Simpan!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Gagal Simpan: {e}")

    with tab_riwayat:
        st.subheader("Riwayat Personal")
        try:
            df = conn.read(worksheet="Sheet1", ttl=0)
            if df is not None and not df.empty:
                # Bersihkan kolom secara paksa
                df.columns = [str(c).strip().lower() for c in df.columns]
                user_email = str(st.session_state['user_email']).strip().lower()
                
                # Filter menggunakan metode query agar lebih aman
                if 'email' in df.columns:
                    df['email'] = df['email'].astype(str).str.strip().lower()
                    user_history = df[df['email'] == user_email]
                    
                    if not user_history.empty:
                        st.dataframe(user_history, use_container_width=True)
                    else:
                        st.warning(f"Data buat {user_email} nggak ketemu. Cek tab Detektif, Bro!")
                else:
                    st.error("Kolom 'Email' nggak deteksi. Cek tab Detektif!")
            else:
                st.info("Sheets masih kosong.")
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_debug:
        st.subheader("🔍 Mode Detektif (Cek Isi Asli Sheets)")
        st.write("Tabel di bawah ini nampilin **SEMUA** data yang ada di Google Sheets tanpa filter:")
        try:
            raw_df = conn.read(worksheet="Sheet1", ttl=0)
            st.write("Nama Kolom yang terdeteksi:", list(raw_df.columns))
            st.dataframe(raw_df)
        except Exception as e:
            st.error(f"Gagal baca Sheets: {e}")
