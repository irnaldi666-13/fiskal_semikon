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
st.markdown("Alat bantu pengambilan keputusan untuk menyelaraskan kebijakan insentif perpajakan, belanja K/L, dan investasi Danantara.")

# Membuat 2 Tab Utama
tab_asumsi, tab_output = st.tabs(["📝 PAGE 1: Asumsi & Parameter Interaktif", "📊 PAGE 2: Hasil Simulasi & Dampak Fiskal"])

# ==============================================================================
# TAB 1: ASUMSI & PARAMETER INTERAKTIF (PAGE 1)
# ==============================================================================
with tab_asumsi:
    st.header("1. Parameter Global & Fasilitas Impor")
    
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        kurs_usd = st.number_input("Kurs USD/IDR", value=18000, step=100)
        pph_badan = st.number_input("Tarif PPh Badan Normal (%)", value=22.0, step=0.5) / 100
    with col_g2:
        super_deduction = st.number_input("Super Deduction R&D (%)", value=200.0, step=10.0) / 100
        durasi_sd = st.number_input("Durasi Super Deduction (Tahun)", value=10, step=1)
    with col_g3:
        st.markdown("**Komponen Fasilitas Impor (Fasilitas Kemenkeu):**")
        bm_rate = st.number_input("Bea Masuk Dibebaskan (%)", value=5.0, step=0.5) / 100
        pph22_rate = st.number_input("PPh 22 Impor Dibebaskan (%)", value=2.5, step=0.5) / 100
        ppn_impor_rate = st.number_input("PPN Impor Dibebaskan (%)", value=11.0, step=0.5) / 100
        total_tarif_impor = bm_rate + pph22_rate + ppn_impor_rate
        st.info(f"Total Tarif Fasilitas Impor Efektif: **{total_tarif_impor*100:.1f}%**")

    st.markdown("---")
    st.header("2. Karakteristik Sub-Kategori & Investasi per Unit")
    
    # Data Dataframe Karakteristik & Investasi
    df_char = pd.DataFrame([
        {"Segmen": "Design House", "Sub-Kategori": "Small Scale", "Investasi USD M": 15.0, "Ramp-up": 1, "EBT Margin": 0.15, "Instrumen Utama": "Tax Holiday", "Durasi": 5, "Rasionalisasi": "Skala individual, di luar cakupan GMT."},
        {"Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Investasi USD M": 50.0, "Ramp-up": 1, "EBT Margin": 0.20, "Instrumen Utama": "Tax Holiday", "Durasi": 5, "Rasionalisasi": "Penguat ekosistem desain lokal."},
        {"Segmen": "Design House", "Sub-Kategori": "Large Scale", "Investasi USD M": 200.0, "Ramp-up": 2, "EBT Margin": 0.25, "Instrumen Utama": "Tax Allowance", "Durasi": 7, "Rasionalisasi": "Skala ekspansi desain/packaging besar."},
        {"Segmen": "Foundry", "Sub-Kategori": "Small/Power Dev", "Investasi USD M": 500.0, "Ramp-up": 2, "EBT Margin": 0.20, "Instrumen Utama": "Tax Holiday", "Durasi": 10, "Rasionalisasi": "Fabrikasi komponen daya/spesifik."},
        {"Segmen": "Foundry", "Sub-Kategori": "Medium/Power Dev", "Investasi USD M": 1000.0, "Ramp-up": 4, "EBT Margin": 0.25, "Instrumen Utama": "Tax Allowance", "Durasi": 15, "Rasionalisasi": "Fasilitas wafer 8 inci mature node."},
        {"Segmen": "Foundry", "Sub-Kategori": "Large Node/Logic", "Investasi USD M": 7000.0, "Ramp-up": 4, "EBT Margin": 0.25, "Instrumen Utama": "Tax Allowance", "Durasi": 25, "Rasionalisasi": "Skala raksasa global (misal: TSMC/GlobalFoundries)."},
        {"Segmen": "Foundry", "Sub-Kategori": "Cutting Edge Tech", "Investasi USD M": 20000.0, "Ramp-up": 4, "EBT Margin": 0.30, "Instrumen Utama": "Tax Allowance", "Durasi": 25, "Rasionalisasi": "Teknologi terdepan sub-5nm, butuh insentif maksimal."},
        {"Segmen": "ATP", "Sub-Kategori": "Fasilitas Perakitan", "Investasi USD M": 300.0, "Ramp-up": 2, "EBT Margin": 0.125, "Instrumen Utama": "Tax Holiday", "Durasi": 10, "Rasionalisasi": "Assembly & testing konvensional."},
        {"Segmen": "ATP", "Sub-Kategori": "Advance Packaging", "Investasi USD M": 1000.0, "Ramp-up": 3, "EBT Margin": 0.15, "Instrumen Utama": "Tax Allowance", "Durasi": 15, "Rasionalisasi": "Teknologi pengemasan chip tingkat tinggi (CoWoS/3D)."}
    ])
    
    edited_char = st.data_editor(df_char, num_rows="fixed", use_container_width=True, key="char_editor")

    st.markdown("---")
    st.header("3. Rencana Penambahan Unit Usaha per Fase & Skenario (A3)")
    
    # Data Target Unit Usaha A3
    df_unit = pd.DataFrame([
        # Fase 1
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Design House", "Sub-Kategori": "Small Scale", "Skenario 1": 4, "Skenario 2": 6, "Skenario 3": 7, "Rasionalisasi": "Inkubasi startup lokal awal"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Skenario 1": 2, "Skenario 2": 2, "Skenario 3": 2, "Rasionalisasi": "Pusat desain regional"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "Foundry", "Sub-Kategori": "Small/Power Dev", "Skenario 1": 0, "Skenario 2": 1, "Skenario 3": 1, "Rasionalisasi": "Pilot fab power dev"},
        {"Fase": "Fase 1 (2027-2029)", "Segmen": "ATP", "Sub-Kategori": "Fasilitas Perakitan", "Skenario 1": 2, "Skenario 2": 3, "Skenario 3": 4, "Rasionalisasi": "Perakitan konvensional"},
        
        # Fase 2
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Design House", "Sub-Kategori": "Small Scale", "Skenario 1": 10, "Skenario 2": 15, "Skenario 3": 20, "Rasionalisasi": "Eksplorasi pasar komersial"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Design House", "Sub-Kategori": "Medium Scale", "Skenario 1": 5, "Skenario 2": 6, "Skenario 3": 10, "Rasionalisasi": "Peningkatan skala usaha"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "Foundry", "Sub-Kategori": "Large Node/Logic", "Skenario 1": 1, "Skenario 2": 1, "Skenario 3": 1, "Rasionalisasi": "Masuknya legacy fab"},
        {"Fase": "Fase 2 (2030-2035)", "Segmen": "ATP", "Sub-Kategori": "Advance Packaging", "Skenario 1": 1, "Skenario 2": 1, "Skenario 3": 1, "Rasionalisasi": "Advance packaging awal"},
        
        # Fase 3
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Design House", "Sub-Kategori": "Small Scale", "Skenario 1": 20, "Skenario 2": 25, "Skenario 3": 30, "Rasionalisasi": "Maturitas ekosistem"},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "Foundry", "Sub-Kategori": "Cutting Edge Tech", "Skenario 1": 1, "Skenario 2": 1, "Skenario 3": 1, "Rasionalisasi": "Pencapaian mega-investasi"},
        {"Fase": "Fase 3 (2036-2045)", "Segmen": "ATP", "Sub-Kategori": "Advance Packaging", "Skenario 1": 2, "Skenario 2": 2, "Skenario 3": 2, "Rasionalisasi": "Dukungan AI chip packaging"}
    ])
    
    edited_unit = st.data_editor(df_unit, num_rows="dynamic", use_container_width=True, key="unit_editor")

# ==============================================================================
# TAB 2: HASIL SIMULASI & DAMPAK FISKAL (PAGE 2)
# ==============================================================================
with tab_output:
    st.sidebar.header("🕹️ Filter Simulasi")
    skenario_pilihan = st.sidebar.selectbox("Pilih Skenario Proyeksi:", ["Skenario 1 (Konservatif)", "Skenario 2 (Moderat)", "Skenario 3 (Optimis)"])
    col_skenario_map = {"Skenario 1 (Konservatif)": "Skenario 1", "Skenario 2 (Moderat)": "Skenario 2", "Skenario 3 (Optimis)": "Skenario 3"}
    skenario_col = col_skenario_map[skenario_pilihan]
    
    fase_pilihan = st.sidebar.multiselect("Pilih Fase:", ["Fase 1 (2027-2029)", "Fase 2 (2030-2035)", "Fase 3 (2036-2045)"], default=["Fase 1 (2027-2029)", "Fase 2 (2030-2035)", "Fase 3 (2036-2045)"])

    # LOGIKA ENGINE PERHITUNGAN SIMULASI
    df_merged = pd.merge(edited_unit, edited_char, on=["Segmen", "Sub-Kategori"])
    df_filtered = df_merged[df_merged["Fase"].isin(fase_pilihan)].copy()
    
    # Hitung Investasi
    df_filtered["Total Investasi USD M"] = df_filtered[skenario_col] * df_filtered["Investasi USD M"]
    df_filtered["Total Investasi IDR T"] = (df_filtered["Total Investasi USD M"] * kurs_usd) / 1000
    
    # Estimasi Dukungan Kemenkeu (Tax Holiday / Allowance + Bea Masuk)
    # Asumsi Sederhana Engine: Foregone Tax = Total Inv * EBT Margin * PPh * Durasi
    df_filtered["Dukungan Kemenkeu (USD M)"] = (df_filtered["Total Investasi USD M"] * total_tarif_impor * 0.6) + \
                                               (df_filtered["Total Investasi USD M"] * df_filtered["EBT Margin"] * pph_badan * df_filtered["Durasi"])
    df_filtered["Dukungan Kemenkeu (IDR T)"] = (df_filtered["Dukungan Kemenkeu (USD M)"] * kurs_usd) / 1000

    # Estimasi Dukungan Danantara (Equity Injection)
    danantara_map = {"Design House": 0.30, "Foundry": 0.30, "ATP": 0.25}
    df_filtered["% Danantara"] = df_filtered["Segmen"].map(danantara_map)
    df_filtered["Dukungan Danantara (IDR T)"] = df_filtered["Total Investasi IDR T"] * df_filtered["% Danantara"]

    # Estimasi Dukungan K/L (APBN Direct)
    df_filtered["Dukungan KL (IDR T)"] = df_filtered[skenario_col] * 0.05  # Standardized direct spending per unit

    # REKAP OUTPUT 1 & 2
    st.subheader("1. Ringkasan Dukungan Fiskal & Modal per Institusi")
    
    summary_segmen = df_filtered.groupby("Segmen").agg({
        "Total Investasi IDR T": "sum",
        "Dukungan Kemenkeu (IDR T)": "sum",
        "Dukungan Danantara (IDR T)": "sum",
        "Dukungan KL (IDR T)": "sum"
    }).reset_index()

    # Tambahkan Baris Lintas Ekosistem (K/L)
    lintas_kl_val = 2.5  # Fixed value estimasi program LPDP, Magang, Teaching Factory
    df_lintas = pd.DataFrame([{
        "Segmen": "4. Lintas Ekosistem (KL)",
        "Total Investasi IDR T": 0.0,
        "Dukungan Kemenkeu (IDR T)": 0.0,
        "Dukungan Danantara (IDR T)": 0.0,
        "Dukungan KL (IDR T)": lintas_kl_val
    }])
    
    summary_final = pd.concat([summary_segmen, df_lintas], ignore_index=True)
    summary_final["Total Support Publik (IDR T)"] = summary_final["Dukungan Kemenkeu (IDR T)"] + summary_final["Dukungan Danantara (IDR T)"] + summary_final["Dukungan KL (IDR T)"]
    
    # Rasio Intensitas
    summary_final["Rasio Support Kemenkeu (%)"] = (summary_final["Dukungan Kemenkeu (IDR T)"] / summary_final["Total Investasi IDR T"].replace(0, 1)) * 100
    summary_final["Rasio Total Support (%)"] = (summary_final["Total Support Publik (IDR T)"] / summary_final["Total Investasi IDR T"].replace(0, 1)) * 100

    st.dataframe(summary_final.style.format({
        "Total Investasi IDR T": "{:,.2f}",
        "Dukungan Kemenkeu (IDR T)": "{:,.2f}",
        "Dukungan Danantara (IDR T)": "{:,.2f}",
        "Dukungan KL (IDR T)": "{:,.2f}",
        "Total Support Publik (IDR T)": "{:,.2f}",
        "Rasio Support Kemenkeu (%)": "{:.1f}%",
        "Rasio Total Support (%)": "{:.1f}%"
    }), use_container_width=True)

    st.markdown("---")
    
    # OUTPUT 3: VISUALISASI PERBANDINGAN & RINCIAN INSTRUMEN
    st.subheader("2. Visualisasi Perbandingan Dukungan vs Investasi")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig_bar = px.bar(
            summary_segmen, 
            x="Segmen", 
            y=["Dukungan Kemenkeu (IDR T)", "Dukungan Danantara (IDR T)", "Dukungan KL (IDR T)"],
            title="Komposisi Dukungan Publik per Segmen (Triliun Rp)",
            barmode="stack"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_chart2:
        fig_pie = px.pie(
            summary_final[summary_final["Segmen"] != "4. Lintas Ekosistem (KL)"], 
            names="Segmen", 
            values="Total Investasi IDR T",
            title="Distribusi Proyeksi Nilai Investasi per Segmen"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("3. Rincian per Instrumen / Program Institusi")
    col_det1, col_det2, col_det3 = st.columns(3)
    
    with col_det1:
        st.markdown("**Dukungan Kemenkeu:**")
        st.write("• Tax Holiday / Allowance")
        st.write("• Super Deduction R&D (200%)")
        st.write(f"• Pembebasan BM & Impor ({total_tarif_impor*100:.1f}%)")
        
    with col_det2:
        st.markdown("**Dukungan Danantara:**")
        st.write("• Equity Design House (30%)")
        st.write("• Equity Foundry (30%)")
        st.write("• Equity ATP (25%)")
        
    with col_det3:
        st.markdown("**Dukungan K/L & Lintas Ekosistem:**")
        st.write("• Seed Funding Design House")
        st.write("• Beasiswa LPDP & Magang Industri")
        st.write("• Pusat Desain Chip & Pilot Wafer Fab")