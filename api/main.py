
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


# ==========================================
# 1. LOKASI MODEL
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "artifacts"
    /  "model_rul_random_forest_compressed.joblib"
)

# Muat model satu kali saat API dijalankan
model = joblib.load(MODEL_PATH)


# ==========================================
# 2. DAFTAR FITUR MODEL
# ==========================================

FEATURES = [
    "tipe_motor",
    "lokasi",
    "hari_operasi",
    "beban_pct",
    "arus_A",
    "tegangan_V",
    "suhu_belitan_C",
    "getaran_rms_mm_s",
    "kecepatan_rpm"
]


# ==========================================
# 3. INISIALISASI FASTAPI
# ==========================================

app = FastAPI(
    title="Prediksi RUL Motor Induksi API",
    description="API untuk memprediksi sisa umur pakai motor induksi.",
    version="1.0.0"
)


# ==========================================
# 4. FORMAT INPUT PREDIKSI
# ==========================================

class MotorInput(BaseModel):
    tipe_motor: str
    lokasi: str
    hari_operasi: float

    # Sensor boleh kosong
    beban_pct: Optional[float] = None
    arus_A: Optional[float] = None
    tegangan_V: Optional[float] = None
    suhu_belitan_C: Optional[float] = None
    getaran_rms_mm_s: Optional[float] = None
    kecepatan_rpm: Optional[float] = None


# ==========================================
# 5. ENDPOINT PEMERIKSAAN API
# ==========================================

@app.get("/")
def home():
    return {
        "message": "API Prediksi RUL Motor Induksi aktif"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "Random Forest Regressor"
    }


# ==========================================
# 6. ENDPOINT PREDIKSI
# ==========================================

@app.post("/predict")
def predict_rul(data: MotorInput):

    # Periksa apakah minimal satu sensor tersedia
    sensor_values = [
        data.beban_pct,
        data.arus_A,
        data.tegangan_V,
        data.suhu_belitan_C,
        data.getaran_rms_mm_s,
        data.kecepatan_rpm
    ]

    if all(value is None for value in sensor_values):
        raise HTTPException(
            status_code=400,
            detail="Minimal satu data sensor harus tersedia."
        )

    # Ubah input menjadi DataFrame
    input_data = pd.DataFrame(
        [data.model_dump()],
        columns=FEATURES
    )

    # Prediksi RUL
    prediction = float(model.predict(input_data)[0])

    # Pastikan RUL tidak negatif
    prediction = max(0, prediction)

    # Tentukan status motor
    if prediction <= 7:
        status = "ORDER REPLACEMENT NOW"
    elif prediction <= 30:
        status = "REPLACE SOON"
    else:
        status = "SAFE"

    return {
        "predicted_rul_days": round(prediction, 2),
        "status": status,
        "model": "Random Forest Regressor"
    }
