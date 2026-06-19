# 💻 Laptop Market Intelligence

Proyek Big Data ini berfokus pada pengumpulan, pengolahan, dan visualisasi data laptop dari Tokopedia untuk menghasilkan insight mengenai pasar laptop di Indonesia. Data yang diperoleh digunakan untuk analisis harga, merek, dan karakteristik produk melalui dashboard interaktif berbasis Streamlit.

## 📌 Fitur Utama

- Scraping data laptop dari Tokopedia.
- Pengumpulan data dari berbagai merek laptop.
- Pembersihan dan preprocessing data.
- Analisis dan eksplorasi data menggunakan Jupyter Notebook.
- Dashboard interaktif menggunakan Streamlit.
- Visualisasi data menggunakan Plotly.

---

## 👥 Anggota Kelompok

| Nama | NPM |
|--------|--------|
| Praja Lohphinesti Subiarto | 24083010060 |
| Gusti Jogishwara Adji | 24083010107 |
| Muhammad Rudmardiansyah Pratama Putra | 24083010108 |

---

## 📂 Struktur Project

```
big-data-scraping-main/
│
├── app.py                          # Dashboard Streamlit
├── cleaned_laptops.csv             # Dataset hasil preprocessing
├── requirements.txt                # Library yang digunakan
├── analysis.ipynb                  # Notebook analisis data
├── insight.ipynb                   # Notebook insight data
├── scraping_big_data.ipynb         # Notebook scraping
├── codingan scraping tokopedia.ipynb
├── generate_dashboard_project.py
├── scrape_all_brands.py
├── scrape_macbook.py
│
├── tokopedia_acer_17-06-2026.csv
├── tokopedia_advan_17-06-2026.csv
├── tokopedia_asus_17-06-2026.csv
├── tokopedia_axioo_17-06-2026.csv
├── tokopedia_colorful_17-06-2026.csv
├── tokopedia_dell_17-06-2026.csv
├── tokopedia_gigabyte_17-06-2026.csv
├── tokopedia_hp_17-06-2026.csv
├── tokopedia_lenovo_17-06-2026.csv
├── tokopedia_macbook_17-06-2026.csv
├── tokopedia_msi_17-06-2026.csv
│
└── README.md
```

---

## 🛠️ Teknologi yang Digunakan

- Python
- Pandas
- NumPy
- Scikit-Learn
- Plotly
- Streamlit
- Jupyter Notebook

---

## 📦 Instalasi

Clone repository:

```bash
git clone https://github.com/username/big-data-scraping.git
cd big-data-scraping
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Menjalankan Dashboard

Jalankan perintah berikut:

```bash
streamlit run app.py
```

Dashboard akan berjalan pada browser secara otomatis.

---

## 📊 Dataset

Dataset diperoleh melalui proses web scraping dari Tokopedia dan mencakup berbagai merek laptop seperti:

- Acer
- Advan
- Asus
- Axioo
- Colorful
- Dell
- Gigabyte
- HP
- Lenovo
- MacBook
- MSI

Data yang dikumpulkan meliputi:

- Nama produk
- Harga
- Brand
- Rating
- Jumlah terjual
- Spesifikasi laptop

---

## 📈 Analisis

Analisis dilakukan menggunakan beberapa notebook:

- `scraping_big_data.ipynb` → proses scraping data.
- `analysis.ipynb` → eksplorasi dan analisis data.
- `insight.ipynb` → menghasilkan insight pasar laptop.

---

## 📚 Referensi

### Paper
https://docs.google.com/document/d/1POIkzIa7lpvRkhnJBtlyVBQryr9J8KyVwPHTX18zyqw

### Presentasi
https://www.canva.com/design/DAHELgPlJV0/M5XMZvUpQcGickW3lGQHbw

### Notebook Colab
https://colab.research.google.com/drive/1eKXZsRZTqcdYGMH3aWtPwDHQpuuZPW1r

---

## 📝 Deskripsi

Proyek ini dibuat sebagai tugas mata kuliah **Big Data** Program Studi Sains Data UPN "Veteran" Jawa Timur. Tujuan utama proyek adalah memanfaatkan teknik web scraping dan analisis data untuk memperoleh insight mengenai kondisi pasar laptop di Indonesia berdasarkan data yang tersedia pada Tokopedia.
