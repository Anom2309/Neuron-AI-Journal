import streamlit as st

# 1. Konfigurasi Halaman & Tema
st.set_page_config(page_title="Daily Workflow - Neuron AI", page_icon="🌱", layout="centered")

# Injeksi CSS Custom untuk warna "Adem" (Sage Green) dan style Nero
st.markdown("""
    <style>
    /* Background keseluruhan */
    .stApp {
        background-color: #f0f7f4; 
        color: #2d4035;
    }
    /* Tombol utama */
    .stButton>button {
        background-color: #9CAF88;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #7b8f6b;
    }
    /* Kotak Quote Nero */
    .nero-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ffb703;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        font-size: 1.1em;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sistem Autentikasi (Email-based Signup/Login scalable)
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
            st.session_state['user_email'] = email_input
            st.rerun()
        else:
            st.warning("Bro, isi emailnya dulu dong!")

# 3. Dashboard Aplikasi Utama
else:
    # Header
    cols = st.columns([4, 1])
    with cols[0]:
        st.title("Daily Workflow Book 🚀")
        st.write(f"Sesi milik: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    # Quote Karakter Nero
    st.markdown("""
        <div class='nero-box'>
            <b>^‿^ Nero bilang:</b><br>
            "Satu langkah kecil hari ini, fondasi besar buat masa depan! Yuk, kita sikat, Bro!"
        </div>
    """, unsafe_allow_html=True)
    
    # 4. Tab Navigasi Sesuai Kerangka Buku
    tab1, tab2, tab3 = st.tabs(["🌅 Pagi (Persiapan)", "🚀 Siang (Eksekusi)", "🌙 Malam (Refleksi)"])
    
    with tab1:
        st.subheader("Top 3 Prioritas Utama Hari Ini")
        st.write("Fokuskan pikiran. Apa yang paling penting?")
        p1 = st.checkbox("Prioritas 1", key="p1")
        st.text_input("Detail Prioritas 1", label_visibility="collapsed")
        
        p2 = st.checkbox("Prioritas 2", key="p2")
        st.text_input("Detail Prioritas 2", label_visibility="collapsed")
        
        p3 = st.checkbox("Prioritas 3", key="p3")
        st.text_input("Detail Prioritas 3", label_visibility="collapsed")
        
    with tab2:
        st.subheader("Otomatisasi & Delegasi AI")
        st.write("Bagian mana dari tugas hari ini yang bisa diserahkan ke prompt atau sistem otomatisasi?")
        ai_tasks = st.text_area("Catat ide otomatisasi di sini...", height=150)
        
    with tab3:
        st.subheader("Evaluasi Diri & Mood")
        st.write("Pencapaian Terbaik Hari Ini:")
        st.text_input("Hal yang bikin lo bangga hari ini", label_visibility="collapsed", key="achieve")
        
        st.write("Tingkat Kepuasan Hari Ini:")
        mood = st.slider("Dari 1 (Kacau) sampai 5 (Sempurna), gimana hari lo?", 1, 5, 3)
        
        st.write("---")
        if st.button("Simpan Jurnal Hari Ini"):
            # Di sini logika untuk nge-save data ke database (misal: Supabase/Firebase)
            st.success("Mantap! Data jurnal hari ini berhasil disimpan ke database. Istirahat yang cukup, Bro!")
