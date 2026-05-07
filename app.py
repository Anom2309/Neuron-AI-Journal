import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Konfigurasi Halaman & Tema (Tetap Sesuai Request)
st.set_page_config(page_title="Daily Workflow - Neuron AI", page_icon="🌱", layout="centered")

# Koneksi Database
conn = st.connection("gsheets", type=GSheetsConnection)

# Injeksi CSS Custom (Tetap Sesuai Request)
st.markdown("""
    <style>
    .stApp { background-color: #f0f7f4; color: #2d4035; }
    .stButton>button { background-color: #9CAF88; color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; }
    .stButton>button:hover { background-color: #7b8f6b; }
    .nero-box { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ffb703; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 25px; font-size: 1.1em; }
    </style>
""", unsafe_allow_html=True)

# 2. Sistem Autentikasi
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = ""

if not st.session_state['logged_in']:
    st.title("🌱 Selamat Datang di Neuron AI")
    st.write("Silakan masukkan email lo untuk mengakses Daily Workflow Book.")
    
    email_input = st.text_input("Alamat Email")
    if st.button("Masuk / Daftar"):
        if email_input:
            st.session_state['logged_in'] = True
            # Simpan email dalam format bersih (kecil semua, tanpa spasi)
            st.session_state['user_email'] = email_input.strip().lower()
            st.rerun()
        else:
            st.warning("Bro, isi emailnya dulu dong!")

# 3. Dashboard Aplikasi Utama
else:
    cols = st.columns([4, 1])
    with cols[0]:
        st.title("Daily Workflow Book 🚀")
        st.write(f"Sesi milik: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    st.markdown(f"""
        <div class='nero-box'>
            <b>^‿^ Nero bilang:</b><br>
            "Satu langkah kecil hari ini, fondasi besar buat masa depan! Yuk, kita sikat, Bro!"
        </div>
    """, unsafe_allow_html=True)
    
    # 4. Tab Navigasi (GW TAMBAHKAN TAB RIWAYAT DI AKHIR)
    tab1, tab2, tab3, tab4 = st.tabs(["🌅 Pagi (Persiapan)", "🚀 Siang (Eksekusi)", "🌙 Malam (Refleksi)", "📜 Riwayat"])
    
    with tab1:
        st.subheader("Top 3 Prioritas Utama Hari Ini")
        st.write("Fokuskan pikiran. Apa yang paling penting?")
        st.checkbox("Prioritas 1", key="p1")
        det1 = st.text_input("Detail Prioritas 1", label_visibility="collapsed", key="d1")
        
        st.checkbox("Prioritas 2", key="p2")
        det2 = st.text_input("Detail Prioritas 2", label_visibility="collapsed", key="d2")
        
        st.checkbox("Prioritas 3", key="p3")
        det3 = st.text_input("Detail Prioritas 3", label_visibility="collapsed", key="d3")
        
    with tab2:
        st.subheader("Otomatisasi & Delegasi AI")
        st.write("Bagian mana dari tugas hari ini yang bisa diserahkan ke prompt atau sistem otomatisasi?")
        ai_tasks = st.text_area("Catat ide otomatisasi di sini...", height=150, key="ai")
        
    with tab3:
        st.subheader("Evaluasi Diri & Mood")
        st.write("Pencapaian Terbaik Hari Ini:")
        achieve = st.text_input("Hal yang bikin lo bangga hari ini", label_visibility="collapsed", key="achieve")
        
        st.write("Tingkat Kepuasan Hari Ini:")
        mood_val = st.slider("Dari 1 (Kacau) sampai 5 (Sempurna), gimana hari lo?", 1, 5, 3)
        
        st.write("---")
        if st.button("Simpan Jurnal Hari Ini"):
            # Gabungkan detail prioritas menjadi satu teks untuk disimpan ke Sheets
            prioritas_gabungan = f"1. {det1} | 2. {det2} | 3. {det3}"
            
            new_entry = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Email": st.session_state['user_email'],
                "Prioritas": prioritas_gabungan,
                "AI_Tasks": ai_tasks,
                "Pencapaian": achieve,
                "Mood": mood_val
            }])
            
            try:
                df_lama = conn.read(worksheet="Sheet1", ttl=0)
                df_baru = pd.concat([df_lama, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_baru)
                st.success("Mantap! Data jurnal hari ini berhasil disimpan ke database. Istirahat yang cukup, Bro!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Waduh, gagal nyimpen Bro. Masalahnya: {e}")

    # --- TAB BARU: RIWAYAT ---
    with tab4:
        st.subheader("Riwayat Jurnal Lo")
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
            
        try:
            df_riwayat = conn.read(worksheet="Sheet1", ttl=0)
            if df_riwayat is not None and not df_riwayat.empty:
                # Bersihkan kolom Email di dataframe buat filter
                df_riwayat.columns = [str(c).strip().capitalize() for c in df_riwayat.columns]
                df_riwayat['Email_Clean'] = df_riwayat['Email'].astype(str).str.strip().lower()
                
                # Filter berdasarkan email user yang login
                user_mail = st.session_state['user_email']
                user_history = df_riwayat[df_riwayat['Email_Clean'] == user_mail].copy()
                
                if not user_history.empty:
                    # Buang kolom bantuan & tampilkan
                    final_display = user_history.drop(columns=['Email_Clean'])
                    st.dataframe(final_display.sort_values(by="Timestamp", ascending=False), use_container_width=True)
                else:
                    st.info(f"Belum ada riwayat buat {user_mail}. Yuk nulis jurnal dulu!")
            else:
                st.info("Database masih kosong, Bro.")
        except Exception as e:
            st.write("Lagi narik data... kalau lama klik Refresh ya.")
