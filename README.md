# Project-ML-Praktisi-kel-21-kasus-3
# [project ML] · Tim [21]

**Kasus:** [3. sisa umur pakai motor induksi] · **Aplikasi:** [tautan aplikasi] · **Video:** [tautan video]

| Anggota | NIM | Bagian yang dikerjakan |
|---|---|---|
| Fathin Tsamratul Fu'adah | 2407290 | All Role |
| Iqbal Novianto | 2407976 | Hadir Kerkom |

## Masalah dan pengguna

Proyek ini ditujukan untuk membantu manajer dan tim pemeliharaan motor induksi di lingkungan industri, khususnya dalam merencanakan pemeriksaan dan penggantian motor. Model memprediksi Remaining Useful Life (RUL) dalam satuan hari berdasarkan tipe motor, lokasi, lama operasi, beban, arus, tegangan, suhu belitan, getaran, dan kecepatan motor. Hasil prediksi dapat digunakan sebagai informasi pendukung dalam menentukan prioritas pemeliharaan.

## Data dan pembersihan

| Masalah yang ditemukan | Jumlah baris | Cara menangani |
|---|---|---|
| Baris duplikat | 493 | Dihapus menggunakan drop_duplicates() |
| Nilai kosong pada arus_A | 1.588 setelah penghapusan duplikat | Ditangani menggunakan median melalui SimpleImputer |
| Nilai kosong pada suhu_belitan_C | 787 setelah penghapusan duplikat | Ditangani menggunakan median melalui SimpleImputer |
| Nilai getaran negatif (-1) | 239 | Dianggap sebagai nilai tidak valid dan diubah menjadi NaN |
| Penulisan kategori tipe_motor tidak konsisten | Beberapa variasi penulisan | Dinormalisasi menjadi 5.5kW, 11kW, dan 22kW |
|  |  |  |

## Hasil

| Model | [metrik utama] *validation* | [metrik utama] *test* |
|---|---|---|
| *Baseline*: linear regression | | |
| [model final] | | |

*Threshold* yang dipakai: [angka], karena [alasan bisnis].

## Cara menjalankan

```bash
pip install -r requirements.txt
uvicorn app.api.main:app --reload       # API
streamlit run app/ui/streamlit_app.py   # aplikasi
```

## Struktur repositori

```
notebooks/      notebook dari EDA sampai penyimpanan model
data/           data mentah (dan data bersih jika perlu)
src/features.py fungsi pembuat fitur, dipakai saat pelatihan dan saat prediksi
artifacts/      model.joblib + metadata.json
app/            API (FastAPI) dan antarmuka (Streamlit)
```

## Keterbatasan

[Dalam kondisi apa model ini tidak dapat dipercaya? Data apa yang belum tersedia?]

## Daftar periksa sebelum dikumpulkan

- [*] Repositori bersifat publik dan setiap anggota memiliki *commit*
- [ ] *Notebook* dapat dijalankan ulang dari awal sampai akhir tanpa galat
- [ ] *Baseline* wajib dilaporkan dan dibandingkan
- [ ] Data *test* hanya dibuka satu kali, di akhir
- [ ] `artifacts/metadata.json` berisi versi model, fitur masukan, *threshold*, dan metrik
- [ ] Aplikasi dapat dibuka orang lain melalui tautan, termasuk dari ponsel
- [ ] Aplikasi tidak berhenti mendadak ketika menerima masukan yang tidak wajar
- [ ] Laporan paling banyak 6 halaman dan video paling lama 5 menit
