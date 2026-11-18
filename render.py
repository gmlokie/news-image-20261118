#!/usr/bin/env python3
"""Front page for Wednesday 18 November 2026: 34 real world-news stories,
6 continents, one image. Drawn flat-style with Pillow shapes only.

Everything on the page is a story that happened or was first reported on
18 November 2026 (lead: Trump lands in Manila for the Quad/ASEAN summits).
Run: python3 render.py  ->  writes entry.png (1024x1024) next to this file.
"""
from PIL import Image, ImageDraw, ImageFont
import os

PAGE = 1024
PAPER = (247, 242, 230)
INK = (20, 20, 20)
RED = (180, 35, 24)
NAVY = (29, 53, 87)
GREY = (90, 90, 90)
PALE = (168, 184, 200)
SEA = (46, 110, 166)
SKY = (191, 217, 232)
GOLD = (200, 160, 0)
WHITE = (255, 255, 255)

FONTS = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONTS, "DejaVuSans-Bold.ttf")
REGULAR = os.path.join(FONTS, "DejaVuSans.ttf")


def load(path, size):
    return ImageFont.truetype(path, int(round(size)))


def shrink(draw, text, path, start, limit):
    """Largest font size (down to 10) that fits the text inside limit px."""
    size = start
    while size > 10:
        face = load(path, size)
        if draw.textlength(text, font=face) <= limit:
            return face
        size -= 1
    return load(path, size)


def wrap_lines(draw, text, face, limit):
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=face) <= limit:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def shorten(draw, text, face, limit):
    """Drop whole words from the end until it fits; ellipsis only if needed."""
    if draw.textlength(text, font=face) <= limit:
        return text
    words = text.split()
    while len(words) > 1 and draw.textlength(" ".join(words) + " \u2026", font=face) > limit:
        words.pop()
    return " ".join(words) + " \u2026"


canvas = Image.new("RGB", (PAGE, PAGE), PAPER)
d = ImageDraw.Draw(canvas)

# ---------- masthead ----------
d.rectangle([0, 0, PAGE, 6], fill=RED)
d.text((PAGE // 2, 12), "THE WORLD IN ONE IMAGE",
       font=load(BOLD, 19), fill=NAVY, anchor="ma")
date_face = shrink(d, "WEDNESDAY 18 NOVEMBER 2026", BOLD, 44, 984)
d.text((PAGE // 2, 34), "WEDNESDAY 18 NOVEMBER 2026", font=date_face, fill=INK, anchor="ma")
sub_face = shrink(d, "34 STORIES \u00b7 6 CONTINENTS \u2014 EVERY STORY HAPPENED OR WAS FIRST REPORTED TODAY",
                  BOLD, 16, 984)
d.text((PAGE // 2, 84), "34 STORIES \u00b7 6 CONTINENTS \u2014 EVERY STORY HAPPENED OR WAS FIRST REPORTED TODAY",
       font=sub_face, fill=RED, anchor="ma")
d.line([24, 104, 1000, 104], fill=INK, width=2)

# ---------- lead: Trump lands in Manila ----------
d.rectangle([24, 112, 1000, 352], outline=INK, width=2)
ax, ay, bx, by = 32, 120, 424, 344
d.rectangle([ax, ay, bx, by], fill=SKY)
d.ellipse([ax + 300, ay + 14, ax + 356, ay + 70], fill=(255, 200, 60))
for cx, cy, r in [(ax + 40, ay + 30, 16), (ax + 70, ay + 24, 20), (ax + 100, ay + 32, 14),
                  (ax + 220, ay + 52, 14), (ax + 246, ay + 46, 18)]:
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=WHITE)
for bx0, bw, bh in [(ax + 6, 34, 84), (ax + 46, 26, 108), (ax + 78, 40, 70),
                    (ax + 124, 24, 96), (ax + 154, 30, 118), (ax + 190, 36, 78),
                    (ax + 232, 28, 104), (ax + 266, 38, 66), (ax + 310, 30, 92),
                    (ax + 346, 40, 74)]:
    d.rectangle([bx0, by - 78 - bh, bx0 + bw, by - 78], fill=(70, 90, 120))
d.rectangle([ax, by - 78, bx, by], fill=SEA)
for wx in range(ax + 8, bx - 10, 28):
    d.arc([wx, by - 44, wx + 24, by - 28], 180, 360, fill=WHITE, width=2)
px, py = ax + 130, ay + 108
d.polygon([(px, py), (px + 150, py), (px + 168, py + 10), (px + 150, py + 18),
           (px, py + 18)], fill=(240, 240, 240))
d.polygon([(px + 118, py - 2), (px + 138, py - 26), (px + 150, py - 26),
           (px + 140, py - 2)], fill=(200, 40, 30))
d.polygon([(px + 60, py + 16), (px + 96, py + 44), (px + 110, py + 44),
           (px + 82, py + 16)], fill=(200, 200, 200))
for wx in range(px + 18, px + 140, 18):
    d.ellipse([wx, py + 6, wx + 7, py + 12], fill=NAVY)
for rx in range(ax + 20, bx - 20, 44):
    d.ellipse([rx, by - 70, rx + 8, by - 62], fill=GOLD)
d.rectangle([ax, ay, bx, by], outline=INK, width=1)

tx = 440
d.text((tx, 124), "LEAD \u00b7 ASIA \u2014 TRUMP IN ASIA", font=load(BOLD, 15), fill=RED)
head_face = shrink(d, "TRUMP LANDS IN MANILA", BOLD, 40, 1000 - tx - 8)
lead_lines = wrap_lines(d, "TRUMP LANDS IN MANILA", head_face, 1000 - tx - 8)
y = 150
for line in lead_lines[:2]:
    d.text((tx, y), line, font=head_face, fill=INK)
    y += int(head_face.size * 1.12)
sub_lines = wrap_lines(d, "Quad talks open in Manila as Trump heads to a historic Xi meeting on Thursday.",
                       load(REGULAR, 19), 1000 - tx - 8)
y += 6
for line in sub_lines:
    d.text((tx, y), line, font=load(REGULAR, 19), fill=INK)
    y += 24
quote_lines = wrap_lines(d, "Trump praised \u201cfriend\u201d Albanese as leaders gathered for the ASEAN and Quad summits.",
                         load(REGULAR, 15), 1000 - tx - 8)
y += 4
for line in quote_lines:
    d.text((tx, y), line, font=load(REGULAR, 15), fill=GREY)
    y += 20

# ---------- four medium stories ----------
PANELS = [
    ("UKRAINE HITS KERCH BRIDGE AGAIN", "Second strike in two days; Russia hits Kyiv bridges", "bridge"),
    ("HORMUZ TANKERS MINED", "Iran claims six tankers sunk since Sunday; 3rd US carrier in", "tanker"),
    ("CANADA\u2013CHINA EXTEND TRADE DEALS", "Xi meets Carney ahead of APEC summit", "flags"),
    ("UK SANCTIONS WEST BANK FIRMS", "Eight settlement builders hit in two-state push", "ban"),
]
mx, my, mgap = 24, 360, 8
mw = (1024 - 48 - 3 * mgap) // 4
for i, (head, sub, kind) in enumerate(PANELS):
    x0 = mx + i * (mw + mgap)
    x1 = x0 + mw
    d.rectangle([x0, my, x1, 496], outline=INK, width=1)
    d.line([x0, my + 52, x1, my + 52], fill=GREY, width=1)
    ix, iy = x0 + 8, my + 6
    if kind == "bridge":
        d.rectangle([ix + 12, iy + 30, ix + 92, iy + 38], fill=(107, 114, 128))
        d.rectangle([ix + 128, iy + 30, ix + 208, iy + 38], fill=(107, 114, 128))
        d.rectangle([ix + 20, iy + 38, ix + 28, iy + 48], fill=(90, 96, 104))
        d.rectangle([ix + 180, iy + 38, ix + 188, iy + 48], fill=(90, 96, 104))
        d.polygon([(ix + 96, iy + 44), (ix + 124, iy + 40), (ix + 122, iy + 48),
                   (ix + 96, iy + 50)], fill=(107, 114, 128))
        for sx, sy, sr in [(ix + 96, iy + 14, 9), (ix + 112, iy + 8, 11), (ix + 128, iy + 14, 9)]:
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120))
        d.ellipse([ix + 100, iy + 20, ix + 122, iy + 34], fill=(255, 140, 0))
    elif kind == "tanker":
        d.rectangle([ix + 10, iy + 24, ix + 150, iy + 38], fill=(40, 40, 40))
        d.rectangle([ix + 115, iy + 10, ix + 150, iy + 24], fill=(90, 90, 90))
        for fx, fy in [(ix + 30, iy + 6), (ix + 62, iy + 2)]:
            d.polygon([(fx, fy + 18), (fx + 8, fy), (fx + 16, fy + 18)], fill=(255, 140, 0))
        d.rectangle([ix + 10, iy + 42, ix + 200, iy + 45], fill=SEA)
    elif kind == "flags":
        for j, col in enumerate([(200, 40, 40), WHITE]):
            fx = ix + 30 + j * 70
            d.line([fx, iy + 4, fx, iy + 42], fill=INK, width=2)
            d.polygon([(fx, iy + 4), (fx + 44, iy + 12), (fx, iy + 20)], fill=col, outline=INK)
        d.arc([ix + 80, iy + 26, ix + 140, iy + 48], 180, 360, fill=NAVY, width=3)
    else:
        d.rectangle([ix + 60, iy + 2, ix + 150, iy + 46], fill=WHITE, outline=INK)
        for ly in (10, 20, 30):
            d.line([ix + 70, iy + ly, ix + 140, iy + ly], fill=GREY, width=2)
        d.ellipse([ix + 30, iy + 4, ix + 74, iy + 48], outline=RED, width=4)
        d.line([ix + 36, iy + 42, ix + 68, iy + 10], fill=RED, width=4)
    panel_head = load(BOLD, 17)
    head_lines = wrap_lines(d, head, panel_head, mw - 16)
    yy = my + 60
    for line in head_lines[:2]:
        d.text((x0 + 8, yy), line, font=panel_head, fill=INK)
        yy += 20
    sub_lines = wrap_lines(d, sub, load(REGULAR, 13), mw - 16)
    for line in sub_lines[:2]:
        d.text((x0 + 8, yy), line, font=load(REGULAR, 13), fill=GREY)
        yy += 17

# ---------- map strip ----------
d.rectangle([24, 504, 1000, 596], outline=INK, width=1)
d.text((32, 508), "WHERE THE DAY HAPPENED", font=load(BOLD, 13), fill=NAVY)
LAND = [
    [(60, 534), (150, 528), (230, 534), (240, 552), (200, 566), (150, 570), (110, 560), (70, 548)],
    [(268, 530), (292, 528), (296, 540), (276, 542)],
    [(240, 572), (280, 570), (300, 580), (288, 592), (262, 590), (244, 580)],
    [(468, 534), (508, 530), (528, 538), (516, 550), (488, 550), (470, 542)],
    [(478, 556), (522, 554), (542, 566), (530, 588), (500, 590), (480, 572)],
    [(548, 530), (700, 526), (820, 532), (860, 548), (830, 566), (740, 570), (640, 568), (556, 556)],
    [(760, 572), (800, 570), (830, 576), (800, 582), (765, 580)],
    [(800, 578), (860, 576), (880, 586), (850, 592), (808, 590)],
]
for poly in LAND:
    d.polygon(poly, fill=PALE, outline=(120, 140, 160))
PINS = [
    (500, 542, "Kerch", 8, 6),
    (600, 556, "Hormuz", 8, 6),
    (812, 562, "Manila", 8, 6),
    (196, 540, "Ottawa", 8, -14),
    (742, 548, "Shenzhen", 8, -14),
]
pin_face = load(BOLD, 11)
for x, y, label, dx, dy in PINS:
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=RED, outline=WHITE, width=1)
    d.text((x + dx, y + dy), label, font=pin_face, fill=RED)

# ---------- story grid 06-34 ----------
STORIES = [
    (6, "EUROPE", "Russia hits two Dnipro bridges in Kyiv"),
    (7, "ASIA", "Japan scrambles jets on Russian planes"),
    (8, "MIDEAST", "Iran drones hit US radar base in Bahrain"),
    (9, "MIDEAST", "Houthis seize strait; hit Saudi airport"),
    (10, "MIDEAST", "US strikes Qeshm Island, Iran says; US silent"),
    (11, "MIDEAST", "Iran claims 18th US MQ-1 drone downed"),
    (12, "MIDEAST", "Israel MPs elect Eisenkot ally as speaker"),
    (13, "MIDEAST", "Jordan bans Telegram over national security"),
    (14, "MIDEAST", "Taiwan \u2018urgently needs\u2019 $14bn US arms"),
    (15, "EUROPE", "EU to borrow \u20ac45bn to plug Ukraine budget gap"),
    (16, "EUROPE", "New Kyiv\u2013Europe\u2013US talks, Zelenskyy says"),
    (17, "ASIA", "Modi offers free e-visas, maritime ties to ASEAN"),
    (18, "ASIA", "Baidu chief warns of AI \u2018bubble\u2019 before APEC"),
    (19, "ASIA", "US widens chip-export checks to SE Asia, Brazil"),
    (20, "ASIA", "Cyclone Akvan strengthens over Bay of Bengal"),
    (21, "ASIA", "Amazon pledges $7bn for India\u2019s renewables"),
    (22, "AFRICA", "South Africa: 17 dead in two mass shootings"),
    (23, "AFRICA", "Guinea mining crackdown displaces thousands"),
    (24, "AFRICA", "South Sudan delays first elections to February"),
    (25, "AFRICA", "Ethiopia accuses Eritrea over Tigray offensive"),
    (26, "AFRICA", "Congo Ebola outbreak \u2018defies control\u2019"),
    (27, "USA", "US banks hit by outage; Chase, Wells Fargo down"),
    (28, "USA", "Microsoft services back after 36-hour outage"),
    (29, "USA", "Epstein \u2018did not kill himself\u2019, expert says"),
    (30, "AMERICAS", "Costa Rican journalist killed probing cartels"),
    (31, "OCEANIA", "Trump hails \u2018friend\u2019 Albanese at Quad"),
    (32, "OCEANIA", "Australia pay gap falls below 20% first time"),
    (33, "WORLD", "Dhoni retires from IPL; becomes CSK mentor"),
    (34, "WORLD", "Pope Leo backs Amazon defenders on Peru trip"),
]
num_face = load(BOLD, 13)
reg_face = load(BOLD, 13)
head_face = load(REGULAR, 13)
left_col, right_col = STORIES[:15], STORIES[15:]
d.line([508, 604, 508, 996], fill=(200, 190, 170), width=1)
for col_i, items in enumerate((left_col, right_col)):
    cx = 24 if col_i == 0 else 520
    col_w = 476
    for row, (n, region, headline) in enumerate(items):
        y = 606 + row * 26
        num_txt = f"{n:02d} \u00b7 "
        reg_txt = region + " \u2014 "
        w_num = d.textlength(num_txt, font=num_face)
        w_reg = d.textlength(reg_txt, font=reg_face)
        room = col_w - w_num - w_reg
        shown = shorten(d, headline, head_face, room)
        x = cx
        d.text((x, y), num_txt, font=num_face, fill=RED)
        x += w_num
        d.text((x, y), reg_txt, font=reg_face, fill=NAVY)
        x += w_reg
        d.text((x, y), shown, font=head_face, fill=INK)

# ---------- footer ----------
d.line([24, 1000, 1000, 1000], fill=INK, width=1)
d.text((PAGE // 2, 1004), "All 34 stories happened or were first reported on Wednesday 18 November 2026.",
       font=load(REGULAR, 13), fill=GREY, anchor="ma")

canvas.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", canvas.size)
