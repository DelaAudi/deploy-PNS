import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load Model
saved = joblib.load("simulator.pkl")
model = saved["model"]
baseline_pred = saved["baseline_pred"]

def run_simulation(iklan, diskon):
    input_data = np.array([[iklan, diskon]])
    prediction = model.predict(input_data)[0]
    delta = prediction - baseline_pred
    return prediction, delta

def classify_result(delta):
    if delta > 5:
        return "🟢 Optimal"
    elif delta > 0:
        return "🟡 Cukup baik"
    elif delta > -5:
        return "🟠 Kurang optimal"
    else:
        return "🔴 Berisiko"


st.markdown(
    """
    <div style="text-align: center; padding: 10px; border-bottom: 2px solid #4F46E5; margin-bottom: 20px;">
        <span style="letter-spacing: 2px; font-weight: 600; color: #6B7280; font-size: 0.85rem;">
            DELA AUDI SETYAWATI | 2313020185 | PEMODELAN DAN SIMULASI
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="margin: 0; font-size: 2.5rem;">Simulator Kebijakan Keuntungan Toko</h1>
        <p style="color: #6B7280; font-size: 1rem; margin-top: 5px;">
            Simulasi skenario intervensi anggaran iklan dan diskon terhadap keuntungan toko.
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- KONTROL & ENGINE ---
st.markdown("### Tuas Kebijakan")
col_input1, col_input2 = st.columns(2)

with col_input1:
    iklan_slider = st.slider("Anggaran Iklan (Juta)", 0, 50, 10)
with col_input2:
    diskon_slider = st.slider("Besaran Diskon (%)", 0, 50, 10)

# Jalankan Simulasi
hasil_pred, delta = run_simulation(iklan_slider, diskon_slider)

st.markdown(
    """
    <div style="height: 1px; background: linear-gradient(to right, #4F46E5, transparent); margin: 30px 0;"></div>
    """, 
    unsafe_allow_html=True
)

# --- HASIL SIMULASI ---
st.markdown("### Hasil Analisis")

with st.container(border=True):
    col_metric, col_status = st.columns([1, 1.5])
    
    with col_metric:
        st.metric(
            label="Prediksi Keuntungan", 
            value=f"Rp {hasil_pred:.2f} Jt", 
            delta=f"{delta:.2f} Jt"
        )
    
    with col_status:
        st.write("") 
        if delta > 0:
            st.success(f"Meningkat Rp {delta:.2f} Juta dibanding kondisi baseline.")
        elif delta < 0:
            st.warning(f"Menurun Rp {abs(delta):.2f} Juta dibanding kondisi baseline.")
        else:
            st.info("Tidak ada perubahan dari kondisi baseline.")

st.markdown("<br>", unsafe_allow_html=True)

data_plot = pd.DataFrame({
    'Skenario': ['Baseline', 'Intervensi'],
    'Keuntungan': [baseline_pred, hasil_pred]
})

st.bar_chart(data=data_plot, x='Skenario', y='Keuntungan')
status = classify_result(delta)
st.subheader("Status Strategi")
st.write(status)
if delta > 0:
    st.success(
        f"Skenario ini diperkirakan meningkatkan keuntungan sebesar {delta:.2f} juta dibanding kondisi saat ini."
    )

elif delta < 0:
    st.warning(
        f"Skenario ini diperkirakan menurunkan keuntungan sebesar {abs(delta):.2f} juta dibanding kondisi saat ini."
    )

else:
    st.info(
        "Skenario ini tidak memberikan perubahan terhadap kondisi baseline."
    )
