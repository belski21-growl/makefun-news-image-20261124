# Goldfish Review — news-image-20261124, revisi r2 (RE-REVIEW RONDE 1)

**Reviewer:** Goldfish (penilai independen, bukan builder)
**Tanggal review:** Rab 25 Nov 2026 ~03:30 WIB
**Entry dinilai:** `entry.png` r2 — 1024×1024, 50.263 byte, sha256
`96c141880f51cf7c853b91cc5addbc1aba71a228a0fea68f4690d09a4327aff0`
(terverifikasi cocok dengan build-log.md §8; render 2× byte-identik), `main.py`,
`build-log.md` §8, `top10-analysis.md` (UPDATE RONDE 1),
`goldfish-review-2.md`.
**Metode:** baca langsung entry.png (1024px + downscale 300px + crop-zoom 2×/4×
hero, sekunder baris 1–2, peta/ALSO, DATE CHECK) + baca `main.py` (data +
assert); verifikasi faktual via pencarian web untuk ke-13 cerita utama,
ke-6 tonggak timeline, ke-6 angka strip, dan 21/21 item ALSO #14–34
(total 25+ kueri pencarian, sumber Reuters/AP/AFP/BBC/ABC/Euronews/
Xinhua/NASA/Roscosmos/Arianespace/dll).

**Keterbatasan penting:** gambar pemenang ronde 1 (`/tmp/ni24-top/r1_darren.webp`,
`r5_puffin.webp`, `r3_koala.webp`) **sudah tidak ada** — `/tmp` dibersihkan
antar-run di VM ini (build-log §8 sendiri mencatatnya); pencarian di seluruh
`~/workspace` tidak menemukan salinannya. Perbandingan craft vs pemenang di
bawah ini karena itu memakai deskripsi tertulis yang detail di
top10-analysis.md UPDATE RONDE 1 + build-log §8, BUKAN pengamatan langsung
atas gambar r1/r5. Bila koordinator masih punya file webp itu, perbandingan
visual langsung layak diulang sebelum submit.

## VERDICT: LAYAK LANJUT BELUM LAYAK SUBMIT

Rebuild r2 adalah lompatan besar dan nyata dari r1/r4: struktur kini sejajar
template pemenang (3 hero berilustrasi + 10 panel berilustrasi + peta berpin
+ timeline UTC + strip angka + region bar yang direkonsiliasi + DATE CHECK
dengan daftar eksklusi jujur + Oseania 5 cerita), dan 30 dari 34 cerita
terverifikasi BENAR sebagai berita Selasa 24 Nov 2026, termasuk semua angka
hero (Taiex +9%, Kospi +7,5%, Nikkei +4,5%; 96 drone/73 downed; M5.3
01:32 UTC; Sanofi $41BN/$175; supermoon 14:53 UTC).

Tapi blocker ronde lalu **belum tertutup penuh, hanya mengecil**: klaim
tanggal universal di gambar — "EVERY ONE DATED TUE 24 NOV 2026" (strip
header) dan "EVERY STORY ABOVE HAPPENED OR WAS FIRST REPORTED ON TUESDAY
24 NOVEMBER 2026" (DATE CHECK) — masih dipalsukan oleh **4 dari 34 item**
(#12, #22, #24, #25), ditambah 1 abu-abu (#23). Di ronde lalu angkanya
16/34 (47%); kini 4/34 (12%). Itu kemajuan besar, tapi kelas cacatnya
persis sama dengan blocker ronde-2 — klaim universal yang terbukti salah —
dan build-log §8 justru salah memberi tanggal pada 3 dari 4 item itu
(ditulis "24 Nov", nyatanya 23 Nov). Perbaikannya murah (satu putaran,
tanpa ubah layout bila penggantinya cerita teks ALSO; panel #12 hanya
butuh ganti teks + kicker). Selama klaim itu masih salah di gambar,
entry ini belum layak submit.

## Blocker

1. **Klaim tanggal universal masih salah untuk 4 item — #12, #22, #24,
   #25 (plus #23 abu-abu).** Detail per item di tabel §Fakta:
   - **#12 DR Congo:** pesawat jatuh Minggu 22 Nov ~06:00; klaim tembak
     FRN Minggu 22 Nov; pernyataan hilang-kontak FARDC Senin 23 Nov.
     Yang Selasa hanyalah pernyataan FRN menyebut tipenya Cessna 208 dan
     tulisan BBC/Reuters Selasa tentang pernyataan Senin itu. Inti berita
     ("pesawat hilang + pemberontak klaim menembak") pertama dilaporkan
     22–23 Nov, bukan 24 Nov.
   - **#22 UN AI safety:** pidato Guterres di Bridgetown **Senin 23 Nov**,
     dilaporkan Senin itu juga (Al Jazeera: "said Monday"; diplomacy.edu:
     "on 23 November 2026"). Build-log §8 menulis sumber "UN News,
     24 Nov" — tanggal UN News bukan tanggal pidatonya.
   - **#24 Denmark:** kesepakatan larangan HP diumumkan Kementerian
     Pendidikan Denmark **Senin 23 Nov** (semua sumber: "announced on
     November 23", "said on Monday"). Build-log §8 menulis "Govt
     statement, 24 Nov" — salah.
   - **#25 Syria demining:** eksklusif Reuters berdateline **"DAMASCUS,
     Nov 23"** ("Reuters reported on Monday, November 23"). Build-log §8
     menulis "Reuters, 24 Nov" — salah.
   - **#23 Grok (abu-abu, condong gagal):** gugatan Virginia + Oregon
     diajukan **Senin 23 Nov**; liputan besar (NPR, Reuters) Selasa pagi.
     Bila pengumuman AG Senin sore adalah laporan pertamanya, item ini
     gagal juga — putaran perbaikan wajib memverifikasi tanggal laporan
     pertamanya sebelum memutuskan dipertahankan atau diganti.
   Klaim "EVERY STORY" / "EVERY ONE DATED" hanya butuh satu counterexample
   untuk runtuh; di sini ada empat (lima bila #23 ikut). Risiko praktis
   dari judge memang lebih kecil daripada ronde lalu — keempat item ini
   jauh lebih tidak terkenal daripada Huang/COP31, dan judge (tanpa feed
   berita) kemungkinan besar tidak tahu tanggal persisnya — tapi Goldfish
   menilai klaimnya, bukan peluang judge menangkapnya: klaim yang kita
   TAHU salah tidak boleh disubmit. Catatan jujur: 8 eksklusi di DATE
   CHECK semuanya benar tanggalnya (Huang Sen 23, COP31 Min 22, Benghazi
   Min 22, sanksi UE ke-22 Sen 23, ATC Belgia Sen 23, UK 2035 Sen 23,
   Demokrat 258 Min 22, Gomez Sen 23) — kejujuran di sisi eksklusi sudah
   penuh; yang bocor hanya sisi inklusi.

## Major

2. **Sanofi "A 46% PREMIUM" tanpa basis — angka benar, konteks hilang.**
   $175/saham dan $41BN benar (Sanofi, 24 Nov). Tapi premi 46% adalah vs
   harga **pra-rumor 18 Nov** ($119,90); premi vs penutupan Senin yang
   dipakai hampir semua headline adalah **~17%** ($149,09). Tanpa
   kualifikasi, "A 46% PREMIUM" terbaca sebagai premi atas harga Senin —
   angka yang kemungkinan besar dikenal judge adalah 17%. Satu frasa
   ("46% OVER PRE-RUMOUR PRICE") atau ganti ke "17% OVER MONDAY CLOSE"
   menutupnya. "LARGEST SINCE 2004" benar ("biggest deal in over two
   decades", GlobalData).
3. **Craft masih satu tingkat di bawah pemenang — ini pembatas rank
   utama.** (Perbandingan via deskripsi tertulis pemenang, lihat
   keterbatasan di atas.) Font bitmap 5×7 kita terbaca sebagai pixel-art,
   bukan serif koran raksasa milik r1; ilustrasi kita geometri sederhana
   (balok, segitiga, titik) vs ilustrasi pemenang yang jauh lebih detail
   (asap berlapis, kota malam berpuluh jendela); peta kita poligon kasar
   (Korea jadi gumpalan tanpa bentuk, Taiwan tidak digambar sebagai
   daratan, Jepang selipis garis, tanpa label kota) vs peta pemenang yang
   rapi. Struktur sudah sejajar pemenang; polish tipografi + ilustrasi
   belum. Satu putaran perbaikan tidak menutup gap ini — yang bisa
   ditutup putaran ini hanya blocker tanggal + angka Sanofi.
4. **#9 / strip angka: "1,283 ASYLUM SEEKERS MOVED" melebih-lebihkan —
   1.283 adalah proyeksi akhir tahun, bukan yang sudah pindah.**
   Euronews (eksklusif 24 Nov): baru **562** yang sudah direlokasi
   (Siprus → Lithuania, Rumania, Bulgaria, Prancis); 1.283 adalah total
   yang **diharapkan tercapai akhir 2026** lewat penerbangan tambahan.
   Headline "EU MOVES 1,283" + strip angka "1,283 ASYLUM SEEKERS MOVED
   BY EU" (past tense) menyatakan sebagai sudah terjadi. Dek
   "RELOCATIONS FALL SHORT. TWO STATES OPT OUT." benar (Hungaria +
   Polandia opt-out). Perbaikan: "EU TO MOVE 1,283" / "1,283 PLANNED",
   atau pakai angka 562 sebagai yang sudah terjadi.
5. **Hero #3: "A LATE-MONDAY STRIKE TORE OPEN A FIVE-STOREY BLOCK" —
   waktunya tidak tepat.** Serangan drone memang dimulai Senin 18:00,
   tapi hantaman Zaporizhzhia yang merobek blok 5 lantai itu adalah
   **serangan fajar Selasa** ("dawn raid", Al Jazeera). Frasa
   "late-Monday" menempel pada peristiwa Selasa pagi. Selebihnya hero #3
   akurat penuh: 96 drone, 73 downed/jammed per 08:00, 2 tewas, 40 luka
   (beberapa sumber: 40+ / 44 — "40 HURT" masih dalam rentang laporan).
   Ganti "LATE-MONDAY" → "OVERNIGHT" atau "DAWN".

## Minor

6. **Panel gempa: "M5.3" tertutup sebagian segitiga salju.** Zoom 4×:
   segitiga putih puncak gunung menabrak huruf "3" dari "M5.3" (teks
   skala 2 di (x+8, y+4) bertabrakan dengan snowcap di (x+54..62,
   y+8..20)). Di 1× masih terbaca, tapi cacatnya nyata di zoom.
7. **Panel radar: "5 MIN ALERT" menabrak tepi daratan; daratan tidak
   menyerupai Korea.** Teks merah di kiri bawah ditulis menumpuk tepi
   bawah poligon daratan (tan); masih terbaca tapi kotor. Poligonnya
   sendiri pentagon abstrak, bukan bentuk Korea; "radar" (lingkaran +
   segitiga hitam) mengambang di laut, terputus dari daratan.
8. **#5 "FELT IN 4 NATIONS" — hitungannya 5 bila Nepal dihitung.**
   Guncangan terasa di Nepal, India, Bhutan, Bangladesh, dan China
   (5 negara). "4 NATIONS" hanya benar sebagai "4 negara selain Nepal".
   Perjelas ("FELT IN 4 NATIONS BESIDES NEPAL" — tidak muat; atau
   "FELT ACROSS THE REGION").
9. **#13 "HOSPITAL SAYS" — atribusi kurang tepat.** Angka 3 tewas, 5
   luka berasal dari petugas medis/pejabat kesehatan (Reuters: "local
   health officials", "medics said"); jenazah dibawa ke RS Nasser.
   Bukan RS-nya yang mengumumkan. Sepele; "MEDICS SAY" lebih tepat.
10. **#29 "VOWS TO SHUT MISSION" melebih-lebihkan.** Kim Yo-jong bilang
    kantor Swiss "kehilangan alasan keberadaan" dan ia akan
    **menyarankan** Kemenlu meninjau penarikan kantor dalam beberapa
    hari — bukan berjanji menutup. "THREATENS SWISS OFFICE" (judul)
    sudah tepat; deknya yang overstate.
11. **#30 "REACHES NASSAU" — statusnya perkiraan, bukan konfirmasi.**
    PM Office Cook Islands: Te Kukupa II "**expected to reach** Nassau
    on Tuesday morning". Kapal berangkat Senin 23 Nov; tibanya Selasa
    adalah jadwal, bukan laporan tiba. "DUE IN NASSAU" lebih jujur.
12. **Badge #13: REPORTED padahal 2+ outlet.** Reuters + Anadolu +
    Al Jazeera sama-sama melaporkan serangan Al-Mawasi 24 Nov; menurut
    legenda sendiri (CONFIRMED = dua outlet atau lebih) badge-nya
    seharusnya CONFIRMED. Under-badging itu konservatif dan aman — hanya
    inkonsisten dengan legenda. (Sebaliknya #9 REPORTED sudah tepat:
    eksklusif Euronews, satu outlet.)
13. **Footer/legenda skala-1 tetap tidak terbaca di ~300px** (sudah
    dicatat ronde-1/2; metadata saja, dampak rendah). Detail sekunder
    skala-1 juga jadi tekstur di thumbnail — sama seperti r1 lama dan
    sama seperti pemenang; bukan pembeda.

## Fakta: tabel verifikasi 34 cerita + timeline + angka

Skala: ✅ BENAR (Selasa 24 Nov, angka cocok) · ⚠️ BENAR ISI, CATATAN ·
❌ GAGAL TANGGAL (terjadi/pertama dilaporkan sebelum Selasa).

| # | Klaim | Verdict | Bukti singkat |
|---|---|---|---|
| 1 | Taiex +9%, Kospi +7,5%, Nikkei +4,5% | ✅ | Reuters 24 Nov: Taiex +9,1%, Kospi +7,5%, Nikkei +4,5% (penutupan Selasa; "TAIEX CLOSES UP 9%" benar) |
| 2 | IRGC: 3 tanker kena ranjau, Hormuz | ✅ | IRNA bawa pernyataan Selasa pagi; Tasnim: pernyataan Senin malam; klaim unverified (Iran International/JPost). Badge CLAIM tepat. "TWO SHIPS HAD US AIR ESCORT" ✓ ("under extensive US military air cover and escort") |
| 3 | 96 drone, 73 downed/jammed, Zaporizhzhia 2 tewas 40 luka | ✅ isi, ⚠️ frasa | AU Ukraina: 96 drone dari Senin 18:00, 73 dinetralisir per 08:00 Selasa; 2 tewas, 40 luka, blok 5 lantai. Tapi lihat Major 5 ("LATE-MONDAY" vs serangan fajar) |
| 4 | Jet Rusia, alert Ulleung, shelter 5 mnt | ✅ | Yonhap/JCS 24 Nov: alert 07:52 KST, dicabut ~5 mnt (stempel 07:52→07:55; JoongAng: "approximately five minutes"); jet masuk KADIZ, TIDAK langgar wilayah udara — dek "ENTER KOREA'S ZONE" tepat |
| 5 | Nepal M5.3, 01:32 UTC, Taplejung | ✅ | USGS/EMSC: M5.3, 24 Nov 01:32:42 UTC, Koshi/Taplejung; 0 korban; terasa di Nepal/India/Bhutan/Bangladesh/China. Lihat Minor 8 soal "4 NATIONS". (NEMRC Nepal sendiri: 5.6 — varian antar-lembaga, 5.3 USGS/EMSC sah) |
| 6 | Pakistan umumkan astronot pertama, Shenzhou-24 | ✅ | CMSA umumkan kru Selasa 24 Nov (konferensi pers Jiuquan); Zeeshan Ali = astronot Pakistan pertama + asing pertama di Tiangong; luncur Rabu 25 Nov 00:18 UTC. Badge OFFICIAL tepat |
| 7 | Australia denda tek s.d. 5% | ✅ | Reuters/AP 24 Nov: deal Labor-Greens Selasa; denda maks 5% pendapatan global (dari A$109 jt); hak gugat perorangan |
| 8 | Wong: Singapura bukan jalur chip AS | ✅ | Reuters 24 Nov: Wong (Canberra, Selasa) — "We do not want Singapore to be used and abused as a conduit…"; investigasi Megaspeed lanjut. Badge OFFICIAL tepat |
| 9 | EU pindah 1.283 pencari suaka | ⚠️ angka | Euronews eksklusif 24 Nov: 1.283 = total tahun pertama; baru 562 sudah pindah; 2 negara opt-out (Hungaria, Polandia) ✓. Lihat Major 4 |
| 10 | Sanofi beli Insmed $41BN, $175/saham | ✅ isi, ⚠️ premi | Sanofi 24 Nov: $41,0BN tunai, $175/saham ✓. "46% PREMIUM" = vs harga pra-rumor 18 Nov; vs Senin ~17%. Lihat Major 2 |
| 11 | Iowa: pengadilan izinkan ledakkan 5 ton lead azide | ✅ (abu-abu ringan) | 8th Circuit tolak permohonan darurat Senin; pertama dilaporkan Selasa 05:44 (KTBB 24 Nov); 68 barel ≈ 9.700 pon ≈ 5 ton ✓; detonasi dijadwalkan Rabu. Badge CONFIRMED ✓ |
| 12 | Pesawat DR Congo hilang, pemberontak klaim tembak | ❌ TANGGAL | Jatuh Min 22 Nov ~06:00; klaim FRN Min; pernyataan FARDC Sen; hanya identifikasi "Cessna 208" oleh FRN yang Selasa. Badge CLAIM tepat untuk klaimnya; tanggalnya yang gagal |
| 13 | Serangan Gaza Al-Mawasi, 3 tewas 5 luka | ✅ | Reuters 24 Nov: serangan fajar Selasa di pos polisi Al-Mawasi, Khan Younis; ≥3 tewas, 5 luka (medics). Lihat Minor 9 + 12 |
| 14 | SAWS: alert banjir Johannesburg | ✅ | SAWS Yellow Level 4 Selasa 24 Nov (Gauteng incl. Johannesburg; berlaku s.d. malam) |
| 15 | Commanders kalahkan Bengals 22-20 | ✅ | AP 24 Nov: Stevens FG 26 yard saat waktu habis, MNF Senin malam lokal = Selasa UTC ("MNF, TUE UTC" tepat) |
| 16 | Ariane 6 VA271, 36 satelit, 11:14 UTC | ✅ | Arianespace/Amazon: lepas landas Selasa 24 Nov 11:14 UTC, Kourou, 36 satelit Leo |
| 17 | Singapura naikkan proyeksi PDB ~6%, Q3 +6,1% | ✅ | MTI Selasa 24 Nov: Q3 +6,1% yoy; proyeksi 2026 "around 6%" (dari 4,5–5,5%) |
| 18 | Australia: AI jadi inti keamanan (Wong) | ✅ | Menlu Penny Wong pidato ke Senat Selasa 24 Nov ("AI reshapes power"); + pernyataan bersama AI Aus–Singapura hari yang sama |
| 19 | Davis Cup Final 8 dibuka, Bologna | ✅ | ITF/Tennis Canada: dibuka Selasa 24 Nov, Czechia vs Kanada 16:00 CET |
| 20 | Progress MS-36 lepas landas 10:17 UTC | ✅ | NASA/Roscosmos: Soyuz lepas landas Baikonur Selasa 24 Nov 10:17:46 UTC |
| 21 | Final Miss Universe, 116, San Juan 8PM ET | ✅ | Wikipedia/panitia: final Selasa 24 Nov, Coliseo San Juan, 116 kontestan, 20:00 ET |
| 22 | PBB minta aturan keamanan AI setahun | ❌ TANGGAL | Pidato Guterres di Bridgetown **Senin 23 Nov** ("said Monday"); kerangka "within the next year" + "independent oversight" isinya benar |
| 23 | Negara bagian gugat Musk soal Grok | ⚠️ ABU-ABU | Gugatan Virginia + Oregon diajukan **Senin 23 Nov** (Spicy Mode, CSAM); liputan besar Selasa pagi (NPR 24 Nov 04:52 EST). Perlu verifikasi tanggal laporan pertama |
| 24 | Denmark larang HP sekolah s.d. kelas 10 | ❌ TANGGAL | Diumumkan Kemendik Denmark **Senin 23 Nov**; berlaku tahun ajaran 2027-28, s.d. kelas 10 ✓ isinya |
| 25 | AS timbang tim demining Suriah 15 negara | ❌ TANGGAL | Eksklusif Reuters berdateline **Senin 23 Nov**; isi benar (15 sekutu incl. UK, Prancis, Jerman; mulai Mar 2027) |
| 26 | Kecelakaan bus UAE, 13 tewas | ✅ | RAK Police Selasa 24 Nov: tabrakan bus vs truk parkir, toll naik 11 → 13 (update Selasa) |
| 27 | Tokyo percepat dana ICC | ✅ | Reuters Selasa 24 Nov: Takaichi (pertemuan Selasa) bayar penuh iuran 2027 akhir tahun; Jepang ~15% anggaran ICC, donor terbesar |
| 28 | Beijing perpanjang jeda mineral s.d. 27 Jan 2027 | ✅ | MoC Selasa 24 Nov: jeda larangan ekspor gallium/germanium/antimon diperpanjang s.d. 27 Jan 2027 (SCMP/Reuters) |
| 29 | Pyongyang ancam kantor Swiss | ✅ | KCNA Selasa 24 Nov: Kim Yo-jong kecam sanksi Swiss atas kamp Songdowon, ancam tinjau penutupan kantor. Lihat Minor 10 ("VOWS TO SHUT") |
| 30 | Te Kukupa II ke Nassau | ✅ (catatan) | PM Office Cook Islands: kapal "expected to reach Nassau on Tuesday morning" + bawa makanan/bahan bakar/medis. Lihat Minor 11 ("REACHES" vs "expected") |
| 31 | Pakta Vanuatu pecah belah Canberra | ✅ | ABC/AAP Selasa 24 Nov: komite rekomendasikan ratifikasi Nakamal A$500 jt; Koalisi dissent soal klausul net-zero 2050; Wong di ABC Radio Selasa |
| 32 | Inggris hancurkan Australia T20 | ✅ | ESPNcricinfo Selasa 24 Nov: Donald 85 (32 bola), Inggris menang 8 wicket |
| 33 | Bom mobil Villavicencio, 23 luka | ✅ | AP Selasa 24 Nov: ledakan Senin 21:30 lokal = **02:30 UTC Selasa**; toll naik ke 23 (Selasa); kantor gubernur Meta. Penggunaan jam UTC di sini tepat |
| 34 | Alarm drone Sudan membesar | ✅ | Plan International **Selasa 24 Nov**: pernyataan soal serangan drone Khartoum (Min) + gedung PBB kena; 3.000+ keluarga mengungsi Blue Nile |

**Timeline UTC (strip):** 01:32 gempa Nepal ✅ · 06:00 Kyiv hitung 96
(08:00 lokal = 06:00 UTC ✅) · 10:17 Progress ✅ · 11:14 Ariane ✅ ·
14:53 supermoon ✅ (Beaver Moon, puncak 14:53 UTC, USNO) · 20:00 UCL
Night (penanda malam; laga UCL Selasa malam ✅).
**THE DAY IN NUMBERS:** +9% ✅ · 96 ✅ · 5.3 ✅ · 5% ✅ ·
1,283 ⚠️ (proyeksi, lihat Major 4) · $41BN ✅.

**Rekap tanggal:** 29 item ✅ murni Selasa · 3 item ⚠️ abu-abu tapi
dipertahankan di bawah standar "pertama dilaporkan Selasa" (#2 pernyataan
Senin malam yang pertama dibawa IRNA Selasa pagi; #3 serangan dimulai
Senin 18:00 tapi hitungan + laporan Selasa 08:00; #11 putusan Senin yang
pertama dilaporkan Selasa pagi) · **4 item ❌ gagal** (#12, #22, #24,
#25) · 1 item ⚠️ belum terverifikasi penuh (#23). Standar "KETAT" yang
diklaim build-log §8 TIDAK terpenuhi — dan §8 salah tanggal untuk #22,
#24, #25 (ditulis 24 Nov, nyatanya 23 Nov).

## (a) Region bar — rekonsiliasi PERSIS ✅

Dihitung dari `main.py` (dan di-assert di program: `counts == bar`,
total 34): EUROPE 6 (#3, #9, #10, #19, #20, #24) · MIDDLE EAST 4 (#2,
#13, #25, #26) · AFRICA 3 (#12, #14, #34) · EAST ASIA 5 (#1, #4, #27,
#28, #29) · SOUTH ASIA 2 (#5, #6) · SE ASIA 2 (#8, #17) · OCEANIA 5
(#7, #18, #30, #31, #32) · N. AMERICA 3 (#11, #15, #23) · LATAM 3
(#16, #21, #33) · WORLD 1 (#22) = **34** ✅. Strip masthead "34 STORIES
- 9 REGIONS" benar (9 region + WORLD). Satu-satunya yang salah di strip
itu adalah klaim "EVERY ONE DATED TUE 24 NOV 2026" (lihat Blocker 1).

## (b) Pin peta 1–13 — lokasi kasar BENAR ✅ (dengan 1 catatan)

Taipei (pin 1, laut timur China — pulau Taiwan tidak digambar sebagai
daratan, jadi pin jatuh di laut tepat di sisi timur pantai; arah benar,
kasar) · Hormuz pin 2 (Teluk ✅) · Zaporizhzhia pin 3 (Ukraina ✅) ·
Ulleung pin 4 (timur Korea ✅) · Nepal pin 5 (Himalaya ✅) · Jiuquan pin 6
(China barat laut ✅) · Canberra pin 7 (Australia tenggara ✅) ·
Singapura pin 8 ✅ · Brussels pin 9 + Paris pin 10 (titik berbeda,
label tidak bertumpuk — Paris di kiri Brussels, benar) · Iowa pin 11
(AS tengah ✅) · DR Congo pin 12 (Afrika tengah ✅) · Gaza pin 13
(Levant, Med timur ✅ — TIDAK di Afrika). Tidak ada pin yang salah
benua/wilayah. Kelemahan peta: Korea gumpalan tanpa bentuk, Jepang
selipis garis, Selandia Baru nyaris tak terlihat, tanpa label kota —
peta "kasar" sesuai klaim builder, tapi di bawah kerapian peta pemenang.

## (c) Keterbacaan ~300px

Masthead "TUESDAY 24 NOVEMBER 2026" + dek merah terbaca penuh; 3 headline
hero (skala 2) terbaca; angka besar strip (+9%, 96, 5.3, 5%, 1,283, $41BN)
terbaca; segmen region bar terbaca sebagai warna (labelnya tidak); headline
sekunder skala 2 sebagian terbaca; dek skala-1, daftar ALSO, strip timeline,
dan teks DATE CHECK menjadi tekstur; footer/legenda tidak terbaca. Polanya
SAMA seperti r1 lama dan seperti pemenang (teks kecil jadi tekstur di
thumbnail) — bukan pembeda negatif, tapi juga bukan keunggulan: yang
membaca di 300px hanya mendapat masthead + 3 hero + angka. Catatan:
di 300px, panel "5 TONS" segitiga kuning dan ilustrasi tanker/drone
masih terbaca sebagai gambar — ilustrasi bekerja di thumbnail, teks
tidak.

## (d) Badge status — sebagian besar TEPAT ✅

CONFIRMED #1, #4, #5, #7, #10, #11 (2+ outlet / hasil final) ✅ ·
OFFICIAL #3 (AU Ukraina), #6 (CMSA), #8 (PM Wong on the record) ✅ ·
CLAIM #2 (IRGC, unverified), #12 (klaim pemberontak) ✅ · REPORTED #9
(Euronews eksklusif, 1 outlet) ✅. Satu inkonsistensi: #13 REPORTED
padahal Reuters + Anadolu + Al Jazeera (Minor 12).

## (e) Teks terpotong / overlap / garbled / typo

Tidak ada teks terpotong, tidak ada garbled, tidak ada typo ejaan yang
terlihat (TSHISEKEDI tidak ada di r2; TAPLEJUNG, ZAPORIZHZHIA, ULLEUNG,
MINEMBWE, VILLAVICENCIO, ZEESHAN semua benar). Overlap yang terbukti:
Minor 6 (M5.3 vs snowcap) dan Minor 7 ("5 MIN ALERT" vs daratan).
Sisanya bersih di full-res + semua crop-zoom: tidak ada headline/dek yang
bersentuhan dengan panel tetangga; leading headline 16px sudah cukup
(perbaikan dari r2 awal yang 14px).

## (f) Ilustrasi vector vs pemenang — di mana masih kalah

Struktur sudah sama (13 cerita bergambar + peta + angka + timeline);
craft belum: (1) tipografi — font bitmap 5×7 kita = pixel-art; pemenang
pakai serif/display raksasa yang langsung terbaca "koran"; (2) detail
ilustrasi — hero pasar kita (3 balok + garis merah) bersih tapi datar;
tanker kita (3 kapal identik + segitiga api) vs tanker pemenang (asap
berlapis, detail kapal); kota malam kita (grid jendela + ledakan oranye)
adalah panel terkuat kita dan paling dekat dengan pemenang; (3) panel
sekunder kita sebagian besar ikon tunggal (chip "AI", pil, segitiga
kuning, pesawat siluet) — fungsional, bukan ilustrasi adegan; (4) peta
kasar (lihat (b)). Yang sudah setara: komposisi koran, hierarki
masthead → hero → sekunder → ALSO → peta → DATE CHECK, dan kejujuran
DATE CHECK di sisi eksklusi.

## Perbandingan ronde-1 → r2 (blocker lama)

| Poin goldfish-review-2 | Status r2 |
|---|---|
| Banner tanggal salah harfiah, ~16/34 item 22–23 Nov | ⚠️ **SEBAGIAN TERTUTUP.** Banner (a) sudah dibuang; DATE CHECK + strip header kini klaim standar ketat — tapi klaim itu masih salah untuk 4/34 item (#12, #22, #24, #25) + 1 abu-abu (#23). Bukan lagi 47%, tapi 12% — dan kelas cacatnya sama |
| #16 "BRING BACK" overstate; #19 "NATO WARNS" overstate | ✅ Tidak ada lagi di r2 (item diganti total) |
| Oseania 0 cerita | ✅ Kini 5 cerita (#7, #18, #30, #31, #32) |
| Tanpa ilustrasi/peta/timeline/angka/badge | ✅ Semua ada di r2 |
| Region tidak direkonsiliasi | ✅ Rekonsiliasi persis, di-assert program |
| Estimasi ronde-2: top 10–25, 50–65% | ❌ Terbukti meleset total (nyata: rank 4805, skor 458.194). Estimasi kali ini dikalibrasi konservatif di bawah |

## Estimasi rank/peluang (JUJUR, dikalibrasi ke skor ronde 1)

- **Rank: 50–150, paling mungkin ~75–120. Peluang top-50: ~30%.
  Peluang top-10: ~5%.**
- Kalibrasi: skor r1 458.194 (rank 4805/7302); cutoff rank 50 = 654.221
  (gap +196.027), rank 10 = 803.073, rank 1 = 863.545. r2 menutup gap
  STRUKTUR (yang membuat r1 kalah telak: tanpa ilustrasi/peta/badge/
  tanggal jujur), tapi TIDAK menutup gap POLISH (font bitmap vs serif,
  ilustrasi sederhana vs detail, peta kasar) — dan polish itulah yang
  membedakan rank 1–50 dari rank 50–150 di lapangan 7.302 entry.
  Struktur saja, tanpa polish, secara realistis mengangkat entry dari
  dasar klasemen ke sekitaran garis top-50, bukan ke top-10.
- **Aturan CHASE-TOP-10:** target TOP 10 **TIDAK** tercapai pada estimasi
  paling mungkin; lantai rank 25 **TIDAK** tercapai; peluang top-50
  minimal 30% terpenuhi **tipis di batas** (~30%). Setelah putaran
  perbaikan di bawah (tutup blocker tanggal + premi Sanofi), estimasi
  naik sedikit: rank ~50–120, peluang top-50 ~35% — tetap di bawah
  target top-10, karena pembatasnya kini craft, bukan fakta.
- Estimasi Goldfish ronde-2 ("top 10–25, 50–65%") terbukti salah total
  dan TIDAK dipakai sebagai acuan di sini; angka di atas dihitung dari
  skor nyata ronde 1 + perbandingan struktur/craft, bukan dari optimisme
  dev-phase.

## Satu putaran perbaikan paling berdampak (maks. 3 perubahan)

1. **Tutup blocker tanggal — ganti #12, #22, #24, #25 (dan verifikasi
   #23) dengan cerita Selasa 24 Nov murni.** Syarat tiap pengganti:
   terjadi ATAU pertama dilaporkan Selasa 24 Nov (UTC atau lokal) —
   diverifikasi via pencarian SEBELUM render, dan tanggalnya ditulis
   benar di build-log (tiga kesalahan tanggal §8 — #22, #24, #25 ditulis
   "24 Nov" padahal 23 Nov — tidak boleh terulang). Alternatif murah
   untuk #12 saja: reframe ke sudut Selasa-nya (FRN Selasa menyebut
   tipe pesawat Cessna 208) — tapi #22/#24/#25 tidak punya sudut Selasa,
   wajib diganti. #22/#24/#25 adalah item ALSO (ganti teks saja, tanpa
   ubah layout); #12 panel sekunder (ganti headline/dek/sumber/kicker;
   ilustrasi pesawat bisa dipakai ulang untuk cerita penerbangan Selasa).
   Klaim "EVERY ONE DATED" / "EVERY STORY ABOVE" di header + DATE CHECK
   baru benar setelah ini. JANGAN ubah klaimnya menjadi longgar — justru
   klaim ketat itulah yang dinilai pemenang.
2. **Sanofi: kualifikasi premi.** "A 46% PREMIUM" → "46% OVER
   PRE-RUMOUR PRICE" atau ganti ke "17% OVER MONDAY CLOSE". Satu frasa,
   satu panel.
3. **Perbaiki 2 tabrakan gambar:** geser snowcap panel gempa agar tidak
   menabrak "M5.3"; pindah teks "5 MIN ALERT" panel radar ke area laut
   kosong (atau perkecil poligon daratan). Dua edit koordinat, tanpa
   ubah layout.
4. JANGAN: tambah cerita, ubah layout/grid, ganti item lain yang sudah
   terverifikasi, atau sentuh tipografi/peta (di luar scope putaran ini
   — polish font/peta butuh rebuild, bukan perbaikan).

**Setelah 1–3 selesai + render ulang 2× terverifikasi (sha baru):
LAYAK SUBMIT.** Tidak perlu Goldfish ronde penuh lagi; cukup konfirmasi
render (sha + visual check cepat + re-verifikasi tanggal 4 pengganti)
sebelum submit.
