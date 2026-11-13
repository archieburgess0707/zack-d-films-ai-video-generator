#!/usr/bin/env python3
"""
Free, no-API renderer for the "no wheels" short.

Draws every shot procedurally with Pillow (stylized shaded shapes), syncs the
shots and word-by-word captions to the Kokoro narration timing, synthesizes a
light music bed + whoosh/thud sound effects with numpy, and encodes with ffmpeg.

Usage: python3 out/no_wheels/render_free.py   (after make_voice.py)
"""
import json, math, os, random, subprocess, sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, K = 720, 1280, 30, 2          # K = supersampling factor
OUTRO = 3.5
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fonts = {}


def font(size):
    size = int(size * K)
    if size not in _fonts:
        _fonts[size] = ImageFont.truetype(FONT_B, size)
    return _fonts[size]


def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def clamp(p):
    return max(0.0, min(1.0, p))


def mix(c1, c2, p):
    return tuple(int(a + (b - a) * clamp(p)) for a, b in zip(c1, c2))


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


# --------------------------------------------------------------------------- drawing helpers
class D:
    def __init__(self, img):
        self.img = img
        self.d = ImageDraw.Draw(img, "RGBA")

    def rect(self, x0, y0, x1, y1, fill, r=0, outline=None, w=0):
        box = [x0 * K, y0 * K, x1 * K, y1 * K]
        if r:
            self.d.rounded_rectangle(box, r * K, fill=fill, outline=outline, width=int(w * K))
        else:
            self.d.rectangle(box, fill=fill, outline=outline, width=int(w * K))

    def ell(self, cx, cy, rx, ry, fill, outline=None, w=0):
        self.d.ellipse([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K],
                       fill=fill, outline=outline, width=int(w * K))

    def poly(self, pts, fill):
        self.d.polygon([(x * K, y * K) for x, y in pts], fill=fill)

    def line(self, pts, fill, w):
        self.d.line([(x * K, y * K) for x, y in pts], fill=fill, width=max(1, int(w * K)), joint="curve")

    def text(self, x, y, s, size, fill=(255, 255, 255), anchor="mm", stroke=0, sfill=(0, 0, 0)):
        self.d.text((x * K, y * K), s, font=font(size), fill=fill, anchor=anchor,
                    stroke_width=int(stroke * K), stroke_fill=sfill)

    def shadow(self, cx, cy, rx, ry=None, a=90):
        self.ell(cx, cy, rx, ry or rx * 0.18, (0, 0, 0, a))

    def ball(self, cx, cy, r, c):
        """Shaded sphere-ish circle for a clay/3D feel."""
        self.ell(cx, cy, r, r, shade(c, 0.7))
        self.ell(cx - r * 0.08, cy - r * 0.08, r * 0.9, r * 0.9, c)
        self.ell(cx - r * 0.35, cy - r * 0.38, r * 0.28, r * 0.2, (255, 255, 255, 110))


_bg_cache = {}


def gradient(top, bottom):
    key = (top, bottom)
    if key not in _bg_cache:
        col = np.linspace(0, 1, H * K)[:, None]
        arr = (np.array(top)[None, :] * (1 - col) + np.array(bottom)[None, :] * col).astype(np.uint8)
        arr = np.repeat(arr[:, None, :], W * K, axis=1)
        _bg_cache[key] = Image.fromarray(arr, "RGB")
    return _bg_cache[key].copy()


# --------------------------------------------------------------------------- props
SKIN, HOODIE, HAIR = (240, 196, 160), (52, 120, 220), (90, 60, 40)
CAR_RED = (226, 58, 52)


def wheel(d, cx, cy, r, ang, s=1.0):
    if s <= 0.02:
        return
    r *= s
    d.ell(cx, cy, r, r, (34, 34, 40))
    d.ell(cx, cy, r * 0.58, r * 0.58, (190, 195, 205))
    d.ell(cx, cy, r * 0.2, r * 0.2, (120, 125, 135))
    for k in range(5):
        a = ang + k * 2 * math.pi / 5
        d.line([(cx, cy), (cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55)], (120, 125, 135), r * 0.12)


def car(d, x, ground, sc=1.0, wheel_s=1.0, drop=0.0, ang=0.0, color=CAR_RED):
    """Side-view hatchback. `drop` lowers the body toward the ground (0..1)."""
    wr = 34 * sc
    body_bottom = ground - wr * 0.9 * (1 - drop) - 4 * sc * drop
    d.shadow(x, ground + 4, 170 * sc, 16 * sc)
    bw, bh = 330 * sc, 80 * sc
    y0 = body_bottom - bh
    d.rect(x - bw / 2 + 30 * sc, y0 - 70 * sc, x + bw / 2 - 70 * sc, y0 + 20 * sc, shade(color, 0.85), r=34 * sc)
    d.rect(x - bw / 2 + 52 * sc, y0 - 54 * sc, x - 6 * sc, y0 + 4 * sc, (160, 215, 245), r=14 * sc)
    d.rect(x + 6 * sc, y0 - 54 * sc, x + bw / 2 - 92 * sc, y0 + 4 * sc, (160, 215, 245), r=14 * sc)
    d.rect(x - bw / 2, y0, x + bw / 2, body_bottom, color, r=30 * sc)
    d.rect(x - bw / 2 + 10 * sc, y0 + 8 * sc, x + bw / 2 - 10 * sc, y0 + 22 * sc, (255, 255, 255, 70), r=7 * sc)
    d.ell(x + bw / 2 - 16 * sc, y0 + 30 * sc, 12 * sc, 9 * sc, (255, 240, 170))
    for wx in (x - bw / 2 + 70 * sc, x + bw / 2 - 70 * sc):
        d.ell(wx, body_bottom - 4 * sc, wr * 1.15, wr * 1.0, shade(color, 0.45))
        wheel(d, wx, ground - wr, wr, ang, wheel_s)


def person(d, x, ground, sc=1.0, mood="neutral", arms="down", lean=0.0):
    d.shadow(x, ground + 2, 60 * sc, 12 * sc)
    hip = ground - 95 * sc
    for dx in (-16, 16):
        d.line([(x + dx * sc, hip), (x + dx * sc + lean * 20 * sc, ground - 6 * sc)], (40, 45, 70), 22 * sc)
        d.ell(x + dx * sc + lean * 20 * sc + 6 * sc, ground - 6 * sc, 17 * sc, 9 * sc, (30, 30, 35))
    tx = x - lean * 30 * sc
    d.rect(tx - 48 * sc, hip - 120 * sc, tx + 48 * sc, hip + 6 * sc, HOODIE, r=34 * sc)
    d.rect(tx - 40 * sc, hip - 112 * sc, tx - 18 * sc, hip - 10 * sc, (255, 255, 255, 40), r=10 * sc)
    sh = hip - 100 * sc
    if arms == "up":
        hands = [(tx - 70 * sc, sh - 95 * sc), (tx + 70 * sc, sh - 95 * sc)]
    elif arms == "forward":
        hands = [(tx + 85 * sc, sh + 25 * sc), (tx + 90 * sc, sh + 40 * sc)]
    elif arms == "shock":
        hands = [(tx - 30 * sc, sh - 70 * sc), (tx + 30 * sc, sh - 70 * sc)]
    else:
        hands = [(tx - 62 * sc, sh + 85 * sc), (tx + 62 * sc, sh + 85 * sc)]
    for side, hnd in zip((-1, 1), hands):
        d.line([(tx + side * 42 * sc, sh), hnd], shade(HOODIE, 0.85), 22 * sc)
        d.ell(hnd[0], hnd[1], 13 * sc, 13 * sc, SKIN)
    hx, hy = tx + lean * 10 * sc, sh - 62 * sc
    d.ball(hx, hy, 52 * sc, SKIN)
    d.d.chord([(hx - 54 * sc) * K, (hy - 58 * sc) * K, (hx + 54 * sc) * K, (hy + 30 * sc) * K], 180, 360, fill=HAIR)
    ey = hy + 4 * sc
    for ex in (-18, 18):
        r = 9 if mood == "shock" else 7
        d.ell(hx + ex * sc, ey, r * sc, r * sc * 1.2, (255, 255, 255))
        d.ell(hx + ex * sc, ey + 1 * sc, 4.5 * sc, 5 * sc, (30, 30, 40))
    if mood == "shock":
        d.ell(hx, hy + 30 * sc, 9 * sc, 12 * sc, (90, 30, 30))
    elif mood == "happy":
        d.d.arc([(hx - 18 * sc) * K, (hy + 12 * sc) * K, (hx + 18 * sc) * K, (hy + 36 * sc) * K], 10, 170,
                fill=(90, 30, 30), width=int(5 * sc * K))
    elif mood == "strain":
        d.line([(hx - 14 * sc, hy + 28 * sc), (hx + 14 * sc, hy + 26 * sc)], (90, 30, 30), 5 * sc)
        d.ell(hx + 40 * sc, hy - 20 * sc, 6 * sc, 9 * sc, (120, 190, 255))
    else:
        d.line([(hx - 12 * sc, hy + 28 * sc), (hx + 12 * sc, hy + 28 * sc)], (90, 30, 30), 5 * sc)
    return hands


def gear_pts(cx, cy, r, teeth, ang):
    pts = []
    n = teeth * 4
    for i in range(n):
        a = ang + i * 2 * math.pi / n
        rr = r if (i % 4) in (0, 1) else r * 0.82
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def gear(d, cx, cy, r, teeth, ang, c, alpha=255):
    if alpha <= 3:
        return
    col = c + (int(alpha),)
    d.poly(gear_pts(cx + 4, cy + 6, r, teeth, ang), (0, 0, 0, int(alpha * 0.35)))
    d.poly(gear_pts(cx, cy, r, teeth, ang), col)
    d.ell(cx, cy, r * 0.62, r * 0.62, shade(c, 1.15) + (int(alpha),))
    d.ell(cx, cy, r * 0.18, r * 0.18, (40, 40, 50, int(alpha)))


def sparks(d, x, y, t, n=14, seed=1, spread=120, col=(255, 210, 90)):
    rnd = random.Random(seed + int(t * 12))
    for _ in range(n):
        a = rnd.uniform(math.pi * 1.05, math.pi * 1.95)
        L = rnd.uniform(15, spread)
        sx, sy = x + rnd.uniform(-30, 30), y
        d.line([(sx, sy), (sx + math.cos(a) * L, sy + math.sin(a) * L)], col, rnd.uniform(2, 5))


def ground_scene(d, horizon=880, sky=None, road=(70, 72, 82)):
    d.rect(0, horizon, W, H, road)
    d.rect(0, horizon, W, horizon + 10, shade(road, 1.3))
    for i in range(6):
        d.rect(i * 140 + 20, horizon + 70, i * 140 + 100, horizon + 82, (230, 220, 120))


def label(d, s, y=230, size=46, fill=(255, 255, 255), bg=(0, 0, 0, 150), p=1.0):
    if p <= 0:
        return
    sc = 0.6 + 0.4 * ease(p * 3)
    tw = font(size * sc).getlength(s) / K
    d.rect(W / 2 - tw / 2 - 24, y - size * sc * 0.8, W / 2 + tw / 2 + 24, y + size * sc * 0.8, bg, r=18)
    d.text(W / 2, y, s, size * sc, fill, stroke=3)


def stamp(d, s, y, p, col=(235, 50, 50)):
    if p <= 0:
        return
    sc = 1.8 - 0.8 * ease(p * 4)
    tw = font(64 * sc).getlength(s) / K
    d.rect(W / 2 - tw / 2 - 26, y - 52 * sc, W / 2 + tw / 2 + 26, y + 52 * sc, None, r=14, outline=col, w=8 * sc)
    d.text(W / 2, y, s, 64 * sc, col)


# --------------------------------------------------------------------------- shots
# each shot: fn(d, t, T) with local time t (s) and shot length T; returns background colors

def s1a(d, t, T):
    p = t / T
    ground_scene(d, 900)
    d.rect(60, 560, 330, 900, (236, 214, 180), r=8)
    d.poly([(40, 570), (195, 440), (350, 570)], (170, 70, 60))
    d.rect(170, 760, 230, 900, (120, 80, 60), r=6)
    person(d, 560, 905, 0.95, mood="shock" if p > 0.35 else "neutral", arms="shock" if p > 0.35 else "down")
    ws = 1 - ease((p - 0.25) / 0.5)
    car(d, 300, 1010, 0.95, wheel_s=ws, drop=0)
    rnd = random.Random(3)
    if 0.25 < p < 0.95:
        for wx in (300 - 157 + 66, 300 + 157 - 66):
            for _ in range(10):
                a, rr = rnd.uniform(0, 6.28), rnd.uniform(10, 70) * (0.5 + p)
                d.ell(wx + math.cos(a) * rr, 978 - abs(math.sin(a) * rr) * 1.4 - p * 40, 5, 5, (255, 230, 120, 200))
    label(d, "EVERY WHEEL... GONE", 300, 44, p=p * 2)
    return (120, 180, 235), (250, 210, 170)


def s1b(d, t, T):
    p = t / T
    ground_scene(d, 860)
    drop = ease(p / 0.18)
    car(d, 360, 1010, 1.6, wheel_s=0, drop=drop)
    if 0.15 < p < 0.6:
        sparks(d, 200, 1000, t, 18, spread=160)
        sparks(d, 520, 1000, t, 18, seed=9, spread=160)
        for i in range(8):
            d.ell(150 + i * 60, 1000 - (p - 0.15) * 160, 26 + (p * 60), 18 + p * 30, (200, 190, 170, int(140 * (1 - p))))
    if p > 0.2:
        d.text(W / 2, 420, "THUD!", 96 * (1 + 0.15 * (1 - ease((p - 0.2) * 5))), (255, 235, 80), stroke=6)
    return (110, 165, 225), (240, 200, 160)


def top_car(d, x, y, c, w=110, h=56):
    d.rect(x + 5, y + 7, x + w + 5, y + h + 7, (0, 0, 0, 90), r=16)
    d.rect(x, y, x + w, y + h, c, r=16)
    d.rect(x + w * 0.55, y + 7, x + w * 0.78, y + h - 7, (150, 205, 240), r=6)
    d.rect(x + 8, y + 6, x + w * 0.45, y + 14, (255, 255, 255, 70), r=4)


def s2a(d, t, T):
    p = t / T
    d.rect(0, 380, W, 1020, (64, 66, 76))
    for lane in range(1, 5):
        y = 380 + lane * 128
        for i in range(10):
            d.rect(i * 90 - (p * 120) % 90, y - 4, i * 90 + 45 - (p * 120) % 90, y + 4, (220, 220, 220))
    rnd = random.Random(7)
    cols = [(226, 58, 52), (60, 140, 230), (250, 200, 60), (240, 240, 240), (60, 180, 110), (150, 90, 200)]
    off = -p * 160
    for lane in range(5):
        x = -60 + rnd.uniform(0, 40)
        while x < W + 200:
            if rnd.random() < 0.12:
                d.rect(x + off, 400 + lane * 128, x + off + 230, 480 + lane * 128, (240, 160, 40), r=12)
                x += 250
            else:
                top_car(d, x + off, 412 + lane * 128, rnd.choice(cols))
                x += 130
    d.rect(0, 360, W, 380, (120, 160, 90))
    d.rect(0, 1020, W, 1040, (120, 160, 90))
    stamp(d, "GRIDLOCK", 270, (p - 0.35))
    return (120, 175, 110), (90, 140, 80)


def s2b(d, t, T):
    p = t / T
    d.rect(0, 930, W, H, (110, 95, 80))
    for i in range(12):
        d.rect(i * 70 - (p * 50) % 70, 940, i * 70 + 40 - (p * 50) % 70, 960, (90, 70, 50))
    d.rect(0, 920, W, 934, (170, 170, 180))
    x = 60 - 140 * (1 - (1 - p) ** 2)
    d.rect(x, 640, x + 380, 920, (40, 110, 200), r=24)
    d.rect(x + 20, 590, x + 160, 650, (30, 85, 160), r=12)
    for i in range(3):
        d.rect(x + 40 + i * 110, 690, x + 120 + i * 110, 770, (170, 220, 250), r=10)
    d.rect(x + 400, 660, x + 820, 920, (220, 220, 225), r=22)
    for i in range(3):
        d.rect(x + 430 + i * 130, 700, x + 520 + i * 130, 770, (170, 220, 250), r=10)
    d.rect(x, 880, x + 820, 900, (250, 200, 40))
    sparks(d, x + 120, 920, t, 16, spread=110)
    sparks(d, x + 330, 920, t, 16, seed=4, spread=110)
    sparks(d, x + 600, 920, t, 16, seed=8, spread=110)
    label(d, "NO WHEELS = NO TRAINS", 330, 40, p=p * 2)
    return (150, 190, 230), (230, 220, 200)


def s3a(d, t, T):
    p = t / T
    cx, cy = 360, 700
    d.ell(cx, cy + 300, 120, 30, (0, 0, 0, 60))
    d.rect(cx - 70, cy - 470, cx + 70, cy - 200, (90, 60, 40), r=30)
    d.rect(cx - 70, cy + 200, cx + 70, cy + 470, (90, 60, 40), r=30)
    d.ell(cx, cy, 250, 250, (200, 170, 90))
    d.ell(cx, cy, 228, 228, (30, 34, 48))
    speed = max(0.0, 1 - ease((p - 0.4) / 0.4))
    a = t * 2.2 * speed + (0 if speed > 0 else 0)
    fade = lambda k: 255 * (1 - ease((p - 0.35 - k * 0.1) / 0.15))
    gear(d, cx - 70, cy - 40, 95, 14, a, (220, 180, 70), fade(0))
    gear(d, cx + 85, cy + 30, 70, 10, -a * 1.36 + 0.2, (200, 200, 210), fade(1))
    gear(d, cx - 10, cy + 120, 55, 8, a * 1.7, (230, 140, 60), fade(2))
    gear(d, cx + 60, cy - 120, 45, 7, -a * 2.1, (220, 180, 70), fade(3))
    d.ell(cx, cy, 228, 228, None, outline=(255, 255, 255, 60), w=6)
    label(d, "GEARS = WHEELS WITH TEETH", 200, 36, p=p * 2)
    return (40, 50, 80), (20, 24, 40)


def s3b(d, t, T):
    p = t / T
    d.rect(80, 420, 640, 940, (55, 60, 72), r=40)
    d.rect(80, 420, 640, 450, (255, 255, 255, 30), r=40)
    speed = max(0.0, 1 - ease((p - 0.3) / 0.5))
    a = t * 3 * speed
    gear(d, 250, 620, 120, 16, a, (200, 200, 210))
    gear(d, 450, 750, 90, 12, -a * 1.33 + 0.13, (220, 180, 70))
    gear(d, 280, 860, 70, 10, -a * 1.7, (230, 140, 60))
    d.text(360, 340, "ENGINES", 54, (255, 255, 255), stroke=4)
    if p > 0.55:
        stamp(d, "STOPPED", 1010, p - 0.55)
    return (50, 60, 90), (25, 28, 45)


def s4a(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (60, 64, 76))
    d.rect(60, 380, 660, 1000, (90, 96, 110), r=30)
    cx, cy, r = 360, 690, 240
    speed = max(0.0, 1 - ease(p / 0.8))
    a = 8 * (t - t * t / (2 * T * 0.8)) if p < 0.8 else 8 * (T * 0.8) / 2
    d.ell(cx, cy, r + 14, r + 14, (50, 54, 64))
    for k in range(18):
        b = a + k * 2 * math.pi / 18
        p1 = (cx + math.cos(b) * 60, cy + math.sin(b) * 60)
        p2 = (cx + math.cos(b + 0.25) * r, cy + math.sin(b + 0.25) * r)
        p3 = (cx + math.cos(b + 0.45) * r, cy + math.sin(b + 0.45) * r)
        d.poly([p1, p2, p3], (180, 190, 205) if k % 2 else (150, 160, 175))
    d.ball(cx, cy, 60, (120, 130, 150))
    blink = int(t * 4) % 2 == 0 and p > 0.4
    d.ell(140, 440, 26, 26, (255, 60, 50) if blink else (110, 40, 40))
    d.ell(580, 440, 26, 26, (255, 60, 50) if blink else (110, 40, 40))
    label(d, "POWER PLANT TURBINE", 270, 38, p=p * 2)
    return (60, 66, 84), (30, 32, 42)


def s4b(d, t, T):
    p = t / T
    rnd = random.Random(11)
    for _ in range(80):
        d.ell(rnd.uniform(0, W), rnd.uniform(0, H), 1.6, 1.6, (255, 255, 255, 180))
    cx, cy, r = 360, 700, 300
    d.ell(cx, cy, r + 18, r + 18, (60, 120, 220, 60))
    d.ell(cx, cy, r, r, (16, 34, 78))
    rnd = random.Random(5)
    blobs = [(-120, -100, 120, 80), (60, -40, 140, 110), (-60, 140, 90, 70), (150, 170, 60, 50)]
    for bx, by, rx, ry in blobs:
        d.ell(cx + bx, cy + by, rx, ry, (36, 62, 70))
    sweep = -r + ease(p / 0.85) * 2.4 * r
    for bx, by, rx, ry in blobs:
        for _ in range(55):
            a, rr = rnd.uniform(0, 6.28), rnd.random() ** 0.5
            lx, ly = cx + bx + math.cos(a) * rx * rr * 0.9, cy + by + math.sin(a) * ry * rr * 0.9
            if lx - cx > sweep:
                d.ell(lx, ly, 7, 7, (255, 200, 80, 70))
                d.ell(lx, ly, 3.5, 3.5, (255, 235, 150))
    d.ell(cx, cy, r, r, None, outline=(120, 170, 255, 120), w=4)
    if p > 0.75:
        label(d, "LIGHTS OUT", 1140, 56, fill=(255, 220, 120), p=(p - 0.75) * 2)
    return (4, 6, 16), (10, 12, 26)


def crate(d, x, y, c=(190, 140, 80), s=60):
    d.rect(x, y, x + s, y + s, c, r=6)
    d.line([(x + 6, y + 6), (x + s - 6, y + s - 6)], shade(c, 0.75), 6)
    d.line([(x + s - 6, y + 6), (x + 6, y + s - 6)], shade(c, 0.75), 6)


def s5a(d, t, T):
    p = t / T
    ground_scene(d, 860)
    d.shadow(360, 990, 330, 20)
    d.rect(40, 700, 520, 985, (240, 240, 245), r=14)
    d.text(280, 840, "FOOD CO.", 50, (60, 140, 90))
    d.rect(530, 790, 690, 985, (60, 140, 230), r=20)
    d.rect(590, 810, 670, 880, (170, 220, 250), r=10)
    rnd = random.Random(2)
    for i in range(6):
        q = ease((p - 0.15 - i * 0.07) / 0.35)
        if q <= 0:
            continue
        x = 40 - q * (60 + i * 30) - 10
        y = 760 + i % 3 * 60 + q * (985 - 60 - (760 + i % 3 * 60))
        crate(d, x, y)
    for i in range(10):
        q = ease((p - 0.25 - i * 0.04) / 0.3)
        if q > 0:
            d.ball(40 - q * rnd.uniform(40, 240), 760 + q * (970 - 760) + rnd.uniform(-5, 5), 16,
                   rnd.choice([(230, 50, 50), (250, 160, 40), (120, 200, 60)]))
    label(d, "NO TRUCKS. NO DELIVERIES.", 300, 38, p=p * 2)
    return (130, 185, 235), (240, 215, 180)


def s5b(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (200, 200, 205))
    for row in range(4):
        y = 430 + row * 150
        d.rect(40, y + 110, 680, y + 126, (150, 150, 160))
        rnd = random.Random(row)
        for i in range(9):
            gone = rnd.random() < ease(p / 0.75) * 1.05
            if not gone:
                c = rnd.choice([(230, 70, 60), (250, 190, 50), (70, 150, 230), (80, 190, 110)])
                d.rect(55 + i * 70, y + 30, 105 + i * 70, y + 110, c, r=6)
    day = 1 + min(2, int(p * 3))
    d.text(360, 330, f"DAY {day}", 80, (255, 255, 255), stroke=6)
    person(d, 360, 1150, 0.85, mood="shock" if p > 0.6 else "neutral")
    return (240, 240, 235), (210, 210, 215)


def plane(d, x, y, sc=1.0):
    d.shadow(x, y + 60 * sc, 330 * sc, 18 * sc)
    d.poly([(x + 230 * sc, y - 20 * sc), (x + 330 * sc, y - 170 * sc), (x + 360 * sc, y - 170 * sc),
            (x + 330 * sc, y - 10 * sc)], (220, 60, 60))
    d.rect(x - 330 * sc, y - 60 * sc, x + 340 * sc, y + 55 * sc, (240, 242, 248), r=55 * sc)
    d.rect(x - 330 * sc, y + 10 * sc, x + 340 * sc, y + 55 * sc, (200, 205, 215), r=40 * sc)
    for i in range(9):
        d.ell(x - 200 * sc + i * 55 * sc, y - 20 * sc, 10 * sc, 12 * sc, (90, 140, 200))
    d.ell(x - 300 * sc, y - 25 * sc, 30 * sc, 18 * sc, (90, 140, 200))
    d.poly([(x - 40 * sc, y + 20 * sc), (x + 100 * sc, y + 20 * sc), (x + 40 * sc, y + 110 * sc),
            (x - 100 * sc, y + 110 * sc)], (190, 195, 210))


def s6a(d, t, T):
    p = t / T
    d.rect(0, 860, W, H, (80, 84, 92))
    for i in range(8):
        d.rect(i * 110 - p * 40, 1060, i * 110 + 60 - p * 40, 1074, (240, 240, 240))
    plane(d, 360, 940, 1.0 - 0.15 * ease(p))
    sparks(d, 300, 1000, t, 8, spread=60)
    label(d, "NO LANDING GEAR", 300, 44, p=p * 2)
    return (140, 190, 240), (220, 230, 240)


def s6b(d, t, T):
    p = t / T
    cx, cy = 360, 700
    d.ell(cx, cy, 300, 300, (200, 205, 215))
    d.ell(cx, cy, 270, 270, (40, 44, 54))
    w = 9 * max(0.0, 1 - ease(p / 0.8))
    a = 9 * (t - t * t / (2 * T * 0.8)) if p < 0.8 else 9 * T * 0.4
    for k in range(20):
        b = a + k * 2 * math.pi / 20
        pts = [(cx + math.cos(b) * 70, cy + math.sin(b) * 70),
               (cx + math.cos(b + 0.3) * 260, cy + math.sin(b + 0.3) * 260),
               (cx + math.cos(b + 0.42) * 260, cy + math.sin(b + 0.42) * 260),
               (cx + math.cos(b + 0.1) * 70, cy + math.sin(b + 0.1) * 70)]
        d.poly(pts, (170, 175, 190) if k % 2 else (140, 145, 160))
    d.ball(cx, cy, 72, (200, 205, 215))
    d.d.arc([(cx - 20) * K, (cy - 20) * K, (cx + 20) * K, (cy + 20) * K], 0, 300, fill=(60, 60, 70), width=6 * K)
    label(d, "JET ENGINE = SPINNING WHEELS", 260, 34, p=p * 2)
    return (120, 160, 210), (60, 80, 120)


def sledge(d, x, ground, sc=1.0):
    d.shadow(x + 120 * sc, ground + 4, 170 * sc, 14 * sc)
    d.rect(x - 40 * sc, ground - 26 * sc, x + 300 * sc, ground - 6 * sc, (150, 100, 60), r=10 * sc)
    d.d.arc([(x - 60 * sc) * K, (ground - 40 * sc) * K, (x + 0 * sc) * K, (ground + 2 * sc) * K], 90, 270,
            fill=(120, 80, 45), width=int(10 * sc * K))
    d.rect(x + 120 * sc, ground - 260 * sc, x + 260 * sc, ground - 26 * sc, (235, 238, 245), r=14 * sc)
    d.line([(x + 135 * sc, ground - 180 * sc), (x + 245 * sc, ground - 180 * sc)], (190, 195, 205), 4 * sc)
    d.rect(x + 240 * sc, ground - 240 * sc, x + 250 * sc, ground - 200 * sc, (160, 165, 175), r=4)
    crate(d, x - 10 * sc, ground - 96 * sc, s=70 * sc)
    crate(d, x + 50 * sc, ground - 86 * sc, (200, 160, 90), s=60 * sc)
    return (x - 50 * sc, ground - 20 * sc)


def s7a(d, t, T):
    p = t / T
    ground_scene(d, 900, road=(150, 150, 155))
    jitter = math.sin(t * 9) * 4
    x0 = 40 + p * 40
    hook = sledge(d, x0 + jitter * 0.3, 1080, 0.95)
    hands = person(d, 560 + p * 30, 1080, 0.95, mood="strain", arms="down", lean=0.6)
    d.line([hook, (hands[0][0] - 10, hands[0][1] + 10)], (220, 200, 140), 6)
    label(d, "THE ANCIENT WAY", 330, 46, p=p * 2)
    return (190, 205, 225), (225, 215, 200)


def s7b(d, t, T):
    p = t / T
    d.rect(0, 900, W, H, (130, 130, 136))
    for i in range(14):
        d.rect(i * 60 - (t * 20) % 60, 960, i * 60 + 30 - (t * 20) % 60, 966, (110, 110, 116))
    d.rect(-20, 760, 760, 860, (150, 100, 60), r=20)
    d.rect(-20, 860, 760, 905, (120, 80, 45), r=12)
    for i in range(6):
        d.line([(120 * i, 770), (120 * i + 60, 850)], (125, 82, 48), 5)
    rnd = random.Random(int(t * 10))
    for _ in range(14):
        d.ell(rnd.uniform(0, W), 900 - rnd.uniform(0, 120), rnd.uniform(14, 40), rnd.uniform(10, 24),
              (205, 195, 170, 120))
    d.text(360, 480, "SCRRRAPE", 84 * (1 + 0.03 * math.sin(t * 30)), (255, 235, 80), stroke=6)
    return (170, 175, 185), (140, 140, 150)


def s8a(d, t, T):
    p = t / T
    d.text(360, 330, "HUMANS", 54, (255, 255, 255), stroke=4)
    d.text(360, 390, "~300,000 YEARS", 40, (180, 220, 255), stroke=3)
    L = 600 * ease(p / 0.45)
    d.rect(60, 430, 60 + L, 490, (80, 170, 255), r=18)
    if p > 0.45:
        q = ease((p - 0.45) / 0.3)
        d.text(360, 640, "THE WHEEL", 54, (255, 255, 255), stroke=4)
        d.text(360, 700, "~5,500 YEARS", 40, (255, 210, 120), stroke=3)
        d.rect(60, 740, 60 + max(14, 11 * q), 800, (255, 170, 60), r=6)
        if p > 0.75:
            d.text(360, 950, "THAT'S ONLY 2%!", 60, (255, 235, 80), stroke=5)
    return (40, 40, 80), (90, 50, 90)


def cart(d, x, y, sc=1.0):
    d.shadow(x, y + 80 * sc, 200 * sc, 16 * sc)
    d.rect(x - 200 * sc, y - 90 * sc, x + 200 * sc, y + 10 * sc, (160, 110, 65), r=10 * sc)
    for i in range(5):
        d.line([(x - 180 * sc + i * 90 * sc, y - 85 * sc), (x - 180 * sc + i * 90 * sc, y + 5 * sc)], (130, 85, 50), 6 * sc)
    for wx in (x - 120 * sc, x + 120 * sc):
        d.ell(wx, y + 20 * sc, 70 * sc, 70 * sc, (120, 80, 45))
        d.ell(wx, y + 20 * sc, 52 * sc, 52 * sc, (190, 150, 100))
        d.ell(wx, y + 20 * sc, 14 * sc, 14 * sc, (100, 65, 40))


def s8b(d, t, T):
    p = t / T
    cart(d, 360, 760, 1.2)
    q = ease((p - 0.3) / 0.25)
    if q > 0:
        d.line([(160, 520), (160 + 400 * q, 520 + 400 * q)], (235, 50, 50), 30)
        d.line([(560, 520), (560 - 400 * q, 520 + 400 * q)], (235, 50, 50), 30)
    label(d, "NOT FOR CARTS...", 330, 50, p=p * 2)
    return (235, 210, 160), (205, 160, 110)


def s9a(d, t, T):
    p = t / T
    cx, base = 360, 900
    d.shadow(cx, base + 140, 280, 30)
    d.rect(cx - 30, base + 20, cx + 30, base + 140, (110, 100, 95))
    d.ell(cx, base + 20, 260, 60, (130, 120, 115))
    d.ell(cx, base, 260, 60, (165, 155, 150))
    for k in range(8):
        a = t * 6 + k * math.pi / 4
        if math.sin(a) > 0:
            d.ell(cx + math.cos(a) * 220, base + math.sin(a) * 50, 10, 6, (120, 110, 105))
    hgt = 80 + 170 * ease(p / 0.8)
    wid = 120 - 20 * ease(p)
    clay = (190, 110, 70)
    d.ell(cx, base - 4, wid, 26, shade(clay, 0.8))
    d.rect(cx - wid, base - hgt, cx + wid, base, clay)
    d.rect(cx - wid * 0.9, base - hgt - 10, cx + wid * 0.9, base - hgt + 30, clay, r=20)
    d.ell(cx, base - hgt, wid * 0.75, 18, shade(clay, 0.6))
    off = math.sin(t * 6) * 6
    d.rect(cx - wid - 90 + off, base - hgt * 0.6, cx - wid + 10 + off, base - hgt * 0.6 + 70, SKIN, r=34)
    d.rect(cx + wid - 10 - off, base - hgt * 0.6, cx + wid + 90 - off, base - hgt * 0.6 + 70, SKIN, r=34)
    d.rect(cx - 30 + 20, base - hgt * 0.6, cx - 30 + 32, base - hgt * 0.6 + 40, (255, 255, 255, 80), r=6)
    label(d, "...BUT FOR POTTERY!", 330, 48, p=p * 2)
    return (230, 190, 140), (190, 130, 90)


def s9b(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (150, 120, 90))
    d.rect(40, 420, 680, 1000, (190, 160, 125), r=10)
    for i in range(6):
        d.line([(60, 480 + i * 90), (660, 480 + i * 90)], (170, 140, 105), 4)
    lift = ease(p / 0.4)
    hands = person(d, 360, 1150, 1.05, mood="happy", arms="up")
    wy = hands[0][1] - 100 - 20 * lift
    wheel(d, 360, wy, 95, t * 1.5)
    if p > 0.3:
        g = 0.5 + 0.5 * math.sin(t * 8)
        d.ell(560, 360, 70 + 10 * g, 70 + 10 * g, (255, 240, 120, 90))
        d.ball(560, 350, 46, (255, 236, 120))
        d.rect(540, 392, 580, 430, (160, 160, 170), r=6)
    label(d, "REINVENTED IN A WEEK", 250, 42, p=p * 2)
    return (200, 170, 130), (150, 115, 85)


def s10a(d, t, T):
    p = t / T
    ground_scene(d, 860)
    ws = ease((p - 0.1) / 0.45)
    drop = 1 - ease((p - 0.45) / 0.3)
    car(d, 360, 1010, 1.45, wheel_s=ws, drop=drop, ang=t * 5 * (p > 0.75))
    rnd = random.Random(4)
    if 0.05 < p < 0.8:
        for wx in (360 - 239 + 101, 360 + 239 - 101):
            for _ in range(10):
                a, rr = rnd.uniform(0, 6.28), rnd.uniform(40, 120) * (1 - p)
                d.ell(wx + math.cos(a) * rr, 960 + math.sin(a) * rr, 6, 6, (255, 240, 140, 220))
    label(d, "WHEELS ARE BACK", 330, 46, p=(p - 0.4) * 2)
    return (120, 180, 235), (250, 210, 170)


def s10b(d, t, T):
    p = t / T
    rnd = random.Random(21)
    x = 0
    while x < W:
        bw, bh = rnd.uniform(70, 130), rnd.uniform(250, 560)
        d.rect(x, 900 - bh, x + bw - 6, 900, (60, 50, 90))
        for wy in range(int(900 - bh + 20), 880, 40):
            for wx in range(int(x + 10), int(x + bw - 20), 28):
                if rnd.random() < ease(p / 0.6):
                    d.rect(wx, wy, wx + 14, wy + 20, (255, 215, 120))
                else:
                    d.rect(wx, wy, wx + 14, wy + 20, (80, 70, 110))
        x += bw
    tx, ty = 600, 420
    d.line([(tx, ty), (tx, 900)], (230, 230, 240), 10)
    for k in range(3):
        a = t * 3 + k * 2.094
        d.line([(tx, ty), (tx + math.cos(a) * 110, ty + math.sin(a) * 110)], (240, 240, 250), 14)
    ground_scene(d, 900)
    cols = [(226, 58, 52), (60, 140, 230), (250, 200, 60)]
    for i in range(3):
        cx = (i * 330 + t * 260) % (W + 400) - 200
        car(d, cx, 1060 + (i % 2) * 90, 0.6, ang=t * 9, color=cols[i])
    return (250, 140, 90), (120, 70, 140)


def outro(d, t, T):
    p = t / T
    wheel(d, 360, 560, 150 * ease(p * 3), t * 3)
    d.text(360, 820, "NO WHEELS", 78, (255, 255, 255), stroke=5)
    d.text(360, 910, "=", 70, (255, 235, 80), stroke=5)
    d.text(360, 1000, "NO MODERN WORLD", 52, (255, 235, 80), stroke=5)
    return (30, 40, 80), (70, 40, 90)


SHOTS = {"beat_1_a": s1a, "beat_1_b": s1b, "beat_2_a": s2a, "beat_2_b": s2b, "beat_3_a": s3a, "beat_3_b": s3b,
         "beat_4_a": s4a, "beat_4_b": s4b, "beat_5_a": s5a, "beat_5_b": s5b, "beat_6_a": s6a, "beat_6_b": s6b,
         "beat_7_a": s7a, "beat_7_b": s7b, "beat_8_a": s8a, "beat_8_b": s8b, "beat_9_a": s9a, "beat_9_b": s9b,
         "beat_10_a": s10a, "beat_10_b": s10b, "outro": outro}


# --------------------------------------------------------------------------- timeline
def build_timeline():
    beats = json.load(open(os.path.join(HERE, "beats.json")))["beats"]
    timing = {x["beat_id"]: x for x in json.load(open(os.path.join(HERE, "audio", "timing.json")))}
    shots, words = [], []
    for b in beats:
        tm = timing[b["beat_id"]]
        # optional per-shot "share" of the beat (default: equal split) to land cuts on the right words
        shares = [s.get("share") for s in b["shots"]]
        rest = 1 - sum(x for x in shares if x)
        free = sum(1 for x in shares if not x)
        shares = [x if x else rest / free for x in shares]
        st = tm["start"]
        for s, sh in zip(b["shots"], shares):
            shots.append({"id": s["shot_id"], "start": st, "dur": tm["dur"] * sh,
                          "impact": s.get("zoom_impact", False)})
            st += tm["dur"] * sh
        ws = b["narration"].split()
        speak = tm["dur"] - 0.25
        weights = [len(w) + 2 for w in ws]
        tot, acc = sum(weights), 0
        group = []
        for i, w in enumerate(ws):
            st = tm["start"] + speak * acc / tot
            acc += weights[i]
            words.append({"w": w, "start": st, "end": tm["start"] + speak * acc / tot, "beat": b["beat_id"]})
    narr_end = shots[-1]["start"] + shots[-1]["dur"]
    shots.append({"id": "outro", "start": narr_end, "dur": OUTRO, "impact": True})
    # caption chunks of up to 3 words, never crossing a beat
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) == 3 or cur[-1]["beat"] != w["beat"] or cur[-1]["w"][-1] in ".,:?!"):
            chunks.append(cur); cur = []
        cur.append(w)
    chunks.append(cur)
    return shots, chunks, narr_end + OUTRO


def draw_caption(d, chunks, T):
    for ch in chunks:
        if ch[0]["start"] <= T < ch[-1]["end"] + 0.05:
            texts = [w["w"].upper() for w in ch]
            size = 58
            gap = font(size).getlength(" ") / K
            widths = [font(size).getlength(s) / K for s in texts]
            total = sum(widths) + gap * (len(texts) - 1)
            if total > W - 60:
                size = size * (W - 60) / total
                widths = [x * (W - 60) / total for x in widths]; gap *= (W - 60) / total; total = W - 60
            x = W / 2 - total / 2
            pop = 1 + 0.12 * (1 - ease((T - ch[0]["start"]) / 0.12))
            for w, s, wd in zip(ch, texts, widths):
                active = w["start"] <= T < w["end"] + 0.05
                d.text(x + wd / 2, 1150, s, size * (pop if active else 1),
                       (255, 230, 40) if active else (255, 255, 255), stroke=6)
                x += wd + gap
            return


SHOTS_TL, CHUNKS, TOTAL = None, None, None
BG = {}


def init():
    global SHOTS_TL, CHUNKS, TOTAL
    SHOTS_TL, CHUNKS, TOTAL = build_timeline()


def render(fi):
    T = fi / FPS
    shot = SHOTS_TL[-1]
    for s in SHOTS_TL:
        if s["start"] <= T < s["start"] + s["dur"]:
            shot = s
            break
    t = T - shot["start"]
    if shot["id"] not in BG:  # backgrounds are constant per shot; learn once
        BG[shot["id"]] = SHOTS[shot["id"]](D(Image.new("RGB", (W * K, H * K))), 0.0, shot["dur"])
    bg = BG[shot["id"]]
    img = gradient(*bg)
    d = D(img)
    SHOTS[shot["id"]](d, t, shot["dur"])
    d.rect(0, 40, W, 130, (0, 0, 0, 110))
    d.text(W / 2, 86, "WHAT IF THERE WERE NO WHEELS?", 34, (255, 255, 255), stroke=3)
    draw_caption(d, CHUNKS, T)
    img = img.reduce(K)
    # slow push-in on every shot + punch zoom/shake on impact shots
    z = 1 + 0.04 * (t / shot["dur"])
    dx = dy = 0
    if shot["impact"] and t < 0.45:
        z += 0.08 * (1 - t / 0.45)
        dx, dy = math.sin(fi * 2.1) * 10 * (1 - t / 0.45), math.cos(fi * 1.7) * 10 * (1 - t / 0.45)
    cw, chh = W / z, H / z
    x0, y0 = (W - cw) / 2 + dx, (H - chh) / 2 + dy
    img = img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + chh))
    if t < 0.12:  # quick flash on every cut
        img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.55 * (1 - t / 0.12))
    return img.tobytes()


# --------------------------------------------------------------------------- audio
def make_audio(total, out_path):
    narr, sr = sf.read(os.path.join(HERE, "audio", "narration.wav"))
    n = int(total * sr)
    tt = np.arange(n) / sr
    music = np.zeros(n)
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [261.63, 329.63, 392.0], [196.0, 246.94, 293.66]]
    bar = 2.0
    for i in range(int(total / bar) + 1):
        a, b = int(i * bar * sr), min(n, int((i + 1) * bar * sr))
        seg = tt[a:b] - i * bar
        env = np.minimum(1, seg / 0.3) * np.exp(-seg * 0.6)
        for f in chords[i % 4]:
            music[a:b] += np.sin(2 * np.pi * f * seg) * env * 0.05 + np.sin(2 * np.pi * f / 2 * seg) * env * 0.04
        for k in range(4):  # soft pulse
            s0 = a + int(k * 0.5 * sr)
            L = min(int(0.12 * sr), n - s0)
            if L > 0:
                music[s0:s0 + L] += np.sin(2 * np.pi * chords[i % 4][0] / 4 * np.arange(L) / sr) * np.exp(-np.arange(L) / sr * 30) * 0.18
    sfx = np.zeros(n)
    rng = np.random.default_rng(0)
    shots, _, _ = build_timeline()
    for s in shots[1:]:
        a = int(max(0, s["start"] - 0.12) * sr)
        L = min(int(0.3 * sr), n - a)
        noise = rng.standard_normal(L)
        noise = np.convolve(noise, np.ones(30) / 30, mode="same")
        sfx[a:a + L] += noise * np.sin(np.linspace(0, np.pi, L)) * 0.5
        if s["impact"]:
            a = int(s["start"] * sr)
            L = min(int(0.4 * sr), n - a)
            x = np.arange(L) / sr
            sfx[a:a + L] += np.sin(2 * np.pi * (90 - 50 * x) * x) * np.exp(-x * 9) * 0.6
    voice = np.zeros(n)
    voice[:min(n, len(narr))] = narr[:n]
    duck = 1 - 0.55 * (np.convolve(np.abs(voice) > 0.02, np.ones(sr // 4) / (sr // 4), mode="same") > 0.05)
    mixd = voice * 1.1 + music * duck * 0.9 + sfx * 0.35
    mixd /= max(1.0, np.abs(mixd).max() / 0.95)
    sf.write(out_path, mixd.astype(np.float32), sr)


def main():
    init()
    nframes = int(round(TOTAL * FPS))
    audio = os.path.join(HERE, "audio", "mix.wav")
    make_audio(TOTAL, audio)
    out = os.path.join(HERE, "final.mp4")
    if len(sys.argv) > 1:  # preview stills: render_free.py 1.5 12.0 ...
        for s in sys.argv[1:]:
            fi = int(float(s) * FPS)
            Image.frombytes("RGB", (W, H), render(fi)).save(os.path.join(HERE, f"preview_{s}.png"))
        return
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out],
                          stdin=subprocess.PIPE)
    with Pool(os.cpu_count(), initializer=init) as pool:
        for i, frame in enumerate(pool.imap(render, range(nframes), chunksize=8)):
            ff.stdin.write(frame)
            if i % 300 == 0:
                print(f"frame {i}/{nframes}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("wrote", out, f"{TOTAL:.1f}s")


if __name__ == "__main__":
    main()
