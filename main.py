#!/usr/bin/env python3
"""make.fun news-image-20261124: THE WORLD IN ONE DAY - TUESDAY 24 NOVEMBER 2026.

Draws a 1024x1024 newspaper front page with 34 verified stories from
Tuesday 24 November 2026, using only the Python standard library.
The program renders every pixel itself (zlib+struct PNG encoder, a
hand-defined 5x7 bitmap font) - no network, no external files, fully
deterministic: two runs produce byte-identical output.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
BG = (247, 243, 232)      # newsprint cream
INK = (17, 24, 39)        # near-black
NAVY = (11, 42, 74)       # header band
NAVY_SOFT = (31, 56, 100)
TITLE = (11, 42, 74)
BODY = (51, 51, 51)
RULE = (203, 197, 184)    # thin row rules
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
FOOT = (90, 88, 80)

CAT_COLORS = {
    "CONFLICT": (192, 57, 43),
    "POLITICS": (31, 56, 100),
    "ECONOMY": (30, 122, 52),
    "TECH": (108, 52, 131),
    "CLIMATE": (14, 124, 123),
    "HEALTH": (93, 109, 126),
    "SPORT": (211, 84, 0),
    "CULTURE": (183, 149, 11),
}

# ------------------------------------------------------- 5x7 bitmap font
# Each glyph: 7 rows of 5 cells, '#' = on. Uppercase, digits, punctuation.
FONT = {
    "A": (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "B": ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    "C": (" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "),
    "D": ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
    "E": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    "F": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    "G": (" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"),
    "H": ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "I": (" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "J": ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    "K": ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    "L": ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    "M": ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
    "N": ("#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"),
    "O": (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "P": ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    "Q": (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    "R": ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    "S": (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    "T": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    "U": ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "V": ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "W": ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
    "X": ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    "Y": ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
    "Z": ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    "0": (" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "),
    "1": ("  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "2": (" ### ", "#   #", "    #", "  ## ", " #   ", "#    ", "#####"),
    "3": ("#####", "   # ", "  #  ", "   # ", "    #", "#   #", " ### "),
    "4": ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    "5": ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    "6": ("  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "),
    "7": ("#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "),
    "8": (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    "9": (" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "),
    " ": ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
    ".": ("     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "),
    ",": ("     ", "     ", "     ", "     ", " ##  ", "  #  ", " #   "),
    ":": ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "),
    ";": ("     ", " ##  ", " ##  ", "     ", " ##  ", "  #  ", " #   "),
    "'": ("  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "),
    "-": ("     ", "     ", "     ", " ### ", "     ", "     ", "     "),
    "(": ("   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "),
    ")": (" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "),
    "/": ("    #", "   # ", "   # ", "  #  ", " #   ", " #   ", "#    "),
    "&": (" ##  ", "#  # ", "# #  ", " #   ", "# # #", "#  # ", " ## #"),
    "%": ("##  #", "## # ", "   # ", "  #  ", " #   ", "# ## ", "#  ##"),
    "+": ("     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "),
    "=": ("     ", "     ", "#####", "     ", "#####", "     ", "     "),
    "?": (" ### ", "#   #", "    #", "  ## ", "  #  ", "     ", "  #  "),
    "!": ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
    '"': (" # # ", " # # ", "     ", "     ", "     ", "     ", "     "),
    "$": ("  #  ", " ####", "# #  ", " ### ", "  # #", "#### ", "  #  "),
    "#": (" # # ", " # # ", "#####", " # # ", "#####", " # # ", " # # "),
    "*": ("     ", "  #  ", "# # #", " ### ", "# # #", "  #  ", "     "),
    "_": ("     ", "     ", "     ", "     ", "     ", "     ", "#####"),
    "<": ("    #", "   # ", "  #  ", " #   ", "  #  ", "   # ", "    #"),
    ">": ("#    ", " #   ", "  #  ", "   # ", "  #  ", " #   ", "#    "),
    "[": (" ### ", " #   ", " #   ", " #   ", " #   ", " #   ", " ### "),
    "]": (" ### ", "   # ", "   # ", "   # ", "   # ", "   # ", " ### "),
    "@": (" ### ", "#   #", "# ###", "# # #", "# ## ", "#    ", " ### "),
}


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_text(buf, x, y, text, scale, color):
    """Draw uppercase ASCII text with the 5x7 font at integer scale."""
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            line = glyph[row]
            for col in range(5):
                if line[col] == "#":
                    for dy in range(scale):
                        for dx in range(scale):
                            set_pixel(buf, cx + col * scale + dx,
                                      y + row * scale + dy, color)
        cx += 6 * scale
    return cx


def draw_text_centered(buf, cx, y, text, scale, color):
    draw_text(buf, cx - text_width(text, scale) // 2, y, text, scale, color)


# ------------------------------------------------------------------ canvas
def new_canvas():
    buf = bytearray(W * H * 3)
    for i in range(0, len(buf), 3):
        buf[i] = BG[0]
        buf[i + 1] = BG[1]
        buf[i + 2] = BG[2]
    return buf


def set_pixel(buf, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = color[0]
        buf[i + 1] = color[1]
        buf[i + 2] = color[2]


def fill_rect(buf, x, y, w, h, color):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            set_pixel(buf, xx, yy, color)


def hline(buf, x, y, w, color):
    for xx in range(x, x + w):
        set_pixel(buf, xx, y, color)


def wrap(text, max_chars):
    """Greedy word wrap to lines of at most max_chars characters."""
    lines = []
    for word in text.split(" "):
        if not lines:
            lines.append(word)
            continue
        if len(lines[-1]) + 1 + len(word) <= max_chars:
            lines[-1] += " " + word
        else:
            lines.append(word)
    return lines


# ------------------------------------------------------------------ stories
# (category, title <=36 chars, detail <=72 chars over 2 lines)
# Edition: the news of Tuesday 24 November 2026. The banner is an
# edition label, not a per-item date claim: many items were first
# reported 22-23 Nov and developed into 24 Nov (see goldfish-review-2.md).
STORIES = [
    ("TECH", "HUANG BACK AT NVIDIA",
     "BOARD REINSTATES CEO AFTER TRUMP PUSH. SHARES JUMP ABOUT 31 PERCENT."),
    ("TECH", "US BLACKLISTS MEGASPEED",
     "COMMERCE ADDS SINGAPORE AI FIRM AND 6 AFFILIATES TO ENTITY LIST."),
    ("POLITICS", "ZELENSKY SEEKS 4-WAY TALKS",
     "KYIV SEEKS TALKS WITH EU, US AND RUSSIA, ZELENSKY TELLS NATO MPS."),
    ("CONFLICT", "EU PLANS 22ND RUSSIA SANCTIONS",
     "PACKAGE TARGETS BANKS, CRYPTO AND RUSSIAN SPORT UNDER THE EU FLAG."),
    ("CONFLICT", "UKRAINE SHARES LIBYA STRIKE VIDEO",
     "KYIV POSTS DRONE VIDEO OF SINKING. SATELLITES SHOW SHIP CAPSIZED."),
    ("CLIMATE", "COP31 FALLOUT: WHAT NEXT",
     "FIVE TAKEAWAYS FROM FAILED TALKS. EXPERTS URGE COP REFORM."),
    ("POLITICS", "TRUMP ATTACKS NEWSOM AT DOJ",
     "SLAMS 548 COMMUTATIONS, ORDERS WIDER FEDERAL DEATH PENALTY PUSH."),
    ("POLITICS", "HUSH MONEY CASE REVIVED",
     "APPEALS COURT GIVES TRUMP PATH TO MOVE CONVICTION TO FEDERAL COURT."),
    ("CONFLICT", "MEXICO: 20 DEAD IN CARTEL ARREST",
     "TROOPS SHOT AT IN SINALOA. 8 HELD, US SEEKS EXTRADITION."),
    ("CONFLICT", "US SANCTIONS IRAN SHADOW BANKS",
     "TREASURY HITS MORE THAN 20 TARGETS IN IRANIAN SHADOW BANKING NETWORK."),
    ("CONFLICT", "GAZA STRIKES KILL NINE IN 2 DAYS",
     "UNRWA STAFFER KILLED IN JABALIA. OXFAM CALLS GAZA A TOXIC WASTELAND."),
    ("CONFLICT", "SUDAN BLACKOUTS AFTER DRONE HITS",
     "RSF DRONES HIT POWER STATIONS. US URGES ARMS HALT AND TRUCE."),
    ("CONFLICT", "YEMEN ROAD ATTACK KILLS 6",
     "BUSES AND TRUCKS HIT IN LAHJ. HOUTHIS AND OFFICIALS TRADE BLAME."),
    ("POLITICS", "UK SANCTIONS MYANMAR GENERALS",
     "LONDON ACTS AFTER ICJ GENOCIDE RULING. UN COUNCIL MEETS 25 NOV."),
    ("POLITICS", "DEMOCRATS WIN 258 HOUSE SEATS",
     "LARGEST HOUSE MAJORITY SINCE 1992. DEMS GAIN 44 SEATS SO FAR."),
    ("POLITICS", "KENYA AND DRC RESTORE TIES",
     "RUTO AND TSHISEKEDI WORK TO BRING BACK AMBASSADORS AFTER 3 YEARS."),
    ("ECONOMY", "BELGIUM STRIKE GROUNDS FLIGHTS",
     "404 FLIGHTS AXED, 50,000 HIT AS UNIONS PROTEST AUSTERITY CUTS."),
    ("HEALTH", "NIGERIA BOAT TOLL RISES TO 29",
     "SEARCH GOES ON AFTER FUNERAL BOAT CAPSIZES IN BAYELSA. 50 RESCUED."),
    ("CLIMATE", "SPACE NUKE THREAT LOOMS",
     "INTEL: RUSSIA MAY LAUNCH NUCLEAR-ARMED SATELLITE BY YEAR END."),
    ("CONFLICT", "NATO SENDS AWACS TO POLAND",
     "ALLIANCE SENDS EARLY WARNING JET AFTER 3 RUSSIAN MISSILES HIT POLAND."),
    ("POLITICS", "GERMANY: 450 SCHOOLS THREATENED",
     "EMAIL BOMB THREATS HIT ABOUT 450 SCHOOLS. MERZ WARNS MOSCOW."),
    ("POLITICS", "NEPAL PM VISITS DELHI",
     "INDIA PLEDGES $1.6BN FOR FLOOD-HIT NEPAL AFTER MODI-SHAH TALKS."),
    ("POLITICS", "BANGLADESH: YUNUS WARNS OF PLOT",
     "YUNUS SAYS A HIGHER LEVEL DIRECTS ATTACKS ON GRAMEEN BANK BRANCHES."),
    ("POLITICS", "CHINA: SPY LEAK DEATH SENTENCE",
     "OFFICIAL GETS DEATH SENTENCE FOR LEAKING 100 REPORTS, 35 SECRETS."),
    ("POLITICS", "IOWA BLAST ON HOLD",
     "COURT CLEARS ARMY TO DETONATE 5 TONS OF LEAD AZIDE. TRUMP HOLDS OFF."),
    ("POLITICS", "MINNESOTA FRAUD RAIDS",
     "PATEL OPENS 41M DOLLAR FRAUD PROBE. CHILD CENTRES RAIDED IN MINNESOTA."),
    ("POLITICS", "IRAN FLOGS SINGER",
     "SINGER FLOGGED FOR PERFORMING WITHOUT HIJAB, LAWYERS SAY."),
    ("SPORT", "UK TO HOST 2035 WOMEN'S CUP",
     "FIFA CONFIRMS UK AS HOST OF THE 2035 WOMEN'S WORLD CUP."),
    ("SPORT", "CHAMPIONS LEAGUE NIGHT",
     "ARSENAL FACE DORTMUND, REAL HOST PSV, MAN CITY MEET NAPOLI TONIGHT."),
    ("TECH", "APPLE IPHONE 18E LEAK",
     "LEAKED CAD FILES SHOW BUDGET IPHONE 18E BORROWING PRO-STYLE CAMERA BUMP."),
    ("HEALTH", "NHS AI CANCER TRIAL",
     "NHS LAUNCHES WORLD'S LARGEST TRIAL OF AI TO SPOT BREAST CANCER EARLIER."),
    ("POLITICS", "SAHEL TALKS RESTART",
     "SAHEL STATES RESTART DIALOGUE WITH WEST AFRICA BLOC ECOWAS."),
    ("POLITICS", "ICE ARREST SPARKS SEATTLE OUTRAGE",
     "FATHER AND DAUGHTER SEIZED BOARDING SEATTLE FLIGHT. OUTRAGE GROWS."),
    ("POLITICS", "GOMEZ QUITS OVER ETHICS REPORT",
     "CALIFORNIA DEMOCRAT RESIGNS AFTER PANEL FINDS SEXUAL MISCONDUCT."),
]

FOOTER_SOURCES = "SOURCES: BBC - REUTERS - AP - FRANCE 24 - SEMAFOR - NYT - TIMES OF INDIA"
FOOTER_LEGEND = "RED CONFLICT - NAVY POLITICS - GREEN ECONOMY - PURPLE TECH - TEAL CLIMATE - GREY HEALTH - ORANGE SPORT AND CULTURE"


def draw_circle(buf, cx, cy, r, color):
    """Midpoint circle outline, 1px."""
    x, y, d = 0, r, 1 - r
    while x <= y:
        for px, py in ((cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y),
                       (cx - x, cy - y), (cx + y, cy + x), (cx - y, cy + x),
                       (cx + y, cy - x), (cx - y, cy - x)):
            set_pixel(buf, px, py, color)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1


def draw_ellipse(buf, cx, cy, rx, ry, color):
    """Parametric ellipse outline, 1px."""
    import math
    for deg in range(360):
        a = math.radians(deg)
        set_pixel(buf, cx + int(rx * math.cos(a)),
                  cy + int(ry * math.sin(a)), color)


def draw_globe(buf, cx, cy, r, color):
    draw_circle(buf, cx, cy, r, color)
    draw_circle(buf, cx, cy, r - 2, color)
    draw_ellipse(buf, cx, cy, r // 2, r, color)
    draw_ellipse(buf, cx, cy, r, r // 2, color)
    hline(buf, cx - r, cy, 2 * r + 1, color)


def render():
    buf = new_canvas()

    # --- header band ------------------------------------------------------
    fill_rect(buf, 0, 0, W, 116, NAVY)
    fill_rect(buf, 0, 116, W, 4, GOLD)
    draw_globe(buf, 92, 58, 40, WHITE)
    # calendar date box, right side
    fill_rect(buf, 906, 16, 84, 84, WHITE)
    fill_rect(buf, 906, 16, 84, 20, GOLD)
    draw_text_centered(buf, 948, 20, "NOV", 2, NAVY)
    draw_text_centered(buf, 948, 44, "24", 5, NAVY)
    draw_text_centered(buf, W // 2, 16, "THE WORLD IN ONE DAY", 5, WHITE)
    draw_text_centered(buf, W // 2, 62, "TUESDAY 24 NOVEMBER 2026", 3, (255, 214, 90))
    draw_text_centered(buf, W // 2, 100, "34 STORIES - EVERY REGION, EVERY BEAT", 2, WHITE)

    # --- deck strip -------------------------------------------------------
    draw_text_centered(
        buf, W // 2, 130,
        "THE NEWS OF TUESDAY 24 NOVEMBER 2026",
        2, NAVY_SOFT)

    # --- story grid: 2 columns x 17 rows, 48px rows ----------------------
    # 48px rows: title at y+2 (14px tall), detail lines at y+18 and y+34
    # (14px tall each) -> 2px gaps throughout, no row rules (a rule at
    # y+45 would strike through the second detail line).
    col_x = [16, 520]
    col_w = 488
    y0 = 150
    row_h = 48
    per_col = 17
    for idx, (cat, title, detail) in enumerate(STORIES):
        col = idx // per_col
        row = idx % per_col
        x = col_x[col]
        y = y0 + row * row_h
        color = CAT_COLORS[cat]
        # number badge, coloured by category; story 1 (top story) in gold
        badge, num_color = (GOLD, NAVY) if idx == 0 else (color, WHITE)
        fill_rect(buf, x, y + 2, 30, 30, badge)
        num = str(idx + 1)
        draw_text(buf, x + (30 - text_width(num, 2)) // 2, y + 10, num, 2, num_color)
        # title
        draw_text(buf, x + 38, y + 2, title, 2, TITLE)
        # detail, wrapped to at most 2 lines of 36 chars, 16px leading
        lines = wrap(detail, 36)[:2]
        for li, line in enumerate(lines):
            draw_text(buf, x + 38, y + 18 + li * 16, line, 2, BODY)

    # --- footer -----------------------------------------------------------
    fy = y0 + per_col * row_h + 6
    draw_text_centered(buf, W // 2, fy, FOOTER_SOURCES, 2, FOOT)
    draw_text_centered(buf, W // 2, fy + 17, FOOTER_LEGEND, 1, FOOT)
    return buf


# -------------------------------------------------------------------- PNG
def png_bytes(buf):
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)  # filter: none
        raw += buf[y * stride:(y + 1) * stride]
    compressed = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", compressed) + chunk(b"IEND", b""))


def main():
    # Validate copy fits before rendering: titles <=36 chars, details <=2 lines.
    for cat, title, detail in STORIES:
        assert cat in CAT_COLORS, cat
        assert len(title) <= 36, (title, len(title))
        lines = wrap(detail, 36)
        assert len(lines) <= 2, (detail, lines)
        for line in lines:
            assert len(line) <= 36, line
    data = png_bytes(render())
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(data)} bytes, {len(STORIES)} stories)")


if __name__ == "__main__":
    main()
