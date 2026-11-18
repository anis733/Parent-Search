"""
Web Crawler untuk Mesin Pencari Panduan Parenting & Tumbuh Kembang Anak
Kelompok 11:
1. M. Anis Fathin
2. Muhammad Razi Siregar
3. Fachraja Ramadhan Sukma

Target Web:
- popmama.com (baby, kid, pregnancy)
- id.theasianparent.com
- parenting.co.id

Mengumpulkan minimal 300 artikel riil dengan URL asli yang aktif (bukan dummy).
"""

import os
import re
import json
import time
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(BASE_DIR, "corpus")
TARGET_COUNT = 300

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
}

def fetch_sitemap_urls():
    """Mengambil kandidat URL artikel riil dari sitemap website target."""
    candidate_urls = []
    
    # 1. Popmama sitemaps
    popmama_sitemaps = [
        ("https://www.popmama.com/baby/sitemap-web.xml", "popmama.com"),
        ("https://www.popmama.com/pregnancy/sitemap-web.xml", "popmama.com"),
    ]
    for sm_url, src in popmama_sitemaps:
        try:
            resp = requests.get(sm_url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                locs = [e.text for e in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
                for l in locs:
                    if l and ('/baby/' in l or '/pregnancy/' in l or '/kid/' in l):
                        candidate_urls.append((l.strip(), src))
        except Exception as e:
            print(f"Gagal mengambil sitemap {sm_url}: {e}")

    # 2. TheAsianParent sitemaps
    asianparent_sitemaps = [
        ("https://id.theasianparent.com/post-sitemap.xml", "id.theasianparent.com"),
        ("https://id.theasianparent.com/post-sitemap2.xml", "id.theasianparent.com"),
        ("https://id.theasianparent.com/post-sitemap3.xml", "id.theasianparent.com"),
        ("https://id.theasianparent.com/post-sitemap4.xml", "id.theasianparent.com"),
    ]
    for sm_url, src in asianparent_sitemaps:
        try:
            resp = requests.get(sm_url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                locs = [e.text for e in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
                for l in locs:
                    if l and not any(skip in l for skip in ['/author/', '/category/', '/tag/', '/privacy']):
                        candidate_urls.append((l.strip(), src))
        except Exception as e:
            print(f"Gagal mengambil sitemap {sm_url}: {e}")

    print(f"Total URL kandidat terkumpul: {len(candidate_urls)}")
    return candidate_urls

def scrape_single_article(url, source):
    """Mendownload dan mengekstrak judul serta teks artikel dari URL riil."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.content, "html.parser")

        # Ekstraksi Judul
        title_tag = soup.find("h1")
        if not title_tag:
            return None
        title = title_tag.get_text(strip=True)
        if len(title) < 5 or "oops" in title.lower() or "404" in title.lower():
            return None

        # Ekstraksi Konten
        content_div = (
            soup.find("div", class_="content-post") or
            soup.find("div", class_="read__content") or
            soup.find("article") or
            soup.find("div", class_="article-content")
        )

        paragraphs = []
        if content_div:
            p_tags = content_div.find_all("p")
        else:
            p_tags = soup.find_all("p")

        for p in p_tags:
            t = p.get_text(strip=True)
            # Filter teks pendek, navigasi, atau disclaimer iklan
            if len(t) > 35 and not any(kw in t.lower() for kw in ["kebijakan privasi", "pedoman komunitas", "peta situs", "copyright", "hak cipta"]):
                paragraphs.append(t)

        full_content = "\n\n".join(paragraphs)

        # Validasi konten artikel harus cukup panjang (minimal 200 karakter)
        if len(full_content) < 200:
            return None

        return {
            "title": title,
            "url": url,
            "content": full_content,
            "source": source,
            "date_crawled": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception:
        return None

def run_crawler():
    os.makedirs(CORPUS_DIR, exist_ok=True)
    print("=" * 65)
    print("MEMULAI WEB CRAWLER REAL UNTUK PARENTING & TUMBUH KEMBANG ANAK")
    print(f"Target Dokumen: {TARGET_COUNT}")
    print("=" * 65)

    candidates = fetch_sitemap_urls()
    if not candidates:
        print("Tidak ada kandidat URL yang dapat diambil.")
        return

    # Filter URL unik
    seen_urls = set()
    unique_candidates = []
    for u, src in candidates:
        if u not in seen_urls:
            seen_urls.add(u)
            unique_candidates.append((u, src))

    print(f"Kandidat URL unik: {len(unique_candidates)}. Memulai unduhan...")

    crawled_articles = []
    saved_count = 0

    # Gunakan thread pool untuk mengunduh secara cepat dan stabil
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {
            executor.submit(scrape_single_article, url, src): (url, src)
            for url, src in unique_candidates[:600]
        }

        for future in as_completed(future_to_url):
            if saved_count >= TARGET_COUNT:
                break

            result = future.result()
            if result:
                saved_count += 1
                doc_id = f"doc_{saved_count:03d}"
                result["id"] = doc_id

                # Simpan dokumen langsung ke file corpus/doc_xxx.json
                out_path = os.path.join(CORPUS_DIR, f"{doc_id}.json")
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

                crawled_articles.append(result)

                if saved_count % 25 == 0 or saved_count == TARGET_COUNT:
                    print(f"  [{saved_count}/{TARGET_COUNT}] Berhasil crawl: {result['title'][:50]}... ({result['source']})")

    print("=" * 65)
    print(f"CRAWLING SELESAI! {saved_count} dokumen riil berhasil disimpan di:")
    print(f"{CORPUS_DIR}")
    print("Semua URL adalah tautan aktif dan dapat dibuka langsung di browser.")
    print("=" * 65)

if __name__ == "__main__":
    run_crawler()
