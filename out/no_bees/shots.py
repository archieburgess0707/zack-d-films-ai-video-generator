"""Procedural scenes for the no_bees short (rendered by scripts/free_render.py)."""
import importlib.util
import os

from free_render import *  # noqa: F401,F403

HERE_ = os.path.dirname(os.path.abspath(__file__))


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE_, "..", rel, "shots.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = _load("dispenser_foods", "dispenser_choice")   # burger, pancakes, waffle, ... + gloss/drip helpers
E = _load("earth_shots", "earth_stops_spinning")    # grass, tree, sun

SKY = ((140, 200, 245), (215, 235, 250))
WARM = ((255, 225, 170), (245, 190, 130))
GREY = (150, 150, 155)


def bee(d, x, y, s=1.0, t=0.0, face=1):
    flap = 0.6 + 0.4 * abs(math.sin(t * 30))
    d.ell(x - 10 * s, y - 34 * s, 26 * s, 34 * s * flap, (220, 240, 255, 170))
    d.ell(x + 16 * s, y - 32 * s, 22 * s, 30 * s * flap, (220, 240, 255, 170))
    d.poly([(x - 50 * s * face, y), (x - 66 * s * face, y + 4 * s), (x - 50 * s * face, y + 8 * s)], (40, 30, 20))
    d.ell(x, y, 52 * s, 36 * s, (250, 200, 40))
    for k in (-18, 4):
        d.rect(x + (k - 1) * s * face - 6 * s, y - 34 * s, x + (k - 1) * s * face + 6 * s, y + 34 * s, (40, 30, 20), r=5 * s)
    d.ell(x - 14 * s, y - 14 * s, 18 * s, 8 * s, (255, 255, 255, 90))
    hx = x + 44 * s * face
    d.ball(hx, y - 4 * s, 24 * s, (40, 30, 20))
    d.ell(hx + 8 * s * face, y - 10 * s, 7 * s, 8 * s, (255, 255, 255))
    d.ell(hx + 9 * s * face, y - 9 * s, 3.5 * s, 4 * s, (20, 20, 20))
    d.d.arc([(hx - 4 * s) * K, (y - 2 * s) * K, (hx + 16 * s) * K, (y + 12 * s) * K], 20, 160,
            fill=(255, 255, 255), width=int(3 * s * K))
    for side in (-1, 1):
        d.line([(hx, y - 26 * s), (hx + side * 10 * s + 8 * s * face, y - 48 * s)], (40, 30, 20), 3 * s)
        d.ell(hx + side * 10 * s + 8 * s * face, y - 50 * s, 4 * s, 4 * s, (40, 30, 20))


def flower(d, x, y, s=1.0, petal=(250, 120, 160), stem=True, pollen=1.0):
    if stem:
        d.line([(x, y), (x, y + 260 * s)], (70, 160, 70), 10 * s)
        d.ell(x + 30 * s, y + 150 * s, 30 * s, 12 * s, (80, 180, 80))
    for k in range(6):
        a = k * math.pi / 3
        d.ell(x + math.cos(a) * 34 * s, y + math.sin(a) * 34 * s, 26 * s, 26 * s, petal)
    d.ell(x, y, 24 * s, 24 * s, mix((160, 110, 40), (255, 200, 40), pollen))


def apple(d, x, y, s=1.0, col=(220, 40, 40)):
    d.ell(x - 22 * s, y, 40 * s, 44 * s, col)
    d.ell(x + 22 * s, y, 40 * s, 44 * s, col)
    d.ell(x, y + 4 * s, 50 * s, 44 * s, col)
    F.gloss(d, x - 28 * s, y - 16 * s, 12 * s, 18 * s, 120)
    d.line([(x, y - 36 * s), (x + 6 * s, y - 62 * s)], (100, 70, 40), 6 * s)
    d.ell(x + 22 * s, y - 52 * s, 18 * s, 9 * s, (80, 170, 70))


def blueberries(d, x, y, s=1.0):
    for bx, by in ((-24, 10), (20, 14), (0, -14), (-6, 30), (30, -10)):
        d.ball(x + bx * s, y + by * s, 18 * s, (70, 80, 170))
        d.ell(x + bx * s, y + (by - 10) * s, 5 * s, 3 * s, (40, 40, 90))


def cherries(d, x, y, s=1.0):
    d.line([(x - 22 * s, y), (x + 4 * s, y - 70 * s), (x + 30 * s, y - 4 * s)], (90, 120, 40), 5 * s)
    for cx in (-22, 30):
        d.ball(x + cx * s, y + 10 * s, 24 * s, (200, 20, 40))


def almond(d, x, y, s=1.0):
    for ax, ay, ang in ((-20, 0, -0.4), (22, 6, 0.3), (0, -24, 0.0)):
        d.ell(x + ax * s, y + ay * s, 16 * s, 26 * s, (190, 130, 80))
        d.ell(x + ax * s - 3 * s, y + ay * s - 4 * s, 10 * s, 18 * s, (215, 160, 105))


def price_tag(d, x, y, txt, rise):
    d.rect(x - 60, y - 26 - rise, x + 60, y + 26 - rise, (255, 255, 255), r=10)
    d.ell(x - 44, y - rise, 6, 6, (200, 200, 205))
    d.text(x + 6, y - rise, txt, 32, (220, 50, 50))


def cow(d, x, y, s=1.0, t=0.0):
    d.shadow(x, y + 120 * s, 170 * s, 18 * s)
    for lx in (-90, -50, 50, 90):
        d.rect(x + lx * s - 14 * s, y + 20 * s, x + lx * s + 14 * s, y + 120 * s, (240, 240, 240), r=8 * s)
        d.rect(x + lx * s - 14 * s, y + 104 * s, x + lx * s + 14 * s, y + 120 * s, (60, 50, 50), r=4 * s)
    d.rect(x - 130 * s, y - 70 * s, x + 130 * s, y + 50 * s, (245, 245, 245), r=50 * s)
    d.ell(x - 40 * s, y - 20 * s, 40 * s, 30 * s, (40, 40, 45))
    d.ell(x + 60 * s, y + 10 * s, 30 * s, 22 * s, (40, 40, 45))
    chew = 4 * s * math.sin(t * 8)
    hx, hy = x + 150 * s, y + 10 * s
    d.rect(hx - 50 * s, hy - 50 * s, hx + 50 * s, hy + 60 * s + chew, (245, 245, 245), r=30 * s)
    d.rect(hx - 44 * s, hy + 20 * s + chew, hx + 44 * s, hy + 70 * s + chew, (250, 190, 200), r=20 * s)
    d.ell(hx - 16 * s, hy - 10 * s, 7 * s, 8 * s, (20, 20, 20))
    d.ell(hx + 16 * s, hy - 10 * s, 7 * s, 8 * s, (20, 20, 20))
    for side in (-1, 1):
        d.ell(hx + side * 60 * s, hy - 40 * s, 22 * s, 10 * s, (240, 240, 240))
        d.line([(hx + side * 30 * s, hy - 50 * s), (hx + side * 40 * s, hy - 80 * s)], (230, 210, 170), 8 * s)


def alfalfa(d, x, y, s=1.0):
    d.line([(x, y), (x, y - 120 * s)], (70, 160, 70), 6 * s)
    for k in range(3):
        d.ell(x + (-14 + k * 14) * s, y - (40 + k * 25) * s, 12 * s, 7 * s, (90, 180, 80))
    d.ell(x, y - 130 * s, 14 * s, 18 * s, (160, 110, 210))


def milk(d, x, y, s=1.0):
    d.rect(x - 40 * s, y - 50 * s, x + 40 * s, y + 70 * s, (250, 250, 250), r=8 * s)
    d.poly([(x - 40 * s, y - 50 * s), (x, y - 90 * s), (x + 40 * s, y - 50 * s)], (230, 230, 235))
    d.rect(x - 40 * s, y - 10 * s, x + 40 * s, y + 30 * s, (80, 140, 230))
    d.text(x, y + 10 * s, "MILK", 22 * s, (255, 255, 255))


def cotton_plant(d, x, y, s=1.0, t=0.0):
    d.line([(x, y + 300 * s), (x, y)], (110, 80, 50), 12 * s)
    for k, (bx, by) in enumerate(((-90, 40), (80, 10), (-40, -60), (60, -100), (0, 120), (-100, -130))):
        d.line([(x, y + (by + 70) * s), (x + bx * s, y + by * s)], (110, 80, 50), 7 * s)
        for c in range(4):
            a = c * 1.57 + 0.4
            d.ball(x + bx * s + math.cos(a) * 18 * s, y + by * s + math.sin(a) * 14 * s, 22 * s, (250, 250, 248))


def tshirt(d, x, y, s=1.0, col=(80, 150, 230)):
    d.poly([(x - 70 * s, y - 120 * s), (x - 160 * s, y - 60 * s), (x - 120 * s, y + 10 * s), (x - 80 * s, y - 20 * s),
            (x - 80 * s, y + 160 * s), (x + 80 * s, y + 160 * s), (x + 80 * s, y - 20 * s), (x + 120 * s, y + 10 * s),
            (x + 160 * s, y - 60 * s), (x + 70 * s, y - 120 * s)], col)
    d.d.chord([(x - 40 * s) * K, (y - 150 * s) * K, (x + 40 * s) * K, (y - 90 * s) * K], 0, 180, fill=(255, 255, 255))
    F.gloss(d, x - 40 * s, y, 14 * s, 80 * s, 50)


def coffee_plant(d, x, y, s=1.0):
    d.line([(x, y + 320 * s), (x, y - 40 * s)], (110, 80, 50), 12 * s)
    for k in range(5):
        by = y - 20 * s + k * 70 * s
        for side in (-1, 1):
            d.ell(x + side * 80 * s, by, 70 * s, 22 * s, (50, 140, 60))
            for c in range(3):
                d.ball(x + side * (30 + c * 18) * s, by + 22 * s, 11 * s, (210, 40, 40))


def mug(d, x, y, s=1.0, empty=True):
    d.d.arc([(x + 32 * s) * K, (y - 22 * s) * K, (x + 82 * s) * K, (y + 34 * s) * K], 270, 90,
            fill=(240, 240, 240), width=int(14 * s * K))
    d.rect(x - 50 * s, y - 40 * s, x + 50 * s, y + 56 * s, (240, 240, 240), r=14 * s)
    d.ell(x, y - 40 * s, 50 * s, 12 * s, (200, 200, 205) if empty else (110, 60, 30))


def wheat(d, x, y, s=1.0, sway=0.0):
    top = (x + sway * 40 * s, y - 220 * s)
    d.line([(x, y), top], (210, 170, 70), 6 * s)
    for k in range(6):
        for side in (-1, 1):
            d.ell(top[0] + side * 10 * s, top[1] + k * 16 * s, 8 * s, 12 * s, (235, 195, 90))


def corn(d, x, y, s=1.0, sway=0.0):
    d.line([(x, y), (x + sway * 20 * s, y - 300 * s)], (80, 160, 70), 12 * s)
    d.ell(x + 26 * s, y - 160 * s, 18 * s, 50 * s, (250, 210, 70))
    d.ell(x + 40 * s, y - 150 * s, 20 * s, 56 * s, (110, 180, 80))
    for side in (-1, 1):
        d.ell(x + side * 50 * s + sway * 10 * s, y - 220 * s, 50 * s, 12 * s, (90, 170, 80))


def rice_bowl(d, x, y, s=1.0):
    d.ell(x, y - 10 * s, 120 * s, 40 * s, (255, 255, 252))
    for k in range(20):
        a = k * 0.9
        d.ell(x + math.cos(a) * 80 * s * (k / 20), y - 20 * s + math.sin(a) * 20 * s * (k / 20), 8 * s, 4 * s, (240, 240, 235))
    d.d.chord([(x - 130 * s) * K, (y - 60 * s) * K, (x + 130 * s) * K, (y + 120 * s) * K], 0, 180, fill=(220, 60, 60))
    d.line([(x + 40 * s, y - 70 * s), (x + 170 * s, y - 170 * s)], (150, 100, 60), 8 * s)
    d.line([(x + 60 * s, y - 60 * s), (x + 190 * s, y - 150 * s)], (150, 100, 60), 8 * s)


def choc_bar(d, x, y, s=1.0, t=0.0, happy=True):
    d.rect(x - 90 * s, y - 130 * s, x + 90 * s, y + 130 * s, (100, 55, 30), r=14 * s)
    for i in range(3):
        for j in range(4):
            cx, cy = x - 60 * s + i * 60 * s, y - 97 * s + j * 65 * s
            d.rect(cx - 24 * s, cy - 26 * s, cx + 24 * s, cy + 26 * s, (125, 70, 40), r=6 * s)
    F.gloss(d, x - 55 * s, y - 90 * s, 18 * s, 6 * s, 110)
    d.rect(x - 96 * s, y + 40 * s, x + 96 * s, y + 140 * s, (220, 40, 60), r=10 * s)
    d.text(x, y + 90 * s, "CHOC", 40 * s, (255, 255, 255))
    for ex in (-30, 30):
        d.ell(x + ex * s, y - 20 * s, 12 * s, 14 * s, (255, 255, 255))
        d.ell(x + ex * s, y - 18 * s, 6 * s, 7 * s, (20, 20, 20))
    d.d.arc([(x - 26 * s) * K, (y - 10 * s) * K, (x + 26 * s) * K, (y + 26 * s) * K], 20, 160,
            fill=(255, 255, 255), width=int(5 * s * K))
    wave = math.sin(t * 8) * 30 * s
    d.line([(x - 90 * s, y - 20 * s), (x - 150 * s, y - 80 * s - wave)], (100, 55, 30), 14 * s)
    d.line([(x + 90 * s, y - 20 * s), (x + 150 * s, y - 80 * s + wave)], (100, 55, 30), 14 * s)


def confetti(d, t, n=40, seed=1):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(0, W)
        y = (rnd.uniform(0, H) + t * rnd.uniform(150, 300)) % H
        d.rect(x, y, x + 12, y + 6, rnd.choice([(255, 80, 80), (255, 220, 60), (80, 200, 255), (120, 220, 120)]), r=2)


def grey_mix(c, g):
    lum = int(0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2])
    return mix(c, (lum, lum, lum), g)


def plate(d, x, y, g=0.0):
    d.ell(x, y + 10, 260, 90, grey_mix((230, 230, 235), g))
    d.ell(x, y, 250, 84, grey_mix((250, 250, 252), g))
    items = [((-120, -20), (220, 40, 40)), ((-40, -40), (70, 80, 170)), ((50, -30), (250, 150, 60)),
             ((130, -10), (120, 200, 70)), ((-70, 30), (200, 20, 40)), ((40, 30), (250, 210, 70))]
    for (ix, iy), c in items:
        d.ball(x + ix, y + iy, 36, grey_mix(c, g))


# --------------------------------------------------------------------------- beat 1
def s1a(d, t, T):
    p = t / T
    d.rect(0, 900, W, H, (190, 140, 90))
    d.rect(0, 880, W, 910, (215, 165, 110))
    d.ell(360, 860, 250, 60, (250, 250, 252))
    fruit = [lambda: apple(d, 220, 790, 0.9), lambda: blueberries(d, 360, 820, 1.0), lambda: cherries(d, 490, 800, 1.0)]
    for k, fn in enumerate(fruit):
        if p < 0.35 + k * 0.18:
            fn()
        elif p < 0.4 + k * 0.18:
            d.text(220 + k * 135, 780, "POOF", 30, (255, 255, 255), stroke=3)
    F.pancakes(d, 360, 560, 1.4)
    label(d, "YOUR BREAKFAST...", 300, 46, p=p * 2)
    return WARM


def s1b(d, t, T):
    p = t / T
    x = 360 + p * 500
    bee(d, x, 640 - 80 * math.sin(t * 3), 1.6, t)
    d.text(x - 160, 520, "BYE!", 60, (255, 255, 255), stroke=5)
    return SKY


# --------------------------------------------------------------------------- beat 2
def s2a(d, t, T):
    p = t / T
    E.grass(d, 1000)
    flower(d, 170, 700, 1.0)
    flower(d, 550, 640, 1.0, petal=(250, 190, 60))
    q = ease(p)
    bx, by = 170 + 380 * q, 600 - 140 * math.sin(q * math.pi)
    for k in range(10):
        qq = q - k * 0.04
        if qq > 0:
            d.ell(170 + 380 * qq, 600 - 140 * math.sin(qq * math.pi) + 30, 5, 5, (255, 210, 40, 220))
    bee(d, bx, by, 0.9, t)
    label(d, "CARRYING POLLEN", 300, 46, p=p * 2)
    return SKY


def s2b(d, t, T):
    p = t / T
    E.grass(d, 1000)
    q = ease((p - 0.2) / 0.5)
    d.line([(360, 1000), (360, 700)], (110, 80, 50), 14)
    if q < 1:
        flower(d, 360, 640, 1.4 * (1 - q) + 0.01, stem=False)
    if q > 0:
        apple(d, 360, 650, 1.6 * q)
    label(d, "FLOWER → FRUIT", 330, 50, p=p * 2)
    return SKY


# --------------------------------------------------------------------------- beat 3
def s3a(d, t, T):
    p = t / T
    rise = 60 * ease((p - 0.2) / 0.6)
    items = [(apple, 200, 520), (blueberries, 520, 520), (cherries, 200, 860), (almond, 520, 860)]
    for k, (fn, x, y) in enumerate(items):
        d.ell(x, y + 70, 120, 26, (0, 0, 0, 40))
        fn(d, x, y, 1.3)
        price_tag(d, x, y + 140, "$$$" if rise > 30 else "$", rise)
    return WARM


def s3b(d, t, T):
    p = t / T
    E.grass(d, 1050)
    d.line([(360, 1050), (360, 700)], (110, 80, 50), 30)
    for bx, by, r in ((360, 560, 200), (220, 640, 120), (500, 640, 120)):
        d.ell(bx, by, r, r * 0.8, (250, 220, 230))
    rnd = random.Random(2)
    for _ in range(40):
        d.ell(rnd.uniform(180, 540), rnd.uniform(430, 720), 8, 8, (250, 170, 200))
    for k in range(3):
        bee(d, 200 + k * 160 + 20 * math.sin(t * 3 + k), 480 + 60 * math.cos(t * 2 + k), 0.5, t + k)
    label(d, "ALMONDS NEED BEES", 300, 46, p=p * 2)
    return SKY


# --------------------------------------------------------------------------- beat 4
def s4a(d, t, T):
    p = t / T
    E.grass(d, 950)
    for k in range(8):
        alfalfa(d, 420 + k * 40, 1080)
    cow(d, 260, 850, 1.0, t)
    label(d, "COWS EAT ALFALFA", 300, 46, p=p * 2)
    return SKY


def s4b(d, t, T):
    p = t / T
    rise = 60 * ease((p - 0.2) / 0.6)
    F.burger(d, 220, 650, 1.5)
    milk(d, 520, 650, 1.5)
    price_tag(d, 220, 880, "$$$" if rise > 30 else "$", rise)
    price_tag(d, 520, 880, "$$$" if rise > 30 else "$", rise)
    return WARM


# --------------------------------------------------------------------------- beat 5
def s5a(d, t, T):
    p = t / T
    E.grass(d, 1050)
    cotton_plant(d, 360, 650, 1.3, t)
    label(d, "COTTON", 300, 56, p=p * 2)
    return SKY


def s5b(d, t, T):
    p = t / T
    tshirt(d, 360, 680, 1.5)
    label(d, "= YOUR CLOTHES", 300, 52, p=p * 2)
    return (245, 230, 210), (220, 200, 180)


# --------------------------------------------------------------------------- beat 6
def s6a(d, t, T):
    p = t / T
    E.grass(d, 1050)
    coffee_plant(d, 360, 560, 1.2)
    label(d, "COFFEE PLANTS", 300, 50, p=p * 2)
    return SKY


def s6b(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (190, 140, 90))
    person(d, 300, 1100, 1.0, mood="tired", arms="forward")
    mug(d, 430, 820, 0.8)
    label(d, "NOT ENOUGH COFFEE!", 300, 46, p=p * 2)
    return WARM


# --------------------------------------------------------------------------- beat 7
def s7a(d, t, T):
    p = t / T
    E.grass(d, 1050)
    d.line([(520, 1050), (520, 650)], (110, 80, 50), 28)
    d.ell(520, 520, 200, 170, (90, 170, 80))
    rnd = random.Random(5)
    for _ in range(18):
        flower(d, rnd.uniform(370, 670), rnd.uniform(400, 640), 0.25, petal=(255, 255, 255), stem=False)
    for k in range(5):
        d.line([(220 - k * 6, 1050 - k * 100), (300 - k * 6, 1050 - k * 100)], (180, 130, 80), 8)
    d.line([(200, 1050), (260, 600)], (180, 130, 80), 10)
    d.line([(300, 1050), (330, 600)], (180, 130, 80), 10)
    hands = person(d, 290, 760, 0.8, mood="happy", arms="up")
    d.line([hands[1], (hands[1][0] + 40, hands[1][1] - 40)], (150, 100, 60), 6)
    label(d, "POLLINATING BY HAND", 300, 44, p=p * 2)
    return SKY


def s7b(d, t, T):
    p = t / T
    flower(d, 360, 640, 2.4, petal=(255, 255, 255), stem=False, pollen=1.0)
    bx = 360 + 60 * math.sin(t * 6)
    d.line([(bx + 30, 600), (bx + 300, 300)], (180, 120, 70), 18)
    d.rect(bx - 10, 570, bx + 50, 640, (250, 220, 120), r=20)
    label(d, "ONE FLOWER AT A TIME", 1000, 44, p=p * 2)
    return SKY


# --------------------------------------------------------------------------- beat 8
def s8a(d, t, T):
    p = t / T
    E.grass(d, 1050)
    sway = math.sin(t * 3) * 0.6
    for k in range(10):
        wheat(d, 30 + k * 40, 1080, 1.0, sway)
    for k in range(3):
        corn(d, 470 + k * 90, 1080, 1.0, sway)
    rnd = random.Random(1)
    for _ in range(10):
        y = rnd.uniform(400, 800)
        x = (rnd.uniform(0, W) + t * 500) % (W + 200) - 100
        d.line([(x, y), (x + 120, y)], (255, 255, 255, 170), 5)
    label(d, "POLLINATED BY WIND", 300, 46, p=p * 2)
    return SKY


def s8b(d, t, T):
    p = t / T
    rice_bowl(d, 360, 720, 1.5)
    F.steam(d, 360, 560, t, 1.4)
    label(d, "YOU WOULDN'T STARVE", 300, 46, p=p * 2)
    return WARM


# --------------------------------------------------------------------------- beat 9
def s9a(d, t, T):
    p = t / T
    confetti(d, t)
    choc_bar(d, 360, 680, 1.4, t)
    label(d, "CHOCOLATE SURVIVES!", 300, 46, fill=(255, 235, 80), p=p * 2)
    return (250, 170, 110), (220, 110, 80)


def s9b(d, t, T):
    p = t / T
    d.ell(360, 760, 120, 70, (190, 90, 40))
    d.ell(340, 740, 80, 40, (210, 120, 60))
    flower(d, 360, 600, 1.1, petal=(255, 240, 230), stem=False)
    mx, my = 360 + 30 * math.sin(t * 4), 560 + 20 * math.cos(t * 5)
    d.ell(mx, my, 10, 7, (40, 40, 40))
    d.ell(mx - 6, my - 8, 8, 5, (220, 240, 255, 180))
    d.ell(mx + 6, my - 8, 8, 5, (220, 240, 255, 180))
    d.ell(360, 580, 150, 150, None, outline=(90, 90, 100), w=16)
    d.line([(465, 685), (580, 800)], (90, 90, 100), 26)
    label(d, "TINY FLIES CALLED MIDGES", 300, 40, p=p * 2)
    return (200, 230, 200), (150, 200, 150)


# --------------------------------------------------------------------------- beat 10
def s10a(d, t, T):
    p = t / T
    g = ease((p - 0.2) / 0.6)
    plate(d, 360, 700, g)
    label(d, "LESS COLOURFUL", 300, 50, p=p * 2)
    return mix((255, 225, 170), (200, 200, 200), g), mix((245, 190, 130), (170, 170, 170), g)


def s10b(d, t, T):
    p = t / T
    plate(d, 360, 700, 1.0)
    label(d, "BORING!", 300, 60, fill=(200, 200, 200), p=p * 2)
    return (200, 200, 200), (170, 170, 170)


# --------------------------------------------------------------------------- beat 11
def s11a(d, t, T):
    p = t / T
    E.grass(d, 1000)
    person(d, 360, 1120, 1.0, mood="happy")
    bee(d, -100 + p * 900, 520 + 60 * math.sin(t * 4), 0.9, t)
    label(d, "DON'T PANIC...", 300, 50, p=p * 2)
    return SKY


def s11b(d, t, T):
    p = t / T
    bee(d, 360, 680, 2.2, t)
    beat_ = 1 + 0.1 * math.sin(t * 8)
    d.ell(500 - 26 * beat_, 430, 34 * beat_, 34 * beat_, (240, 60, 90))
    d.ell(500 + 26 * beat_, 430, 34 * beat_, 34 * beat_, (240, 60, 90))
    d.poly([(500 - 58 * beat_, 445), (500 + 58 * beat_, 445), (500, 445 + 70 * beat_)], (240, 60, 90))
    label(d, "LET IT BEE", 1000, 60, fill=(255, 235, 80), p=p * 2)
    return SKY


def outro(d, t, T):
    bee(d, 360, 560, 1.6 * ease(t / T * 3) + 0.01, t)
    d.text(360, 860, "WHAT SHOULD I", 62, (255, 255, 255), stroke=5)
    d.text(360, 950, "EXPLAIN NEXT?", 62, (255, 235, 80), stroke=5)
    d.text(360, 1050, "COMMENT BELOW", 38, (255, 255, 255), stroke=3)
    return (250, 190, 60), (230, 140, 40)


SHOTS = {f"beat_{i}_{ab}": globals()[f"s{i}{ab}"] for i in range(1, 12) for ab in "ab"}
SHOTS["outro"] = outro
