/**
 * ParentSearch - JavaScript Frontend Interactivity & Visualization
 * Kelompok 11:
 * - M. Anis Fathin
 * - Muhammad Razi Siregar
 * - Fachraja Ramadhan Sukma
 */

// Kueri populer untuk auto-complete
const POPULAR_QUERIES = [
    "nutrisi anak",
    "MPASI pertama untuk bayi 6 bulan",
    "cara merawat bayi baru lahir",
    "jadwal imunisasi vaksinasi anak",
    "stimulasi perkembangan motorik balita",
    "tips menyusui dan manajemen ASI eksklusif",
    "cara mengatasi tantrum pada balita",
    "tanda bahaya dehidrasi dan diare anak",
    "nutrisi dan gizi seimbang tumbuh kembang",
    "penanganan demam dan kejang demam anak",
    "posisi dan pola tidur bayi aman",
    "perkembangan bahasa dan bicara speech delay",
    "dampak screen time gadget bagi anak",
    "cara menyapih anak dengan cinta",
    "tips mengatasi anak GTM gerakan tutup mulut",
    "perawatan tali pusat newborn"
];

document.addEventListener("DOMContentLoaded", function () {
    // 1. Mobile Navbar Toggle
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");
    if (navToggle && navLinks) {
        navToggle.addEventListener("click", function () {
            navLinks.classList.toggle("open");
        });
    }

    // 2. Auto-submit saat pengguna mengklik radio button algoritma
    const algoRadios = document.querySelectorAll('input[type="radio"][name="algorithm"]');
    algoRadios.forEach(radio => {
        radio.addEventListener("change", function () {
            const form = this.closest("form");
            const searchInput = form ? form.querySelector('input[name="q"]') : null;
            if (form && searchInput && searchInput.value.trim().length > 0) {
                // Tampilkan loading visual indicator jika ada
                form.submit();
            }
        });
    });

    // 3. Search Autocomplete & Suggestions
    const searchInput = document.getElementById("searchInput");
    const suggestionsBox = document.getElementById("searchSuggestions");

    if (searchInput && suggestionsBox) {
        searchInput.addEventListener("input", function () {
            const val = this.value.trim().toLowerCase();
            if (val.length < 2) {
                suggestionsBox.innerHTML = "";
                suggestionsBox.style.display = "none";
                return;
            }

            const matches = POPULAR_QUERIES.filter(q => q.toLowerCase().includes(val)).slice(0, 5);

            if (matches.length > 0) {
                suggestionsBox.innerHTML = matches.map(m => `
                    <div class="suggestion-item">
                        <i class="fas fa-search"></i>
                        <span>${escapeHtml(m)}</span>
                    </div>
                `).join("");
                suggestionsBox.style.display = "block";

                suggestionsBox.querySelectorAll(".suggestion-item").forEach(item => {
                    item.addEventListener("click", function () {
                        searchInput.value = this.querySelector("span").textContent;
                        suggestionsBox.style.display = "none";
                        const form = searchInput.closest("form");
                        if (form) form.submit();
                    });
                });
            } else {
                suggestionsBox.innerHTML = "";
                suggestionsBox.style.display = "none";
            }
        });

        // Tutup saran saat klik di luar
        document.addEventListener("click", function (e) {
            if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
                suggestionsBox.style.display = "none";
            }
        });
    }
});

function escapeHtml(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}

/**
 * Inisialisasi Chart.js untuk halaman compare.html
 * Memperbaiki masalah visualisasi render, tinggi container, dan kontras warna
 */
function initComparisonCharts(data) {
    if (!data || !data.metrics) {
        console.warn("Data evaluasi tidak ditemukan untuk rendering chart.");
        return;
    }

    const tfidf = data.metrics.tfidf;
    const bm25 = data.metrics.bm25;

    // Skema warna visual kontras tinggi
    const COLOR_TFIDF = {
        fill: "rgba(235, 110, 85, 0.85)",
        border: "rgba(215, 80, 55, 1)",
        light: "rgba(235, 110, 85, 0.25)",
        hover: "rgba(215, 80, 55, 0.95)"
    };
    const COLOR_BM25 = {
        fill: "rgba(42, 157, 143, 0.85)",
        border: "rgba(26, 122, 111, 1)",
        light: "rgba(42, 157, 143, 0.25)",
        hover: "rgba(26, 122, 111, 0.95)"
    };

    // 1. BAR CHART: Perbandingan Metrik Evaluasi
    const ctxBar = document.getElementById("metricsBarChart");
    if (ctxBar) {
        new Chart(ctxBar, {
            type: "bar",
            data: {
                labels: [
                    "Precision@5",
                    "Precision@10",
                    "Recall@5",
                    "Recall@10",
                    "F1-Score",
                    "MAP"
                ],
                datasets: [
                    {
                        label: "TF-IDF (Cosine)",
                        data: [
                            tfidf.precision_at_5,
                            tfidf.precision_at_10,
                            tfidf.recall_at_5,
                            tfidf.recall_at_10,
                            tfidf.f1_score,
                            tfidf.map
                        ],
                        backgroundColor: COLOR_TFIDF.fill,
                        borderColor: COLOR_TFIDF.border,
                        borderWidth: 1.5,
                        borderRadius: 6,
                        hoverBackgroundColor: COLOR_TFIDF.hover
                    },
                    {
                        label: "Okapi BM25",
                        data: [
                            bm25.precision_at_5,
                            bm25.precision_at_10,
                            bm25.recall_at_5,
                            bm25.recall_at_10,
                            bm25.f1_score,
                            bm25.map
                        ],
                        backgroundColor: COLOR_BM25.fill,
                        borderColor: COLOR_BM25.border,
                        borderWidth: 1.5,
                        borderRadius: 6,
                        hoverBackgroundColor: COLOR_BM25.hover
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 900,
                    easing: "easeOutQuart"
                },
                layout: {
                    padding: { top: 15, bottom: 5 }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        min: 0,
                        max: 1.0,
                        ticks: {
                            stepSize: 0.2,
                            callback: function (val) {
                                return (val * 100).toFixed(0) + "%";
                            },
                            font: { size: 11, weight: "600" }
                        },
                        grid: {
                            color: "rgba(0, 0, 0, 0.06)"
                        }
                    },
                    x: {
                        grid: { display: false },
                        ticks: {
                            font: { size: 11, weight: "700" },
                            color: "#333"
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: "top",
                        labels: {
                            font: { size: 12, weight: "bold" },
                            padding: 16,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: "rgba(30, 41, 59, 0.95)",
                        titleFont: { size: 13, weight: "bold" },
                        bodyFont: { size: 12 },
                        padding: 10,
                        cornerRadius: 8,
                        callbacks: {
                            label: function (ctx) {
                                const val = ctx.raw;
                                return ` ${ctx.dataset.label}: ${val.toFixed(4)} (${(val * 100).toFixed(1)}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // 2. RADAR CHART: Radar Performa Multi-Dimensi
    const ctxRadar = document.getElementById("metricsRadarChart");
    if (ctxRadar) {
        new Chart(ctxRadar, {
            type: "radar",
            data: {
                labels: [
                    "Precision@5",
                    "Precision@10",
                    "Recall@5",
                    "Recall@10",
                    "F1-Score",
                    "MAP"
                ],
                datasets: [
                    {
                        label: "TF-IDF (Cosine)",
                        data: [
                            tfidf.precision_at_5,
                            tfidf.precision_at_10,
                            tfidf.recall_at_5,
                            tfidf.recall_at_10,
                            tfidf.f1_score,
                            tfidf.map
                        ],
                        fill: true,
                        backgroundColor: COLOR_TFIDF.light,
                        borderColor: COLOR_TFIDF.border,
                        pointBackgroundColor: COLOR_TFIDF.border,
                        pointBorderColor: "#fff",
                        pointHoverBackgroundColor: "#fff",
                        pointHoverBorderColor: COLOR_TFIDF.border,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        borderWidth: 2.5
                    },
                    {
                        label: "Okapi BM25",
                        data: [
                            bm25.precision_at_5,
                            bm25.precision_at_10,
                            bm25.recall_at_5,
                            bm25.recall_at_10,
                            bm25.f1_score,
                            bm25.map
                        ],
                        fill: true,
                        backgroundColor: COLOR_BM25.light,
                        borderColor: COLOR_BM25.border,
                        pointBackgroundColor: COLOR_BM25.border,
                        pointBorderColor: "#fff",
                        pointHoverBackgroundColor: "#fff",
                        pointHoverBorderColor: COLOR_BM25.border,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        borderWidth: 2.5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 900
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        min: 0,
                        max: 1.0,
                        ticks: {
                            stepSize: 0.2,
                            display: true,
                            backdropColor: "transparent",
                            callback: function (val) {
                                return (val * 100).toFixed(0) + "%";
                            },
                            font: { size: 10 }
                        },
                        pointLabels: {
                            font: { size: 11, weight: "bold" },
                            color: "#2C3E50"
                        },
                        grid: {
                            color: "rgba(0, 0, 0, 0.08)"
                        },
                        angleLines: {
                            color: "rgba(0, 0, 0, 0.1)"
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: "top",
                        labels: {
                            font: { size: 12, weight: "bold" },
                            padding: 16,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: "rgba(30, 41, 59, 0.95)",
                        padding: 10,
                        cornerRadius: 8,
                        callbacks: {
                            label: function (ctx) {
                                const val = ctx.raw;
                                return ` ${ctx.dataset.label}: ${val.toFixed(4)} (${(val * 100).toFixed(1)}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // 3. LINE CHART: Per-Query Average Precision
    const ctxQuery = document.getElementById("perQueryChart");
    if (ctxQuery && data.queries && data.queries.length > 0) {
        const queryLabels = data.queries.map((q, i) => `Q${i + 1}`);
        const queryTitles = data.queries.map(q => q.query);
        const tfidfAPs = data.queries.map(q => q.tfidf_ap);
        const bm25APs = data.queries.map(q => q.bm25_ap);

        new Chart(ctxQuery, {
            type: "line",
            data: {
                labels: queryLabels,
                datasets: [
                    {
                        label: "TF-IDF AP",
                        data: tfidfAPs,
                        borderColor: COLOR_TFIDF.border,
                        backgroundColor: COLOR_TFIDF.fill,
                        tension: 0.25,
                        pointRadius: 5,
                        pointHoverRadius: 8,
                        borderWidth: 2.5
                    },
                    {
                        label: "Okapi BM25 AP",
                        data: bm25APs,
                        borderColor: COLOR_BM25.border,
                        backgroundColor: COLOR_BM25.fill,
                        tension: 0.25,
                        pointRadius: 5,
                        pointHoverRadius: 8,
                        borderWidth: 2.5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        min: 0,
                        max: 1.0,
                        title: { display: true, text: "Average Precision (AP)", font: { weight: "bold" } },
                        ticks: {
                            stepSize: 0.2,
                            callback: function (val) {
                                return val.toFixed(2);
                            }
                        },
                        grid: { color: "rgba(0, 0, 0, 0.06)" }
                    },
                    x: {
                        title: { display: true, text: "Kueri Benchmark (Q1 - Q12)", font: { weight: "bold" } },
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        position: "top",
                        labels: { font: { size: 12, weight: "bold" }, usePointStyle: true }
                    },
                    tooltip: {
                        backgroundColor: "rgba(30, 41, 59, 0.95)",
                        padding: 10,
                        cornerRadius: 8,
                        callbacks: {
                            title: function (items) {
                                const idx = items[0].dataIndex;
                                return `Q${idx + 1}: "${queryTitles[idx]}"`;
                            },
                            label: function (ctx) {
                                return ` ${ctx.dataset.label}: ${ctx.raw.toFixed(4)}`;
                            }
                        }
                    }
                }
            }
        });
    }
}
