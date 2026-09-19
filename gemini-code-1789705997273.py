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

tab_asumsi, tab_output = st.tabs(["📝 PAGE 1: Asumsi & Parameter Interaktif", "📊 PAGE 2: Hasil Simulasi & Visualisasi Multidimensi"])

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
    
    df_char_init = pd.DataFrame([
        {"Segmen": "Design House", "Sub-Kategori": "Small Scale", "Investasi USD M": 15.0, "Ramp-up": 1, "Asset Turnover (x)": 1.2, "EBT Margin": 0.15, "Instrumen Utama": "Tax Holiday", "TH % Utama": 0.60, "TH % Transisi": 0.30, "Durasi (Thn)": 5, "Rasio Impor (%)": 0.135},
        {"Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Investasi USD M": 50.0, "Ramp-up": 1, "Asset Turnover (x)": 1.1, "EBT Margin": 0.20, "Instrumen Utama": "Tax Holiday", "TH % Utama": 0.80, "TH % Transisi": 0.40, "Durasi (Thn)": 5, "Rasio Impor (%)": 0.135},
        {"Segmen": "Design House", "Sub-Kategori": "Large Scale", "Investasi USD M": 200.0, "Ramp-up": 2, "Asset Turnover (x)": 1.0, "EBT Margin": 0.25, "Instrumen Utama": "Tax Allowance", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 7, "Rasio Impor (%)": 0.135},
        {"Segmen": "Foundry", "Sub-Kategori": "Small/Power Device", "Investasi USD M": 500.0, "Ramp-up": 2, "Asset Turnover (x)": 0.4, "EBT Margin": 0.20, "Instrumen Utama": "Tax Holiday", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 10, "Rasio Impor (%)": 0.65625},
        {"Segmen": "Foundry", "Sub-Kategori": "Medium/Power Device", "Investasi USD M": 1000.0, "Ramp-up": 4, "Asset Turnover (x)": 0.45, "EBT Margin": 0.25, "Instrumen Utama": "Tax Allowance", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 15, "Rasio Impor (%)": 0.65625},
        {"Segmen": "Foundry", "Sub-Kategori": "Large Node/Logic", "Investasi USD M": 7000.0, "Ramp-up": 4, "Asset Turnover (x)": 0.4, "EBT Margin": 0.25, "Instrumen Utama": "Tax Allowance", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 25, "Rasio Impor (%)": 0.65625},
        {"Segmen": "Foundry", "Sub-Kategori": "Cutting Edge Technology", "Investasi USD M": 20000.0, "Ramp-up": 4, "Asset Turnover (x)": 0.35, "EBT Margin": 0.30, "Instrumen Utama": "Tax Allowance", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 25, "Rasio Impor (%)": 0.65625},
        {"Segmen": "ATP", "Sub-Kategori": "Fasilitas Perakitan ATP", "Investasi USD M": 300.0, "Ramp-up": 2, "Asset Turnover (x)": 1.0, "EBT Margin": 0.125, "Instrumen Utama": "Tax Holiday", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 10, "Rasio Impor (%)": 0.595},
        {"Segmen": "ATP", "Sub-Kategori": "Advance Packaging ATP (AI)", "Investasi USD M": 1000.0, "Ramp-up": 3, "Asset Turnover (x)": 1.0, "EBT Margin": 0.15, "Instrumen Utama": "Tax Allowance", "TH % Utama": 0.90, "TH % Transisi": 0.50, "Durasi (Thn)": 15, "Rasio Impor (%)": 0.595}
    ])
    edited_char = st.data_editor(df_char_init, num_rows="fixed", use_container_width=True, key="char_editor_9sub")

    st.markdown("---")
    st.header("3. Rincian Rencana Penambahan Unit Usaha (A3)")
    
    data_unit_full = [
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Design House", "Sub-Kategori": "Small Scale", "Skenario 1": 4, "Skenario 2": 6, "Skenario 3": 7},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Skenario 1": 2, "Skenario 2": 2, "Skenario 3": 2},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Design House", "Sub-Kategori": "Large Scale", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Foundry", "Sub-Kategori": "Small/Power Device", "Skenario 1": 0, "Skenario 2": 1, "Skenario 3": 1},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Foundry", "Sub-Kategori": "Medium/Power Device", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Foundry", "Sub-Kategori": "Large Node/Logic", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Foundry", "Sub-Kategori": "Cutting Edge Technology", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "ATP", "Sub-Kategori": "Fasilitas Perakitan ATP", "Skenario 1": 2, "Skenario 2": 3, "Skenario 3": 4},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "ATP", "Sub-Kategori": "Advance Packaging ATP (AI)", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0},
        
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Design House", "Sub-Kategori": "Small Scale", "Skenario 1": 10, "Skenario 2": 15, "Skenario 3": 20},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Skenario 1": 5, "Skenario 2": 6, "Skenario 3": 10},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Design House", "Sub-Kategori": "Large Scale", "Skenario 1": 0, "Skenario 2": 1, "Skenario 3": 2},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Foundry", "Sub-Kategori": "Small/Power Device", "Skenario 1": 0, "Skenario 2": 1, "Skenario 3": 1},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Foundry", "Sub-Kategori": "Medium/Power Device", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 1},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Foundry", "Sub-Kategori": "Large Node/Logic", "Skenario 1": 1, "Skenario 2": 1, "Skenario 3": 1},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Foundry", "Sub-Kategori": "Cutting Edge Technology", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "ATP", "Sub-Kategori": "Fasilitas Perakitan ATP", "Skenario 1": 5, "Skenario 2": 8, "Skenario 3": 10},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "ATP", "Sub-Kategori": "Advance Packaging ATP (AI)", "Skenario 1": 1, "Skenario 2": 1, "Skenario 3": 1},
        
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Design House", "Sub-Kategori": "Small Scale", "Skenario 1": 20, "Skenario 2": 25, "Skenario 3": 30},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Skenario 1": 10, "Skenario 2": 12, "Skenario 3": 15},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Design House", "Sub-Kategori": "Large Scale", "Skenario 1": 2, "Skenario 2": 5, "Skenario 3": 5},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Foundry", "Sub-Kategori": "Small/Power Device", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Foundry", "Sub-Kategori": "Medium/Power Device", "Skenario 1": 0, "Skenario 2": 0, "Skenario 3": 0},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Foundry", "Sub-Kategori": "Large Node/Logic", "Skenario 1": 0, "Skenario 2": 1, "Skenario 3": 1},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Foundry", "Sub-Kategori": "Cutting Edge Technology", "Skenario 1": 1, "Skenario 2": 1, "Skenario 3": 1},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "ATP", "Sub-Kategori": "Fasilitas Perakitan ATP", "Skenario 1": 5, "Skenario 2": 8, "Skenario 3": 10},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "ATP", "Sub-Kategori": "Advance Packaging ATP (AI)", "Skenario 1": 2, "Skenario 2": 2, "Skenario 3": 2}
    ]
    edited_unit = st.data_editor(pd.DataFrame(data_unit_full), num_rows="fixed", use_container_width=True, key="unit_editor_full")

    st.markdown("---")
    col_k1, col_k2 = st.columns(2)
    
    with col_k1:
        st.header("4. Asumsi Beasiswa, Magang & Co-Funding per Segmen")
        df_sdm_init = pd.DataFrame([
            {"Segmen": "Design House", "LPDP (Orang/Unit)": 15, "LPDP Biaya/Orang (USD M)": 0.22, "Magang (Orang/Unit)": 50, "Magang Biaya/Orang (USD M)": 0.002, "Co-Funding Riset/Unit (USD M)": 1.67},
            {"Segmen": "Foundry", "LPDP (Orang/Unit)": 10, "LPDP Biaya/Orang (USD M)": 0.22, "Magang (Orang/Unit)": 200, "Magang Biaya/Orang (USD M)": 0.002, "Co-Funding Riset/Unit (USD M)": 1.67},
            {"Segmen": "ATP", "LPDP (Orang/Unit)": 5, "LPDP Biaya/Orang (USD M)": 0.22, "Magang (Orang/Unit)": 200, "Magang Biaya/Orang (USD M)": 0.002, "Co-Funding Riset/Unit (USD M)": 1.67}
        ])
        edited_sdm = st.data_editor(df_sdm_init, use_container_width=True, key="sdm_editor")
        
    with col_k2:
        st.header("5. Asumsi Danantara (% Ekuitas dalam JV)")
        df_danantara_init = pd.DataFrame([
            {"Segmen": "Design House", "% Ekuitas Danantara": 0.30},
            {"Segmen": "Foundry", "% Ekuitas Danantara": 0.30},
            {"Segmen": "ATP", "% Ekuitas Danantara": 0.25}
        ])
        edited_danantara = st.data_editor(df_danantara_init, use_container_width=True, key="danantara_editor")

    st.markdown("---")
    st.header("6. Asumsi Program K/L Terpusat (Tabel G3 & G4 - Input Fase x Skenario)")
    
    col_infra1, col_infra2 = st.columns(2)
    with col_infra1:
        st.subheader("G3. Pusat Desain Chip & Teaching Factory (USD M per Fase)")
        df_g3_init = pd.DataFrame([
            {"Program": "Pusat Desain Chip", "Fase": "Fase 1 (2027-2029)", "Skenario 1": 20.0, "Skenario 2": 35.0, "Skenario 3": 60.0},
            {"Program": "Pusat Desain Chip", "Fase": "Fase 2 (2030-2035)", "Skenario 1": 30.0, "Skenario 2": 45.0, "Skenario 3": 70.0},
            {"Program": "Pusat Desain Chip", "Fase": "Fase 3 (2036-2045)", "Skenario 1": 40.0, "Skenario 2": 55.0, "Skenario 3": 80.0},
            {"Program": "Teaching Factory", "Fase": "Fase 1 (2027-2029)", "Skenario 1": 7.50, "Skenario 2": 7.80, "Skenario 3": 8.00},
            {"Program": "Teaching Factory", "Fase": "Fase 2 (2030-2035)", "Skenario 1": 15.00, "Skenario 2": 15.30, "Skenario 3": 15.50},
            {"Program": "Teaching Factory", "Fase": "Fase 3 (2036-2045)", "Skenario 1": 25.00, "Skenario 2": 25.30, "Skenario 3": 25.50}
        ])
        edited_g3 = st.data_editor(df_g3_init, use_container_width=True, key="g3_editor")

    with col_infra2:
        st.subheader("G4. Pusat Pilot Wafer Fab (Biaya & Jumlah Pusat)")
        df_g4_init = pd.DataFrame([
            {"Parameter": "Biaya per pusat (USD M)", "Skenario 1": 50.0, "Skenario 2": 75.0, "Skenario 3": 100.0},
            {"Parameter": "Jumlah pusat di Fase 1 (2027-2029)", "Skenario 1": 1.0, "Skenario 2": 1.0, "Skenario 3": 1.0},
            {"Parameter": "Jumlah pusat di Fase 2 (2030-2035)", "Skenario 1": 1.0, "Skenario 2": 1.0, "Skenario 3": 1.0},
            {"Parameter": "Jumlah pusat di Fase 3 (2036-2045)", "Skenario 1": 0.0, "Skenario 2": 0.0, "Skenario 3": 1.0}
        ])
        edited_g4 = st.data_editor(df_g4_init, use_container_width=True, key="g4_editor")

# ==============================================================================
# TAB 2: HASIL SIMULASI & VISUALISASI MULTIDIMENSI (PAGE 2)
# ==============================================================================
with tab_output:
    st.sidebar.header("🕹️ Filter Simulasi Dashboard")
    skenario_pilihan = st.sidebar.selectbox("Pilih Skenario Proyeksi:", ["Skenario 1 (Konservatif)", "Skenario 2 (Moderat)", "Skenario 3 (Optimis)"])
    col_skenario_map = {"Skenario 1 (Konservatif)": "Skenario 1", "Skenario 2 (Moderat)": "Skenario 2", "Skenario 3 (Optimis)": "Skenario 3"}
    skenario_col = col_skenario_map[skenario_pilihan]
    
    fase_pilihan = st.sidebar.multiselect("Pilih Fase Evaluasi:", ["Fase 1 (2027-2029)", "Fase 2 (2030-2035)", "Fase 3 (2036-2045)"], default=["Fase 1 (2027-2029)", "Fase 2 (2030-2035)", "Fase 3 (2036-2045)"])

    # ENGINE KALKULASI UTAMA
    df_m = pd.merge(edited_unit, edited_char, on=["Segmen", "Sub-Kategori"])
    df_calc = df_m[df_m["Fase"].isin(fase_pilihan)].copy()
    
    df_calc["Jumlah Unit"] = df_calc[skenario_col]
    df_calc["Investasi USD M"] = df_calc["Jumlah Unit"] * df_calc["Investasi USD M"]
    df_calc["Investasi IDR T"] = (df_calc["Investasi USD M"] * kurs_usd) / 1000

    # KEMENKEU
    df_calc["Tax Holiday (IDR T)"] = (df_calc["Investasi IDR T"] * df_calc["Asset Turnover (x)"] * df_calc["EBT Margin"] * pph_badan) * \
                                      ((df_calc["TH % Utama"] * df_calc["Durasi (Thn)"]) + (df_calc["TH % Transisi"] * durasi_transisi_th)) * \
                                      (df_calc["Instrumen Utama"] == "Tax Holiday").astype(int)
    df_calc["Tax Allowance (IDR T)"] = (df_calc["Investasi IDR T"] * 0.30 * pph_badan) * (df_calc["Instrumen Utama"] == "Tax Allowance").astype(int)
    df_calc["Super Deduction (IDR T)"] = (df_calc["Investasi IDR T"] * 0.03 * super_deduction * pph_badan)
    df_calc["Fasilitas Impor (IDR T)"] = df_calc["Investasi IDR T"] * df_calc["Rasio Impor (%)"] * total_tarif_impor
    df_calc["Total Kemenkeu (IDR T)"] = df_calc["Tax Holiday (IDR T)"] + df_calc["Tax Allowance (IDR T)"] + df_calc["Super Deduction (IDR T)"] + df_calc["Fasilitas Impor (IDR T)"]

    # DANANTARA
    df_calc = pd.merge(df_calc, edited_danantara[["Segmen", "% Ekuitas Danantara"]], on="Segmen")
    df_calc["Danantara Equity (IDR T)"] = df_calc["Investasi IDR T"] * df_calc["% Ekuitas Danantara"]

    # K/L PER SEGMEN (LPDP, MAGANG, CO-FUNDING)
    df_calc = pd.merge(df_calc, edited_sdm, on="Segmen")
    df_calc["KL - LPDP (IDR T)"] = (df_calc["Jumlah Unit"] * df_calc["LPDP (Orang/Unit)"] * df_calc["LPDP Biaya/Orang (USD M)"] * kurs_usd) / 1000
    df_calc["KL - Magang (IDR T)"] = (df_calc["Jumlah Unit"] * df_calc["Magang (Orang/Unit)"] * df_calc["Magang Biaya/Orang (USD M)"] * kurs_usd) / 1000
    df_calc["KL - CoFunding Riset (IDR T)"] = (df_calc["Jumlah Unit"] * df_calc["Co-Funding Riset/Unit (USD M)"] * kurs_usd) / 1000
    df_calc["Total KL Spesifik Segmen (IDR T)"] = df_calc["KL - LPDP (IDR T)"] + df_calc["KL - Magang (IDR T)"] + df_calc["KL - CoFunding Riset (IDR T)"]

    # K/L TERPUSAT (INFRASTRUKTUR PER FASE)
    biaya_pilot_fab = edited_g4[edited_g4["Parameter"] == "Biaya per pusat (USD M)"][skenario_col].values[0]
    
    g3_filtered = edited_g3[edited_g3["Fase"].isin(fase_pilihan)].copy()
    g3_grouped = g3_filtered.groupby("Fase")[skenario_col].sum().reset_index()
    g3_grouped.rename(columns={skenario_col: "G3_USD_M"}, inplace=True)

    g4_p1 = edited_g4[edited_g4["Parameter"] == "Jumlah pusat di Fase 1 (2027-2029)"][skenario_col].values[0] * biaya_pilot_fab
    g4_p2 = edited_g4[edited_g4["Parameter"] == "Jumlah pusat di Fase 2 (2030-2035)"][skenario_col].values[0] * biaya_pilot_fab
    g4_p3 = edited_g4[edited_g4["Parameter"] == "Jumlah pusat di Fase 3 (2036-2045)"][skenario_col].values[0] * biaya_pilot_fab
    
    df_g4_fase = pd.DataFrame([
        {"Fase": "Fase 1 (2027-2029)", "G4_USD_M": g4_p1},
        {"Fase": "Fase 2 (2030-2035)", "G4_USD_M": g4_p2},
        {"Fase": "Fase 3 (2036-2045)", "G4_USD_M": g4_p3}
    ])
    
    df_infra_fase = pd.merge(g3_grouped, df_g4_fase, on="Fase")
    df_infra_fase["KL Terpusat (IDR T)"] = ((df_infra_fase["G3_USD_M"] + df_infra_fase["G4_USD_M"]) * kurs_usd) / 1000

    # ---------------------------------------------------------
    # VISUALISASI POIN 4: DUKUNGAN FISKAL PER INSTITUSI PER FASE
    # ---------------------------------------------------------
    st.subheader(f"📊 1. Proyeksi Dukungan Fiskal per Institusi per Fase ({skenario_pilihan})")
    
    fase_inst_df = df_calc.groupby("Fase").agg({
        "Total Kemenkeu (IDR T)": "sum",
        "Danantara Equity (IDR T)": "sum",
        "Total KL Spesifik Segmen (IDR T)": "sum"
    }).reset_index()

    fase_inst_df = pd.merge(fase_inst_df, df_infra_fase[["Fase", "KL Terpusat (IDR T)"]], on="Fase", how="left")
    fase_inst_df["Total K/L (IDR T)"] = fase_inst_df["Total KL Spesifik Segmen (IDR T)"] + fase_inst_df["KL Terpusat (IDR T)"]

    fig_poin4 = px.bar(
        fase_inst_df,
        x="Fase",
        y=["Total Kemenkeu (IDR T)", "Danantara Equity (IDR T)", "Total K/L (IDR T)"],
        title=f"Total Dukungan Fiskal & Modal per Institusi per Fase - {skenario_pilihan}",
        barmode="group",
        labels={"value": "Triliun IDR", "variable": "Institusi Pengampu"}
    )
    st.plotly_chart(fig_poin4, use_container_width=True)

    st.markdown("---")
    
    # ---------------------------------------------------------
    # VISUALISASI POIN 5: BREAKDOWN PER INSTRUMEN PER SEGMEN PER FASE
    # ---------------------------------------------------------
    st.subheader("🎨 2. Visualisasi Rincian per Instrumen / Program (Per Segmen & Fase)")
    
    tab_kem, tab_dan, tab_kl = st.tabs(["🏛️ Kemenkeu (Per Instrumen)", "🏢 Danantara (Per Equity)", "🎓 K/L (Per Program)"])
    
    with tab_kem:
        df_kem_melt = df_calc.groupby(["Fase", "Segmen"]).agg({
            "Tax Holiday (IDR T)": "sum",
            "Tax Allowance (IDR T)": "sum",
            "Super Deduction (IDR T)": "sum",
            "Fasilitas Impor (IDR T)": "sum"
        }).reset_index()
        
        fig_kem = px.bar(
            df_kem_melt,
            x="Fase",
            y=["Tax Holiday (IDR T)", "Tax Allowance (IDR T)", "Super Deduction (IDR T)", "Fasilitas Impor (IDR T)"],
            facet_col="Segmen",
            title="Breakdown Instrumen Kemenkeu per Segmen per Fase",
            barmode="stack"
        )
        st.plotly_chart(fig_kem, use_container_width=True)

    with tab_dan:
        df_dan_graph = df_calc.groupby(["Fase", "Segmen"])["Danantara Equity (IDR T)"].sum().reset_index()
        fig_dan = px.bar(
            df_dan_graph,
            x="Fase",
            y="Danantara Equity (IDR T)",
            color="Segmen",
            title="Penyertaan Modal Danantara per Segmen per Fase",
            barmode="group"
        )
        st.plotly_chart(fig_dan, use_container_width=True)

    with tab_kl:
        df_kl_melt = df_calc.groupby(["Fase", "Segmen"]).agg({
            "KL - LPDP (IDR T)": "sum",
            "KL - Magang (IDR T)": "sum",
            "KL - CoFunding Riset (IDR T)": "sum"
        }).reset_index()
        
        fig_kl = px.bar(
            df_kl_melt,
            x="Fase",
            y=["KL - LPDP (IDR T)", "KL - Magang (IDR T)", "KL - CoFunding Riset (IDR T)"],
            facet_col="Segmen",
            title="Breakdown Program Belanja K/L Spesifik Segmen per Fase",
            barmode="stack"
        )
        st.plotly_chart(fig_kl, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 3. Tabel Detail Rincian Akhir Simulasi")
    
    st.dataframe(df_calc[[
        "Fase", "Segmen", "Sub-Kategori", "Jumlah Unit", "Investasi IDR T",
        "Tax Holiday (IDR T)", "Tax Allowance (IDR T)", "Super Deduction (IDR T)", "Fasilitas Impor (IDR T)",
        "Danantara Equity (IDR T)", "KL - LPDP (IDR T)", "KL - Magang (IDR T)", "KL - CoFunding Riset (IDR T)"
    ]].style.format({
        "Investasi IDR T": "{:,.2f}", "Tax Holiday (IDR T)": "{:,.2f}", "Tax Allowance (IDR T)": "{:,.2f}",
        "Super Deduction (IDR T)": "{:,.2f}", "Fasilitas Impor (IDR T)": "{:,.2f}", "Danantara Equity (IDR T)": "{:,.2f}",
        "KL - LPDP (IDR T)": "{:,.2f}", "KL - Magang (IDR T)": "{:,.2f}", "KL - CoFunding Riset (IDR T)": "{:,.2f}"
    }), use_container_width=True)
