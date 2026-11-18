"""
Generate Sample Corpus - 300 Dokumen Sintetis Parenting & Tumbuh Kembang Anak
Menghasilkan artikel realistis dalam Bahasa Indonesia untuk keperluan
Mesin Pencari Panduan Parenting.
"""

import os
import json
import random
from datetime import datetime

CORPUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus")
NUM_DOCS = 300

# ────────────────────── Data Template ──────────────────────────────────

SOURCES = [
    {"name": "theasianparent.com/id", "base_url": "https://id.theasianparent.com/artikel/"},
    {"name": "popmama.com", "base_url": "https://www.popmama.com/artikel/"},
    {"name": "parenting.co.id", "base_url": "https://www.parenting.co.id/artikel/"},
]

# Kategori topik dengan judul dan konten template
TOPICS = [
    # ─── ASI & Menyusui ───
    {
        "category": "ASI & Menyusui",
        "titles": [
            "Panduan Lengkap Menyusui untuk Ibu Baru",
            "Cara Meningkatkan Produksi ASI Secara Alami",
            "Posisi Menyusui yang Benar dan Nyaman",
            "Manfaat ASI Eksklusif untuk Bayi 0-6 Bulan",
            "Tips Menyimpan ASI Perah yang Benar",
            "Mengatasi Masalah Puting Lecet Saat Menyusui",
            "Makanan yang Membantu Melancarkan ASI",
            "Kapan Waktu yang Tepat untuk Menyapih Anak",
            "Cara Menyusui Bayi Kembar dengan Efektif",
            "Perbedaan ASI Kolostrum dan ASI Matur",
            "Jadwal Menyusui yang Ideal untuk Bayi Baru Lahir",
            "Tips Menyusui di Tempat Umum dengan Nyaman",
            "Mitos dan Fakta Seputar ASI Eksklusif",
            "Cara Mengatasi Mastitis pada Ibu Menyusui",
            "Donor ASI: Panduan dan Ketentuan yang Perlu Diketahui",
        ],
        "paragraphs": [
            "ASI merupakan makanan terbaik untuk bayi karena mengandung semua nutrisi yang dibutuhkan untuk tumbuh kembang optimal. World Health Organization (WHO) merekomendasikan pemberian ASI eksklusif selama 6 bulan pertama kehidupan bayi, dilanjutkan dengan makanan pendamping ASI hingga usia 2 tahun.",
            "Produksi ASI bekerja berdasarkan prinsip supply and demand. Semakin sering bayi menyusu, semakin banyak ASI yang diproduksi oleh tubuh ibu. Oleh karena itu, penting untuk menyusui bayi sesering mungkin, terutama pada minggu-minggu awal setelah kelahiran.",
            "Teknik pelekatan (latch) yang benar sangat penting untuk keberhasilan menyusui. Pastikan mulut bayi terbuka lebar dan mencakup sebagian besar areola, bukan hanya puting. Pelekatan yang salah dapat menyebabkan puting lecet dan produksi ASI berkurang.",
            "Kolostrum, atau ASI yang keluar pada hari-hari pertama setelah melahirkan, mengandung antibodi dan nutrisi penting yang sangat bermanfaat untuk sistem imun bayi. Meskipun jumlahnya sedikit, kolostrum sudah cukup untuk memenuhi kebutuhan bayi baru lahir.",
            "Ibu menyusui perlu mengonsumsi makanan bergizi seimbang untuk mendukung produksi ASI. Perbanyak konsumsi sayuran hijau, kacang-kacangan, buah-buahan, dan pastikan cukup minum air putih minimal 8 gelas sehari. Hindari konsumsi kafein berlebihan karena dapat masuk ke ASI.",
            "Menyimpan ASI perah memerlukan perhatian khusus agar kualitasnya tetap terjaga. ASI segar dapat disimpan pada suhu ruang selama 4-6 jam, di dalam kulkas selama 3-5 hari, dan di dalam freezer hingga 6 bulan. Gunakan wadah khusus ASI yang steril.",
            "Masalah umum yang sering dialami ibu menyusui antara lain puting lecet, payudara bengkak (engorgement), saluran ASI tersumbat, dan mastitis. Sebagian besar masalah ini dapat diatasi dengan teknik menyusui yang benar dan perawatan payudara yang tepat.",
            "Power pumping adalah teknik memompa ASI secara intensif selama 1 jam untuk merangsang peningkatan produksi ASI. Caranya adalah memompa 20 menit, istirahat 10 menit, memompa 10 menit, istirahat 10 menit, lalu memompa lagi 10 menit.",
        ],
    },
    # ─── MPASI ───
    {
        "category": "MPASI",
        "titles": [
            "Panduan MPASI Pertama untuk Bayi 6 Bulan",
            "Resep MPASI 4 Bintang yang Bergizi Lengkap",
            "Jadwal Pemberian MPASI Sesuai Usia Bayi",
            "Tanda-Tanda Bayi Siap Menerima MPASI",
            "MPASI Homemade vs Instan: Mana yang Lebih Baik?",
            "Tekstur MPASI yang Tepat Sesuai Tahapan Usia",
            "Menu MPASI untuk Bayi dengan Alergi Makanan",
            "Cara Mengatasi Bayi yang Menolak MPASI (GTM)",
            "MPASI dengan Metode Baby Led Weaning (BLW)",
            "Daftar Makanan yang Harus Dihindari untuk MPASI",
            "Resep MPASI Kaya Zat Besi untuk Mencegah Anemia",
            "Tips Menyiapkan MPASI untuk Bayi yang Bepergian",
            "MPASI Organik: Apakah Perlu untuk Bayi?",
            "Cara Memperkenalkan Finger Food pada Bayi",
            "Porsi MPASI yang Tepat untuk Setiap Tahapan Usia",
        ],
        "paragraphs": [
            "Makanan Pendamping ASI (MPASI) diberikan mulai usia 6 bulan ketika ASI saja sudah tidak mencukupi kebutuhan nutrisi bayi yang semakin berkembang. Pemberian MPASI yang terlalu dini (sebelum 4 bulan) maupun terlambat (setelah 6 bulan) sama-sama berisiko bagi kesehatan bayi.",
            "Tanda kesiapan bayi menerima MPASI antara lain: mampu duduk dengan kepala tegak, menunjukkan ketertarikan pada makanan, refleks tongue thrust sudah berkurang, dan mampu mengoordinasikan mata-tangan-mulut untuk melihat makanan, mengambilnya, dan memasukkannya ke mulut.",
            "MPASI 4 bintang mengacu pada menu yang mengandung empat kelompok makanan: karbohidrat (nasi, kentang, ubi), protein hewani (daging, ikan, telur), protein nabati (tahu, tempe, kacang-kacangan), dan sayuran atau buah-buahan.",
            "Tekstur MPASI perlu disesuaikan dengan usia bayi. Usia 6-8 bulan: puree halus, 8-9 bulan: makanan yang dihancurkan kasar (mashed), 9-11 bulan: makanan dicincang halus, dan 12 bulan ke atas: makanan keluarga yang dipotong kecil.",
            "Zat besi merupakan nutrisi penting yang harus ada dalam MPASI bayi. Sumber zat besi yang baik antara lain hati ayam, daging merah, kuning telur, dan bayam. Kekurangan zat besi pada bayi dapat menyebabkan anemia yang mengganggu tumbuh kembang.",
            "Baby Led Weaning (BLW) adalah metode pemberian MPASI di mana bayi dibiarkan makan sendiri tanpa disuapi. Makanan disajikan dalam bentuk potongan yang bisa digenggam bayi. Metode ini dipercaya membantu perkembangan motorik halus dan kemandirian bayi.",
            "Gerakan Tutup Mulut (GTM) adalah fase di mana bayi menolak makan MPASI. Hal ini normal terjadi dan bisa disebabkan oleh berbagai faktor seperti tumbuh gigi, sedang sakit, bosan dengan tekstur atau rasa makanan, atau gangguan saat makan.",
            "Saat memulai MPASI, berikan satu jenis makanan baru selama 2-3 hari untuk mengamati reaksi alergi. Tanda-tanda alergi makanan pada bayi meliputi ruam kulit, diare, muntah, bengkak pada wajah, atau kesulitan bernapas.",
        ],
    },
    # ─── Vaksinasi & Imunisasi ───
    {
        "category": "Vaksinasi & Imunisasi",
        "titles": [
            "Jadwal Imunisasi Lengkap untuk Anak 0-18 Bulan",
            "Pentingnya Vaksinasi untuk Melindungi Anak dari Penyakit",
            "Efek Samping Vaksin pada Bayi dan Cara Mengatasinya",
            "Vaksin Wajib vs Vaksin Tambahan: Apa Bedanya?",
            "Mitos dan Fakta Seputar Vaksinasi Anak",
            "Vaksin MR: Manfaat dan Jadwal Pemberiannya",
            "Apa yang Harus Dilakukan Jika Jadwal Vaksin Terlewat",
            "Vaksin Booster: Mengapa Anak Perlu Dosis Penguat",
            "Vaksinasi Saat Pandemi: Panduan untuk Orang Tua",
            "Daftar Vaksin yang Direkomendasikan IDAI untuk Anak",
            "Persiapan Sebelum Membawa Anak Vaksin",
            "Vaksin PCV: Perlindungan dari Infeksi Pneumokokus",
            "Memahami Kandungan dan Keamanan Vaksin untuk Anak",
            "Vaksin Influenza untuk Anak: Perlukah Setiap Tahun?",
            "Herd Immunity dan Peran Vaksinasi dalam Masyarakat",
        ],
        "paragraphs": [
            "Vaksinasi atau imunisasi merupakan cara paling efektif untuk melindungi anak dari berbagai penyakit berbahaya. Program imunisasi nasional di Indonesia mewajibkan pemberian beberapa jenis vaksin dasar untuk semua anak, termasuk BCG, hepatitis B, polio, DPT-HB-Hib, dan campak-rubella.",
            "Ikatan Dokter Anak Indonesia (IDAI) merekomendasikan jadwal imunisasi yang mencakup vaksin wajib dan vaksin tambahan. Vaksin wajib disediakan gratis oleh pemerintah, sementara vaksin tambahan seperti PCV, rotavirus, dan influenza perlu dibeli sendiri namun sangat direkomendasikan.",
            "Efek samping vaksin umumnya ringan dan bersifat sementara. Reaksi yang umum terjadi meliputi demam ringan, kemerahan atau bengkak di tempat suntikan, rewel, dan penurunan nafsu makan. Efek samping serius sangat jarang terjadi.",
            "Jika jadwal vaksinasi anak terlewat, jangan panik. Hubungi dokter atau bidan untuk mendapatkan jadwal kejar (catch-up schedule). Sebagian besar vaksin dapat diberikan meskipun terlambat, karena lebih baik terlambat daripada tidak divaksin sama sekali.",
            "Sebelum vaksinasi, pastikan anak dalam kondisi sehat. Informasikan kepada dokter jika anak sedang sakit, memiliki riwayat alergi, atau pernah mengalami reaksi berat terhadap vaksin sebelumnya. Berikan paracetamol jika anak mengalami demam setelah divaksin.",
            "Vaksin bekerja dengan cara merangsang sistem imun tubuh untuk membentuk antibodi terhadap penyakit tertentu tanpa menyebabkan penyakit itu sendiri. Ketika anak terpapar kuman penyakit di kemudian hari, tubuhnya sudah siap melawan.",
            "Herd immunity atau kekebalan kelompok tercapai ketika sebagian besar populasi sudah divaksinasi, sehingga penyebaran penyakit terhambat dan melindungi juga mereka yang tidak bisa divaksinasi karena kondisi medis tertentu.",
            "Vaksin PCV melindungi anak dari infeksi bakteri pneumokokus yang dapat menyebabkan pneumonia, meningitis, dan infeksi telinga. Vaksin ini diberikan pada usia 2, 4, 6, dan 12-15 bulan.",
        ],
    },
    # ─── Pola Asuh & Parenting ───
    {
        "category": "Pola Asuh & Parenting",
        "titles": [
            "Mengenal 4 Tipe Pola Asuh dan Dampaknya pada Anak",
            "Tips Positive Parenting untuk Membentuk Karakter Anak",
            "Cara Menghadapi Anak yang Tantrum dengan Sabar",
            "Pentingnya Quality Time antara Orang Tua dan Anak",
            "Mendidik Anak Tanpa Kekerasan: Panduan Disiplin Positif",
            "Peran Ayah dalam Pengasuhan Anak Modern",
            "Cara Membangun Komunikasi Efektif dengan Anak",
            "Tips Mengajarkan Anak tentang Emosi dan Empati",
            "Dampak Screen Time Berlebihan pada Anak",
            "Cara Mengatasi Sibling Rivalry antar Saudara",
            "Mempersiapkan Anak untuk Masuk Sekolah Pertama Kali",
            "Gentle Parenting: Mendidik dengan Kelembutan dan Ketegasan",
            "Cara Membangun Kepercayaan Diri Anak Sejak Dini",
            "Tips Menghadapi Anak yang Pemalu dan Pendiam",
            "Mengajarkan Anak Bertanggung Jawab Sesuai Usianya",
            "Cara Mengatasi Anak yang Suka Berbohong",
            "Tips Co-Parenting Efektif Setelah Perceraian",
            "Mendidik Anak di Era Digital: Tantangan dan Solusi",
        ],
        "paragraphs": [
            "Pola asuh otoriter, permisif, uninvolved, dan otoritatif memiliki dampak yang berbeda pada perkembangan anak. Penelitian menunjukkan bahwa pola asuh otoritatif—yang menggabungkan kehangatan dengan batasan yang jelas—memberikan hasil terbaik untuk perkembangan sosial-emosional anak.",
            "Positive parenting berfokus pada penguatan perilaku baik anak alih-alih menghukum perilaku buruk. Berikan pujian spesifik ketika anak melakukan hal yang benar, misalnya 'Kakak hebat sudah membereskan mainan sendiri' daripada sekadar 'Anak pintar'.",
            "Tantrum adalah ledakan emosi yang normal terjadi pada anak usia 1-4 tahun karena mereka belum mampu mengekspresikan keinginan dan frustrasi dengan kata-kata. Saat anak tantrum, tetap tenang, pastikan keamanannya, dan tunggu hingga emosinya mereda sebelum berbicara.",
            "Quality time tidak harus memakan waktu lama atau biaya mahal. Aktivitas sederhana seperti membacakan buku cerita, bermain bersama di taman, memasak bersama, atau sekadar ngobrol saat makan malam sudah cukup untuk memperkuat ikatan emosional.",
            "Disiplin positif mengajarkan anak tentang konsekuensi alami dari perilakunya tanpa menggunakan hukuman fisik atau verbal yang menyakiti. Alih-alih memukul atau membentak, gunakan teknik seperti time-out, pengalihan perhatian, dan percakapan yang menjelaskan mengapa perilaku tertentu tidak tepat.",
            "Penelitian menunjukkan bahwa keterlibatan aktif ayah dalam pengasuhan memberikan dampak positif yang signifikan pada perkembangan kognitif, emosional, dan sosial anak. Anak yang memiliki hubungan dekat dengan ayahnya cenderung lebih percaya diri dan memiliki kemampuan akademik yang lebih baik.",
            "Screen time berlebihan pada anak di bawah 5 tahun dikaitkan dengan gangguan perkembangan bahasa, masalah tidur, dan peningkatan risiko obesitas. American Academy of Pediatrics merekomendasikan tidak ada screen time untuk anak di bawah 18 bulan, dan maksimal 1 jam per hari untuk anak usia 2-5 tahun.",
            "Gentle parenting menggabungkan empati, rasa hormat, dan pemahaman dalam mendidik anak. Pendekatan ini tidak berarti permisif; orang tua tetap menetapkan batasan yang jelas namun melakukannya dengan cara yang menghargai perasaan dan perspektif anak.",
        ],
    },
    # ─── Nutrisi Anak ───
    {
        "category": "Nutrisi Anak",
        "titles": [
            "Panduan Gizi Seimbang untuk Anak Usia 1-5 Tahun",
            "Mengatasi Anak yang Picky Eater",
            "Makanan Kaya Kalsium untuk Pertumbuhan Tulang Anak",
            "Bahaya Junk Food dan Gula Berlebih pada Anak",
            "Menu Bekal Sehat dan Menarik untuk Anak Sekolah",
            "Kebutuhan Vitamin dan Mineral Penting untuk Anak",
            "Cara Membiasakan Anak Makan Sayur dan Buah",
            "Suplemen Vitamin untuk Anak: Perlu atau Tidak?",
            "Resep Camilan Sehat Pengganti Jajanan Kemasan",
            "Porsi Makan yang Tepat untuk Anak Sesuai Usianya",
            "Makanan Peningkat Daya Tahan Tubuh Anak",
            "Dampak Kekurangan Gizi pada Tumbuh Kembang Anak",
            "Cara Mencegah dan Mengatasi Obesitas pada Anak",
            "Alergi Makanan pada Anak: Gejala dan Penanganannya",
            "Pentingnya Sarapan untuk Konsentrasi Belajar Anak",
        ],
        "paragraphs": [
            "Gizi seimbang sangat penting untuk mendukung pertumbuhan dan perkembangan anak. Isi Piringku untuk anak terdiri dari makanan pokok (35%), lauk pauk (35%), sayuran (15%), dan buah-buahan (15%), disertai air putih yang cukup.",
            "Anak yang picky eater atau susah makan merupakan tantangan umum yang dihadapi orang tua. Strategi yang dapat dicoba antara lain: menyajikan makanan dalam bentuk yang menarik, melibatkan anak dalam proses memasak, makan bersama keluarga, dan tidak memaksa anak menghabiskan makanannya.",
            "Kalsium sangat dibutuhkan untuk pertumbuhan tulang dan gigi anak. Sumber kalsium yang baik antara lain susu, yogurt, keju, ikan teri, brokoli, dan tahu. Anak usia 1-3 tahun membutuhkan sekitar 700 mg kalsium per hari, sementara usia 4-8 tahun membutuhkan 1000 mg per hari.",
            "Konsumsi gula berlebih pada anak dikaitkan dengan risiko obesitas, kerusakan gigi, diabetes tipe 2, dan gangguan konsentrasi. Batasi konsumsi gula tambahan pada anak tidak lebih dari 25 gram (6 sendok teh) per hari, dan hindari minuman manis seperti soda dan jus kemasan.",
            "Zat besi merupakan mineral penting yang sering kekurangan pada anak-anak Indonesia. Defisiensi zat besi dapat menyebabkan anemia, yang berdampak pada kemampuan belajar, daya tahan tubuh, dan pertumbuhan. Pastikan anak mengonsumsi sumber zat besi seperti daging merah, hati, bayam, dan kacang-kacangan.",
            "Vitamin D penting untuk penyerapan kalsium dan kesehatan tulang anak. Sumber vitamin D antara lain paparan sinar matahari pagi (15-30 menit), ikan berlemak, kuning telur, dan susu yang difortifikasi. Di Indonesia, meskipun banyak sinar matahari, banyak anak yang ternyata kekurangan vitamin D.",
            "Omega-3, terutama DHA dan EPA, berperan penting dalam perkembangan otak dan fungsi kognitif anak. Sumber omega-3 terbaik adalah ikan berlemak seperti salmon, sarden, dan makarel. Konsumsi ikan dianjurkan 2-3 kali seminggu untuk anak.",
            "Probiotik dan prebiotik membantu menjaga kesehatan saluran pencernaan anak. Probiotik terdapat dalam yogurt, tempe, dan kimchi, sementara prebiotik terdapat dalam pisang, bawang putih, asparagus, dan oat. Kesehatan usus yang baik mendukung sistem imun anak.",
        ],
    },
    # ─── Perkembangan Motorik ───
    {
        "category": "Perkembangan Motorik",
        "titles": [
            "Tahapan Perkembangan Motorik Kasar Bayi 0-12 Bulan",
            "Stimulasi Motorik Halus untuk Anak Usia Dini",
            "Kapan Bayi Mulai Tengkurap, Duduk, dan Berjalan?",
            "Aktivitas Bermain untuk Melatih Koordinasi Motorik Anak",
            "Tanda-Tanda Keterlambatan Perkembangan Motorik pada Anak",
            "Manfaat Tummy Time untuk Perkembangan Bayi",
            "Mainan Edukatif yang Mendukung Perkembangan Motorik",
            "Perkembangan Kemampuan Menulis dan Menggambar Anak",
            "Olahraga yang Cocok untuk Anak Usia 3-6 Tahun",
            "Cara Melatih Keseimbangan dan Koordinasi Anak",
            "Perkembangan Motorik Anak Prematur: Apa yang Perlu Diketahui",
            "Sensory Play: Bermain Sensorik untuk Perkembangan Anak",
            "Milestone Perkembangan Anak Usia 1-3 Tahun",
            "Fisioterapi untuk Anak dengan Gangguan Motorik",
            "Hubungan Perkembangan Motorik dengan Kemampuan Akademik",
        ],
        "paragraphs": [
            "Perkembangan motorik kasar meliputi kemampuan menggunakan otot-otot besar tubuh seperti berguling, duduk, merangkak, berdiri, dan berjalan. Setiap anak memiliki kecepatan perkembangan yang berbeda, namun ada rentang usia normal yang dapat dijadikan acuan.",
            "Motorik halus melibatkan koordinasi otot-otot kecil, terutama tangan dan jari. Kemampuan ini penting untuk aktivitas sehari-hari seperti makan sendiri, mengancingkan baju, menulis, dan menggunting. Stimulasi motorik halus bisa dimulai sejak bayi dengan aktivitas sederhana seperti meremas benda lunak.",
            "Tummy time atau waktu tengkurap penting untuk memperkuat otot leher, bahu, dan punggung bayi yang akan mendukung kemampuan duduk dan merangkak nantinya. Mulai tummy time sejak bayi baru lahir, dimulai dari 3-5 menit beberapa kali sehari, dan tingkatkan durasinya secara bertahap.",
            "Milestone perkembangan motorik bayi: usia 2-4 bulan mulai mengangkat kepala, 4-6 bulan berguling, 6-8 bulan duduk tanpa bantuan, 8-10 bulan merangkak, 9-12 bulan berdiri berpegangan, dan 12-15 bulan mulai berjalan. Ingat bahwa setiap anak unik dan berkembang dengan kecepatannya sendiri.",
            "Bermain sensori (sensory play) seperti bermain pasir, air, playdough, atau finger painting sangat bermanfaat untuk perkembangan motorik halus, kreativitas, dan kemampuan pemecahan masalah anak. Aktivitas ini juga membantu perkembangan koneksi saraf di otak.",
            "Tanda-tanda yang perlu diwaspadai terkait keterlambatan motorik antara lain: bayi 4 bulan belum bisa mengangkat kepala, 9 bulan belum bisa duduk, 18 bulan belum bisa berjalan, atau anak tampak sangat kaku atau terlalu lemas. Konsultasikan dengan dokter anak jika ada kekhawatiran.",
            "Mainan yang mendukung perkembangan motorik anak antara lain balok susun, puzzle, manik-manik untuk dironce, playdough, bola, sepeda roda tiga, dan trampolin kecil. Pilih mainan yang sesuai usia dan pastikan aman dari bahan berbahaya.",
            "Olahraga terstruktur untuk anak usia 3-6 tahun sebaiknya bersifat menyenangkan dan tidak terlalu kompetitif. Renang, senam, bersepeda, dan menari adalah pilihan yang baik karena melatih berbagai kelompok otot sekaligus meningkatkan koordinasi dan keseimbangan.",
        ],
    },
    # ─── Kesehatan Anak ───
    {
        "category": "Kesehatan Anak",
        "titles": [
            "Cara Mengatasi Demam pada Anak di Rumah",
            "Tanda-Tanda Dehidrasi pada Bayi dan Anak",
            "Panduan Pertolongan Pertama untuk Orang Tua",
            "Penyakit Umum pada Anak dan Cara Pencegahannya",
            "Kapan Harus Membawa Anak ke Dokter atau IGD",
            "Cara Menurunkan Panas Anak Secara Alami",
            "Mengenal Alergi pada Anak: Gejala dan Penanganan",
            "Tips Menjaga Kesehatan Gigi Anak Sejak Dini",
            "Ruam Popok: Penyebab dan Cara Mengatasinya",
            "Infeksi Saluran Pernapasan pada Anak: Yang Perlu Diketahui",
            "Cara Mengatasi Sembelit pada Bayi dan Anak",
            "Kolik pada Bayi: Penyebab dan Tips Meredakannya",
            "Kesehatan Mata Anak: Kapan Harus Periksa ke Dokter Mata",
            "Diare pada Anak: Penanganan dan Pencegahan",
            "Tips Menjaga Kebersihan dan Higienitas Anak",
        ],
        "paragraphs": [
            "Demam pada anak umumnya merupakan respons alami tubuh melawan infeksi. Anak dikatakan demam jika suhu tubuhnya di atas 37.5°C. Kompres dengan air hangat (bukan dingin), berikan parasetamol sesuai dosis berat badan, dan pastikan anak cukup minum cairan.",
            "Tanda dehidrasi pada anak meliputi: jarang buang air kecil (kurang dari 6 kali sehari untuk bayi), mulut dan bibir kering, menangis tanpa air mata, ubun-ubun cekung, dan anak tampak lesu. Dehidrasi berat memerlukan penanganan medis segera.",
            "Setiap orang tua perlu mengetahui dasar-dasar pertolongan pertama: cara menangani luka, luka bakar, kecelakaan, tersedak, dan reaksi alergi. Siapkan kotak P3K di rumah yang berisi plester, kasa steril, antiseptik, termometer, dan obat-obatan dasar.",
            "Penyakit umum pada anak usia dini meliputi ISPA (Infeksi Saluran Pernapasan Atas), diare, cacar air, campak, dan infeksi telinga. Pencegahan terbaik adalah dengan menjaga kebersihan, vaksinasi lengkap, nutrisi yang baik, dan istirahat yang cukup.",
            "Segera bawa anak ke dokter atau IGD jika: demam tinggi di atas 39°C yang tidak turun dengan obat, kejang, sesak napas, muntah terus-menerus, dehidrasi berat, atau anak tampak sangat lemas dan tidak responsif. Jangan tunda pertolongan medis dalam kondisi darurat.",
            "Kesehatan gigi anak harus diperhatikan sejak gigi pertama muncul (sekitar usia 6 bulan). Bersihkan gigi dengan sikat gigi lembut dan pasta gigi berfluoride seukuran beras (di bawah 3 tahun) atau seukuran kacang polong (3 tahun ke atas). Kunjungi dokter gigi setiap 6 bulan.",
            "Ruam popok sering terjadi pada bayi karena kulit yang lembab dan terpapar urin/feses terlalu lama. Pencegahannya: ganti popok secara teratur, bersihkan area popok dengan lembut, biarkan kulit kering sebelum memasang popok baru, dan gunakan krim pelindung seperti zinc oxide.",
            "Kolik pada bayi ditandai dengan tangisan intens yang berlangsung lebih dari 3 jam sehari, 3 hari seminggu, selama lebih dari 3 minggu. Penyebab pastinya belum diketahui, namun bisa diredakan dengan teknik menggendong, mengayun lembut, suara white noise, dan pijat bayi.",
        ],
    },
    # ─── Perkembangan Kognitif & Bahasa ───
    {
        "category": "Perkembangan Kognitif & Bahasa",
        "titles": [
            "Tahapan Perkembangan Bahasa Anak 0-5 Tahun",
            "Cara Merangsang Kecerdasan Anak Sejak Dini",
            "Manfaat Membacakan Buku untuk Anak Setiap Hari",
            "Bilingual: Mengajarkan Dua Bahasa pada Anak",
            "Mainan Edukatif untuk Merangsang Kecerdasan Anak",
            "Tanda-Tanda Speech Delay dan Kapan Harus Khawatir",
            "Cara Mengembangkan Kreativitas dan Imajinasi Anak",
            "Stimulasi Otak Anak Melalui Musik dan Seni",
            "Memahami Gaya Belajar Anak: Visual, Auditori, Kinestetik",
            "Aktivitas Montessori untuk Anak di Rumah",
            "Perkembangan Emosional dan Sosial Anak Usia Dini",
            "Cara Mengajarkan Anak Membaca dengan Metode Fonik",
            "Peran Bermain dalam Perkembangan Kognitif Anak",
            "Kecerdasan Majemuk: Mengenali Potensi Unik Anak",
            "Tips Melatih Konsentrasi dan Fokus pada Anak",
        ],
        "paragraphs": [
            "Perkembangan bahasa anak dimulai sejak lahir. Bayi 0-3 bulan mulai mengeluarkan suara cooing, 4-6 bulan babbling, 9-12 bulan mengucapkan kata pertama, 18-24 bulan menggabungkan dua kata, dan pada usia 3 tahun sudah bisa membentuk kalimat sederhana. Stimulasi melalui percakapan dan membacakan cerita sangat penting.",
            "Membacakan buku untuk anak setiap hari memiliki banyak manfaat: meningkatkan kosakata, mengembangkan kemampuan mendengarkan, membangun koneksi emosional, merangsang imajinasi, dan menanamkan kebiasaan membaca. Mulailah membacakan buku sejak bayi, meskipun mereka belum memahami kata-katanya.",
            "Tanda-tanda speech delay yang perlu diperhatikan: bayi 12 bulan tidak babbling, 18 bulan belum mengucapkan satu kata pun, 2 tahun kosakata kurang dari 50 kata, atau 3 tahun belum bisa membuat kalimat sederhana. Intervensi dini sangat penting untuk hasil yang optimal.",
            "Metode Montessori menekankan pembelajaran mandiri dan eksplorasi melalui lingkungan yang disiapkan. Di rumah, orang tua bisa menerapkan prinsip Montessori dengan menyediakan mainan open-ended, membiarkan anak memilih aktivitasnya, dan mengatur ruangan setinggi mata anak.",
            "Kecerdasan majemuk (multiple intelligences) yang dikemukakan Howard Gardner mencakup: linguistik, logis-matematis, spasial, musikal, kinestetik, interpersonal, intrapersonal, dan naturalis. Setiap anak memiliki kombinasi kecerdasan yang unik, dan tugas orang tua adalah mengenali dan mendukung potensi tersebut.",
            "Bermain adalah cara utama anak belajar tentang dunia. Melalui bermain, anak mengembangkan kemampuan kognitif, sosial, emosional, dan fisik. Bermain pura-pura (pretend play) khususnya penting untuk mengembangkan kemampuan berpikir abstrak dan keterampilan sosial.",
            "Musik memiliki pengaruh positif pada perkembangan otak anak. Belajar musik meningkatkan kemampuan matematika, bahasa, koordinasi motorik, dan kecerdasan emosional. Perkenalkan musik pada anak sejak dini melalui menyanyi bersama, mendengarkan berbagai jenis musik, dan bermain alat musik sederhana.",
            "Stimulasi kognitif yang tepat sesuai usia sangat penting. Untuk bayi: mobile warna-warni dan mainan bertekstur. Untuk toddler: puzzle sederhana, mencocokan bentuk, dan bermain peran. Untuk prasekolah: menghitung, mengenal huruf, eksperimen sains sederhana, dan permainan strategi dasar.",
        ],
    },
    # ─── Tidur Anak ───
    {
        "category": "Tidur & Istirahat Anak",
        "titles": [
            "Panduan Kebutuhan Tidur Anak Sesuai Usia",
            "Tips Membangun Rutinitas Tidur yang Baik untuk Anak",
            "Cara Mengatasi Anak yang Susah Tidur Malam",
            "Sleep Training: Metode Melatih Bayi Tidur Sendiri",
            "Bahaya Kurang Tidur pada Anak dan Dampaknya",
            "Tidur Siang untuk Anak: Kapan Harus Berhenti?",
            "Mengatasi Night Terror dan Mimpi Buruk pada Anak",
            "Posisi Tidur yang Aman untuk Bayi Baru Lahir",
            "Tips Agar Bayi Tidur Nyenyak Sepanjang Malam",
            "Hubungan Kualitas Tidur dengan Pertumbuhan Anak",
        ],
        "paragraphs": [
            "Kebutuhan tidur anak bervariasi sesuai usia: bayi baru lahir membutuhkan 14-17 jam, bayi 4-11 bulan 12-15 jam, toddler 1-2 tahun 11-14 jam, prasekolah 3-5 tahun 10-13 jam, dan anak usia sekolah 6-12 tahun 9-12 jam per hari termasuk tidur siang.",
            "Rutinitas tidur yang konsisten membantu anak tidur lebih mudah dan nyenyak. Contoh rutinitas: mandi air hangat, mengganti baju tidur, sikat gigi, membacakan buku cerita, berdoa, dan mematikan lampu pada jam yang sama setiap malam.",
            "Sleep training adalah proses mengajarkan bayi untuk tidur sendiri tanpa bantuan orang tua. Beberapa metode populer antara lain: Ferber method (graduated extinction), Chair method, Pick up put down, dan Fading method. Setiap metode memiliki pendekatan yang berbeda.",
            "Kurang tidur pada anak berdampak pada kemampuan konsentrasi, mood, perilaku, dan daya tahan tubuh. Penelitian menunjukkan bahwa anak yang kurang tidur cenderung lebih rewel, sulit fokus di sekolah, dan lebih rentan sakit.",
            "Untuk mencegah Sudden Infant Death Syndrome (SIDS), bayi harus tidur telentang di permukaan yang rata dan keras, tanpa bantal, selimut tebal, boneka, atau bumper di boks bayi. Suhu ruangan yang nyaman (20-22°C) juga penting untuk tidur yang aman.",
            "Night terror berbeda dengan mimpi buruk. Night terror terjadi saat tidur dalam (deep sleep), anak tampak ketakutan tapi tidak benar-benar sadar dan biasanya tidak ingat keesokan harinya. Yang terbaik adalah memastikan keamanan anak dan menunggu episodenya berlalu.",
            "Tidur siang masih dibutuhkan oleh sebagian besar anak hingga usia 3-4 tahun. Tanda anak sudah siap berhenti tidur siang: sulit tidur malam meskipun sudah tidur siang, tidur siang semakin singkat, atau anak tetap segar dan aktif tanpa tidur siang.",
            "Hormon pertumbuhan (growth hormone) paling banyak diproduksi saat anak tidur nyenyak, terutama pada fase deep sleep. Oleh karena itu, kualitas dan kuantitas tidur yang cukup sangat penting untuk pertumbuhan fisik anak secara optimal.",
        ],
    },
    # ─── Kehamilan & Persiapan ───
    {
        "category": "Kehamilan & Persiapan",
        "titles": [
            "Panduan Nutrisi Ibu Hamil Trimester 1, 2, dan 3",
            "Persiapan Menyambut Kelahiran Bayi Pertama",
            "Olahraga yang Aman untuk Ibu Hamil",
            "Tanda-Tanda Bahaya Kehamilan yang Perlu Diwaspadai",
            "Mual Morning Sickness: Penyebab dan Cara Mengatasinya",
            "Pemeriksaan Kehamilan (ANC) yang Penting Dilakukan",
            "Tips Memilih Rumah Sakit dan Dokter Kandungan",
            "Perlengkapan Bayi Baru Lahir: Daftar Belanja Lengkap",
            "Baby Blues vs Depresi Pasca Melahirkan: Cara Membedakannya",
            "Pemulihan Pasca Melahirkan: Tips untuk Ibu Baru",
        ],
        "paragraphs": [
            "Nutrisi selama kehamilan sangat penting untuk perkembangan janin. Asam folat dibutuhkan terutama pada trimester pertama untuk mencegah cacat tabung saraf. Zat besi untuk mencegah anemia, kalsium untuk pembentukan tulang janin, dan DHA untuk perkembangan otak.",
            "Persiapan menyambut kelahiran bayi meliputi: menyiapkan perlengkapan bayi, memilih rumah sakit, mengikuti kelas persiapan persalinan, menyiapkan tas persalinan, dan merencanakan cuti melahirkan. Jangan lupa juga mempersiapkan mental dan emosional.",
            "Olahraga selama kehamilan aman dan dianjurkan untuk menjaga kebugaran, mengurangi keluhan kehamilan, dan mempersiapkan persalinan. Pilihan yang baik antara lain jalan kaki, renang, yoga prenatal, dan senam hamil. Hindari olahraga dengan risiko jatuh atau benturan.",
            "Tanda-tanda bahaya kehamilan yang memerlukan penanganan segera: perdarahan, nyeri perut hebat, pecah ketuban sebelum waktunya, bengkak berlebihan pada wajah dan tangan, sakit kepala berat disertai pandangan kabur, dan gerakan janin berkurang drastis.",
            "Morning sickness dialami oleh sekitar 80% ibu hamil, biasanya pada trimester pertama. Tips mengatasinya: makan dalam porsi kecil tapi sering, hindari makanan berminyak dan berbau menyengat, makan crackers sebelum bangun tidur, dan cukup istirahat.",
            "Baby blues adalah perubahan mood ringan yang dialami sekitar 80% ibu baru dalam 2 minggu pertama setelah melahirkan, yang biasanya membaik dengan sendirinya. Berbeda dengan depresi pasca melahirkan (postpartum depression) yang berlangsung lebih lama dan lebih berat, memerlukan bantuan profesional.",
            "Pemeriksaan kehamilan (ANC) sebaiknya dilakukan minimal: 1 kali pada trimester pertama, 1 kali pada trimester kedua, dan 2 kali pada trimester ketiga. Pemeriksaan meliputi tekanan darah, berat badan, tinggi fundus uteri, denyut jantung janin, dan pemeriksaan laboratorium.",
            "Pemulihan pasca melahirkan membutuhkan waktu 6-8 minggu. Selama masa nifas, ibu perlu istirahat cukup, makan bergizi untuk mendukung produksi ASI, menjaga kebersihan luka (jahitan), dan melakukan senam nifas ringan. Jangan ragu meminta bantuan keluarga.",
        ],
    },
    # ─── Tumbuh Kembang Umum ───
    {
        "category": "Tumbuh Kembang Umum",
        "titles": [
            "Memantau Tumbuh Kembang Anak dengan KMS dan KIA",
            "Stunting pada Anak: Penyebab, Dampak, dan Pencegahan",
            "Berat Badan Ideal Anak Sesuai Usia dan Tinggi Badan",
            "1000 Hari Pertama Kehidupan: Window of Opportunity",
            "Stimulasi Tumbuh Kembang Anak Sesuai Usia",
            "Kapan Harus Khawatir tentang Pertumbuhan Anak",
            "Peran Lingkungan dalam Tumbuh Kembang Anak",
            "Deteksi Dini Gangguan Tumbuh Kembang Anak",
            "Faktor Genetik dan Lingkungan dalam Pertumbuhan Anak",
            "Golden Age: Memaksimalkan Periode Emas Tumbuh Kembang",
        ],
        "paragraphs": [
            "1000 Hari Pertama Kehidupan (HPK) dihitung sejak pembuahan hingga anak berusia 2 tahun. Periode ini disebut window of opportunity karena merupakan masa paling kritis untuk pertumbuhan fisik, perkembangan otak, dan pembentukan sistem imun yang akan memengaruhi kesehatan anak seumur hidup.",
            "Stunting adalah kondisi gagal tumbuh kronis yang ditandai dengan tinggi badan anak di bawah standar untuk usianya. Penyebab utamanya adalah kekurangan gizi kronis dan infeksi berulang. Stunting tidak hanya memengaruhi tinggi badan, tetapi juga perkembangan kognitif dan produktivitas di masa dewasa.",
            "Kartu Menuju Sehat (KMS) atau Buku Kesehatan Ibu dan Anak (KIA) adalah alat penting untuk memantau pertumbuhan anak. Berat badan anak ditimbang setiap bulan di Posyandu dan diplot pada grafik pertumbuhan. Jika kurva pertumbuhan mendatar atau menurun, perlu evaluasi lebih lanjut.",
            "Golden age atau periode emas tumbuh kembang anak terjadi pada usia 0-5 tahun. Pada periode ini, otak anak berkembang sangat pesat hingga mencapai 80% ukuran otak dewasa pada usia 3 tahun. Stimulasi yang tepat pada periode ini akan membentuk fondasi kecerdasan anak.",
            "Deteksi dini gangguan tumbuh kembang dapat dilakukan melalui skrining rutin menggunakan instrumen seperti KPSP (Kuesioner Pra Skrining Perkembangan). Skrining sebaiknya dilakukan pada usia 3, 6, 9, 12, 15, 18, 21, 24, 30, 36, 42, 48, 54, 60, 66, dan 72 bulan.",
            "Lingkungan yang kaya stimulasi sangat penting untuk tumbuh kembang anak. Ini mencakup lingkungan fisik yang aman untuk dieksplorasi, interaksi sosial dengan orang tua dan teman sebaya, kesempatan bermain yang beragam, dan paparan pada berbagai pengalaman belajar.",
            "Pertumbuhan anak dipengaruhi oleh faktor genetik (tinggi orang tua, ras) dan lingkungan (nutrisi, penyakit, aktivitas fisik, tidur). Meskipun genetik menentukan potensi maksimal, lingkungan yang optimal diperlukan agar potensi tersebut dapat tercapai.",
            "Stimulasi tumbuh kembang harus disesuaikan dengan usia anak. Untuk bayi: stimulasi visual, auditori, dan taktil. Untuk toddler: stimulasi bahasa, motorik, dan sosial. Untuk prasekolah: stimulasi kognitif, kreativitas, dan kemandirian.",
        ],
    },
]

# Variasi intro dan penutup untuk membuat konten lebih bervariasi
INTRO_TEMPLATES = [
    "Sebagai orang tua, memahami {topic} sangat penting untuk mendukung tumbuh kembang anak secara optimal.",
    "Banyak orang tua yang bertanya-tanya tentang {topic}. Artikel ini akan membahas secara lengkap hal-hal yang perlu Anda ketahui.",
    "{topic} merupakan salah satu aspek penting dalam pengasuhan anak yang sering kali membuat orang tua bingung.",
    "Membahas tentang {topic}, ada banyak hal yang perlu dipahami oleh setiap orang tua, terutama yang baru pertama kali memiliki anak.",
    "Dalam perjalanan menjadi orang tua, pengetahuan tentang {topic} akan sangat membantu Anda mengambil keputusan yang tepat untuk buah hati.",
    "Para ahli kesehatan anak menekankan pentingnya pemahaman yang baik tentang {topic} bagi setiap orang tua.",
    "Topik {topic} selalu menarik perhatian para orang tua, karena berkaitan langsung dengan kesejahteraan anak-anak mereka.",
]

CLOSING_TEMPLATES = [
    "Konsultasikan dengan dokter anak atau tenaga kesehatan profesional jika Anda memiliki pertanyaan atau kekhawatiran terkait topik ini.",
    "Setiap anak adalah unik dan berkembang dengan kecepatannya sendiri. Jangan ragu untuk berkonsultasi dengan profesional jika diperlukan.",
    "Semoga informasi ini bermanfaat bagi para orang tua dalam mendukung tumbuh kembang anak secara optimal.",
    "Ingatlah bahwa tidak ada orang tua yang sempurna. Yang terpenting adalah terus belajar dan memberikan yang terbaik untuk anak Anda.",
    "Dengan pengetahuan yang tepat dan kasih sayang yang tulus, Anda dapat memberikan fondasi terbaik untuk masa depan anak Anda.",
]

# ────────────────────── Generator ──────────────────────────────────────

def generate_article(doc_id, topic_data, title):
    """Generate satu artikel sintetis."""
    source = random.choice(SOURCES)
    slug = title.lower().replace(" ", "-").replace(":", "").replace("?", "").replace(",", "")
    url = source["base_url"] + slug

    # Build content
    intro = random.choice(INTRO_TEMPLATES).format(topic=topic_data["category"].lower())
    body_paragraphs = random.sample(topic_data["paragraphs"], min(random.randint(3, 6), len(topic_data["paragraphs"])))
    closing = random.choice(CLOSING_TEMPLATES)

    content = intro + "\n\n" + "\n\n".join(body_paragraphs) + "\n\n" + closing

    return {
        "id": f"doc_{doc_id:03d}",
        "title": title,
        "url": url,
        "content": content,
        "source": source["name"],
        "date_crawled": datetime.now().isoformat(),
    }


def main():
    """Generate 300 dokumen sampel."""
    print("=" * 60)
    print("GENERATING SAMPLE CORPUS")
    print("300 Dokumen Parenting & Tumbuh Kembang Anak")
    print("=" * 60)

    os.makedirs(CORPUS_DIR, exist_ok=True)

    # Kumpulkan semua judul dari semua topik
    all_titles = []
    for topic in TOPICS:
        for title in topic["titles"]:
            all_titles.append((topic, title))

    # Jika judul kurang dari 300, buat variasi tambahan
    extra_prefixes = [
        "Panduan Lengkap: ", "Tips Praktis: ", "Yang Perlu Diketahui: ",
        "Memahami ", "Mengenal ", "Cara Efektif: ",
    ]
    extra_suffixes = [
        " yang Wajib Diketahui Orang Tua",
        " Menurut Dokter Anak",
        " Berdasarkan Penelitian Terbaru",
        " untuk Orang Tua Baru",
        " di Era Modern",
    ]

    while len(all_titles) < NUM_DOCS:
        topic = random.choice(TOPICS)
        base_title = random.choice(topic["titles"])
        # Variasikan judul
        variation = random.choice([
            random.choice(extra_prefixes) + base_title,
            base_title + random.choice(extra_suffixes),
            base_title + f" ({random.randint(2024, 2026)})",
        ])
        all_titles.append((topic, variation))

    random.shuffle(all_titles)

    for i in range(NUM_DOCS):
        topic_data, title = all_titles[i]
        doc = generate_article(i + 1, topic_data, title)

        filepath = os.path.join(CORPUS_DIR, f"doc_{i+1:03d}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)

        if (i + 1) % 50 == 0 or i == 0:
            print(f"  [{i+1}/{NUM_DOCS}] Generated: {title}")

    print(f"\n{'=' * 60}")
    print(f"SELESAI! {NUM_DOCS} dokumen berhasil di-generate.")
    print(f"Disimpan di: {CORPUS_DIR}")
    print(f"Format: doc_001.json - doc_{NUM_DOCS:03d}.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
