"""Procedural scenes for the no_wheels short (rendered by scripts/free_render.py)."""
from free_render import *  # noqa: F401,F403

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
