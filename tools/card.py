#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""card.py — the share card, 1200x630, drawn from the same math as the page.

The outcomes-over-time chart — the expected line climbing green past break-even, with
runs of luck around it — under the title. Written to docs/card.jpg and referenced by the
pages' og:image / twitter:image.

    python3 tools/card.py
"""
from __future__ import annotations

import random
from math import comb
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DOCS = Path(__file__).resolve().parent.parent / "docs"
W, H = 1200, 630
BG = (18, 16, 14)
INK = (240, 230, 214)
RED = (239, 75, 75)
GREEN = (76, 196, 135)
MUTE = (166, 148, 124)

COND = "/System/Library/Fonts/Avenir Next Condensed.ttc"
BODY = "/System/Library/Fonts/Avenir Next.ttc"


def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()


def outcomes(payoff):
    """The page's own model: per hand, hit -> +pot+payoff, miss -> -call."""
    unseen, outs = 47, 9
    p = 1 - (comb(unseen - outs, 2) / comb(unseen, 2))  # flush draw, two cards to come
    pot, bet = 100, 50
    total, call = pot + bet, bet
    ev = p * (total + payoff) - (1 - p) * call
    N = 150
    expected = [i * ev for i in range(N + 1)]
    runs = []
    for seed in (1, 7, 23, 99):
        rng = random.Random(seed)
        cum, walk = 0.0, [0.0]
        for _ in range(N):
            cum += (total + payoff) if rng.random() < p else -call
            walk.append(cum)
        runs.append(walk)
    return expected, runs, N


def build():
    img = Image.new("RGB", (W, H), BG)

    # the chart, computed, drawn large at 2x then downscaled for clean lines
    scale = 2
    lay = Image.new("RGBA", (W * scale, H * scale), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    expected, runs, N = outcomes(payoff=170)

    ox, oy = int(W * 0.02) * scale, int(H * 0.30) * scale
    bw, bh = int(W * 1.02) * scale, int(H * 0.74) * scale
    allv = expected + [v for r in runs for v in r] + [0]
    lo, hi = min(allv), max(allv)
    span = (hi - lo) or 1

    def pt(i, v):
        x = ox + (i / N) * bw
        y = oy + (1 - (v - lo) / span) * bh
        return (x, y)

    # zero baseline
    y0 = pt(0, 0)[1]
    ld.line([(ox, y0), (ox + bw, y0)], fill=(*MUTE, 60), width=2)
    # runs of luck, faint
    for r in runs:
        ld.line([pt(i, v) for i, v in enumerate(r)], fill=(*MUTE, 95), width=3, joint="curve")
    # the expected line, bold green
    ld.line([pt(i, v) for i, v in enumerate(expected)], fill=(*GREEN, 235), width=8, joint="curve")

    lay = lay.resize((W, H), Image.LANCZOS)
    img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")

    # scrim from the left so the text sits clean, and a bottom strip
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for x in range(W):
        a = int(240 * max(0, 1 - x / (W * 0.62)))
        sd.line([(x, 0), (x, H)], fill=(*BG, a))
    sd.rectangle([0, H - 130, W, H], fill=(*BG, 175))
    sd.rectangle([0, 0, W, 40], fill=(*BG, 120))
    img = Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")
    dr = ImageDraw.Draw(img, "RGBA")

    # the brand heart, drawn as a card mark
    cx, cy = 78, 92
    dr.rounded_rectangle([cx - 34, cy - 40, cx + 34, cy + 40], radius=10,
                         fill=(255, 250, 240), outline=(180, 178, 169), width=2)
    hx, hy, s = cx, cy + 6, 22
    dr.polygon([(hx, hy + s * 0.9),
                (hx - s, hy - s * 0.15),
                (hx - s * 0.5, hy - s * 0.75),
                (hx, hy - s * 0.25),
                (hx + s * 0.5, hy - s * 0.75),
                (hx + s, hy - s * 0.15)], fill=RED)

    kick = font(COND, 32, index=2)
    title = font(COND, 150, index=2)
    sub = font(BODY, 34, index=0)
    tiny = font(BODY, 26, index=0)

    dr.text((132, 66), "TEXAS HOLD'EM, DRAWN WITH THE MATH", font=kick, fill=RED)
    dr.text((60, 150), "IMPLIED", font=title, fill=INK)
    dr.text((60, 300), "ODDS", font=title, fill=RED)
    dr.text((64, 476), "The money you ain't won yet — and when",
            font=sub, fill=INK)
    dr.text((64, 516), "chasin' the draw actually pays.", font=sub, fill=INK)
    dr.text((64, H - 52), "hongdam.net · Chiang Rai", font=tiny, fill=MUTE)

    out = DOCS / "card.jpg"
    img.save(out, format="JPEG", quality=86, optimize=True)
    print(f"card -> {out}  ({out.stat().st_size // 1024} KB, {W}x{H})")


if __name__ == "__main__":
    build()
