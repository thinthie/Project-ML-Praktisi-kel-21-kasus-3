from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

original_path = BASE_DIR / "artifacts" / "model_rul_random_forest.joblib"
compressed_path = BASE_DIR / "artifacts" / "model_rul_random_forest_compressed.joblib"

print("Memuat model asli...")
model = joblib.load(original_path)

print("Mengompres model...")
joblib.dump(model, compressed_path, compress=3)

print("Memeriksa model hasil kompresi...")
compressed_model = joblib.load(compressed_path)

sample = pd.DataFrame([{
    "tipe_motor": "11kW",
    "lokasi": "Cikarang",
    "hari_operasi": 1200,
    "beban_pct": 75.0,
    "arus_A": 18.5,
    "tegangan_V": 380.0,
    "suhu_belitan_C": 70.0,
    "getaran_rms_mm_s": 2.5,
    "kecepatan_rpm": 1450.0
}])

original_prediction = float(model.predict(sample)[0])
compressed_prediction = float(compressed_model.predict(sample)[0])

original_size = original_path.stat().st_size / (1024 * 1024)
compressed_size = compressed_path.stat().st_size / (1024 * 1024)

print("\n===== HASIL KOMPRESI =====")
print(f"Ukuran model asli      : {original_size:.2f} MB")
print(f"Ukuran model kompresi  : {compressed_size:.2f} MB")
print(f"Prediksi model asli    : {original_prediction:.6f}")
print(f"Prediksi model kompresi: {compressed_prediction:.6f}")
print(f"Ukuran di bawah 100 MB : {compressed_size < 100}")
print("\nSelesai.")