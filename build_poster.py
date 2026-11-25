#!/usr/bin/env python3
"""Draw the news-image-20261125 poster: one 1024x1024 cartoon front page.

Layout: cherry-red masthead, Nvidia lead story (generated flat-vector hero
beside a navy lead panel), four rounded cards for the other stories, footer
with the date and sources. The output is deterministic: fixed fonts, fixed
geometry, no timestamps, no randomness.
"""

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
HERO = ROOT / "hero-huawei.png"
OUT = HERE / "entry.png"

W, H = 1024, 1024
BG = (255, 246, 236)
RED = (210, 31, 60)
NAVY = (20, 38, 76)
GREEN = (74, 222, 128)
INK = (26, 32, 44)
GREY = (90, 96, 110)
WHITE = (255, 255, 255)
PALE = (255, 233, 214)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    path = FONT_DIR / name
    if not path.exists():
        raise SystemExit(f"missing font: {path}")
    return ImageFont.truetype(str(path), size)


BOLD = "DejaVuSans-Bold.ttf"
PLAIN = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels, word by word."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt_name, start_size, max_w):
    """Largest bold size at or below start_size that fits max_w."""
    size = start_size
    while size > 10:
        fnt = font(fnt_name, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 2
    return font(fnt_name, 10)


def rounded(canvas, box, radius, fill):
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(box, radius=radius, fill=fill)
    return draw


def paste_hero(canvas, hero_path, box):
    """Paste the hero image into box, keeping its aspect, corners rounded."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    hero = Image.open(hero_path).convert("RGB")
    scale = max(bw / hero.width, bh / hero.height)
    nw, nh = round(hero.width * scale), round(hero.height * scale)
    hero = hero.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - bw) // 2, (nh - bh) // 2
    hero = hero.crop((left, top, left + bw, top + bh))
    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw, bh], radius=18, fill=255)
    canvas.paste(hero, (x0, y0), mask)


def card(draw, x, y, w, h, accent, kicker, headline, body):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=WHITE)
    draw.rounded_rectangle([x, y, x + w, y + 10], radius=5, fill=accent)
    draw.rectangle([x, y + 5, x + w, y + 10], fill=accent)
    pad = 24
    inner = w - 2 * pad
    ky = y + 26
    draw.text((x + pad, ky), kicker, font=font(BOLD, 16), fill=accent)
    head_f = font(BOLD, 25)
    lines = wrap(draw, headline, head_f, inner)
    if len(lines) > 2:
        raise SystemExit(f"headline too long for card: {headline!r}")
    hy = ky + 28
    for line in lines[:2]:
        draw.text((x + pad, hy), line, font=head_f, fill=INK)
        hy += 31
    body_f = font(PLAIN, 18)
    blines = wrap(draw, body, body_f, inner)
    if len(blines) > 3:
        raise SystemExit(f"body too long for card: {body!r}")
    by = hy + 8
    for line in blines[:3]:
        draw.text((x + pad, by), line, font=body_f, fill=GREY)
        by += 25


def main():
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # Masthead.
    draw.rectangle([0, 0, W, 108], fill=RED)
    title_f = font(BOLD, 72)
    draw.text((W / 2, 6), "WORLD NEWS", font=title_f, fill=WHITE, anchor="ma")
    date_f = font(BOLD, 23)
    draw.text(
        (W / 2, 78),
        "WEDNESDAY \u00b7 25 NOVEMBER 2026",
        font=date_f,
        fill=PALE,
        anchor="ma",
    )

    # Lead row: hero left, navy panel right.
    row_y, row_h = 124, 338
    hero_w = 470
    hero_h = round(hero_w * 2 / 3)
    paste_hero(
        canvas,
        HERO,
        (24, row_y + (row_h - hero_h) // 2, 24 + hero_w,
         row_y + (row_h - hero_h) // 2 + hero_h),
    )
    panel = (510, row_y, 1000, row_y + row_h)
    draw.rounded_rectangle(panel, radius=18, fill=NAVY)
    px, pw = panel[0] + 28, panel[2] - panel[0] - 56
    draw.text((px, row_y + 22), "THE LEAD \u2014 HUAWEI", font=font(BOLD, 18),
              fill=GREEN)
    head_f = fit(draw, "GUILTY ON 10", BOLD, 54, pw)
    draw.text((px, row_y + 52), "GUILTY ON 10", font=head_f, fill=WHITE)
    draw.line([(px, row_y + 122), (px + 64, row_y + 122)], fill=GREEN, width=5)
    sub_f = font(PLAIN, 23)
    sub = ("A U.S. jury convicts Huawei on 10 of 12 counts \u2014 "
           "bank fraud, wire fraud, sanctions breaches and "
           "trade-secret theft. Sentencing next September.")
    sy = row_y + 142
    for line in wrap(draw, sub, sub_f, pw):
        draw.text((px, sy), line, font=sub_f, fill=WHITE)
        sy += 31
    tag = "10 OF 12 COUNTS \u00b7 2018 CASE"
    tag_f = fit(draw, tag, BOLD, 16, pw)
    draw.text((px, row_y + row_h - 40), tag, font=tag_f, fill=GREEN)

    # Four story cards, 2 x 2.
    cw, ch = 478, 238
    stories = [
        ((198, 44, 62), "CHINA \u00b7 POLITICS",
         "Shanghai chief Chen Jining probed",
         "Beijing says the Politburo member faces a graft probe, "
         "the fourth Politburo member investigated since 2025."),
        ((24, 110, 196), "UNITED STATES \u00b7 CYBER",
         "CIA and spy chief's office hacked",
         "Hackers hit unclassified open-source systems, CNN says. "
         "Officials say no classified data was affected."),
        ((214, 110, 20), "CHINA \u00b7 AVIATION",
         "Xiamen Air buys 50 Boeing 737-8s",
         "List price about $7.4bn, deliveries 2031-2034. First big "
         "Chinese Boeing order since 2017."),
        ((13, 140, 130), "SAUDI ARABIA",
         "Riyadh tower hit again, 11 hurt",
         "The 385m PIF tower is struck a second time in a week. "
         "At least two are seriously hurt, civil defence says."),
    ]
    positions = [(24, 478), (522, 478), (24, 732), (522, 732)]
    for (accent, kicker, headline, body), (cx, cy) in zip(stories, positions):
        card(draw, cx, cy, cw, ch, accent, kicker, headline, body)

    # Footer: shrink until it fits the full width.
    foot_text = ("25 NOVEMBER 2026 \u00b7 SOURCES: REUTERS \u00b7 CNN "
                 "\u00b7 AIRWAYS MAGAZINE \u00b7 AL JAZEERA")
    foot_f = fit(draw, foot_text, PLAIN, 16, W - 32)
    draw.text((W / 2, 988), foot_text, font=foot_f, fill=GREY, anchor="ma")

    canvas.save(OUT, optimize=True)
    data = OUT.read_bytes()
    print(f"wrote {OUT}  {len(data)} bytes  "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
