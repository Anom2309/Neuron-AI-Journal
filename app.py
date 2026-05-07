import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Konfigurasi (Tetap Aman)
st.set_page_config(page_title="Daily Workflow - Neuron AI", page_icon="🌱", layout="centered")
conn = st.connection("gsheets", type=GSheetsConnection)

# CSS Custom
st.markdown("""
    <style>
    .stApp { background-color: #f0f7f4; color: #2d4035; }
    .stButton>button { background-color: #9CAF88; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .nero-box { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ffb703; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# 2. Login Logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = ""

if not st.session_state['logged_in']:
    st.title("🌱 Neuron AI Login")
    email_input = st.text_input("Alamat Email")
    if st.button("Masuk / Daftar", key="btn_login"): # Tambah key unik
        if email_input:
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email_input.strip().lower()
            st.rerun()
        else:
            st.warning("Isi email dulu, Bro!")

else:
    # 3. Header Utama
    cols = st.columns([4, 1])
    with cols[0]:
        st.title("Daily Workflow Book 🚀")
        st.write(f"User: **{st.session_state['user_email']}**")
    with cols[1]:
        # KUNCI PERBAIKAN: Tambah key="btn_logout_top" agar tidak duplikat ID
        if st.button("Logout", key="btn_logout_top"):
            st.session_state.clear()
            st.rerun()

    st.markdown("<div class='nero-box'><b>^‿^ Nero:</b> Ayo sikat progres hari ini!</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🌅 Pagi", "🚀 Siang", "🌙 Malam", "📜 Riwayat"])
    
    with tab1:
        st.subheader("Top 3 Prioritas")
        d1 = st.text_input("Prioritas 1", key="in_p1")
        d2 = st.text_input("Prioritas 2", key="in_p2")
        d3 = st.text_input("Prioritas 3", key="in_p3")
        
    with tab2:
        st.subheader("Otomatisasi AI")
        ai_tasks = st.text_area("Ide otomatisasi...", height=150, key="in_ai")
        
    with tab3:
        st.subheader("Refleksi Malam")
        achieve = st.text_input("Pencapaian", key="in_achieve")
        mood_val = st.slider("Mood (1-5)", 1, 5, 3, key="in_mood")
        
        # Tambah key unik buat tombol simpan
        if st.button("Simpan Jurnal Hari Ini", key="btn_save_jurnal"):
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
                st.success("✅ Tersimpan!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Gagal simpan: {e}")

    with tab4:
        st.subheader("Riwayat Jurnal Personal Lo")
        # Tambah key unik buat tombol refresh
        if st.button("🔄 Paksa Muat Ulang", key="btn_refresh_data"):
            st.cache_data.clear()
            st.rerun()
            
        try:
            df_full = conn.read(worksheet="Sheet1", ttl=0)
            if df_full is not None and not df_full.empty:
                user_email = str(st.session_state['user_email']).strip().lower()
                # Cari kolom email secara case-insensitive
                target_col = [c for c in df_full.columns if 'email' in str(c).lower()]
                
                if target_col:
                    col_key = target_col[0]
                    mask = df_full[col_key].astype(str).str.strip().lower() == user_email
                    user_df = df_full[mask].copy()
                    
                    if not user_df.empty:
                        st.dataframe(user_df.sort_values(by=user_df.columns[0], ascending=False), use_container_width=True)
                    else:
                        st.info("Belum ada data.")
                else:
                    st.dataframe(df_full) # Fallback nampilin semua kalau kolom email ga ketemu
            else:
                st.info("Sheets kosong.")
        except Exception as e:
            st.error(f"Error: {e}")
