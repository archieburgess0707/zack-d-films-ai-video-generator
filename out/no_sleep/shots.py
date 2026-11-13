"""Procedural scenes for the no_sleep short (rendered by scripts/free_render.py)."""
from free_render import *  # noqa: F401,F403

NIGHT = ((20, 24, 60), (45, 35, 85))
BRAIN, BRAIN_D = (245, 160, 175), (215, 120, 140)
RANDY = (200, 60, 60)


# --------------------------------------------------------------------------- props
def head(d, hx, hy, sc=1.0, mood="open"):
    d.ball(hx, hy, 52 * sc, SKIN)
    d.d.chord([(hx - 54 * sc) * K, (hy - 58 * sc) * K, (hx + 54 * sc) * K, (hy + 30 * sc) * K], 180, 360, fill=HAIR)
    for ex in (-18, 18):
        if mood == "closed":
            d.d.arc([(hx + (ex - 9) * sc) * K, (hy - 2 * sc) * K, (hx + (ex + 9) * sc) * K, (hy + 10 * sc) * K],
                    10, 170, fill=(40, 30, 30), width=int(3 * sc * K))
            continue
        d.ell(hx + ex * sc, hy + 4 * sc, 10 * sc, 12 * sc, (255, 255, 255))
        d.ell(hx + ex * sc, hy + 5 * sc, 5 * sc, 5.5 * sc, (30, 30, 40))
        d.d.arc([(hx + (ex - 10) * sc) * K, (hy + 8 * sc) * K, (hx + (ex + 10) * sc) * K, (hy + 22 * sc) * K],
                20, 160, fill=(150, 110, 140), width=int(3 * sc * K))
    if mood == "closed":
        d.d.arc([(hx - 10 * sc) * K, (hy + 22 * sc) * K, (hx + 10 * sc) * K, (hy + 34 * sc) * K], 10, 170,
                fill=(90, 30, 30), width=int(4 * sc * K))
    else:
        d.line([(hx - 10 * sc, hy + 32 * sc), (hx + 10 * sc, hy + 32 * sc)], (90, 30, 30), 4 * sc)


def bed(d, x, y, mood="open", sc=1.0):
    d.rect(x - 280 * sc, y - 40 * sc, x - 250 * sc, y + 160 * sc, (120, 80, 55), r=8)
    d.rect(x - 280 * sc, y + 60 * sc, x + 280 * sc, y + 160 * sc, (140, 95, 65), r=14)
    d.rect(x - 250 * sc, y - 10 * sc, x - 80 * sc, y + 60 * sc, (245, 245, 250), r=30)
    head(d, x - 160 * sc, y - 20 * sc, sc, mood)
    d.rect(x - 120 * sc, y + 0 * sc, x + 270 * sc, y + 90 * sc, (90, 120, 200), r=30)
    d.rect(x - 110 * sc, y + 8 * sc, x + 260 * sc, y + 24 * sc, (255, 255, 255, 50), r=8)


def bedroom(d, lamp=False):
    d.rect(0, 1000, W, H, (70, 55, 80))
    d.rect(420, 260, 640, 520, (30, 40, 90), r=10)
    d.rect(420, 260, 640, 520, None, r=10, outline=(140, 120, 150), w=10)
    d.line([(530, 260), (530, 520)], (140, 120, 150), 8)
    d.ball(590, 320, 26, (240, 240, 220))
    rnd = random.Random(2)
    for _ in range(10):
        d.ell(rnd.uniform(430, 630), rnd.uniform(270, 510), 2, 2, (255, 255, 255, 200))


def digital_clock(d, x, y, txt, col=(255, 70, 60)):
    d.rect(x - 130, y - 55, x + 130, y + 55, (25, 25, 30), r=16)
    d.text(x, y, txt, 56, col)


def brain(d, cx, cy, r, dim=None, t=0.0):
    """Cartoon brain; `dim` is a list of 0..1 darkness values for 6 lobes."""
    d.ell(cx + 6, cy + 10, r * 1.05, r * 0.82, (0, 0, 0, 60))
    lobes = [(-0.45, -0.25), (0.0, -0.4), (0.45, -0.25), (-0.5, 0.2), (0.0, 0.15), (0.5, 0.2)]
    for i, (lx, ly) in enumerate(lobes):
        d.ell(cx + lx * r, cy + ly * r, r * 0.55, r * 0.45, BRAIN_D)
    for i, (lx, ly) in enumerate(lobes):
        d.ell(cx + lx * r - 4, cy + ly * r - 4, r * 0.5, r * 0.4, BRAIN)
        for k in range(2):
            d.d.arc([(cx + lx * r - r * 0.3) * K, (cy + ly * r - r * (0.2 - k * 0.15)) * K,
                     (cx + lx * r + r * 0.3) * K, (cy + ly * r + r * (0.05 + k * 0.15)) * K],
                    200, 340, fill=BRAIN_D, width=int(5 * K))
        if dim and dim[i] > 0:
            d.ell(cx + lx * r - 4, cy + ly * r - 4, r * 0.5, r * 0.4, (20, 20, 50, int(190 * dim[i])))
    d.rect(cx - r * 0.12, cy + r * 0.5, cx + r * 0.12, cy + r * 0.95, BRAIN_D, r=20)
    d.ell(cx - r * 0.4, cy - r * 0.45, r * 0.25, r * 0.12, (255, 255, 255, 90))


def zzz(d, x, y, t, n=3, col=(255, 255, 255)):
    for k in range(n):
        ph = (t * 0.7 + k / n) % 1
        d.text(x + ph * 80, y - ph * 160, "Z", 30 + 30 * ph, col + (int(255 * (1 - ph)),), stroke=0)


def meter(d, x, y, lvl, name, col):
    d.rect(x - 70, y - 380, x + 70, y, (40, 40, 55), r=20)
    h = 360 * clamp(lvl)
    d.rect(x - 58, y - 10 - h, x + 58, y - 10, col, r=14)
    d.text(x, y + 50, name, 40, (255, 255, 255), stroke=3)


def burger(d, x, y, s=1.0):
    d.d.chord([(x - 70 * s) * K, (y - 60 * s) * K, (x + 70 * s) * K, (y + 20 * s) * K], 180, 360, fill=(230, 160, 70))
    d.rect(x - 74 * s, y - 22 * s, x + 74 * s, y - 6 * s, (90, 190, 80), r=8)
    d.rect(x - 70 * s, y - 8 * s, x + 70 * s, y + 14 * s, (120, 70, 40), r=10)
    d.rect(x - 68 * s, y + 12 * s, x + 68 * s, y + 34 * s, (230, 160, 70), r=10)


def donut(d, x, y, s=1.0):
    d.ell(x, y, 55 * s, 55 * s, (220, 170, 100))
    d.ell(x, y, 46 * s, 46 * s, (240, 120, 180))
    d.ell(x, y, 18 * s, 18 * s, (0, 0, 0, 0))
    d.ell(x, y, 18 * s, 18 * s, (255, 255, 255, 230))
    for k in range(6):
        a = k * 1.05
        d.line([(x + math.cos(a) * 30 * s, y + math.sin(a) * 30 * s),
                (x + math.cos(a) * 38 * s, y + math.sin(a) * 38 * s)], (255, 240, 120), 5 * s)


def germ(d, x, y, r, t, seed=0):
    for k in range(8):
        a = k * math.pi / 4 + t
        d.line([(x, y), (x + math.cos(a) * r * 1.45, y + math.sin(a) * r * 1.45)], (80, 160, 60), 6)
        d.ell(x + math.cos(a) * r * 1.5, y + math.sin(a) * r * 1.5, 7, 7, (80, 160, 60))
    d.ball(x, y, r, (120, 200, 80))
    d.ell(x - r * 0.3, y - r * 0.1, 6, 7, (20, 20, 20))
    d.ell(x + r * 0.3, y - r * 0.1, 6, 7, (20, 20, 20))


def shield(d, cx, cy, s, crack=0.0):
    pts = [(cx - 160 * s, cy - 180 * s), (cx + 160 * s, cy - 180 * s), (cx + 150 * s, cy + 40 * s),
           (cx, cy + 210 * s), (cx - 150 * s, cy + 40 * s)]
    d.poly([(x + 8, y + 10) for x, y in pts], (0, 0, 0, 70))
    d.poly(pts, (70, 140, 230))
    d.poly([(cx - 120 * s, cy - 150 * s), (cx + 120 * s, cy - 150 * s), (cx + 112 * s, cy + 30 * s),
            (cx, cy + 165 * s), (cx - 112 * s, cy + 30 * s)], (110, 175, 250))
    d.text(cx, cy, "+", 150 * s, (255, 255, 255))
    if crack > 0:
        path = [(cx - 10, cy - 180 * s), (cx + 30, cy - 90 * s), (cx - 20, cy - 20 * s), (cx + 40, cy + 60 * s),
                (cx - 5, cy + 150 * s)]
        n = max(2, int(len(path) * crack) + 1)
        d.line(path[:n], (30, 30, 50), 10)


def calendar(d, cx, cy, top, big, col=(230, 60, 60)):
    d.rect(cx - 190 + 8, cy - 220 + 10, cx + 190 + 8, cy + 220 + 10, (0, 0, 0, 70), r=24)
    d.rect(cx - 190, cy - 220, cx + 190, cy + 220, (250, 250, 250), r=24)
    d.rect(cx - 190, cy - 220, cx + 190, cy - 110, col, r=24)
    d.rect(cx - 190, cy - 140, cx + 190, cy - 110, col)
    d.text(cx, cy - 165, top, 50, (255, 255, 255))
    d.text(cx, cy + 50, big, 150 if len(big) <= 2 else 105, (40, 40, 50))


# --------------------------------------------------------------------------- beat 1
def s1a(d, t, T):
    p = t / T
    bedroom(d)
    bed(d, 360, 820, "open", 1.0)
    digital_clock(d, 200, 360, f"HOUR {min(24, 1 + int(ease(p / 0.8) * 23))}")
    return NIGHT


def s1b(d, t, T):
    p = t / T
    q = ease(p / 0.6)
    brain(d, 360, 680, 280, dim=[q, 0, q * 0.8, 0, q * 0.6, 0], t=t)
    if p > 0.2:
        zzz(d, 200, 520, t)
        zzz(d, 470, 520, t + 0.4)
    label(d, "PARTS OF IT FALL ASLEEP", 260, 40, p=p * 2)
    return (60, 40, 90), (25, 20, 50)


# --------------------------------------------------------------------------- beat 2
def desk(d):
    d.rect(0, 960, W, H, (80, 70, 90))
    d.rect(60, 880, 660, 920, (150, 105, 70), r=10)
    d.rect(120, 920, 150, 1100, (120, 85, 55))
    d.rect(570, 920, 600, 1100, (120, 85, 55))
    d.rect(380, 700, 620, 870, (40, 44, 55), r=12)
    d.rect(395, 715, 605, 855, (130, 190, 240), r=6)
    d.rect(480, 870, 520, 885, (40, 44, 55))


def s2a(d, t, T):
    p = t / T
    desk(d)
    closed = 0.3 < p < 0.62
    person(d, 230, 1060, 0.95, mood="sleep" if closed else "tired")
    if closed:
        zzz(d, 270, 620, t)
    else:
        if p >= 0.62:
            d.text(360, 520, "!", 90, (255, 235, 80), stroke=5)
    stamp(d, "MICROSLEEP", 280, (p - 0.3) * 1.5)
    return (60, 60, 90), (40, 40, 60)


def s2b(d, t, T):
    p = t / T
    on = not (0.25 < p < 0.75)
    d.rect(210, 450, 510, 850, (230, 230, 235), r=30)
    d.rect(240, 480, 480, 820, (200, 200, 210), r=20)
    y = 560 if on else 740
    d.rect(280, y - 70, 440, y + 70, (60, 200, 100) if on else (220, 60, 60), r=20)
    d.text(360, y, "ON" if on else "OFF", 56, (255, 255, 255))
    if not on:
        secs = min(3, 1 + int((p - 0.25) / 0.5 * 3))
        d.text(360, 1000, f"{secs}...", 80, (255, 235, 80), stroke=5)
    label(d, "YOUR BRAIN", 330, 48, p=p * 2)
    return (20, 20, 30), (40, 40, 60)


# --------------------------------------------------------------------------- beat 3
def s3a(d, t, T):
    p = t / T
    d.text(360, 330, "REACTION TIME", 52, (255, 255, 255), stroke=4)
    for i, (name, val, col) in enumerate((("RESTED", 0.35, (80, 200, 120)), ("24H AWAKE", 0.85, (240, 90, 70)))):
        y = 520 + i * 200
        d.text(80, y - 50, name, 34, (255, 255, 255), anchor="lm", stroke=3)
        d.rect(80, y, 640, y + 70, (50, 50, 70), r=20)
        d.rect(80, y, 80 + 560 * val * ease(p / 0.5), y + 70, col, r=20)
    stamp(d, "= DRUNK", 1000, (p - 0.5) * 1.5)
    return (40, 40, 70), (25, 25, 45)


def s3b(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (90, 90, 110))
    sway = math.sin(t * 3)
    person(d, 360 + sway * 30, 1100, 1.05, mood="tired", lean=sway * 0.4)
    for k in range(5):
        a = t * 3 + k * 2 * math.pi / 5
        d.text(360 + sway * 30 + math.cos(a) * 110, 640 + math.sin(a) * 30, "★", 40, (255, 230, 80))
    label(d, "WOBBLY", 330, 56, fill=(255, 235, 80), p=p * 2)
    return (70, 70, 110), (110, 100, 140)


# --------------------------------------------------------------------------- beat 4
def s4a(d, t, T):
    p = t / T
    rnd = random.Random(5)
    brain(d, 360, 700, 280)
    front = -300 + ease(p / 0.9) * 900
    for _ in range(40):
        x, y = rnd.uniform(130, 600), rnd.uniform(500, 880)
        if x > front:
            d.ell(x, y, 9, 9, (110, 90, 60))
    d.rect(front - 120, 440, front, 940, (90, 170, 255, 110), r=60)
    for k in range(6):
        d.ell(front - 20, 470 + k * 80 + 10 * math.sin(t * 8 + k), 14, 22, (220, 240, 255, 200))
    label(d, "THE BRAIN'S CLEANING CREW", 260, 36, p=p * 2)
    return (40, 50, 90), (20, 25, 50)


def s4b(d, t, T):
    p = t / T
    brain(d, 360, 700, 280)
    rnd = random.Random(9)
    n = int(10 + 70 * ease(p))
    for i in range(n):
        d.ell(rnd.uniform(120, 600), rnd.uniform(470, 900), rnd.uniform(8, 16), rnd.uniform(8, 14), (110, 90, 60))
    d.text(360, 1010, f"WASTE: {n}", 52, (255, 235, 80), stroke=4)
    label(d, "THE TRASH PILES UP", 260, 44, p=p * 2)
    return (60, 40, 50), (30, 20, 30)


# --------------------------------------------------------------------------- beat 5
def s5a(d, t, T):
    p = t / T
    q = ease(p / 0.7)
    meter(d, 220, 930, 0.35 + 0.55 * q, "HUNGRY", (240, 120, 60))
    meter(d, 500, 930, 0.8 - 0.6 * q, "FULL", (80, 190, 120))
    d.text(220, 470, "▲", 70, (240, 120, 60))
    d.text(500, 470, "▼", 70, (80, 190, 120))
    label(d, "HUNGER HORMONES", 300, 46, p=p * 2)
    return (50, 40, 70), (30, 25, 45)


def s5b(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (90, 80, 110))
    person(d, 360, 1100, 1.0, mood="tired", arms="forward")
    items = [(burger, 120, 420), (donut, 600, 380), (burger, 610, 720), (donut, 110, 760)]
    for i, (fn, x, y) in enumerate(items):
        q = ease(p / 0.9)
        fn(d, x + (360 - x) * 0.35 * q, y + 20 * math.sin(t * 3 + i), 0.9)
    label(d, "JUNK FOOD CRAVINGS", 250, 42, fill=(255, 235, 80), p=p * 2)
    return (120, 100, 150), (90, 75, 120)


# --------------------------------------------------------------------------- beat 6
def s6a(d, t, T):
    p = t / T
    shield(d, 360, 680, 1.4, crack=ease((p - 0.2) / 0.5))
    for i, (gx, gy) in enumerate(((100, 420), (620, 460), (90, 960), (630, 980))):
        q = ease(p)
        germ(d, gx + (360 - gx) * 0.25 * q, gy + (680 - gy) * 0.25 * q, 38, t + i)
    label(d, "IMMUNE SYSTEM", 260, 48, p=p * 2)
    return (30, 50, 80), (20, 30, 50)


def s6b(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (90, 90, 110))
    person(d, 360, 1100, 1.0, mood="tired")
    d.ell(360, 1100 - 95 - 100 - 62 + 18, 10, 8, (230, 60, 60))
    if p > 0.3:
        d.text(360, 420, "ACHOO!", 90 * (1 + 0.15 * (1 - ease((p - 0.3) * 6))), (255, 235, 80), stroke=6)
    germ(d, 140, 560, 30, t)
    germ(d, 590, 620, 26, t + 1)
    return (120, 140, 170), (90, 100, 130)


# --------------------------------------------------------------------------- beat 7
def s7a(d, t, T):
    p = t / T
    wob = 25 * ease(p / 0.5)
    for i in range(9):
        x = 40 + i * 80
        pts = [(x + wob * math.sin(y / 70 + t * 3 + i), y) for y in range(200, 1001, 40)]
        d.line(pts, (150, 120, 170), 8)
    d.rect(0, 1000, W, H, (70, 55, 80))
    bed(d, 360, 880, "open", 0.9)
    d.text(360, 300, "DAY 3", 96, (255, 235, 80), stroke=6)
    return (50, 40, 70), (35, 28, 55)


def s7b(d, t, T):
    p = t / T
    rnd = random.Random(3)
    for k in range(5):
        a = 0.5 + 0.5 * math.sin(t * 2.5 + k * 1.7)
        x, y = rnd.uniform(60, 660), rnd.uniform(300, 1000)
        d.ell(x, y, 80 + 30 * a, 140 + 30 * a, (10, 10, 20, int(150 * a)))
        d.ell(x - 18, y - 50, 8, 8, (255, 60, 60, int(220 * a)))
        d.ell(x + 18, y - 50, 8, 8, (255, 60, 60, int(220 * a)))
    look = math.sin(t * 2) * 30
    d.ell(360, 680, 200, 110, (250, 250, 250))
    d.ell(360 + look, 680, 80, 80, (90, 150, 210))
    d.ell(360 + look, 680, 38, 38, (20, 20, 30))
    d.ell(340 + look, 660, 14, 10, (255, 255, 255))
    d.ell(360, 680, 200, 110, None, outline=(40, 30, 50), w=10)
    label(d, "SEEING THINGS", 300, 52, fill=(255, 120, 120), p=p * 2)
    return (25, 20, 35), (10, 8, 18)


# --------------------------------------------------------------------------- beat 8
def s8a(d, t, T):
    p = t / T
    calendar(d, 230, 560, "YEAR", "1964", col=(80, 120, 200))
    person(d, 530, 1060, 0.95, mood="happy", hoodie=RANDY)
    label(d, "RANDY GARDNER, AGE 17", 1010, 38, p=(p - 0.3) * 2)
    return (230, 200, 150), (200, 160, 110)


def s8b(d, t, T):
    p = t / T
    day = min(11, 1 + int(ease(p / 0.8) * 10))
    calendar(d, 360, 650, "DAYS AWAKE", str(day))
    if day == 11:
        stamp(d, "11 DAYS!", 1030, (p - 0.8) * 3)
    return (70, 40, 60), (40, 25, 40)


# --------------------------------------------------------------------------- beat 9
def s9a(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (90, 80, 100))
    person(d, 360, 1100, 1.0, mood="tired", hoodie=RANDY)
    for k in range(4):
        ph = (t * 0.5 + k / 4) % 1
        d.text(200 + k * 110, 600 - ph * 200, "?", 60 + 30 * ph, (255, 235, 80, int(255 * (1 - ph))), stroke=0)
    label(d, "MEMORY PROBLEMS", 300, 46, p=p * 2)
    return (80, 70, 100), (60, 50, 80)


def s9b(d, t, T):
    p = t / T
    d.rect(170 + 10, 420 + 12, 550 + 10, 900 + 12, (0, 0, 0, 80), r=20)
    d.rect(170, 420, 550, 900, (40, 100, 180), r=20)
    d.rect(170, 420, 200, 900, (30, 75, 140), r=10)
    d.text(375, 560, "WORLD", 50, (255, 215, 90))
    d.text(375, 630, "RECORDS", 50, (255, 215, 90))
    d.text(375, 760, "NO SLEEP", 40, (255, 255, 255))
    q = ease((p - 0.25) / 0.25)
    if q > 0:
        d.line([(150, 400), (150 + 420 * q, 400 + 520 * q)], (235, 50, 50), 30)
        d.line([(570, 400), (570 - 420 * q, 400 + 520 * q)], (235, 50, 50), 30)
    label(d, "TOO DANGEROUS", 300, 50, fill=(255, 120, 120), p=(p - 0.3) * 2)
    return (60, 40, 50), (30, 20, 30)


# --------------------------------------------------------------------------- beat 10
def s10a(d, t, T):
    p = t / T
    d.rect(0, 900, W, H, (110, 80, 60))
    d.rect(0, 880, W, 910, (140, 100, 75))
    lift = 1 - ease((p - 0.1) / 0.3)
    py = 880 - 30 - lift * 300
    d.rect(250, py - 300, 470, py + 30, (30, 30, 35), r=36)
    on = p < 0.55
    d.rect(266, py - 284, 454, py + 14, (120, 200, 255) if on else (10, 10, 14), r=26)
    if on:
        d.text(360, py - 140, "12:47", 50, (255, 255, 255))
    else:
        d.text(360, 400, "GOODNIGHT", 64, (255, 235, 80), stroke=5)
    return (25, 25, 55), (45, 35, 75)


def s10b(d, t, T):
    p = t / T
    bedroom(d)
    bed(d, 360, 820, "closed", 1.0)
    zzz(d, 260, 780, t)
    d.ell(250, 380, 120, 110, (255, 255, 255, 30))
    brain(d, 250, 380, 80)
    for k in range(6):
        a = t * 2 + k
        d.text(250 + math.cos(a) * 110, 380 + math.sin(a) * 90, "✦", 26, (255, 240, 140))
    label(d, "REPAIR MODE", 560, 46, fill=(150, 230, 255), p=p * 2)
    return NIGHT


def outro(d, t, T):
    brain(d, 360, 560, 190 * ease(t / T * 3))
    d.text(360, 860, "WHAT SHOULD I", 62, (255, 255, 255), stroke=5)
    d.text(360, 950, "EXPLAIN NEXT?", 62, (255, 235, 80), stroke=5)
    d.text(360, 1050, "COMMENT BELOW", 38, (255, 255, 255), stroke=3)
    return NIGHT


SHOTS = {f"beat_{i}_{ab}": globals()[f"s{i}{ab}"] for i in range(1, 11) for ab in "ab"}
SHOTS["outro"] = outro
