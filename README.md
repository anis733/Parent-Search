# ParentSearch — Mesin Pencari Panduan Parenting & Tumbuh Kembang Anak
## Tugas Besar Mata Kuliah Penelusuran Informasi (Information Retrieval)

### Identitas Kelompok 11:
1. **M. Anis Fathin** (Arsitektur Sistem, Algoritma Retrieval TF-IDF & Okapi BM25, Integrasi)
2. **Muhammad Razi Siregar** (Web Crawling Korpus Riil, Ekstraksi Konten, Validasi URL Aktif)
3. **Fachraja Ramadhan Sukma** (Frontend Flask Web UI, Visualisasi Evaluasi Chart.js, Benchmark)

---

## Deskripsi Singkat
**ParentSearch** adalah sebuah *vertical search engine* pada korpus teks Bahasa Indonesia yang difokuskan pada topik **Panduan Parenting dan Tumbuh Kembang Anak** (kesehatan bayi, pola asuh, nutrisi MPASI, vaksinasi/imunisasi, dan stimulasi tumbuh kembang balita).

Sistem ini mengimplementasikan dua paradigma algoritma Information Retrieval:
1. **Vector Space Model (TF-IDF + Cosine Similarity)**
2. **Probabilistic Retrieval Model (Okapi BM25)**

---

## Fitur Utama
- **Korpus 300 Dokumen Asli:** Dikumpulkan secara otomatis melalui web crawler dari sumber resmi (*popmama.com* dan *theasianparent.com*) dengan seluruh tautan URL aktif 100% (HTTP 200 OK).
- **Text Preprocessing Lengkap:** Case folding, cleaning regex, stopword removal Bahasa Indonesia (Sastrawi + custom), dan stemming Sastrawi dengan *memoization cache*.
- **Inverted Index Efisien:** Struktur data postings list tersimpan dalam format JSON dan serialized binary untuk pencarian cepat.
- **Mode Dual Pencarian:** Opsi perbandingan langsung (side-by-side) antara hasil TF-IDF dan BM25 lengkap dengan skor matematis dan cuplikan (*snippet*).
- **Evaluasi & Visualisasi Metrik:** Evaluasi kuantitatif pada 12 kueri benchmark menghitung Precision@5, Precision@10, Recall@5, Recall@10, F1-Score, AP, dan MAP yang divisualisasikan dengan Chart.js (Bar chart, Radar chart, Line chart).
- **Laporan Resmi PDF:** Berkas `Kelompok_11.pdf` yang rapi dan siap dikumpulkan ke e-learning.

---

## Struktur Folder
```
uas/
├── corpus/                     # Berisi 300 dokumen JSON (doc_001.json s.d. doc_300.json)
├── index/                      # Indeks tersimpan
│   ├── inverted_index.json     # Inverted index dalam format JSON
│   ├── index_data.pkl          # Binary bundle (vektor TF-IDF, parameter BM25, vocab)
│   └── index_summary.json      # Statistik indeks
├── static/
│   ├── css/style.css           # Styling modern & responsif (tema parenting)
│   └── js/main.js              # Interaktivitas pencarian & visualisasi Chart.js
├── templates/
│   ├── base.html               # Template dasar (navbar & footer)
│   ├── index.html              # Halaman beranda pencarian
│   ├── results.html            # Halaman hasil pencarian (single & side-by-side)
│   ├── compare.html            # Dashboard perbandingan metrik evaluasi
│   └── about.html              # Informasi tim dan cara kerja sistem
├── app.py                      # Server Flask Web UI
├── crawler.py                  # Skrip web crawler real multi-threaded
├── indexer.py                  # Skrip text preprocessing & inverted indexer
├── search_engine.py            # Modul retrieval TF-IDF & Okapi BM25
├── evaluator.py                # Skrip evaluasi performa retrieval
├── generate_pdf_report.py      # Generator laporan PDF (Kelompok_11.pdf)
├── evaluation_results.json     # Data hasil evaluasi benchmark
├── Laporan_Kelompok_11.md      # Laporan lengkap dalam Markdown
├── Kelompok_11.pdf             # Laporan resmi siap kumpul (PDF)
└── requirements.txt            # Daftar pustaka dependensi Python
```

---

## Cara Menjalankan Mesin Pencari

### 1. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 2. (Opsional) Crawling dan Indexing Ulang
Korpus dan indeks sudah siap digunakan. Namun jika ingin menjalankan proses dari awal:
```bash
# 1. Jalankan crawler (mengunduh 300 artikel riil)
python crawler.py

# 2. Bangun inverted index dan bobot TF-IDF & BM25
python indexer.py

# 3. Jalankan pengujian evaluasi
python evaluator.py
```

### 3. Menjalankan Web UI
```bash
python app.py
```
Buka browser dan akses alamat:
`http://127.0.0.1:5000`

---

## Hasil Evaluasi Komparatif
| Metrik | TF-IDF (Cosine) | Okapi BM25 | Unggul |
|---|---|---|---|
| **Precision@5** | 80.00% | **81.67%** | BM25 |
| **Precision@10** | 76.67% | **77.50%** | BM25 |
| **Recall@5** | 16.26% | **16.52%** | BM25 |
| **Recall@10** | **25.57%** | 23.69% | TF-IDF |
| **F1-Score** | **0.3835** | 0.3629 | TF-IDF |
| **MAP** | **0.2329** | 0.2282 | TF-IDF |
