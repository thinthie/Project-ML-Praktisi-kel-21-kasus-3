import streamlit as st
import pandas as pd
import numpy as np
import requests
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi RUL Motor Induksi",
    page_icon="⚙️",
    layout="centered"
)

# Alamat FastAPI
# Untuk deployment, API_URL akan diatur melalui environment variable
# atau Streamlit Secrets.
try:
    API_URL = st.secrets["API_URL"]
except (KeyError, FileNotFoundError):
    API_URL = os.getenv(
        "API_URL",
        "http://127.0.0.1:8000"
    )

# Tampilan aplikasi
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


# Fungsi input sensor yang boleh tidak tersedia
def input_sensor(label, key, default, step=0.1, max_value=None):
    tidak_tersedia = st.checkbox(
        f"{label} tidak tersedia",
        key=f"{key}_missing"
    )

    if tidak_tersedia:
        st.caption(
            f"Data {label.lower()} akan diperlakukan sebagai kosong."
        )
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


# Proses prediksi melalui FastAPI
if st.button("Prediksi Sisa Umur Pakai", type="primary"):

    # Kumpulkan nilai sensor
    nilai_sensor = [
        beban_pct,
        arus_A,
        tegangan_V,
        suhu_belitan_C,
        getaran_rms_mm_s,
        kecepatan_rpm
    ]

    # Pastikan minimal satu sensor tersedia
    if all(pd.isna(nilai) for nilai in nilai_sensor):

        st.warning(
            "Minimal satu data sensor harus tersedia "
            "agar prediksi dapat dilakukan."
        )

    else:

        # Siapkan data untuk dikirim ke FastAPI
        payload = {
            "tipe_motor": tipe_motor,
            "lokasi": lokasi,
            "hari_operasi": hari_operasi,
            "beban_pct": beban_pct,
            "arus_A": arus_A,
            "tegangan_V": tegangan_V,
            "suhu_belitan_C": suhu_belitan_C,
            "getaran_rms_mm_s": getaran_rms_mm_s,
            "kecepatan_rpm": kecepatan_rpm
        }

        # Ubah nilai NaN menjadi None agar menjadi JSON null
        payload = {
            key: None if pd.isna(value) else value
            for key, value in payload.items()
        }

        try:

            with st.spinner("Sedang menghitung prediksi RUL..."):

                response = requests.post(
                    f"{API_URL.rstrip('/')}/predict",
                    json=payload,
                    timeout=30
                )

            # Tangani error dari FastAPI
            if response.status_code == 400:
                detail = response.json().get(
                    "detail",
                    "Data input tidak valid."
                )
                st.error(detail)
                st.stop()

            response.raise_for_status()

            # Ambil hasil prediksi dari API
            hasil = response.json()

            prediction = float(hasil["predicted_rul_days"])
            status = hasil["status"]

            # Tampilkan hasil
            st.header("Hasil Prediksi")

            st.metric(
                label="Perkiraan Sisa Umur Pakai",
                value=f"{prediction:.1f} hari"
            )

            if status == "ORDER REPLACEMENT NOW":

                st.error("ORDER REPLACEMENT NOW")

                st.write(
                    "Sisa umur pakai sangat pendek. "
                    "Prioritaskan pemeriksaan dan pengadaan pengganti."
                )

            elif status == "REPLACE SOON":

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

            st.caption(
                f"Model yang digunakan: {hasil['model']}"
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Tidak dapat terhubung ke FastAPI. "
                "Pastikan server FastAPI sedang berjalan."
            )

        except requests.exceptions.Timeout:

            st.error(
                "Permintaan prediksi melewati batas waktu. "
                "Silakan coba kembali."
            )

        except requests.exceptions.HTTPError:

            st.error(
                f"FastAPI mengembalikan error "
                f"{response.status_code}: {response.text}"
            )

        except (KeyError, ValueError, TypeError):

            st.error(
                "Respons dari FastAPI tidak sesuai format yang diharapkan."
            )

        except requests.exceptions.RequestException as error:

            st.error(f"Terjadi kesalahan komunikasi API: {error}")