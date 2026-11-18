"""
Indexer untuk Mesin Pencari Panduan Parenting & Tumbuh Kembang Anak
Kelompok 11:
1. M. Anis Fathin
2. Muhammad Razi Siregar
3. Fachraja Ramadhan Sukma

Modul ini melakukan:
1. Pembersihan teks (cleaning), tokenisasi, penghapusan stopword (Sastrawi + custom), dan stemming (Sastrawi)
2. Pembentukan Inverted Index
3. Perhitungan TF-IDF & Vektor Dokumen (Cosine Similarity)
4. Perhitungan Okapi BM25 parameters & weights
5. Penyimpanan hasil indeks ke direktori index/
"""

import os
import re
import json
import math
import pickle
import time
from collections import defaultdict, Counter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(BASE_DIR, "corpus")
INDEX_DIR = os.path.join(BASE_DIR, "index")

# Inisialisasi Sastrawi Stemmer dan Stopwords
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

stopword_factory = StopWordRemoverFactory()
indonesian_stopwords = set(stopword_factory.get_stop_words())

# Tambahan stopwords umum bahasa Indonesia
extra_stopwords = {
    "yang", "untuk", "pada", "ke", "para", "namun", "menurut", "antara", "dia", "dua",
    "ia", "seperti", "jika", "sehingga", "kembali", "dan", "ini", "karena", "kepada",
    "oleh", "saat", "harus", "sementara", "setelah", "belum", "kami", "sekitar", "bagi",
    "serta", "di", "dari", "telah", "sebagai", "masih", "hal", "ketika", "adalah", "itu",
    "bisa", "dapat", "akan", "juga", "ada", "mereka", "sudah", "saya", "anda", "kita",
    "banyak", "lebih", "sangat", "tiap", "setiap", "lain", "nya", "secara", "agar",
    "tentang", "maupun", "lalu", "ikut", "hanya", "jangan", "tersebut", "yakni", "yaitu"
}
indonesian_stopwords.update(extra_stopwords)

# Cache stemming untuk performa cepat
STEM_CACHE = {}

def stem_word(word: str) -> str:
    """Stem sebuah kata dengan memoization cache."""
    if not word:
        return ""
    if word not in STEM_CACHE:
        STEM_CACHE[word] = stemmer.stem(word)
    return STEM_CACHE[word]

def clean_and_tokenize(text: str) -> list[str]:
    """
    Pembersihan teks dan tokenisasi:
    1. Lowercasing
    2. Menghapus URL, angka, karakter spesial / tanda baca
    3. Ekstraksi token kata Bahasa Indonesia
    """
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    tokens = text.split()
    return tokens

def preprocess_text(text: str) -> list[str]:
    """
    Pipeline lengkap preprocessing:
    1. Tokenisasi & cleaning
    2. Stopword removal
    3. Stemming Sastrawi
    """
    tokens = clean_and_tokenize(text)
    filtered = [w for w in tokens if len(w) > 2 and w not in indonesian_stopwords]
    stemmed = [stem_word(w) for w in filtered]
    final_tokens = [w for w in stemmed if len(w) > 2 and w not in indonesian_stopwords]
    return final_tokens

def build_index():
    """Membangun indeks lengkap dari seluruh dokumen di corpus/."""
    os.makedirs(INDEX_DIR, exist_ok=True)
    start_time = time.time()
    
    print("=" * 60)
    print("MEMULAI PENGINDEKSAN KORPUS PARENTING")
    print(f"Direktori Corpus: {CORPUS_DIR}")
    print(f"Direktori Index : {INDEX_DIR}")
    print("=" * 60)

    # 1. Baca seluruh file JSON dari corpus/
    doc_files = [f for f in os.listdir(CORPUS_DIR) if f.endswith(".json")]
    doc_files.sort()
    num_docs = len(doc_files)
    print(f"Ditemukan {num_docs} dokumen untuk diindeks.")

    if num_docs == 0:
        raise ValueError("Corpus kosong! Harap jalankan crawler/generator corpus terlebih dahulu.")

    documents = {}          # doc_id -> raw doc dict
    doc_tokens = {}         # doc_id -> list of tokens
    doc_lengths = {}        # doc_id -> total tokens
    inverted_index = defaultdict(dict)  # term -> {doc_id: term_frequency}
    doc_freq = defaultdict(int)         # term -> document frequency (DF)

    for idx, filename in enumerate(doc_files, 1):
        filepath = os.path.join(CORPUS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        doc_id = data.get("id", filename.replace(".json", ""))
        title = data.get("title", "")
        content = data.get("content", "")
        url = data.get("url", "")
        source = data.get("source", "")

        # Gabungkan title (dengan bobot lebih tinggi jika diinginkan, misal diulang 2x) dan content
        combined_text = f"{title} {title} {content}"
        tokens = preprocess_text(combined_text)

        documents[doc_id] = {
            "id": doc_id,
            "title": title,
            "content": content,
            "url": url,
            "source": source,
            "snippet": content[:220] + "..." if len(content) > 220 else content
        }
        doc_tokens[doc_id] = tokens
        doc_lengths[doc_id] = len(tokens)

        # Hitung term frequency per dokumen
        tf_counts = Counter(tokens)
        for term, count in tf_counts.items():
            inverted_index[term][doc_id] = count

        if idx % 50 == 0 or idx == num_docs:
            print(f"  [{idx}/{num_docs}] Dokumen terproses (Cached stems: {len(STEM_CACHE)})")

    # Hitung Document Frequency (DF)
    for term, postings in inverted_index.items():
        doc_freq[term] = len(postings)

    vocabulary = sorted(list(inverted_index.keys()))
    avg_dl = sum(doc_lengths.values()) / num_docs if num_docs > 0 else 0

    print("-" * 60)
    print(f"Total Dokumen (N)      : {num_docs}")
    print(f"Total Unik Term (Vocab): {len(vocabulary)}")
    print(f"Rata-rata Panjang Dok  : {avg_dl:.2f} kata")

    # 2. Perhitungan Bobot TF-IDF & Normalisasi Vektor Dokumen
    print("Menghitung model Vector Space Model (TF-IDF)...")
    idf_tfidf = {}
    for term in vocabulary:
        df = doc_freq[term]
        # Rumus IDF standard dengan smoothing: log((N + 1) / (df + 1)) + 1
        idf_tfidf[term] = math.log((num_docs + 1.0) / (df + 1.0)) + 1.0

    doc_vectors = {}  # doc_id -> {term: normalized_tfidf_weight}
    for doc_id, tokens in doc_tokens.items():
        tf_counts = Counter(tokens)
        vec = {}
        for term, count in tf_counts.items():
            # Sublinear tf scaling: 1 + log(count)
            tf = 1.0 + math.log(count)
            vec[term] = tf * idf_tfidf[term]
        
        # L2 Normalization (Cosine Normalization)
        norm = math.sqrt(sum(w * w for w in vec.values()))
        if norm > 0:
            doc_vectors[doc_id] = {term: w / norm for term, w in vec.items()}
        else:
            doc_vectors[doc_id] = vec

    # 3. Perhitungan Bobot Okapi BM25 Parameters
    print("Menghitung model Okapi BM25...")
    k1 = 1.5
    b = 0.75
    idf_bm25 = {}
    for term in vocabulary:
        df = doc_freq[term]
        # Rumus Okapi BM25 IDF: ln((N - df + 0.5) / (df + 0.5) + 1.0)
        idf_val = math.log((num_docs - df + 0.5) / (df + 0.5) + 1.0)
        idf_bm25[term] = max(0.01, idf_val)  # Cegah nilai negatif

    # 4. Simpan ke File
    # A. Inverted index JSON (format terstruktur & dapat dibaca)
    inverted_index_dict = {
        term: dict(postings) for term, postings in inverted_index.items()
    }
    with open(os.path.join(INDEX_DIR, "inverted_index.json"), "w", encoding="utf-8") as f:
        json.dump(inverted_index_dict, f, ensure_ascii=False, indent=2)

    # B. Metadata ringkasan indeks
    summary = {
        "num_documents": num_docs,
        "vocabulary_size": len(vocabulary),
        "average_doc_length": round(avg_dl, 2),
        "k1": k1,
        "b": b,
        "sample_terms": vocabulary[:30],
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(os.path.join(INDEX_DIR, "index_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # C. Objek lengkap dalam binary pickle untuk pencarian ultra cepat
    index_bundle = {
        "documents": documents,
        "inverted_index": inverted_index_dict,
        "doc_freq": dict(doc_freq),
        "doc_lengths": doc_lengths,
        "avg_dl": avg_dl,
        "num_docs": num_docs,
        "idf_tfidf": idf_tfidf,
        "doc_vectors": doc_vectors,
        "idf_bm25": idf_bm25,
        "k1": k1,
        "b": b,
        "vocabulary": vocabulary
    }
    with open(os.path.join(INDEX_DIR, "index_data.pkl"), "wb") as f:
        pickle.dump(index_bundle, f, protocol=pickle.HIGHEST_PROTOCOL)

    elapsed = round(time.time() - start_time, 2)
    print("=" * 60)
    print(f"PENGINDEKSAN SUKSES! Waktu: {elapsed} detik")
    print(f"File index_data.pkl, inverted_index.json, dan index_summary.json berhasil disimpan di: {INDEX_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    build_index()
