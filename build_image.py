#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Draw entry.png: one glossy beef burger — a picture that tastes of ONE
ingredient, BEEF.

Flat vector-style illustration rendered with Pillow. The scene is drawn at
2x resolution (2048x2048) and downsampled to 1024x1024 with LANCZOS so
edges and lettering stay crisp. Fully deterministic: every speck, seed and
steam curl comes from a seeded RNG (seed 20261122), so repeated runs
produce byte-identical output. No network, no external assets beyond the
system DejaVu fonts.

Run: python3 build_image.py   (writes entry.png next to this file)
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SCALE = 2
W = H = 1024 * SCALE
CX = W // 2
RNG = random.Random(20261122)

HERE = Path(__file__).resolve().parent
FONTS = Path("/usr/share/fonts/truetype/dejavu")

# ---- palette ------------------------------------------------------------
INK = (26, 17, 10)          # near-black warm edge
EMBER = (64, 38, 18)        # warm brown centre
AMBER = (226, 148, 52)      # glow behind the burger
PLATE = (244, 234, 212)     # cream plate
PLATE_RIM = (212, 190, 150)
BUN_TOP = (238, 176, 84)
BUN_SHADE = (186, 116, 34)
BUN_BASE = (210, 144, 64)
MEAT = (82, 42, 18)
MEAT_DARK = (52, 24, 10)
MEAT_GLOSS = (158, 98, 52)
CHEDDAR = (248, 172, 38)
CHEDDAR_HI = (255, 202, 96)
TOMATO_RED = (214, 64, 42)
TOMATO_DARK = (178, 38, 26)
LEAF = (96, 168, 60)
LEAF_HI = (132, 190, 80)
SESAME = (252, 230, 182)
CREAM_TEXT = (246, 234, 208)


def vertical_gradient(width, height, top_rgb, bottom_rgb):
    """RGB image blending top_rgb at the top into bottom_rgb at the bottom."""
    ramp = Image.linear_gradient("L").resize((width, height))
    return Image.composite(
        Image.new("RGB", (width, height), bottom_rgb),
        Image.new("RGB", (width, height), top_rgb),
        ramp,
    )


def soft_disc(diameter, rgb, peak_alpha):
    """A soft radial disc, brightest at the centre, fading to transparent."""
    mask = Image.radial_gradient("L").resize((diameter, diameter))
    mask = mask.point(lambda v: int(v * peak_alpha / 255))
    layer = Image.new("RGBA", (diameter, diameter), rgb + (0,))
    layer.putalpha(mask)
    return layer


def seed_ellipse(canvas, cx, cy, w, h, tilt, fill):
    """One rotated sesame seed, drawn on its own tile then pasted.

    canvas is the RGBA Image to paste onto.
    """
    tile = Image.new("RGBA", (int(w * 4), int(h * 4)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.ellipse([w, h, 3 * w, 3 * h], fill=fill + (255,))
    tile = tile.rotate(tilt, resample=Image.BICUBIC,
                       center=(w * 2, h * 2))
    canvas.paste(tile, (int(cx - w * 2), int(cy - h * 2)), tile)


def steam_layer():
    """Three blurred, translucent steam curls rising above the bun."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for base_x, phase, strength in ((CX - 190, 0.3, 64),
                                    (CX + 10, 1.7, 88),
                                    (CX + 200, 3.1, 64)):
        for dx, alpha in ((-16, strength // 2), (0, strength),
                          (16, strength // 2)):
            points = []
            for step in range(101):
                y = 600 - step * 3.4
                x = base_x + dx + math.sin(step / 100 * math.pi * 2.2 + phase) * 36
                points.append((x, y))
            d.line(points, fill=(255, 251, 242, alpha), width=24,
                   joint="curve")
    return layer.filter(ImageFilter.GaussianBlur(9))


def draw_caption(canvas):
    """Bottom caption: 'ONE INGREDIENT' small, 'BEEF' large, letterspaced."""
    d = ImageDraw.Draw(canvas)
    small = ImageFont.truetype(str(FONTS / "DejaVuSerif-Bold.ttf"), 58)
    big = ImageFont.truetype(str(FONTS / "DejaVuSerif-Bold.ttf"), 138)

    def spaced(text, font, y, fill, gap=16):
        widths = [d.textlength(ch, font=font) for ch in text]
        total = sum(widths) + gap * (len(text) - 1)
        x = CX - total // 2
        for ch, wch in zip(text, widths):
            d.text((x, y), ch, font=font, fill=fill)
            x += wch + gap

    spaced("ONE INGREDIENT", small, 1808, CREAM_TEXT + (255,))
    d.text((CX, 1868), "BEEF", font=big, fill=CREAM_TEXT + (255,),
           anchor="ma")


def render():
    # ---- backdrop: dark warm vignette with an amber halo ---------------
    mask = Image.radial_gradient("L").resize((W, H))
    img = Image.composite(
        Image.new("RGB", (W, H), EMBER),
        Image.new("RGB", (W, H), INK),
        mask,
    ).convert("RGBA")
    halo = soft_disc(W, AMBER, 150)
    img.alpha_composite(halo, (0, 0))

    d = ImageDraw.Draw(img)

    # ---- plate ----------------------------------------------------------
    d.ellipse([CX - 840, 1500, CX + 840, 1800], fill=PLATE_RIM + (255,))
    d.ellipse([CX - 806, 1512, CX + 806, 1776], fill=PLATE + (255,))
    d.ellipse([CX - 806, 1512, CX + 806, 1776],
              outline=(196, 172, 132, 255), width=5)
    # burger shadow on the plate
    d.ellipse([CX - 560, 1430, CX + 560, 1610], fill=(118, 92, 58, 80))

    # ---- bottom bun -----------------------------------------------------
    heel = vertical_gradient(1240, 190, (226, 164, 78), BUN_BASE).convert("RGBA")
    heel_mask = Image.new("L", (1240, 190), 0)
    ImageDraw.Draw(heel_mask).rounded_rectangle(
        [0, 0, 1240, 190], radius=85, fill=255)
    img.paste(heel, (CX - 620, 1390), heel_mask)
    d = ImageDraw.Draw(img)
    d.arc([CX - 620, 1390, CX + 620, 1570], start=180, end=360,
          fill=(244, 196, 116, 255), width=9)

    # ---- beef patty: thick, charred, wider than the buns ---------------
    patty = vertical_gradient(1360, 176, (104, 54, 24), MEAT_DARK).convert("RGBA")
    patty_mask = Image.new("L", (1360, 176), 0)
    ImageDraw.Draw(patty_mask).rounded_rectangle(
        [0, 0, 1360, 176], radius=88, fill=255)
    img.paste(patty, (CX - 680, 1252), patty_mask)
    d = ImageDraw.Draw(img)
    # grill stripes
    for i, gx in enumerate(range(CX - 560, CX + 561, 140)):
        d.line([(gx, 1270), (gx + 60, 1410)], fill=(34, 15, 6, 150), width=26)
    # charred speckles
    for _ in range(80):
        x = RNG.uniform(CX - 640, CX + 640)
        y = RNG.uniform(1272, 1408)
        r = RNG.uniform(4, 10)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(28, 12, 5, 150))
    # glossy highlight on the patty's top edge
    d.arc([CX - 620, 1228, CX + 620, 1396], start=200, end=340,
          fill=MEAT_GLOSS + (210,), width=13)

    # ---- cheddar: bright slice melting over the patty -------------------
    d.polygon([(CX - 600, 1192), (CX + 600, 1192), (CX + 556, 1296),
               (CX - 556, 1296)], fill=CHEDDAR + (255,))
    d.polygon([(CX - 600, 1192), (CX + 600, 1192), (CX + 578, 1236),
               (CX - 578, 1236)], fill=CHEDDAR_HI + (255,))
    for cx, drop in ((CX - 390, 120), (CX + 30, 158), (CX + 410, 104)):
        d.rounded_rectangle([cx - 40, 1232, cx + 40, 1232 + drop],
                            radius=40, fill=CHEDDAR + (255,))
        d.ellipse([cx - 40, 1232 + drop - 40, cx + 40, 1232 + drop + 40],
                  fill=CHEDDAR + (255,))
    d.line([(CX - 592, 1202), (CX + 592, 1202)],
           fill=(255, 210, 110, 255), width=7)

    # ---- tomato slice peeking out on the right --------------------------
    d.ellipse([CX + 290, 1144, CX + 700, 1246], fill=TOMATO_DARK + (255,))
    d.ellipse([CX + 322, 1156, CX + 668, 1234], fill=TOMATO_RED + (255,))
    d.arc([CX + 352, 1164, CX + 638, 1226], start=200, end=340,
          fill=(255, 128, 100, 220), width=9)

    # ---- lettuce: ruffled green band ------------------------------------
    d.rectangle([CX - 640, 1072, CX + 640, 1152], fill=LEAF + (255,))
    for i in range(17):
        cx = CX - 618 + i * 78
        r = 54 + (10 if i % 2 == 0 else -6)
        d.ellipse([cx - r, 1094, cx + r, 1094 + 2 * r], fill=LEAF + (255,))
        d.ellipse([cx - r + 14, 1106, cx + r - 14, 1094 + 2 * r - 12],
                  fill=LEAF_HI + (255,))
    d.line([(CX - 618, 1082), (CX + 618, 1082)],
           fill=(156, 208, 100, 255), width=7)

    # ---- top bun: golden dome -------------------------------------------
    dome = vertical_gradient(1280, 470, BUN_TOP, BUN_SHADE).convert("RGBA")
    dome_mask = Image.new("L", (1280, 470), 0)
    dm = ImageDraw.Draw(dome_mask)
    dm.pieslice([0, 0, 1280, 740], start=180, end=360, fill=255)
    dm.rectangle([0, 360, 1280, 470], fill=255)
    img.paste(dome, (CX - 640, 640), dome_mask)
    d = ImageDraw.Draw(img)
    # gloss arc on the dome
    d.arc([CX - 470, 700, CX + 310, 1170], start=195, end=285,
          fill=(255, 236, 192, 150), width=32)
    # sesame seeds scattered on the dome
    for _ in range(13):
        x = RNG.uniform(CX - 460, CX + 460)
        y = RNG.uniform(760, 1000)
        if ((x - CX) / 560) ** 2 + ((y - 900) / 300) ** 2 > 1:
            continue
        seed_ellipse(img, x, y, 26, 15, RNG.uniform(-35, 35), SESAME)
    # warm rim light at the dome base
    d.arc([CX - 640, 640, CX + 640, 1110], start=0, end=180,
          fill=(244, 184, 102, 170), width=8)

    # ---- steam ----------------------------------------------------------
    img = Image.alpha_composite(img, steam_layer())
    d = ImageDraw.Draw(img)

    # ---- crumbs on the plate --------------------------------------------
    for _ in range(12):
        x = RNG.uniform(CX - 720, CX + 720)
        y = RNG.uniform(1550, 1700)
        if abs(x - CX) < 560 and 1460 < y < 1620:
            continue
        seed_ellipse(img, x, y, 16, 9, RNG.uniform(0, 180), (236, 206, 162))

    # ---- caption ---------------------------------------------------------
    draw_caption(img)

    # ---- vignette, downsample, save --------------------------------------
    vig = Image.radial_gradient("L").resize((W, H)).point(
        lambda v: int(255 - (255 - v) * 0.45))
    img = Image.composite(img, Image.new("RGBA", (W, H), (0, 0, 0, 255)), vig)

    out = img.convert("RGB").resize((1024, 1024), Image.LANCZOS)
    target = HERE / "entry.png"
    out.save(target, optimize=True)
    print("wrote", target, out.size, target.stat().st_size, "bytes")


if __name__ == "__main__":
    render()
