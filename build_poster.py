#!/usr/bin/env python3
"""Draw the 25 November 2026 cartoon front page and save it as entry.png.

The page is a 1024x1024 newspaper front: a red masthead, a courtroom hero
photo on the left with a navy lead story on the right, four short news
cards in a 2x2 grid, and a footer line with the date and sources.

Everything is drawn from fixed coordinates, so running this script twice
produces the same bytes. The hero artwork comes from the upscaled render
in the parent directory (hero-huawei-x4.png); it is shrunk to the hero
box and centre-cropped vertically.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO_PATH = os.path.join(HERE, "..", "hero-huawei-x4.png")
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE = 1024
CREAM = (255, 246, 236)
PAPER = (255, 255, 255)
INK = (26, 32, 44)
GREY = (90, 96, 110)
MASTHEAD_RED = (210, 31, 60)
PEACH = (255, 233, 214)
NAVY = (20, 38, 76)
GREEN = (74, 222, 128)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(SANS_BOLD if bold else SANS, size)


def place(draw, x, y, text, size, color, bold=False):
    """Draw one left-aligned line; (x, y) is the top of the ascender box."""
    draw.text((x, y), text, font=font(size, bold), fill=color)


def centred(draw, cx, y, text, size, color, bold=False):
    """Draw one line centred on cx; y is the top of the ascender box."""
    f = font(size, bold)
    x = (PAGE - int(f.getlength(text))) // 2
    draw.text((x, y), text, font=f, fill=color)


def top_strip(draw, x, y, width, color):
    """A coloured band across the top of a card, rounded at the top only."""
    height = 11
    draw.rounded_rectangle((x, y, x + width, y + height - 1), radius=5, fill=color)
    # Square off the bottom corners of the band.
    draw.rectangle((x, y + 5, x + width, y + height - 1), fill=color)


def hero_picture():
    """Shrink the upscaled courtroom render and cut its middle band."""
    art = Image.open(HERO_PATH).convert("RGB")
    art = art.resize((470, 470), Image.LANCZOS)
    return art.crop((0, 78, 470, 391))


def build():
    page = Image.new("RGB", (PAGE, PAGE), CREAM)
    draw = ImageDraw.Draw(page)

    # --- Masthead -------------------------------------------------------
    draw.rectangle((0, 0, PAGE, 108), fill=MASTHEAD_RED)
    centred(draw, 512, 6, "WORLD NEWS", 72, PAPER, bold=True)
    centred(draw, 512, 78, "WEDNESDAY · 25 NOVEMBER 2026", 23, PEACH, bold=True)

    # --- Hero photo (left) and lead story (right) -----------------------
    photo = hero_picture()
    mask = Image.new("L", photo.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 470, 313), radius=18, fill=255)
    page.paste(photo, (24, 136), mask)

    draw.rounded_rectangle((510, 124, 1000, 462), radius=18, fill=NAVY)
    lead_x = 538
    place(draw, lead_x, 146, "THE LEAD — HUAWEI", 18, GREEN, bold=True)
    place(draw, lead_x, 176, "GUILTY ON 10", 54, PAPER, bold=True)
    draw.rectangle((538, 244, 602, 248), fill=GREEN)
    lead_lines = [
        "A U.S. jury convicts Huawei on 10 of",
        "12 counts — bank fraud, wire fraud,",
        "sanctions breaches and trade-secret",
        "theft. Sentencing next September.",
    ]
    for i, line in enumerate(lead_lines):
        place(draw, lead_x, 266 + 31 * i, line, 23, PAPER)
    place(draw, lead_x, 422, "10 OF 12 COUNTS · 2018 CASE", 16, GREEN, bold=True)

    # --- Four news cards -------------------------------------------------
    cards = [
        # (x, y, strip, kicker, headline lines, body lines)
        (24, 478, (198, 44, 62), "CHINA · POLITICS",
         ["Shanghai chief Chen Jining", "probed"],
         ["Beijing says the Politburo member faces a graft",
          "probe, the fourth Politburo member",
          "investigated since 2025."]),
        (522, 478, (24, 110, 196), "UNITED STATES · CYBER",
         ["CIA and spy chief's office", "hacked"],
         ["Hackers hit unclassified open-source systems,",
          "CNN says. Officials say no classified data was",
          "affected."]),
        (24, 732, (214, 110, 20), "CHINA · AVIATION",
         ["Xiamen Air buys 50 Boeing", "737-8s"],
         ["List price about $7.4bn, deliveries 2031-2034.",
          "First big Chinese Boeing order since 2017."]),
        (522, 732, (13, 140, 130), "SAUDI ARABIA",
         ["Riyadh tower hit again, 11", "hurt"],
         ["The 385m PIF tower is struck a second time in",
          "a week. At least two are seriously hurt, civil",
          "defence says."]),
    ]
    for x, y, strip, kicker, headlines, body in cards:
        draw.rounded_rectangle((x, y, x + 478, y + 238), radius=16, fill=PAPER)
        top_strip(draw, x, y, 478, strip)
        text_x = x + 24
        place(draw, text_x, y + 26, kicker, 16, strip, bold=True)
        for i, line in enumerate(headlines):
            place(draw, text_x, y + 54 + 31 * i, line, 25, INK, bold=True)
        for i, line in enumerate(body):
            place(draw, text_x, y + 124 + 25 * i, line, 18, GREY)

    # --- Footer -----------------------------------------------------------
    centred(draw, 512, 988,
            "25 NOVEMBER 2026 · SOURCES: REUTERS · CNN · AIRWAYS MAGAZINE · AL JAZEERA",
            16, GREY)

    page.save(OUT_PATH, optimize=True)
    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes)")


if __name__ == "__main__":
    build()
