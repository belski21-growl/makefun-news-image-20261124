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
