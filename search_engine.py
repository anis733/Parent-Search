"""
Mesin Pencari Informasi (Search Engine Engine)
Kelompok 11:
1. M. Anis Fathin
2. Muhammad Razi Siregar
3. Fachraja Ramadhan Sukma

Topik: Panduan Parenting & Tumbuh Kembang Anak

Implementasi 2 Algoritma Pencarian:
1. Vector Space Model (TF-IDF + Cosine Similarity)
2. Probabilistic Retrieval Model (Okapi BM25)
"""

import os
import re
import math
import pickle
import json
from collections import Counter, defaultdict
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.path.join(BASE_DIR, "index")
INDEX_BUNDLE_PATH = os.path.join(INDEX_DIR, "index_data.pkl")

# Inisialisasi Stemmer & Stopwords
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

stopword_factory = StopWordRemoverFactory()
indonesian_stopwords = set(stopword_factory.get_stop_words())
indonesian_stopwords.update({
    "yang", "untuk", "pada", "ke", "para", "namun", "menurut", "antara", "dia", "dua",
    "ia", "seperti", "jika", "sehingga", "kembali", "dan", "ini", "karena", "kepada",
    "oleh", "saat", "harus", "sementara", "setelah", "belum", "kami", "sekitar", "bagi",
    "serta", "di", "dari", "telah", "sebagai", "masih", "hal", "ketika", "adalah", "itu",
    "bisa", "dapat", "akan", "juga", "ada", "mereka", "sudah", "saya", "anda", "kita",
    "banyak", "lebih", "sangat", "tiap", "setiap", "lain", "nya", "secara", "agar",
    "tentang", "maupun", "lalu", "ikut", "hanya", "jangan", "tersebut", "yakni", "yaitu"
})

STEM_CACHE = {}

def stem_word(word: str) -> str:
    if not word:
        return ""
    if word not in STEM_CACHE:
        STEM_CACHE[word] = stemmer.stem(word)
    return STEM_CACHE[word]

def preprocess_query(query: str) -> list[str]:
    """Preproses kueri dengan membersihkan teks, stopwords, dan stemming Sastrawi."""
    text = query.lower()
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    tokens = text.split()
    filtered = [w for w in tokens if len(w) > 2 and w not in indonesian_stopwords]
    stemmed = [stem_word(w) for w in filtered]
    return [w for w in stemmed if len(w) > 2 and w not in indonesian_stopwords]

# Global cache indeks dalam memori
_INDEX_BUNDLE = None

def load_index():
    """Memuat data indeks ke memori satu kali (singleton)."""
    global _INDEX_BUNDLE
    if _INDEX_BUNDLE is None:
        if not os.path.exists(INDEX_BUNDLE_PATH):
            raise FileNotFoundError(
                f"File indeks '{INDEX_BUNDLE_PATH}' tidak ditemukan. Jalankan indexer.py terlebih dahulu!"
            )
        with open(INDEX_BUNDLE_PATH, "rb") as f:
            _INDEX_BUNDLE = pickle.load(f)
    return _INDEX_BUNDLE

def create_snippet(content: str, query_terms: list[str], max_length: int = 180) -> str:
    """Membuat cuplikan (snippet) teks yang menonjolkan kecocokan kueri."""
    if not content:
        return ""
    
    sentences = re.split(r'[.\n]+', content)
    best_sentence = ""
    best_score = -1

    q_set = set(query_terms)
    for s in sentences:
        s_clean = s.strip()
        if not s_clean:
            continue
        words_in_s = set(s_clean.lower().split())
        match_count = len(words_in_s.intersection(q_set))
        if match_count > best_score:
            best_score = match_count
            best_sentence = s_clean

    if best_sentence and best_score > 0:
        snippet = best_sentence
    else:
        snippet = content.replace("\n", " ")[:max_length]

    if len(snippet) > max_length:
        snippet = snippet[:max_length].rsplit(' ', 1)[0] + "..."
    elif not snippet.endswith('.'):
        snippet += "..."
    return snippet

def search_tfidf(query: str, top_k: int = 10) -> list[dict]:
    """
    Pencarian menggunakan Vector Space Model (TF-IDF + Cosine Similarity).
    
    Formula Cosine Similarity:
    Cosine(Q, D) = (V_Q . V_D) / (|V_Q| * |V_D|)
    Karena V_D sudah ternormalisasi L2 saat indexing:
    Cosine(Q, D) = sum_{t in Q} (w_{t,Q_norm} * w_{t,D_norm})
    """
    index = load_index()
    q_tokens = preprocess_query(query)
    if not q_tokens:
        return []

    num_docs = index["num_docs"]
    idf_dict = index["idf_tfidf"]
    doc_vectors = index["doc_vectors"]
    inverted_index = index["inverted_index"]
    documents = index["documents"]

    # 1. Bangun vektor kueri
    q_counts = Counter(q_tokens)
    q_vec = {}
    for term, count in q_counts.items():
        if term in idf_dict:
            tf = 1.0 + math.log(count)
            q_vec[term] = tf * idf_dict[term]

    if not q_vec:
        return []

    # Normalisasi L2 vektor kueri
    q_norm = math.sqrt(sum(w * w for w in q_vec.values()))
    if q_norm > 0:
        q_vec = {t: w / q_norm for t, w in q_vec.items()}

    # 2. Hitung dot product (Cosine Similarity) hanya untuk dokumen yang mengandung term kueri
    scores = defaultdict(float)
    for term, q_weight in q_vec.items():
        if term in inverted_index:
            for doc_id in inverted_index[term].keys():
                d_weight = doc_vectors[doc_id].get(term, 0.0)
                scores[doc_id] += q_weight * d_weight

    # 3. Urutkan berdasarkan skor tertinggi
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    results = []
    for rank, (doc_id, score) in enumerate(ranked_docs, 1):
        if score <= 0.0:
            continue
        doc_info = documents.get(doc_id, {})
        snippet = create_snippet(doc_info.get("content", ""), q_tokens)
        results.append({
            "rank": rank,
            "doc_id": doc_id,
            "title": doc_info.get("title", f"Dokumen {doc_id}"),
            "snippet": snippet,
            "score": round(score, 4),
            "url": doc_info.get("url", "#"),
            "source": doc_info.get("source", "Parenting Corpus")
        })

    return results

def search_bm25(query: str, top_k: int = 10) -> list[dict]:
    """
    Pencarian menggunakan model probabilistik Okapi BM25.
    
    Formula BM25:
    Score(D, Q) = sum_{t in Q} IDF(t) * [ (f(t, D) * (k1 + 1)) / (f(t, D) + k1 * (1 - b + b * (|D| / avgdl))) ]
    """
    index = load_index()
    q_tokens = preprocess_query(query)
    if not q_tokens:
        return []

    idf_dict = index["idf_bm25"]
    inverted_index = index["inverted_index"]
    doc_lengths = index["doc_lengths"]
    avg_dl = index["avg_dl"]
    k1 = index["k1"]
    b = index["b"]
    documents = index["documents"]

    scores = defaultdict(float)
    q_counts = Counter(q_tokens)

    for term in q_counts.keys():
        if term not in inverted_index or term not in idf_dict:
            continue
        idf = idf_dict[term]
        postings = inverted_index[term]

        for doc_id, tf in postings.items():
            dl = doc_lengths.get(doc_id, avg_dl)
            numerator = tf * (k1 + 1.0)
            denominator = tf + k1 * (1.0 - b + b * (dl / avg_dl))
            scores[doc_id] += idf * (numerator / denominator)

    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    results = []
    for rank, (doc_id, score) in enumerate(ranked_docs, 1):
        if score <= 0.0:
            continue
        doc_info = documents.get(doc_id, {})
        snippet = create_snippet(doc_info.get("content", ""), q_tokens)
        results.append({
            "rank": rank,
            "doc_id": doc_id,
            "title": doc_info.get("title", f"Dokumen {doc_id}"),
            "snippet": snippet,
            "score": round(score, 4),
            "url": doc_info.get("url", "#"),
            "source": doc_info.get("source", "Parenting Corpus")
        })

    return results

def get_stats():
    """Mengambil ringkasan statistik korpus dan indeks."""
    index = load_index()
    return {
        "num_documents": index["num_docs"],
        "vocabulary_size": len(index["vocabulary"]),
        "average_doc_length": round(index["avg_dl"], 2),
        "k1": index["k1"],
        "b": index["b"]
    }

if __name__ == "__main__":
    test_query = "tips MPASI bayi 6 bulan"
    print(f"Testing pencarian untuk: '{test_query}'")
    
    print("\n--- Hasil TF-IDF ---")
    tfidf_res = search_tfidf(test_query, top_k=3)
    for r in tfidf_res:
        print(f"[{r['rank']}] {r['title']} (Skor: {r['score']}) - {r['doc_id']}")

    print("\n--- Hasil Okapi BM25 ---")
    bm25_res = search_bm25(test_query, top_k=3)
    for r in bm25_res:
        print(f"[{r['rank']}] {r['title']} (Skor: {r['score']}) - {r['doc_id']}")
