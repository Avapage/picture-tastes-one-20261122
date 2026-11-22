#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Render entry.png: one giant glossy beef burger, the single-ingredient hero.

Drawn with Pillow at 2x (2048x2048) and downsampled with LANCZOS to
1024x1024 for crisp edges and text. Deterministic: every random choice
comes from random.Random(7). Run: python3 build_image.py
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 2  # supersample factor
W, H = 1024 * S, 1024 * S
RNG = random.Random(7)

HERE = Path(__file__).resolve().parent
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

DARK_EDGE = (23, 16, 10)
WARM_CENTRE = (58, 36, 19)
GLOW = (214, 138, 48)
CREAM = (243, 233, 210)
BUN_LIGHT = (232, 169, 78)
BUN_DEEP = (178, 111, 31)
BUN_BOTTOM = (203, 138, 62)
PATTY = (74, 36, 16)
PATTY_DARK = (46, 20, 8)
CHEESE = (245, 166, 35)
CHEESE_DEEP = (232, 138, 20)
TOMATO = (210, 60, 40)
LETTUCE = (93, 163, 58)
LETTUCE_LIGHT = (124, 184, 74)
SEED = (250, 226, 178)


def vgrad(w, h, top, bottom):
    """Vertical gradient image from top colour to bottom colour."""
    mask = Image.linear_gradient("L").resize((w, h))
    return Image.composite(
        Image.new("RGB", (w, h), bottom), Image.new("RGB", (w, h), top), mask
    )


def radial_glow(size, colour, max_alpha=255):
    """Soft radial glow: colour at centre fading to transparent."""
    mask = Image.radial_gradient("L").resize((size, size))
    layer = Image.new("RGBA", (size, size), colour + (0,))
    alpha = mask.point(lambda v: int(v * max_alpha / 255))
    layer.putalpha(alpha)
    return layer


def rounded_seed(draw, cx, cy, w, h, angle, fill):
    """A small rotated sesame-seed ellipse centred at (cx, cy)."""
    tmp = Image.new("RGBA", (int(w * 3), int(h * 3)), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.ellipse([w, h, 2 * w, 2 * h], fill=fill + (255,))
    tmp = tmp.rotate(angle, resample=Image.BICUBIC, center=(w * 1.5, h * 1.5))
    draw._image.paste(tmp, (int(cx - w * 1.5), int(cy - h * 1.5)), tmp)


def draw_steam(layer):
    """Three soft translucent wavy steam curls above the bun."""
    d = ImageDraw.Draw(layer)
    for cx0, phase, alpha in ((860, 0.0, 70), (1024, 1.4, 90), (1188, 2.6, 70)):
        for off, a in ((-14, alpha // 2), (0, alpha), (14, alpha // 2)):
            pts = []
            for t in range(0, 101):
                y = 640 - t * 3.6
                x = cx0 + off + math.sin(t / 100 * math.pi * 2.4 + phase) * 34
                pts.append((x, y))
            d.line(pts, fill=(255, 250, 240, a), width=26, joint="curve")
    return layer.filter(ImageFilter.GaussianBlur(10))


def main():
    # --- background: warm radial gradient, dark edges ---
    mask = Image.radial_gradient("L").resize((W, H))
    bg = Image.composite(
        Image.new("RGB", (W, H), WARM_CENTRE),
        Image.new("RGB", (W, H), DARK_EDGE),
        mask,
    )
    img = bg.convert("RGBA")

    # --- amber glow behind the burger: full-canvas radial falloff,
    # so no layer edge can ever show ---
    glow_mask = Image.radial_gradient("L").resize((W, H)).point(
        lambda v: int(v * 0.55))
    img = Image.composite(
        Image.new("RGBA", (W, H), GLOW + (255,)), img, glow_mask)

    d = ImageDraw.Draw(img)

    # --- plate: wide cream ellipse with a rim ---
    d.ellipse([1024 - 830, 1520, 1024 + 830, 1780], fill=(226, 210, 178, 255))
    d.ellipse([1024 - 800, 1530, 1024 + 800, 1760], fill=CREAM + (255,))
    d.ellipse([1024 - 800, 1530, 1024 + 800, 1760], outline=(198, 176, 138, 255), width=6)
    # soft shadow of the burger on the plate
    d.ellipse([1024 - 560, 1440, 1024 + 560, 1620], fill=(120, 95, 60, 90))

    # --- bottom bun: golden, slightly narrower than the patty ---
    bun_bot = vgrad(1280, 180, (222, 158, 74), BUN_BOTTOM).convert("RGBA")
    bun_mask = Image.new("L", (1280, 180), 0)
    dm = ImageDraw.Draw(bun_mask)
    dm.rounded_rectangle([0, 0, 1280, 180], radius=80, fill=255)
    img.paste(bun_bot, (1024 - 640, 1400), bun_mask)
    d = ImageDraw.Draw(img)
    d.arc([1024 - 640, 1400, 1024 + 640, 1580], start=180, end=360,
          fill=(240, 190, 110, 255), width=10)

    # --- beef patty: thick, dark brown, wider than the buns ---
    patty = vgrad(1344, 170, (96, 48, 22), PATTY_DARK).convert("RGBA")
    pmask = Image.new("L", (1344, 170), 0)
    dm = ImageDraw.Draw(pmask)
    dm.rounded_rectangle([0, 0, 1344, 170], radius=85, fill=255)
    img.paste(patty, (1024 - 672, 1264), pmask)
    d = ImageDraw.Draw(img)
    # speckles: charred bits
    for _ in range(90):
        x = RNG.uniform(1024 - 640, 1024 + 640)
        y = RNG.uniform(1280, 1410)
        r = RNG.uniform(4, 11)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(30, 13, 5, 160))
    # glossy highlight along the patty's top edge
    d.arc([1024 - 620, 1240, 1024 + 620, 1400], start=200, end=340,
          fill=(150, 92, 50, 200), width=14)

    # --- cheese: bright orange-yellow slice melting over the patty ---
    d.polygon([(1024 - 610, 1200), (1024 + 610, 1200), (1024 + 560, 1300),
               (1024 - 560, 1300)], fill=CHEESE + (255,))
    d.polygon([(1024 - 610, 1200), (1024 + 610, 1200), (1024 + 580, 1240),
               (1024 - 580, 1240)], fill=(255, 196, 90, 255))
    # three rounded drips hanging over the patty
    for cx, length in ((1024 - 380, 130), (1024 + 40, 165), (1024 + 400, 110)):
        d.rounded_rectangle([cx - 42, 1240, cx + 42, 1240 + length],
                            radius=42, fill=CHEESE + (255,))
        d.ellipse([cx - 42, 1240 + length - 42, cx + 42, 1240 + length + 42],
                  fill=CHEESE + (255,))
    d.line([(1024 - 600, 1210), (1024 + 600, 1210)], fill=(255, 205, 105, 255), width=8)

    # --- tomato: red slice peeking out on the right ---
    d.ellipse([1024 + 300, 1150, 1024 + 700, 1250], fill=(190, 40, 28, 255))
    d.ellipse([1024 + 330, 1162, 1024 + 670, 1238], fill=TOMATO + (255,))
    d.arc([1024 + 360, 1170, 1024 + 640, 1230], start=200, end=340,
          fill=(255, 120, 95, 220), width=10)

    # --- lettuce: ruffled green band under the top bun ---
    d.rectangle([1024 - 640, 1080, 1024 + 640, 1160], fill=LETTUCE + (255,))
    for i in range(17):
        cx = 1024 - 620 + i * 78
        r = 52 + (10 if i % 2 == 0 else -6)
        d.ellipse([cx - r, 1100, cx + r, 1100 + 2 * r], fill=LETTUCE + (255,))
        d.ellipse([cx - r + 14, 1112, cx + r - 14, 1100 + 2 * r - 10],
                  fill=LETTUCE_LIGHT + (255,))
    d.line([(1024 - 620, 1090), (1024 + 620, 1090)], fill=(150, 205, 95, 255), width=8)

    # --- top bun: big golden dome ---
    dome = vgrad(1280, 480, BUN_LIGHT, BUN_DEEP).convert("RGBA")
    dmask = Image.new("L", (1280, 480), 0)
    dm = ImageDraw.Draw(dmask)
    dm.pieslice([0, 0, 1280, 740], start=180, end=360, fill=255)
    dm.rectangle([0, 370, 1280, 480], fill=255)
    img.paste(dome, (1024 - 640, 640), dmask)
    d = ImageDraw.Draw(img)
    # soft white gloss arc on the dome
    d.arc([1024 - 480, 700, 1024 + 300, 1180], start=195, end=285,
          fill=(255, 235, 190, 150), width=34)
    # sesame seeds on the dome
    for _ in range(12):
        x = RNG.uniform(1024 - 460, 1024 + 460)
        y = RNG.uniform(760, 1010)
        # keep seeds inside the dome curve
        if ((x - 1024) / 560) ** 2 + ((y - 900) / 300) ** 2 > 1:
            continue
        rounded_seed(d, x, y, 26, 15, RNG.uniform(-35, 35), SEED)
    # warm rim light along the dome's base
    d.arc([1024 - 640, 640, 1024 + 640, 1120], start=0, end=180,
          fill=(240, 180, 100, 160), width=8)

    # --- steam rising above the bun ---
    steam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    img = Image.alpha_composite(img, draw_steam(steam))
    d = ImageDraw.Draw(img)

    # --- sesame seeds / crumbs scattered on the plate ---
    for _ in range(14):
        x = RNG.uniform(1024 - 720, 1024 + 720)
        y = RNG.uniform(1560, 1700)
        if abs(x - 1024) < 560 and 1460 < y < 1620:
            continue
        rounded_seed(d, x, y, 16, 9, RNG.uniform(0, 180), (235, 205, 160))

    # --- caption: ONE INGREDIENT / BEEF ---
    font_small = ImageFont.truetype(str(FONT_DIR / "DejaVuSerif-Bold.ttf"), 62)
    font_big = ImageFont.truetype(str(FONT_DIR / "DejaVuSerif-Bold.ttf"), 130)
    cream = (245, 232, 205, 255)

    def draw_spaced(text, font, y, fill, spacing=14):
        widths = [d.textlength(ch, font=font) for ch in text]
        total = sum(widths) + spacing * (len(text) - 1)
        x = W // 2 - total // 2
        for ch, wch in zip(text, widths):
            d.text((x, y), ch, font=font, fill=fill)
            x += wch + spacing

    draw_spaced("ONE INGREDIENT", font_small, 1810, cream)
    d.text((W // 2, 1870), "BEEF", font=font_big, fill=cream,
           anchor="ma")

    # --- vignette + downsample ---
    vig = Image.radial_gradient("L").resize((W, H)).point(
        lambda v: int(255 - (255 - v) * 0.45))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img = Image.composite(img, black, vig)

    out = img.convert("RGB").resize((1024, 1024), Image.LANCZOS)
    out.save(HERE / "entry.png", optimize=True)
    print("wrote", HERE / "entry.png", out.size,
          (HERE / "entry.png").stat().st_size, "bytes")


if __name__ == "__main__":
    main()
