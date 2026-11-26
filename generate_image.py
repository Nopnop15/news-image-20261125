#!/usr/bin/env python3
"""Draw the full-day front page for Wednesday 25 November 2026.

A masthead, one wide hero story and five more panels, all drawn with
Pillow. The finished page is written to entry.png next to this file:

    python3 generate_image.py
"""

import math

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PAPER = (247, 242, 230)
INK = (24, 24, 28)
MUTED = (74, 74, 80)
NAVY = (20, 36, 72)
GOLD = (233, 194, 92)
RED = (176, 32, 32)
TEAL = (36, 108, 102)
DARK = (18, 22, 38)
CARD_LINE = (182, 174, 152)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def split_lines(draw, text, face, limit):
    """Greedy wrap: pack words into lines no wider than limit pixels."""
    out = []
    current = ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=face) <= limit:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def put_lines(draw, x, y, lines, face, fill, step):
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        y += step
    return y


def vgrad(draw, box, top, bottom):
    """Vertical gradient fill inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for row in range(y0, y1):
        t = (row - y0) / span
        mix = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, row), (x1, row)], fill=mix)


def flame(draw, x, y, w, h, inner=(255, 214, 90), outer=(255, 122, 0)):
    """A flame tongue rising from (x, y) with width w and height h."""
    draw.polygon(
        [(x, y), (x + w, y), (x + w * 0.72, y - h * 0.62),
         (x + w * 0.5, y - h), (x + w * 0.28, y - h * 0.62)],
        fill=outer,
    )
    draw.polygon(
        [(x + w * 0.22, y), (x + w * 0.78, y), (x + w * 0.62, y - h * 0.45),
         (x + w * 0.5, y - h * 0.72), (x + w * 0.38, y - h * 0.45)],
        fill=inner,
    )


def smoke(draw, puffs, fill=(60, 60, 66)):
    for cx, cy, rx, ry in puffs:
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill)


def tanker(draw, x, y, w, h, hull=(38, 38, 44), deck=(210, 205, 195)):
    """Side view of an oil tanker: hull, deck line, bridge tower, funnel."""
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=hull)
    draw.rectangle([x, y + h * 0.55, x + w, y + h * 0.62], fill=deck)
    draw.rectangle([x + w * 0.72, y, x + w * 0.88, y + h * 0.55], fill=(240, 238, 232))
    draw.rectangle([x + w * 0.72, y + h * 0.14, x + w * 0.88, y + h * 0.2],
                   fill=(70, 70, 78))
    draw.rectangle([x + w * 0.1, y + h * 0.3, x + w * 0.2, y + h * 0.55],
                   fill=(200, 52, 52))


def mine(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 30, 34))
    for k in range(8):
        ang = k * math.pi / 4
        x1 = cx + r * 0.9 * math.cos(ang)
        y1 = cy + r * 0.9 * math.sin(ang)
        x2 = cx + r * 1.5 * math.cos(ang)
        y2 = cy + r * 1.5 * math.sin(ang)
        draw.line([(x1, y1), (x2, y2)], fill=(30, 30, 34), width=3)


def card(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE,
                   outline=CARD_LINE, width=2)


def card_text(draw, x, y, w, h, scene_h, kicker, headline, subline,
              accent, head_size=23):
    tx = x + 14
    tw = w - 28
    ty = y + scene_h + 10
    draw.text((tx, ty), kicker, font=load(SANS_B, 15), fill=accent)
    ty += 24
    face = load(SERIF_B, head_size)
    lines = split_lines(draw, headline, face, tw)
    ty = put_lines(draw, tx, ty, lines, face, INK, head_size + 4)
    ty += 4
    sface = load(SANS_R, 16)
    slines = split_lines(draw, subline, sface, tw)
    put_lines(draw, tx, ty, slines, sface, MUTED, 21)


def hero_hormuz(draw, x, y, w, h):
    """Night sea in the Strait: two tankers burning, a mine in front."""
    vgrad(draw, (x, y, x + w, y + h), (14, 26, 58), (52, 74, 96))
    for px, py in [(30, 26), (120, 60), (210, 20), (330, 52), (430, 30),
                   (80, 100), (280, 92), (470, 96), (180, 130), (380, 128)]:
        draw.ellipse([x + px - 2, y + py - 2, x + px + 2, y + py + 2],
                     fill=(220, 224, 235))
    # Moon.
    draw.ellipse([x + w - 72, y + 18, x + w - 28, y + 62], fill=(238, 234, 214))
    # Sea.
    draw.rectangle([x, y + h - 58, x + w, y + h], fill=(16, 42, 66))
    for wx in range(0, w, 46):
        draw.line([(x + wx, y + h - 34), (x + wx + 24, y + h - 34)],
                  fill=(90, 120, 150), width=2)
    # Two tankers, the nearer one on fire.
    tanker(draw, x + 30, y + h - 118, 200, 62)
    flame(draw, x + 96, y + h - 116, 52, 66)
    flame(draw, x + 150, y + h - 116, 36, 46)
    smoke(draw, [(x + 120, y + 22, 34, 16), (x + 168, y + 8, 26, 12),
                 (x + 90, y + 40, 24, 11)])
    tanker(draw, x + 290, y + h - 104, 170, 50)
    flame(draw, x + 330, y + h - 102, 40, 48)
    smoke(draw, [(x + 350, y + 30, 28, 13), (x + 392, y + 16, 20, 10)])
    # A naval mine drifting in the foreground.
    mine(draw, x + 470, y + h - 22, 13)


def scene_ras_tanura(draw, x, y, w, h):
    """Dusk over a refinery: towers, flare stack, black smoke."""
    vgrad(draw, (x, y, x + w, y + h), (214, 138, 74), (96, 66, 66))
    draw.ellipse([x + w - 52, y + 10, x + w - 12, y + 50], fill=(250, 222, 160))
    # Distillation towers.
    for tx, th in [(26, 62), (66, 78), (112, 56)]:
        draw.rectangle([x + tx, y + h - th, x + tx + 22, y + h],
                       fill=(64, 58, 56))
        draw.rectangle([x + tx - 4, y + h - th - 8, x + tx + 26, y + h - th],
                       fill=(88, 80, 76))
    # Flare stack with flame.
    draw.rectangle([x + w - 66, y + 14, x + w - 56, y + h], fill=(52, 48, 46))
    flame(draw, x + w - 70, y + 16, 18, 22)
    # Storage tanks.
    for tx in (168, 216):
        draw.ellipse([x + tx, y + h - 44, x + tx + 44, y + h - 26],
                     fill=(150, 142, 130))
        draw.rectangle([x + tx, y + h - 30, x + tx + 44, y + h],
                       fill=(176, 168, 154))
    # Thick black smoke.
    smoke(draw, [(x + 60, y + 12, 30, 12), (x + 110, y + 4, 24, 10),
                 (x + 160, y + 14, 26, 11)], fill=(36, 34, 34))


def scene_ukraine(draw, x, y, w, h):
    """Night strike on a refinery: burning towers under a dark sky."""
    vgrad(draw, (x, y, x + w, y + h), (22, 24, 44), (74, 52, 52))
    for px, py in [(24, 14), (90, 30), (180, 12), (250, 28), (140, 44)]:
        draw.ellipse([x + px - 2, y + py - 2, x + px + 2, y + py + 2],
                     fill=(200, 204, 220))
    # Plant silhouettes.
    for tx, th in [(20, 52), (58, 68), (104, 48), (150, 60), (196, 44)]:
        draw.rectangle([x + tx, y + h - th, x + tx + 20, y + h],
                       fill=(24, 22, 30))
    draw.ellipse([x + 232, y + h - 40, x + 276, y + h - 22], fill=(24, 22, 30))
    draw.rectangle([x + 232, y + h - 28, x + 276, y + h], fill=(24, 22, 30))
    # Two big fires.
    flame(draw, x + 62, y + h - 66, 44, 58)
    flame(draw, x + 150, y + h - 58, 38, 48)
    smoke(draw, [(x + 84, y + 6, 26, 11), (x + 170, y + 12, 24, 10)],
          fill=(44, 40, 44))


def scene_huawei(draw, x, y, w, h):
    """A courthouse front: columns, pediment and the scales of justice."""
    draw.rectangle([x, y, x + w, y + h], fill=(28, 44, 84))
    # Pediment and columns.
    draw.polygon([(x + 36, y + 12), (x + w - 36, y + 12), (x + w // 2, y + 38)],
                 fill=(232, 226, 210))
    for cx in (66, 118, 170, 222):
        draw.rectangle([x + cx, y + 40, x + cx + 14, y + h - 12],
                       fill=(232, 226, 210))
    draw.rectangle([x + 48, y + h - 14, x + w - 48, y + h - 6],
                   fill=(232, 226, 210))
    # Scales: pillar, beam, two pans.
    cx = x + w // 2
    draw.rectangle([cx - 3, y + 46, cx + 3, y + h - 20], fill=GOLD)
    draw.line([(cx - 42, y + 52), (cx + 42, y + 52)], fill=GOLD, width=4)
    for sx in (cx - 42, cx + 42):
        draw.line([(sx, y + 52), (sx, y + 70)], fill=GOLD, width=2)
        draw.pieslice([sx - 16, y + 62, sx + 16, y + 78], 0, 180, fill=GOLD)
    draw.ellipse([cx - 5, y + 42, cx + 5, y + 52], fill=GOLD)


def scene_markets(draw, x, y, w, h):
    """A market chart: red plunge, then a green leg up."""
    draw.rectangle([x, y, x + w, y + h], fill=(250, 246, 238))
    for gy in range(y + 18, y + h - 8, 18):
        draw.line([(x + 8, gy), (x + w - 8, gy)], fill=(226, 220, 206))
    # Red falling leg.
    red_pts = [(x + 16, y + 16), (x + 78, y + 30), (x + 140, y + 26),
               (x + 202, y + 52), (x + 250, y + 74)]
    draw.line(red_pts, fill=RED, width=5)
    draw.polygon([(x + 250, y + 74), (x + 232, y + 68), (x + 246, y + 56)],
                 fill=RED)
    # Green rising leg.
    green_pts = [(x + 250, y + 74), (x + 268, y + 58), (x + 288, y + 44)]
    draw.line(green_pts, fill=(30, 130, 60), width=5)
    draw.polygon([(x + 288, y + 44), (x + 272, y + 40), (x + 282, y + 28)],
                 fill=(30, 130, 60))
    draw.text((x + 16, y + 78), "-6.16%", font=load(SANS_B, 17), fill=RED)


def scene_rocket(draw, x, y, w, h):
    """Compact launch: starry sky, a small rocket lifting off."""
    vgrad(draw, (x, y, x + w, y + h), (16, 28, 66), (64, 88, 132))
    for px, py in [(24, 12), (90, 30), (170, 10), (260, 26), (350, 14),
                   (420, 30), (60, 52), (310, 48)]:
        draw.ellipse([x + px - 2, y + py - 2, x + px + 2, y + py + 2],
                     fill=WHITE)
    # Ground.
    draw.rectangle([x, y + h - 16, x + w, y + h], fill=(52, 48, 44))
    # Rocket.
    rx = x + 40
    draw.polygon([(rx, y + 18), (rx + 26, y + 18), (rx + 26, y + 62),
                  (rx, y + 62)], fill=(240, 240, 235))
    draw.pieslice([rx, y + 4, rx + 26, y + 30], 180, 360, fill=(200, 40, 40))
    draw.rectangle([rx, y + 40, rx + 26, y + 50], fill=(200, 40, 40))
    draw.polygon([(rx - 10, y + 62), (rx, y + 42), (rx, y + 62)],
                 fill=(200, 40, 40))
    draw.polygon([(rx + 26, y + 62), (rx + 26, y + 42), (rx + 36, y + 62)],
                 fill=(200, 40, 40))
    flame(draw, rx + 6, y + 62, 14, 20)
    smoke(draw, [(x + 130, y + h - 14, 26, 9), (x + 180, y + h - 10, 20, 8)])
    draw.text((x + 120, y + 22), "SHENZHOU-24", font=load(SANS_B, 20),
              fill=GOLD)


def build():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, PAGE, 118], fill=NAVY)
    d.rectangle([0, 118, PAGE, 122], fill=GOLD)
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=load(SERIF_B, 46))
    d.text(((PAGE - tw) / 2, 14), title, font=load(SERIF_B, 46), fill=WHITE)
    date = "WEDNESDAY 25 NOVEMBER 2026"
    dw = d.textlength(date, font=load(SANS_B, 27))
    d.text(((PAGE - dw) / 2, 72), date, font=load(SANS_B, 27), fill=GOLD)

    # ---- Hero: tankers hit mines in Hormuz ----
    hx, hy, hw, hh = 24, 134, 976, 276
    card(d, hx, hy, hw, hh)
    hero_hormuz(d, hx + 2, hy + 2, 520, hh - 4)
    tx = hx + 544
    tw2 = hw - 568
    d.text((tx, hy + 22), "STRAIT OF HORMUZ  •  ENERGY",
           font=load(SANS_B, 18), fill=RED)
    face = load(SERIF_B, 40)
    ty = put_lines(d, tx, hy + 52,
                   split_lines(d, "TANKERS HIT MINES, BURN", face, tw2),
                   face, INK, 46)
    sub = ("Iran says two tankers struck naval mines and caught fire on "
           "an unauthorised route through the strait.")
    ty = put_lines(d, tx, ty + 10,
                   split_lines(d, sub, load(SANS_R, 20), tw2),
                   load(SANS_R, 20), MUTED, 26)
    d.text((tx, ty + 12), "Brent crude jumps above $91 a barrel.",
           font=load(SERIF_R, 18), fill=(90, 90, 96))

    # ---- Row 1: three panels ----
    row1_y, row1_h, pw = 424, 262, 312
    for x, scene, kicker, headline, subline, accent in [
        (24, scene_ras_tanura, "SAUDI ARABIA  •  OIL",
         "HOUTHIS HIT RAS TANURA",
         "Houthis claim a strike on the kingdom's biggest refinery; "
         "a Riyadh tower is hit again, 11 hurt.",
         (150, 60, 20)),
        (356, scene_ukraine, "UKRAINE  •  RUSSIA",
         "DRONES TORCH TWO REFINERIES",
         "Kyiv says its drones set Rosneft's Syzran and Kuibyshev "
         "plants ablaze; one killed in Samara.",
         (20, 24, 40)),
        (688, scene_huawei, "UNITED STATES  •  TECH",
         "HUAWEI GUILTY ON 10 COUNTS",
         "A Brooklyn jury convicts Huawei of bank fraud, sanctions "
         "breaches and trade-secret theft.",
         NAVY),
    ]:
        card(d, x, row1_y, pw, row1_h)
        scene(d, x + 2, row1_y + 2, pw - 4, 96)
        card_text(d, x, row1_y, pw, row1_h, 96, kicker, headline, subline,
                  accent, head_size=23)

    # ---- Row 2: two wide panels ----
    row2_y, row2_h, w2 = 700, 244, 478
    for x, scene, kicker, headline, subline, accent in [
        (24, scene_markets, "MARKETS  •  STOCKS",
         "KOSPI -6.2%, DOW TOPS 50,000",
         "Asia's tech rout sinks Seoul 6.16% as the Dow closes above "
         "50,000 for the first time.",
         RED),
        (522, scene_rocket, "SPACE  •  CHINA",
         "SHENZHOU-24 LAUNCHES",
         "Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali — the first "
         "Pakistani in orbit — head to Tiangong.",
         TEAL),
    ]:
        card(d, x, row2_y, w2, row2_h)
        scene(d, x + 2, row2_y + 2, w2 - 4, 98)
        card_text(d, x, row2_y, w2, row2_h, 98, kicker, headline, subline,
                  accent, head_size=27)

    # ---- Footer ----
    foot = ("Six stories from Wednesday 25 November 2026  •  "
            "Hormuz, Saudi oil, Ukraine, Huawei, markets and space  •  "
            "The World in One Page")
    fw = d.textlength(foot, font=load(SANS_R, 17))
    d.text(((PAGE - fw) / 2, 962), foot, font=load(SANS_R, 17),
           fill=(90, 84, 70))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
