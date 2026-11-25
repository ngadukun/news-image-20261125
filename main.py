#!/usr/bin/env python3
"""Render a one-image newspaper front page summing up world news on
Wednesday 25 November 2026. Pure Pillow, no network, no external assets:
every glyph, rule and illustration is drawn from code with DejaVu fonts.
Run:  python3 main.py   ->  writes entry.png (1240 x 1754, portrait).
"""

import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1240, 1754
PAPER = (253, 250, 243)
INK = (17, 17, 17)
GREY = (90, 88, 82)
RED = (178, 34, 34)
BLUE = (18, 64, 118)
GREEN = (34, 120, 60)
MIDLINE = (200, 194, 178)

FDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + os.sep


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


SERIF = "DejaVuSerif-Bold.ttf"
SERIF_R = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

M = 64  # page margin
RIGHT = W - M


def rule(y, w=3, color=INK, x0=M, x1=RIGHT):
    d.line([(x0, y), (x1, y)], fill=color, width=w)


def wrap(text, f, width_px):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width_px:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(text, f, x, y, width_px, leading=6, color=INK):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(text, f, width_px):
        d.text((x, y), line, font=f, fill=color)
        y += f.size + leading
    return y


def kicker(text, x, y, color=RED, size=26):
    f = font(SANS_B, size)
    d.text((x, y), text.upper(), font=f, fill=color)
    return y + size + 8


# ---------------------------------------------------------------- top strip
d.rectangle([0, 0, W, 46], fill=INK)
f_small = font(SANS_B, 20)
d.text((M, 12), "WEDNESDAY 25 NOVEMBER 2026", font=f_small, fill=PAPER)
tag = "ONE WORLD  •  ONE PAGE"
tw = d.textlength(tag, font=f_small)
d.text((RIGHT - tw, 12), tag, font=f_small, fill=PAPER)

# ---------------------------------------------------------------- masthead
y = 70
f_mast = font(SERIF, 104)
title = "THE WORLD TODAY"
tw = d.textlength(title, font=f_mast)
d.text(((W - tw) / 2, y), title, font=f_mast, fill=INK)
y += 122
f_tag = font(SERIF_R, 28)
sub = "All the news that matters — in a single image"
tw = d.textlength(sub, font=f_tag)
d.text(((W - tw) / 2, y), sub, font=f_tag, fill=GREY)
y += 48
rule(y, 6)
y += 10
rule(y, 2)
y += 16
f_date = font(SANS_B, 23)
note = "INTERNATIONAL DAY FOR THE ELIMINATION OF VIOLENCE AGAINST WOMEN"
tw = d.textlength(note, font=f_date)
d.text(((W - tw) / 2, y), note, font=f_date, fill=RED)
y += 42
rule(y, 2)

# ---------------------------------------------------------------- lead story
y += 24
y = kicker("Lead story  —  Middle East", M, y, color=RED, size=26)
f_lead = font(SERIF, 58)
lead_head = "Houthi drone strikes Riyadh tower — 11 wounded"
y = para(lead_head, f_lead, M, y, RIGHT - M, leading=8)
y += 8
f_body = font(SANS, 27)
lead_body = (
    "Yemen's Houthi rebels struck the PIF Tower in Saudi Arabia's capital, "
    "Riyadh, for the second time in less than a week on Tuesday, wounding at "
    "least 11 people, Saudi Civil Defense said. The UAE condemned the attack."
)
y = para(lead_body, f_body, M, y, RIGHT - M, leading=7)
y += 16

# Drawn illustration: Riyadh skyline at dusk with the tower and smoke.
ILL_H = 210
ill_x0, ill_y0 = M, y
ill_x1, ill_y1 = RIGHT, y + ILL_H
d.rectangle([ill_x0, ill_y0, ill_x1, ill_y1], fill=(24, 32, 58))
for i in range(6):
    band = (24 + i * 6, 32 + i * 5, 58 + i * 8)
    d.rectangle([ill_x0, ill_y0 + i * ILL_H // 6, ill_x1,
                 ill_y0 + (i + 1) * ILL_H // 6], fill=band)
d.ellipse([ill_x1 - 180, ill_y0 + 26, ill_x1 - 108, ill_y0 + 98],
          fill=(232, 170, 80))
random.seed(25)
base = ill_y1
x = ill_x0 + 8
while x < ill_x1 - 30:
    bw = random.randint(46, 92)
    bh = random.randint(60, 140)
    d.rectangle([x, base - bh, x + bw, base], fill=(12, 16, 34))
    for wy in range(base - bh + 12, base - 14, 26):
        for wx in range(x + 8, x + bw - 10, 18):
            if random.random() < 0.45:
                d.rectangle([wx, wy, wx + 7, wy + 10], fill=(240, 200, 110))
    x += bw + 10
# the tall PIF tower, centre-right, with a smoke plume above its tip
tx0, tx1 = 700, 788
d.rectangle([tx0, ill_y0 + 46, tx1, base], fill=(8, 10, 26))
d.polygon([(tx0, ill_y0 + 46), ((tx0 + tx1) // 2, ill_y0 + 8),
           (tx1, ill_y0 + 46)], fill=(8, 10, 26))
for wy in range(ill_y0 + 62, base - 12, 24):
    d.rectangle([tx0 + 12, wy, tx1 - 12, wy + 9], fill=(250, 214, 130))
for (sx, sy, sr) in [(700, ill_y0 + 16, 18), (668, ill_y0 + 34, 22),
                      (700, ill_y0 + 48, 24), (664, ill_y0 + 62, 18)]:
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(210, 205, 195))
d.text((ill_x0 + 14, ill_y1 - 32), "ILLUSTRATION: THE RIYADH SKYLINE",
       font=font(SANS_B, 18), fill=(255, 255, 255))
y = ill_y1 + 22
rule(y, 2)

# ------------------------------------------------------- secondary stories
y += 22
STORIES = [
    ("WORLD  •  UKRAINE", RED,
     "Kyiv confirms strike on Russian ship",
     "President Volodymyr Zelenskiy confirmed Ukraine was behind Saturday's "
     "drone strike on a Russian cargo ship in the Gulf of Finland. Ally Norway "
     "urged Kyiv to exercise caution in such operations."),
    ("TECH  •  UNITED STATES", BLUE,
     "CIA and spy chief's office hit by cyber breach",
     "The CIA and the Office of the Director of National Intelligence suffered "
     "a cybersecurity breach involving some unclassified information, sources "
     "told Reuters on Tuesday. It is the latest in a run of US government and "
     "private-sector breaches."),
    ("TECH  •  CHINA", BLUE,
     "Huawei convicted in US trial over trade secrets",
     "A federal jury in New York found Huawei guilty on 10 of 12 criminal "
     "counts, including conspiracy to steal trade secrets and bank fraud, after "
     "a trial lasting more than two months. Huawei rejected the verdicts."),
    ("POLITICS  •  UNITED STATES", RED,
     "Trump awards Giuliani the Medal of Freedom",
     "President Donald Trump awarded former New York City mayor Rudy Giuliani "
     "the Presidential Medal of Freedom on Tuesday, the nation's highest "
     "civilian honour, after pardoning him over efforts to overturn the 2020 "
     "election."),
    ("SPACE  •  CHINA", BLUE,
     "Shenzhou 24 launches with three astronauts",
     "China launched the Shenzhou 24 spacecraft carrying two Chinese astronauts "
     "and a Pakistani astronaut, the latest crewed mission in its space "
     "programme."),
    ("SPORT  •  CRICKET", GREEN,
     "England level T20 series against Australia",
     "England beat Australia by eight wickets in the second T20 International, "
     "chasing 185 to level the five-match series 1-1. Jake Fraser-McGurk hit "
     "27 off 13 balls for the hosts."),
]

f_sec = font(SANS_B, 21)
f_head = font(SERIF, 30)
f_txt = font(SANS, 22)
col_w = (RIGHT - M - 36) // 2
col_x = [M, M + col_w + 36]

i = 0
while i < len(STORIES):
    row_top = y
    ends = []
    for col in (0, 1):
        if i + col >= len(STORIES):
            break
        tag, color, head, body = STORIES[i + col]
        x = col_x[col]
        yy = row_top
        d.text((x, yy), tag, font=f_sec, fill=color)
        yy += 30
        yy = para(head, f_head, x, yy, col_w, leading=4)
        yy += 4
        yy = para(body, f_txt, x, yy, col_w, leading=5)
        ends.append(yy)
    y = max(ends) + 20
    # vertical divider between the two columns for this row
    d.line([(M + col_w + 18, row_top), (M + col_w + 18, y - 12)],
           fill=MIDLINE, width=2)
    if i + 2 < len(STORIES):
        rule(y - 8, 1, color=MIDLINE)
    i += 2

# ------------------------------------------------------------------- footer
rule(y, 6)
y += 12
f_foot = font(SANS, 21)
foot = ("Sources: Reuters, CNN, AFP, BBC, The Washington Post — stories "
        "published 24–25 November 2026. Rendered entirely in code; "
        "no photographs used.")
y = para(foot, f_foot, M, y, RIGHT - M, leading=5)
y += 8
f_end = font(SANS_B, 21)
end = "THE WORLD TODAY  •  25 NOVEMBER 2026  •  END OF FRONT PAGE"
tw = d.textlength(end, font=f_end)
d.text(((W - tw) / 2, y), end, font=f_end, fill=GREY)
print("footer baseline y =", y, "page height =", H)

img.save("entry.png")
print("saved entry.png", img.size)
