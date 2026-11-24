#!/usr/bin/env python3
"""make.fun news-image-20261124, revisi r2: THE WORLD IN ONE DAY.

Edisi koran bergambar satu halaman, 1024x1024, 34 cerita Selasa 24 November
2026. Masthead raksasa, region bar yang direkonsiliasi, strip timeline UTC,
strip THE DAY IN NUMBERS, 3 hero berilustrasi vector, 10 panel sekunder
berilustrasi, daftar ALSO #14-34, peta dunia berpin bernomor, dan footer
DATE CHECK yang jujur (lihat build-log.md bagian 8 untuk sumber tiap cerita
dan daftar cerita yang sengaja dikecualikan).

Semua gambar digambar kode (rect/circle/line/polygon), tanpa foto, tanpa
file eksternal, tanpa network. Hanya stdlib Python. Deterministik: dua run
menghasilkan byte yang identik.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import math
import os
import struct
import zlib

SHEET_W = 1024
SHEET_H = 1024

# ------------------------------------------------------------------ warna
PAPER = (247, 243, 232)     # krem koran
PAPER_DIM = (238, 232, 214)
INK = (17, 24, 39)          # nyaris hitam
NAVY = (11, 42, 74)         # pita header / timeline
NAVY_MID = (31, 56, 100)
GOLD = (201, 162, 39)
GOLD_SOFT = (255, 214, 90)
RED = (178, 34, 34)         # merah koran (dek + badge CLAIM)
WHITE = (255, 255, 255)
GREY_TXT = (74, 74, 74)
GREY_LINE = (203, 197, 184)
SKY = (186, 214, 228)
SKY_DEEP = (52, 96, 140)
SEA = (34, 68, 110)
SEA_DARK = (22, 48, 84)
LAND_TAN = (216, 201, 163)
LAND_EDGE = (168, 148, 106)
GREEN = (30, 122, 52)
GREEN_SOFT = (46, 160, 67)
TEAL = (14, 124, 123)
ORANGE = (211, 84, 0)
AMBER = (214, 148, 0)
PURPLE = (108, 52, 131)
MAROON = (128, 32, 48)
SLATE = (93, 109, 126)
FLAME = (232, 116, 24)
FLAME_Y = (244, 196, 48)
NIGHT = (13, 27, 52)

# badge status -> warna latar
BADGE_FILL = {
    "CONFIRMED": (30, 122, 52),
    "OFFICIAL": (31, 56, 100),
    "REPORTED": (196, 120, 0),
    "CLAIM": (178, 34, 34),
}

# region -> warna segmen bar
REGION_FILL = {
    "EUROPE": (31, 56, 100),
    "MIDDLE EAST": (178, 34, 34),
    "AFRICA": (108, 52, 131),
    "EAST ASIA": (128, 32, 48),
    "SOUTH ASIA": (146, 106, 20),
    "SE ASIA": (14, 124, 123),
    "OCEANIA": (30, 122, 52),
    "N. AMERICA": (93, 109, 126),
    "LATAM": (211, 84, 0),
    "WORLD": (74, 74, 74),
}

# --------------------------------------------- font bitmap 5x7 (format 0/1)
# Tiap glyph: 7 baris dipisah "/", "1" = piksel menyala. Huruf besar, angka,
# dan tanda baca yang dipakai edisi ini.
GLYPH_ROWS = {
    "A": "01110/10001/10001/11111/10001/10001/10001",
    "B": "11110/10001/10001/11110/10001/10001/11110",
    "C": "01110/10001/10000/10000/10000/10001/01110",
    "D": "11110/10001/10001/10001/10001/10001/11110",
    "E": "11111/10000/10000/11110/10000/10000/11111",
    "F": "11111/10000/10000/11110/10000/10000/10000",
    "G": "01110/10001/10000/10111/10001/10001/01111",
    "H": "10001/10001/10001/11111/10001/10001/10001",
    "I": "01110/00100/00100/00100/00100/00100/01110",
    "J": "00111/00010/00010/00010/00010/10010/01100",
    "K": "10001/10010/10100/11000/10100/10010/10001",
    "L": "10000/10000/10000/10000/10000/10000/11111",
    "M": "10001/11011/10101/10101/10001/10001/10001",
    "N": "10001/11001/10101/10011/10001/10001/10001",
    "O": "01110/10001/10001/10001/10001/10001/01110",
    "P": "11110/10001/10001/11110/10000/10000/10000",
    "Q": "01110/10001/10001/10001/10101/10010/01101",
    "R": "11110/10001/10001/11110/10100/10010/10001",
    "S": "01111/10000/10000/01110/00001/00001/11110",
    "T": "11111/00100/00100/00100/00100/00100/00100",
    "U": "10001/10001/10001/10001/10001/10001/01110",
    "V": "10001/10001/10001/10001/10001/01010/00100",
    "W": "10001/10001/10001/10101/10101/11011/10001",
    "X": "10001/10001/01010/00100/01010/10001/10001",
    "Y": "10001/10001/01010/00100/00100/00100/00100",
    "Z": "11111/00001/00010/00100/01000/10000/11111",
    "0": "01110/10001/10011/10101/11001/10001/01110",
    "1": "00100/01100/00100/00100/00100/00100/01110",
    "2": "01110/10001/00001/00110/01000/10000/11111",
    "3": "11111/00010/00100/00010/00001/10001/01110",
    "4": "00010/00110/01010/10010/11111/00010/00010",
    "5": "11111/10000/11110/00001/00001/10001/01110",
    "6": "00110/01000/10000/11110/10001/10001/01110",
    "7": "11111/00001/00010/00100/01000/01000/01000",
    "8": "01110/10001/10001/01110/10001/10001/01110",
    "9": "01110/10001/10001/01111/00001/00010/01100",
    " ": "00000/00000/00000/00000/00000/00000/00000",
    ".": "00000/00000/00000/00000/00000/01100/01100",
    ",": "00000/00000/00000/00000/01100/00100/01000",
    ":": "00000/01100/01100/00000/01100/01100/00000",
    ";": "00000/01100/01100/00000/01100/00100/01000",
    "'": "00100/00100/01000/00000/00000/00000/00000",
    "-": "00000/00000/00000/01110/00000/00000/00000",
    "(": "00010/00100/01000/01000/01000/00100/00010",
    ")": "01000/00100/00010/00010/00010/00100/01000",
    "/": "00001/00010/00010/00100/01000/01000/10000",
    "&": "01100/10010/10100/01000/10101/10010/01101",
    "%": "11001/11010/00010/00100/01000/10110/10011",
    "+": "00000/00100/00100/11111/00100/00100/00000",
    "=": "00000/00000/11111/00000/11111/00000/00000",
    "?": "01110/10001/00001/00110/00100/00000/00100",
    "!": "00100/00100/00100/00100/00100/00000/00100",
    '"': "01010/01010/00000/00000/00000/00000/00000",
    "$": "00100/01111/10100/01110/00101/11110/00100",
    "#": "01010/01010/11111/01010/11111/01010/01010",
    "*": "00000/00100/10101/01110/10101/00100/00000",
    "_": "00000/00000/00000/00000/00000/00000/11111",
    "<": "00001/00010/00100/01000/00100/00010/00001",
    ">": "10000/01000/00100/00010/00100/01000/10000",
    "[": "01110/01000/01000/01000/01000/01000/01110",
    "]": "01110/00010/00010/00010/00010/00010/01110",
    "@": "01110/10001/10111/10101/10110/10000/01110",
}


def glyph_rows(ch):
    """Kembalikan 7 string baris '0'/'1' untuk satu karakter."""
    return GLYPH_ROWS.get(ch, GLYPH_ROWS[" "]).split("/")


def measure(text, scale):
    """Lebar piksel teks pada skala tertentu (termasuk spasi antar huruf)."""
    if not text:
        return 0
    return len(text) * 6 * scale - scale


# ------------------------------------------------------------------- kanvas
def make_sheet():
    """Kanvas 1024x1024 terisi warna kertas koran."""
    sheet = bytearray(SHEET_W * SHEET_H * 3)
    for pos in range(0, len(sheet), 3):
        sheet[pos] = PAPER[0]
        sheet[pos + 1] = PAPER[1]
        sheet[pos + 2] = PAPER[2]
    return sheet


def px(sheet, x, y, color):
    if 0 <= x < SHEET_W and 0 <= y < SHEET_H:
        idx = (y * SHEET_W + x) * 3
        sheet[idx] = color[0]
        sheet[idx + 1] = color[1]
        sheet[idx + 2] = color[2]


def box(sheet, x, y, w, h, color):
    for yy in range(y, y + h):
        base = (yy * SHEET_W + x) * 3
        for xx in range(w):
            j = base + xx * 3
            sheet[j] = color[0]
            sheet[j + 1] = color[1]
            sheet[j + 2] = color[2]


def rule_h(sheet, x, y, w, color, thick=1):
    for t in range(thick):
        for xx in range(x, x + w):
            px(sheet, xx, y + t, color)


def seg(sheet, x0, y0, x1, y1, color):
    """Garis Bresenham 1px."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        px(sheet, x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def disc(sheet, cx, cy, r, color):
    """Lingkaran terisi."""
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                px(sheet, xx, yy, color)


def ring(sheet, cx, cy, r, color):
    """Lingkaran garis 1px (midpoint)."""
    x, y, d = 0, r, 1 - r
    while x <= y:
        for qx, qy in ((cx + x, cy + y), (cx - x, cy + y),
                       (cx + x, cy - y), (cx - x, cy - y),
                       (cx + y, cy + x), (cx - y, cy + x),
                       (cx + y, cy - x), (cx - y, cy - x)):
            px(sheet, qx, qy, color)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1


def tri(sheet, pts, color):
    """Segitiga terisi dari 3 titik (scanline)."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    for yy in range(min(ys), max(ys) + 1):
        spans = []
        for i in range(3):
            ax, ay = pts[i]
            bx, by = pts[(i + 1) % 3]
            if ay == by:
                continue
            if min(ay, by) <= yy < max(ay, by):
                xx = ax + (yy - ay) * (bx - ax) / (by - ay)
                spans.append(xx)
        if len(spans) >= 2:
            for xx in range(int(min(spans)), int(max(spans)) + 1):
                px(sheet, xx, yy, color)


def poly_fill(sheet, pts, color):
    """Poligon terisi (scanline, aturan genap-ganjil)."""
    if len(pts) < 3:
        return
    ymin = min(p[1] for p in pts)
    ymax = max(p[1] for p in pts)
    n = len(pts)
    for yy in range(ymin, ymax + 1):
        xs = []
        for i in range(n):
            ax, ay = pts[i]
            bx, by = pts[(i + 1) % n]
            if ay == by:
                continue
            if min(ay, by) <= yy < max(ay, by):
                xs.append(ax + (yy - ay) * (bx - ax) / (by - ay))
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            for xx in range(int(xs[k]), int(xs[k + 1]) + 1):
                px(sheet, xx, yy, color)


def poly_edge(sheet, pts, color):
    n = len(pts)
    for i in range(n):
        ax, ay = pts[i]
        bx, by = pts[(i + 1) % n]
        seg(sheet, ax, ay, bx, by, color)


# --------------------------------------------------------------------- teks
def put_text(sheet, x, y, text, scale, color):
    """Gambar teks huruf besar ASCII dengan font 5x7 pada skala bulat."""
    cx = x
    for ch in text:
        rows = glyph_rows(ch)
        for r in range(7):
            row = rows[r]
            for c in range(5):
                if row[c] == "1":
                    for dy in range(scale):
                        for dx in range(scale):
                            px(sheet, cx + c * scale + dx,
                               y + r * scale + dy, color)
        cx += 6 * scale
    return cx


def put_text_c(sheet, cx, y, text, scale, color):
    put_text(sheet, cx - measure(text, scale) // 2, y, text, scale, color)


def wrap_words(text, limit):
    """Bungkus kata per kata menjadi baris <= limit karakter."""
    out = []
    for word in text.split(" "):
        if not out:
            out.append(word)
            continue
        if len(out[-1]) + 1 + len(word) <= limit:
            out[-1] += " " + word
        else:
            out.append(word)
    return out


# ---------------------------------------------------------------------- PNG
def encode_png(sheet):
    raw = bytearray()
    stride = SHEET_W * 3
    for y in range(SHEET_H):
        raw.append(0)
        raw += sheet[y * stride:(y + 1) * stride]
    blob = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        head = struct.pack(">I", len(data)) + tag + data
        return head + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", SHEET_W, SHEET_H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", blob) + chunk(b"IEND", b""))

# ===================================================================== DATA
# Standar tanggal: tiap cerita TERJADI atau PERTAMA DILAPORKAN pada Selasa
# 24 Nov 2026 (UTC atau tanggal lokal). Sumber + tanggal tiap cerita ada di
# build-log.md bagian 8. Badge: CONFIRMED = 2+ outlet / hasil final,
# OFFICIAL = tercatat dari otoritas, REPORTED = satu outlet bernama,
# CLAIM = klaim satu pihak, belum terverifikasi.
#
# (region, beat, kicker, badge, headline, dek, sumber)
HEROES = [
    ("EAST ASIA", "MARKETS", "TAIPEI - SEOUL - TOKYO", "CONFIRMED",
     "ASIA MARKETS ROAR BACK AS AI TRADE REVIVES",
     "TAIWAN'S TAIEX CLOSES UP 9% AFTER LAST WEEK'S AI ROUT. "
     "SEOUL'S KOSPI GAINS 7.5%. TOKYO'S NIKKEI ADDS 4.5%.",
     "AP - CNA - NIKKEI ASIA - ABC"),
    ("MIDDLE EAST", "SHIPPING", "STRAIT OF HORMUZ", "CLAIM",
     "IRAN SAYS MINES SET THREE TANKERS ABLAZE",
     "THE IRGC NAVY'S LATE-MONDAY STATEMENT WAS STILL UNVERIFIED "
     "ON TUESDAY. TWO SHIPS HAD US AIR ESCORT, IT SAYS.",
     "AL JAZEERA - ANADOLU - IRAN INTERNATIONAL"),
    ("EUROPE", "WAR", "ZAPORIZHZHIA, UKRAINE", "OFFICIAL",
     "RUSSIA FIRES 96 DRONES; ZAPORIZHZHIA FLATS HIT",
     "UKRAINE'S AIR FORCE SAYS 73 WERE DOWNED OR JAMMED BY 08:00. "
     "A DAWN STRIKE TORE OPEN A FIVE-STOREY BLOCK. "
     "TWO DEAD, 40 HURT.",
     "UKRAINIAN AIR FORCE - UKRINFORM - KYIV INDEPENDENT"),
]

# (region, beat, kicker, badge, headline, dek, sumber) -- panel #4-13
SECONDARY = [
    ("EAST ASIA", "DEFENCE", "ULLEUNG, S. KOREA", "CONFIRMED",
     "KOREAN AIR-RAID ALERT",
     "RUSSIAN JETS ENTER KOREA'S ZONE. ISLANDERS SHELTER 5 MIN.",
     "YONHAP - JCS"),
    ("SOUTH ASIA", "DISASTER", "TAPLEJUNG, NEPAL", "CONFIRMED",
     "NEPAL M5.3 QUAKE",
     "01:32 UTC TREMOR HITS KOSHI. FELT ACROSS REGION. NO DEATHS.",
     "USGS - EMSC - KATHMANDU POST"),
    ("SOUTH ASIA", "SPACE", "JIUQUAN, CHINA", "OFFICIAL",
     "PAKISTAN NAMES FIRST ASTRONAUT",
     "ZEESHAN ALI JOINS SHENZHOU-24 CREW. FIRST FOREIGN ASTRONAUT.",
     "XINHUA - CMSA - DAWN"),
    ("OCEANIA", "TECHNOLOGY", "CANBERRA", "CONFIRMED",
     "AUSTRALIA: TECH FINES UP TO 5%",
     "LABOR-GREENS DEAL SETS DIGITAL DUTY OF CARE. FINES UP TO 5%.",
     "ABC - REUTERS"),
    ("SE ASIA", "TRADE", "SINGAPORE", "OFFICIAL",
     "NO BACKDOOR FOR US CHIPS",
     "WONG VOWS TO UPHOLD EXPORT RULES AFTER US BLACKLIST.",
     "FINANCIAL TIMES"),
    ("EUROPE", "MIGRATION", "BRUSSELS", "REPORTED",
     "EU TO RELOCATE 1,283",
     "RELOCATIONS FALL SHORT. TWO STATES OPT OUT.",
     "EURONEWS"),
    ("EUROPE", "PHARMA", "PARIS - NEW JERSEY", "CONFIRMED",
     "SANOFI'S $41BN INSMED DEAL",
     "$175 A SHARE. 46% OVER PRE-RUMOUR PRICE.",
     "SANOFI - CNBC - REUTERS"),
    ("N. AMERICA", "COURTS", "IOWA, USA", "CONFIRMED",
     "IOWA BLAST GETS COURT ALL-CLEAR",
     "ARMY MAY DETONATE 5 TONS OF LEAD AZIDE.",
     "REUTERS - CNN"),
    ("AFRICA", "AVIATION", "SOUTH KIVU, DR CONGO", "CLAIM",
     "DR CONGO HUNTS MISSING PLANE",
     "SEARCH GOES ON FOR CESSNA 208. CLAIM UNVERIFIED.",
     "BBC - REUTERS"),
    ("MIDDLE EAST", "WAR", "KHAN YOUNIS, GAZA", "CONFIRMED",
     "GAZA STRIKE KILLS 3",
     "AL-MAWASI STRIKE AT DAWN. 3 DEAD, 5 HURT, MEDICS SAY.",
     "ANADOLU - TIMES OF ISRAEL"),
]

# (nomor, region, judul baris 1, detail baris 2, sumber singkat) -- #14-34
ALSO = [
    (14, "AFRICA", "JOHANNESBURG FLOOD ALERT",
     "SAWS WARNS OF FLASH FLOODS TUESDAY EVENING.", "SAWS"),
    (15, "N. AMERICA", "COMMANDERS STUN BENGALS 22-20",
     "STEVENS 26-YARD FG AS TIME EXPIRES. MNF, TUE UTC.", "NFL"),
    (16, "LATAM", "ARIANE 6 LIFTS 36 SATELLITES",
     "VA271 LAUNCHES FROM KOUROU AT 11:14 UTC.", "ARIANESPACE"),
    (17, "SE ASIA", "SINGAPORE LIFTS GDP VIEW TO 6%",
     "Q3 GREW 6.1% ON AI DEMAND, SAYS MTI.", "REUTERS"),
    (18, "OCEANIA", "AUSTRALIA PUTS AI AT SECURITY CORE",
     "WONG TELLS PARLIAMENT AI RESHAPES POWER.", "REUTERS"),
    (19, "EUROPE", "DAVIS CUP FINAL 8 UNDER WAY",
     "SEASON FINALS OPEN IN BOLOGNA.", "ITF"),
    (20, "EUROPE", "PROGRESS MS-36 LIFTS OFF FOR ISS",
     "SOYUZ BLASTS OFF BAIKONUR AT 10:17 UTC.", "NASA - ROSCOSMOS"),
    (21, "LATAM", "MISS UNIVERSE FINAL TONIGHT",
     "116 CHASE THE CROWN IN SAN JUAN, 8PM ET.", "GULF NEWS"),
    (22, "WORLD", "UN CHIEF WARNS ON AI WEAPONS",
     "GUTERRES TELLS SECURITY COUNCIL: NO KILLER ROBOTS.", "UN NEWS"),
    (23, "N. AMERICA", "US CONSUMER CONFIDENCE JUMPS",
     "INDEX HITS 103.3, HIGHEST SINCE JAN 2025.", "CONFERENCE BOARD"),
    (24, "EUROPE", "COSTA CALLS EU BUDGET SUMMIT",
     "LEADERS MEET NOV 26-27 ON BUDGET, UKRAINE.", "EUROPEAN COUNCIL"),
    (25, "MIDDLE EAST", "BRITAIN SANCTIONS HOUTHIS",
     "LONDON BLACKLISTS GROUP, FOUR OFFICIALS.", "REUTERS"),
    (26, "MIDDLE EAST", "UAE BUS CRASH KILLS 13",
     "BUS HITS PARKED TRUCK IN RAS AL KHAIMAH.", "REUTERS"),
    (27, "EAST ASIA", "TOKYO SPEEDS ICC FUNDING",
     "TAKAICHI PAYS 2027 SHARE EARLY AS US SANCTIONS LOOM.", "REUTERS"),
    (28, "EAST ASIA", "BEIJING EXTENDS MINERAL CURB PAUSE",
     "GALLIUM CURBS ON HOLD TO JAN 27, 2027.", "SCMP"),
    (29, "EAST ASIA", "PYONGYANG THREATENS SWISS OFFICE",
     "KIM YO-JONG URGES REVIEW OF SWISS OFFICE.", "YONHAP"),
    (30, "OCEANIA", "CYCLONE RELIEF SHIP DUE IN NASSAU",
     "TE KUKUPA II BRINGS FOOD, FUEL, MEDICS.", "RNZ"),
    (31, "OCEANIA", "VANUATU PACT SPLITS CANBERRA",
     "COALITION BALKS AT NET-ZERO CLAUSE IN A$500M DEAL.", "ABC"),
    (32, "OCEANIA", "ENGLAND THRASH AUSTRALIA IN T20",
     "DONALD 85 OFF 32 BALLS. ENGLAND WIN BY 8 WKTS.", "ESPNCRICINFO"),
    (33, "LATAM", "VILLAVICENCIO CAR BOMB HURTS 23",
     "BLAST AT 02:30 UTC WRECKS GOVERNOR'S OFFICE.", "AP"),
    (34, "AFRICA", "SUDAN DRONE ALARM GROWS",
     "PLAN WARNS AFTER DRONES HIT HOMES AND UN HOUSE.", "PLAN INTL"),
]

# (label bar, hitungan) -- urutan tampil di region bar; jumlah = 34
REGION_BAR = [
    ("EUROPE 6", 6),
    ("MIDDLE EAST 4", 4),
    ("AFRICA 3", 3),
    ("EAST ASIA 5", 5),
    ("SOUTH ASIA 2", 2),
    ("SE ASIA 2", 2),
    ("OCEANIA 5", 5),
    ("N. AMERICA 3", 3),
    ("LATAM 3", 3),
    ("WORLD 1", 1),
]

# (jam UTC, peristiwa) -- strip timeline
TIMELINE = [
    ("01:32", "NEPAL QUAKE"),
    ("06:00", "KYIV COUNTS 96"),
    ("10:17", "PROGRESS LIFTS OFF"),
    ("11:14", "ARIANE 6 LIFTS OFF"),
    ("14:53", "SUPERMOON"),
    ("20:00", "UCL NIGHT"),
]

# (angka besar, label) -- strip THE DAY IN NUMBERS
NUMBERS = [
    ("+9%", "TAIEX AT THE CLOSE"),
    ("96", "DRONES AT UKRAINE OVERNIGHT"),
    ("5.3", "MAGNITUDE, NEPAL QUAKE"),
    ("5%", "MAX TECH FINE IN AUSTRALIA"),
    ("1,283", "ASYLUM SEEKERS PLANNED BY EU"),
    ("$41BN", "SANOFI BUYS INSMED"),
]

# Cerita besar yang SENGAJA DIKECUALIKAN (pertama dilaporkan sebelum Selasa)
EXCLUDED = [
    "NVIDIA HUANG REINSTATEMENT (MON 23 NOV)",
    "COP31 ENDS WITH NO DEAL (SUN 22 NOV)",
    "RUSSIAN WARSHIP HIT OFF BENGHAZI (SUN 22 NOV)",
    "EU 22ND SANCTIONS PROPOSAL (MON 23 NOV)",
    "BELGIUM ATC STRIKE (MON 23 NOV)",
    "UK 2035 WOMEN'S CUP (MON 23 NOV)",
    "DEMOCRATS 258 HOUSE SEATS (SUN 22 NOV)",
    "GOMEZ QUITS (MON 23 NOV)",
]

# ------------------------------------------------------------- peta dunia
# Poligon daratan kasar dalam (lon, lat). Digambar tan di atas laut pucat.
LAND = [
    # Amerika Utara
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-95, 19), (-100, 16), (-105, 20),
     (-110, 23), (-115, 28), (-120, 34), (-125, 40), (-125, 49),
     (-130, 55), (-140, 60), (-155, 58), (-165, 60)],
    # Amerika Selatan
    [(-80, 10), (-75, 7), (-70, 11), (-60, 9), (-52, 5), (-50, 0),
     (-45, -5), (-38, -8), (-35, -10), (-40, -20), (-48, -28), (-55, -35),
     (-65, -41), (-70, -50), (-73, -53), (-70, -40), (-72, -30),
     (-70, -18), (-75, -15), (-80, -5)],
    # Afrika
    [(-17, 15), (-15, 27), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (30, 31), (32, 31), (35, 28), (37, 22),
     (40, 15), (43, 11), (48, 11), (51, 10), (48, 5), (42, 0),
     (40, -5), (40, -12), (35, -18), (32, -25), (28, -32), (20, -35),
     (17, -32), (15, -27), (13, -18), (12, -10), (9, 4), (4, 6),
     (-8, 5), (-13, 8)],
    # Eurasia (ujung Semenanjung Malaya ditarik ke Singapura)
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (5, 60), (5, 62), (12, 65), (18, 69), (25, 71), (30, 70),
     (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 70), (170, 67), (178, 65), (178, 62), (170, 60), (162, 56),
     (158, 52), (150, 59), (142, 55), (140, 50), (135, 43), (130, 42),
     (127, 40), (122, 38), (120, 32), (115, 23), (110, 20), (108, 18),
     (105, 10), (103, 1), (100, 8), (97, 10), (94, 17), (91, 22),
     (88, 22), (85, 19), (80, 15), (77, 8), (75, 10), (72, 20),
     (68, 23), (66, 25), (62, 25), (58, 26), (55, 26), (52, 28),
     (50, 29), (48, 30), (44, 29), (40, 31), (36, 36), (30, 36),
     (27, 37), (23, 36), (19, 40), (15, 44), (12, 44), (8, 44),
     (3, 43), (-2, 37), (-9, 37)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
     (130, -32), (135, -35), (138, -35), (140, -38), (145, -38),
     (150, -37), (153, -32), (153, -27), (150, -23), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20)],
    # Britania Raya
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 57), (1, 52), (-1, 51)],
    # Jepang
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (142, 42), (144, 44), (141, 45), (139, 42), (136, 37), (133, 35),
     (130, 33)],
    # Selandia Baru
    [(167, -45), (170, -42), (173, -40), (176, -38), (178, -38),
     (175, -41), (172, -43), (168, -46)],
    # Kalimantan
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -3),
     (110, -1)],
    # Sumatra
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -5),
     (100, 0)],
    # Nugini
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -9),
     (143, -8), (138, -8), (134, -4)],
    # Madagaskar
    [(44, -16), (47, -15), (50, -16), (49, -20), (46, -24), (44, -22),
     (43, -18)],
]

# (nomor cerita, lon, lat, dx label, dy label) -- pin 1-13 di peta
PINS = [
    (1, 121.0, 25.0, -4, 7),
    (2, 56.5, 26.5, -4, 7),
    (3, 35.2, 47.8, -4, 7),
    (4, 130.9, 37.5, -4, 7),
    (5, 87.9, 27.5, -4, 7),
    (6, 98.5, 39.8, -4, 7),
    (7, 149.1, -35.3, -4, 7),
    (8, 103.8, 1.35, -4, 7),
    (9, 4.35, 50.85, 6, -3),
    (10, 2.35, 48.85, -16, -3),
    (11, -93.6, 41.9, -4, 7),
    (12, 29.0, -3.0, -4, 7),
    (13, 34.45, 31.5, -4, 7),
]

# ============================================================ ILUSTRASI
# Semua scene digambar dari bentuk geometris (rect/circle/line/polygon).
# Koordinat relatif terhadap kotak (x, y, w, h) tiap panel.


def scene_markets(s, x, y, w, h):
    box(s, x, y, w, h, (222, 234, 240))
    for gy in (y + 18, y + 42, y + 66):
        for gx in range(x + 8, x + w - 8, 6):
            px(s, gx, gy, (176, 194, 204))
    base = y + h - 24
    seg(s, x + 16, base - 6, x + w - 16, y + 12, RED)
    tri(s, [(x + w - 16, y + 12), (x + w - 30, y + 12), (x + w - 16, y + 24)],
        RED)
    bars = [("TAIPEI", "+9%", 0.92, GREEN),
            ("SEOUL", "+7.5%", 0.76, GREEN_SOFT),
            ("TOKYO", "+4.5%", 0.46, (110, 170, 110))]
    bw = 54
    for i, (name, val, frac, col) in enumerate(bars):
        cx = int(x + w * (0.20 + 0.30 * i))
        bh = int(58 * frac)
        box(s, cx - bw // 2, base - bh, bw, bh, col)
        put_text_c(s, cx, base - bh - 12, val, 1, INK)
        put_text_c(s, cx, base + 5, name, 1, INK)


def scene_hormuz(s, x, y, w, h):
    box(s, x, y, w, int(h * 0.42), (246, 196, 122))
    box(s, x, y + int(h * 0.42), w, h - int(h * 0.42), SEA)
    box(s, x, y + int(h * 0.42), w, 3, (250, 220, 160))
    disc(s, int(x + w * 0.84), y + 16, 11, GOLD_SOFT)
    for gy in range(y + int(h * 0.55), y + h - 6, 12):
        for gx in range(x + 6, x + w - 6, 26):
            seg(s, gx, gy, gx + 12, gy, (120, 170, 205))
    for i, fx in enumerate((0.10, 0.42, 0.70)):
        hx = int(x + w * fx)
        hy = y + int(h * 0.60) + (i % 2) * 8
        box(s, hx, hy, 66, 13, INK)
        box(s, hx + 40, hy - 9, 16, 9, WHITE)
        box(s, hx + 12, hy - 8, 8, 8, RED)
        tri(s, [(hx + 26, hy - 8), (hx + 34, hy - 26), (hx + 42, hy - 8)],
            FLAME)
        tri(s, [(hx + 30, hy - 8), (hx + 34, hy - 20), (hx + 38, hy - 8)],
            FLAME_Y)
        disc(s, hx + 34, hy - 30, 5, (120, 120, 120))
        disc(s, hx + 42, hy - 36, 4, (150, 150, 150))


def scene_drones(s, x, y, w, h):
    box(s, x, y, w, h, NIGHT)
    for fx, fy in ((0.08, 0.12), (0.28, 0.07), (0.48, 0.16), (0.68, 0.08),
                   (0.88, 0.14), (0.18, 0.26), (0.82, 0.28)):
        px(s, int(x + w * fx), int(y + h * fy), WHITE)
    base = y + h - 8
    blocks = [(0.06, 0.30, 0.52), (0.40, 0.36, 0.68), (0.74, 0.28, 0.46)]
    for fx, fw, fh in blocks:
        bx = int(x + w * fx)
        bw = int(w * fw)
        bh = int(h * fh)
        box(s, bx, base - bh, bw, bh, (30, 44, 66))
        for wy in range(base - bh + 6, base - 6, 10):
            for wx in range(bx + 5, bx + bw - 5, 11):
                box(s, wx, wy, 4, 5, GOLD_SOFT)
    ex, ey = int(x + w * 0.58), int(y + h * 0.30)
    disc(s, ex, ey, 11, FLAME)
    disc(s, ex, ey, 6, FLAME_Y)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1),
                   (1, -1), (-1, 1)):
        seg(s, ex + dx * 12, ey + dy * 12, ex + dx * 19, ey + dy * 19, FLAME)
    for fx, fy in ((0.20, 0.22), (0.78, 0.18), (0.52, 0.10)):
        dx, dy = int(x + w * fx), int(y + h * fy)
        disc(s, dx, dy, 2, WHITE)
        for t in range(0, 14, 4):
            px(s, dx - t, dy + 1, WHITE)
            px(s, dx - t - 1, dy + 1, WHITE)


def scene_radar(s, x, y, w, h):
    box(s, x, y, w, h, SKY)
    land = [(int(x + w * fx), int(y + h * fy)) for fx, fy in
            ((0.14, 0.92), (0.24, 0.62), (0.20, 0.32), (0.34, 0.14),
             (0.44, 0.36), (0.40, 0.70), (0.30, 0.95))]
    poly_fill(s, land, LAND_TAN)
    poly_edge(s, land, LAND_EDGE)
    cx, cy = int(x + w * 0.66), int(y + h * 0.34)
    ring(s, cx, cy, 12, RED)
    ring(s, cx, cy, 7, RED)
    tri(s, [(cx, cy - 6), (cx - 5, cy + 5), (cx + 5, cy + 5)], INK)
    seg(s, cx - 16, cy + 8, cx - 6, cy + 4, INK)
    put_text(s, x + w - 72, y + h - 11, "5 MIN ALERT", 1, RED)


def scene_quake(s, x, y, w, h):
    box(s, x, y, w, h, PAPER_DIM)
    tri(s, [(x + 8, y + h - 8), (x + 62, y + 8), (x + 116, y + h - 8)],
        (120, 130, 120))
    tri(s, [(x + 96, y + h - 8), (x + 140, y + 18), (x + 184, y + h - 8)],
        (90, 105, 95))
    tri(s, [(x + 134, y + 18), (x + 146, y + 18), (x + 140, y + 28)], WHITE)
    pts = [(x + 6, y + 30), (x + 26, y + 30), (x + 34, y + 18),
           (x + 42, y + 44), (x + 50, y + 24), (x + 58, y + 36),
           (x + 66, y + 30), (x + 86, y + 30), (x + 94, y + 14),
           (x + 102, y + 46), (x + 110, y + 30), (x + 130, y + 30),
           (x + 150, y + 30), (x + 170, y + 30), (x + 186, y + 30)]
    for a, b in zip(pts, pts[1:]):
        seg(s, a[0], a[1], b[0], b[1], RED)
    put_text(s, x + 8, y + 4, "M5.3", 2, INK)


def scene_rocket(s, x, y, w, h):
    box(s, x, y, w, h, NIGHT)
    for fx, fy in ((0.10, 0.12), (0.85, 0.10), (0.70, 0.22), (0.15, 0.30),
                   (0.90, 0.35), (0.30, 0.08)):
        px(s, int(x + w * fx), int(y + h * fy), WHITE)
    cx = x + w // 2
    box(s, cx - 7, y + 12, 14, 24, WHITE)
    tri(s, [(cx - 7, y + 12), (cx + 7, y + 12), (cx, y + 2)], RED)
    tri(s, [(cx - 7, y + 36), (cx - 13, y + 44), (cx - 7, y + 42)], RED)
    tri(s, [(cx + 7, y + 36), (cx + 13, y + 44), (cx + 7, y + 42)], RED)
    tri(s, [(cx - 5, y + 36), (cx + 5, y + 36), (cx, y + 50)], FLAME_Y)
    put_text_c(s, cx, y + h - 11, "SHENZHOU-24", 1, WHITE)


def scene_fine(s, x, y, w, h):
    box(s, x, y, w, h, PAPER_DIM)
    bx = x + 10
    box(s, bx, y + h - 10, 74, 6, NAVY_MID)
    box(s, bx + 4, y + 16, 66, 4, NAVY_MID)
    tri(s, [(bx, y + 16), (bx + 37, y + 4), (bx + 74, y + 16)], NAVY_MID)
    for i in range(3):
        box(s, bx + 8 + i * 22, y + 22, 8, y + h - 32, WHITE)
    put_text(s, x + w - 62, y + 10, "5%", 3, RED)
    put_text(s, x + w - 62, y + 34, "MAX FINE", 1, INK)


def scene_chip(s, x, y, w, h):
    box(s, x, y, w, h, (222, 234, 240))
    cx, cy = x + w // 2, y + h // 2
    box(s, cx - 22, cy - 22, 44, 44, INK)
    for i in range(4):
        off = -15 + i * 10
        box(s, cx + off, cy - 28, 5, 6, GOLD)
        box(s, cx + off, cy + 22, 5, 6, GOLD)
        box(s, cx - 28, cy + off, 6, 5, GOLD)
        box(s, cx + 22, cy + off, 6, 5, GOLD)
    put_text(s, cx - 11, cy - 7, "AI", 2, WHITE)


def scene_eu(s, x, y, w, h):
    box(s, x, y, w, h, PAPER_DIM)
    cx, cy = x + w // 2, y + h // 2
    for k in range(12):
        a = 2 * math.pi * k / 12
        disc(s, cx + int(21 * math.cos(a)), cy + int(21 * math.sin(a)),
             2, GOLD)
    put_text_c(s, cx, cy - 7, "1,283", 2, NAVY)


def scene_pill(s, x, y, w, h):
    box(s, x, y, w, h, WHITE)
    cx, cy = x + w // 2, y + 20
    box(s, cx - 42, cy - 10, 42, 20, RED)
    box(s, cx, cy - 10, 42, 20, (232, 232, 232))
    disc(s, cx - 42, cy, 10, RED)
    disc(s, cx + 42, cy, 10, (232, 232, 232))
    ring(s, cx - 42, cy, 10, INK)
    ring(s, cx + 42, cy, 10, INK)
    seg(s, cx - 42, cy - 10, cx + 42, cy - 10, INK)
    seg(s, cx - 42, cy + 10, cx + 42, cy + 10, INK)
    put_text_c(s, cx, y + h - 15, "$41BN", 2, INK)


def scene_blast(s, x, y, w, h):
    box(s, x, y, w, h, PAPER_DIM)
    cx = x + w // 2
    tri(s, [(cx, y + 4), (x + 12, y + h - 12), (x + w - 12, y + h - 12)],
        FLAME_Y)
    seg(s, cx, y + 4, x + 12, y + h - 12, INK)
    seg(s, cx, y + 4, x + w - 12, y + h - 12, INK)
    seg(s, x + 12, y + h - 12, x + w - 12, y + h - 12, INK)
    put_text(s, cx - 6, y + h - 34, "!", 2, INK)
    put_text(s, x + 6, y + 2, "5 TONS", 1, RED)


def scene_plane(s, x, y, w, h):
    box(s, x, y, w, h, SKY)
    cx, cy = x + w // 2, y + 20
    box(s, cx - 34, cy - 3, 62, 7, INK)
    tri(s, [(cx + 28, cy - 3), (cx + 44, cy + 1), (cx + 28, cy + 4)], INK)
    tri(s, [(cx - 6, cy - 3), (cx + 6, cy - 16), (cx + 12, cy - 3)], INK)
    tri(s, [(cx - 2, cy + 4), (cx + 8, cy + 16), (cx + 14, cy + 4)], INK)
    tri(s, [(cx - 34, cy - 3), (cx - 26, cy - 14), (cx - 20, cy - 3)], INK)
    px0, py0 = cx + 30, cy + 10
    for t in range(0, 26, 5):
        seg(s, px0 + t, py0 + t // 2, px0 + t + 3, py0 + t // 2 + 1, RED)
    disc(s, px0 + 30, py0 + 14, 3, RED)
    put_text(s, x + 6, y + h - 11, "CESSNA 208", 1, INK)


def scene_gaza(s, x, y, w, h):
    box(s, x, y, w, h, PAPER_DIM)
    base = y + h - 6
    box(s, x + 14, base - 34, 52, 34, (120, 118, 112))
    box(s, x + 78, base - 24, 44, 24, (150, 148, 142))
    for wy in range(base - 30, base - 6, 9):
        for wx in (x + 22, x + 40, x + 86, x + 102):
            box(s, wx, wy, 5, 5, GOLD_SOFT)
    disc(s, x + 40, base - 40, 5, (140, 140, 140))
    disc(s, x + 48, base - 48, 4, (160, 160, 160))
    disc(s, x + 34, base - 52, 4, (170, 170, 170))
    disc(s, x + 40, base - 34, 4, FLAME_Y)


SECONDARY_SCENES = [
    scene_radar, scene_quake, scene_rocket, scene_fine, scene_chip,
    scene_eu, scene_pill, scene_blast, scene_plane, scene_gaza,
]
HERO_SCENES = [scene_markets, scene_hormuz, scene_drones]


# ================================================================ LAYOUT
def paint_badge(s, x_right, y, label):
    """Badge status rata kanan di (x_right, y); kembalikan x awal badge."""
    bw = measure(label, 1) + 8
    bx = x_right - bw
    box(s, bx, y, bw, 12, BADGE_FILL[label])
    put_text(s, bx + 4, y + 2, label, 1, WHITE)
    return bx


def paint_header(s, fields_text):
    put_text(s, 16, 3, "ONE DAY OF WORLD NEWS ON ONE PAGE", 1, RED)
    put_text(s, SHEET_W - 16 - measure(fields_text, 1), 3, fields_text, 1,
             INK)
    put_text_c(s, SHEET_W // 2, 16, "TUESDAY 24 NOVEMBER 2026", 6, INK)
    put_text_c(s, SHEET_W // 2, 62,
               "ASIA'S MARKETS ROAR BACK - THREE TANKERS ABLAZE - "
               "96 DRONES OVER UKRAINE", 2, RED)


def paint_region_bar(s):
    seg_w = 99
    x0 = 17
    y = 80
    for i, (label, _n) in enumerate(REGION_BAR):
        key = label.rsplit(" ", 1)[0]
        box(s, x0 + i * seg_w, y, seg_w, 16, REGION_FILL[key])
        put_text_c(s, x0 + i * seg_w + seg_w // 2, y + 4, label, 1, WHITE)


def paint_timeline(s):
    box(s, 16, 100, 992, 14, NAVY)
    parts = ["UTC"]
    for clock, what in TIMELINE:
        parts.append(clock + " " + what)
    line = "  -  ".join(parts)
    tx = 16 + (992 - measure(line, 1)) // 2
    put_text(s, tx, 103, line, 1, WHITE)
    put_text(s, tx, 103, "UTC", 1, GOLD_SOFT)


def paint_numbers(s):
    put_text(s, 16, 120, "THE DAY IN", 2, RED)
    put_text(s, 16, 136, "NUMBERS", 2, RED)
    for i, (val, label) in enumerate(NUMBERS):
        cx = 160 + i * 141 + 70
        put_text_c(s, cx, 119, val, 3, RED)
        lines = wrap_words(label, 23)
        for li, ln in enumerate(lines):
            put_text_c(s, cx, 141 + li * 8, ln, 1, INK)
        if i:
            rule_h(s, 160 + i * 141, 120, 1, GREY_LINE, 34)


def paint_hero(s, idx, story, x, y):
    _region, _beat, kicker, badge, headline, dek, source = story
    w, h = 320, 194
    HERO_SCENES[idx](s, x, y, w, 112)
    for xx in (x, x + w - 1):
        for yy in range(y, y + 112):
            px(s, xx, yy, GREY_LINE)
    for xx in range(x, x + w):
        px(s, xx, y, GREY_LINE)
        px(s, xx, y + 111, GREY_LINE)
    put_text(s, x, y + 116, kicker, 1, INK)
    paint_badge(s, x + w, y + 115, badge)
    for li, ln in enumerate(wrap_words(headline, 26)):
        put_text(s, x, y + 130 + li * 16, ln, 2, INK)
    for li, ln in enumerate(wrap_words(dek, 50)):
        put_text(s, x, y + 162 + li * 9, ln, 1, GREY_TXT)
    put_text(s, x, y + 189, source, 1, GREY_TXT)


def paint_secondary(s, idx, story, x, y):
    _region, _beat, kicker, badge, headline, dek, source = story
    w = 193
    SECONDARY_SCENES[idx](s, x, y, w, 58)
    for xx in (x, x + w - 1):
        for yy in range(y, y + 58):
            px(s, xx, yy, GREY_LINE)
    for xx in range(x, x + w):
        px(s, xx, y, GREY_LINE)
        px(s, xx, y + 57, GREY_LINE)
    put_text(s, x, y + 62, kicker, 1, INK)
    paint_badge(s, x + w, y + 61, badge)
    for li, ln in enumerate(wrap_words(headline, 15)):
        put_text(s, x, y + 74 + li * 16, ln, 2, INK)
    for li, ln in enumerate(wrap_words(dek, 30)):
        put_text(s, x, y + 107 + li * 9, ln, 1, GREY_TXT)
    put_text(s, x, y + 124, source, 1, GREY_TXT)


def paint_map(s, x, y, w, h):
    box(s, x, y, w, h, (220, 232, 232))
    for poly in LAND:
        pts = [(x + int((lon + 180) * w / 360.0),
                y + int((90 - lat) * h / 180.0)) for lon, lat in poly]
        poly_fill(s, pts, LAND_TAN)
        poly_edge(s, pts, LAND_EDGE)
    nudge = {9: (2, -1), 10: (-2, 1)}
    for num, lon, lat, dx, dy in PINS:
        px0 = x + int((lon + 180) * w / 360.0)
        py0 = y + int((90 - lat) * h / 180.0)
        nx, ny = nudge.get(num, (0, 0))
        r = 3 if num in (9, 10) else 4
        disc(s, px0 + nx, py0 + ny, r, RED)
        ring(s, px0 + nx, py0 + ny, r, WHITE)
        put_text(s, px0 + nx + dx, py0 + ny + dy, str(num), 1, RED)


def paint_also(s):
    put_text(s, 336, 658, "ALSO ON TUESDAY 24 NOVEMBER", 2, INK)
    put_text(s, 16, 658, "WHERE IT HAPPENED", 2, INK)
    paint_map(s, 16, 676, 304, 176)
    put_text(s, 16, 856, "PINS 1-13 PICTURED - 14-34 LISTED", 1, GREY_TXT)
    cols = [336, 676]
    for i, (num, _region, title, detail, _src) in enumerate(ALSO):
        col = i // 11
        row = i % 11
        cx = cols[col]
        ry = 676 + row * 16
        put_text(s, cx, ry, str(num) + " " + title, 1, INK)
        put_text(s, cx, ry + 8, detail, 1, GREY_TXT)


def paint_datecheck(s):
    y = 866
    box(s, 16, y, 992, 78, PAPER)
    for xx in range(16, 1008):
        px(s, xx, y, RED)
        px(s, xx, y + 1, RED)
        px(s, xx, y + 76, RED)
        px(s, xx, y + 77, RED)
    for yy in range(y, y + 78):
        px(s, 16, yy, RED)
        px(s, 17, yy, RED)
        px(s, 1006, yy, RED)
        px(s, 1007, yy, RED)
    put_text(s, 28, y + 6, "DATE CHECK", 2, RED)
    put_text(s, 28, y + 24,
             "EVERY STORY ABOVE HAPPENED OR WAS FIRST REPORTED ON "
             "TUESDAY 24 NOVEMBER 2026 (UTC OR LOCAL DATE).", 1, INK)
    put_text(s, 28, y + 33,
             "LEFT OUT ON PURPOSE - FIRST REPORTED BEFORE TUESDAY: "
             + ", ".join(EXCLUDED[:2]) + ",", 1, INK)
    put_text(s, 28, y + 42, ", ".join(EXCLUDED[2:6]) + ",", 1, INK)
    put_text(s, 28, y + 51, ", ".join(EXCLUDED[6:]) + ".", 1, INK)
    put_text(s, 28, y + 60,
             "NO PHOTOGRAPHS: EVERY PICTURE AND THE MAP WERE DRAWN "
             "IN CODE FOR THIS PAGE.", 1, GREY_TXT)


def paint_footer(s):
    put_text_c(s, SHEET_W // 2, 952,
               "HOW SURE: CONFIRMED = TWO OR MORE OUTLETS - OFFICIAL = "
               "ON THE RECORD FROM AN AUTHORITY - REPORTED = ONE NAMED "
               "OUTLET - CLAIM = ONE SIDE'S WORD, UNVERIFIED", 1, GREY_TXT)
    put_text_c(s, SHEET_W // 2, 966,
               "SOURCES: AP - REUTERS - BBC - AFP - YONHAP - XINHUA - "
               "ABC - EURONEWS - NASA - ROSCOSMOS - ARIANESPACE - USNO",
               1, GREY_TXT)
    put_text_c(s, SHEET_W // 2, 980,
               "ORIGINAL CODE-DRAWN VECTOR SCENES - 1024 X 1024 - "
               "NEWS-IMAGE-20261124", 1, GREY_TXT)


def render():
    s = make_sheet()
    fields = "34 STORIES - 9 REGIONS - EVERY ONE DATED TUE 24 NOV 2026"
    paint_header(s, fields)
    paint_region_bar(s)
    paint_timeline(s)
    paint_numbers(s)
    rule_h(s, 16, 158, 992, INK, 2)
    for i, story in enumerate(HEROES):
        paint_hero(s, i, story, 16 + i * 336, 162)
    rule_h(s, 16, 360, 992, INK, 2)
    put_text(s, 16, 366, "THE DAY IN TEN MORE", 2, INK)
    rule_h(s, 252, 372, 756, GREY_LINE, 1)
    for i, story in enumerate(SECONDARY):
        col, row = i % 5, i // 5
        paint_secondary(s, i, story, 16 + col * 199, 384 + row * 138)
    paint_also(s)
    paint_datecheck(s)
    paint_footer(s)
    return s


# -------------------------------------------------------------- validasi
def check_chars(text):
    assert all(c in GLYPH_ROWS for c in text), "glyph hilang: " + repr(text)


def validate():
    assert len(HEROES) == 3 and len(SECONDARY) == 10 and len(ALSO) == 21
    total = len(HEROES) + len(SECONDARY) + len(ALSO)
    assert total == 34, total
    counts = {}
    for story in HEROES + SECONDARY:
        counts[story[0]] = counts.get(story[0], 0) + 1
    for _num, region, _t, _d, _s in ALSO:
        counts[region] = counts.get(region, 0) + 1
    bar = {label.rsplit(" ", 1)[0]: n for label, n in REGION_BAR}
    assert counts == bar, (counts, bar)
    assert sum(bar.values()) == 34
    assert len(bar) == 10  # 9 region + WORLD
    assert measure("TUESDAY 24 NOVEMBER 2026", 6) <= 1008
    tl = "  -  ".join(["UTC"] + [c + " " + w for c, w in TIMELINE])
    assert measure(tl, 1) <= 992, measure(tl, 1)
    for val, label in NUMBERS:
        assert len(wrap_words(label, 23)) <= 2, label
    for story in HEROES:
        _r, _b, kicker, badge, headline, dek, source = story
        assert badge in BADGE_FILL
        assert len(wrap_words(headline, 26)) <= 2, headline
        assert len(wrap_words(dek, 50)) <= 3, dek
        assert measure(kicker, 1) + measure(badge, 1) + 12 <= 320
        for t in (kicker, headline, dek, source):
            check_chars(t)
    for story in SECONDARY:
        _r, _b, kicker, badge, headline, dek, source = story
        assert badge in BADGE_FILL
        assert len(wrap_words(headline, 15)) <= 2, headline
        assert len(wrap_words(dek, 30)) <= 2, dek
        assert measure(kicker, 1) + measure(badge, 1) + 12 <= 193
        for t in (kicker, headline, dek, source):
            check_chars(t)
    for num, _r, title, detail, _s in ALSO:
        assert len(str(num) + " " + title) <= 54, title
        assert len(detail) <= 54, detail
        check_chars(title)
        check_chars(detail)
    for line in (", ".join(EXCLUDED[:2]), ", ".join(EXCLUDED[2:6]),
                 ", ".join(EXCLUDED[6:])):
        assert measure(line, 1) <= 960, line
    for _num, lon, lat, _dx, _dy in PINS:
        assert -180 <= lon <= 180 and -90 <= lat <= 90
    check_chars("TUESDAY 24 NOVEMBER 2026")
    check_chars("ASIA'S MARKETS ROAR BACK - THREE TANKERS ABLAZE - "
                "96 DRONES OVER UKRAINE")


def main():
    validate()
    data = encode_png(render())
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes, 34 stories, 9 regions + WORLD)"
          % (path, len(data)))


if __name__ == "__main__":
    main()
