import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- KONFIGURASI HALAMAN DAN CSS KUSTOM ---
st.set_page_config(
    page_title="Sistem Pakar Penilaian Kualitas Air Tambak Ikan",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Kustom untuk tema perairan yang modern
st.markdown("""
<style>
    /* VARIABEL WARNA TEMA AIR */
    :root {
        --primary-blue: #0A3D62;
        --secondary-blue: #1E6F9F;
        --accent-teal: #2ECC71;
        --accent-aqua: #00CEC9;
        --light-bg: #F7F9FC;
        --dark-bg: #0A1A2F;
        --text-dark: #2C3E50;
        --text-light: #FFFFFF;
        --success: #27AE60;
        --warning: #F39C12;
        --danger: #E74C3C;
        --border-radius: 12px;
        --box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        --transition: all 0.3s ease;
    }
    
    /* RESET DAN UTILITAS */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* HEADER DAN JUDUL */
    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        padding: 2rem 1.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        color: var(--text-light);
        box-shadow: var(--box-shadow);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M0,0 L100,0 L100,100 Z" fill="rgba(255,255,255,0.1)"/></svg>');
        background-size: cover;
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }
    
    /* SIDEBAR */
    .sidebar-content {
        background: linear-gradient(180deg, var(--dark-bg) 0%, var(--primary-blue) 100%);
        padding: 2rem 1rem;
        height: 100vh;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar-title {
        color: var(--text-light);
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        text-align: center;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--accent-aqua);
    }
    
    /* KARTU (CARDS) */
    .card {
        background: var(--light-bg);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--box-shadow);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: var(--transition);
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
    }
    
    .card-title {
        color: var(--primary-blue);
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-title i {
        color: var(--accent-aqua);
    }
    
    /* METRIC CARDS */
    .metric-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-top: 4px solid var(--accent-aqua);
        transition: var(--transition);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-blue);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-dark);
        opacity: 0.8;
    }
    
    /* INPUT STYLING */
    .stSlider > div > div > div {
        background: linear-gradient(to right, var(--accent-aqua), var(--secondary-blue));
    }
    
    /* BUTTON STYLING */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-aqua) 0%, var(--secondary-blue) 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: var(--transition);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 206, 201, 0.3);
    }
    
    /* TABEL STYLING */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--box-shadow);
    }
    
    .dataframe thead {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        color: white;
    }
    
    .dataframe th {
        padding: 1rem;
        text-align: left;
        font-weight: 600;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .dataframe tr:hover {
        background-color: rgba(0, 206, 201, 0.05);
    }
    
    /* STATUS BADGES */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-baik {
        background-color: rgba(39, 174, 96, 0.15);
        color: var(--success);
    }
    
    .status-cukup {
        background-color: rgba(243, 156, 18, 0.15);
        color: var(--warning);
    }
    
    .status-buruk {
        background-color: rgba(231, 76, 60, 0.15);
        color: var(--danger);
    }
    
    /* ALERT BOXES */
    .stAlert {
        border-radius: var(--border-radius);
        padding: 1rem 1.5rem;
        border-left: 4px solid;
    }
    
    /* DIVIDER */
    .custom-divider {
        height: 1px;
        background: linear-gradient(to right, transparent, var(--accent-aqua), transparent);
        margin: 2rem 0;
    }
    
    /* FOOTER */
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: var(--text-dark);
        opacity: 0.7;
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* ANIMASI */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* RESPONSIVE */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem 1rem;
        }
        
        .header-title {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI LOAD & PELAJARI DATA (HYBRID LEARNING) ---
@st.cache_data
def load_and_learn_data(file_path):
    """
    Membaca CSV dan mempelajari statistik dasar (Mean & Std Dev)
    untuk menetapkan baseline 'Normal' bagi sistem pakar.
    """
    try:
        df = pd.read_csv(file_path)
        # Ganti nama kolom agar lebih mudah diakses
        df.columns = ['ID', 'pH', 'Temp', 'Turbidity', 'DO', 'Conductivity']
        
        # 'Belajar' dari data: Menghitung statistik deskriptif
        stats = {
            'pH': {'mean': df['pH'].mean(), 'std': df['pH'].std(), 'ideal_min': 6.5, 'ideal_max': 8.5},
            'Temp': {'mean': df['Temp'].mean(), 'std': df['Temp'].std(), 'ideal_min': 20, 'ideal_max': 32},
            'Turbidity': {'mean': df['Turbidity'].mean(), 'std': df['Turbidity'].std(), 'ideal_max': 25}, # NTU
            'DO': {'mean': df['DO'].mean(), 'std': df['DO'].std(), 'critical_min': 3, 'good_min': 5},
            'Conductivity': {'mean': df['Conductivity'].mean(), 'std': df['Conductivity'].std()}  # Diperbaiki: .mean() bukan ['mean']
        }
        return df, stats
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None, None

# --- MESIN INFERENSI (LOGIKA PAKAR) ---
def calculate_quality(ph, temp, turb, do, cond, stats):
    """
    Menghitung skor kualitas air menggunakan metode Weighted Quality Index (WQI)
    yang disesuaikan dengan aturan pakar dan statistik data historis.
    """
    scores = []
    reasons = []
    actions = []

    # 1. Penilaian pH (Bobot: 20%)
    # Aturan: Ideal 6.5-8.5, atau dalam rentang deviasi data historis
    if 6.5 <= ph <= 8.5:
        ph_score = 100
    elif (stats['pH']['mean'] - 2*stats['pH']['std']) <= ph <= (stats['pH']['mean'] + 2*stats['pH']['std']):
        ph_score = 70 # Masih oke secara historis meski agak asam/basa
        reasons.append("pH sedikit di luar ideal tapi dalam batas historis.")
    else:
        ph_score = 40
        reasons.append("pH berada di level berbahaya.")
        if ph < 6.5: actions.append("Tambahkan Kapur (Lime) untuk menaikkan pH.")
        if ph > 8.5: actions.append("Ganti sebagian air atau aplikasi bahan organik fermentasi.")

    # 2. Penilaian Temperature (Bobot: 10%)
    if 20 <= temp <= 30:
        temp_score = 100
    else:
        temp_score = 50
        reasons.append(f"Suhu {temp}°C kurang optimal untuk pertumbuhan ikan.")
        actions.append("Pantau suhu, sesuaikan kedalaman air atau peneduh jika perlu.")

    # 3. Penilaian DO / Oksigen Terlarut (Bobot: 35%) - PALING KRITIS
    if do >= 5:
        do_score = 100
    elif 3 <= do < 5:
        do_score = 60
        reasons.append("Oksigen terlarut mulai rendah.")
        actions.append("Nyalakan kincir air/aerator segera.")
    else:
        do_score = 20
        reasons.append("BAHAYA: Oksigen sangat rendah (Hipoksia).")
        actions.append("DARURAT: Nyalakan semua aerator, kurangi pakan, ganti air baru.")

    # 4. Penilaian Turbidity / Kekeruhan (Bobot: 15%)
    if turb <= 10:
        turb_score = 100
    elif turb <= 30:
        turb_score = 70
    else:
        turb_score = 40
        reasons.append("Air terlalu keruh.")
        actions.append("Cek sirkulasi, endapkan partikel lumpur, atau cek filter.")

    # 5. Penilaian Conductivity (Bobot: 20%)
    # Menggunakan statistik data karena konduktivitas sangat bergantung lokasi
    lower_limit = stats['Conductivity']['mean'] - 2*stats['Conductivity']['std']
    upper_limit = stats['Conductivity']['mean'] + 2*stats['Conductivity']['std']
    
    if lower_limit <= cond <= upper_limit:
        cond_score = 100
    else:
        cond_score = 50
        reasons.append("Konduktivitas tidak wajar dibanding data historis.")
        actions.append("Cek salinitas atau kandungan mineral air.")

    # Hitung Final Weighted Score
    final_score = (ph_score * 0.20) + (temp_score * 0.10) + (do_score * 0.35) + (turb_score * 0.15) + (cond_score * 0.20)

    # Klasifikasi Output
    if final_score >= 80:
        status = "BAIK"
        color = "#27AE60"  # Hijau
    elif 50 <= final_score < 80:
        status = "CUKUP"
        color = "#F39C12"  # Oranye
    else:
        status = "BURUK"
        color = "#E74C3C"  # Merah

    return status, final_score, reasons, actions, color

# --- FUNGSI UNTUK TAMPILAN KUSTOM ---
def render_header(title, subtitle=""):
    """Render header dengan styling kustom"""
    st.markdown(f"""
    <div class="main-header fade-in">
        <h1 class="header-title">🐟 {title}</h1>
        <p class="header-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_card(title, content, icon="📊"):
    """Render kartu dengan styling kustom"""
    with st.container():
        st.markdown(f"""
        <div class="card fade-in">
            <div class="card-title">{icon} {title}</div>
            {content}
        </div>
        """, unsafe_allow_html=True)

def render_metric_card(label, value, unit=""):
    """Render kartu metrik dengan styling kustom"""
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}{unit}</div>
        </div>
        """, unsafe_allow_html=True)

def render_divider():
    """Render pembatas kustom"""
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

def render_status_badge(status):
    """Render badge status dengan warna yang sesuai"""
    if status == "BAIK":
        badge_class = "status-baik"
    elif status == "CUKUP":
        badge_class = "status-cukup"
    else:
        badge_class = "status-buruk"
    
    st.markdown(f'<span class="status-badge {badge_class}">{status}</span>', unsafe_allow_html=True)

# --- MAIN APP ---
def main():
    # Load Data
    df, stats = load_and_learn_data("kualitas_air.csv")
    
    if df is None:
        st.warning("⚠️ Data tidak ditemukan. Pastikan file 'kualitas_air.csv' tersedia.")
        return

    # Inisialisasi Session State untuk Riwayat
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Sidebar Navigasi dengan styling kustom
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">🌊 MENU NAVIGASI</div>', unsafe_allow_html=True)
        
        menu_options = {
            "🏠 Beranda": "Dashboard utama sistem",
            "🔍 Penilaian Kualitas": "Analisis parameter air",
            "📜 Riwayat Penilaian": "Riwayat pemeriksaan",
            "ℹ️ Tentang Sistem": "Informasi sistem"
        }
        
        selected_menu = st.radio(
            "Pilih Menu:",
            list(menu_options.keys()),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Tampilkan statistik ringkas di sidebar
        if df is not None and stats is not None:
            st.markdown("### 📈 Statistik Data")
            st.info(f"Total Data: **{len(df)}** sampel")
            st.info(f"Rata-rata DO: **{stats['DO']['mean']:.1f}** mg/L")
            
        st.markdown("</div>", unsafe_allow_html=True)

    # Halaman Beranda
    if selected_menu == "🏠 Beranda":
        render_header(
            "Sistem Pakar Penilaian Kualitas Air Tambak Ikan",
            "Solusi pintar untuk monitoring kesehatan air tambak berbasis AI dan aturan pakar"
        )
        
        # Kartu Pengantar
        render_card(
            "Selamat Datang di Sistem Pakar Kami",
            """
            <div style="line-height: 1.6;">
            <p>Aplikasi ini dirancang untuk membantu petambak memantau dan menganalisis kualitas air tambak 
            secara <strong>real-time</strong> dengan akurasi tinggi.</p>
            
            <p>Dengan mengadopsi metode <strong>Rule-Based dan Data-Driven Logic (Fuzzy Logic)</strong>, 
            sistem ini menggabungkan aturan pakar berbasis pengetahuan biologis ikan dengan analisis data 
            historis untuk memberikan penilaian yang akurat dan rekomendasi tindakan tepat waktu.</p>
            </div>
            """,
            icon="🌊"
        )
        
        # Statistik Dasar dalam Grid
        st.markdown("### 📊 Statistik Data Historis")
        
        if df is not None and stats is not None:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                render_metric_card("Rata-rata pH", f"{stats['pH']['mean']:.2f}", "")
            with col2:
                render_metric_card("Rata-rata Suhu", f"{stats['Temp']['mean']:.1f}", "°C")
            with col3:
                render_metric_card("Rata-rata DO", f"{stats['DO']['mean']:.1f}", " mg/L")
            with col4:
                render_metric_card("Total Data", f"{len(df)}", " sampel")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                render_metric_card("Rata-rata Kekeruhan", f"{stats['Turbidity']['mean']:.1f}", " NTU")
            with col2:
                render_metric_card("Rata-rata Konduktivitas", f"{stats['Conductivity']['mean']:.0f}", " µS/cm")
        
        render_divider()
        
        # Fitur Utama dalam Grid
        st.markdown("### 🚀 Fitur Utama Sistem")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_card(
                "Penilaian Real-Time",
                "Analisis instan parameter air dengan algoritma cerdas untuk deteksi dini masalah.",
                icon="⚡"
            )
        
        with col2:
            render_card(
                "Rekomendasi Tindakan",
                "Saran perbaikan spesifik berdasarkan kondisi aktual dan aturan pakar.",
                icon="🎯"
            )
        
        with col3:
            render_card(
                "Riwayat Lengkap",
                "Penyimpanan dan visualisasi data historis untuk analisis tren jangka panjang.",
                icon="📈"
            )
    
    # Halaman Penilaian Kualitas
    elif selected_menu == "🔍 Penilaian Kualitas":
        render_header(
            "Analisis Kualitas Air",
            "Masukkan parameter air terkini untuk mendapatkan analisis mendalam dan rekomendasi"
        )
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            render_card(
                "Input Parameter Air",
                """
                <div style="color: #555; margin-bottom: 1rem;">
                Masukkan hasil pengukuran parameter air dari alat sensor
                </div>
                """,
                icon="📋"
            )
            
            # Container untuk input dengan padding yang pas
            with st.container():
                # Input dengan label yang lebih jelas
                st.markdown("#### 📊 Parameter Air")
                
                in_ph = st.slider(
                    "**pH** (Derajat Keasaman)", 
                    min_value=0.0, 
                    max_value=14.0, 
                    value=float(stats['pH']['mean']), 
                    step=0.1,
                    help="Skala pH 0-14, ideal untuk tambak: 6.5-8.5"
                )
                
                in_temp = st.slider(
                    "**Suhu Air** (°C)", 
                    min_value=0.0, 
                    max_value=50.0, 
                    value=float(stats['Temp']['mean']), 
                    step=0.1,
                    help="Ideal untuk ikan: 20-30°C"
                )
                
                in_do = st.slider(
                    "**Oksigen Terlarut (DO)** (mg/L)", 
                    min_value=0.0, 
                    max_value=20.0, 
                    value=float(stats['DO']['mean']), 
                    step=0.1,
                    help="Kritis untuk ikan: <3mg/L berbahaya, >5mg/L ideal"
                )
                
                in_turb = st.slider(
                    "**Kekeruhan (Turbidity)** (NTU)", 
                    min_value=0.0, 
                    max_value=100.0, 
                    value=float(stats['Turbidity']['mean']), 
                    step=0.1,
                    help="Semakin tinggi nilai NTU, semakin keruh air"
                )
                
                in_cond = st.slider(
                    "**Konduktivitas** (µS/cm)", 
                    min_value=0.0, 
                    max_value=2000.0, 
                    value=float(stats['Conductivity']['mean']), 
                    step=1.0,
                    help="Mengukur kemampuan air menghantarkan listrik"
                )
                
                # Tombol analisis dengan styling
                if st.button("🚀 Analisis Kualitas Air", use_container_width=True, type="primary"):
                    with st.spinner("Menganalisis data..."):
                        status, score, reasons, actions, color = calculate_quality(
                            in_ph, in_temp, in_turb, in_do, in_cond, stats
                        )
                        
                        # Simpan ke riwayat
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        result_entry = {
                            "Waktu": timestamp,
                            "pH": in_ph, 
                            "Suhu": in_temp, 
                            "DO": in_do, 
                            "NTU": in_turb, 
                            "Cond": in_cond,
                            "Status": status, 
                            "Skor": round(score, 2)
                        }
                        st.session_state.history.append(result_entry)
                        
                        # Simpan hasil di session state
                        st.session_state.last_result = (status, score, reasons, actions, color, 
                                                       in_ph, in_temp, in_turb, in_do, in_cond)
                        
                        st.success("✅ Analisis selesai!")
                        st.rerun()
        
        with col2:
            if 'last_result' in st.session_state:
                status, score, reasons, actions, color, ph, temp, turb, do, cond = st.session_state.last_result
                
                render_card(
                    "Hasil Diagnosis",
                    f"""
                    <div style="text-align: center; margin: 1rem 0;">
                        <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">Status Kualitas Air</div>
                    </div>
                    """,
                    icon="📊"
                )
                
                # Tampilkan skor dengan gauge chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = score,
                    title = {'text': f"SKOR: {score:.1f}/100", 'font': {'size': 20}},
                    delta = {'reference': 80, 'increasing': {'color': "green"}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#2C3E50"},
                        'bar': {'color': color},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 50], 'color': '#FFE4E1'},
                            {'range': [50, 80], 'color': '#FFF9C4'},
                            {'range': [80, 100], 'color': '#E8F5E9'}],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': score}
                    }
                ))
                
                fig.update_layout(
                    height=300,
                    margin=dict(t=50, b=10, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "#2C3E50"}
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Status dengan badge kustom
                st.markdown("### 📋 Status Akhir")
                col_status, col_score = st.columns([1, 1])
                with col_status:
                    st.markdown("**Kategori:**")
                    render_status_badge(status)
                with col_score:
                    st.markdown("**Skor Akhir:**")
                    st.markdown(f"<h3 style='color: {color};'>{score:.1f}/100</h3>", unsafe_allow_html=True)
                
                render_divider()
                
                # Detail Parameter Input
                st.markdown("### 📝 Parameter Input")
                param_cols = st.columns(5)
                params = [
                    ("pH", ph, "6.5-8.5"),
                    ("Suhu", f"{temp}°C", "20-30°C"),
                    ("DO", f"{do} mg/L", ">5 mg/L"),
                    ("Kekeruhan", f"{turb} NTU", "<25 NTU"),
                    ("Konduktivitas", f"{cond} µS/cm", "Bervariasi")
                ]
                
                for idx, (name, value, ideal) in enumerate(params):
                    with param_cols[idx]:
                        render_card(
                            name,
                            f"""
                            <div style="text-align: center; padding: 0.5rem;">
                                <div style="font-size: 1.5rem; font-weight: bold; color: #0A3D62;">{value}</div>
                                <div style="font-size: 0.8rem; color: #666; margin-top: 0.25rem;">Ideal: {ideal}</div>
                            </div>
                            """,
                            icon=""
                        )
                
                render_divider()
                
                # Rekomendasi Tindakan
                st.markdown("### 🛠️ Rekomendasi & Tindakan")
                
                if status == "BAIK":
                    st.success("🎉 **Kondisi Optimal!**")
                    st.info("Kualitas air dalam kondisi terbaik. Pertahankan manajemen pakan, sirkulasi air, dan pemantauan rutin.")
                else:
                    if reasons:
                        st.warning("⚠️ **Masalah Terdeteksi:**")
                        for reason in reasons:
                            st.markdown(f"- {reason}")
                    
                    if actions:
                        st.error("🔧 **Tindakan Perbaikan:**")
                        for action in actions:
                            st.markdown(f"• **{action}**")
                    else:
                        st.info("💡 **Saran Umum:** Pantau parameter lebih sering dan sesuaikan manajemen tambak.")
    
    # Halaman Riwayat Penilaian
    elif selected_menu == "📜 Riwayat Penilaian":
        render_header(
            "Riwayat Pemeriksaan",
            "Data historis analisis kualitas air tambak"
        )
        
        if len(st.session_state.history) > 0:
            df_hist = pd.DataFrame(st.session_state.history)
            
            # Tampilkan statistik riwayat
            col1, col2, col3 = st.columns(3)
            with col1:
                render_metric_card("Total Pemeriksaan", len(df_hist), "")
            with col2:
                avg_score = df_hist['Skor'].mean()
                render_metric_card("Rata-rata Skor", f"{avg_score:.1f}", "")
            with col3:
                latest_status = df_hist.iloc[-1]['Status']
                st.markdown("**Status Terakhir:**")
                render_status_badge(latest_status)
            
            render_card(
                "Data Riwayat Lengkap",
                "",
                icon="📋"
            )
            
            # Styling tabel dengan CSS
            def color_status(val):
                if val == 'BAIK':
                    color = '#27AE60'
                elif val == 'CUKUP':
                    color = '#F39C12'
                else:
                    color = '#E74C3C'
                return f'color: {color}; font-weight: bold;'
            
            # Format tampilan tabel
            styled_df = df_hist.copy()
            styled_df['pH'] = styled_df['pH'].map('{:.1f}'.format)
            styled_df['Suhu'] = styled_df['Suhu'].map('{:.1f}°C'.format)
            styled_df['DO'] = styled_df['DO'].map('{:.1f} mg/L'.format)
            styled_df['NTU'] = styled_df['NTU'].map('{:.1f} NTU'.format)
            styled_df['Cond'] = styled_df['Cond'].map('{:.0f} µS/cm'.format)
            styled_df['Skor'] = styled_df['Skor'].map('{:.1f}'.format)
            
            # Tampilkan tabel
            st.dataframe(
                styled_df,
                column_config={
                    "Waktu": "Waktu Analisis",
                    "pH": "pH",
                    "Suhu": "Suhu",
                    "DO": "Oksigen",
                    "NTU": "Kekeruhan",
                    "Cond": "Konduktivitas",
                    "Status": st.column_config.TextColumn(
                        "Status",
                        help="Status kualitas air"
                    ),
                    "Skor": st.column_config.NumberColumn(
                        "Skor",
                        format="%.1f",
                        help="Skor kualitas (0-100)"
                    )
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Tombol download
            csv = df_hist.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Data (CSV)",
                data=csv,
                file_name=f"riwayat_kualitas_air_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Visualisasi trend skor
            render_divider()
            st.markdown("### 📈 Trend Skor Kualitas Air")
            
            if len(df_hist) > 1:
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=df_hist['Waktu'],
                    y=df_hist['Skor'],
                    mode='lines+markers',
                    name='Skor',
                    line=dict(color='#00CEC9', width=3),
                    marker=dict(size=8, color='#0A3D62')
                ))
                
                fig_trend.update_layout(
                    title="Perkembangan Skor Kualitas Air",
                    xaxis_title="Waktu",
                    yaxis_title="Skor",
                    yaxis_range=[0, 100],
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                
                st.plotly_chart(fig_trend, use_container_width=True)
            
        else:
            render_card(
                "Data Riwayat Kosong",
                """
                <div style="text-align: center; padding: 3rem 1rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">📭</div>
                    <h3 style="color: #666;">Belum ada data pemeriksaan</h3>
                    <p>Lakukan analisis kualitas air terlebih dahulu di halaman "Penilaian Kualitas"</p>
                </div>
                """,
                icon="📭"
            )
    
    # Halaman Tentang Sistem
    elif selected_menu == "ℹ️ Tentang Sistem":
        render_header(
            "Tentang Sistem Pakar",
            "Informasi detail tentang metode dan teknologi yang digunakan"
        )
        
        # Informasi Sistem
        render_card(
            "Metode Hybrid: Rule-Based & Data-Driven Logic",
            """
            <div style="line-height: 1.6;">
            <p>Sistem ini mengadopsi pendekatan <strong>hibrida</strong> yang menggabungkan 
            <strong>Rule-Based Reasoning</strong> (aturan berbasis pengetahuan pakar) dengan 
            <strong>Data-Driven Logic</strong> menggunakan prinsip-prinsip Fuzzy Logic untuk 
            menangani ketidakpastian dan variabilitas data.</p>
            
            <p>Fuzzy Logic memungkinkan penilaian parameter air dalam bentuk <strong>derajat keanggotaan</strong> 
            (membership degrees), bukan hanya biner (baik/buruk), sehingga memberikan analisis 
            yang lebih nuansa dan akurat.</p>
            </div>
            """,
            icon="🧠"
        )
        
        # Cara Kerja dalam Grid
        st.markdown("### ⚙️ Cara Kerja Sistem")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_card(
                "1. Pembelajaran Data",
                "Memuat data historis dan menghitung statistik deskriptif untuk menetapkan baseline 'normalitas lokal'.",
                icon="📚"
            )
        
        with col2:
            render_card(
                "2. Aturan Pakar",
                "Menerapkan aturan biologis ikan yang telah ditetapkan oleh ahli akuakultur.",
                icon="🎓"
            )
        
        with col3:
            render_card(
                "3. Logika Fuzzy",
                "Menggunakan fungsi keanggotaan fuzzy untuk menghitung skor berdasarkan kecocokan kategori.",
                icon="🔮"
            )
        
        # Parameter dan Bobot
        render_divider()
        st.markdown("### 📊 Parameter dan Bobot Penilaian")
        
        parameters = [
            {"name": "Oksigen Terlarut (DO)", "weight": "35%", "desc": "Parameter paling kritis untuk respirasi ikan", "ideal": "≥5 mg/L"},
            {"name": "pH (Derajat Keasaman)", "weight": "20%", "desc": "Keseimbangan asam-basa air", "ideal": "6.5-8.5"},
            {"name": "Konduktivitas", "weight": "20%", "desc": "Indikator kepekatan mineral/salinitas", "ideal": "Sesuai data lokal"},
            {"name": "Kekeruhan (Turbidity)", "weight": "15%", "desc": "Mengukur partikel terlarut", "ideal": "≤10 NTU"},
            {"name": "Suhu (Temperature)", "weight": "10%", "desc": "Mempengaruhi metabolisme ikan", "ideal": "20-30°C"}
        ]
        
        for param in parameters:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 2, 2])
                with col1:
                    st.markdown(f"**{param['name']}**")
                with col2:
                    st.markdown(f"<span style='background: #00CEC9; color: white; padding: 2px 8px; border-radius: 4px;'>{param['weight']}</span>", unsafe_allow_html=True)
                with col3:
                    st.markdown(param['desc'])
                with col4:
                    st.markdown(f"*Ideal: {param['ideal']}*")
                st.markdown("---")
        
        # Klasifikasi Output
        render_divider()
        st.markdown("### 🎯 Klasifikasi Output")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_card(
                "🟢 BAIK",
                "Skor ≥ 80<br><br>Kondisi air optimal untuk pertumbuhan ikan",
                icon="✅"
            )
        
        with col2:
            render_card(
                "🟠 CUKUP",
                "Skor 50-79<br><br>Kondisi memerlukan perhatian, lakukan perbaikan minor",
                icon="⚠️"
            )
        
        with col3:
            render_card(
                "🔴 BURUK",
                "Skor < 50<br><br>Kondisi berbahaya, tindakan segera diperlukan",
                icon="🚨"
            )
        
        # Footer informasi
        render_divider()
        st.markdown("""
        <div class="footer">
            <p><strong>Sistem Pakar Penilaian Kualitas Air Tambak Ikan</strong></p>
            <p>Dikembangkan dengan teknologi AI dan Rule-Based System</p>
            <p>© 2024 - Semua hak dilindungi</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()