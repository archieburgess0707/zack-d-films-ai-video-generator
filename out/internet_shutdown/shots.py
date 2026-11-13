"""Procedural scenes for the internet_shutdown short (rendered by scripts/free_render.py)."""
from free_render import *  # noqa: F401,F403

DARK = ((24, 28, 50), (40, 34, 70))
FRIEND = (240, 150, 50)


# --------------------------------------------------------------------------- props
def phone(d, cx, cy, s=1.0, screen=(30, 34, 46)):
    w, h = 170 * s, 340 * s
    d.rect(cx - w + 10, cy - h + 14, cx + w + 10, cy + h + 14, (0, 0, 0, 80), r=44 * s)
    d.rect(cx - w, cy - h, cx + w, cy + h, (30, 30, 36), r=44 * s)
    d.rect(cx - w + 14 * s, cy - h + 14 * s, cx + w - 14 * s, cy + h - 14 * s, screen, r=32 * s)
    d.rect(cx - 40 * s, cy - h + 22 * s, cx + 40 * s, cy - h + 40 * s, (30, 30, 36), r=9 * s)
    return (cx - w + 14 * s, cy - h + 14 * s, cx + w - 14 * s, cy + h - 14 * s)


def wifi(d, cx, cy, s=1.0, bars=3, col=(255, 255, 255), off=(80, 85, 100), crossed=False):
    for k in range(3):
        r = (60 + k * 50) * s
        d.d.arc([(cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K], 225, 315,
                fill=col if k < bars else off, width=int(20 * s * K))
    d.ell(cx, cy - 10 * s, 16 * s, 16 * s, col if bars > 0 else off)
    if crossed:
        d.line([(cx - 130 * s, cy - 200 * s), (cx + 130 * s, cy + 30 * s)], (235, 50, 50), 18 * s)


def spinner(d, cx, cy, r, t, col=(255, 255, 255)):
    for k in range(8):
        a = k * math.pi / 4 + t * 4
        al = int(60 + 195 * ((k / 8 + t * 0.6) % 1))
        d.ell(cx + math.cos(a) * r, cy + math.sin(a) * r, r * 0.18, r * 0.18, col + (al,))


def card(d, x, y, s=1.0, col=(60, 110, 220)):
    d.rect(x - 130 * s + 6, y - 82 * s + 8, x + 130 * s + 6, y + 82 * s + 8, (0, 0, 0, 80), r=16 * s)
    d.rect(x - 130 * s, y - 82 * s, x + 130 * s, y + 82 * s, col, r=16 * s)
    d.rect(x - 100 * s, y - 40 * s, x - 50 * s, y, (240, 200, 90), r=6 * s)
    d.text(x - 20 * s, y + 45 * s, "**** 4821", 24 * s, (255, 255, 255))


def terminal(d, x, y, err):
    d.rect(x - 110, y - 170, x + 110, y + 170, (50, 50, 60), r=24)
    d.rect(x - 90, y - 150, x + 90, y - 50, (240, 60, 50) if err else (120, 220, 140), r=10)
    d.text(x, y - 100, "ERROR" if err else "...", 34, (255, 255, 255))
    for r_ in range(3):
        for c in range(3):
            d.rect(x - 75 + c * 55, y - 25 + r_ * 55, x - 35 + c * 55, y + 15 + r_ * 55, (90, 90, 105), r=8)


def shelves(d, frac_gone, seed=0):
    for row in range(4):
        y = 430 + row * 150
        d.rect(40, y + 110, 680, y + 126, (150, 150, 160))
        rnd = random.Random(row + seed)
        for i in range(9):
            if rnd.random() >= frac_gone:
                c = rnd.choice([(230, 70, 60), (250, 190, 50), (70, 150, 230), (80, 190, 110)])
                d.rect(55 + i * 70, y + 30, 105 + i * 70, y + 110, c, r=6)


def satellite(d, x, y, s=1.0):
    d.rect(x - 110 * s, y - 22 * s, x - 40 * s, y + 22 * s, (60, 110, 200))
    d.rect(x + 40 * s, y - 22 * s, x + 110 * s, y + 22 * s, (60, 110, 200))
    for k in range(3):
        d.line([(x - 110 * s + k * 23 * s, y - 22 * s), (x - 110 * s + k * 23 * s, y + 22 * s)], (30, 60, 130), 3)
        d.line([(x + 40 * s + k * 23 * s, y - 22 * s), (x + 40 * s + k * 23 * s, y + 22 * s)], (30, 60, 130), 3)
    d.rect(x - 40 * s, y - 34 * s, x + 40 * s, y + 34 * s, (210, 210, 220), r=10 * s)


def bubble(d, x, y, w, h, txt, col=(255, 255, 255), tail=-1, size=34):
    d.rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, col, r=h / 2.5)
    d.poly([(x + tail * w * 0.25, y + h / 2 - 4), (x + tail * w * 0.35, y + h / 2 + 34), (x + tail * w * 0.1, y + h / 2 - 4)], col)
    d.text(x, y, txt, size, (40, 40, 50))


def coin(d, x, y, r=34):
    d.ell(x, y, r, r * 0.95, (200, 150, 40))
    d.ell(x - 2, y - 2, r * 0.82, r * 0.78, (250, 205, 70))
    d.text(x - 2, y - 2, "$", r * 1.1, (200, 150, 40))


# --------------------------------------------------------------------------- beat 1
def s1a(d, t, T):
    p = t / T
    d.rect(0, 950, W, H, (120, 110, 100))
    d.rect(0, 860, W, 960, (90, 80, 75))
    d.rect(0, 840, W, 870, (150, 140, 130))
    err = p > 0.35
    terminal(d, 470, 650, err)
    card(d, 210 + 40 * ease(p / 0.3), 540 + 30 * math.sin(t * 2), 0.8)
    if err and int(t * 5) % 2 == 0:
        d.rect(0, 0, W, H, (255, 0, 0, 30))
    label(d, "PAYMENT FAILED", 300, 50, fill=(255, 120, 120), p=(p - 0.35) * 2)
    return (230, 225, 220), (200, 195, 190)


def s1b(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (150, 150, 160))
    d.rect(60, 400, 660, 1000, (240, 235, 225))
    d.rect(60, 360, 660, 440, (60, 160, 90))
    d.text(360, 400, "SUPERMARKET", 50, (255, 255, 255))
    d.rect(200, 620, 520, 1000, (170, 215, 240))
    d.line([(360, 620), (360, 1000)], (120, 160, 190), 6)
    d.rect(250, 520, 470, 590, (40, 40, 50), r=10)
    d.text(360, 555, "OPEN", 44, (120, 255, 140))
    person(d, 360, 1130, 0.9, mood="shock", arms="shock")
    stamp(d, "CARD DECLINED", 260, (p - 0.25) * 1.5)
    return (140, 190, 235), (220, 230, 240)


# --------------------------------------------------------------------------- beat 2
def bank(d, x, y):
    d.poly([(x - 150, y - 120), (x, y - 220), (x + 150, y - 120)], (220, 220, 230))
    d.rect(x - 140, y - 120, x + 140, y + 120, (235, 235, 240))
    for k in range(4):
        d.rect(x - 115 + k * 70, y - 100, x - 85 + k * 70, y + 100, (200, 200, 210))
    d.rect(x - 160, y + 110, x + 160, y + 140, (200, 200, 210))
    d.text(x, y - 150, "BANK", 34, (90, 90, 110))


def s2a(d, t, T):
    p = t / T
    card(d, 180, 760, 0.75)
    bank(d, 530, 760)
    brk = p > 0.4
    for k in range(8):
        x = 290 + k * 18
        if brk and 3 <= k <= 4:
            continue
        ph = (t * 3 + k * 0.2) % 1
        d.ell(x + ph * 4, 760, 6, 6, (255, 235, 80) if not brk else (120, 120, 140))
    if brk:
        wifi(d, 360, 560, 0.6, bars=0, crossed=True)
    label(d, "CAN'T REACH YOUR BANK", 330, 40, p=p * 2)
    return (60, 70, 110), (35, 40, 70)


def s2b(d, t, T):
    p = t / T
    d.rect(150, 520, 570, 820, (110, 70, 45), r=30)
    d.rect(150, 520, 570, 600, (90, 55, 35), r=30)
    d.d.chord([(310) * K, (560) * K, (410) * K, (640) * K], 0, 180, fill=(60, 40, 25))
    for k in range(3):
        x = 230 + k * 130 + 15 * math.sin(t * 2 + k)
        y = 420 - (t * 40 + k * 60) % 200
        d.ell(x, y, 22, 10, (0, 0, 0, 0))
    moth = ease(p / 0.5)
    d.ell(360, 500 - 140 * moth, 22, 16, (180, 180, 170))
    d.line([(345, 495 - 140 * moth), (330, 470 - 140 * moth)], (150, 150, 140), 6)
    d.line([(375, 495 - 140 * moth), (390, 470 - 140 * moth)], (150, 150, 140), 6)
    d.rect(150, 900, 570, 1000, (250, 250, 245), r=12)
    d.text(360, 950, "CASH ONLY", 56, (220, 50, 50))
    label(d, "EMPTY WALLET", 260, 50, p=p * 2)
    return (210, 200, 180), (180, 165, 145)


# --------------------------------------------------------------------------- beat 3
def s3a(d, t, T):
    p = t / T
    d.rect(100, 420, 620, 860, (40, 44, 55), r=20)
    d.rect(120, 440, 600, 840, (235, 240, 245), r=10)
    d.rect(120, 440, 600, 500, (60, 110, 200), r=10)
    d.text(360, 470, "STOCK ORDERS", 34, (255, 255, 255))
    for k in range(3):
        d.rect(150, 530 + k * 60, 570, 570 + k * 60, (210, 215, 225), r=8)
    if p > 0.35:
        d.rect(170, 620, 550, 800, (240, 60, 50), r=16)
        d.text(360, 690, "CONNECTION", 36, (255, 255, 255))
        d.text(360, 740, "LOST", 46, (255, 255, 255))
    else:
        spinner(d, 360, 720, 50, t, (60, 110, 200))
    d.rect(300, 860, 420, 920, (40, 44, 55))
    d.rect(220, 920, 500, 945, (40, 44, 55), r=8)
    return (60, 70, 100), (40, 45, 70)


def s3b(d, t, T):
    p = t / T
    d.rect(0, 1000, W, H, (200, 200, 205))
    shelves(d, ease(p / 0.8))
    day = 1 + min(4, int(p * 5))
    d.text(360, 320, f"DAY {day}", 80, (255, 255, 255), stroke=6)
    return (240, 240, 235), (210, 210, 215)


# --------------------------------------------------------------------------- beat 4
def s4a(d, t, T):
    p = t / T
    x0, y0, x1, y1 = phone(d, 360, 700, 1.2)
    for r_ in range(4):
        for c in range(3):
            cx, cy = x0 + 70 + c * 120, y0 + 120 + r_ * 120
            d.rect(cx - 40, cy - 40, cx + 40, cy + 40, (90, 95, 110), r=18)
    d.rect(x0, y1 - 200, x1, y1, (20, 22, 30, 220), r=30)
    spinner(d, 360, y1 - 130, 30, t)
    d.text(360, y1 - 60, "NO CONNECTION", 26, (255, 255, 255))
    return DARK


def s4b(d, t, T):
    p = t / T
    d.rect(0, 0, W, H, (10, 10, 18))
    sway = math.sin(t * 1.5) * 0.15
    bx, by = 392, 788
    tip = (bx + math.cos(-1.2 + sway) * 900, by + math.sin(-1.2 + sway) * 900)
    tip2 = (bx + math.cos(-0.7 + sway) * 900, by + math.sin(-0.7 + sway) * 900)
    d.poly([(bx, by), tip, tip2], (255, 250, 210, 80))
    d.ell((tip[0] + tip2[0]) / 2, (tip[1] + tip2[1]) / 2, 180, 120, (255, 250, 210, 50))
    person(d, 300, 1100, 1.0, mood="neutral", arms="forward")
    d.rect(377, 785, 407, 835, (30, 30, 36), r=6)
    label(d, "A VERY EXPENSIVE FLASHLIGHT", 200, 32, p=p * 2)
    return (10, 10, 18), (10, 10, 18)


# --------------------------------------------------------------------------- beat 5
def s5a(d, t, T):
    p = t / T
    rnd = random.Random(1)
    for _ in range(80):
        d.ell(rnd.uniform(0, W), rnd.uniform(0, H), 1.6, 1.6, (255, 255, 255, 170))
    d.ell(360, 1500, 800, 600, (40, 110, 210))
    d.ell(360, 1500, 800, 600, None, outline=(120, 190, 255), w=6)
    px, py = 360, 960
    sats = [(140, 330), (360, 260), (590, 340)]
    for i, (sx, sy) in enumerate(sats):
        sx += 20 * math.sin(t + i)
        satellite(d, sx, sy, 0.8)
        ph = (t * 1.2 + i * 0.33) % 1
        d.line([(sx, sy + 30), (px, py)], (120, 220, 255, 90), 3)
        d.ell(sx + (px - sx) * ph, sy + 30 + (py - sy - 30) * ph, 8, 8, (150, 240, 255))
    d.ell(px, py - 40, 34, 34, (235, 60, 60))
    d.poly([(px - 28, py - 25), (px + 28, py - 25), (px, py + 20)], (235, 60, 60))
    d.ell(px, py - 40, 13, 13, (255, 255, 255))
    label(d, "GPS STILL WORKS", 520, 50, fill=(150, 240, 255), p=(p - 0.3) * 2)
    return (8, 10, 30), (20, 16, 50)


def s5b(d, t, T):
    p = t / T
    x0, y0, x1, y1 = phone(d, 360, 700, 1.2, screen=(225, 228, 232))
    for k in range(9):
        d.line([(x0, y0 + k * 75), (x1, y0 + k * 75)], (205, 208, 214), 3)
    for k in range(5):
        d.line([(x0 + k * 70, y0), (x0 + k * 70, y1)], (205, 208, 214), 3)
    d.ell(360, 640, 30, 30, (235, 60, 60))
    d.poly([(336, 652), (384, 652), (360, 690)], (235, 60, 60))
    d.ell(360, 640, 11, 11, (255, 255, 255))
    spinner(d, 360, 860, 30, t, (90, 95, 110))
    d.text(360, 930, "LOADING MAP...", 30, (90, 95, 110))
    label(d, "BUT NO MAP", 270, 50, p=p * 2)
    return (60, 70, 110), (35, 40, 70)


# --------------------------------------------------------------------------- beat 6
def s6a(d, t, T):
    p = t / T
    shake = 6 * math.sin(t * 40) if int(t * 2) % 2 == 0 else 0
    x0, y0, x1, y1 = phone(d, 360 + shake, 720, 1.1, screen=(60, 180, 100))
    d.ell(360 + shake, 600, 70, 70, (255, 255, 255))
    d.text(360 + shake, 600, "☎", 70, (60, 180, 100))
    d.text(360 + shake, 720, "HOME", 50, (255, 255, 255))
    if p > 0.4:
        bubble(d, 360, 330, 320, 110, "Texts work!", tail=1)
    return (230, 240, 235), (190, 215, 200)


def s6b(d, t, T):
    p = t / T
    blink = int(t * 6) % 2
    d.rect(0, 0, W, H, (230, 40, 40, 70) if blink else (40, 80, 230, 70))
    d.rect(110, 600, 610, 900, (245, 245, 245), r=40)
    d.rect(110, 820, 610, 860, (230, 60, 60))
    d.rect(300, 540, 420, 600, (230, 60, 60) if blink else (60, 100, 230), r=14)
    d.rect(330, 650, 390, 790, (230, 60, 60))
    d.rect(290, 690, 430, 750, (230, 60, 60))
    for wx in (220, 500):
        d.ell(wx, 910, 55, 55, (40, 40, 45))
        d.ell(wx, 910, 25, 25, (180, 180, 190))
    label(d, "EMERGENCY CALLS WORK", 360, 40, p=p * 2)
    return (40, 40, 60), (25, 25, 40)


# --------------------------------------------------------------------------- beat 7
def s7a(d, t, T):
    p = t / T
    d.rect(60, 330, 660, 1010, (20, 22, 28), r=16)
    d.text(360, 380, "DEPARTURES", 44, (255, 210, 60))
    cities = ["LONDON", "NEW YORK", "TOKYO", "PARIS", "DUBAI", "SYDNEY", "ROME", "LIMA"]
    for i, c in enumerate(cities):
        y = 460 + i * 66
        d.text(90, y, c, 30, (230, 230, 230), anchor="lm")
        if p > 0.12 + i * 0.07:
            d.text(630, y, "CANCELLED", 30, (255, 70, 60), anchor="rm")
        else:
            d.text(630, y, "ON TIME", 30, (120, 230, 140), anchor="rm")
    return (50, 55, 70), (30, 32, 45)


def s7b(d, t, T):
    p = t / T
    rnd = random.Random(4)
    for i in range(14):
        x = rnd.uniform(60, 660)
        y = (rnd.uniform(0, 1300) + t * rnd.uniform(250, 450)) % 1400 - 100
        coin(d, x, y, rnd.uniform(24, 40))
    d.rect(60, 560, 660, 800, (0, 0, 0, 170), r=30)
    d.text(360, 630, "WORLD LOSES", 44, (255, 255, 255))
    d.text(360, 720, "BILLIONS OF $", 56 * (0.6 + 0.4 * ease(p * 3)), (255, 90, 80), stroke=3)
    label(d, "EVERY SINGLE DAY", 1000, 46, fill=(255, 235, 80), p=(p - 0.4) * 2)
    return (30, 60, 40), (15, 30, 20)


# --------------------------------------------------------------------------- beat 8
def s8a(d, t, T):
    p = t / T
    dive = ease((p - 0.45) / 0.55) * 900
    for i, (cx, cy) in enumerate(((180, 420), (520, 340))):
        d.ell(cx, cy - dive, 110, 50, (255, 255, 255, 230))
        d.ell(cx + 60, cy - 30 - dive, 70, 50, (255, 255, 255, 230))
    if p < 0.5:
        d.text(360, 300, "IN THE SKY?", 66, (255, 255, 255), stroke=5)
        d.text(600, 200, "?", 80, (255, 235, 80), stroke=5)
    sea = 900 - dive
    d.rect(0, sea, W, H + 10, (30, 100, 180))
    for k in range(12):
        d.ell(k * 70 + (t * 40) % 70, sea, 40, 14, (90, 160, 230))
    if p > 0.6:
        d.text(360, 720, "DOWN HERE", 66, (255, 235, 80), stroke=5)
    return (130, 190, 240), (180, 215, 245)


def s8b(d, t, T):
    p = t / T
    d.rect(0, 0, W, H, (10, 40, 80))
    for k in range(8):
        d.ell(80 + k * 90, 300 + 30 * math.sin(k + t), 4, 4, (180, 220, 255, 120))
    d.d.chord([-200 * K, 960 * K, 920 * K, 1500 * K], 180, 360, fill=(180, 160, 110))
    pts = [(x, 1010 + 20 * math.sin(x / 90)) for x in range(-20, W + 30, 20)]
    d.line(pts, (30, 30, 35), 24)
    for k in range(5):
        ph = (t * 0.5 + k / 5) % 1
        x = -20 + ph * (W + 40)
        d.ell(x, 1010 + 20 * math.sin(x / 90), 14, 14, (120, 230, 255))
        d.ell(x, 1010 + 20 * math.sin(x / 90), 28, 28, (120, 230, 255, 60))
    for i in range(3):
        fx = (i * 260 + t * (80 + i * 30)) % (W + 200) - 100
        fy = 520 + i * 130
        d.ell(fx, fy, 55, 26, (250, 160, 60))
        d.poly([(fx - 50, fy), (fx - 90, fy - 26), (fx - 90, fy + 26)], (250, 160, 60))
        d.ell(fx + 28, fy - 6, 6, 6, (20, 20, 20))
    label(d, "CABLES ON THE OCEAN FLOOR", 300, 36, fill=(150, 230, 255), p=p * 2)
    return (10, 40, 80), (5, 20, 45)


# --------------------------------------------------------------------------- beat 9
def s9a(d, t, T):
    p = t / T
    d.rect(0, 950, W, H, (95, 170, 85))
    d.ball(600, 240, 70, (255, 210, 80))
    d.rect(160, 620, 560, 900, (240, 230, 200))
    d.line([(293, 620), (293, 900)], (210, 200, 170), 4)
    d.line([(426, 620), (426, 900)], (210, 200, 170), 4)
    d.line([(190, 820), (300, 700), (420, 760), (530, 650)], (230, 70, 60), 8)
    d.ell(530, 650, 14, 14, (230, 70, 60))
    d.ell(250, 730, 50, 30, (110, 180, 230))
    person(d, 360, 1170, 0.9, mood="happy", arms="up")
    label(d, "PAPER MAPS!", 400, 50, p=p * 2)
    return (130, 200, 245), (210, 235, 250)


def s9b(d, t, T):
    p = t / T
    d.rect(0, 950, W, H, (95, 170, 85))
    person(d, 200, 1120, 0.9, mood="happy")
    person(d, 520, 1120, 0.9, mood="happy", hoodie=FRIEND)
    if int(t * 1.5) % 2 == 0:
        bubble(d, 220, 520, 300, 110, "Hi!!", tail=-1, size=48)
    else:
        bubble(d, 500, 520, 340, 110, "Hello!", tail=1, size=48)
    label(d, "REAL CONVERSATIONS", 300, 44, p=p * 2)
    return (130, 200, 245), (210, 235, 250)


# --------------------------------------------------------------------------- beat 10
def s10a(d, t, T):
    p = t / T
    bars = min(3, int(ease(p / 0.6) * 4))
    wifi(d, 360, 760, 1.6, bars=bars, col=(120, 230, 140))
    if bars == 3:
        d.text(360, 1000, "BACK ONLINE", 70, (120, 230, 140), stroke=5)
    return DARK


def s10b(d, t, T):
    p = t / T
    shake = 10 * math.sin(t * 50) * ease(p)
    x0, y0, x1, y1 = phone(d, 360 + shake, 720, 1.0, screen=(60, 110, 200))
    rnd = random.Random(6)
    n = int(ease(p) * 26)
    for i in range(n):
        a, dist = rnd.uniform(0, 6.28), rnd.uniform(120, 420) * ease(p)
        bx, by = 360 + math.cos(a) * dist, 720 + math.sin(a) * dist * 1.3
        d.rect(bx - 70, by - 22, bx + 70, by + 22, (255, 255, 255), r=16)
        d.ell(bx - 48, by, 12, 12, rnd.choice([(230, 60, 60), (60, 180, 100), (250, 180, 40)]))
        d.rect(bx - 28, by - 6, bx + 50, by + 6, (200, 205, 215), r=4)
    cnt = int(9999 * ease(p))
    d.ell(470 + shake, 400, 80, 50, (235, 50, 50))
    d.text(470 + shake, 400, f"{cnt:,}+" if cnt >= 9999 else f"{cnt:,}", 36, (255, 255, 255))
    return DARK


def outro(d, t, T):
    wifi(d, 360, 640, 1.3 * ease(t / T * 3) + 0.01, bars=3, col=(120, 230, 140))
    d.text(360, 860, "WHAT SHOULD I", 62, (255, 255, 255), stroke=5)
    d.text(360, 950, "EXPLAIN NEXT?", 62, (255, 235, 80), stroke=5)
    d.text(360, 1050, "COMMENT BELOW", 38, (255, 255, 255), stroke=3)
    return DARK


SHOTS = {f"beat_{i}_{ab}": globals()[f"s{i}{ab}"] for i in range(1, 11) for ab in "ab"}
SHOTS["outro"] = outro
