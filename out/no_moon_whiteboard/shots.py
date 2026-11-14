"""Whiteboard-doodle version of the no_moon short (rendered by scripts/free_render.py)."""
from free_render import *  # noqa: F401,F403
from whiteboard import Board, BOARD, INK, BLUE, RED, YELLOW, GREEN, ORANGE, circle_pts

GREY = (150, 150, 160)


# --------------------------------------------------------------------------- doodle props
def moon(b, x, y, r, at=0.0, dur=0.2, fill=True):
    b.circle(x, y, r, at=at, dur=dur)
    for k, (cx, cy, cr) in enumerate(((-0.35, -0.2, 0.2), (0.3, 0.3, 0.22), (0.25, -0.38, 0.12))):
        b.circle(x + cx * r, y + cy * r, cr * r, at=at + dur + k * 0.03, dur=0.06, w=4)
    if fill:
        b.fill_circle(x, y, r, GREY, at=at + dur + 0.1, alpha=90)


def waves(b, y, at=0.0, dur=0.25, col=BLUE, n=7, amp=14, t=0.0):
    pts = [(x, y + amp * math.sin(x / 40 + t * 2)) for x in range(20, W - 19, 12)]
    return b.stroke(pts, at=at, dur=dur, col=col, w=7)


def earth(b, x, y, r, at=0.0, dur=0.2):
    b.circle(x, y, r, at=at, dur=dur)
    b.fill_circle(x, y, r, BLUE, at=at + dur, alpha=110)
    b.stroke(circle_pts(x - r * 0.3, y - r * 0.2, r * 0.35, r * 0.22, n=20), at=at + dur + 0.02, dur=0.08, col=GREEN, w=6)
    b.stroke(circle_pts(x + r * 0.35, y + r * 0.3, r * 0.25, r * 0.3, n=20), at=at + dur + 0.06, dur=0.08, col=GREEN, w=6)


def crab(b, x, y, s=1.0, at=0.0, sad=False):
    b.circle(x, y, 60 * s, 38 * s, at=at, dur=0.12, col=RED)
    b.fill_circle(x, y, 40 * s, RED, at=at + 0.12, alpha=120)
    for side in (-1, 1):
        for k in range(3):
            b.line(x + side * 50 * s, y + 10 * s, x + side * (85 + k * 6) * s, y + (24 + k * 14) * s,
                   at=at + 0.12, dur=0.05, col=RED, w=5)
        b.line(x + side * 45 * s, y - 20 * s, x + side * 75 * s, y - 55 * s, at=at + 0.16, dur=0.05, col=RED, w=6)
        b.circle(x + side * 82 * s, y - 64 * s, 18 * s, 14 * s, at=at + 0.2, dur=0.05, col=RED)
    for ex in (-18, 18):
        b.line(x + ex * s, y - 34 * s, x + ex * s, y - 58 * s, at=at + 0.22, dur=0.04, w=4)
        b.circle(x + ex * s, y - 64 * s, 8 * s, at=at + 0.24, dur=0.04, w=4)
    mouth = circle_pts(x, y + (18 if sad else 0) * s, 16 * s, 9 * s, n=12, a0=200 if sad else 20, sweep=140)
    b.stroke(mouth, at=at + 0.26, dur=0.05, w=4)


def star(b, x, y, r, at=0.0, dur=0.08, col=INK, w=4):
    pts = []
    for k in range(11):
        a = -math.pi / 2 + k * 4 * math.pi / 5
        pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
    return b.stroke(pts, at=at, dur=dur, col=col, w=w)


def stick(b, x, ground, s=1.0, at=0.0, wave=0.0, happy=True):
    hy = ground - 230 * s
    b.circle(x, hy, 38 * s, at=at, dur=0.08)
    b.line(x, hy + 38 * s, x, ground - 90 * s, at=at + 0.08, dur=0.05)
    b.line(x, ground - 90 * s, x - 35 * s, ground, at=at + 0.13, dur=0.04)
    b.line(x, ground - 90 * s, x + 35 * s, ground, at=at + 0.15, dur=0.04)
    b.line(x, hy + 70 * s, x - 55 * s, hy + 120 * s, at=at + 0.17, dur=0.04)
    b.line(x, hy + 70 * s, x + 60 * s, hy + 10 * s - wave * 40 * s, at=at + 0.19, dur=0.04)
    for ex in (-13, 13):
        b.circle(x + ex * s, hy - 6 * s, 3 * s, at=at + 0.21, dur=0.02, w=5)
    b.stroke(circle_pts(x, hy + 6 * s, 16 * s, 10 * s, n=10, a0=20 if happy else 200, sweep=140),
             at=at + 0.22, dur=0.03, w=4)


def house(b, x, ground, s=1.0, at=0.0):
    b.rect(x - 100 * s, ground - 200 * s, x + 100 * s, ground, at=at, dur=0.1)
    b.stroke([(x - 125 * s, ground - 195 * s), (x, ground - 310 * s), (x + 125 * s, ground - 195 * s)],
             at=at + 0.1, dur=0.07)
    b.rect(x - 28 * s, ground - 100 * s, x + 28 * s, ground, at=at + 0.17, dur=0.05)
    b.fill_rect(x - 125 * s, ground - 310 * s, x + 125 * s, ground - 200 * s, RED, at=at + 0.22, alpha=0)


def tree(b, x, ground, s=1.0, at=0.0):
    b.line(x, ground, x, ground - 150 * s, at=at, dur=0.05, col=(120, 80, 40), w=10)
    b.circle(x, ground - 220 * s, 80 * s, 70 * s, at=at + 0.05, dur=0.1, col=GREEN)
    b.fill_circle(x, ground - 220 * s, 72 * s, GREEN, at=at + 0.15, alpha=100)


def coral(b, x, ground, s=1.0, col=RED, at=0.0):
    for k, (dx, h) in enumerate(((-40, 140), (0, 190), (40, 150), (-70, 90), (70, 100))):
        b.line(x + dx * 0.3 * s, ground, x + dx * s, ground - h * s, at=at + k * 0.02, dur=0.06, col=col, w=12)
        b.circle(x + dx * s, ground - h * s, 14 * s, at=at + 0.1 + k * 0.02, dur=0.04, col=col, w=6)


def sun(b, x, y, r, at=0.0, rays=True):
    b.circle(x, y, r, at=at, dur=0.1, col=ORANGE)
    b.fill_circle(x, y, r, YELLOW, at=at + 0.1)
    if rays:
        for k in range(10):
            a = k * math.pi / 5
            b.line(x + math.cos(a) * r * 1.25, y + math.sin(a) * r * 1.25, x + math.cos(a) * r * 1.6,
                   y + math.sin(a) * r * 1.6, at=at + 0.12 + k * 0.01, dur=0.03, col=ORANGE, w=6)


def ruler(b, x0, x1, y, at=0.0, marks=10):
    b.rect(x0, y - 35, x1, y + 35, at=at, dur=0.12)
    b.fill_rect(x0, y - 35, x1, y + 35, YELLOW, at=at + 0.12, alpha=140)
    for k in range(marks + 1):
        x = x0 + (x1 - x0) * k / marks
        b.line(x, y - 35, x, y - (10 if k % 5 else -5), at=at + 0.14 + k * 0.005, dur=0.02, w=3)


def big_x(b, x, y, r, at=0.0):
    b.line(x - r, y - r, x + r, y + r, at=at, dur=0.08, col=RED, w=16)
    b.line(x + r, y - r, x - r, y + r, at=at + 0.08, dur=0.08, col=RED, w=16)


# --------------------------------------------------------------------------- shots
def s1a(d, t, T):
    b = Board(d, t, T)
    moon(b, 360, 520, 150, at=0.0, dur=0.25)
    b.write("?", 560, 340, 120, at=0.5, dur=0.05, col=RED)
    if b.p > 0.6:
        d.rect(150, 340, 570, 700, BOARD[0] + (int(230 * ease((b.p - 0.6) / 0.3)),), r=40)
        b.write("GONE!", 360, 530, 90, at=0.7, dur=0.12, col=RED)
    b.finish()
    return BOARD


def s1b(d, t, T):
    b = Board(d, t, T)
    for k in range(4):
        waves(b, 640 + k * 70, at=k * 0.12, dur=0.2, t=t)
    b.write("THE OCEAN?", 360, 400, 80, at=0.45, dur=0.25, col=BLUE)
    b.finish()
    return BOARD


def s2a(d, t, T):
    b = Board(d, t, T)
    b.circle(290, 680, 230, 190, at=0.25, dur=0.2, col=BLUE, w=4)
    earth(b, 290, 680, 160, at=0.0, dur=0.18)
    moon(b, 610, 680, 55, at=0.12, dur=0.1)
    b.arrow(540, 680, 470, 680, at=0.5, dur=0.12, col=RED)
    b.write("PULL!", 520, 600, 50, at=0.6, dur=0.1, col=RED)
    b.finish()
    return BOARD


def s2b(d, t, T):
    b = Board(d, t, T)
    b.rect(330, 320, 390, 1060, at=0.0, dur=0.15)
    for k in range(8):
        b.line(330, 380 + k * 85, 360, 380 + k * 85, at=0.12 + k * 0.01, dur=0.02, w=4)
    waves(b, 470, at=0.2, dur=0.15)
    b.write("NOW", 200, 470, 46, at=0.3, dur=0.06, col=BLUE)
    waves(b, 860, at=0.5, dur=0.15, col=RED)
    b.write("1/3", 540, 790, 70, at=0.62, dur=0.06, col=RED)
    b.arrow(560, 520, 560, 720, at=0.68, dur=0.12, col=RED)
    b.finish()
    return BOARD


def s3a(d, t, T):
    b = Board(d, t, T)
    for x, y, rx, ry in ((90, 900, 130, 80), (640, 900, 140, 90)):
        b.circle(x, y, rx, ry, at=0.0, dur=0.12, col=GREY)
    b.circle(360, 930, 230, 60, at=0.12, dur=0.12, col=BLUE)
    b.fill_circle(360, 930, 60, BLUE, at=0.24, alpha=0)
    crab(b, 300, 820, 0.8, at=0.25)
    star(b, 500, 870, 34, at=0.55, col=ORANGE, w=6)
    b.write("ROCK POOLS", 360, 360, 70, at=0.62, dur=0.15)
    b.finish()
    return BOARD


def s3b(d, t, T):
    b = Board(d, t, T)
    crab(b, 360, 700, 1.9, at=0.0, sad=True)
    b.circle(250, 600, 10, 18, at=0.4, dur=0.05, col=BLUE)
    b.write("STRUGGLING", 360, 350, 70, at=0.5, dur=0.2, col=RED)
    b.finish()
    return BOARD


def s4a(d, t, T):
    b = Board(d, t, T)
    house(b, 230, 980, 1.0, at=0.0)
    tree(b, 540, 980, 0.9, at=0.15)
    moon(b, 560, 330, 70, at=0.3, dur=0.1)
    b.line(30, 980, 690, 980, at=0.05, dur=0.15)
    q = ease((b.p - 0.6) / 0.35)
    if q > 0:
        for k in range(int(q * 40)):
            y = 160 + k * 22
            d.line([(20, y), (700, y - 60)], (40, 40, 60, 90), 8)
    b.finish()
    return BOARD


def s4b(d, t, T):
    b = Board(d, t, T)
    rnd = random.Random(3)
    for k in range(18):
        y = rnd.choice((rnd.uniform(220, 530), rnd.uniform(720, 980)))  # keep the middle clear for the words
        star(b, rnd.uniform(60, 660), y, rnd.uniform(14, 30), at=k * 0.03, dur=0.05)
    b.write("JUST STARS", 360, 620, 80, at=0.55, dur=0.2)
    b.finish()
    return BOARD


def s5a(d, t, T):
    b = Board(d, t, T)
    moon(b, 360, 300, 70, at=0.0, dur=0.1)
    b.line(30, 1060, 690, 1060, at=0.05, dur=0.1)
    for k, (x, col) in enumerate(((150, RED), (360, ORANGE), (570, (170, 90, 200)))):
        coral(b, x, 1060, 1.0, col, at=0.12 + k * 0.08)
    if b.p > 0.5:
        rnd = random.Random(2)
        for _ in range(40):
            x = rnd.uniform(80, 640)
            y = 980 - ((rnd.uniform(0, 500) + t * rnd.uniform(40, 90)) % 560)
            d.ell(x, y, 6, 6, (240, 120, 160))
    b.write("CORAL EGGS", 360, 470, 60, at=0.55, dur=0.15, col=RED)
    b.finish()
    return BOARD


def s5b(d, t, T):
    b = Board(d, t, T)
    b.line(30, 1060, 690, 1060, at=0.0, dur=0.1)
    for k, x in enumerate((150, 360, 570)):
        coral(b, x, 1060, 1.0, GREY, at=0.05 + k * 0.06)
    for k in range(3):
        b.write("?", 210 + k * 150, 640 - (k % 2) * 60, 100, at=0.4 + k * 0.08, dur=0.04, col=RED)
    b.write("NO SIGNAL", 360, 400, 70, at=0.65, dur=0.15)
    b.finish()
    return BOARD


def s6a(d, t, T):
    b = Board(d, t, T)
    sun(b, 360, 640, 150, at=0.0)
    q = ease((b.p - 0.35) / 0.4)
    if q > 0:
        d.ell(360 - 300 + 300 * q, 640, 150, 150, INK)
    b.write("ECLIPSE", 360, 950, 70, at=0.6, dur=0.15)
    b.finish()
    return BOARD


def s6b(d, t, T):
    b = Board(d, t, T)
    sun(b, 360, 640, 150, at=-1)
    d.ell(360, 640, 150, 150, INK)
    big_x(b, 360, 640, 230, at=0.15)
    b.write("NO MORE!", 360, 960, 80, at=0.45, dur=0.15, col=RED)
    b.finish()
    return BOARD


def s7a(d, t, T):
    b = Board(d, t, T)
    b.rect(90, 400, 630, 960, at=0.0, dur=0.15)
    b.line(90, 490, 630, 490, at=0.15, dur=0.05)
    b.write("CALENDAR", 360, 445, 50, at=0.2, dur=0.1)
    for k in range(8):
        x, y = 170 + (k % 4) * 127, 620 + (k // 4) * 200
        at = 0.3 + k * 0.05
        b.circle(x, y, 45, at=at, dur=0.04, w=4)
        f = (k + 0.5) / 8
        if b.prog(at + 0.04, 0.02) > 0:
            off = (1 - 2 * abs(f - 0.5)) * 90 * (1 if f < 0.5 else -1)
            d.d.chord([(x - 45) * K, (y - 45) * K, (x + 45) * K, (y + 45) * K], -90 if off > 0 else 90,
                      90 if off > 0 else 270, fill=GREY + (150,)) if abs(f - 0.5) > 0.05 else d.ell(x, y, 43, 43, GREY + (150,))
    b.finish()
    return BOARD


def s7b(d, t, T):
    b = Board(d, t, T)
    b.write("MOON", 360, 520, 120, at=0.0, dur=0.15)
    b.arrow(360, 600, 360, 720, at=0.2, dur=0.1, col=RED)
    b.write("MONTH", 360, 820, 120, at=0.35, dur=0.2, col=BLUE)
    b.stroke([(170, 880), (550, 880)], at=0.6, dur=0.1, col=YELLOW, w=14)
    b.finish()
    return BOARD


def s8a(d, t, T):
    b = Board(d, t, T)
    earth(b, 360, 680, 210, at=0.0, dur=0.2)
    tilt = math.radians(23 + 20 * math.sin(t * 2) * ease((b.p - 0.4) * 3))
    dx, dy = math.sin(tilt) * 320, -math.cos(tilt) * 320
    if b.p > 0.3:
        d.line([(360 - dx, 680 - dy), (360 + dx, 680 + dy)], RED, 6)
    b.write("WOBBLE!", 360, 300, 80, at=0.5, dur=0.15, col=RED)
    b.finish()
    return BOARD


def s8b(d, t, T):
    b = Board(d, t, T)
    b.line(360, 200, 360, 1060, at=0.0, dur=0.1)
    sun(b, 190, 520, 80, at=0.1)
    for k in range(3):
        a = k * math.pi / 3
        b.line(540 - math.cos(a) * 80, 520 - math.sin(a) * 80, 540 + math.cos(a) * 80, 520 + math.sin(a) * 80,
               at=0.35 + k * 0.05, dur=0.05, col=BLUE, w=8)
    b.write("HOT!", 190, 760, 70, at=0.55, dur=0.08, col=RED)
    b.write("COLD!", 540, 760, 70, at=0.65, dur=0.08, col=BLUE)
    b.finish()
    return BOARD


def s9a(d, t, T):
    b = Board(d, t, T)
    earth(b, 170, 680, 120, at=0.0, dur=0.15)
    mx = 460 + 140 * ease((b.p - 0.3) / 0.6)
    moon(b, mx, 680, 50, at=0.1, dur=0.1)
    b.arrow(mx + 70, 680, mx + 150, 680, at=0.35, dur=0.1, col=RED)
    b.write("BYE?!", 460, 480, 70, at=0.5, dur=0.1, col=RED)
    b.finish()
    return BOARD


def s9b(d, t, T):
    b = Board(d, t, T)
    earth(b, 110, 680, 80, at=-1)
    moon(b, 620, 680, 40, at=-1)
    ruler(b, 210, 570, 680, at=0.1)
    b.finish()
    return BOARD


def s10a(d, t, T):
    b = Board(d, t, T)
    b.write("+4 cm", 360, 480, 130, at=0.0, dur=0.2, col=RED)
    b.write("EVERY YEAR", 360, 600, 60, at=0.2, dur=0.15)
    ruler(b, 110, 610, 780, at=0.35, marks=20)
    b.finish()
    return BOARD


def s10b(d, t, T):
    b = Board(d, t, T)
    b.stroke([(220, 1240), (220, 620), (240, 520), (360, 470), (480, 520), (500, 620), (500, 1240)], at=0.0, dur=0.25)
    grow = 50 * ease((b.p - 0.4) / 0.5)
    b.stroke([(270, 640), (270, 520 - grow), (360, 490 - grow), (450, 520 - grow), (450, 640), (270, 640)],
             at=0.25, dur=0.2, col=(220, 120, 140))
    b.fill_rect(270, 500 - grow, 450, 640, (255, 200, 210), at=0.45)
    b.write("NAILS GROW", 360, 300, 70, at=0.5, dur=0.15)
    b.write("THIS FAST!", 360, 380, 70, at=0.62, dur=0.15, col=RED)
    b.finish()
    return BOARD


def s11a(d, t, T):
    b = Board(d, t, T)
    my = 760 - 360 * ease(b.p)
    moon(b, 360, my, 100, at=0.0, dur=0.15)
    b.fill_rect(0, 860, W, H, BOARD[0], at=0.0, dur=0.01, alpha=255)
    b.stroke([(x, 900 - 60 * math.sin(x / 230)) for x in range(0, W + 1, 20)], at=0.05, dur=0.2, col=GREEN, w=8)
    b.write("BILLIONS OF YEARS", 360, 1010, 50, at=0.45, dur=0.2)
    b.finish()
    return BOARD


def s11b(d, t, T):
    b = Board(d, t, T)
    moon(b, 540, 330, 90, at=0.0, dur=0.12)
    b.stroke([(x, 1000 - 40 * math.sin(x / 200)) for x in range(0, W + 1, 20)], at=0.1, dur=0.15, col=GREEN, w=8)
    stick(b, 280, 990, 1.0, at=0.2, wave=0.5 + 0.5 * math.sin(t * 8) if b.p > 0.45 else 0)
    b.write("ENJOY THE VIEW!", 360, 620, 60, at=0.5, dur=0.2, col=BLUE)
    b.finish()
    return BOARD


def outro(d, t, T):
    b = Board(d, t, T)
    moon(b, 360, 500, 140, at=0.0, dur=0.2)
    b.write("WHAT SHOULD I", 360, 800, 70, at=0.25, dur=0.15)
    b.write("EXPLAIN NEXT?", 360, 890, 70, at=0.4, dur=0.15, col=BLUE)
    b.write("comment below", 360, 990, 46, at=0.55, dur=0.15, col=RED)
    b.finish()
    return BOARD


SHOTS = {f"beat_{i}_{ab}": globals()[f"s{i}{ab}"] for i in range(1, 12) for ab in "ab"}
SHOTS["outro"] = outro
