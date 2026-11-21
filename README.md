# Project-ML-Praktisi-kel-21-kasus-3
# [project ML] · Tim [21]

**Kasus:** [3. sisa umur pakai motor induksi] · **Aplikasi:** [(https://prediksi-rul-motor.streamlit.app/)] · **Video:** [(https://drive.google.com/drive/folders/10BofIehbL5mQrpWb1xkRlGcQVgRMdQUL?usp=drive_link)]

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
| Beban motor di atas 100% | 788 | Dipertahankan sebagai kemungkinan kondisi overload |

## Hasil

| Model | MAE *validation* | MAE *test* |
|---|---|---|
| *Baseline*: linear regression | 35,32 hari (RUL ≤ 60); 52,58 hari (seluruh data) | 34,20 hari (RUL ≤ 60); 50,26 hari (seluruh data) |
| [model final] | 10,87 hari (RUL ≤ 60); 44,08 hari (seluruh data) | 8,75 hari (RUL ≤ 60); 42,06 hari (seluruh data) |

*Threshold* yang dipakai: rul_hari <= 60 hari, mengikuti ketentuan kasus untuk mengevaluasi performa prediksi pada motor yang mendekati akhir masa pakainya.

Threshold status aplikasi:

- SAFE: RUL lebih dari 30 hari. (Motor dapat terus dipantau)

- REPLACE SOON: RUL lebih dari 7 hingga 30 hari. (Jadwalkan pemeriksaan dan persiapan penggantian)

- ORDER REPLACEMENT NOW: RUL maksimal 7 hari. (Prioritaskan pemeriksaan dan proses penggantian)

Threshold status tersebut merupakan aturan sementara untuk demonstrasi aplikasi dan belum divalidasi sebagai standar keselamatan atau pemeliharaan industri.

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

- Prediksi bergantung pada kualitas, kelengkapan, dan distribusi data pelatihan.

- Nilai sensor yang kosong diimputasi menggunakan median dari data training. Jika banyak sensor tidak tersedia, ketidakpastian prediksi dapat meningkat.

- Dataset memiliki anomali distribusi suhu belitan, termasuk sejumlah nilai pada rentang 250–372 °C yang perlu diverifikasi terhadap sumber data.

- Nilai beban di atas 100% dipertahankan sebagai kemungkinan kondisi overload, tetapi interpretasi fisiknya tetap memerlukan verifikasi.

- Evaluasi dilakukan menggunakan satu pembagian train-validation-test, sehingga performa pada data atau kondisi industri lain belum dapat dipastikan.

- Data test pernah digunakan dalam eksperimen awal sebelum alur validation terpisah disusun ulang. Oleh karena itu, hasil test perlu ditafsirkan dengan mempertimbangkan keterbatasan proses eksperimen tersebut.

- Prediksi RUL bukan pengganti pemeriksaan teknisi dan tidak boleh menjadi satu-satunya dasar keputusan keselamatan atau penggantian motor.

- Kategori SAFE, REPLACE SOON, dan ORDER REPLACEMENT NOW menggunakan threshold sementara yang memerlukan validasi dari ahli pemeliharaan industri.

## Daftar periksa sebelum dikumpulkan

- [*] Repositori bersifat publik dan setiap anggota memiliki *commit*
- [ ] *Notebook* dapat dijalankan ulang dari awal sampai akhir tanpa galat
- [ ] *Baseline* wajib dilaporkan dan dibandingkan
- [ ] Data *test* hanya dibuka satu kali, di akhir
- [ ] `artifacts/metadata.json` berisi versi model, fitur masukan, *threshold*, dan metrik
- [ ] Aplikasi dapat dibuka orang lain melalui tautan, termasuk dari ponsel
- [ ] Aplikasi tidak berhenti mendadak ketika menerima masukan yang tidak wajar
- [ ] Laporan paling banyak 6 halaman dan video paling lama 5 menit
