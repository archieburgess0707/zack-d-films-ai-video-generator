"""Procedural scenes for the no_moon short (rendered by scripts/free_render.py)."""
import importlib.util
import os

from free_render import *  # noqa: F401,F403

# reuse globe, stars, sun, house, tree and grass from the Earth video
_spec = importlib.util.spec_from_file_location(
    "earth_shots", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "earth_stops_spinning", "shots.py"))
E = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(E)

NIGHT = ((10, 14, 40), (30, 30, 70))
SEA = (30, 80, 150)


def moon(d, x, y, r, alpha=255):
    if alpha <= 3:
        return
    a = int(alpha)
    d.ell(x, y, r * 1.3, r * 1.3, (230, 235, 255, int(a * 0.18)))
    d.ell(x, y, r, r, (200, 200, 205, a))
    d.ell(x - r * 0.06, y - r * 0.06, r * 0.93, r * 0.93, (232, 232, 236, a))
    for cx, cy, cr in ((-0.35, -0.2, 0.18), (0.25, 0.3, 0.22), (0.3, -0.35, 0.12), (-0.2, 0.45, 0.1), (0.0, 0.0, 0.08)):
        d.ell(x + cx * r, y + cy * r, cr * r, cr * r, (190, 190, 198, a))
        d.ell(x + cx * r + cr * r * 0.15, y + cy * r + cr * r * 0.15, cr * r * 0.8, cr * r * 0.8, (210, 210, 216, a))


def sea(d, y0, t, col=SEA, amp=10):
    d.rect(0, y0, W, H, col)
    for row in range(5):
        yy = y0 + 20 + row * 60
        for k in range(10):
            x = (k * 90 + t * (30 + row * 10)) % (W + 90) - 45
            d.ell(x, yy + amp * math.sin(t * 2 + k), 40, 8, shade(col, 1.25))


def crab(d, x, y, s=1.0, sad=False):
    c = (230, 80, 60)
    for side in (-1, 1):
        for k in range(3):
            d.line([(x + side * 30 * s, y + 10 * s), (x + side * (60 + k * 6) * s, y + (20 + k * 12) * s)], shade(c, 0.8), 6 * s)
        d.line([(x + side * 35 * s, y - 10 * s), (x + side * 60 * s, y - 40 * s)], shade(c, 0.8), 8 * s)
        d.ell(x + side * 68 * s, y - 50 * s, 18 * s, 14 * s, c)
    d.ell(x, y, 50 * s, 32 * s, c)
    d.ell(x - 12 * s, y - 10 * s, 26 * s, 12 * s, (255, 255, 255, 60))
    for ex in (-14, 14):
        d.line([(x + ex * s, y - 24 * s), (x + ex * s, y - 44 * s)], shade(c, 0.8), 5 * s)
        d.ell(x + ex * s, y - 48 * s, 9 * s, 9 * s, (255, 255, 255))
        d.ell(x + ex * s, y - 46 * s, 4.5 * s, 4.5 * s, (20, 20, 20))
    if sad:
        d.d.arc([(x - 12 * s) * K, (y + 4 * s) * K, (x + 12 * s) * K, (y + 20 * s) * K], 200, 340,
                fill=(90, 20, 20), width=int(4 * s * K))
    else:
        d.d.arc([(x - 12 * s) * K, (y - 6 * s) * K, (x + 12 * s) * K, (y + 10 * s) * K], 20, 160,
                fill=(90, 20, 20), width=int(4 * s * K))


def starfish(d, x, y, r, col=(250, 150, 60)):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    d.poly(pts, col)


def coral(d, x, y, s, col, t):
    for k, (dx, h) in enumerate(((-40, 140), (0, 190), (40, 150), (-70, 90), (70, 100))):
        sway = 6 * math.sin(t * 1.5 + k)
        d.line([(x + dx * 0.3 * s, y), (x + dx * s + sway, y - h * s)], col, 22 * s)
        d.ell(x + dx * s + sway, y - h * s, 16 * s, 16 * s, shade(col, 1.15))


# --------------------------------------------------------------------------- beat 1
def s1a(d, t, T):
    p = t / T
    E.stars(d)
    moon(d, 520, 330, 110, 255 * (1 - ease((p - 0.3) / 0.5)))
    sea(d, 900, t)
    label(d, "THE MOON... GONE", 640, 46, p=(p - 0.6) * 3)
    return NIGHT


def s1b(d, t, T):
    p = t / T
    E.stars(d)
    sea(d, 700, t, amp=18)
    d.text(360, 420, "THE OCEAN?", 80, (150, 220, 255), stroke=6)
    return NIGHT


# --------------------------------------------------------------------------- beat 2
def s2a(d, t, T):
    p = t / T
    E.stars(d)
    d.ell(300, 700, 250 + 15 * math.sin(t * 2), 200, (80, 160, 255, 90))
    E.earth(d, 300, 700, 190, t * 0.6, glow=False)
    moon(d, 620, 700, 55)
    for k in range(3):
        y = 660 + k * 40
        d.line([(560, y), (470, y)], (255, 235, 80, 200), 6)
        d.poly([(470, y - 12), (470, y + 12), (450, y)], (255, 235, 80, 200))
    label(d, "THE MOON PULLS THE OCEANS", 300, 36, p=p * 2)
    return NIGHT


def s2b(d, t, T):
    p = t / T
    lvl = 520 + 330 * ease((p - 0.2) / 0.6)
    d.rect(0, lvl, W, H, SEA)
    d.rect(330, 300, 390, 1100, (230, 230, 235), r=10)
    for k in range(9):
        d.rect(330, 340 + k * 80, 370, 348 + k * 80, (60, 60, 70))
    d.text(240, 520, "NOW", 40, (255, 255, 255), stroke=3)
    d.line([(280, 520), (330, 520)], (255, 255, 255), 5)
    if p > 0.6:
        d.text(500, 850, "1/3", 70, (255, 235, 80), stroke=5)
    sea(d, lvl, t)
    return (60, 80, 130), (30, 40, 80)


# --------------------------------------------------------------------------- beat 3
def s3a(d, t, T):
    p = t / T
    d.rect(0, 860, W, H, (200, 185, 150))
    for x, y, rx, ry in ((60, 860, 140, 90), (660, 870, 160, 110), (360, 1000, 200, 60)):
        d.ell(x, y, rx, ry, (120, 120, 130))
        d.ell(x - 20, y - 20, rx * 0.7, ry * 0.5, (150, 150, 160))
    lvl = 0.9 - 0.75 * ease(p / 0.8)
    d.ell(360, 880, 230, 70 * max(0.15, lvl) + 10, (60, 130, 200))
    crab(d, 290, 860, 0.8, sad=p > 0.5)
    starfish(d, 470, 880, 34)
    label(d, "ROCK POOLS DRY OUT", 300, 44, p=p * 2)
    return (130, 180, 230), (210, 220, 230)


def s3b(d, t, T):
    p = t / T
    d.rect(0, 900, W, H, (200, 185, 150))
    crab(d, 360, 760, 2.0, sad=True)
    d.ell(300, 700, 8, 14, (120, 190, 255))
    label(d, "SEA LIFE STRUGGLES", 320, 46, p=p * 2)
    return (130, 180, 230), (210, 220, 230)


# --------------------------------------------------------------------------- beat 4
def s4a(d, t, T):
    p = t / T
    E.stars(d)
    q = ease((p - 0.2) / 0.6)
    moon(d, 560, 300, 80, 255 * (1 - q))
    E.grass(d, 950)
    E.house(d, 250, 950, 1.0)
    E.tree(d, 560, 950, 0.9)
    d.rect(0, 0, W, H, (0, 0, 10, int(200 * q)))
    return NIGHT


def s4b(d, t, T):
    p = t / T
    d.rect(0, 0, W, H, (2, 2, 8))
    E.stars(d, 4, 160)
    d.text(360, 640, "JUST STARS", 70, (255, 255, 255), stroke=4)
    return (2, 2, 8), (2, 2, 8)


# --------------------------------------------------------------------------- beat 5
def s5a(d, t, T):
    p = t / T
    d.rect(0, 0, W, H, (10, 40, 90))
    moon(d, 360, 260, 70)
    d.d.polygon([(330 * K, 330 * K), (390 * K, 330 * K), (520 * K, H * K), (200 * K, H * K)], fill=(220, 230, 255, 35))
    d.rect(0, 1040, W, H, (190, 170, 120))
    for x, col in ((150, (250, 110, 120)), (360, (255, 170, 80)), (570, (200, 110, 220))):
        coral(d, x, 1060, 1.0, col, t)
    rnd = random.Random(2)
    for _ in range(60):
        x = rnd.uniform(60, 660)
        y = 1000 - ((rnd.uniform(0, 600) + t * rnd.uniform(40, 90)) % 650)
        d.ell(x, y, 5, 5, (255, 190, 210, 220))
    label(d, "CORALS RELEASE EGGS", 430, 40, p=p * 2)
    return (10, 40, 90), (5, 20, 50)


def s5b(d, t, T):
    p = t / T
    d.rect(0, 0, W, H, (6, 20, 50))
    d.rect(0, 1040, W, H, (150, 135, 100))
    for x, col in ((150, (180, 90, 100)), (360, (190, 130, 70)), (570, (150, 90, 170))):
        coral(d, x, 1060, 1.0, col, t)
    for k in range(3):
        ph = (t * 0.5 + k / 3) % 1
        d.text(200 + k * 160, 760 - ph * 200, "?", 70, (255, 235, 80, int(255 * (1 - ph))))
    label(d, "NO MOON = NO SIGNAL", 360, 44, p=p * 2)
    return (6, 20, 50), (3, 10, 30)


# --------------------------------------------------------------------------- beat 6
def eclipse(d, x, y, cover):
    for k in range(16):
        a = k * math.pi / 8
        d.line([(x + math.cos(a) * 130, y + math.sin(a) * 130), (x + math.cos(a) * 200, y + math.sin(a) * 200)],
               (255, 250, 220, 120), 14)
    d.ell(x, y, 150, 150, (255, 245, 210, 120))
    d.ell(x, y, 125, 125, (255, 220, 110))
    d.ell(x - 250 + 250 * cover, y, 127, 127, (8, 8, 16))


def s6a(d, t, T):
    p = t / T
    E.stars(d, 9, 50)
    eclipse(d, 360, 640, ease(p / 0.7))
    label(d, "TOTAL SOLAR ECLIPSE", 1000, 40, p=p * 2)
    return (8, 8, 20), (8, 8, 20)


def s6b(d, t, T):
    p = t / T
    E.stars(d, 9, 50)
    eclipse(d, 360, 640, 1.0)
    q = ease((p - 0.2) / 0.3)
    if q > 0:
        d.line([(160, 440), (160 + 400 * q, 440 + 400 * q)], (235, 50, 50), 30)
        d.line([(560, 440), (560 - 400 * q, 440 + 400 * q)], (235, 50, 50), 30)
    label(d, "NO MORE ECLIPSES", 1000, 46, fill=(255, 120, 120), p=(p - 0.3) * 2)
    return (8, 8, 20), (8, 8, 20)


# --------------------------------------------------------------------------- beat 7
def phase(d, x, y, r, f):
    """Moon phase icon: f = 0 new .. 0.5 full .. 1 new (a dark disc slides across a lit one)."""
    size = int(2 * r * K)
    lay = Image.new("RGBA", (size, size), (40, 44, 60, 255))
    L = ImageDraw.Draw(lay)
    L.ellipse([0, 0, size - 1, size - 1], fill=(235, 235, 240, 255))
    off = (1 - 2 * abs(f - 0.5)) * size * (1 if f < 0.5 else -1)
    L.ellipse([-off, 0, size - 1 - off, size - 1], fill=(40, 44, 60, 255))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    d.img.paste(lay, (int((x - r) * K), int((y - r) * K)), mask)


def s7a(d, t, T):
    p = t / T
    d.rect(80, 380, 640, 980, (250, 250, 250), r=24)
    d.rect(80, 380, 640, 480, (90, 110, 200), r=24)
    d.rect(80, 450, 640, 480, (90, 110, 200))
    d.text(360, 430, "CALENDAR", 48, (255, 255, 255))
    shown = int(ease(p / 0.8) * 8) + 1
    for k in range(8):
        if k < shown:
            phase(d, 160 + (k % 4) * 133, 600 + (k // 4) * 200, 50, (k + 0.5) / 8)
    return (40, 40, 80), (70, 50, 100)


def s7b(d, t, T):
    p = t / T
    q = ease((p - 0.25) / 0.4)
    d.text(360, 560, "MOON", 120, (235, 235, 240), stroke=6)
    d.text(360, 690, "↓", 80, (255, 235, 80))
    if q > 0:
        d.text(360, 830, "MONTH", 120 * (0.7 + 0.3 * q), (255, 235, 80), stroke=6)
    return (40, 40, 80), (70, 50, 100)


# --------------------------------------------------------------------------- beat 8
def s8a(d, t, T):
    p = t / T
    E.stars(d)
    tilt = math.radians(23 + 18 * math.sin(t * 2) * ease(p * 2))
    cx, cy, r = 360, 680, 230
    dx, dy = math.sin(tilt) * 330, -math.cos(tilt) * 330
    d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], (255, 255, 255, 150), 6)
    E.earth(d, cx, cy, r, t)
    label(d, "EARTH'S TILT WOBBLES", 270, 42, p=p * 2)
    return NIGHT


def s8b(d, t, T):
    p = t / T
    d.rect(0, 0, W / 2, H, (250, 190, 90))
    d.rect(W / 2, 0, W, H, (190, 220, 245))
    E.sun(d, 180, 520, 90, t)
    rnd = random.Random(3)
    for _ in range(40):
        x = rnd.uniform(380, 700)
        y = (rnd.uniform(0, H) + t * 120) % H
        d.ell(x, y, 6, 6, (255, 255, 255))
    d.rect(0, 950, W / 2, H, (230, 170, 80))
    d.rect(W / 2, 950, W, H, (245, 250, 255))
    d.text(180, 820, "SCORCHING", 40, (255, 255, 255), stroke=4)
    d.text(540, 820, "FREEZING", 40, (60, 110, 180), stroke=4)
    return (250, 190, 90), (190, 220, 245)


# --------------------------------------------------------------------------- beat 9
def s9a(d, t, T):
    p = t / T
    E.stars(d)
    E.earth(d, 180, 700, 140, t * 0.5)
    mx = 450 + 140 * ease(p)
    moon(d, mx, 700, 50)
    d.line([(mx + 70, 700), (mx + 130, 700)], (255, 235, 80), 8)
    d.poly([(mx + 130, 685), (mx + 130, 715), (mx + 155, 700)], (255, 235, 80))
    label(d, "THE MOON IS LEAVING", 320, 46, p=p * 2)
    return NIGHT


def ruler(d, x0, x1, y, marks=10):
    d.rect(x0, y - 40, x1, y + 40, (250, 215, 90), r=8)
    for k in range(marks + 1):
        x = x0 + (x1 - x0) * k / marks
        d.line([(x, y - 40), (x, y - (5 if k % 5 else -10))], (90, 70, 30), 4)


def s9b(d, t, T):
    p = t / T
    E.stars(d)
    E.earth(d, 110, 700, 80, t * 0.5)
    moon(d, 620, 700, 40)
    ruler(d, 200, 570, 700)
    return NIGHT


# --------------------------------------------------------------------------- beat 10
def s10a(d, t, T):
    p = t / T
    ruler(d, 110, 610, 700, 20)
    w = 500 * 0.4 * ease(p / 0.7)
    d.rect(110, 760, 110 + w, 790, (255, 90, 80), r=10)
    d.text(360, 480, "+4 cm", 120, (255, 255, 255), stroke=6)
    d.text(360, 590, "EVERY YEAR", 50, (255, 235, 80), stroke=4)
    return NIGHT


def s10b(d, t, T):
    p = t / T
    d.rect(200, 560, 520, 1300, SKIN, r=150)
    d.rect(232, 600, 488, 860, shade(SKIN, 0.9), r=110)
    grow = 30 + 50 * ease(p)
    d.rect(250, 560 - grow, 470, 760, (255, 230, 225), r=100)
    d.rect(250, 560 - grow, 470, 560 - grow + 40, (255, 255, 255), r=20)
    d.rect(265, 600, 300, 740, (255, 255, 255, 90), r=16)
    d.text(360, 300, "AS FAST AS", 50, (255, 255, 255), stroke=4)
    d.text(360, 370, "YOUR NAILS GROW!", 50, (255, 235, 80), stroke=4)
    return (60, 50, 90), (40, 35, 70)


# --------------------------------------------------------------------------- beat 11
def s11a(d, t, T):
    p = t / T
    E.stars(d)
    my = 760 - 380 * ease(p)
    moon(d, 360, my, 110)
    d.d.chord([-200 * K, 820 * K, 920 * K, 1500 * K], 180, 360, fill=(30, 50, 40))
    label(d, "BILLIONS OF YEARS LEFT", 1000, 40, p=(p - 0.3) * 2)
    return NIGHT


def s11b(d, t, T):
    p = t / T
    E.stars(d)
    moon(d, 520, 300, 90)
    d.d.chord([-200 * K, 900 * K, 920 * K, 1600 * K], 180, 360, fill=(30, 50, 40))
    person(d, 300, 1100, 1.0, mood="happy", arms="up" if int(t * 3) % 2 else "down")
    label(d, "ENJOY THE VIEW!", 560, 50, fill=(255, 235, 80), p=p * 2)
    return NIGHT


def outro(d, t, T):
    E.stars(d)
    moon(d, 360, 560, 160 * ease(t / T * 3) + 1)
    d.text(360, 860, "WHAT SHOULD I", 62, (255, 255, 255), stroke=5)
    d.text(360, 950, "EXPLAIN NEXT?", 62, (255, 235, 80), stroke=5)
    d.text(360, 1050, "COMMENT BELOW", 38, (255, 255, 255), stroke=3)
    return NIGHT


SHOTS = {f"beat_{i}_{ab}": globals()[f"s{i}{ab}"] for i in range(1, 12) for ab in "ab"}
SHOTS["outro"] = outro
