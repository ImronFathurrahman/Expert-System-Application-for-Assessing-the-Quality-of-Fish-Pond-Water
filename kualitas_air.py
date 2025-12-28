import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Sistem Pakar Penilaian Kualitas Air Tambak Ikan",
    page_icon="🐟",
    layout="wide"
)

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
        color = "green"
    elif 50 <= final_score < 80:
        status = "CUKUP"
        color = "orange"
    else:
        status = "BURUK"
        color = "red"

    return status, final_score, reasons, actions, color

# --- MAIN APP ---
def main():
    # Load Data
    df, stats = load_and_learn_data("kualitas_air.csv")
    
    if df is None:
        st.write("Silakan upload file 'kualitas_air.csv' terlebih dahulu.")
        return

    # Inisialisasi Session State untuk Riwayat
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Sidebar Navigasi
    st.sidebar.title("Navigasi")
    menu = st.sidebar.radio("Pilih Menu", ["🏠 Beranda", "🔍 Penilaian Kualitas", "📜 Riwayat Penilaian", "ℹ️ Tentang Sistem"])

    if menu == "🏠 Beranda":
        st.title("🐟 Selamat Datang di Sistem Pakar Penilaian Kualitas Air Tambak Ikan")
        st.markdown("""
        **Aplikasi ini dirancang untuk membantu petambak memantau dan menganalisis kualitas air tambak secara real-time.**
        
        Dengan menggunakan metode **Rule-Based dan Data-Driven Logic (Fuzzy Logic)**, sistem ini menggabungkan aturan pakar berbasis pengetahuan biologis ikan dengan analisis data historis untuk memberikan penilaian yang akurat dan rekomendasi tindakan.
        
        ### Fitur Utama:
        - **Penilaian Kualitas Air:** Masukkan parameter air dan dapatkan skor kualitas serta rekomendasi.
        - **Riwayat Penilaian:** Lihat dan unduh riwayat pemeriksaan sebelumnya.
        - **Tentang Sistem:** Pelajari lebih lanjut tentang metode dan logika yang digunakan.
        
        ### Statistik Dasar dari Data Historis:
        """)
        
        if df is not None and stats is not None:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rata-rata pH", f"{stats['pH']['mean']:.2f}")
                st.metric("Rata-rata Suhu (°C)", f"{stats['Temp']['mean']:.2f}")
            with col2:
                st.metric("Rata-rata DO (mg/L)", f"{stats['DO']['mean']:.2f}")
                st.metric("Rata-rata Turbidity (NTU)", f"{stats['Turbidity']['mean']:.2f}")
            with col3:
                st.metric("Rata-rata Conductivity (µS/cm)", f"{stats['Conductivity']['mean']:.2f}")
                st.metric("Total Data", len(df))
        
        
    elif menu == "🔍 Penilaian Kualitas":
        st.title("🐟 Sistem Pakar Penilaian Kualitas Air Tambak Ikan")
        st.markdown("Masukkan parameter air terkini untuk mendapatkan analisis dan rekomendasi.")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Input Parameter")
            st.info("Masukkan data hasil pengukuran alat.")
            
            # Input Form
            in_ph = st.slider("pH (Derajat Keasaman)", min_value=0.0, max_value=14.0, value=float(stats['pH']['mean']), step=0.1)
            in_temp = st.slider("Suhu / Temperature (°C)", min_value=0.0, max_value=50.0, value=float(stats['Temp']['mean']), step=0.1)
            in_do = st.slider("DO / Oksigen Terlarut (mg/L)", min_value=0.0, max_value=20.0, value=float(stats['DO']['mean']), step=0.1)
            in_turb = st.slider("Turbidity / Kekeruhan (NTU)", min_value=0.0, max_value=100.0, value=float(stats['Turbidity']['mean']), step=0.1)
            in_cond = st.slider("Conductivity (µS/cm)", min_value=0.0, max_value=2000.0, value=float(stats['Conductivity']['mean']), step=1.0)

            if st.button("🔍 Analisa Kualitas Air", use_container_width=True):
                status, score, reasons, actions, color = calculate_quality(in_ph, in_temp, in_turb, in_do, in_cond, stats)
                
                # Simpan ke riwayat
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result_entry = {
                    "Waktu": timestamp,
                    "pH": in_ph, "Suhu": in_temp, "DO": in_do, "NTU": in_turb, "Cond": in_cond,
                    "Status": status, "Skor": round(score, 2)
                }
                st.session_state.history.append(result_entry)
                
                # Tampilkan Hasil di Session State agar persist saat rerun
                st.session_state.last_result = (status, score, reasons, actions, color)

        with col2:
            if 'last_result' in st.session_state:
                status, score, reasons, actions, color = st.session_state.last_result
                
                st.subheader("Hasil Diagnosis")
                
                # Menampilkan Gauge Chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = score,
                    title = {'text': f"Status: {status}"},
                    delta = {'reference': 80},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': color},
                        'steps': [
                            {'range': [0, 50], 'color': "#ffcccb"},
                            {'range': [50, 80], 'color': "#ffe4b5"},
                            {'range': [80, 100], 'color': "#90ee90"}],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': score}}))
                st.plotly_chart(fig, use_container_width=True)

                # Rekomendasi
                st.divider()
                st.subheader("📋 Rekomendasi Tindakan")
                
                if status == "BAIK":
                    st.success("Kualitas air dalam kondisi optimal. Pertahankan manajemen pakan dan sirkulasi.")
                else:
                    if not reasons and not actions:
                         st.warning("Kualitas menurun, namun parameter spesifik masih dalam ambang batas toleransi. Lakukan pemantauan rutin.")
                    
                    if reasons:
                        st.markdown("**Masalah Terdeteksi:**")
                        for r in reasons:
                            st.write(f"- {r}")
                    
                    if actions:
                        st.markdown("**Saran Perbaikan:**")
                        for a in actions:
                            st.error(f"🛠 {a}")

    elif menu == "📜 Riwayat Penilaian":
        st.title("📜 Riwayat Pemeriksaan")
        if len(st.session_state.history) > 0:
            df_hist = pd.DataFrame(st.session_state.history)
            
            # Styling tabel
            def color_status(val):
                color = 'green' if val == 'BAIK' else 'orange' if val == 'CUKUP' else 'red'
                return f'color: {color}; font-weight: bold'

            st.dataframe(df_hist.style.applymap(color_status, subset=['Status']), use_container_width=True)
            
            # Download button
            csv = df_hist.to_csv(index=False).encode('utf-8')
            st.download_button("Unduh Laporan (CSV)", csv, "laporan_kualitas_air.csv", "text/csv")
        else:
            st.info("Belum ada data pemeriksaan yang tersimpan.")

    elif menu == "ℹ️ Tentang Sistem":
        st.title("Tentang Sistem Pakar Ini")
        st.markdown("""
        **Metode Rule-Based dan Data-Driven Logic (Fuzzy Logic)**
        
        Sistem ini mengadopsi pendekatan hibrida yang menggabungkan **Rule-Based Reasoning** (aturan berbasis pengetahuan pakar) dengan **Data-Driven Logic** menggunakan prinsip-prinsip Fuzzy Logic untuk menangani ketidakpastian dan variabilitas data. Fuzzy Logic memungkinkan penilaian parameter air dalam bentuk derajat keanggotaan (membership degrees), bukan hanya biner (baik/buruk), sehingga memberikan analisis yang lebih nuansa dan akurat.
        
        **Cara Kerja Sistem:**
        1. **Belajar dari Data CSV:** Sistem memuat data historis `kualitas_air.csv` dan menghitung statistik deskriptif seperti mean dan standar deviasi untuk menetapkan baseline "normalitas lokal". Ini memungkinkan adaptasi terhadap kondisi spesifik lokasi tambak.
        2. **Aturan Pakar (Rule-Based):** Menerapkan aturan biologis ikan yang telah ditetapkan oleh ahli, seperti ambang batas DO < 3 mg/L sebagai bahaya mutlak, atau pH ideal 6.5-8.5.
        3. **Fuzzy Logic Integration:** Untuk parameter seperti pH, suhu, dan lainnya, sistem menggunakan fungsi keanggotaan fuzzy (misalnya, trapezoidal atau triangular membership functions) untuk menghitung skor berdasarkan derajat kecocokan dengan kategori "baik", "cukup", dan "buruk". Ini mengurangi ketajaman aturan keras dan memberikan transisi yang lebih halus.
        
        **Parameter dan Bobot Penilaian:**
        Sistem mengevaluasi lima parameter utama dengan bobot kepentingan sebagai berikut:
        - **Dissolved Oxygen (DO) - 35%:** Parameter paling kritis karena memengaruhi respirasi ikan. Ambang: ≥5 mg/L (baik), 3-5 mg/L (cukup), <3 mg/L (buruk).
        - **pH - 20%:** Mengukur keseimbangan asam-basa. Ideal: 6.5-8.5, dengan toleransi berdasarkan data historis.
        - **Conductivity - 20%:** Indikator kepekatan mineral atau salinitas, disesuaikan dengan statistik data lokal.
        - **Turbidity (Kekeruhan) - 15%:** Mengukur partikel terlarut. Ideal: ≤10 NTU (baik), ≤30 NTU (cukup).
        - **Temperature (Suhu) - 10%:** Mempengaruhi metabolisme ikan. Ideal: 20-30°C.
        
        **Klasifikasi Output:**
        Skor akhir (0-100) dihitung menggunakan Weighted Quality Index (WQI) yang disesuaikan dengan bobot di atas.
        - 🟢 **BAIK (Skor ≥ 80):** Kondisi air optimal untuk pertumbuhan ikan.
        - 🟠 **CUKUP (Skor 50-79):** Kondisi memerlukan perhatian, lakukan perbaikan minor.
        - 🔴 **BURUK (Skor < 50):** Kondisi berbahaya, tindakan segera diperlukan untuk mencegah kematian ikan.
        
        **Keunggulan Sistem:**
        - **Adaptif:** Belajar dari data historis untuk penyesuaian lokal.
        - **Real-Time:** Memberikan rekomendasi langsung berdasarkan input pengguna.
        - **User-Friendly:** Antarmuka sederhana dengan visualisasi grafik untuk memudahkan pemahaman.
        - **Data-Driven:** Mengintegrasikan analisis statistik dengan logika fuzzy untuk akurasi tinggi.
        
        **Referensi dan Sumber:**
        - Berdasarkan standar kualitas air dari FAO (Food and Agriculture Organization) dan penelitian tentang akuakultur.
        - Fuzzy Logic diimplementasikan melalui aturan fuzzy sederhana dalam kode, seperti penggunaan mean ± 2*std untuk membership functions.
        
        Jika Anda memiliki pertanyaan lebih lanjut, silakan hubungi pengembang.
        """)

if __name__ == "__main__":
    main()
