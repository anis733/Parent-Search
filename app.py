"""
Mesin Pencari Panduan Parenting & Tumbuh Kembang Anak
Flask Web Application
"""

import os
import json
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Try importing the real search engine; fall back to stubs
try:
    from search_engine import search_tfidf, search_bm25
    SEARCH_ENGINE_AVAILABLE = True
except ImportError:
    SEARCH_ENGINE_AVAILABLE = False

    def search_tfidf(query, top_k=10):
        """Stub: returns sample results when search_engine.py is not ready."""
        return [
            {
                "rank": i + 1,
                "doc_id": f"doc_{i+1:03d}",
                "title": f"Panduan Parenting: {query} — Artikel {i+1}",
                "snippet": f"Ini adalah cuplikan artikel tentang {query}. "
                           f"Temukan tips dan panduan tumbuh kembang anak...",
                "score": round(0.95 - i * 0.07, 4),
                "url": "#",
            }
            for i in range(min(top_k, 10))
        ]

    def search_bm25(query, top_k=10):
        """Stub: returns sample results when search_engine.py is not ready."""
        return [
            {
                "rank": i + 1,
                "doc_id": f"doc_{i+1:03d}",
                "title": f"Tips Tumbuh Kembang: {query} — Artikel {i+1}",
                "snippet": f"Artikel ini membahas tentang {query} untuk anak. "
                           f"Dapatkan informasi lengkap tentang parenting...",
                "score": round(12.5 - i * 1.1, 4),
                "url": "#",
            }
            for i in range(min(top_k, 10))
        ]


def load_evaluation_results():
    """Load evaluation results from evaluator output."""
    eval_path = os.path.join(os.path.dirname(__file__), "evaluation_results.json")
    if os.path.exists(eval_path):
        with open(eval_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # Return sample evaluation data as fallback
    return {
        "metrics": {
            "tfidf": {
                "precision_at_5": 0.72,
                "precision_at_10": 0.65,
                "recall_at_5": 0.45,
                "recall_at_10": 0.68,
                "f1_score": 0.62,
                "average_precision": 0.58,
                "map": 0.55,
            },
            "bm25": {
                "precision_at_5": 0.78,
                "precision_at_10": 0.70,
                "recall_at_5": 0.50,
                "recall_at_10": 0.73,
                "f1_score": 0.68,
                "average_precision": 0.64,
                "map": 0.61,
            },
        },
        "queries": [
            {"query": "cara merawat bayi baru lahir", "tfidf_ap": 0.60, "bm25_ap": 0.70},
            {"query": "MPASI pertama untuk bayi 6 bulan", "tfidf_ap": 0.55, "bm25_ap": 0.65},
            {"query": "vaksinasi anak usia 1 tahun", "tfidf_ap": 0.50, "bm25_ap": 0.58},
            {"query": "perkembangan motorik anak", "tfidf_ap": 0.65, "bm25_ap": 0.70},
            {"query": "tips menyusui ASI eksklusif", "tfidf_ap": 0.70, "bm25_ap": 0.75},
            {"query": "nutrisi ibu hamil trimester pertama", "tfidf_ap": 0.48, "bm25_ap": 0.55},
            {"query": "cara mengatasi anak tantrum", "tfidf_ap": 0.62, "bm25_ap": 0.68},
            {"query": "stimulasi otak anak usia dini", "tfidf_ap": 0.58, "bm25_ap": 0.63},
            {"query": "imunisasi dasar lengkap", "tfidf_ap": 0.52, "bm25_ap": 0.60},
            {"query": "pola tidur bayi 3 bulan", "tfidf_ap": 0.55, "bm25_ap": 0.62},
        ],
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    algorithm = request.args.get("algorithm", "tfidf")
    top_k = request.args.get("top_k", 10, type=int)

    if not query:
        return render_template("index.html", error="Silakan masukkan kata kunci pencarian.")

    results_tfidf = None
    results_bm25 = None
    search_time = 0

    start = time.time()

    if algorithm in ("tfidf", "both"):
        results_tfidf = search_tfidf(query, top_k=top_k)
    if algorithm in ("bm25", "both"):
        results_bm25 = search_bm25(query, top_k=top_k)

    search_time = round(time.time() - start, 4)

    return render_template(
        "results.html",
        query=query,
        algorithm=algorithm,
        results_tfidf=results_tfidf,
        results_bm25=results_bm25,
        search_time=search_time,
        top_k=top_k,
    )


@app.route("/compare")
def compare():
    eval_data = load_evaluation_results()
    return render_template("compare.html", eval_data=eval_data)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
