#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news summary image (1024x1024 PNG).

Deterministic: fixed data, fixed fonts, fixed geometry, no timestamps,
no randomness, no network. Running this script twice produces byte-identical
output (PIL's PNG encoder embeds no time data).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"

PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
NAVY2 = (28, 48, 88)
GOLD = (217, 164, 65)
RED = (178, 44, 36)
RED_LT = (251, 233, 228)
GREY = (90, 90, 86)
CARD = (255, 255, 255)
GREEN = (34, 139, 80)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for i, ln in enumerate(lines):
        draw.text((x, y + i * leading), ln, font=fnt, fill=fill)
    return y + len(lines) * leading


def starburst(draw, cx, cy, r_out, r_in, n, fill):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_skyline(draw, x0, y0, x1, y1, color, accent=None):
    """Simple city skyline silhouette inside the given box."""
    base = y1
    towers = [
        (0.00, 0.55, 0.10), (0.11, 0.38, 0.09), (0.21, 0.62, 0.11),
        (0.33, 0.28, 0.10), (0.44, 0.50, 0.09), (0.54, 0.34, 0.10),
        (0.65, 0.58, 0.09), (0.75, 0.42, 0.11), (0.87, 0.60, 0.10),
    ]
    wbox = x1 - x0
    for fx, fh, fw in towers:
        tx = x0 + fx * wbox
        tw = fw * wbox
        th = fh * (y1 - y0)
        draw.rectangle([tx, base - th, tx + tw, base], fill=color)
        # tiny lit windows
        for wy in range(int(base - th + 8), int(base - 6), 16):
            for wx in range(int(tx + 5), int(tx + tw - 4), 12):
                if (int(wx) + int(wy)) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 3, wy + 5], fill=GOLD)
    if accent is not None:
        # explosion burst over the tallest tower (index 3)
        tx = x0 + 0.33 * wbox
        tw = 0.10 * wbox
        cx, cy = tx + tw / 2, y0 + 0.28 * (y1 - y0) - 18
        starburst(draw, cx, cy, 52, 24, 10, (232, 126, 32))
        starburst(draw, cx, cy, 34, 16, 10, (245, 196, 66))
        starburst(draw, cx, cy, 18, 9, 8, (255, 240, 180))
        # smoke puffs
        for sx, sy, sr in [(cx - 46, cy - 30, 13), (cx + 40, cy - 42, 16),
                           (cx + 58, cy - 12, 11), (cx - 60, cy - 6, 9)]:
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 118))


def draw_tanker(draw, x0, y0, x1, y1):
    """Oil tanker on waves with a flame."""
    sea_y = y0 + int((y1 - y0) * 0.62)
    draw.rectangle([x0, sea_y, x1, y1], fill=(31, 78, 121))
    for k in range(4):
        wx = x0 + 12 + k * ((x1 - x0 - 24) // 4)
        draw.arc([wx, sea_y + 6, wx + 34, sea_y + 22], 0, 180, fill=(160, 200, 230), width=3)
    # hull
    hx0, hx1 = x0 + 18, x1 - 18
    hy0, hy1 = sea_y - 26, sea_y + 14
    draw.polygon([(hx0, hy0), (hx1, hy0), (hx1 - 14, hy1), (hx0 + 22, hy1)], fill=(60, 60, 64))
    draw.rectangle([hx0, hy0 - 16, hx0 + 46, hy0], fill=(200, 200, 200))
    draw.rectangle([hx0 + 8, hy0 - 30, hx0 + 26, hy0 - 16], fill=(200, 200, 200))
    # containers
    for i, c in enumerate([(178, 44, 36), (217, 164, 65), (34, 139, 80)]):
        cx0 = hx0 + 56 + i * 52
        draw.rectangle([cx0, hy0 - 14, cx0 + 46, hy0], fill=c)
    # flame on the deck (kept short so it stays inside the icon zone)
    fx = hx1 - 66
    fy = hy0 - 14
    draw.polygon([(fx - 10, fy), (fx - 3, fy - 16), (fx + 2, fy - 7),
                  (fx + 7, fy - 19), (fx + 13, fy - 4), (fx + 6, fy)],
                 fill=(232, 126, 32))
    draw.polygon([(fx - 4, fy), (fx, fy - 10), (fx + 6, fy)], fill=(245, 196, 66))


def draw_wall(draw, x0, y0, x1, y1):
    """Stylised red gate / Great Wall crenellation."""
    draw.rectangle([x0, y0 + 34, x1, y1 - 10], fill=(178, 44, 36))
    # crenellations
    for i in range(6):
        cx0 = x0 + 8 + i * ((x1 - x0 - 16) // 6)
        draw.rectangle([cx0, y0 + 18, cx0 + 16, y0 + 34], fill=(178, 44, 36))
    # gold roof line + star
    draw.rectangle([x0, y0 + 30, x1, y0 + 38], fill=GOLD)
    starburst(draw, (x0 + x1) // 2, y0 + 62, 16, 7, 5, GOLD)
    # columns
    for i in range(4):
        cx0 = x0 + 26 + i * ((x1 - x0 - 52) // 4)
        draw.rectangle([cx0, y0 + 78, cx0 + 12, y1 - 10], fill=(120, 28, 22))
    draw.rectangle([x0 + 14, y1 - 22, x1 - 14, y1 - 10], fill=(120, 28, 22))


def draw_chip(draw, x0, y0, x1, y1, body=(30, 30, 34), accent=GOLD):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    s = min(x1 - x0, y1 - y0) - 24
    bx0, by0, bx1, by1 = cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2
    # pins
    for i in range(5):
        off = -s // 2 + 8 + i * ((s - 16) // 4)
        draw.line([cx + off, by0 - 12, cx + off, by0], fill=accent, width=4)
        draw.line([cx + off, by1, cx + off, by1 + 12], fill=accent, width=4)
        draw.line([bx0 - 12, cy + off, bx0, cy + off], fill=accent, width=4)
        draw.line([bx1, cy + off, bx1 + 12, cy + off], fill=accent, width=4)
    draw.rectangle([bx0, by0, bx1, by1], fill=body, outline=accent, width=3)
    draw.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], fill=accent)
    draw.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], fill=body)


def draw_rocket(draw, x0, y0, x1, y1):
    cx = (x0 + x1) // 2
    # stars
    for sx, sy, sr in [(x0 + 16, y0 + 14, 3), (x1 - 22, y0 + 30, 2),
                       (x0 + 34, y0 + 56, 2), (x1 - 40, y0 + 8, 3)]:
        starburst(draw, sx, sy, sr + 2, sr // 2 + 1, 5, GOLD)
    # body
    bx0, bx1 = cx - 16, cx + 16
    by0, by1 = y0 + 8, y1 - 34
    draw.polygon([(cx, by0), (bx1, by0 + 22), (bx1, by1), (bx0, by1),
                  (bx0, by0 + 22)], fill=(225, 225, 228))
    draw.polygon([(cx, by0), (bx1, by0 + 22), (bx0, by0 + 22)], fill=RED)
    draw.ellipse([cx - 8, by0 + 26, cx + 8, by0 + 42], fill=(31, 78, 121))
    draw.polygon([(bx0, by1 - 18), (bx0 - 14, by1 + 6), (bx0, by1)], fill=RED)
    draw.polygon([(bx1, by1 - 18), (bx1 + 14, by1 + 6), (bx1, by1)], fill=RED)
    # flame
    draw.polygon([(cx - 10, by1), (cx, by1 + 26), (cx + 10, by1)], fill=(232, 126, 32))
    draw.polygon([(cx - 5, by1), (cx, by1 + 15), (cx + 5, by1)], fill=(245, 196, 66))
    # ground line
    draw.line([x0 + 10, y1 - 4, x1 - 10, y1 - 4], fill=GREY, width=2)


def draw_graph(draw, x0, y0, x1, y1):
    pts = [(x0 + 10, y1 - 30), (x0 + 46, y1 - 52), (x0 + 82, y1 - 40),
           (x0 + 118, y1 - 66), (x0 + 154, y1 - 48), (x0 + 190, y1 - 78)]
    draw.line(pts, fill=GREEN, width=5, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=GREEN)
    # arrow head at the top
    ex, ey = pts[-1]
    draw.polygon([(ex, ey - 14), (ex + 16, ey - 2), (ex + 2, ey + 2)], fill=GREEN)
    # dashed baseline
    for dx in range(x0 + 10, x1 - 10, 14):
        draw.line([dx, y1 - 12, dx + 8, y1 - 12], fill=GREY, width=2)
    # small chip
    draw.rectangle([x0 + 14, y0 + 6, x0 + 44, y0 + 30], fill=(30, 30, 34))
    draw.rectangle([x0 + 22, y0 + 12, x0 + 36, y0 + 24], fill=GREEN)


def draw_city_smoke(draw, x0, y0, x1, y1):
    draw_skyline(draw, x0, y0 + 18, x1, y1 - 6, (70, 70, 74), accent=None)
    # smoke plume over the middle
    cx = (x0 + x1) // 2
    for sx, sy, sr in [(cx - 30, y0 + 26, 12), (cx - 8, y0 + 12, 15),
                       (cx + 18, y0 + 24, 11), (cx + 34, y0 + 40, 8)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(130, 130, 128))
    draw.ellipse([cx - 6, y0 + 34, cx + 6, y0 + 46], fill=(232, 126, 32))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.rectangle([0, 112, W, 116], fill=GOLD)
    d.text((24, 30), "THE WORLD IN ONE DAY", font=font(SERIF_B, 44), fill=(255, 255, 255))
    d.text((24, 84), "WORLD NEWS  •  SUMMED UP IN A SINGLE PICTURE",
           font=font(SANS_B, 15), fill=GOLD)
    d.text((W - 24, 32), "WEDNESDAY", font=font(SANS_B, 26), fill=(255, 255, 255), anchor="ra")
    d.text((W - 24, 66), "25 NOVEMBER 2026", font=font(SANS_B, 26), fill=GOLD, anchor="ra")

    # ---- tagline ----
    d.text((W // 2, 128), "Seven stories that defined the day — as reported on 25 November 2026",
           font=font(SANS, 17), fill=GREY, anchor="ma")

    # ---- lead story: Riyadh ----
    lx0, ly0, lx1, ly1 = 16, 152, 1008, 396
    d.rectangle([lx0, ly0, lx1, ly1], fill=CARD, outline=(200, 192, 176), width=2)
    d.rectangle([lx0, ly0, lx1, ly0 + 6], fill=RED)
    d.text((36, ly0 + 20), "MIDDLE EAST  •  LEAD STORY", font=font(SANS_B, 17), fill=RED)
    head = wrap(d, "Houthi missile hits Riyadh's tallest tower — again",
                font(SANS_B, 36), 600)
    text_block(d, 36, ly0 + 48, head, font(SANS_B, 36), INK, 42)
    sub = wrap(d, "Eleven people hurt as a second strike in under a week hits the "
                  "King Abdullah Financial District. The US warns of more Houthi "
                  "attacks across the region.",
               font(SANS, 19), 600)
    text_block(d, 36, ly0 + 48 + len(head) * 42 + 8, sub, font(SANS, 19), (60, 60, 58), 25)
    # illustration: skyline with explosion
    draw_skyline(d, 668, ly0 + 26, 988, ly1 - 16, NAVY2, accent=True)

    # ---- grid of six stories ----
    stories = [
        ("STRAIT OF HORMUZ", (31, 78, 121),
         "Three oil tankers struck by mines in the Strait of Hormuz",
         "Iran says the tankers caught fire after hitting naval mines in the "
         "world's busiest oil chokepoint.", "tanker"),
        ("CHINA", RED,
         "Beijing opens corruption probe into Politburo member Chen Jining",
         "Shanghai's party chief, a future leadership contender, is probed "
         "for \u201csevere violations of discipline\u201d.", "wall"),
        ("UNITED STATES", (40, 40, 46),
         "US jury convicts Huawei of stealing trade secrets",
         "The Chinese tech giant is found guilty of conspiracy and bank fraud "
         "over its Iran business.", "chip"),
        ("SPACE", NAVY2,
         "Shenzhou-24 carries Pakistan's first astronaut into orbit",
         "China launches a new crew to its space station — the first foreign "
         "astronaut aboard.", "rocket"),
        ("TECH  •  NVIDIA", (34, 120, 60),
         "Nvidia chief Huang: reinstated, in therapy, pardon floated",
         "A day after returning as CEO, Jensen Huang says he made \u201cterrible "
         "mistakes\u201d; Trump calls a pardon \u201calways an option\u201d.", "graph"),
        ("GAZA", (96, 96, 92),
         "Israeli strike kills Hamas security chief in Gaza City",
         "Naim Abu Nahal is killed despite the ceasefire in place since last "
         "year, officials say.", "city"),
    ]
    gx0, gy0 = 16, 408
    col_w, row_h, gap = 322, 282, 12
    for i, (kicker, color, headline, subtext, icon) in enumerate(stories):
        r, c = divmod(i, 3)
        x0 = gx0 + c * (col_w + gap)
        y0 = gy0 + r * (row_h + gap)
        x1, y1 = x0 + col_w, y0 + row_h
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=(200, 192, 176), width=2)
        d.rectangle([x0, y0, x1, y0 + 36], fill=color)
        d.text((x0 + 14, y0 + 9), kicker, font=font(SANS_B, 16), fill=(255, 255, 255))
        ix0, iy0, ix1, iy1 = x0 + 14, y0 + 44, x1 - 14, y0 + 132
        if icon == "tanker":
            draw_tanker(d, ix0, iy0, ix1, iy1)
        elif icon == "wall":
            draw_wall(d, ix0, iy0, ix1, iy1)
        elif icon == "chip":
            draw_chip(d, ix0, iy0, ix1, iy1)
        elif icon == "rocket":
            draw_rocket(d, ix0, iy0, ix1, iy1)
        elif icon == "graph":
            draw_graph(d, ix0, iy0, ix1, iy1)
        else:
            draw_city_smoke(d, ix0, iy0, ix1, iy1)
        hl = wrap(d, headline, font(SANS_B, 21), col_w - 28)
        hy = text_block(d, x0 + 14, y0 + 140, hl[:3], font(SANS_B, 21), INK, 25)
        sl = wrap(d, subtext, font(SANS, 15), col_w - 28)
        text_block(d, x0 + 14, hy + 6, sl[:3], font(SANS, 15), (60, 60, 58), 19)

    # ---- footer ----
    d.text((W // 2, 992), "Sources: South China Morning Post, The Hindu, The Economic Times, "
           "The Japan Times, Qatar Tribune — 25 November 2026",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG", optimize=False)


if __name__ == "__main__":
    main()
