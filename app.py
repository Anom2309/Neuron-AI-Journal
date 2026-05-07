import streamlit as st

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada - Daily Workflow", 
    page_icon="🌱", 
    layout="wide"
)

# --- 2. CSS CUSTOM (Estetika Adem/Sage Green) ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f7f4; color: #2d4035; }
    .stButton>button { background-color: #9CAF88; color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; }
    .stButton>button:hover { background-color: #7b8f6b; }
    .nero-box { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #ffb703; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 25px; font-size: 1.1em; }
    .header-title { color: #1D3557; font-family: sans-serif; font-weight: 700; }
    .sub-header { color: #9CAF88; font-weight: bold; border-bottom: 2px solid #9CAF88; padding-bottom: 10px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SISTEM LOGIN (Email-Based Signup) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_email'] = ""

if not st.session_state['logged_in']:
    st.markdown("<h1 class='header-title'>🌱 Neuro Nada Daily Workflow</h1>", unsafe_allow_html=True)
    st.write("Silakan masukkan email lo untuk mengakses jurnal produktivitas 30 hari ini.")
    
    email_input = st.text_input("Alamat Email")
    if st.button("Masuk / Daftar"):
        if email_input:
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email_input
            st.rerun()
        else:
            st.warning("Bro, isi emailnya dulu dong biar bisa masuk!")

# --- 4. DASHBOARD UTAMA (Setelah Login) ---
else:
    # Header & Tombol Logout
    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("<h1 class='header-title'>Neuro Nada Daily Workflow 🚀</h1>", unsafe_allow_html=True)
        st.write(f"Sesi milik: **{st.session_state['user_email']}**")
    with cols[1]:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    # Karakter Nero Quote
    st.markdown("""
        <div class='nero-box'>
            <b>^‿^ Nero bilang:</b><br>
            "Satu langkah kecil hari ini, fondasi besar buat masa depan! Yuk, optimasi alur kerja lo dengan Neuro Nada, Bro!"
        </div>
    """, unsafe_allow_html=True)
    
    # --- 5. GABUNGAN KONTEN: Panduan (Slide) + Jurnal (App) ---
    tab_panduan, tab_harian, tab_mingguan = st.tabs(["📖 Panduan Neuro Nada", "✍️ Jurnal Harian", "🔄 Reset Mingguan"])
    
    # TAB 1: Panduan (Diambil dari desain presentasi)
    with tab_panduan:
        st.markdown("<h3 class='sub-header'>Filosofi & Kerangka Kerja</h3>", unsafe_allow_html=True)
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.write("🌿 **Mindset 'Adem'**")
            st.write("Produktivitas bukan berarti sibuk tanpa henti. Aplikasi ini dirancang untuk menurunkan ketegangan pikiran dan menjaga fokus.")
            st.write("🤖 **Integrasi AI**")
            st.write("Fokuskan energi pada strategi krusial. Biarkan AI dan sistem yang menangani tugas repetitif.")
        with col_p2:
            st.write("✨ **Tentang Nero**")
            st.write("Nero adalah personifikasi dari neuron otak lo. Dia hadir di sini buat ngasih pengingat prioritas pagi, ide otomatisasi siang hari, dan teman refleksi di malam hari.")
        
        st.info("💡 Tips: Gunakan tab 'Jurnal Harian' setiap hari, dan tab 'Reset Mingguan' setiap hari ke-7.")

    # TAB 2: Input Jurnal Harian
    with tab_harian:
        col_pagi, col_siang, col_malam = st.columns(3)
        
        with col_pagi:
            st.subheader("🌅 Pagi (Persiapan)")
            st.write("Top 3 Prioritas Utama Hari Ini:")
            st.checkbox("Prioritas 1", key="p1")
            st.text_input("Detail Prioritas 1", label_visibility="collapsed")
            st.checkbox("Prioritas 2", key="p2")
            st.text_input("Detail Prioritas 2", label_visibility="collapsed")
            st.checkbox("Prioritas 3", key="p3")
            st.text_input("Detail Prioritas 3", label_visibility="collapsed")
            
        with col_siang:
            st.subheader("🚀 Siang (Eksekusi)")
            st.write("Otomatisasi Neural (AI):")
            st.text_area("Tugas apa yang lo delegasikan ke AI hari ini?", height=130)
            
        with col_malam:
            st.subheader("🌙 Malam (Refleksi)")
            st.write("Pencapaian Terbaik:")
            st.text_input("Hal yang bikin bangga hari ini", label_visibility="collapsed")
            st.write("Tingkat Kepuasan:")
            st.slider("Mood hari ini (1 = Kacau, 5 = Sempurna)", 1, 5, 3)
        
        st.write("---")
        if st.button("💾 Simpan Jurnal Hari Ini", use_container_width=True):
            st.success("Mantap! Jurnal harian lo berhasil disimpan. Istirahat yang cukup, Bro!")

    # TAB 3: Evaluasi Mingguan (Diambil dari kerangka buku PDF)
    with tab_mingguan:
        st.markdown("<h3 class='sub-header'>Evaluasi Mingguan & Kalibrasi Sistem</h3>", unsafe_allow_html=True)
        st.write("Luangkan waktu sejenak untuk me-review 7 hari ke belakang.")
        
        st.text_area("✅ Apa yang berjalan sangat lancar minggu ini?")
        st.text_area("🚧 Hambatan apa yang paling sering muncul?")
        st.text_area("🤖 Sistem AI/Otomatisasi apa yang mau ditambah atau diperbaiki minggu depan?")
        
        if st.button("🔄 Simpan Evaluasi Mingguan"):
            st.success("Evaluasi mingguan tersimpan! Karakter Nero bangga banget sama progres konsisten lo!")
