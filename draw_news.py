"""Render the 18 November front page from original vector-style artwork."""

import os
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = "#f8f2e7"
INK = "#142f35"
MUTED = "#405c5b"
RULE = "#b9beb0"
CREAM = "#fff4db"
GOLD = "#ffc681"
TEAL = "#185955"
RED = "#9b3d32"
FONT_DIR = Path(os.environ.get("NOTO_SANS_DIR", "/usr/share/fonts/truetype/noto"))


@lru_cache(maxsize=None)
def font(size, weight):
    return ImageFont.truetype(str(FONT_DIR / f"NotoSans-{weight}.ttf"), size)


def text(draw, x, y, value, size, color=INK, weight="Bold", max_width=None):
    face = font(size, weight)
    if max_width is not None and draw.textlength(value, font=face) > max_width:
        raise ValueError(f"Text overflows {max_width}px: {value!r}")
    draw.text((x, y), value, fill=color, font=face, anchor="lt")


def globe(draw, x, y):
    draw.ellipse((x, y, x + 74, y + 74), outline=INK, width=4)
    draw.ellipse((x + 20, y, x + 54, y + 74), outline=INK, width=3)
    for offset in (21, 37, 53):
        inset = 4 if offset != 37 else 1
        draw.line((x + inset, y + offset, x + 74 - inset, y + offset), fill=INK, width=3)


def skyline(draw):
    draw.ellipse((607, 202, 936, 498), fill="#215452")
    draw.arc((620, 213, 923, 480), 181, 358, fill="#55827a", width=2)
    buildings = [
        (554, 30, 312), (585, 33, 282), (619, 24, 314), (644, 39, 273),
        (687, 31, 297), (723, 26, 248), (754, 21, 273), (778, 32, 221),
        (814, 35, 288), (853, 38, 262), (895, 28, 302), (927, 35, 277),
    ]
    for x, width, top in buildings:
        draw.polygon([(x, 430), (x, top + 9), (x + width // 2, top),
                      (x + width, top + 9), (x + width, 430)], fill="#2b615d")
        for window in range(top + 18, 407, 14):
            draw.line((x + 8, window, x + width - 8, window), fill="#477670", width=2)
    draw.line((794, 222, 794, 207), fill="#477670", width=3)


def portrait(draw, x, y, skin, shade, hair, tie, haircut):
    def polygon(points, fill):
        draw.polygon([(x + px, y + py) for px, py in points], fill=fill)

    polygon([(-61, 167), (-56, 127), (-43, 112), (-22, 103), (0, 96),
             (24, 103), (49, 114), (58, 130), (62, 167)], "#102b30")
    polygon([(-22, 105), (-10, 94), (13, 94), (23, 105), (0, 154)], CREAM)
    polygon([(-7, 115), (6, 115), (10, 122), (5, 128), (11, 148),
             (0, 157), (-10, 147), (-4, 128), (-9, 122)], tie)
    polygon([(-16, 79), (15, 79), (18, 102), (0, 114), (-18, 102)], shade)
    draw.ellipse((x - 35, y + 45, x - 18, y + 74), fill=shade)
    draw.ellipse((x + 18, y + 45, x + 35, y + 74), fill=shade)
    polygon([(-29, 30), (-22, 16), (17, 15), (30, 30), (28, 68), (20, 84),
             (9, 95), (-8, 95), (-21, 85), (-28, 69)], skin)
    polygon([(2, 49), (7, 66), (0, 69), (-5, 66)], shade)
    polygon(haircut, hair)
    draw.line((x - 17, y + 50, x - 8, y + 49), fill="#3c322c", width=3)
    draw.line((x + 9, y + 49, x + 18, y + 50), fill="#3c322c", width=3)
    draw.line((x - 7, y + 79, x + 8, y + 79), fill=shade, width=3)


def summit_art(draw):
    skyline(draw)
    portrait(draw, 614, 273, "#eeb486", "#a66754", "#eec174", RED,
             [(-32, 50), (-34, 30), (-49, 25), (-28, 13), (-8, 8),
              (14, 11), (31, 21), (35, 39), (29, 49), (22, 31), (-17, 27)])
    portrait(draw, 752, 265, "#d79d73", "#965e51", "#20282a", "#bc5245",
             [(-31, 53), (-34, 34), (-28, 16), (-15, 10), (11, 10),
              (29, 19), (34, 32), (29, 53), (24, 31), (-15, 27), (-26, 38)])
    portrait(draw, 890, 273, "#e8bb98", "#9e705f", "#ad9c85", "#406e88",
             [(-30, 50), (-34, 34), (-28, 20), (-17, 14), (9, 12),
              (27, 19), (32, 32), (29, 47), (24, 29), (7, 21), (-17, 25)])
    draw.polygon([(565, 431), (936, 431), (961, 457), (542, 457)], fill="#36716a")
    draw.rectangle((542, 457, 961, 513), fill="#102e33")
    draw.line((551, 456, 952, 456), fill=GOLD, width=3)
    for x, name in [(614, "TRUMP"), (752, "XI"), (890, "PUTIN")]:
        face = font(25, "ExtraBold")
        text(draw, x - draw.textlength(name, font=face) / 2, 472, name, 25, CREAM, "ExtraBold")


def icon(draw, x, y, kind, color):
    def line(points, width=3):
        draw.line([(x + px, y + py) for px, py in points], fill=color, width=width)

    def box(left, top, right, bottom):
        draw.rectangle((x + left, y + top, x + right, y + bottom), outline=color, width=3)

    if kind == "waves":
        for offset in (11, 23, 35):
            line([(1, offset), (10, offset + 4), (20, offset), (30, offset + 4), (40, offset)])
    elif kind == "bridge":
        line([(0, 28), (41, 28)])
        for post in (10, 30):
            line([(post, 39), (post, 9)])
        line([(0, 23), (10, 11), (20, 22), (30, 11), (41, 23)])
    elif kind == "ballot":
        box(3, 19, 38, 39)
        line([(13, 25), (29, 25)])
        line([(13, 11), (19, 17), (30, 4)])
    elif kind == "chart":
        line([(3, 5), (3, 38), (39, 38)])
        line([(9, 30), (19, 20), (25, 23), (38, 8)])
        line([(28, 8), (38, 8), (38, 18)])
    elif kind == "chip":
        box(8, 8, 33, 33)
        box(15, 15, 26, 26)
        for pin in (13, 21, 29):
            line([(pin, 2), (pin, 8)])
            line([(pin, 33), (pin, 39)])
            line([(2, pin), (8, pin)])
            line([(33, pin), (39, pin)])
    elif kind == "shelter":
        line([(1, 30), (20, 7), (40, 30), (1, 30)])
        line([(14, 29), (20, 20), (26, 29)])
        line([(1, 38), (12, 35), (22, 38), (32, 35), (40, 38)])


STORIES = [
    ("PERSIAN GULF", ("Iran hits", "US sites"), "Kuwait & Bahrain", "waves", RED),
    ("UKRAINE", ("Ukraine hits", "Crimea bridge"), "Third strike in a week", "bridge", RED),
    ("US SENATE", ("Peltola wins", "in Alaska"), "Defeats Dan Sullivan", "ballot", TEAL),
    ("MARKETS", ("Anthropic", "raises $81.3B"), "Record IPO", "chart", TEAL),
    ("TECHNOLOGY", ("Nvidia rejects", "Huang return"), "CEO exit stands", "chip", TEAL),
    ("GAZA", ("Ceasefire", "under strain"), "950,000 at flood risk", "shelter", RED),
]


def front_page():
    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1023, 11), fill=INK)
    text(draw, 43, 36, "THE WORLD", 104, INK, "Black")
    globe(draw, 902, 43)
    draw.line((44, 130, 980, 130), fill=INK, width=2)
    text(draw, 44, 145, "WEDNESDAY, 18 NOVEMBER 2026", 30, INK, "ExtraBold", 936)

    draw.rectangle((44, 187, 979, 534), fill="#153a3e")
    summit_art(draw)
    text(draw, 68, 212, "APEC  /  CHINA", 25, GOLD, "ExtraBold")
    text(draw, 68, 257, "Shenzhen", 76, CREAM, "Black", 470)
    text(draw, 68, 339, "summit set", 76, CREAM, "Black", 470)
    text(draw, 68, 437, "Trump, Xi and Putin", 34, CREAM, "Bold", 470)
    text(draw, 68, 479, "to meet Thursday", 34, CREAM, "Bold", 470)

    for index, (region, headline, detail, kind, accent) in enumerate(STORIES):
        row, column = divmod(index, 3)
        x, y = 44 + column * 319, 553 + row * 195
        draw.line((x, y, x + 297, y), fill=accent, width=4)
        text(draw, x, y + 14, region, 23, accent, "ExtraBold", 246)
        icon(draw, x + 255, y + 14, kind, accent)
        for line_number, title_line in enumerate(headline):
            text(draw, x, y + 57 + line_number * 45, title_line, 40, INK, "Black", 301)
        text(draw, x, y + 151, detail, 23, MUTED, "Bold", 304)
        if column < 2:
            draw.line((x + 308, y + 13, x + 308, y + 173), fill=RULE, width=1)

    draw.rectangle((0, 943, 1023, 1023), fill=INK)
    text(draw, 44, 969, "18 November 2026 — World news in one image", 28, CREAM, "Bold", 936)
    return image


if __name__ == "__main__":
    front_page().save(Path(__file__).with_name("entry.png"), optimize=True)
