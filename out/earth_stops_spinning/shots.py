"""Procedural scenes for the earth_stops_spinning short (rendered by scripts/free_render.py)."""
from free_render import *  # noqa: F401,F403

OCEAN, LAND, LAND2 = (40, 110, 210), (70, 170, 90), (150, 120, 70)
SPACE = ((8, 10, 30), (24, 16, 50))
CONTINENTS = [(0.0, -0.35, 0.55, 0.30), (1.3, 0.25, 0.45, 0.40), (2.6, -0.15, 0.60, 0.25),
              (3.9, 0.40, 0.35, 0.22), (5.0, -0.50, 0.40, 0.18), (4.4, 0.05, 0.30, 0.30)]


def stars(d, seed=11, n=90):
    rnd = random.Random(seed)
    for _ in range(n):
        d.ell(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1, 2.2), rnd.uniform(1, 2.2), (255, 255, 255, 170))


def earth(d, cx, cy, r, rot, glow=True):
    """Globe with continents scrolling by rotation `rot` (radians)."""
    if glow:
        d.ell(cx, cy, r * 1.08, r * 1.08, (90, 160, 255, 60))
    d.ell(cx, cy, r, r, shade(OCEAN, 0.7))
    d.ell(cx - r * 0.05, cy - r * 0.05, r * 0.95, r * 0.95, OCEAN)
    for lon, lat, w, h in CONTINENTS:
        a = lon + rot
        c = math.cos(a)
        if c <= 0.05:
            continue
        x = cx + math.sin(a) * r * 0.82
        y = cy + lat * r
        d.ell(x, y, w * r * 0.8 * c, h * r * 0.85, LAND)
        d.ell(x - w * r * 0.18 * c, y - h * r * 0.25, w * r * 0.35 * c, h * r * 0.35, (110, 200, 120))
    d.ell(cx - r * 0.38, cy - r * 0.42, r * 0.28, r * 0.18, (255, 255, 255, 60))


def night_half(d, cx, cy, r, a=170):
    """Darken the right half of a globe (sun on the left)."""
    d.d.chord([(cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K], -90, 90, fill=(0, 0, 25, a))


def speed_lines(d, x0, x1, y0, y1, t, n=14, seed=3, col=(255, 255, 255, 150), speed=900):
    rnd = random.Random(seed)
    for _ in range(n):
        y = rnd.uniform(y0, y1)
        L = rnd.uniform(60, 200)
        x = x0 + ((rnd.uniform(0, x1 - x0) + t * speed) % (x1 - x0 + L)) - L
        d.line([(x, y), (x + L, y)], col, rnd.uniform(3, 7))


def layer_rotated(d, w, h, ang, cx, cy, draw_fn):
    """Draw with draw_fn(D) on a small transparent layer, rotate it, paste at (cx, cy)."""
    lay = Image.new("RGBA", (int(w * K), int(h * K)), (0, 0, 0, 0))
    draw_fn(D(lay))
    lay = lay.rotate(math.degrees(ang), resample=Image.BICUBIC, expand=True)
    d.img.paste(lay, (int(cx * K - lay.width / 2), int(cy * K - lay.height / 2)), lay)


def house(d, x, ground, sc=1.0, col=(236, 214, 180)):
    d.rect(x - 110 * sc, ground - 210 * sc, x + 110 * sc, ground, col, r=8)
    d.poly([(x - 135 * sc, ground - 200 * sc), (x, ground - 320 * sc), (x + 135 * sc, ground - 200 * sc)], (170, 70, 60))
    d.rect(x - 30 * sc, ground - 110 * sc, x + 30 * sc, ground, (120, 80, 60), r=6)
    d.rect(x + 50 * sc, ground - 170 * sc, x + 95 * sc, ground - 125 * sc, (160, 215, 245), r=4)


def tree(d, x, ground, sc=1.0, bend=0.0):
    top = (x + bend * 150 * sc, ground - 240 * sc)
    d.line([(x, ground), (x + bend * 40 * sc, ground - 120 * sc), top], (110, 75, 45), 24 * sc)
    for dx, dy, r in ((0, -20, 80), (-55, 15, 60), (55, 15, 60), (0, 45, 55)):
        d.ball(top[0] + dx * sc + bend * 40 * sc, top[1] + dy * sc, r * sc, (70, 165, 80))


def grass(d, horizon=900):
    d.rect(0, horizon, W, H, (95, 170, 85))
    d.rect(0, horizon, W, horizon + 10, (125, 200, 110))


# --------------------------------------------------------------------------- beat 1
def s1a(d, t, T):
    p = t / T
    stars(d)
    stop = T * 0.5
    rot = 2.2 * min(t, stop)
    shake = 8 * math.sin(t * 60) * max(0, 1 - (t - stop) / 0.3) if t > stop else 0
    earth(d, 360 + shake, 680, 270, rot)
    if t < stop:
        d.d.arc([(360 - 330) * K, (680 - 330) * K, (360 + 330) * K, (680 + 330) * K], 200, 340,
                fill=(255, 220, 90), width=10 * K)
        d.poly([(670, 560), (700, 620), (640, 610)], (255, 220, 90))
        label(d, "SPINNING...", 270, 44, p=p * 3)
    else:
        stamp(d, "STOP!", 270, (t - stop) / T * 2)
        label(d, "EVERYTHING KEEPS GOING: 1,000 MPH", 1040, 30, fill=(255, 230, 90), p=(t - stop) / T * 3)
    return SPACE


def s1b(d, t, T):
    p = t / T
    grass(d)
    house(d, 120, 900, 0.8)
    tree(d, 600, 900, 0.8)
    x = -80 + ease(p) * 900
    speed_lines(d, -200, x - 40, 520, 780, t, 10, speed=0)
    for i in range(6):
        y = 560 + i * 40
        d.line([(x - 260 - i * 30, y), (x - 70, y)], (255, 255, 255, 170), 6)
    person(d, x, 820, 0.9, mood="shock", arms="up", lean=1.0)
    label(d, "WHOOSH →", 300, 56, fill=(255, 235, 80), p=p * 3)
    return (120, 180, 235), (220, 235, 250)


# --------------------------------------------------------------------------- beat 2
def s2a(d, t, T):
    p = t / T
    stars(d)
    rot = t * 1.2
    earth(d, 360, 700, 300, rot)
    d.d.arc([(360 - 300) * K, (700 - 40) * K, (360 + 300) * K, (700 + 40) * K], 0, 180, fill=(255, 220, 90), width=6 * K)
    d.ell(360, 740, 12, 12, (255, 80, 80))
    d.ell(360, 740, 22, 22, (255, 80, 80, 80))
    mph = int(round(1000 * ease(p / 0.6), -1))
    d.text(360, 300, f"{mph:,} MPH", 80, (255, 235, 80), stroke=5)
    label(d, "YOU, AT THE EQUATOR", 1080, 38, p=p * 2)
    return SPACE


def s2b(d, t, T):
    p = t / T
    grass(d)
    for i, (cx, cy) in enumerate([(150, 330), (520, 260), (380, 420)]):
        d.ell(cx, cy, 90, 40, (255, 255, 255, 220))
        d.ell(cx + 50, cy - 20, 60, 40, (255, 255, 255, 220))
    tree(d, 140, 900, 0.75)
    person(d, 420, 1000, 1.0, mood="neutral")
    d.rect(80, 445, 640, 495, (0, 0, 0, 120), r=25)
    d.text(360, 470, "EVERYTHING MOVES TOGETHER →", 28, (255, 255, 255))
    label(d, "YOU CAN'T FEEL IT", 560 - 180, 50, p=(p - 0.3) * 2)
    return (120, 180, 235), (220, 235, 250)


# --------------------------------------------------------------------------- beat 3
def s3a(d, t, T):
    p = t / T
    ground_scene(d, 900)
    q = ease((p - 0.15) / 0.85) ** 1.5
    off = q * 900
    house(d, 200 + off * 0.8, 900, 0.9)
    tree(d, 520 + off, 900, 0.8, bend=-0.3 * q)
    car(d, 260 + off * 1.2, 1060, 0.8)
    if q > 0.02:
        speed_lines(d, 0, W, 450, 1060, t, 16, col=(255, 255, 255, 120))
    stamp(d, "GROUND STOPS", 260, p * 1.5)
    return (120, 180, 235), (250, 210, 170)


def s3b(d, t, T):
    p = t / T
    ground_scene(d, 900)
    speed_lines(d, 0, W, 300, 900, t, 18, col=(255, 255, 255, 140), speed=1400)
    x = -150 + p * 1050
    layer_rotated(d, 420, 260, -t * 4, x, 640, lambda L: car(L, 210, 230, 0.75))
    rnd = random.Random(8)
    for i in range(7):
        bx = (rnd.uniform(-200, W) + t * rnd.uniform(500, 900)) % (W + 200) - 100
        layer_rotated(d, 70, 70, t * rnd.uniform(-6, 6), bx, rnd.uniform(380, 860),
                      lambda L, c=rnd.choice([(190, 140, 80), (200, 70, 60), (120, 120, 130)]): L.rect(8, 8, 62, 62, c, r=6))
    label(d, "CARS. TREES. HOUSES.", 260, 44, p=p * 2)
    return (130, 170, 220), (230, 200, 170)


# --------------------------------------------------------------------------- beat 4
def s4a(d, t, T):
    p = t / T
    grass(d, 950)
    for i, x in enumerate((140, 380, 620)):
        tree(d, x, 950, 0.9, bend=0.85 + 0.08 * math.sin(t * 25 + i))
    speed_lines(d, -100, W + 100, 250, 900, t, 26, seed=5, col=(255, 255, 255, 170), speed=2200)
    label(d, "SUPERSONIC WINDS", 270, 50, fill=(255, 235, 80), p=p * 2)
    return (110, 130, 160), (170, 180, 190)


def s4b(d, t, T):
    p = t / T
    stars(d)
    cx, cy, r = 360, 700, 300
    earth(d, cx, cy, r, 1.0)
    rnd = random.Random(4)
    for _ in range(26):
        yy = rnd.uniform(-r * 0.92, r * 0.92)
        half = math.sqrt(r * r - yy * yy)
        L = rnd.uniform(60, 200)
        x = cx - half + ((rnd.uniform(0, 2 * half) + t * rnd.uniform(500, 900)) % (2 * half + L)) - L
        x0, x1 = max(cx - half, x), min(cx + half, x + L)
        if x1 > x0:
            d.line([(x0, cy + yy), (x1, cy + yy)], (255, 255, 255, 190), rnd.uniform(4, 9))
    label(d, "THE WHOLE PLANET", 280, 44, p=p * 2)
    return SPACE


# --------------------------------------------------------------------------- beat 5
def skyline(d, base=1000, seed=21, lit=0.3):
    rnd = random.Random(seed)
    x = 0
    while x < W:
        bw, bh = rnd.uniform(70, 130), rnd.uniform(200, 460)
        d.rect(x, base - bh, x + bw - 6, base, (90, 95, 120))
        for wy in range(int(base - bh + 20), base - 20, 40):
            for wx in range(int(x + 10), int(x + bw - 20), 28):
                d.rect(wx, wy, wx + 14, wy + 20, (255, 215, 120) if rnd.random() < lit else (120, 125, 150))
        x += bw


def wave_poly(d, crest_x, height, base, t):
    pts = [(-50, base)]
    for i in range(0, 41):
        x = -50 + i * (crest_x + 50) / 40
        f = (i / 40) ** 2.2
        pts.append((x, base - height * f + 10 * math.sin(i * 0.8 + t * 6)))
    pts += [(crest_x + 60, base - height + 40), (crest_x + 90, base - height + 120), (crest_x + 20, base)]
    d.poly(pts, (30, 100, 190))
    d.line(pts[1:-2], (220, 240, 255), 14)


def s5a(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (40, 110, 200))
    skyline(d)
    wave_poly(d, 180 + 260 * ease(p), 250 + 500 * ease(p), 1120, t)
    label(d, "MEGA WAVES", 260, 56, fill=(255, 235, 80), p=p * 2)
    return (150, 170, 200), (200, 210, 225)


def s5b(d, t, T):
    p = t / T
    skyline(d)
    lvl = 1000 - 620 * ease(p / 0.7)
    d.rect(0, lvl, W, H, (30, 100, 190, 230))
    for i in range(14):
        fx = (i * 70 + t * 300) % (W + 100) - 50
        d.ell(fx, lvl + 5 * math.sin(t * 8 + i), 50, 16, (230, 245, 255, 220))
    rnd = random.Random(int(t * 15))
    for _ in range(20):
        d.ell(rnd.uniform(0, W), lvl - rnd.uniform(0, 120), rnd.uniform(6, 16), rnd.uniform(6, 16), (220, 240, 255, 200))
    label(d, "MILES INLAND", 260, 52, p=p * 2)
    return (130, 140, 160), (170, 180, 200)


# --------------------------------------------------------------------------- beat 6
def sun(d, x, y, r, t):
    for k in range(12):
        a = t * 0.5 + k * math.pi / 6
        d.line([(x + math.cos(a) * r * 1.2, y + math.sin(a) * r * 1.2),
                (x + math.cos(a) * r * 1.55, y + math.sin(a) * r * 1.55)], (255, 210, 80), 10)
    d.ell(x, y, r * 1.15, r * 1.15, (255, 220, 100, 80))
    d.ball(x, y, r, (255, 205, 70))


def s6a(d, t, T):
    p = t / T
    stars(d)
    sun(d, 90, 700, 120, t)
    earth(d, 470, 700, 210, 0.4, glow=True)
    night_half(d, 470, 700, 210)
    d.text(360, 330, "1 DAY", 84, (255, 255, 255), stroke=5)
    d.text(360, 420, "=", 70, (255, 235, 80), stroke=5)
    if p > 0.3:
        d.text(360, 960, "1 YEAR", 90 * (1 + 0.2 * (1 - ease((p - 0.3) * 6))), (255, 235, 80), stroke=6)
    return SPACE


def s6b(d, t, T):
    p = t / T
    month = min(12, 1 + int(p * 12))
    dayness = 1 - ease((p - 0.42) / 0.16)
    sky = mix((20, 24, 60), (120, 185, 240), dayness)
    d.rect(0, 0, W, H, sky)
    if dayness > 0.05:
        sun(d, 360, 420 + (1 - dayness) * 400, 80, t)
    if dayness < 0.95:
        stars(d, 7, 60)
        d.ball(560, 300, 50, (235, 235, 220))
    grass(d, 950)
    house(d, 360, 950, 1.0)
    d.rect(110, 160, 610, 250, (0, 0, 0, 140), r=20)
    d.text(360, 205, f"MONTH {month}: {'SUNLIGHT' if month <= 6 else 'DARKNESS'}",
           40, (255, 255, 255))
    return (120, 185, 240), (200, 220, 240)


# --------------------------------------------------------------------------- beat 7
def band_earth(d, cx, cy, r, band, cap):
    """Globe where land (band) grows around the equator and water gathers at the poles (cap)."""
    lay = Image.new("RGBA", (int(2 * r * K), int(2 * r * K)), (0, 0, 0, 0))
    L = D(lay)
    L.rect(0, 0, 2 * r, 2 * r, OCEAN)
    L.rect(0, r - band, 2 * r, r + band, LAND2)
    L.rect(0, r - band * 0.6, 2 * r, r + band * 0.6, shade(LAND2, 1.1))
    L.rect(0, 0, 2 * r, cap, (60, 140, 235))
    L.rect(0, 2 * r - cap, 2 * r, 2 * r, (60, 140, 235))
    mask = Image.new("L", lay.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, lay.width - 1, lay.height - 1], fill=255)
    d.ell(cx, cy, r * 1.08, r * 1.08, (90, 160, 255, 60))
    d.img.paste(lay, (int((cx - r) * K), int((cy - r) * K)), mask)
    d.ell(cx - r * 0.38, cy - r * 0.42, r * 0.28, r * 0.18, (255, 255, 255, 60))


def s7a(d, t, T):
    p = t / T
    stars(d)
    q = ease(p)
    band_earth(d, 360, 700, 280, 20 + 60 * q, 30 + 50 * q)
    for sgn in (-1, 1):
        y = 700 + sgn * (140 + 40 * math.sin(t * 4))
        d.line([(360, y), (360, y + sgn * 70)], (255, 255, 255), 10)
        d.poly([(340, y + sgn * 70), (380, y + sgn * 70), (360, y + sgn * 100)], (255, 255, 255))
    label(d, "OCEANS FLOW TO THE POLES", 280, 36, p=p * 2)
    return SPACE


def s7b(d, t, T):
    p = t / T
    stars(d)
    band_earth(d, 360, 760, 420, 90 + 110 * ease(p), 90)
    label(d, "A GIANT NEW CONTINENT", 260, 40, fill=(255, 235, 80), p=p * 2)
    return SPACE


# --------------------------------------------------------------------------- beat 8
def s8a(d, t, T):
    p = t / T
    cx, cy, r = 360, 760, 260
    d.d.pieslice([(cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K], 180, 360, fill=(40, 44, 60))
    d.d.arc([(cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K], 180, 360, fill=(255, 255, 255), width=10 * K)
    for k in range(11):
        a = math.pi + k * math.pi / 10
        d.line([(cx + math.cos(a) * r * 0.85, cy + math.sin(a) * r * 0.85),
                (cx + math.cos(a) * r * 0.97, cy + math.sin(a) * r * 0.97)], (255, 255, 255), 6)
    a = math.pi + math.pi * (0.85 - 0.25 * ease(p) + 0.01 * math.sin(t * 30))
    d.line([(cx, cy), (cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8)], (255, 80, 60), 12)
    earth(d, cx, cy, 60, t, glow=False)
    stamp(d, "SLOWING DOWN", 1000, p * 1.5)
    return (40, 40, 80), (90, 50, 90)


def s8b(d, t, T):
    p = t / T
    cx, cy = 360, 700
    d.ell(cx, cy, 250, 250, (240, 240, 245))
    d.ell(cx, cy, 250, 250, None, outline=(60, 60, 70), w=14)
    for k in range(12):
        a = k * math.pi / 6
        d.line([(cx + math.cos(a) * 200, cy + math.sin(a) * 200), (cx + math.cos(a) * 230, cy + math.sin(a) * 230)],
               (60, 60, 70), 8)
    for L, sp, w in ((150, 0.6, 14), (200, 6, 8)):
        a = t * sp - math.pi / 2
        d.line([(cx, cy), (cx + math.cos(a) * L, cy + math.sin(a) * L)], (40, 40, 50), w)
    d.text(360, 300, "RIGHT NOW", 70, (255, 235, 80), stroke=5)
    return (40, 40, 80), (90, 50, 90)


# --------------------------------------------------------------------------- beat 9
def dino(d, x, ground, t):
    g = (110, 175, 90)
    d.shadow(x, ground, 220, 20)
    d.poly([(x - 120, ground - 170), (x - 380, ground - 60), (x - 120, ground - 120)], shade(g, 0.9))
    for lx in (-90, -30, 60, 120):
        d.rect(x + lx - 22, ground - 140, x + lx + 22, ground, shade(g, 0.85), r=14)
    d.ell(x, ground - 180, 170, 95, g)
    d.ell(x - 20, ground - 215, 120, 40, (255, 255, 255, 50))
    nod = 10 * math.sin(t * 2)
    d.line([(x + 120, ground - 220), (x + 200, ground - 380), (x + 240, ground - 470 + nod)], g, 46)
    d.ell(x + 265, ground - 475 + nod, 50, 30, g)
    d.ell(x + 280, ground - 485 + nod, 7, 7, (20, 20, 20))


def s9a(d, t, T):
    p = t / T
    grass(d, 1000)
    sun(d, 580, 300, 70, t)
    dino(d, 330, 1080, t)
    d.rect(60, 160, 380, 290, (0, 0, 0, 140), r=20)
    d.text(220, 205, "DAY LENGTH", 30, (255, 255, 255))
    d.text(220, 255, "23.5 HOURS", 42, (255, 235, 80))
    return (250, 200, 130), (240, 160, 110)


def s9b(d, t, T):
    p = t / T
    stars(d)
    cx, cy = 300, 700
    d.ell(cx, cy, 260, 210, (80, 160, 255, 90))
    earth(d, cx, cy, 190, t * 0.8, glow=False)
    mx = 610
    d.ball(mx, cy, 60, (220, 220, 210))
    for k in range(3):
        y = cy - 40 + k * 40
        d.line([(mx - 80, y), (cx + 280, y)], (255, 235, 80, 200), 6)
        d.poly([(cx + 270, y - 12), (cx + 270, y + 12), (cx + 250, y)], (255, 235, 80, 200))
    label(d, "THE MOON PUTS ON THE BRAKES", 300, 32, p=p * 2)
    return SPACE


# --------------------------------------------------------------------------- beat 10
def s10a(d, t, T):
    p = t / T
    cx, cy = 360, 700
    d.rect(cx - 30, cy - 330, cx + 30, cy - 270, (90, 95, 110), r=10)
    d.ell(cx, cy, 260, 260, (90, 95, 110))
    d.ell(cx, cy, 230, 230, (245, 245, 250))
    a = t * 0.4 - math.pi / 2
    d.line([(cx, cy), (cx + math.cos(a) * 190, cy + math.sin(a) * 190)], (230, 60, 50), 10)
    d.ell(cx, cy, 16, 16, (40, 40, 50))
    d.text(cx, cy + 90, "+0.002 s", 64, (40, 40, 50))
    label(d, "PER CENTURY", 1020, 52, fill=(255, 235, 80), p=p * 2)
    return (40, 60, 100), (30, 40, 70)


def s10b(d, t, T):
    p = t / T
    stars(d)
    earth(d, 360, 430, 230, t * 1.5)
    d.d.arc([(360 - 280) * K, (430 - 280) * K, (360 + 280) * K, (430 + 280) * K], 200, 340, fill=(255, 220, 90), width=8 * K)
    d.rect(0, 1000, W, H, (95, 170, 85))
    person(d, 360, 1140, 0.95, mood="happy", arms="up" if int(t * 3) % 2 else "down")
    label(d, "STILL SPINNING!", 760, 52, fill=(255, 235, 80), p=(p - 0.3) * 2)
    return SPACE


def outro(d, t, T):
    stars(d)
    earth(d, 360, 560, 170 * ease(t / T * 3), t * 1.5)
    d.text(360, 860, "WHAT SHOULD I", 62, (255, 255, 255), stroke=5)
    d.text(360, 950, "EXPLAIN NEXT?", 62, (255, 235, 80), stroke=5)
    d.text(360, 1050, "COMMENT BELOW", 38, (255, 255, 255), stroke=3)
    return SPACE


SHOTS = {f"beat_{i}_{ab}": globals()[f"s{i}{ab}"] for i in range(1, 11) for ab in "ab"}
SHOTS["outro"] = outro
