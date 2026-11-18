"""
Generate 300 synthetic parenting & child development documents in Bahasa Indonesia.
Each document is saved as a JSON file in the corpus/ directory.
"""
import json
import os
import random
from datetime import datetime, timedelta

CORPUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus")
os.makedirs(CORPUS_DIR, exist_ok=True)

SOURCES = [
    {"name": "theasianparent.com/id", "base_url": "https://id.theasianparent.com/"},
    {"name": "popmama.com", "base_url": "https://www.popmama.com/"},
    {"name": "parenting.co.id", "base_url": "https://www.parenting.co.id/"},
]

# Topic templates with title patterns and content paragraphs
TOPICS = [
    {
        "category": "ASI & Menyusui",
        "titles": [
            "Panduan Lengkap Menyusui untuk Ibu Baru",
            "Manfaat ASI Eksklusif untuk Bayi 0-6 Bulan",
            "Tips Mengatasi ASI Seret pada Ibu Menyusui",
            "Posisi Menyusui yang Benar dan Nyaman",
            "Cara Menyimpan ASI Perah yang Tepat",
            "Makanan Pelancar ASI yang Wajib Dikonsumsi Ibu",
            "Tanda Bayi Cukup Mendapat ASI",
            "Menyusui Saat Ibu Sakit: Aman atau Tidak?",
            "Perlengkapan Menyusui yang Harus Disiapkan",
            "Kapan Waktu yang Tepat untuk Menyapih Anak",
            "Mengatasi Puting Lecet Saat Menyusui",
            "Donor ASI: Hal yang Perlu Diketahui",
            "ASI Booster Alami untuk Meningkatkan Produksi ASI",
            "Perbedaan ASI dan Susu Formula",
            "Tantangan Menyusui dan Cara Mengatasinya",
        ],
        "contents": [
            "Air Susu Ibu (ASI) merupakan makanan terbaik untuk bayi yang mengandung semua nutrisi yang dibutuhkan untuk tumbuh kembang optimal. WHO merekomendasikan pemberian ASI eksklusif selama 6 bulan pertama kehidupan bayi. ASI mengandung antibodi yang membantu melindungi bayi dari berbagai penyakit infeksi. Kolostrum, ASI pertama yang keluar setelah melahirkan, sangat kaya akan antibodi dan nutrisi penting.",
            "Menyusui adalah proses alami namun tidak selalu mudah bagi setiap ibu. Banyak ibu baru mengalami kesulitan dalam proses menyusui, mulai dari puting lecet, ASI yang belum lancar, hingga posisi menyusui yang belum tepat. Penting bagi ibu untuk mendapatkan dukungan dari keluarga dan tenaga kesehatan. Konsultasi dengan konselor laktasi dapat membantu mengatasi berbagai masalah menyusui.",
            "Produksi ASI bekerja berdasarkan prinsip supply and demand. Semakin sering bayi menyusu, semakin banyak ASI yang diproduksi. Ibu perlu menyusui minimal 8-12 kali dalam 24 jam pada minggu-minggu awal. Pastikan bayi melekat dengan benar pada payudara untuk memastikan transfer ASI yang efektif. Tanda bayi mendapat cukup ASI antara lain berat badan naik sesuai kurva pertumbuhan dan buang air kecil minimal 6 kali sehari.",
            "Penyimpanan ASI perah harus dilakukan dengan benar agar kualitas ASI tetap terjaga. ASI segar dapat disimpan pada suhu ruangan selama 4-6 jam, di lemari es selama 3-5 hari, dan di freezer hingga 6 bulan. Gunakan wadah yang bersih dan steril, beri label tanggal perah, dan hangatkan ASI beku dengan cara direndam dalam air hangat, bukan dengan microwave.",
        ]
    },
    {
        "category": "MPASI",
        "titles": [
            "Panduan MPASI 6 Bulan Pertama untuk Bayi",
            "Resep MPASI Sehat dan Bergizi untuk Bayi",
            "Jadwal Pemberian MPASI yang Tepat",
            "Tanda Bayi Siap Menerima MPASI",
            "Makanan yang Harus Dihindari Saat MPASI",
            "MPASI Homemade vs MPASI Instan: Mana yang Lebih Baik?",
            "Tekstur MPASI Sesuai Usia Bayi",
            "Baby Led Weaning: Metode MPASI Modern",
            "Menu MPASI 4 Bintang untuk Bayi",
            "Mengatasi Bayi yang Susah Makan MPASI",
            "Alergi Makanan pada Bayi Saat MPASI",
            "MPASI dengan Bahan Lokal Indonesia",
            "Tips Menyiapkan MPASI Praktis untuk Ibu Bekerja",
            "Porsi MPASI yang Tepat Sesuai Usia",
            "Finger Food untuk Bayi: Kapan dan Bagaimana",
        ],
        "contents": [
            "Makanan Pendamping ASI (MPASI) diberikan mulai usia 6 bulan ketika ASI saja sudah tidak cukup memenuhi kebutuhan nutrisi bayi yang semakin meningkat. MPASI pertama sebaiknya berupa puree halus dengan tekstur yang lembut. Mulailah dengan satu jenis makanan terlebih dahulu untuk mengidentifikasi kemungkinan alergi. WHO merekomendasikan MPASI diberikan 2-3 kali sehari pada usia 6-8 bulan.",
            "Pemberian MPASI harus memperhatikan prinsip empat bintang, yaitu mengandung karbohidrat, protein hewani, protein nabati, dan sayur atau buah. Contoh menu MPASI 4 bintang adalah nasi tim dengan ayam, tahu, dan wortel yang dihaluskan. Variasi menu sangat penting untuk memperkenalkan berbagai rasa dan tekstur pada bayi serta memastikan asupan gizi yang seimbang.",
            "Baby Led Weaning (BLW) adalah metode pemberian MPASI di mana bayi diberi makanan dalam bentuk potongan yang bisa digenggam, bukan puree. Metode ini melatih kemampuan motorik halus bayi dan membantu bayi belajar mengunyah. Namun, orang tua perlu waspada terhadap risiko tersedak. Pastikan makanan dipotong sesuai ukuran yang aman dan selalu awasi bayi saat makan.",
            "Tekstur MPASI perlu ditingkatkan secara bertahap seiring bertambahnya usia bayi. Pada usia 6-8 bulan, berikan puree halus hingga kasar. Usia 9-11 bulan, berikan makanan yang dicincang halus atau finger food lembut. Usia 12 bulan ke atas, bayi sudah bisa makan makanan keluarga dengan tekstur yang disesuaikan. Peningkatan tekstur yang tepat waktu penting untuk perkembangan kemampuan mengunyah bayi.",
        ]
    },
    {
        "category": "Vaksinasi & Imunisasi",
        "titles": [
            "Jadwal Imunisasi Lengkap untuk Anak 0-18 Bulan",
            "Pentingnya Vaksinasi untuk Melindungi Anak",
            "Efek Samping Vaksin dan Cara Mengatasinya",
            "Vaksin Wajib vs Vaksin Tambahan: Apa Bedanya?",
            "Mitos dan Fakta Seputar Vaksinasi Anak",
            "Vaksin COVID-19 untuk Anak: Yang Perlu Diketahui",
            "Apa yang Terjadi Jika Anak Tidak Divaksin?",
            "Persiapan Sebelum Membawa Anak Vaksinasi",
            "Vaksin MR: Manfaat dan Jadwal Pemberiannya",
            "Imunisasi Dasar Lengkap Menurut Kemenkes RI",
            "Vaksin Booster untuk Anak: Kapan Diperlukan?",
            "Mengatasi Demam Setelah Imunisasi pada Bayi",
            "Vaksin PCV untuk Mencegah Pneumonia pada Anak",
            "Imunisasi Kejar untuk Anak yang Terlambat Vaksin",
            "Herd Immunity dan Pentingnya Vaksinasi Massal",
        ],
        "contents": [
            "Imunisasi adalah cara paling efektif untuk melindungi anak dari berbagai penyakit berbahaya. Program imunisasi nasional Indonesia mencakup vaksin BCG, DPT-HB-Hib, Polio, Campak-Rubella (MR), dan PCV. Setiap vaksin diberikan pada usia tertentu sesuai jadwal yang ditetapkan oleh Kementerian Kesehatan. Imunisasi dasar lengkap harus diberikan sebelum anak berusia 1 tahun.",
            "Efek samping vaksin umumnya ringan dan bersifat sementara. Reaksi yang umum terjadi meliputi demam ringan, nyeri atau bengkak di tempat suntikan, dan rewel. Efek samping ini biasanya hilang dalam 1-3 hari. Berikan paracetamol sesuai dosis jika anak mengalami demam. Kompres dingin dapat membantu mengurangi nyeri di tempat suntikan. Efek samping serius sangat jarang terjadi.",
            "Vaksinasi menciptakan kekebalan kelompok (herd immunity) yang melindungi anggota masyarakat yang tidak bisa divaksin, seperti bayi yang terlalu muda atau orang dengan gangguan sistem imun. Ketika cakupan vaksinasi tinggi, penyebaran penyakit menular dapat dicegah. Target cakupan imunisasi nasional adalah 95% untuk mencapai herd immunity yang efektif.",
            "Jadwal imunisasi anak di Indonesia mengikuti rekomendasi IDAI (Ikatan Dokter Anak Indonesia). Vaksin hepatitis B diberikan saat lahir, BCG pada usia 1 bulan, DPT-HB-Hib pada usia 2, 3, dan 4 bulan, Polio pada usia 1, 2, 3, dan 4 bulan, serta Campak-Rubella pada usia 9 bulan. Vaksin tambahan yang direkomendasikan termasuk Rotavirus, Influenza, Varisela, dan Hepatitis A.",
        ]
    },
    {
        "category": "Perkembangan Motorik",
        "titles": [
            "Tahapan Perkembangan Motorik Anak 0-12 Bulan",
            "Stimulasi Motorik Kasar untuk Bayi dan Balita",
            "Kapan Bayi Mulai Tengkurap, Duduk, dan Berjalan?",
            "Aktivitas Motorik Halus untuk Anak Usia 1-3 Tahun",
            "Tanda Keterlambatan Perkembangan Motorik Anak",
            "Mainan Edukatif untuk Melatih Motorik Anak",
            "Perkembangan Motorik Anak Usia Prasekolah",
            "Tummy Time: Manfaat dan Cara Melakukannya",
            "Latihan Koordinasi Mata-Tangan untuk Balita",
            "Milestone Perkembangan Anak yang Perlu Dipantau",
            "Melatih Keseimbangan pada Anak Balita",
            "Perkembangan Kemampuan Menulis pada Anak",
            "Fisioterapi untuk Anak dengan Keterlambatan Motorik",
            "Olahraga yang Cocok untuk Anak Usia 3-5 Tahun",
            "Sensori Integrasi dan Perkembangan Motorik Anak",
        ],
        "contents": [
            "Perkembangan motorik anak meliputi motorik kasar dan motorik halus. Motorik kasar melibatkan gerakan otot besar seperti merangkak, berdiri, dan berjalan. Motorik halus melibatkan gerakan otot kecil seperti menggenggam, menjepit, dan menulis. Setiap anak berkembang dengan kecepatan yang berbeda, namun ada milestone umum yang bisa dijadikan acuan oleh orang tua.",
            "Tummy time atau waktu tengkurap adalah aktivitas penting untuk perkembangan motorik bayi. Praktik ini membantu memperkuat otot leher, bahu, dan punggung bayi yang diperlukan untuk merangkak dan berjalan. Mulailah tummy time sejak bayi baru lahir, dimulai dari 3-5 menit beberapa kali sehari dan tingkatkan durasinya secara bertahap. Selalu awasi bayi selama tummy time.",
            "Stimulasi motorik halus pada anak usia 1-3 tahun dapat dilakukan melalui berbagai aktivitas seperti bermain plastisin, menyusun balok, meronce manik-manik, menggambar dengan krayon, dan bermain puzzle sederhana. Aktivitas-aktivitas ini melatih koordinasi mata-tangan, kekuatan jari, dan ketelitian yang diperlukan untuk kemampuan menulis di kemudian hari.",
            "Keterlambatan perkembangan motorik perlu dideteksi sedini mungkin agar dapat diberikan intervensi yang tepat. Tanda-tanda yang perlu diwaspadai antara lain: bayi belum bisa mengangkat kepala pada usia 4 bulan, belum bisa duduk tanpa bantuan pada usia 9 bulan, atau belum bisa berjalan pada usia 18 bulan. Konsultasikan dengan dokter anak jika Anda menemukan tanda-tanda tersebut.",
        ]
    },
    {
        "category": "Nutrisi Anak",
        "titles": [
            "Panduan Nutrisi Seimbang untuk Anak Usia 1-5 Tahun",
            "Makanan Sehat untuk Mendukung Pertumbuhan Anak",
            "Mengatasi Anak yang Pilih-pilih Makanan (Picky Eater)",
            "Kebutuhan Zat Besi pada Anak dan Sumbernya",
            "Menu Makan Sehat untuk Anak Sekolah",
            "Bahaya Junk Food bagi Kesehatan Anak",
            "Vitamin dan Mineral Penting untuk Tumbuh Kembang Anak",
            "Resep Camilan Sehat untuk Anak Balita",
            "Kalsium untuk Pertumbuhan Tulang Anak",
            "Pola Makan Anak yang Alergi Makanan",
            "Suplemen Vitamin untuk Anak: Perlu atau Tidak?",
            "Makanan Penambah Berat Badan Anak",
            "Gizi Buruk pada Anak: Penyebab dan Pencegahan",
            "Omega-3 dan Perkembangan Otak Anak",
            "Hidrasi yang Cukup untuk Anak Aktif",
        ],
        "contents": [
            "Nutrisi yang seimbang sangat penting untuk mendukung pertumbuhan dan perkembangan anak. Anak usia 1-5 tahun membutuhkan makanan yang mengandung karbohidrat, protein, lemak sehat, vitamin, dan mineral dalam proporsi yang tepat. Piring makan anak idealnya terdiri dari sepertiga karbohidrat, sepertiga protein, dan sepertiga sayur dan buah.",
            "Anak yang pilih-pilih makanan (picky eater) merupakan masalah umum yang dihadapi banyak orang tua. Strategi yang dapat dilakukan antara lain: memperkenalkan makanan baru secara bertahap, membuat tampilan makanan yang menarik, melibatkan anak dalam proses memasak, makan bersama keluarga, dan tidak memaksa anak makan. Penelitian menunjukkan bahwa anak mungkin perlu mencoba makanan baru hingga 15 kali sebelum menerimanya.",
            "Zat besi merupakan mineral penting yang dibutuhkan anak untuk pembentukan sel darah merah dan perkembangan otak. Kekurangan zat besi dapat menyebabkan anemia yang berdampak pada kemampuan belajar dan konsentrasi anak. Sumber zat besi yang baik antara lain daging merah, hati ayam, bayam, kacang-kacangan, dan sereal yang difortifikasi zat besi.",
            "Kebutuhan kalori anak berbeda-beda tergantung usia, berat badan, dan tingkat aktivitas. Anak usia 1-3 tahun membutuhkan sekitar 1000-1400 kalori per hari, sedangkan anak usia 4-5 tahun membutuhkan sekitar 1200-1600 kalori per hari. Pemberian makan sebaiknya dibagi menjadi 3 kali makan utama dan 2 kali camilan sehat. Hindari memberikan makanan tinggi gula dan garam berlebihan.",
        ]
    },
    {
        "category": "Pola Asuh",
        "titles": [
            "Pola Asuh Positif untuk Membentuk Karakter Anak",
            "Gentle Parenting: Mendidik Anak Tanpa Kekerasan",
            "Cara Mengatasi Tantrum pada Anak Balita",
            "Membangun Bonding yang Kuat dengan Anak",
            "Dampak Pola Asuh Otoriter terhadap Anak",
            "Tips Mendisiplinkan Anak dengan Cara yang Tepat",
            "Peran Ayah dalam Pengasuhan Anak",
            "Co-Parenting: Mengasuh Anak Bersama Pasangan",
            "Mengelola Screen Time Anak di Era Digital",
            "Cara Mengajarkan Anak Mandiri Sejak Dini",
            "Sibling Rivalry: Mengatasi Persaingan Antar Saudara",
            "Membesarkan Anak dengan Rasa Percaya Diri",
            "Komunikasi Efektif antara Orang Tua dan Anak",
            "Kesalahan Umum dalam Pola Asuh yang Harus Dihindari",
            "Mengajarkan Nilai-nilai Moral pada Anak",
        ],
        "contents": [
            "Pola asuh positif menekankan pada penghargaan, komunikasi yang baik, dan pemberian batasan yang jelas namun penuh kasih sayang. Pendekatan ini membantu anak mengembangkan rasa percaya diri, kemampuan sosial, dan regulasi emosi yang baik. Orang tua yang menerapkan pola asuh positif cenderung memiliki hubungan yang lebih erat dengan anak-anak mereka.",
            "Tantrum adalah ledakan emosi yang umum terjadi pada anak usia 1-4 tahun. Tantrum terjadi karena anak belum mampu mengekspresikan perasaannya dengan kata-kata. Cara mengatasi tantrum antara lain: tetap tenang, validasi perasaan anak, berikan pelukan jika anak mau, alihkan perhatian, dan ajarkan anak cara mengekspresikan emosi yang lebih baik. Hindari memenuhi keinginan anak saat tantrum karena akan memperkuat perilaku tersebut.",
            "Screen time atau waktu layar pada anak perlu dibatasi sesuai rekomendasi American Academy of Pediatrics. Anak di bawah 18 bulan sebaiknya tidak terpapar layar sama sekali kecuali video call. Anak usia 18-24 bulan boleh menonton program edukatif berkualitas tinggi dengan pendampingan orang tua. Anak usia 2-5 tahun dibatasi maksimal 1 jam per hari. Pastikan konten yang ditonton sesuai dengan usia anak.",
            "Peran ayah dalam pengasuhan anak sama pentingnya dengan peran ibu. Penelitian menunjukkan bahwa keterlibatan ayah secara aktif dalam pengasuhan berdampak positif pada perkembangan kognitif, emosional, dan sosial anak. Ayah dapat berperan melalui bermain bersama, membacakan cerita, membantu mengerjakan tugas, dan menjadi teladan yang baik. Quality time bersama ayah membantu anak merasa dicintai dan aman.",
        ]
    },
    {
        "category": "Kesehatan Anak",
        "titles": [
            "Mengenali Gejala Demam pada Anak dan Penanganannya",
            "Penyakit Umum pada Anak dan Cara Pencegahannya",
            "Pertolongan Pertama pada Anak Tersedak",
            "Cara Merawat Anak yang Sedang Sakit di Rumah",
            "Kapan Harus Membawa Anak ke Dokter?",
            "Alergi pada Anak: Jenis dan Penanganannya",
            "Menjaga Kesehatan Gigi Anak Sejak Dini",
            "Penyakit Kulit pada Anak: Ruam Popok hingga Eksim",
            "Diare pada Anak: Penyebab dan Cara Mengatasinya",
            "Infeksi Saluran Pernapasan pada Anak",
            "Pertolongan Pertama Luka pada Anak",
            "Kesehatan Mata Anak di Era Digital",
            "Gangguan Tidur pada Anak dan Solusinya",
            "Obesitas pada Anak: Faktor Risiko dan Pencegahan",
            "P3K untuk Anak: Perlengkapan yang Harus Ada di Rumah",
        ],
        "contents": [
            "Demam pada anak adalah mekanisme pertahanan tubuh melawan infeksi. Demam dikatakan terjadi ketika suhu tubuh anak di atas 37.5°C. Penanganan pertama meliputi memberikan cairan yang cukup, mengompres dengan air hangat, dan memberikan obat penurun panas seperti paracetamol sesuai dosis. Segera bawa ke dokter jika demam berlangsung lebih dari 3 hari atau disertai kejang.",
            "Kebersihan tangan yang baik adalah cara paling efektif untuk mencegah penyebaran penyakit pada anak. Ajarkan anak mencuci tangan dengan sabun dan air mengalir selama minimal 20 detik, terutama sebelum makan, setelah dari toilet, dan setelah bermain di luar. Selain itu, pastikan lingkungan rumah bersih dan ventilasi udara yang baik untuk mengurangi risiko infeksi saluran pernapasan.",
            "Diare pada anak dapat disebabkan oleh infeksi virus, bakteri, atau parasit. Penanganan utama diare adalah mencegah dehidrasi dengan memberikan oralit atau cairan rehidrasi oral. Terus berikan ASI atau makanan seperti biasa. Hindari memberikan obat anti-diare pada anak tanpa resep dokter. Tanda dehidrasi yang perlu diwaspadai meliputi mulut kering, mata cekung, menangis tanpa air mata, dan buang air kecil yang berkurang.",
            "Kesehatan gigi anak harus diperhatikan sejak gigi pertama tumbuh, biasanya sekitar usia 6 bulan. Bersihkan gigi bayi dengan kain lembut yang dibasahi air bersih. Mulai gunakan sikat gigi khusus bayi dengan pasta gigi berfluoride seukuran biji beras saat usia 1 tahun. Hindari kebiasaan minum susu dengan botol saat tidur karena dapat menyebabkan karies gigi. Kunjungi dokter gigi anak setiap 6 bulan.",
        ]
    },
    {
        "category": "Perkembangan Kognitif",
        "titles": [
            "Stimulasi Perkembangan Otak Anak Sejak Dini",
            "Aktivitas Bermain yang Merangsang Kecerdasan Anak",
            "Tahapan Perkembangan Bahasa Anak 0-5 Tahun",
            "Cara Mengajarkan Anak Membaca Sejak Dini",
            "Pentingnya Bermain untuk Perkembangan Kognitif Anak",
            "Musik dan Perkembangan Otak Anak",
            "Mengembangkan Kreativitas Anak Melalui Seni",
            "Tanda Anak Cerdas dan Cara Mendukungnya",
            "Metode Montessori untuk Anak Usia Dini",
            "Perkembangan Memori pada Anak Balita",
            "Bermain Peran dan Manfaatnya untuk Anak",
            "Kecerdasan Majemuk pada Anak: Teori Howard Gardner",
            "Mengajarkan Konsep Matematika Dasar pada Anak",
            "Bilingual: Mengajarkan Dua Bahasa pada Anak",
            "Critical Thinking: Melatih Berpikir Kritis pada Anak",
        ],
        "contents": [
            "Perkembangan otak anak paling pesat terjadi pada 1000 hari pertama kehidupan, yaitu sejak dalam kandungan hingga usia 2 tahun. Stimulasi yang tepat pada periode ini sangat penting untuk membentuk koneksi saraf yang kuat. Stimulasi dapat berupa berbicara, bernyanyi, membacakan buku, dan bermain bersama anak. Interaksi yang responsif dan penuh kasih sayang juga berkontribusi besar pada perkembangan otak anak.",
            "Bermain adalah cara utama anak belajar tentang dunia di sekitarnya. Melalui bermain, anak mengembangkan kemampuan kognitif, sosial, emosional, dan fisik. Jenis permainan yang baik untuk perkembangan kognitif antara lain puzzle, balok susun, permainan peran, permainan memori, dan permainan kreatif seperti menggambar dan bermain plastisin. Biarkan anak bermain secara bebas dan terarah.",
            "Perkembangan bahasa anak dimulai sejak lahir. Bayi 0-3 bulan mulai mengenal suara dan berceloteh. Usia 6-9 bulan mulai mengoceh dengan suku kata berulang. Usia 12 bulan mulai mengucapkan kata pertama. Usia 18-24 bulan mulai menggabungkan dua kata. Usia 3-5 tahun kemampuan bahasa berkembang pesat dengan kalimat yang semakin kompleks. Stimulasi bahasa yang baik meliputi banyak berbicara, membacakan cerita, dan bernyanyi bersama anak.",
            "Metode Montessori menekankan pada kemandirian anak, pembelajaran melalui pengalaman langsung, dan lingkungan yang disiapkan sesuai kebutuhan anak. Prinsip dasar Montessori meliputi menghormati anak sebagai individu, mengikuti minat anak, menyediakan material belajar yang konkret, dan memberi kebebasan dalam batas-batas yang jelas. Metode ini dapat diterapkan di rumah maupun di sekolah.",
        ]
    },
    {
        "category": "Kesehatan Ibu",
        "titles": [
            "Pemulihan Pasca Melahirkan yang Perlu Diketahui",
            "Baby Blues vs Depresi Pasca Melahirkan",
            "Nutrisi Penting untuk Ibu Menyusui",
            "Tips Menjaga Kesehatan Mental Ibu Baru",
            "Olahraga Aman Setelah Melahirkan",
            "Mengatasi Kelelahan pada Ibu Baru",
            "Self-Care untuk Ibu: Pentingnya Me Time",
            "Kontrasepsi Setelah Melahirkan: Pilihan yang Tersedia",
            "Nutrisi Ibu Hamil Trimester Pertama",
            "Persiapan Persalinan Normal dan Caesar",
            "Mengatasi Morning Sickness Saat Hamil",
            "Kesehatan Mental Ibu dan Dampaknya pada Anak",
            "Work-Life Balance untuk Ibu Bekerja",
            "Perawatan Luka Caesar yang Benar",
            "Suplemen yang Dibutuhkan Ibu Hamil dan Menyusui",
        ],
        "contents": [
            "Pemulihan pasca melahirkan membutuhkan waktu 6-8 minggu untuk persalinan normal dan 8-12 minggu untuk operasi caesar. Selama masa ini, ibu perlu istirahat yang cukup, makan makanan bergizi, dan menjaga kebersihan luka. Penting untuk tidak mengangkat beban berat dan menghindari aktivitas fisik yang terlalu berat. Dukungan keluarga sangat diperlukan selama masa pemulihan.",
            "Baby blues adalah perubahan suasana hati yang umum dialami 50-80% ibu baru dalam 2 minggu pertama setelah melahirkan. Gejala meliputi menangis tanpa alasan, mudah tersinggung, dan merasa cemas. Baby blues biasanya hilang dengan sendirinya. Namun jika gejala berlangsung lebih dari 2 minggu dan semakin berat, bisa jadi itu merupakan depresi pasca melahirkan yang memerlukan penanganan profesional.",
            "Ibu menyusui membutuhkan tambahan kalori sekitar 300-500 kalori per hari dibandingkan saat tidak menyusui. Nutrisi yang penting untuk ibu menyusui meliputi protein, kalsium, zat besi, vitamin D, dan asam lemak omega-3. Minum air putih yang cukup juga penting untuk menjaga produksi ASI. Hindari alkohol dan batasi konsumsi kafein karena dapat masuk ke dalam ASI.",
            "Kesehatan mental ibu sangat berpengaruh terhadap kualitas pengasuhan dan perkembangan anak. Ibu yang mengalami stres, kecemasan, atau depresi mungkin kesulitan merespons kebutuhan anak secara optimal. Penting bagi ibu untuk meluangkan waktu untuk diri sendiri, meminta bantuan ketika membutuhkannya, dan tidak ragu berkonsultasi dengan profesional kesehatan mental.",
        ]
    },
    {
        "category": "Keamanan Anak",
        "titles": [
            "Tips Childproofing Rumah untuk Keamanan Bayi",
            "Keselamatan Anak di Kolam Renang dan Pantai",
            "Car Seat: Pentingnya Kursi Mobil untuk Anak",
            "Bahaya Benda Kecil dan Risiko Tersedak pada Anak",
            "Keamanan Internet untuk Anak dan Remaja",
            "Mencegah Kecelakaan di Rumah pada Anak Balita",
            "Tips Memilih Mainan yang Aman untuk Anak",
            "Pertolongan Pertama Jika Anak Terjatuh",
            "Keselamatan Anak Saat Bermain di Luar Rumah",
            "Bahaya Produk Rumah Tangga bagi Anak",
            "Mengajarkan Anak tentang Stranger Danger",
            "Keamanan Pangan untuk Anak: Mencegah Keracunan",
            "Tips Perjalanan Aman dengan Bayi dan Balita",
            "Sun Safety: Melindungi Kulit Anak dari Sinar UV",
            "Mengajarkan Anak Mengenali Sentuhan yang Tidak Pantas",
        ],
        "contents": [
            "Childproofing atau pengamanan rumah sangat penting untuk melindungi bayi dan balita dari kecelakaan. Langkah-langkah yang perlu dilakukan meliputi: memasang pengaman stopkontak, mengunci lemari yang berisi bahan berbahaya, memasang pagar pengaman di tangga, memastikan perabotan berat terpasang dengan aman di dinding, dan menjauhkan benda-benda kecil yang bisa tertelan.",
            "Kecelakaan di rumah merupakan penyebab cedera yang paling umum pada anak balita. Jenis kecelakaan yang sering terjadi meliputi jatuh, terbakar, tersedak, dan keracunan. Pencegahan dapat dilakukan dengan mengawasi anak secara aktif, menghilangkan bahaya potensial, dan mengajarkan anak tentang keselamatan sesuai usianya. Selalu simpan nomor darurat di tempat yang mudah dijangkau.",
            "Penggunaan car seat atau kursi mobil khusus anak sangat penting untuk keselamatan anak saat berkendara. Anak di bawah 2 tahun sebaiknya duduk menghadap ke belakang. Anak usia 2-7 tahun menggunakan car seat menghadap ke depan dengan harness. Anak yang sudah lebih besar menggunakan booster seat hingga sabuk pengaman mobil pas dengan benar, biasanya saat tinggi anak mencapai 145 cm.",
            "Keamanan internet untuk anak menjadi semakin penting di era digital. Orang tua perlu mengawasi aktivitas online anak, menggunakan fitur parental control, mengajarkan anak tentang privasi dan keamanan online, serta membangun komunikasi terbuka tentang pengalaman online anak. Tetapkan aturan yang jelas tentang penggunaan internet dan media sosial.",
        ]
    },
    {
        "category": "Perkembangan Sosial-Emosional",
        "titles": [
            "Mengembangkan Kecerdasan Emosional Anak",
            "Cara Mengajarkan Empati pada Anak",
            "Mengatasi Rasa Takut dan Kecemasan pada Anak",
            "Membangun Keterampilan Sosial Anak Sejak Dini",
            "Attachment Parenting dan Bonding Anak-Orang Tua",
            "Mengenali Tanda Stres pada Anak",
            "Cara Membantu Anak Mengekspresikan Emosi",
            "Bullying: Cara Melindungi Anak dari Perundungan",
            "Mempersiapkan Anak Masuk Sekolah Pertama Kali",
            "Mengajarkan Anak Berbagi dan Bergiliran",
            "Separation Anxiety pada Anak: Normal atau Tidak?",
            "Membangun Harga Diri Positif pada Anak",
            "Friendship: Membantu Anak Membangun Pertemanan",
            "Mengajarkan Anak Mengelola Kemarahan",
            "Perkembangan Emosional Anak Usia Prasekolah",
        ],
        "contents": [
            "Kecerdasan emosional (EQ) sama pentingnya dengan kecerdasan intelektual (IQ) untuk kesuksesan anak di masa depan. Kecerdasan emosional meliputi kemampuan mengenali emosi diri sendiri, mengelola emosi, memotivasi diri, berempati, dan membangun hubungan sosial yang baik. Orang tua dapat membantu mengembangkan EQ anak dengan menjadi contoh yang baik dalam mengelola emosi.",
            "Separation anxiety atau kecemasan berpisah adalah hal yang normal pada anak usia 8-14 bulan. Anak merasa cemas dan menangis ketika berpisah dari orang tua atau pengasuh utamanya. Hal ini menunjukkan bahwa anak telah membentuk ikatan yang kuat dengan orang tuanya. Cara mengatasinya adalah dengan memberikan transisi yang bertahap, memastikan anak bahwa orang tua akan kembali, dan menciptakan rutinitas perpisahan yang konsisten.",
            "Bullying atau perundungan dapat berdampak serius pada kesehatan mental dan emosional anak. Tanda anak menjadi korban bullying antara lain: perubahan perilaku, menolak pergi ke sekolah, menghindari situasi sosial, dan perubahan pola makan atau tidur. Orang tua perlu membangun komunikasi terbuka dengan anak, mengajarkan cara merespons bullying, dan bekerja sama dengan pihak sekolah untuk mengatasi masalah ini.",
            "Mempersiapkan anak masuk sekolah pertama kali membutuhkan persiapan fisik, emosional, dan sosial. Ajak anak mengunjungi sekolah sebelum hari pertama, ceritakan hal-hal menyenangkan tentang sekolah, latih kemandirian anak dalam hal makan, ke toilet, dan berpakaian. Pastikan anak terbiasa berinteraksi dengan teman sebaya melalui playdate atau kegiatan kelompok.",
        ]
    },
    {
        "category": "Tidur Anak",
        "titles": [
            "Panduan Pola Tidur Bayi 0-12 Bulan",
            "Sleep Training: Melatih Bayi Tidur Sendiri",
            "Tips Agar Bayi Tidur Nyenyak Sepanjang Malam",
            "Rutinitas Sebelum Tidur yang Membantu Anak Istirahat",
            "Kebutuhan Jam Tidur Anak Sesuai Usia",
            "Night Terror vs Mimpi Buruk pada Anak",
            "Bahaya Co-Sleeping dan Panduan SIDS",
            "Mengatasi Bayi yang Sering Terbangun di Malam Hari",
            "Transisi dari Ranjang Bayi ke Tempat Tidur Anak",
            "Mengapa Tidur Siang Penting untuk Balita",
            "Melatonin untuk Anak: Aman atau Tidak?",
            "Lingkungan Tidur yang Ideal untuk Bayi",
            "Mengatur Jadwal Tidur Anak Saat Liburan",
            "Sleep Regression: Mengapa Bayi Tiba-tiba Sulit Tidur",
            "Dongeng Sebelum Tidur dan Manfaatnya",
        ],
        "contents": [
            "Kebutuhan tidur bayi bervariasi sesuai usia. Bayi baru lahir tidur 16-17 jam sehari, bayi 3-6 bulan tidur 14-15 jam, bayi 6-12 bulan tidur 12-14 jam. Penting untuk membangun rutinitas tidur yang konsisten untuk membantu bayi mengenal pola tidur yang teratur. Rutinitas sebelum tidur dapat berupa mandi, mengganti pakaian, membacakan cerita, dan menyanyikan lagu nina bobo.",
            "Sleep training adalah proses mengajarkan bayi untuk tidur sendiri tanpa bantuan orang tua. Ada beberapa metode sleep training, termasuk Ferber method (graduated extinction), cry it out, pick up put down, dan fading method. Setiap metode memiliki kelebihan dan kekurangan. Penting untuk memilih metode yang sesuai dengan temperamen bayi dan kenyamanan orang tua. Sleep training umumnya dapat dimulai pada usia 4-6 bulan.",
            "Sudden Infant Death Syndrome (SIDS) atau sindrom kematian bayi mendadak dapat dicegah dengan mengikuti panduan tidur yang aman. Bayi harus tidur dalam posisi telentang, di permukaan yang rata dan keras, tanpa bantal, selimut tebal, atau boneka di sekitarnya. Suhu ruangan yang nyaman dan sirkulasi udara yang baik juga penting. Hindari merokok di dekat bayi dan pastikan bayi tidak kepanasan.",
            "Night terror berbeda dengan mimpi buruk. Night terror terjadi pada fase tidur dalam dan anak tidak benar-benar terbangun, biasanya pada sepertiga pertama malam. Anak mungkin menjerit, berkeringat, dan terlihat ketakutan tapi tidak merespons orang tua. Night terror lebih umum pada anak usia 3-8 tahun dan biasanya hilang dengan sendirinya. Pastikan anak cukup tidur dan memiliki rutinitas tidur yang teratur untuk mengurangi frekuensi night terror.",
        ]
    },
    {
        "category": "Tumbuh Kembang Usia Sekolah",
        "titles": [
            "Mempersiapkan Anak untuk Masuk SD",
            "Tips Belajar Efektif untuk Anak Usia Sekolah",
            "Peran Orang Tua dalam Pendidikan Anak",
            "Mengatasi Kesulitan Belajar pada Anak",
            "Homeschooling: Alternatif Pendidikan untuk Anak",
            "Mengembangkan Minat dan Bakat Anak",
            "Dampak Tekanan Akademik pada Anak",
            "Les Tambahan: Perlu atau Tidak untuk Anak SD?",
            "Mengajarkan Anak Time Management",
            "Pendidikan Karakter di Rumah dan Sekolah",
            "PAUD dan Manfaatnya untuk Perkembangan Anak",
            "Memilih Sekolah yang Tepat untuk Anak",
            "Anak Berkebutuhan Khusus: Pendidikan Inklusif",
            "Disiplin Positif di Rumah dan Sekolah",
            "Memotivasi Anak untuk Senang Belajar",
        ],
        "contents": [
            "Kesiapan sekolah tidak hanya tentang kemampuan akademik, tetapi juga kematangan sosial-emosional, kemandirian, dan kemampuan mengikuti instruksi. Anak yang siap masuk SD umumnya sudah bisa duduk tenang selama 15-30 menit, mengikuti aturan sederhana, berinteraksi dengan teman sebaya, dan melakukan tugas-tugas dasar secara mandiri seperti makan, ke toilet, dan berpakaian.",
            "Orang tua memiliki peran penting dalam mendukung pendidikan anak. Caranya antara lain: menciptakan lingkungan belajar yang kondusif di rumah, membantu anak mengerjakan PR tanpa mengambil alih, membacakan buku bersama, berkomunikasi aktif dengan guru, dan menunjukkan antusiasme terhadap proses belajar anak. Hindari memberikan tekanan berlebihan tentang nilai dan peringkat.",
            "Kesulitan belajar pada anak bisa disebabkan oleh berbagai faktor seperti gangguan belajar spesifik (disleksia, diskalkulia, disgrafia), masalah konsentrasi (ADHD), atau faktor lingkungan. Deteksi dini sangat penting agar anak mendapatkan intervensi yang tepat. Konsultasikan dengan psikolog anak atau ahli pendidikan khusus untuk evaluasi dan penanganan yang sesuai.",
            "Homeschooling menjadi pilihan pendidikan alternatif yang semakin populer di Indonesia. Keuntungannya meliputi kurikulum yang disesuaikan dengan kebutuhan dan minat anak, jadwal yang fleksibel, dan perhatian individual yang maksimal. Namun, orang tua perlu memastikan anak tetap memiliki kesempatan bersosialisasi melalui kegiatan komunitas, olahraga, atau kelas ekstrakurikuler.",
        ]
    },
    {
        "category": "Pertumbuhan Fisik",
        "titles": [
            "Memantau Pertumbuhan Anak dengan KMS",
            "Stunting: Penyebab, Dampak, dan Pencegahannya",
            "Berat Badan Ideal Anak Sesuai Usia",
            "Faktor-faktor yang Mempengaruhi Pertumbuhan Anak",
            "Hormon Pertumbuhan dan Tinggi Badan Anak",
            "Kapan Anak Perlu Periksa ke Dokter Tumbuh Kembang?",
            "Kurva Pertumbuhan WHO untuk Anak Indonesia",
            "Gizi Seimbang untuk Mencegah Stunting",
            "Olahraga dan Aktivitas Fisik untuk Pertumbuhan Anak",
            "Pubertas Dini pada Anak: Penyebab dan Penanganan",
            "Memantau Lingkar Kepala Bayi",
            "Pertumbuhan Gigi Anak: Jadwal dan Perawatan",
            "Wasting dan Underweight pada Anak Balita",
            "Suplemen Pertumbuhan untuk Anak: Fakta dan Mitos",
            "Perbedaan Pertumbuhan Anak Laki-laki dan Perempuan",
        ],
        "contents": [
            "Stunting atau perawakan pendek merupakan masalah gizi kronis yang disebabkan oleh asupan gizi yang kurang dalam jangka waktu lama. Indonesia masih menghadapi masalah stunting dengan prevalensi sekitar 21.6% pada tahun 2022. Pencegahan stunting dimulai dari pemenuhan gizi sejak dalam kandungan, pemberian ASI eksklusif, MPASI yang bergizi, dan pemantauan pertumbuhan secara rutin melalui posyandu.",
            "Kartu Menuju Sehat (KMS) adalah alat pemantauan pertumbuhan anak yang digunakan di posyandu. KMS menampilkan kurva pertumbuhan berat badan menurut usia yang membantu mendeteksi gangguan pertumbuhan secara dini. Anak yang pertumbuhannya baik akan mengikuti pita hijau pada KMS. Jika berat badan anak tidak naik selama 2 bulan berturut-turut atau berada di bawah garis merah, perlu dilakukan evaluasi lebih lanjut.",
            "Aktivitas fisik sangat penting untuk pertumbuhan dan perkembangan anak. Anak usia 1-5 tahun direkomendasikan untuk aktif bergerak minimal 180 menit per hari, termasuk 60 menit aktivitas fisik intensitas sedang hingga tinggi untuk anak usia 3-5 tahun. Aktivitas fisik membantu memperkuat tulang dan otot, mengembangkan koordinasi, menjaga berat badan ideal, dan meningkatkan kesehatan kardiovaskular.",
            "Pertumbuhan gigi susu dimulai sekitar usia 6 bulan dan lengkap pada usia 2.5-3 tahun dengan total 20 gigi susu. Urutan tumbuh gigi umumnya dimulai dari gigi seri bawah depan. Gejala tumbuh gigi meliputi gusi bengkak, air liur berlebih, rewel, dan keinginan menggigit. Berikan teething ring yang sudah didinginkan atau gosok gusi bayi dengan jari yang bersih untuk meredakan ketidaknyamanan.",
        ]
    },
    {
        "category": "Parenting Modern",
        "titles": [
            "Digital Parenting di Era Teknologi",
            "Mindful Parenting: Pengasuhan Penuh Kesadaran",
            "Positive Discipline: Disiplin Tanpa Hukuman Fisik",
            "Helicopter Parenting vs Free-Range Parenting",
            "Mengajarkan Financial Literacy pada Anak",
            "Eco-Friendly Parenting: Mengajarkan Cinta Lingkungan",
            "Parenting Anak Generasi Alpha",
            "Single Parenting: Tips Mengasuh Anak Sendiri",
            "Grandparenting: Peran Kakek Nenek dalam Pengasuhan",
            "Parenting Anak dengan Kebutuhan Khusus",
            "Conscious Parenting: Menjadi Orang Tua yang Sadar",
            "Work from Home dengan Anak: Tips dan Strategi",
            "Membangun Tradisi Keluarga yang Bermakna",
            "Menghadapi Fase Terrible Two pada Anak",
            "Parenting Islami: Mendidik Anak Sesuai Nilai Agama",
        ],
        "contents": [
            "Di era digital, orang tua menghadapi tantangan baru dalam mengasuh anak. Anak-anak terpapar teknologi sejak usia sangat dini, sehingga orang tua perlu bijak dalam mengelola penggunaan gadget. Tetapkan aturan screen time yang jelas, pilih konten yang edukatif, dan jadilah role model dalam penggunaan teknologi. Penting juga untuk memastikan bahwa interaksi langsung tetap menjadi prioritas dalam keluarga.",
            "Mindful parenting adalah pendekatan pengasuhan yang menekankan pada kehadiran penuh dan kesadaran saat berinteraksi dengan anak. Praktik ini membantu orang tua merespons anak dengan tenang dan bijaksana, bukan bereaksi secara emosional. Teknik mindful parenting meliputi mendengarkan aktif, mengamati tanpa menghakimi, dan merespons dengan penuh perhatian. Penelitian menunjukkan bahwa mindful parenting dapat mengurangi stres orang tua dan meningkatkan kualitas hubungan orang tua-anak.",
            "Financial literacy atau literasi keuangan sebaiknya diajarkan pada anak sejak dini. Mulai dengan konsep dasar seperti menabung, perbedaan antara kebutuhan dan keinginan, dan nilai uang. Berikan anak uang saku dan ajarkan cara mengelolanya. Gunakan celengan transparan agar anak bisa melihat uangnya bertambah. Seiring bertambahnya usia, ajarkan konsep yang lebih kompleks seperti anggaran, investasi, dan donasi.",
            "Fase terrible two biasanya terjadi pada anak usia 18 bulan hingga 3 tahun. Pada fase ini, anak mulai mengembangkan kemandirian dan sering mengatakan 'tidak'. Tantrum, perubahan suasana hati yang cepat, dan perilaku menantang adalah hal yang normal pada fase ini. Orang tua perlu bersabar, konsisten dengan batasan, memberikan pilihan terbatas, dan memuji perilaku positif anak.",
        ]
    },
]

EXTRA_PARAGRAPHS = [
    "Konsultasikan dengan dokter anak atau tenaga kesehatan profesional jika Anda memiliki kekhawatiran tentang tumbuh kembang anak. Deteksi dini dan intervensi yang tepat dapat membuat perbedaan besar dalam perkembangan anak.",
    "Setiap anak adalah unik dan berkembang dengan kecepatannya sendiri. Hindari membandingkan anak dengan anak lain. Yang terpenting adalah memberikan stimulasi yang tepat, kasih sayang yang cukup, dan lingkungan yang mendukung untuk tumbuh kembang optimal.",
    "Orang tua tidak perlu sempurna. Yang dibutuhkan anak adalah orang tua yang hadir, responsif, dan terus belajar. Jangan ragu untuk meminta bantuan ketika merasa kewalahan. Bergabung dengan komunitas parenting dapat memberikan dukungan dan berbagi pengalaman.",
    "Pola hidup sehat harus ditanamkan sejak dini. Ajak anak untuk aktif bergerak, makan makanan bergizi, cukup tidur, dan menjaga kebersihan. Kebiasaan baik yang terbentuk di masa kecil akan terbawa hingga dewasa.",
    "Komunikasi yang terbuka dan hangat antara orang tua dan anak merupakan kunci pengasuhan yang berhasil. Luangkan waktu setiap hari untuk berbicara dengan anak, mendengarkan ceritanya, dan menunjukkan bahwa Anda peduli dengan perasaan dan pengalamannya.",
    "Lingkungan yang aman dan penuh kasih sayang adalah fondasi penting bagi tumbuh kembang anak. Pastikan rumah menjadi tempat yang nyaman bagi anak untuk belajar, bermain, dan berkembang. Ciptakan rutinitas yang konsisten untuk memberikan rasa aman pada anak.",
    "Pendidikan anak dimulai dari rumah. Orang tua adalah guru pertama dan utama bagi anak. Setiap momen bersama anak adalah kesempatan untuk mengajarkan nilai-nilai kehidupan, berbagi pengetahuan, dan membangun karakter yang baik.",
    "Indonesia memiliki berbagai program pemerintah untuk mendukung tumbuh kembang anak, termasuk posyandu, PAUD, dan program pemberian makanan tambahan. Manfaatkan layanan kesehatan dan pendidikan yang tersedia di lingkungan Anda untuk memastikan anak tumbuh dan berkembang secara optimal.",
    "Penelitian menunjukkan bahwa intervensi dini pada masa kanak-kanak memiliki dampak jangka panjang yang signifikan terhadap kesehatan, pendidikan, dan kesejahteraan anak di masa dewasa. Investasi pada tumbuh kembang anak adalah investasi untuk masa depan bangsa.",
    "Masa kanak-kanak adalah periode emas yang tidak akan terulang. Nikmati setiap momen bersama anak, karena waktu berlalu sangat cepat. Ciptakan kenangan indah bersama anak melalui kegiatan bermain, petualangan, dan tradisi keluarga yang bermakna.",
]

def generate_content(topic, title_idx):
    """Generate realistic content for a document."""
    content_parts = []
    # Pick 2-3 content paragraphs from the topic
    n_paragraphs = random.randint(2, 3)
    selected = random.sample(topic["contents"], min(n_paragraphs, len(topic["contents"])))
    content_parts.extend(selected)
    
    # Add 1-2 extra paragraphs
    n_extra = random.randint(1, 2)
    extras = random.sample(EXTRA_PARAGRAPHS, n_extra)
    content_parts.extend(extras)
    
    # Add topic-specific elaboration
    elaborations = [
        f"Topik {topic['category'].lower()} merupakan salah satu aspek penting dalam parenting yang perlu dipahami oleh setiap orang tua. Pemahaman yang baik tentang {topic['category'].lower()} akan membantu orang tua dalam mengambil keputusan terbaik untuk anak-anak mereka.",
        f"Para ahli menyarankan agar orang tua terus memperbarui pengetahuan mereka tentang {topic['category'].lower()} seiring dengan perkembangan ilmu pengetahuan dan rekomendasi terbaru dari organisasi kesehatan dunia.",
        f"Di Indonesia, kesadaran masyarakat tentang pentingnya {topic['category'].lower()} semakin meningkat. Banyak komunitas dan organisasi yang aktif memberikan edukasi kepada orang tua melalui seminar, workshop, dan media sosial.",
    ]
    content_parts.append(random.choice(elaborations))
    
    random.shuffle(content_parts)
    return "\n\n".join(content_parts)

def generate_url(source, title):
    """Generate a realistic URL for the document."""
    slug = title.lower().replace(" ", "-").replace(":", "").replace("?", "").replace("(", "").replace(")", "").replace(",", "")
    return source["base_url"] + slug

def main():
    random.seed(42)
    doc_id = 0
    base_date = datetime(2024, 1, 1)
    
    # Calculate how many docs per topic to reach 300
    # We have 15 topics with 15 titles each = 225 titles
    # We need 300 docs, so we'll reuse some titles with variations
    
    all_docs = []
    
    # First pass: use all titles (225 docs)
    for topic in TOPICS:
        for title in topic["titles"]:
            doc_id += 1
            source = random.choice(SOURCES)
            crawl_date = base_date + timedelta(days=random.randint(0, 365))
            
            doc = {
                "id": f"doc_{doc_id:03d}",
                "title": title,
                "url": generate_url(source, title),
                "content": generate_content(topic, doc_id),
                "source": source["name"],
                "date_crawled": crawl_date.strftime("%Y-%m-%d %H:%M:%S")
            }
            all_docs.append(doc)
    
    # Second pass: generate 75 more docs with title variations
    variation_prefixes = [
        "Tips ", "Panduan ", "Cara ", "Info Lengkap: ", "Fakta Tentang ",
        "Yang Perlu Diketahui Tentang ", "Update Terbaru: ", "Penjelasan ",
    ]
    variation_suffixes = [
        " - Panduan Lengkap", " untuk Orang Tua Baru", " Menurut Dokter Anak",
        " yang Wajib Diketahui", " Terbaru 2024", " di Indonesia",
        " Berdasarkan Penelitian", " ala Pakar",
    ]
    
    while doc_id < 300:
        topic = random.choice(TOPICS)
        base_title = random.choice(topic["titles"])
        
        # Create a variation
        if random.random() < 0.5:
            title = random.choice(variation_prefixes) + base_title
        else:
            title = base_title + random.choice(variation_suffixes)
        
        doc_id += 1
        source = random.choice(SOURCES)
        crawl_date = base_date + timedelta(days=random.randint(0, 365))
        
        doc = {
            "id": f"doc_{doc_id:03d}",
            "title": title,
            "url": generate_url(source, title),
            "content": generate_content(topic, doc_id),
            "source": source["name"],
            "date_crawled": crawl_date.strftime("%Y-%m-%d %H:%M:%S")
        }
        all_docs.append(doc)
    
    # Save all documents
    for doc in all_docs:
        filepath = os.path.join(CORPUS_DIR, f"{doc['id']}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated {len(all_docs)} documents in {CORPUS_DIR}")
    print(f"Documents range: doc_001.json to doc_{len(all_docs):03d}.json")
    
    # Print sample
    sample = all_docs[0]
    print(f"\nSample document (doc_001.json):")
    print(f"  Title: {sample['title']}")
    print(f"  Source: {sample['source']}")
    print(f"  Content length: {len(sample['content'])} chars")

if __name__ == "__main__":
    main()
