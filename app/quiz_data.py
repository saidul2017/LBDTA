"""Bank soal kuis Literasi Big Data PAI — 36 soal akademis.

Setiap soal:
- 4 pilihan ganda (a, b, c, d)
- 1 jawaban benar (index 0-3)
- penjelasan singkat
- rujukan ke berkas modul

Catatan pedagogis:
- Soal dirancang menguji pemahaman konseptual + aplikatif, bukan hafalan.
- Distraktor (jawaban salah) dipilih agar masuk akal, bukan absurd.
- Penjelasan tetap merujuk ke berkas modul agar mahasiswa belajar
  dari kesalahan.

Bobot kuis dalam nilai akhir UAS: 10% (skor terbaik dari attempts).
"""
from __future__ import annotations

from typing import List, TypedDict


class Soal(TypedDict):
    soal: str
    opsi: List[str]
    jawaban: int  # index 0-3
    penjelasan: str
    rujukan: str


# ============================================================
# M01 — Pondasi: Konsep, Lanskap, Etika Pengantar, Kritik AI
# ============================================================
QUIZ_M01: List[Soal] = [
    {
        "soal": "Komponen 5V big data yang paling kritis dalam menentukan apakah kita bisa percaya data adalah:",
        "opsi": [
            "Volume (banyak baris)",
            "Velocity (cepat alir)",
            "Variety (bermacam bentuk)",
            "Veracity (kebenaran/kredibilitas)",
        ],
        "jawaban": 3,
        "penjelasan": (
            "Veracity adalah dimensi yang menanyakan: 'apakah data ini "
            "benar dan dapat dipercaya?' Tanpa veracity, volume sebanyak "
            "apa pun sia-sia. Inilah yang paling dekat dengan prinsip "
            "tabayyun."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §2",
    },
    {
        "soal": "Sumber data resmi untuk monitoring guru madrasah dan status sertifikasinya adalah:",
        "opsi": ["BPS", "AKMI", "Simpatika", "PISA"],
        "jawaban": 2,
        "penjelasan": (
            "Simpatika dikelola Kemenag khusus untuk data guru madrasah "
            "dan sertifikasi. BPS untuk statistik umum, AKMI untuk asesmen "
            "literasi-numerasi siswa, PISA studi internasional."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §3",
    },
    {
        "soal": "Prinsip *tabayyun* dalam Q.S. al-Ḥujurāt: 6 mengajarkan kepada analis data untuk:",
        "opsi": [
            "Menjaga kerahasiaan data pribadi",
            "Verifikasi sumber sebelum menyimpulkan",
            "Membagi data dengan adil",
            "Menganonimkan identitas",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Tabayyun secara harfiah berarti 'meneliti hingga jelas'. "
            "Dalam analitik data, ini berarti memverifikasi sumber, "
            "tahun, definisi variabel, dan metode pengumpulan sebelum "
            "menarik kesimpulan apa pun."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §4",
    },
    {
        "soal": "Risiko paling besar saat mahasiswa mengandalkan jawaban AI tanpa verifikasi independen adalah:",
        "opsi": [
            "Respons AI lambat",
            "Halusinasi — AI mengarang ayat/hadis/sumber yang tidak ada",
            "Limit token harian habis",
            "Server vendor down",
        ],
        "jawaban": 1,
        "penjelasan": (
            "LLM (Large Language Model) terkenal bisa menghasilkan teks "
            "yang terdengar meyakinkan tetapi salah — termasuk mengarang "
            "ayat Al-Qur'an, hadis, atau referensi buku fiktif. Ini "
            "pelanggaran serius prinsip ṣidq."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §5a",
    },
    {
        "soal": "*Cognitive offloading* dalam konteks pemakaian AI sebagai mitra belajar berarti:",
        "opsi": [
            "Memuat data ke server cloud",
            "Menurunnya kemampuan berpikir kritis karena terlalu mengandalkan AI",
            "Backup memori ke disk eksternal",
            "Multitasking antar aplikasi",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Cognitive offloading adalah fenomena turunnya kemampuan "
            "kognitif manusia ketika tugas berpikir 'dipindahkan' ke alat "
            "eksternal. Studi pendidikan menunjukkan ketergantungan AI "
            "yang berlebihan dapat mengikis kemampuan berpikir kritis."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §5e",
    },
    {
        "soal": "Manakah yang BUKAN termasuk lanskap data pendidikan Islam resmi di Indonesia?",
        "opsi": ["EMIS Kemenag", "Simpatika", "Wikipedia Indonesia", "AKMI"],
        "jawaban": 2,
        "penjelasan": (
            "Wikipedia adalah sumber sekunder yang dapat disunting siapa "
            "pun — bukan sumber resmi. EMIS, Simpatika, AKMI semua "
            "dikelola Kemenag/Kemdikbud sebagai sumber primer."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §3",
    },
    {
        "soal": "Definisi literasi data yang paling tepat untuk calon guru PAI adalah kemampuan:",
        "opsi": [
            "Hanya menghitung statistika dasar",
            "Membaca, memahami, mengkritisi, mengkomunikasikan, dan bertindak atas data",
            "Membuat dashboard interaktif",
            "Mengoperasikan Microsoft Excel dengan rumus rumit",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Literasi data mencakup 5 dimensi sekaligus: baca, paham, "
            "kritis, komunikasi, dan bertindak. Bukan hanya keterampilan "
            "teknis seperti Excel atau pembuatan chart."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §1",
    },
    {
        "soal": "Asisten AI yang mengutip 'kitab al-Bidāyah karya al-Ghazālī halaman 234' dalam jawabannya — Anda harus melakukan apa?",
        "opsi": [
            "Langsung kutip di brief Anda",
            "Verifikasi ke kitab cetak/database resmi sebelum dipakai (tabayyun)",
            "Percaya saja karena AI canggih",
            "Tanya AI lagi untuk konfirmasi",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Ini contoh klasik halusinasi AI: mengutip sumber yang "
            "kelihatan kredibel tapi mungkin tidak ada. Verifikasi ke "
            "sumber primer (kitab cetak, islamweb.net, dll.) WAJIB "
            "dilakukan sebelum mengutip. Bertanya ke AI lagi tidak akan "
            "memvalidasi — AI bisa konsisten salah."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §5a",
    },
    {
        "soal": "Prinsip *amānah* dalam etika data Islam berarti data dianggap sebagai:",
        "opsi": [
            "Titipan yang wajib dijaga",
            "Komoditas yang bebas diperdagangkan",
            "Aset yang harus dipublikasikan",
            "Catatan yang harus dihapus berkala",
        ],
        "jawaban": 0,
        "penjelasan": (
            "Amānah berarti titipan — data orang lain (siswa, guru, "
            "dsb.) adalah amanah yang wajib dijaga kerahasiaan dan "
            "integritasnya. Ini termasuk akses terbatas (least privilege) "
            "dan anonimisasi yang sungguh-sungguh."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §4",
    },
    {
        "soal": "AKMI (Asesmen Kompetensi Madrasah Indonesia) mengukur kompetensi:",
        "opsi": [
            "Tingkat ekonomi keluarga siswa",
            "Literasi membaca dan numerasi siswa madrasah",
            "Sertifikasi guru",
            "Akreditasi madrasah",
        ],
        "jawaban": 1,
        "penjelasan": (
            "AKMI adalah asesmen literasi-numerasi siswa madrasah, mirip "
            "AKM untuk sekolah umum. Bukan tentang ekonomi, sertifikasi "
            "guru, atau akreditasi institusi."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §3",
    },
    {
        "soal": "Uji Verifikasi 4 Langkah sebelum memakai jawaban AI mencakup: cek sumber, cek fakta, cek bias, dan:",
        "opsi": [
            "Cek waktu respons",
            "Cek bahasa yang dipakai",
            "Cek implikasi etis",
            "Cek format keluaran",
        ],
        "jawaban": 2,
        "penjelasan": (
            "Cek etis adalah langkah keempat yang krusial: apakah "
            "rekomendasi AI merugikan kelompok tertentu? Apakah "
            "menghormati maqāṣid? Aspek etis tidak dapat diserahkan ke AI."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §5",
    },
    {
        "soal": "Dimensi 'Variety' dalam 5V big data merujuk pada:",
        "opsi": [
            "Banyak baris data",
            "Bermacam bentuk: tabel, teks, audio, video",
            "Cepatnya data berubah",
            "Kesulitan akses ke data",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Variety adalah keragaman bentuk data — tabular, teks "
            "tidak terstruktur, audio kajian, video pembelajaran, dst. "
            "Volume terkait jumlah, Velocity terkait kecepatan, Variety "
            "terkait jenis."
        ),
        "rujukan": "modul/M01-pondasi-literasi-data.md §2",
    },
]


# ============================================================
# M02 — Praktik: Cleaning, Statistika Deskriptif, Visualisasi
# ============================================================
QUIZ_M02: List[Soal] = [
    {
        "soal": "Langkah pertama yang HARUS dilakukan saat menerima dataset baru adalah:",
        "opsi": [
            "Hitung mean semua kolom",
            "Inspeksi tipe data, missing values, duplikat",
            "Buat visualisasi spektakuler",
            "Hitung korelasi antar variabel",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Inspeksi awal (data understanding) wajib dilakukan dulu "
            "untuk mengetahui apa yang kita pegang. Tanpa ini, semua "
            "analisis berikutnya berisiko salah karena asumsi yang keliru."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §2",
    },
    {
        "soal": "Untuk membandingkan distribusi nilai PAI antar 4 kelompok akreditasi (A, B, C, Belum), visualisasi paling tepat adalah:",
        "opsi": ["Pie chart", "Boxplot", "Line chart", "Scatter plot"],
        "jawaban": 1,
        "penjelasan": (
            "Boxplot menunjukkan distribusi (median, kuartil, outlier) "
            "untuk tiap kelompok dalam satu visual — memungkinkan "
            "perbandingan langsung. Pie chart untuk proporsi, Line "
            "untuk time series, Scatter untuk dua numerik."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §4",
    },
    {
        "soal": "Median lebih tepat dipakai dibanding mean ketika:",
        "opsi": [
            "Data berdistribusi normal",
            "Ada outlier ekstrem dalam data",
            "Sampel sangat kecil (<5)",
            "Data berupa kategori",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Mean sensitif terhadap outlier — satu nilai sangat ekstrem "
            "bisa menggeser mean jauh dari pusat sebenarnya. Median (nilai "
            "tengah) tidak terpengaruh outlier, sehingga lebih robust."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §3",
    },
    {
        "soal": "Untuk memvisualisasikan hubungan antara dua variabel numerik kontinu, chart paling tepat adalah:",
        "opsi": ["Bar chart", "Pie chart", "Scatter plot", "Histogram"],
        "jawaban": 2,
        "penjelasan": (
            "Scatter plot adalah chart standar untuk 2 variabel numerik. "
            "Histogram untuk 1 variabel numerik (distribusi), bar untuk "
            "kategori, pie untuk proporsi."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §4",
    },
    {
        "soal": "Anti-pola visualisasi yang harus dihindari adalah:",
        "opsi": [
            "Sumbu y mulai dari nol untuk bar kuantitas",
            "Pie chart dengan lebih dari 5 irisan",
            "Label sumbu yang jelas",
            "Caption yang informatif",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Pie chart >5 irisan sulit dibaca — mata manusia kesulitan "
            "membandingkan sudut yang banyak dan kecil. Bar chart lebih "
            "efektif untuk >5 kategori. Tiga opsi lainnya justru praktik "
            "baik."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §4",
    },
    {
        "soal": "Standar deviasi (standard deviation) mengukur:",
        "opsi": [
            "Nilai tengah data",
            "Sebaran (dispersi) data dari mean",
            "Korelasi antar variabel",
            "Frekuensi kategori",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Standar deviasi adalah ukuran sebaran — seberapa jauh nilai "
            "individual menyimpang dari mean. SD kecil = data terkonsentrasi, "
            "SD besar = data tersebar luas."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §3",
    },
    {
        "soal": "Untuk meringkas variabel kategorik dengan banyak nilai unik (mis. provinsi), cara yang tepat adalah:",
        "opsi": [
            "Hitung mean dan median",
            "Tabel frekuensi + persentase",
            "Buat boxplot",
            "Buat scatter plot",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Variabel kategorik tidak punya 'mean' yang bermakna. Tabel "
            "frekuensi (count + persentase per kategori) adalah ringkasan "
            "standar. Boxplot/scatter untuk numerik."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §3",
    },
    {
        "soal": "Manakah yang BUKAN termasuk pembersihan data (data cleaning)?",
        "opsi": [
            "Menangani missing values",
            "Menghapus duplikat",
            "Menafsirkan implikasi pedagogis hasil",
            "Standardisasi label inkonsisten",
        ],
        "jawaban": 2,
        "penjelasan": (
            "Penafsiran adalah tahap setelah analisis, bukan cleaning. "
            "Cleaning fokus pada kualitas data: missing, duplikat, tipe, "
            "konsistensi label."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §2",
    },
    {
        "soal": "IQR (Interquartile Range = Q3 - Q1) berguna utamanya untuk:",
        "opsi": [
            "Mendeteksi outlier",
            "Menghitung rata-rata",
            "Membuat histogram",
            "Menghitung korelasi",
        ],
        "jawaban": 0,
        "penjelasan": (
            "IQR adalah ukuran sebaran 50% data tengah. Outlier biasanya "
            "didefinisikan sebagai nilai di bawah Q1 - 1.5*IQR atau di "
            "atas Q3 + 1.5*IQR (aturan Tukey)."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §3",
    },
    {
        "soal": "*Data storytelling* yang baik dicirikan oleh:",
        "opsi": [
            "Menampilkan sebanyak mungkin chart sekaligus",
            "Naratif yang membimbing pembaca melalui temuan secara logis",
            "Penggunaan efek 3D agar terlihat menarik",
            "Memotong sumbu y untuk mendramatisir perbedaan",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Data storytelling adalah seni menyusun temuan menjadi "
            "narasi yang bermakna. Chart melimpah, efek 3D, dan sumbu "
            "manipulatif justru anti-pola."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §4",
    },
    {
        "soal": "Notebook analisis yang reproducible berarti:",
        "opsi": [
            "Banyak komentar di kode",
            "Bisa dijalankan ulang dari awal (kernel restart → run all) tanpa error",
            "Memakai banyak library populer",
            "Dipresentasikan dengan font besar",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Reproducible = orang lain (atau Anda di masa depan) bisa "
            "menjalankan ulang dan mendapat hasil sama persis. Ini "
            "mensyaratkan kode yang bersih, dependency yang jelas, dan "
            "tidak ada 'state tersembunyi'."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §5",
    },
    {
        "soal": "Untuk visualisasi PROPORSI 3 kategori (mis. distribusi madrasah Negeri-Swasta-Lainnya), pilihan terbaik adalah:",
        "opsi": [
            "Pie chart (jika kategori sedikit) atau bar chart",
            "Scatter plot",
            "Boxplot",
            "Heatmap",
        ],
        "jawaban": 0,
        "penjelasan": (
            "Untuk 2-5 kategori dengan proporsi, pie chart bisa OK, "
            "tapi bar chart lebih akurat. Boxplot/scatter/heatmap tidak "
            "cocok untuk proporsi sederhana."
        ),
        "rujukan": "modul/M02-praktik-analisis-data.md §4",
    },
]


# ============================================================
# M03 — Sintesis: Confounder, Maqāṣid, Ghībah, Policy Brief
# ============================================================
QUIZ_M03: List[Soal] = [
    {
        "soal": "Korelasi positif yang tinggi antara variabel X dan Y berarti:",
        "opsi": [
            "X pasti menyebabkan Y",
            "Y pasti menyebabkan X",
            "X dan Y bergerak bersama, tetapi sebab-akibat belum tentu",
            "Tidak ada hubungan apa pun",
        ],
        "jawaban": 2,
        "penjelasan": (
            "Korelasi ≠ kausalitas. Mereka bergerak bersama, tapi "
            "penyebab bisa: X→Y, Y→X, atau confounder Z→keduanya. "
            "Inilah inti tabayyun dalam analisis data."
        ),
        "rujukan": "modul/M03-sintesis-etika-dan-kebijakan.md §1",
    },
    {
        "soal": "Dalam contoh 'sertifikasi guru ↔ nilai PAI tinggi', confounder yang paling mungkin adalah:",
        "opsi": [
            "Warna kulit guru",
            "Akreditasi madrasah (mempengaruhi keduanya)",
            "Hari absensi",
            "Nama madrasah",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Akreditasi A cenderung punya guru lebih sering disertifikasi "
            "DAN nilai siswa lebih tinggi — mempengaruhi kedua variabel "
            "secara independen. Tanpa mengontrol akreditasi, korelasi "
            "sertifikasi-nilai bisa menyesatkan."
        ),
        "rujukan": "modul/M03-sintesis-etika-dan-kebijakan.md §1",
    },
    {
        "soal": "*Reverse causation* (sebab-akibat terbalik) terjadi ketika:",
        "opsi": [
            "Korelasi sama dengan kausalitas",
            "Y sebenarnya yang menyebabkan X, bukan X→Y seperti yang kita kira",
            "Sampel terlalu kecil",
            "Variabel tidak relevan",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Contoh: madrasah dengan dashboard data kelihatan punya nilai "
            "tinggi. Tapi mungkin BUKAN dashboard → nilai naik, melainkan "
            "madrasah unggul (nilai tinggi) → mampu beli dashboard."
        ),
        "rujukan": "modul/M03-sintesis-etika-dan-kebijakan.md §1",
    },
    {
        "soal": "*Selection bias* dalam survei online tentang literasi digital guru terjadi karena:",
        "opsi": [
            "Sampel acak yang representatif",
            "Yang mengisi survei online cenderung yang melek digital — sampel tidak mewakili semua guru",
            "Skor tertinggi otomatis dipilih",
            "Variabel yang salah diukur",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Selection bias = sampel yang masuk ke analisis bukan sampel "
            "acak dari populasi. Survei online inherently bias — guru "
            "yang gaptek mungkin tidak akan mengisi sama sekali."
        ),
        "rujukan": "modul/M03-sintesis-etika-dan-kebijakan.md §1",
    },
    {
        "soal": "Lima ḍarūriyyāt (kebutuhan primer) dalam maqāṣid al-syarīʿah meliputi:",
        "opsi": [
            "Ḥifẓ al-dīn, al-nafs, al-ʿaql, al-nasl, al-māl",
            "Ḥifẓ al-ʿuqūd, al-buyūʿ, al-rahn, al-qarḍ, al-syarikāt",
            "Sholat, zakat, puasa, haji, syahadat",
            "Tauhid, kenabian, kitab, malaikat, akhirat",
        ],
        "jawaban": 0,
        "penjelasan": (
            "Lima ḍarūriyyāt adalah perlindungan agama (dīn), jiwa (nafs), "
            "akal (ʿaql), keturunan (nasl), dan harta (māl). Ini kerangka "
            "klasik al-Syāṭibī yang diperluas Ibn ʿĀshūr & Auda."
        ),
        "rujukan": "modul/M03-sintesis-etika-dan-kebijakan.md §2",
    },
    {
        "soal": "Plagiarisme dalam policy brief paling jelas melanggar maqṣad:",
        "opsi": [
            "Ḥifẓ al-māl (perlindungan harta)",
            "Ḥifẓ al-dīn (perlindungan agama)",
            "Ḥifẓ al-ʿaql (perlindungan akal/keilmuan)",
            "Ḥifẓ al-nasl (perlindungan keturunan)",
        ],
        "jawaban": 2,
        "penjelasan": (
            "Plagiarisme merusak integritas keilmuan — yang sangat "
            "terkait dengan ḥifẓ al-ʿaql. Calon guru yang melegitimasi "
            "kebohongan akademik akan meneruskan budaya itu ke murid-"
            "muridnya."
        ),
        "rujukan": "modul/M03-sintesis-etika-dan-kebijakan.md §2",
    },
    {
        "soal": "*Ghībah* dalam analisis data terjadi ketika analis:",
        "opsi": [
            "Menganonimkan data dengan benar",
            "Mempublikasikan kelemahan kelompok tertentu (mis. madrasah X kurang) tanpa kemaslahatan kebijakan yang jelas",
            "Menabulasi data agregat",
            "Menghitung rata-rata kelas",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Ghībah = membicarakan kekurangan orang/kelompok di belakang. "
            "Data analytic bisa terjebak ghībah sistematis kalau "
            "menyebarkan kekurangan tanpa tujuan kemaslahatan. Hadis "
            "Bukhari-Muslim menegaskan: ghībah tetap berdosa walau "
            "yang dikatakan benar."
        ),
        "rujukan": "modul/M03-sintesis-etika-dan-kebijakan.md §4",
    },
    {
        "soal": "*Cherry-picking visual* dalam policy brief berarti:",
        "opsi": [
            "Memakai banyak warna menarik",
            "Hanya menampilkan grafik yang mendukung argumen kita, mengabaikan yang menentangnya",
            "Memakai chart 3D untuk efek wow",
            "Mulai sumbu y dari nol",
        ],
        "jawaban": 1,
        "penjelasan": (
            "Cherry-picking = memilih bukti selektif. Ini pelanggaran "
            "ṣidq — kejujuran. Brief yang etis menampilkan SEMUA bukti, "
            "termasuk yang melemahkan argumen sendiri, lalu menjelaskan "
            "kenapa tetap mengambil kesimpulan tertentu."
        ),
        "rujukan": "modul/M03-sintesis-etika-dan-kebijakan.md §5",
    },
    {
        "soal": "Manakah bagian yang TIDAK ada dalam template policy brief mini UAS?",
        "opsi": [
            "Ringkasan eksekutif",
            "Daftar pustaka & data",
            "Bahasan ghībah dosen pengampu",
            "Pertimbangan etis Islam",
        ],
        "jawaban": 2,
        "penjelasan": (
            "Template policy brief punya 7 bagian: ringkasan eksekutif, "
            "latar belakang, temuan, diskusi & batasan, rekomendasi, "
            "pertimbangan etis, daftar pustaka. Tidak ada bahasan ghībah "
            "dosen — itu di luar konteks akademik dan tidak etis."
        ),
        "rujukan": "modul/M03-sintesis-etika-dan-kebijakan.md §6",
    },
    {
        "soal": "Pengurangan nilai paling berat dalam rubrik R03 adalah untuk pelanggaran:",
        "opsi": [
            "Tidak isi Form Pengungkapan AI (-20)",
            "Cherry-picking visual (-15)",
            "Plagiarisme/fabrikasi/joki (nilai 0 keseluruhan)",
            "Telat submit 1 hari (-5)",
        ],
        "jawaban": 2,
        "penjelasan": (
            "Plagiarisme, fabrikasi data, atau joki adalah pelanggaran "
            "fundamental terhadap ṣidq dan ḥifẓ al-ʿaql — sehingga "
            "konsekuensinya juga fundamental: nilai 0 keseluruhan, "
            "bukan sekadar pengurangan poin."
        ),
        "rujukan": "rubrik/R03-policy-brief-mini.md",
    },
    {
        "soal": "Indikator rekomendasi kebijakan yang baik mencakup semua, KECUALI:",
        "opsi": [
            "Aktor yang harus melaksanakan",
            "Jangka waktu",
            "Indikator keberhasilan yang terukur",
            "Nama dosen yang membimbing",
        ],
        "jawaban": 3,
        "penjelasan": (
            "Rekomendasi yang konkret butuh: SIAPA (aktor), KAPAN "
            "(jangka), dan APA UKURAN SUKSES (indikator). Nama dosen "
            "tidak relevan dalam rekomendasi kebijakan."
        ),
        "rujukan": "tugas/template-policy-brief.md §5",
    },
    {
        "soal": "Bila rekomendasi kebijakan Anda lebih menguntungkan madrasah perkotaan dan merugikan madrasah 3T, prinsip etika yang paling dilanggar adalah:",
        "opsi": [
            "Tabayyun",
            "Ṣidq",
            "ʿAdl",
            "Amānah",
        ],
        "jawaban": 2,
        "penjelasan": (
            "ʿAdl (keadilan) khusus mengatur fairness lintas kelompok. "
            "Rekomendasi yang sistematis merugikan kelompok marjinal "
            "(seperti madrasah 3T) adalah pelanggaran ʿadl, walaupun "
            "data dan analisisnya teknis benar."
        ),
        "rujukan": "modul/M03-sintesis-etika-dan-kebijakan.md §3c",
    },
]


# Mapping modul → daftar soal
QUIZ_BY_MODUL = {
    "M01": {
        "judul": "M01 — Pondasi Literasi Data",
        "deskripsi": "Konsep big data, lanskap data PAI, etika pengantar, kritik AI",
        "soal": QUIZ_M01,
    },
    "M02": {
        "judul": "M02 — Praktik Analisis Data",
        "deskripsi": "Cleaning, statistika deskriptif, visualisasi",
        "soal": QUIZ_M02,
    },
    "M03": {
        "judul": "M03 — Sintesis Etika & Kebijakan",
        "deskripsi": "Confounder, maqāṣid, ghībah, policy brief",
        "soal": QUIZ_M03,
    },
}


def get_modul_list() -> list[str]:
    """Daftar kode modul yang punya kuis."""
    return list(QUIZ_BY_MODUL.keys())


def get_quiz(modul: str) -> dict | None:
    return QUIZ_BY_MODUL.get(modul)


def total_soal(modul: str) -> int:
    q = get_quiz(modul)
    return len(q["soal"]) if q else 0
