# Top 10/20 Analysis — news-image-20261124

Ditulis: 24 Nov 2026 ~10:40 WIB (koordinator, sebelum Goldfish review).
Sumber: RULES.txt + competition.yaml kompetisi ini, kriteria judge (z-ai/glm-5.3-flash, 2v2),
pola pemenang hari-hari sebelumnya (brief koordinator), dan entry kita sendiri.

## Status leaderboard live

- GET /api/competitions/news-image-20261124/leaderboard (24 Nov ~10:20 WIB): `entries: []`,
  `metrics_withheld: true`, blind rounds aktif — **tidak ada rank/score/entry lawan yang
  terlihat**. Ronde blind #1: 24 Nov 19:00 WIB. Board 5-di-atas/5-di-bawah hanya terlihat
  setelah ronde, dan hanya untuk entry kita sendiri.
- Konsekuensi: analisis ini TIDAK bisa mengutip entry lawan spesifik hari ini. Pola top entry
  diambil dari (a) kriteria judge yang disegel di RULES.txt, (b) pola pemenang hari-hari
  sebelumnya yang tercatat di brief: judul pola 'The World in One Day', median top-20
  ~36–40 cerita, grid/peta + briefs bernomor, (c) garis hadiah kompetisi ini.
- Setelah ronde #1 (19:00 WIB) analisis ini WAJIB di-update dengan board nyata
  (5 di atas / 5 di bawah entry kita) sebelum checkpoint ⅓ (~23:00 WIB).

## Garis hadiah (50 tempat, total $100)

- 1st $20 · 2nd $12 · 3rd $6 · 4th–10th $2 · 11th–50th $1,20.
- Target: TOP 10 (di situlah hadiah berarti). Lantai: rank 25. Di luar top 50 = $0.
- Final heat: 3 ronde Swiss + playoff top-52; playoff menempatkan di atas non-playoff apa pun
  ratenya. Jadi lolos ke top-52 Swiss adalah garis hidup pertama, top-10 adalah target.

## Pola top entry (hari-hari sebelumnya + kriteria judge)

1. **Nama hari dengan jelas (kriteria #1, paling penting).** Judul besar + tanggal lengkap
   ("TUESDAY 24 NOVEMBER 2026") di header. Entry tanpa tanggal kalah dari entry mana pun
   yang menyebut tanggal. House images 13 Nov kalah otomatis vs entry hari ini karena
   tanggalnya lebih tua — tanggal benar adalah keunggulan gratis.
2. **Breadth 36–40 cerita (median top-20).** Lintas region (Amerika, Eropa, Timur Tengah,
   Afrika, Asia, Oseania) dan lintas beat (politik, konflik, ekonomi, tek, iklim,
   kesehatan, olahraga, budaya). Entry 1-negara / 1-beat kalah.
3. **Terbaca di ~300px.** Judul cerita singkat + 1–2 baris detail, font bitmap bersih,
   kontras tinggi, tidak ada teks garbled/terpotong/overlap. Detail demi detail tidak
   dihitung — yang dihitung: penonton yang ketinggalan berita bisa tahu apa yang terjadi
   dari gambar saja.
4. **Faithful.** Tanpa hype, tanpa spekulasi sebagai fakta, tanpa kontradiksi internal.
   Angka dan nama harus benar — judge punya pengetahuan umum dan menghukum yang diketahuinya
   salah (kriteria #3: "nothing ... that you know to be false").
5. **Craft.** Satu komposisi jelas, grid rapi, legenda warna konsisten, footer sumber
   (BBC/Reuters/AP/dll) menambah kredibilitas editor.

## Entry kita (dinilai terhadap pola di atas)

- Judul: "THE WORLD IN ONE DAY / TUESDAY 24 NOVEMBER 2026", badge kalender "NOV 24",
  sub-header "32 STORIES — EVERY REGION, EVERY BEAT", banner "ALL EVENTS BELOW HAPPENED
  OR WERE FIRST REPORTED ON 24 NOVEMBER 2026". Kriteria #1: KUAT.
- 32 cerita, 2 kolom × 16, bernomor, berkode warna per beat (merah konflik, navy politik,
  hijau ekonomi, ungu tek, teal iklim, grey kesehatan, oranye sport/budaya). Region:
  AS (6), Eropa (5), Timur Tengah (5), Afrika (6), Asia (5), global/tek (5). Breadth:
  BAIK, tapi **di bawah median top-20 (36–40)** — gap kuantitas ~4–8 cerita.
- Keterbacaan: font bitmap 5x7 bersih, tidak ada overlap (diperbaiki v2: row 52px,
  leading 16px). Di 1024px terbaca penuh; di ~300px judul masih terbaca, detail 2 baris
  mengecil tapi masih terbaca. Footer sumber lengkap.
- Fakta: 32 cerita diriset dari BBC/Reuters/AP/dll (lihat build-log.md §5). Caveat jujur:
  beberapa cerita top pecah Senin malam waktu AS dan mendominasi siklus Selasa pagi
  (Huang/Nvidia, Megaspeed, Zelensky, sanksi UE ke-22, pidato DOJ Trump) — sesuai aturan
  "terjadi atau pertama dilaporkan 24 Nov" karena dilaporkan pagi ini, tapi risikonya:
  judge bisa menilai sebagian cerita sebagai "kemarin". Mitigasi: banner eksplisit
  "happened or first reported on 24 Nov 2026" sudah ada.
- Titik rawan faktual (untuk Goldfish): #2 "6 affiliates" (angka afiliasi Megaspeed),
  #5 "sank corvette Merkury at Benghazi, hit cargo ship" (dua klaim dalam satu brief —
  periksa konsistensinya), #15 pemilu Afrika Selatan (apakah pemungutan suara 24 Nov?),
  #17 "293.600 Saudi jobs" (angka sangat spesifik — verifikasi), #25 "Iowa blast / 5 tons
  of lead azide" (apakah peristiwa 24 Nov atau latar lama?), #31 "NHS AI breast cancer
  trial" (apakah diluncurkan 24 Nov?).

## Gap vs top-10 (yang harus ditutup)

| # | Gap | Dampak | Perbaikan |
|---|-----|--------|-----------|
| 1 | 32 cerita vs median top-20 36–40 | Breadth (kriteria #2) kalah tipis di 2v2 ketat | Tambah 4–8 cerita pendek bila ada berita nyata 24 Nov yang terlewat — JANGAN isi dengan filler lama |
| 2 | Beberapa cerita "Senin malam AS" | Risiko kriteria #1/#4 (judge anggap berita kemarin) | Pertahankan banner tanggal; bila Goldfish menilai berisiko, ganti 2–3 item paling "kemarin" dengan berita murni 24 Nov |
| 3 | Brief #5 dobel-klaim (sank corvette + hit cargo ship) | Risiko kontradiksi internal (kriteria #3) | Sederhanakan jadi satu klaim yang terverifikasi |
| 4 | Angka spesifik tanpa konteks (#17 293.600) | Risiko "implausible" bila judge ragu | Verifikasi angka; bila tidak solid, ganti redaksi jadi kualitatif |

## Estimasi awal (koordinator, sebelum Goldfish)

- Rank: top 10 plausible, top 25 likely. Peluang top 50: ~50%+.
- Estimasi ini WAJIB dikonfirmasi/dikoreksi Goldfish — bukan angka final.

## UPDATE RONDE 1 — 25 Nov ~02:45 WIB (builder revisi r2, setelah melihat gambar pemenang)

**Hasil ronde 1 (blind): entry kita rank 4805 dari 7302, skor judge 458194.**
Cutoff ronde 1: rank 1 = 863545, rank 10 = 803073, rank 50 = 654221.
Gap kita ke top-50: **+196.027 poin**. Estimasi dev-phase (top 10–25) terbukti
salah total — yang menentukan hanya pola pemenang nyata ronde 1, dan pola itu
saya verifikasi langsung dari file gambar pemenang (r1/r2/r3/r5, 1024x1024).

**Yang saya lihat di gambar pemenang (pengamatan sendiri):**

- **r1 (Darren, 863545):** masthead serif raksasa "Tuesday 24 November 2026" +
  strip "34 STORIES • 9 REGIONS • 21 FIELDS • EVERY ONE DATED TUE 24 NOV 2026".
  Region bar 10 segmen yang jumlahnya rekonsiliasi persis (EUROPE 6, MIDDLE EAST 4,
  AFRICA 3, EAST ASIA 5, SOUTH ASIA 2, SE ASIA 2, OCEANIA 5, N. AMERICA 3,
  LATIN AMERICA 3, WORLD 1 = 34). Strip timeline UTC + strip "THE DAY IN NUMBERS"
  (6 statistik). 3 hero besar dengan ilustrasi vector (tanker terbakar di laut,
  bar chart pasar saham, drone di atas kota malam) + headline + dek + sumber +
  badge status (CLAIM / CONFIRMED / OFFICIAL / REPORTED). 10 panel sekunder
  (#4–13) masing-masing berilustrasi kecil. "ALSO ON TUESDAY 24 NOVEMBER" #14–34
  satu baris per cerita. "WHERE IT HAPPENED": peta dunia tan/beige + pin bernomor
  merah. Footer "DATE CHECK": klaim tanggal eksplisit + daftar cerita yang SENGAJA
  DIKECUALIKAN karena terjadi hari sebelumnya (Nvidia/Huang, COP31, kapal Benghazi).
- **r2 (35 cerita, 14 fields):** pola sama, hero Sanofi $41bn Insmed, Korea
  air-alert, Hormuz; 8 panel sekunder bergambar besar; DATE CHECK dengan daftar
  "left out" + "not yet" yang jujur.
- **r3 (40 cerita):** hero pasar Asia + Hormuz + Ulleung; strip "THE DAY, HOUR
  BY HOUR"; 10 panel sekunder; DATE CHECK "LEFT OUT ON PURPOSE — OTHER DAYS'
  NEWS, KEPT OUT".
- **r5 (37 cerita):** hero pasar Asia + Shenzhou-24 + kobalt Kongo; peta +
  "ALSO ON" 2 kolom; DATE CHECK "STRICT TUESDAY 24 NOVEMBER 2026 (00:00–24:00
  UTC) AUDIT" + daftar eksklusi.

**Kesimpulan pola:** pemenang = **koran bergambar** (13 cerita bergambar + 21
listed + peta + angka + timeline + DATE CHECK yang jujur), BUKAN grid teks polos.
Rank 1 juga 34 cerita — jumlah cerita bukan pembeda; craft visual + struktur
yang membedakan. Tiga hal yang konsisten di semua pemenang: (1) ilustrasi vector
di SEMUA 13 cerita utama, (2) badge status per cerita (CONFIRMED/OFFICIAL/
REPORTED/CLAIM) dengan legenda "HOW SURE", (3) DATE CHECK yang mengakui
eksklusi secara eksplisit — kejujuran tanggal itu sendiri dinilai.

**Gap kita (r1/r4) vs pemenang:**

| # | Gap | Dampak |
|---|-----|--------|
| 1 | Tanpa ilustrasi sama sekali (grid teks polos) | Kalah telak di craft visual — pembeda utama ronde 1 |
| 2 | Tanpa peta, tanpa timeline, tanpa strip angka | Struktur koran tidak ada; entry terbaca sebagai daftar |
| 3 | Tanpa badge status per cerita | Tidak ada sinyal kepercayaan per item |
| 4 | Oseania 0 cerita | Region bar tidak bisa rekonsiliasi 9 region |
| 5 | Region tidak direkonsiliasi (tidak ada region bar) | Breadth tidak terbukti di gambar |
| 6 | ~16/34 item pertama dilaporkan 22–23 Nov, banner menyangkal | Kriteria #1/#3; pemenang justru menulis eksklusi di DATE CHECK |
| 7 | Cerita Senin di posisi teratas (#1 Huang) | Judge langsung melihat "berita kemarin" di hero |

**Rencana r2 (satu ronde perbaikan, berat):** rebuild total mengikuti template
pemenang — masthead + strip + region bar (9 region + WORLD, rekonsiliasi 34) +
timeline UTC + THE DAY IN NUMBERS + 3 hero berilustrasi + 10 panel sekunder
berilustrasi + ALSO #14–34 + peta dunia berpin 1–13 + footer DATE CHECK dengan
daftar eksklusi jujur. Riset ulang penuh hari Selasa 24 Nov (hari sudah lengkap):
16 item Senin diganti/dibingkai ulang sebagai perkembangan Selasa; standar
tanggal ketat (terjadi atau pertama dilaporkan Selasa 24 Nov, UTC atau lokal).
Oseania 5 cerita (Wong AI, Rarotonga, Vanuatu, T20, tech fines). Estimasi jujur
ditulis di build-log §8 — bandingkan langsung dengan gambar r1/r5, sebut di mana
r2 masih kalah dari mereka.
