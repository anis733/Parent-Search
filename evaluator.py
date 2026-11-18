"""
Evaluator Kinerja Information Retrieval
Kelompok 11:
1. M. Anis Fathin
2. Muhammad Razi Siregar
3. Fachraja Ramadhan Sukma

Modul ini melakukan:
1. Evaluasi retrieval TF-IDF (Vector Space Model) vs Okapi BM25
2. Menggunakan benchmark queries & ground-truth relevance judgements
3. Menghitung Precision@5, Precision@10, Recall@5, Recall@10, F1-Score, AP (Average Precision), dan MAP (Mean Average Precision)
4. Menyimpan hasil ke evaluation_results.json
"""

import os
import json
import math
from search_engine import search_tfidf, search_bm25, load_index

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_JSON_PATH = os.path.join(BASE_DIR, "evaluation_results.json")

def build_benchmark_ground_truth():
    """
    Menentukan ground truth dokumen relevan untuk setiap kueri benchmark
    berdasarkan konten nyata dokumen di korpus.
    """
    index = load_index()
    docs = index["documents"]

    queries = [
        {
            "query": "cara merawat bayi baru lahir",
            "keywords": ["bayi baru lahir", "perawatan", "tali pusat", "memandikan", "kulit bayi"],
            "must_any": ["baru lahir", "newborn", "merawat bayi"]
        },
        {
            "query": "MPASI pertama untuk bayi 6 bulan",
            "keywords": ["mpasi", "6 bulan", "tekstur mpasi", "makanan pendamping", "puree"],
            "must_any": ["mpasi", "makanan pendamping", "bubur bayi"]
        },
        {
            "query": "jadwal imunisasi vaksinasi anak",
            "keywords": ["imunisasi", "vaksin", "jadwal", "hepatitis", "polio", "campak", "bcg"],
            "must_any": ["imunisasi", "vaksin"]
        },
        {
            "query": "stimulasi perkembangan motorik balita",
            "keywords": ["motorik", "stimulasi", "merangkak", "berjalan", "koordinasi", "balita"],
            "must_any": ["motorik", "stimulasi"]
        },
        {
            "query": "tips menyusui dan manajemen ASI eksklusif",
            "keywords": ["asi", "menyusui", "asi perah", "asip", "laktasi", "puting"],
            "must_any": ["asi", "menyusui", "laktasi"]
        },
        {
            "query": "cara mengatasi tantrum pada balita",
            "keywords": ["tantrum", "marah", "emosi", "mengamuk", "tenang", "disiplin"],
            "must_any": ["tantrum", "emosi anak", "mengamuk"]
        },
        {
            "query": "tanda bahaya dehidrasi dan diare anak",
            "keywords": ["dehidrasi", "diare", "cairan", "oralit", "haus", "mata cekung"],
            "must_any": ["dehidrasi", "diare"]
        },
        {
            "query": "nutrisi dan gizi seimbang tumbuh kembang",
            "keywords": ["nutrisi", "gizi", "stunting", "protein", "vitamin", "zat besi", "sayur"],
            "must_any": ["nutrisi", "gizi", "stunting"]
        },
        {
            "query": "penanganan demam dan kejang demam anak",
            "keywords": ["demam", "suhu", "paracetamol", "kompres", "kejang", "step"],
            "must_any": ["demam", "kejang"]
        },
        {
            "query": "posisi dan pola tidur bayi aman",
            "keywords": ["tidur", "telentang", "sids", "boks", "sleep training", "lelap"],
            "must_any": ["tidur", "sids", "sleep"]
        },
        {
            "query": "perkembangan bahasa dan bicara speech delay",
            "keywords": ["bicara", "bahasa", "speech delay", "kosakata", "kata", "terlambat"],
            "must_any": ["bicara", "bahasa", "speech"]
        },
        {
            "query": "dampak screen time gadget bagi anak",
            "keywords": ["screen time", "gadget", "gawai", "layar", "hp", "mata"],
            "must_any": ["gadget", "screen time", "gawai", "layar"]
        }
    ]

    benchmark = []
    for item in queries:
        q_text = item["query"]
        must_any = item["must_any"]
        keywords = item["keywords"]

        relevant_docs = set()
        for doc_id, doc in docs.items():
            full_text = (doc["title"] + " " + doc["content"]).lower()
            
            # Dokumen relevan jika mengandung kata kunci wajib dan beberapa keyword pendukung
            has_must = any(m in full_text for m in must_any)
            if not has_must:
                continue

            # Skor kecocokan relevansi
            score = sum(1 for kw in keywords if kw in full_text)
            if score >= 1:
                relevant_docs.add(doc_id)

        benchmark.append({
            "query": q_text,
            "relevant_doc_ids": sorted(list(relevant_docs))
        })

    return benchmark

def compute_ap(retrieved_ids: list[str], relevant_set: set[str], cutoff: int = None) -> float:
    """Menghitung Average Precision (AP) untuk satu kueri."""
    if not relevant_set:
        return 0.0

    if cutoff is not None:
        retrieved_ids = retrieved_ids[:cutoff]

    hits = 0
    sum_precisions = 0.0

    for i, doc_id in enumerate(retrieved_ids, 1):
        if doc_id in relevant_set:
            hits += 1
            precision_at_i = hits / i
            sum_precisions += precision_at_i

    # Normalisasi dengan total dokumen relevan (atau minimum cutoff jika dievaluasi pada k)
    total_relevant = len(relevant_set)
    return sum_precisions / total_relevant if total_relevant > 0 else 0.0

def evaluate_retrieval():
    """Menjalankan evaluasi lengkap TF-IDF vs Okapi BM25."""
    print("=" * 65)
    print("MEMULAI EVALUASI SISTEM TEMU KEMBALI INFORMASI")
    print("Kelompok 11 - Topik: Parenting & Tumbuh Kembang Anak")
    print("=" * 65)

    benchmark = build_benchmark_ground_truth()
    num_queries = len(benchmark)
    print(f"Jumlah benchmark queries: {num_queries}\n")

    tfidf_p5_list, tfidf_p10_list = [], []
    tfidf_r5_list, tfidf_r10_list = [], []
    tfidf_ap_list = []

    bm25_p5_list, bm25_p10_list = [], []
    bm25_r5_list, bm25_r10_list = [], []
    bm25_ap_list = []

    query_eval_results = []

    for idx, item in enumerate(benchmark, 1):
        query = item["query"]
        relevant_set = set(item["relevant_doc_ids"])
        total_rel = len(relevant_set)

        # Retrieval TF-IDF (top 10)
        res_tfidf = search_tfidf(query, top_k=10)
        tfidf_ids = [r["doc_id"] for r in res_tfidf]

        # Retrieval BM25 (top 10)
        res_bm25 = search_bm25(query, top_k=10)
        bm25_ids = [r["doc_id"] for r in res_bm25]

        # Precision & Recall @5
        t_rel_5 = sum(1 for d in tfidf_ids[:5] if d in relevant_set)
        b_rel_5 = sum(1 for d in bm25_ids[:5] if d in relevant_set)

        t_p5 = t_rel_5 / 5.0
        b_p5 = b_rel_5 / 5.0
        t_r5 = t_rel_5 / total_rel if total_rel > 0 else 0.0
        b_r5 = b_rel_5 / total_rel if total_rel > 0 else 0.0

        # Precision & Recall @10
        t_rel_10 = sum(1 for d in tfidf_ids[:10] if d in relevant_set)
        b_rel_10 = sum(1 for d in bm25_ids[:10] if d in relevant_set)

        t_p10 = t_rel_10 / 10.0 if len(tfidf_ids) >= 10 else (t_rel_10 / len(tfidf_ids) if tfidf_ids else 0.0)
        b_p10 = b_rel_10 / 10.0 if len(bm25_ids) >= 10 else (b_rel_10 / len(bm25_ids) if bm25_ids else 0.0)
        t_r10 = t_rel_10 / total_rel if total_rel > 0 else 0.0
        b_r10 = b_rel_10 / total_rel if total_rel > 0 else 0.0

        # Average Precision
        t_ap = compute_ap(tfidf_ids, relevant_set)
        b_ap = compute_ap(bm25_ids, relevant_set)

        tfidf_p5_list.append(t_p5)
        tfidf_p10_list.append(t_p10)
        tfidf_r5_list.append(t_r5)
        tfidf_r10_list.append(t_r10)
        tfidf_ap_list.append(t_ap)

        bm25_p5_list.append(b_p5)
        bm25_p10_list.append(b_p10)
        bm25_r5_list.append(b_r5)
        bm25_r10_list.append(b_r10)
        bm25_ap_list.append(b_ap)

        query_eval_results.append({
            "query": query,
            "num_relevant": total_rel,
            "tfidf_p5": round(t_p5, 4),
            "tfidf_p10": round(t_p10, 4),
            "tfidf_ap": round(t_ap, 4),
            "bm25_p5": round(b_p5, 4),
            "bm25_p10": round(b_p10, 4),
            "bm25_ap": round(b_ap, 4)
        })

        print(f"[{idx:02d}] Query: {query}")
        print(f"     Relevant Docs: {total_rel}")
        print(f"     TF-IDF -> P@5: {t_p5:.2f}, P@10: {t_p10:.2f}, R@10: {t_r10:.2f}, AP: {t_ap:.4f}")
        print(f"     BM25   -> P@5: {b_p5:.2f}, P@10: {b_p10:.2f}, R@10: {b_r10:.2f}, AP: {b_ap:.4f}")

    # Rata-rata keseluruhan (Macro-Averages)
    mean_t_p5 = sum(tfidf_p5_list) / num_queries
    mean_t_p10 = sum(tfidf_p10_list) / num_queries
    mean_t_r5 = sum(tfidf_r5_list) / num_queries
    mean_t_r10 = sum(tfidf_r10_list) / num_queries
    map_tfidf = sum(tfidf_ap_list) / num_queries
    f1_tfidf = 2 * (mean_t_p10 * mean_t_r10) / (mean_t_p10 + mean_t_r10) if (mean_t_p10 + mean_t_r10) > 0 else 0

    mean_b_p5 = sum(bm25_p5_list) / num_queries
    mean_b_p10 = sum(bm25_p10_list) / num_queries
    mean_b_r5 = sum(bm25_r5_list) / num_queries
    mean_b_r10 = sum(bm25_r10_list) / num_queries
    map_bm25 = sum(bm25_ap_list) / num_queries
    f1_bm25 = 2 * (mean_b_p10 * mean_b_r10) / (mean_b_p10 + mean_b_r10) if (mean_b_p10 + mean_b_r10) > 0 else 0

    print("\n" + "=" * 65)
    print("HASIL EVALUASI AKHIR & PERBANDINGAN PERFORMA")
    print("=" * 65)
    print(f"{'Metrik':<20} | {'TF-IDF (Cosine)':<15} | {'Okapi BM25':<15} | {'Selisih':<10} | {'Unggul'}")
    print("-" * 75)
    
    metrics_summary = [
        ("Precision@5", mean_t_p5, mean_b_p5),
        ("Precision@10", mean_t_p10, mean_b_p10),
        ("Recall@5", mean_t_r5, mean_b_r5),
        ("Recall@10", mean_t_r10, mean_b_r10),
        ("F1-Score", f1_tfidf, f1_bm25),
        ("Average Precision", map_tfidf, map_bm25),
        ("MAP (Mean AP)", map_tfidf, map_bm25),
    ]

    for name, t_val, b_val in metrics_summary:
        diff = abs(b_val - t_val)
        winner = "BM25" if b_val > t_val else ("TF-IDF" if t_val > b_val else "Seri")
        print(f"{name:<20} | {t_val:<15.4f} | {b_val:<15.4f} | {diff:<10.4f} | {winner}")

    output_payload = {
        "metrics": {
            "tfidf": {
                "precision_at_5": round(mean_t_p5, 4),
                "precision_at_10": round(mean_t_p10, 4),
                "recall_at_5": round(mean_t_r5, 4),
                "recall_at_10": round(mean_t_r10, 4),
                "f1_score": round(f1_tfidf, 4),
                "average_precision": round(map_tfidf, 4),
                "map": round(map_tfidf, 4)
            },
            "bm25": {
                "precision_at_5": round(mean_b_p5, 4),
                "precision_at_10": round(mean_b_p10, 4),
                "recall_at_5": round(mean_b_r5, 4),
                "recall_at_10": round(mean_b_r10, 4),
                "f1_score": round(f1_bm25, 4),
                "average_precision": round(map_bm25, 4),
                "map": round(map_bm25, 4)
            }
        },
        "queries": query_eval_results
    }

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=2)

    print(f"\nHasil evaluasi lengkap disimpan di: {OUTPUT_JSON_PATH}")
    print("=" * 65)

if __name__ == "__main__":
    evaluate_retrieval()
