import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Dashboard Fiskal Semikonduktor 2027-2045",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚡ Dashboard Simulasi Dukungan Fiskal Semikonduktor (2027–2045)")
st.markdown("Alat bantu pengambilan keputusan terintegrasi untuk insentif perpajakan (Kemenkeu), penyertaan modal (Danantara), dan belanja K/L.")

tab_asumsi, tab_output = st.tabs(["📝 PAGE 1: Asumsi & Parameter Interaktif", "📊 PAGE 2: Hasil Simulasi & Breakdown Dimensi Fiskal"])

# ==============================================================================
# TAB 1: ASUMSI & PARAMETER INTERAKTIF (PAGE 1)
# ==============================================================================
with tab_asumsi:
    st.header("1. Parameter Global & Fasilitas Perpajakan / Kepabeanan")
    
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        kurs_usd = st.number_input("Kurs USD/IDR", value=18000, step=100)
        pph_badan = st.number_input("Tarif PPh Badan Normal (%)", value=22.0, step=0.5) / 100
        durasi_transisi_th = st.number_input("Durasi Masa Transisi Tax Holiday (Tahun)", value=2, step=1)
    with col_g2:
        super_deduction = st.number_input("Super Deduction R&D (%)", value=200.0, step=10.0) / 100
        durasi_sd = st.number_input("Durasi Pemanfaatan Super Deduction (Tahun)", value=10, step=1)
        durasi_ta = st.number_input("Durasi Tax Allowance (Tahun)", value=6, step=1)
    with col_g3:
        st.markdown("**Komponen Fasilitas Impor (Fasilitas Kemenkeu):**")
        bm_rate = st.number_input("Bea Masuk Dibebaskan (%)", value=5.0, step=0.5) / 100
        pph22_rate = st.number_input("PPh 22 Impor Dibebaskan (%)", value=2.5, step=0.5) / 100
        ppn_impor_rate = st.number_input("PPN Impor Dibebaskan (%)", value=11.0, step=0.5) / 100
        total_tarif_impor = bm_rate + pph22_rate + ppn_impor_rate
        st.info(f"Total Tarif Fasilitas Impor Efektif: **{total_tarif_impor*100:.1f}%**")

    st.markdown("---")
    st.header("2. Karakteristik Mikro 9 Sub-Kategori & Instrumen Utama")
    
    # 9 Sub-Kategori Presisi
    df_char_init = pd.DataFrame([
        {"Segmen": "Design House", "Sub-Kategori": "Small Scale", "Investasi USD M": 15.0, "Ramp-up": 1, "Asset Turnover (x)": 1.2, "EBT Margin": 0.15, "Instrumen Utama": "Tax Holiday", "TH % Utama": 0.60, "TH % Transisi": 0.30, "Durasi (Thn)": 5, "Rasio Impor (%)": 0.135, "Rasionalisasi": "Skala individual, di luar cakupan GMT."},
        {"Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Investasi USD M": 50.0, "Ramp-up": 1, "Asset Turnover (x)": 1.1, "EBT Margin": 0.20, "Instrumen Utama": "Tax Holiday", "TH % Utama": 0.80, "TH % Transisi": 0.40, "Durasi (Thn)": 5, "Rasio Impor (%)": 0.135, "Rasionalisasi": "Penguat ekosistem desain lokal."},
        {"Segmen": "Design House", "Sub-Kategori": "Large Scale", "Investasi USD M": 200.0, "Ramp-up": 2, "Asset Turnover (x)": 1.0, "EBT Margin": 0.25, "Instrumen Utama": "Tax Allowance", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 7, "Rasio Impor (%)": 0.135, "Rasionalisasi": "Skala ekspansi desain/packaging besar."},
        {"Segmen": "Foundry", "Sub-Kategori": "Small/Power Device", "Investasi USD M": 500.0, "Ramp-up": 2, "Asset Turnover (x)": 0.4, "EBT Margin": 0.20, "Instrumen Utama": "Tax Holiday", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 10, "Rasio Impor (%)": 0.65625, "Rasionalisasi": "Fabrikasi komponen daya/spesifik."},
        {"Segmen": "Foundry", "Sub-Kategori": "Medium/Power Device", "Investasi USD M": 1000.0, "Ramp-up": 4, "Asset Turnover (x)": 0.45, "EBT Margin": 0.25, "Instrumen Utama": "Tax Allowance", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 15, "Rasio Impor (%)": 0.65625, "Rasionalisasi": "Fasilitas wafer 8 inci mature node."},
        {"Segmen": "Foundry", "Sub-Kategori": "Large Node/Logic", "Investasi USD M": 7000.0, "Ramp-up": 4, "Asset Turnover (x)": 0.4, "EBT Margin": 0.25, "Instrumen Utama": "Tax Allowance", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 25, "Rasio Impor (%)": 0.65625, "Rasionalisasi": "Skala raksasa global (misal: TSMC/GlobalFoundries)."},
        {"Segmen": "Foundry", "Sub-Kategori": "Cutting Edge Technology", "Investasi USD M": 20000.0, "Ramp-up": 4, "Asset Turnover (x)": 0.35, "EBT Margin": 0.30, "Instrumen Utama": "Tax Allowance", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 25, "Rasio Impor (%)": 0.65625, "Rasionalisasi": "Teknologi terdepan sub-5nm."},
        {"Segmen": "ATP", "Sub-Kategori": "Fasilitas Perakitan ATP", "Investasi USD M": 300.0, "Ramp-up": 2, "Asset Turnover (x)": 1.0, "EBT Margin": 0.125, "Instrumen Utama": "Tax Holiday", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 10, "Rasio Impor (%)": 0.595, "Rasionalisasi": "Assembly & testing konvensional."},
        {"Segmen": "ATP", "Sub-Kategori": "Advance Packaging ATP (AI)", "Investasi USD M": 1000.0, "Ramp-up": 3, "Asset Turnover (x)": 1.0, "EBT Margin": 0.15, "Instrumen Utama": "Tax Allowance", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 15, "Rasio Impor (%)": 0.595, "Rasionalisasi": "Teknologi pengemasan chip AI (CoWoS/3D)."}
    ])
    
    edited_char = st.data_editor(df_char_init, num_rows="fixed", use_container_width=True, key="char_editor_9sub")

    st.markdown("---")
    st.header("3. Rincian Rencana Penambahan Unit Usaha (Rinci per 9 Sub-Kategori, Fase & Skenario)")
    
    sub_kat_list = list(df_char_init["Sub-Kategori"])
    fase_list = ["Fase 1 (2027-2029)", "Fase 2 (2030-2035)", "Fase 3 (2036-2045)"]
    
    # Preset Unit Usaha Rinci (Skenario 1, 2, 3)
    data_unit_full = [
        # Fase 1
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Design House", "Sub-Kategori": "Small Scale", "Skenario 1": 4, "Skenario 2": 6, "Skenario 3": 7, "Catatan": "Inkubasi startup lokal"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Skenario 1": 2, "Skenario 2": 2, "Skenario 3": 2, "Catatan": "Design center menengah"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Design House", "Sub-Kategori": "Large Scale", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0, "Catatan": "-"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Foundry", "Sub-Kategori": "Small/Power Device", "Skenario 1": 0, "Skenario 2": 1, "Skenario 3": 1, "Catatan": "Pilot Fab Power Dev"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Foundry", "Sub-Kategori": "Medium/Power Device", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0, "Catatan": "-"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Foundry", "Sub-Kategori": "Large Node/Logic", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0, "Catatan": "-"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Foundry", "Sub-Kategori": "Cutting Edge Technology", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0, "Catatan": "-"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "ATP", "Sub-Kategori": "Fasilitas Perakitan ATP", "Skenario 1": 2, "Skenario 2": 3, "Skenario 3": 4, "Catatan": "Perakitan standar"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "ATP", "Sub-Kategori": "Advance Packaging ATP (AI)", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0, "Catatan": "-"},
        
        # Fase 2
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Design House", "Sub-Kategori": "Small Scale", "Skenario 1": 10, "Skenario 2": 15, "Skenario 3": 20, "Catatan": "Skala komersial"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Skenario 1": 5, "Skenario 2": 6, "Skenario 3": 10, "Catatan": "Ekspansi pasar"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Design House", "Sub-Kategori": "Large Scale", "Skenario 1": 0, "Skenario 2": 1, "Skenario 3": 2, "Catatan": "Pusat desain global"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Foundry", "Sub-Kategori": "Small/Power Device", "Skenario 1": 0, "Skenario 2": 1, "Skenario 3": 1, "Catatan": "Fasilitas kedua"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Foundry", "Sub-Kategori": "Medium/Power Device", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 1, "Catatan": "Wafer 8 inch"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Foundry", "Sub-Kategori": "Large Node/Logic", "Skenario 1": 1, "Skenario 2": 1, "Skenario 3": 1, "Catatan": "Legacy Fab mega proyek"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Foundry", "Sub-Kategori": "Cutting Edge Technology", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0, "Catatan": "-"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "ATP", "Sub-Kategori": "Fasilitas Perakitan ATP", "Skenario 1": 5, "Skenario 2": 8, "Skenario 3": 10, "Catatan": "Kapasitas tinggi"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "ATP", "Sub-Kategori": "Advance Packaging ATP (AI)", "Skenario 1": 1, "Skenario 2": 1, "Skenario 3": 1, "Catatan": "High-end packaging"},
        
        # Fase 3
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Design House", "Sub-Kategori": "Small Scale", "Skenario 1": 20, "Skenario 2": 25, "Skenario 3": 30, "Catatan": "Ekosistem mandiri"},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Skenario 1": 10, "Skenario 2": 12, "Skenario 3": 15, "Catatan": "Desain ekspor"},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Design House", "Sub-Kategori": "Large Scale", "Skenario 1": 2, "Skenario 2": 5, "Skenario 3": 5, "Catatan": "Pusat R&D multinasional"},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Foundry", "Sub-Kategori": "Small/Power Device", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0, "Catatan": "-"},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Foundry", "Sub-Kategori": "Medium/Power Device", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0, "Catatan": "-"},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Foundry", "Sub-Kategori": "Large Node/Logic", "Skenario 1": 0, "Skenario 2": 1, "Skenario 3": 1, "Catatan": "Dukungan suplai lokal"},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Foundry", "Sub-Kategori": "Cutting Edge Technology", "Skenario 1": 1, "Skenario 2": 1, "Skenario 3": 1, "Catatan": "Sub-5nm Fab terdepan"},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "ATP", "Sub-Kategori": "Fasilitas Perakitan ATP", "Skenario 1": 5, "Skenario 2": 8, "Skenario 3": 10, "Catatan": "Maturitas perakitan"},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "ATP", "Sub-Kategori": "Advance Packaging ATP (AI)", "Skenario 1": 2, "Skenario 2": 2, "Skenario 3": 2, "Catatan": "Advanced AI packaging hub"}
    ]
    
    df_unit_init = pd.DataFrame(data_unit_full)
    edited_unit = st.data_editor(df_unit_init, num_rows="fixed", use_container_width=True, key="unit_editor_full")

    st.markdown("---")
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.header("4. Asumsi Danantara (% Ekuitas dalam JV)")
        df_danantara_init = pd.DataFrame([
            {"Segmen": "Design House", "% Ekuitas Danantara": 0.30, "Catatan": "Kemitraan strategis (misal: Danantara-Arm)"},
            {"Segmen": "Foundry", "% Ekuitas Danantara": 0.30, "Catatan": "Preseden SSMC/TSMC/GlobalFoundries"},
            {"Segmen": "ATP", "% Ekuitas Danantara": 0.25, "Catatan": "Segmen menengah packaging"}
        ])
        edited_danantara = st.data_editor(df_danantara_init, use_container_width=True, key="danantara_editor")
        
    with col_d2:
        st.header("5. Asumsi Rincian Program Belanja K/L")
        df_kl_init = pd.DataFrame([
            {"Program K/L": "Seed Funding Design House", "Cakupan": "Spesifik Design House", "Biaya Unit (USD M)": 1.5, "Rasionalisasi": "Hibah modal desain awal"},
            {"Program K/L": "Beasiswa LPDP (Tenaga Ahli)", "Cakupan": "Lintas Ekosistem", "Biaya Unit (USD M)": 0.22, "Rasionalisasi": "Pendidikan spesialis S2/S3 luar negeri"},
            {"Program K/L": "Co-funding Research Industri", "Cakupan": "Lintas Ekosistem", "Biaya Unit (USD M)": 1.67, "Rasionalisasi": "Skema RISPRO matching grant"},
            {"Program K/L": "Program Magang Vokasi", "Cakupan": "Lintas Ekosistem", "Biaya Unit (USD M)": 0.002, "Rasionalisasi": "Uang saku & insentif perakitan/pabrik"},
            {"Program K/L": "Pusat Desain Chip (BRIN/Kemenperin)", "Cakupan": "Lintas Ekosistem", "Biaya Unit (USD M)": 35.0, "Rasionalisasi": "Fasilitas EDA tools terpusat"},
            {"Program K/L": "Teaching Factory (Kemenperin)", "Cakupan": "Lintas Ekosistem", "Biaya Unit (USD M)": 15.0, "Rasionalisasi": "Fasilitas latih perakitan SMK/Politeknik"},
            {"Program K/L": "Pusat Pilot Wafer Fab", "Cakupan": "Spesifik Foundry", "Biaya Unit (USD M)": 75.0, "Rasionalisasi": "Pusat riset & uji coba wafer fab nasional"}
        ])
        edited_kl = st.data_editor(df_kl_init, use_container_width=True, key="kl_editor")

# ==============================================================================
# TAB 2: HASIL SIMULASI & BREAKDOWN DIMENSI FISKAL (PAGE 2)
# ==============================================================================
with tab_output:
    st.sidebar.header("🕹️ Filter Dimensi Simulasi")
    skenario_pilihan = st.sidebar.selectbox("Pilih Skenario Proyeksi:", ["Skenario 1 (Konservatif)", "Skenario 2 (Moderat)", "Skenario 3 (Optimis)"])
    col_skenario_map = {"Skenario 1 (Konservatif)": "Skenario 1", "Skenario 2 (Moderat)": "Skenario 2", "Skenario 3 (Optimis)": "Skenario 3"}
    skenario_col = col_skenario_map[skenario_pilihan]
    
    fase_pilihan = st.sidebar.multiselect("Pilih Fase Evaluasi:", ["Fase 1 (2027-2029)", "Fase 2 (2030-2035)", "Fase 3 (2036-2045)"], default=["Fase 1 (2027-2029)", "Fase 2 (2030-2035)", "Fase 3 (2036-2045)"])

    # LOGIKA ENGINE PERHITUNGAN SIMULASI
    df_m = pd.merge(edited_unit, edited_char, on=["Segmen", "Sub-Kategori"])
    df_calc = df_m[df_m["Fase"].isin(fase_pilihan)].copy()
    
    # Calculate Base Metrics
    df_calc["Jumlah Unit"] = df_calc[skenario_col]
    df_calc["Investasi USD M"] = df_calc["Jumlah Unit"] * df_calc["Investasi USD M"]
    df_calc["Investasi IDR T"] = (df_calc["Investasi USD M"] * kurs_usd) / 1000

    # 1. PERHITUNGAN INSTRUMEN KEMENKEU (FOREGONE REVENUE)
    # Tax Holiday: (Asset * Turn * EBT% * PPh%) * (TH_Utama * Durasi + TH_Transisi * 2)
    df_calc["Kemenkeu - Tax Holiday (IDR T)"] = (df_calc["Investasi IDR T"] * df_calc["Asset Turnover (x)"] * df_calc["EBT Margin"] * pph_badan) * \
                                                ((df_calc["TH % Utama"] * df_calc["Durasi (Thn)"]) + (df_calc["TH % Transisi"] * durasi_transisi_th)) * \
                                                (df_calc["Instrumen Utama"] == "Tax Holiday").astype(int)

    # Tax Allowance: 30% dari Investasi (5% x 6 thn) x Tarif PPh 22%
    df_calc["Kemenkeu - Tax Allowance (IDR T)"] = (df_calc["Investasi IDR T"] * 0.30 * pph_badan) * (df_calc["Instrumen Utama"] == "Tax Allowance").astype(int)
    
    # Super Deduction R&D: 200% x Estimasi Biaya R&D (dianggar 3% dari inv) x PPh %
    df_calc["Kemenkeu - Super Deduction (IDR T)"] = (df_calc["Investasi IDR T"] * 0.03 * super_deduction * pph_badan)
    
    # Pembebasan Bea Masuk & Impor: Inv * Rasio Impor * Total Tarif Impor Efektif
    df_calc["Kemenkeu - Fasilitas Impor (IDR T)"] = df_calc["Investasi IDR T"] * df_calc["Rasio Impor (%)"] * total_tarif_impor
    
    df_calc["Total Kemenkeu (IDR T)"] = df_calc["Kemenkeu - Tax Holiday (IDR T)"] + df_calc["Kemenkeu - Tax Allowance (IDR T)"] + \
                                       df_calc["Kemenkeu - Super Deduction (IDR T)"] + df_calc["Kemenkeu - Fasilitas Impor (IDR T)"]

    # 2. PERHITUNGAN DANANTARA (EQUITY INJECTION)
    df_calc = pd.merge(df_calc, edited_danantara[["Segmen", "% Ekuitas Danantara"]], on="Segmen")
    df_calc["Danantara - Equity Injection (IDR T)"] = df_calc["Investasi IDR T"] * df_calc["% Ekuitas Danantara"]

    # 3. PERHITUNGAN K/L (DIRECT APBN SPENDING)
    df_calc["KL - Seed Funding (IDR T)"] = (df_calc["Jumlah Unit"] * 1.5 * kurs_usd / 1000) * (df_calc["Segmen"] == "Design House").astype(int)
    df_calc["KL - Pilot Wafer Fab (IDR T)"] = (df_calc["Jumlah Unit"] * 75.0 * kurs_usd / 1000) * (df_calc["Segmen"] == "Foundry").astype(int) * 0.2
    df_calc["Total KL Spesifik (IDR T)"] = df_calc["KL - Seed Funding (IDR T)"] + df_calc["KL - Pilot Wafer Fab (IDR T)"]

    st.subheader("1. Ringkasan Matriks Dukungan Publik per Segmen & Lintas Ekosistem")
    
    summary_seg = df_calc.groupby("Segmen").agg({
        "Investasi IDR T": "sum",
        "Total Kemenkeu (IDR T)": "sum",
        "Danantara - Equity Injection (IDR T)": "sum",
        "Total KL Spesifik (IDR T)": "sum"
    }).reset_index()
    
    # Tambah Lintas Ekosistem KL
    kl_lintas_val = (35.0 + 15.0 + (10 * 0.22) + (5 * 1.67)) * kurs_usd / 1000  # Estimasi gabungan LPDP, R&D, Teaching Factory
    df_lintas = pd.DataFrame([{
        "Segmen": "4. Lintas Ekosistem (KL)",
        "Investasi IDR T": 0.0,
        "Total Kemenkeu (IDR T)": 0.0,
        "Danantara - Equity Injection (IDR T)": 0.0,
        "Total KL Spesifik (IDR T)": kl_lintas_val
    }])
    
    sum_final = pd.concat([summary_seg, df_lintas], ignore_index=True)
    sum_final["Total Support Publik (IDR T)"] = sum_final["Total Kemenkeu (IDR T)"] + sum_final["Danantara - Equity Injection (IDR T)"] + sum_final["Total KL Spesifik (IDR T)"]
    sum_final["Rasio Support Kemenkeu (%)"] = (sum_final["Total Kemenkeu (IDR T)"] / sum_final["Investasi IDR T"].replace(0, 1)) * 100
    sum_final["Rasio Total Support (%)"] = (sum_final["Total Support Publik (IDR T)"] / sum_final["Investasi IDR T"].replace(0, 1)) * 100

    st.dataframe(sum_final.style.format({
        "Investasi IDR T": "{:,.2f}",
        "Total Kemenkeu (IDR T)": "{:,.2f}",
        "Danantara - Equity Injection (IDR T)": "{:,.2f}",
        "Total KL Spesifik (IDR T)": "{:,.2f}",
        "Total Support Publik (IDR T)": "{:,.2f}",
        "Rasio Support Kemenkeu (%)": "{:.1f}%",
        "Rasio Total Support (%)": "{:.1f}%"
    }), use_container_width=True)

    st.markdown("---")
    st.subheader("2. BREAKDOWN DETAILED: Insentif Fiskal per Instansi, Segmen, Sub-Kategori, Instrumen, dan Fase")
    st.caption("Tabel multidimensi di bawah ini memberikan gambaran komprehensif hingga level paling teknis bagi pembaca yang ingin mendalami angka simulasi.")

    # Table Rinci Multidimensi
    df_detail_view = df_calc[[
        "Fase", "Segmen", "Sub-Kategori", "Jumlah Unit", "Investasi IDR T",
        "Kemenkeu - Tax Holiday (IDR T)", "Kemenkeu - Tax Allowance (IDR T)", 
        "Kemenkeu - Super Deduction (IDR T)", "Kemenkeu - Fasilitas Impor (IDR T)",
        "Total Kemenkeu (IDR T)", "Danantara - Equity Injection (IDR T)",
        "Total KL Spesifik (IDR T)"
    ]].copy()

    st.dataframe(df_detail_view.style.format({
        "Investasi IDR T": "{:,.2f}",
        "Kemenkeu - Tax Holiday (IDR T)": "{:,.2f}",
        "Kemenkeu - Tax Allowance (IDR T)": "{:,.2f}",
        "Kemenkeu - Super Deduction (IDR T)": "{:,.2f}",
        "Kemenkeu - Fasilitas Impor (IDR T)": "{:,.2f}",
        "Total Kemenkeu (IDR T)": "{:,.2f}",
        "Danantara - Equity Injection (IDR T)": "{:,.2f}",
        "Total KL Spesifik (IDR T)": "{:,.2f}"
    }), use_container_width=True)

    st.markdown("---")
    st.subheader("3. Grafik Perbandingan Komposisi Instrumen per Fase")
    
    df_fase_graph = df_calc.groupby("Fase").agg({
        "Kemenkeu - Tax Holiday (IDR T)": "sum",
        "Kemenkeu - Tax Allowance (IDR T)": "sum",
        "Kemenkeu - Fasilitas Impor (IDR T)": "sum",
        "Danantara - Equity Injection (IDR T)": "sum",
        "Total KL Spesifik (IDR T)": "sum"
    }).reset_index()

    fig_fase = px.bar(
        df_fase_graph, 
        x="Fase", 
        y=[
            "Kemenkeu - Tax Holiday (IDR T)", 
            "Kemenkeu - Tax Allowance (IDR T)", 
            "Kemenkeu - Fasilitas Impor (IDR T)",
            "Danantara - Equity Injection (IDR T)",
            "Total KL Spesifik (IDR T)"
        ],
        title=f"Sebaran Alokasi Dukungan Fiskal & Modal per Fase ({skenario_pilihan})",
        barmode="stack"
    )
    st.plotly_chart(fig_fase, use_container_width=True)
