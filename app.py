import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# Lokasi model
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "artifacts" / "model_rul_random_forest.joblib"

# Memuat model
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi RUL Motor Induksi",
    page_icon="⚙️",
    layout="centered"
)

st.title("⚙️ Prediksi Remaining Useful Life")
st.subheader("Motor Induksi")
st.write(
    "Masukkan kondisi operasional motor untuk memperkirakan "
    "sisa umur pakainya dalam hari."
)

st.divider()

# Form input
st.header("Data Motor")

tipe_motor = st.selectbox(
    "Tipe Motor",
    ["5.5kW", "11kW", "22kW"]
)

lokasi = st.selectbox(
    "Lokasi Motor",
    ["Cikarang", "Karawang", "Purwakarta"]
)

hari_operasi = st.number_input(
    "Hari Operasi",
    min_value=0,
    value=100,
    step=1
)

st.subheader("Pengukuran Sensor")

# Fungsi untuk input sensor yang boleh tidak tersedia
def input_sensor(label, key, default, step=0.1, max_value=None):
    tidak_tersedia = st.checkbox(
        f"{label} tidak tersedia",
        key=f"{key}_missing"
    )

    if tidak_tersedia:
        st.caption(f"Data {label.lower()} akan diperlakukan sebagai kosong.")
        return np.nan

    return st.number_input(
        label,
        min_value=0.0,
        max_value=max_value,
        value=default,
        step=step,
        key=key
    )

# Input sensor
beban_pct = input_sensor(
    "Beban Motor (%)",
    "beban",
    75.0,
    max_value=150.0
)

arus_A = input_sensor(
    "Arus (A)",
    "arus",
    15.0
)

tegangan_V = input_sensor(
    "Tegangan (V)",
    "tegangan",
    380.0
)

suhu_belitan_C = input_sensor(
    "Suhu Belitan (°C)",
    "suhu",
    70.0
)

getaran_rms_mm_s = input_sensor(
    "Getaran RMS (mm/s)",
    "getaran",
    2.5
)

kecepatan_rpm = input_sensor(
    "Kecepatan Motor (RPM)",
    "kecepatan",
    1470.0
)

st.divider()

# Prediksi

if st.button("Prediksi Sisa Umur Pakai", type="primary"):

    # Kumpulkan seluruh nilai sensor
    nilai_sensor = [
        beban_pct,
        arus_A,
        tegangan_V,
        suhu_belitan_C,
        getaran_rms_mm_s,
        kecepatan_rpm
    ]

    # Periksa apakah semua sensor tidak tersedia
    if all(pd.isna(nilai) for nilai in nilai_sensor):
        st.warning(
            "Minimal satu data sensor harus tersedia "
            "agar prediksi dapat dilakukan."
        )

    else:
        input_data = pd.DataFrame([{
            "tipe_motor": tipe_motor,
            "lokasi": lokasi,
            "hari_operasi": hari_operasi,
            "beban_pct": beban_pct,
            "arus_A": arus_A,
            "tegangan_V": tegangan_V,
            "suhu_belitan_C": suhu_belitan_C,
            "getaran_rms_mm_s": getaran_rms_mm_s,
            "kecepatan_rpm": kecepatan_rpm
        }])

        prediction = float(model.predict(input_data)[0])
        prediction = max(0.0, prediction)

        st.header("Hasil Prediksi")

        st.metric(
            label="Perkiraan Sisa Umur Pakai",
            value=f"{prediction:.1f} hari"
        )

        if prediction <= 7:
            st.error("ORDER REPLACEMENT NOW")
            st.write(
                "Sisa umur pakai sangat pendek. "
                "Prioritaskan pemeriksaan dan pengadaan pengganti."
            )

        elif prediction <= 30:
            st.warning("REPLACE SOON")
            st.write(
                "Rencanakan penggantian motor dalam waktu dekat."
            )

        else:
            st.success("SAFE")
            st.write(
                "Belum masuk ambang penggantian berdasarkan prediksi ini."
            )

        st.caption(
            "Status menggunakan ambang sementara 7 dan 30 hari, "
            "bukan standar keselamatan yang telah divalidasi."
        )
