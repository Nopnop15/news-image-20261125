#!/usr/bin/env python3
"""Draw the 25 November 2026 front page: a masthead, a hero rocket story,
and five more news panels, all rendered with Pillow from scratch."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 30)
NAVY = (22, 38, 74)
GOLD = (232, 193, 90)
RED = (178, 34, 34)
TEAL = (38, 110, 104)
BLUE = (31, 58, 147)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, f, fill, leading):
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def star_circle(d, cx, cy, r, n, sr, fill):
    import math
    for i in range(n):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        star(d, cx + r * math.cos(ang), cy + r * math.sin(ang), sr, fill)


def panel(d, x, y, w, h, kicker, headline, subline, accent, head_size=25):
    """A white card: drawn scene on top, kicker + headline + subline below."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=(180, 172, 150), width=2)
    scene_h = 108
    return x, y, w, h, scene_h, kicker, headline, subline, accent, head_size


def panel_text(d, x, y, w, h, scene_h, kicker, headline, subline, accent,
               head_size=25):
    tx = x + 14
    tw = w - 28
    ty = y + scene_h + 10
    d.text((tx, ty), kicker, font=font(SANS_B, 15), fill=accent)
    ty += 24
    hl = wrap(d, headline, font(SERIF, head_size), tw)
    ty = text_block(d, tx, ty, hl, font(SERIF, head_size), INK, head_size + 4)
    ty += 4
    sl = wrap(d, subline, font(SANS, 16), tw)
    text_block(d, tx, ty, sl, font(SANS, 16), (70, 70, 76), 21)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=font(SERIF, 46))
    d.text(((W - tw) / 2, 14), title, font=font(SERIF, 46), fill=(255, 255, 255))
    date = "WEDNESDAY 25 NOVEMBER 2026"
    dw = d.textlength(date, font=font(SANS_B, 27))
    d.text(((W - dw) / 2, 72), date, font=font(SANS_B, 27), fill=GOLD)

    # ---- Hero: Shenzhou-24 launch ----
    hx, hy, hw, hh = 24, 134, 976, 276
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(255, 255, 255),
                outline=(180, 172, 150), width=2)
    # Sky scene on the left half.
    sx, sy, sw, sh = hx + 2, hy + 2, 520, hh - 4
    for i in range(sh):
        t = i / sh
        d.line([(sx, sy + i), (sx + sw, sy + i)],
               fill=(int(16 + 30 * t), int(28 + 46 * t), int(66 + 74 * t)))
    for (px, py, r) in [(40, 30, 2), (120, 70, 2), (200, 25, 3), (300, 60, 2),
                        (420, 35, 2), (500, 80, 3), (80, 120, 2), (260, 110, 2),
                        (470, 130, 2), (160, 150, 2), (350, 150, 2)]:
        d.ellipse([sx + px - r, sy + py - r, sx + px + r, sy + py + r],
                  fill=(255, 255, 255))
    # Ground and launch pad.
    d.rectangle([sx, sy + sh - 34, sx + sw, sy + sh], fill=(52, 48, 44))
    d.rectangle([sx + 210, sy + sh - 52, sx + 350, sy + sh - 34], fill=(120, 116, 110))
    # Rocket body.
    rx, ry = sx + 250, sy + 42
    d.polygon([(rx, ry), (rx + 60, ry), (rx + 60, ry + 150), (rx, ry + 150)],
              fill=(240, 240, 235))
    d.pieslice([rx, ry - 34, rx + 60, ry + 34], 180, 360, fill=(200, 40, 40))
    d.rectangle([rx, ry + 60, rx + 60, ry + 82], fill=(200, 40, 40))
    d.text((rx + 22, ry + 95), "24", font=font(SANS_B, 26), fill=NAVY)
    d.polygon([(rx - 26, ry + 150), (rx, ry + 96), (rx, ry + 150)], fill=(200, 40, 40))
    d.polygon([(rx + 60, ry + 150), (rx + 60, ry + 96), (rx + 86, ry + 150)],
              fill=(200, 40, 40))
    # Flame and smoke.
    d.polygon([(rx + 12, ry + 150), (rx + 48, ry + 150), (rx + 30, ry + 208)],
              fill=(255, 140, 0))
    d.polygon([(rx + 20, ry + 150), (rx + 40, ry + 150), (rx + 30, ry + 186)],
              fill=(255, 220, 80))
    for (cx, cy, cr) in [(150, 235, 26), (200, 246, 32), (420, 238, 26),
                         (470, 248, 30), (120, 252, 20), (500, 252, 20)]:
        d.ellipse([sx + cx - cr, sy + cy - cr // 2, sx + cx + cr,
                   sy + cy + cr // 2], fill=(210, 205, 195))
    # Hero text on the right.
    tx, tw = hx + 544, hw - 568
    d.text((tx, hy + 22), "SPACE  •  CHINA", font=font(SANS_B, 18), fill=RED)
    hl = wrap(d, "SHENZHOU-24 LAUNCHES", font(SERIF, 40), tw)
    ty = text_block(d, tx, hy + 52, hl, font(SERIF, 40), INK, 46)
    sub = ("Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali — the first "
           "Pakistani in orbit — head to Tiangong.")
    sl = wrap(d, sub, font(SANS, 20), tw)
    ty = text_block(d, tx, ty + 10, sl, font(SANS, 20), (70, 70, 76), 26)
    d.text((tx, ty + 12), "Lift-off 08:18 Beijing time, Jiuquan.",
           font=font(SERIF_REG, 18), fill=(90, 90, 96))

    # ---- Row 1: three panels ----
    row1_y, row1_h, pw = 424, 262, 312
    xs = [24, 356, 688]

    # EU sanctions: blue field, circle of gold stars, bank building, red slash.
    x = xs[0]
    panel(d, x, row1_y, pw, row1_h, "", "", "", BLUE)
    d.rectangle([x + 2, row1_y + 2, x + pw - 2, row1_y + 98], fill=BLUE)
    star_circle(d, x + 156, row1_y + 50, 40, 12, 7, GOLD)
    d.rectangle([x + 128, row1_y + 42, x + 184, row1_y + 48], fill=(255, 255, 255))
    d.polygon([(x + 122, row1_y + 44), (x + 156, row1_y + 26),
               (x + 190, row1_y + 44)], fill=(255, 255, 255))
    for cx in (136, 149, 162, 175):
        d.rectangle([cx, row1_y + 50, cx + 6, row1_y + 72], fill=(255, 255, 255))
    d.rectangle([x + 124, row1_y + 72, x + 188, row1_y + 78], fill=(255, 255, 255))
    d.line([(x + 128, row1_y + 84), (x + 184, row1_y + 28)], fill=RED, width=7)
    panel_text(d, x, row1_y, pw, row1_h, 96, "EUROPE  •  RUSSIA",
               "EU SANCTIONS RUSSIA",
               "Brussels proposes a broad package on banks, "
               "crypto and sport.",
               BLUE, head_size=23)

    # CIA / ODNI hacked: dark screen, warning triangle, binary rain.
    x = xs[1]
    panel(d, x, row1_y, pw, row1_h, "", "", "", (20, 24, 40))
    d.rectangle([x + 2, row1_y + 2, x + pw - 2, row1_y + 98], fill=(20, 24, 40))
    for (bx, by) in [(20, 16), (60, 44), (250, 20), (280, 60), (30, 80), (270, 88)]:
        d.text((x + bx, row1_y + by), "01", font=font(SANS_B, 13), fill=(70, 90, 120))
    d.rectangle([x + 96, row1_y + 18, x + 216, row1_y + 92], outline=(120, 130, 150),
                width=3)
    d.polygon([(x + 156, row1_y + 30), (x + 196, row1_y + 80), (x + 116, row1_y + 80)],
              fill=(255, 200, 40))
    d.text((x + 150, row1_y + 50), "!", font=font(SANS_B, 30), fill=(20, 24, 40))
    panel_text(d, x, row1_y, pw, row1_h, 96, "UNITED STATES  •  CYBER",
               "CIA AND ODNI HACKED",
               "A cyberattack hits unclassified systems at the "
               "CIA and ODNI.",
               (20, 24, 40), head_size=23)

    # Australia–Solomons pact: teal sea, two landmasses, dashed link.
    x = xs[2]
    panel(d, x, row1_y, pw, row1_h, "", "", "", TEAL)
    d.rectangle([x + 2, row1_y + 2, x + pw - 2, row1_y + 98], fill=(46, 126, 120))
    d.ellipse([x + 28, row1_y + 58, x + 118, row1_y + 94], fill=(214, 164, 90))
    d.ellipse([x + 210, row1_y + 22, x + 268, row1_y + 54], fill=(120, 190, 110))
    for i in range(7):
        t = i / 6
        px = x + 120 + t * 92
        py = row1_y + 66 - 26 * (1 - (2 * t - 1) ** 2)
        if i % 2 == 0:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    d.polygon([(x + 156, row1_y + 30), (x + 166, row1_y + 20), (x + 176, row1_y + 30),
               (x + 176, row1_y + 48), (x + 166, row1_y + 58), (x + 156, row1_y + 48)],
              fill=GOLD)
    panel_text(d, x, row1_y, pw, row1_h, 96, "PACIFIC  •  SECURITY",
               "AUSTRALIA–SOLOMONS PACT",
               "Canberra becomes the Solomons' primary security "
               "partner.",
               TEAL, head_size=23)

    # ---- Row 2: two wide panels ----
    row2_y, row2_h = 700, 244
    # Sanofi buys Insmed: capsule pill and $41bn.
    x, w2 = 24, 478
    panel(d, x, row2_y, w2, row2_h, "", "", "", (150, 30, 90))
    d.rectangle([x + 2, row2_y + 2, x + w2 - 2, row2_y + 100], fill=(238, 232, 222))
    d.rounded_rectangle([x + 40, row2_y + 30, x + 210, row2_y + 72], radius=21,
                        fill=(200, 40, 60))
    d.rounded_rectangle([x + 40, row2_y + 30, x + 125, row2_y + 72], radius=21,
                        fill=(255, 255, 255))
    d.ellipse([x + 150, row2_y + 42, x + 158, row2_y + 60], fill=(200, 40, 60))
    d.text((x + 250, row2_y + 26), "$41bn", font=font(SERIF, 46), fill=(150, 30, 90))
    panel_text(d, x, row2_y, w2, row2_h, 98, "BUSINESS  •  PHARMA",
               "SANOFI BUYS INSMED",
               "French drugmaker Sanofi agrees a $41 billion takeover "
               "of US biotech Insmed.",
               (150, 30, 90), head_size=27)

    # Rial at record low: falling chart and banknote.
    x = 522
    panel(d, x, row2_y, w2, row2_h, "", "", "", RED)
    d.rectangle([x + 2, row2_y + 2, x + w2 - 2, row2_y + 100], fill=(250, 244, 230))
    d.rectangle([x + 30, row2_y + 22, x + 130, row2_y + 78], fill=(140, 190, 120),
                outline=(90, 130, 80), width=2)
    d.ellipse([x + 66, row2_y + 38, x + 94, row2_y + 62], outline=(255, 255, 255),
              width=3)
    pts = [(150, 30), (210, 42), (270, 38), (330, 58), (390, 74), (440, 88)]
    pts = [(x + px, row2_y + py) for (px, py) in pts]
    d.line(pts, fill=RED, width=5)
    d.polygon([(x + 440, row2_y + 88), (x + 424, row2_y + 82),
               (x + 440, row2_y + 70)], fill=RED)
    panel_text(d, x, row2_y, w2, row2_h, 98, "IRAN  •  ECONOMY",
               "RIAL AT RECORD LOW",
               "Iran's currency sinks to 2.856 million per dollar "
               "after fresh US sanctions hit its banks.",
               RED, head_size=27)

    # ---- Footer ----
    foot = ("Six stories from Wednesday 25 November 2026  •  "
            "Space, sanctions, cyber, security, pharma and markets  •  "
            "The World in One Page")
    fw = d.textlength(foot, font=font(SANS, 17))
    d.text(((W - fw) / 2, 962), foot, font=font(SANS, 17), fill=(90, 84, 70))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
