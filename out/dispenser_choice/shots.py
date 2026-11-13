"""Procedural scenes for the dispenser_choice short (rendered by scripts/free_render.py)."""
from free_render import *  # noqa: F401,F403
import free_render

STEP = free_render.COUNT_STEP
COUNT = 3.6          # must match beats.json "countdown"
LX, RX, CY = 190, 530, 620


# --------------------------------------------------------------------------- foods (centred on x, y; ~120px at s=1)
def gloss(d, x, y, rx, ry, a=130):
    d.ell(x, y, rx, ry, (255, 255, 255, a))


def drip(d, x, y, length, w, col):
    d.rect(x - w / 2, y, x + w / 2, y + length, col, r=w / 2)
    d.ell(x, y + length, w * 0.65, w * 0.7, col)


def steam(d, x, y, t, s=1.0, n=3):
    for k in range(n):
        ph = (t * 0.6 + k / n) % 1
        ox = x + (k - (n - 1) / 2) * 26 * s + 10 * s * math.sin(t * 3 + k)
        d.ell(ox, y - ph * 90 * s, (10 + ph * 14) * s, (14 + ph * 16) * s, (255, 255, 255, int(150 * (1 - ph))))


SYRUP, SYRUP_HI = (150, 70, 15, 235), (230, 150, 70, 200)
BUTTER = (255, 228, 120)


def butter(d, x, y, s):
    d.rect(x - 20 * s, y - 13 * s, x + 20 * s, y + 13 * s, (235, 190, 70), r=5 * s)
    d.rect(x - 19 * s, y - 15 * s, x + 17 * s, y + 9 * s, BUTTER, r=5 * s)
    gloss(d, x - 8 * s, y - 8 * s, 8 * s, 3 * s, 170)


def waffle(d, x, y, s=1.0):
    d.ell(x + 4 * s, y + 66 * s, 70 * s, 12 * s, (0, 0, 0, 60))
    d.rect(x - 64 * s, y - 56 * s, x + 64 * s, y + 66 * s, (175, 105, 35), r=18 * s)
    d.rect(x - 62 * s, y - 62 * s, x + 62 * s, y + 58 * s, (225, 150, 55), r=18 * s)
    for i in range(4):
        for j in range(4):
            cx, cy = x - 42 * s + i * 28 * s, y - 42 * s + j * 28 * s
            d.rect(cx - 10 * s, cy - 10 * s, cx + 10 * s, cy + 10 * s, (170, 95, 30), r=4 * s)
            d.rect(cx - 9 * s, cy - 9 * s, cx + 7 * s, cy + 3 * s, (195, 120, 40), r=3 * s)
    d.ell(x + 8 * s, y - 4 * s, 44 * s, 30 * s, SYRUP)
    for dx, L in ((-26, 40), (14, 58), (40, 30)):
        drip(d, x + dx * s, y + 10 * s, L * s, 12 * s, SYRUP)
    gloss(d, x - 4 * s, y - 16 * s, 18 * s, 6 * s, 120)
    butter(d, x + 4 * s, y - 22 * s, s)
    gloss(d, x - 40 * s, y - 52 * s, 16 * s, 5 * s, 90)


def pancakes(d, x, y, s=1.0):
    d.ell(x, y + 58 * s, 80 * s, 16 * s, (0, 0, 0, 60))
    for k in range(5):
        yy = y + 42 * s - k * 19 * s
        d.ell(x, yy + 7 * s, 72 * s, 20 * s, (165, 95, 35))
        d.ell(x, yy, 72 * s, 19 * s, (235, 175, 95))
        d.ell(x, yy - 3 * s, 62 * s, 13 * s, (245, 200, 125))
    top = y + 42 * s - 4 * 19 * s
    d.ell(x + 4 * s, top, 54 * s, 15 * s, SYRUP)
    for dx, L in ((-52, 50), (-20, 70), (30, 60), (58, 38)):
        drip(d, x + dx * s, top + 4 * s, L * s, 11 * s, SYRUP)
    gloss(d, x - 14 * s, top - 4 * s, 20 * s, 4 * s, 130)
    butter(d, x + 2 * s, top - 14 * s, s)
    for bx in (-34, 38):
        d.ball(x + bx * s, top - 2 * s, 9 * s, (70, 80, 170))


def pizza(d, x, y, s=1.0):
    d.ell(x, y + 70 * s, 50 * s, 10 * s, (0, 0, 0, 60))
    d.poly([(x - 68 * s, y - 52 * s), (x + 68 * s, y - 52 * s), (x, y + 72 * s)], (240, 175, 60))
    d.poly([(x - 60 * s, y - 50 * s), (x + 60 * s, y - 50 * s), (x, y + 62 * s)], (255, 210, 80))
    for bx, by, r in ((-30, -30, 9), (10, -12, 7), (28, -38, 6), (-6, 22, 6)):
        d.ell(x + bx * s, y + by * s, r * s, r * s * 0.8, (255, 235, 150))
        d.ell(x + (bx + 6) * s, y + (by + 5) * s, r * s * 0.6, r * s * 0.4, (215, 140, 50))
    for px, py in ((-26, -10), (22, -30), (2, 20), (-36, -38)):
        d.ell(x + px * s, y + py * s, 15 * s, 14 * s, (150, 30, 25))
        d.ell(x + px * s - 1 * s, y + py * s - 1 * s, 13 * s, 12 * s, (205, 55, 40))
        gloss(d, x + (px - 4) * s, y + (py - 5) * s, 5 * s, 3 * s, 150)
    d.ell(x + 34 * s, y - 14 * s, 9 * s, 5 * s, (60, 140, 50))
    drip(d, x, y + 58 * s, 22 * s, 8 * s, (255, 215, 90))
    d.rect(x - 76 * s, y - 72 * s, x + 76 * s, y - 44 * s, (170, 95, 35), r=14 * s)
    d.rect(x - 74 * s, y - 74 * s, x + 74 * s, y - 50 * s, (215, 140, 60), r=12 * s)
    gloss(d, x - 30 * s, y - 66 * s, 30 * s, 4 * s, 110)


def burger(d, x, y, s=1.0):
    d.ell(x, y + 50 * s, 78 * s, 13 * s, (0, 0, 0, 60))
    d.rect(x - 64 * s, y + 18 * s, x + 64 * s, y + 46 * s, (200, 125, 45), r=12 * s)
    d.rect(x - 62 * s, y + 16 * s, x + 62 * s, y + 38 * s, (235, 165, 70), r=12 * s)
    d.rect(x - 70 * s, y - 4 * s, x + 70 * s, y + 22 * s, (90, 45, 25), r=12 * s)
    for k in range(5):
        d.line([(x - 50 * s + k * 25 * s, y), (x - 40 * s + k * 25 * s, y + 18 * s)], (60, 30, 15), 4 * s)
    d.poly([(x - 72 * s, y - 6 * s), (x + 72 * s, y - 6 * s), (x + 50 * s, y + 4 * s), (x + 30 * s, y + 26 * s),
            (x + 10 * s, y + 4 * s), (x - 40 * s, y + 4 * s), (x - 52 * s, y + 24 * s), (x - 66 * s, y + 4 * s)],
           (255, 190, 40))
    d.rect(x - 64 * s, y - 16 * s, x + 64 * s, y - 4 * s, (220, 60, 50), r=6 * s)
    for k in range(9):
        d.ell(x - 64 * s + k * 16 * s, y - 20 * s, 11 * s, 8 * s, (80, 180, 60))
    d.d.chord([(x - 68 * s) * K, (y - 86 * s) * K, (x + 68 * s) * K, (y - 2 * s) * K], 180, 360, fill=(205, 125, 45))
    d.d.chord([(x - 64 * s) * K, (y - 84 * s) * K, (x + 64 * s) * K, (y - 8 * s) * K], 180, 360, fill=(240, 170, 75))
    gloss(d, x - 22 * s, y - 64 * s, 24 * s, 8 * s, 120)
    for sx, sy in ((-34, -50), (-10, -62), (14, -56), (36, -48), (0, -44), (-24, -36), (24, -36)):
        d.ell(x + sx * s, y + sy * s, 4 * s, 2.5 * s, (255, 245, 215))


def ice_cream(d, x, y, s=1.0):
    y -= 10 * s
    d.poly([(x - 44 * s, y + 4 * s), (x + 44 * s, y + 4 * s), (x, y + 104 * s)], (205, 140, 60))
    d.poly([(x - 44 * s, y + 4 * s), (x - 4 * s, y + 4 * s), (x, y + 104 * s)], (225, 165, 80))
    for k in range(5):
        d.line([(x - 40 * s + k * 18 * s, y + 6 * s), (x + 4 * s + k * 6 * s, y + 80 * s)], (165, 100, 40), 3 * s)
        d.line([(x + 40 * s - k * 18 * s, y + 6 * s), (x - 4 * s - k * 6 * s, y + 80 * s)], (165, 100, 40), 3 * s)
    d.ball(x, y - 18 * s, 42 * s, (250, 150, 180))
    drip(d, x - 28 * s, y + 2 * s, 20 * s, 11 * s, (250, 150, 180))
    drip(d, x + 20 * s, y + 4 * s, 28 * s, 11 * s, (250, 150, 180))
    d.ball(x, y - 62 * s, 34 * s, (255, 240, 205))
    drip(d, x + 22 * s, y - 46 * s, 16 * s, 9 * s, (255, 240, 205))
    d.ell(x, y - 84 * s, 24 * s, 9 * s, (110, 50, 20, 220))
    for k, c in enumerate([(255, 80, 80), (80, 200, 255), (255, 230, 60), (120, 220, 120), (255, 255, 255)]):
        a = k * 1.3
        d.line([(x + math.cos(a) * 20 * s, y - 64 * s + math.sin(a) * 13 * s),
                (x + math.cos(a) * 20 * s + 6 * s, y - 64 * s + math.sin(a) * 13 * s + 3 * s)], c, 4 * s)
    d.ball(x + 4 * s, y - 102 * s, 12 * s, (210, 20, 40))
    d.line([(x + 4 * s, y - 112 * s), (x + 14 * s, y - 132 * s)], (90, 60, 30), 3 * s)


def donut(d, x, y, s=1.0):
    d.ell(x + 4 * s, y + 8 * s, 62 * s, 58 * s, (0, 0, 0, 60))
    d.ell(x, y, 62 * s, 58 * s, (205, 140, 70))
    d.ell(x - 2 * s, y - 3 * s, 60 * s, 55 * s, (230, 170, 95))
    pts = []
    for k in range(40):
        a = k * 2 * math.pi / 40
        r = 50 * s + 5 * s * math.sin(a * 7) + (6 * s if k % 9 == 0 else 0)
        pts.append((x + math.cos(a) * r, y - 4 * s + math.sin(a) * r * 0.94))
    d.poly(pts, (245, 110, 170))
    gloss(d, x - 22 * s, y - 30 * s, 20 * s, 8 * s, 140)
    d.ell(x, y - 2 * s, 19 * s, 17 * s, (205, 140, 70))
    d.ell(x, y, 16 * s, 14 * s, (120, 70, 30))
    cols = [(255, 240, 120), (120, 210, 255), (255, 255, 255), (120, 230, 140), (255, 140, 60)]
    rnd = random.Random(3)
    for k in range(18):
        a, rr = rnd.uniform(0, 6.28), rnd.uniform(26, 44) * s
        ang = rnd.uniform(0, 3.14)
        px, py = x + math.cos(a) * rr, y - 4 * s + math.sin(a) * rr * 0.9
        d.line([(px, py), (px + math.cos(ang) * 8 * s, py + math.sin(ang) * 8 * s)], cols[k % 5], 4 * s)


def fries(d, x, y, s=1.0):
    rnd = random.Random(2)
    for k in range(9):
        fx = x - 44 * s + k * 11 * s
        top = y - 78 * s + rnd.uniform(0, 26) * s
        d.rect(fx - 6 * s, top, fx + 6 * s, y, (225, 160, 40), r=3 * s)
        d.rect(fx - 6 * s, top, fx + 2 * s, y, (255, 210, 80), r=3 * s)
        d.rect(fx - 5 * s, top + 2 * s, fx - 1 * s, top + 30 * s, (255, 240, 170), r=2 * s)
    d.poly([(x - 56 * s, y - 34 * s), (x + 56 * s, y - 34 * s), (x + 42 * s, y + 62 * s), (x - 42 * s, y + 62 * s)],
           (200, 30, 35))
    d.poly([(x - 52 * s, y - 30 * s), (x + 50 * s, y - 30 * s), (x + 38 * s, y + 58 * s), (x - 38 * s, y + 58 * s)],
           (235, 55, 50))
    d.d.chord([(x - 56 * s) * K, (y - 60 * s) * K, (x + 56 * s) * K, (y - 10 * s) * K], 0, 180, fill=(235, 55, 50))
    d.ell(x, y + 18 * s, 18 * s, 18 * s, (255, 210, 50))
    gloss(d, x - 30 * s, y, 8 * s, 30 * s, 70)


def nuggets(d, x, y, s=1.0):
    d.ell(x, y + 48 * s, 80 * s, 13 * s, (0, 0, 0, 60))
    for nx, ny, r in ((-34, 14, 32), (30, 20, 30), (-2, -22, 33)):
        pts = []
        for k in range(24):
            a = k * 2 * math.pi / 24
            rr = r * s * (1 + 0.08 * math.sin(a * 5 + nx))
            pts.append((x + nx * s + math.cos(a) * rr * 1.15, y + ny * s + math.sin(a) * rr * 0.9))
        d.poly([(px + 3 * s, py + 4 * s) for px, py in pts], (170, 95, 30))
        d.poly(pts, (230, 160, 65))
        d.ell(x + nx * s - 6 * s, y + ny * s - 6 * s, r * s * 0.8, r * s * 0.55, (245, 190, 95))
        for k in range(5):
            d.ell(x + (nx - 14 + k * 7) * s, y + (ny - 4 + (k % 2) * 9) * s, 3 * s, 3 * s, (200, 120, 40))
    d.ell(x + 56 * s, y - 30 * s, 26 * s, 10 * s, (240, 240, 240))
    d.rect(x + 30 * s, y - 30 * s, x + 82 * s, y - 6 * s, (240, 240, 240), r=6 * s)
    d.ell(x + 56 * s, y - 30 * s, 22 * s, 7 * s, (210, 40, 30))


def hot_choc(d, x, y, s=1.0, t=0.0):
    d.ell(x, y + 56 * s, 64 * s, 12 * s, (0, 0, 0, 60))
    d.d.arc([(x + 32 * s) * K, (y - 22 * s) * K, (x + 82 * s) * K, (y + 34 * s) * K], 270, 90,
            fill=(190, 50, 50), width=int(14 * s * K))
    d.rect(x - 50 * s, y - 40 * s, x + 50 * s, y + 56 * s, (190, 50, 50), r=16 * s)
    d.rect(x - 48 * s, y - 40 * s, x + 30 * s, y + 52 * s, (225, 75, 70), r=16 * s)
    gloss(d, x - 30 * s, y + 6 * s, 7 * s, 30 * s, 90)
    d.ell(x, y - 40 * s, 50 * s, 13 * s, (95, 50, 25))
    for k, (wx, wy, wr) in enumerate(((0, -58, 36), (-6, -78, 26), (2, -94, 16))):
        d.ell(x + wx * s, y + wy * s, wr * s, wr * s * 0.6, (255, 250, 245))
        d.ell(x + (wx - 6) * s, y + (wy - 4) * s, wr * s * 0.5, wr * s * 0.25, (255, 255, 255))
    for k in range(6):
        d.ell(x + (-20 + k * 8) * s, y + (-70 + (k % 2) * 10) * s, 2.5 * s, 2.5 * s, (130, 70, 30))
    d.rect(x - 44 * s, y - 52 * s, x - 28 * s, y - 38 * s, (250, 200, 220), r=4 * s)
    d.rect(x + 26 * s, y - 50 * s, x + 42 * s, y - 36 * s, (255, 255, 255), r=4 * s)
    steam(d, x, y - 110 * s, t, s)


def lemonade(d, x, y, s=1.0):
    d.ell(x, y + 64 * s, 46 * s, 10 * s, (0, 0, 0, 60))
    d.poly([(x - 46 * s, y - 66 * s), (x + 46 * s, y - 66 * s), (x + 36 * s, y + 64 * s), (x - 36 * s, y + 64 * s)],
           (230, 245, 255, 180))
    d.poly([(x - 42 * s, y - 40 * s), (x + 42 * s, y - 40 * s), (x + 35 * s, y + 60 * s), (x - 35 * s, y + 60 * s)],
           (255, 215, 60))
    d.poly([(x - 42 * s, y - 40 * s), (x + 42 * s, y - 40 * s), (x + 38 * s, y + 4 * s), (x - 38 * s, y + 4 * s)],
           (255, 235, 120))
    for cx, cy in ((-16, -24), (14, -10), (-4, 20)):
        d.rect(x + (cx - 12) * s, y + (cy - 12) * s, x + (cx + 12) * s, y + (cy + 12) * s, (255, 255, 255, 150), r=5 * s)
        d.rect(x + (cx - 9) * s, y + (cy - 9) * s, x + (cx - 2) * s, y + (cy - 4) * s, (255, 255, 255, 220), r=2 * s)
    for k in range(6):
        d.ell(x + (-30 + k * 12) * s, y + (30 - (k % 3) * 22) * s, 3 * s, 4 * s, (255, 255, 255, 200))
    gloss(d, x - 30 * s, y - 10 * s, 5 * s, 34 * s, 120)
    d.line([(x + 16 * s, y - 56 * s), (x + 40 * s, y - 112 * s)], (235, 70, 100), 8 * s)
    d.line([(x + 18 * s, y - 62 * s), (x + 26 * s, y - 80 * s)], (255, 255, 255), 8 * s)
    d.ell(x - 44 * s, y - 64 * s, 26 * s, 26 * s, (230, 200, 30))
    d.ell(x - 44 * s, y - 64 * s, 21 * s, 21 * s, (255, 245, 160))
    for k in range(6):
        a = k * math.pi / 3
        d.line([(x - 44 * s, y - 64 * s), (x - 44 * s + math.cos(a) * 19 * s, y - 64 * s + math.sin(a) * 19 * s)],
               (240, 220, 90), 2 * s)


def cookie(d, x, y, s=1.0):
    d.ell(x + 4 * s, y + 8 * s, 64 * s, 58 * s, (0, 0, 0, 60))
    pts = []
    for k in range(30):
        a = k * 2 * math.pi / 30
        r = 62 * s * (1 + 0.05 * math.sin(a * 6))
        pts.append((x + math.cos(a) * r, y + math.sin(a) * r * 0.92))
    d.poly(pts, (185, 115, 50))
    d.ell(x - 4 * s, y - 4 * s, 56 * s, 51 * s, (220, 155, 80))
    d.ell(x - 10 * s, y - 10 * s, 40 * s, 34 * s, (235, 180, 105))
    for cx, cy in ((-12, -20), (22, -6), (-28, 10), (8, 26), (32, 24)):
        d.line([(x + cx * s, y + cy * s), (x + (cx + 8) * s, y + (cy - 4) * s)], (190, 125, 60), 2 * s)
    for cx, cy, r in ((-24, -22, 10), (20, -26, 9), (28, 12, 11), (-14, 22, 10), (2, -2, 9), (-38, 2, 7)):
        d.ell(x + cx * s, y + cy * s, r * s, r * s * 0.85, (70, 35, 15))
        d.ell(x + cx * s, y + cy * s, r * s * 0.85, r * s * 0.7, (105, 55, 25))
        gloss(d, x + (cx - 3) * s, y + (cy - 3) * s, 3 * s, 2 * s, 170)


def cupcake(d, x, y, s=1.0):
    d.ell(x, y + 66 * s, 44 * s, 9 * s, (0, 0, 0, 60))
    d.poly([(x - 46 * s, y), (x + 46 * s, y), (x + 34 * s, y + 64 * s), (x - 34 * s, y + 64 * s)], (90, 150, 220))
    for k in range(7):
        d.line([(x - 40 * s + k * 13.3 * s, y + 2 * s), (x - 30 * s + k * 10 * s, y + 62 * s)], (140, 190, 245), 5 * s)
    for k, (ry, rx, rr) in enumerate(((-6, 0, 48), (-38, 0, 38), (-66, 0, 26), (-86, 0, 13))):
        d.ell(x + rx * s, y + ry * s + 4 * s, rr * s, rr * s * 0.62, (235, 140, 185))
        d.ell(x + rx * s, y + ry * s, rr * s, rr * s * 0.58, (255, 185, 215))
        gloss(d, x - rr * 0.4 * s, y + (ry - rr * 0.2) * s, rr * 0.35 * s, rr * 0.12 * s, 150)
    cols = [(255, 240, 120), (120, 210, 255), (255, 255, 255), (120, 230, 140)]
    rnd = random.Random(5)
    for k in range(12):
        px, py = x + rnd.uniform(-38, 38) * s, y + rnd.uniform(-80, -4) * s
        d.line([(px, py), (px + 6 * s, py + 2 * s)], cols[k % 4], 4 * s)
    d.ball(x + 2 * s, y - 104 * s, 13 * s, (210, 20, 40))
    d.line([(x + 2 * s, y - 115 * s), (x + 10 * s, y - 134 * s)], (90, 60, 30), 3 * s)


def taco(d, x, y, s=1.0):
    d.ell(x, y + 62 * s, 76 * s, 12 * s, (0, 0, 0, 60))
    # back rim of the shell, just peeking above the fillings
    d.d.arc([(x - 70 * s) * K, (y - 40 * s) * K, (x + 70 * s) * K, (y + 40 * s) * K], 200, 340,
            fill=(225, 165, 65), width=int(10 * s * K))
    # fillings poking out of the top
    for k in range(7):
        d.ell(x - 52 * s + k * 17 * s, y - 14 * s - (k % 2) * 8 * s, 15 * s, 11 * s, (70, 175, 60))
    for k in range(6):
        d.ell(x - 44 * s + k * 17 * s, y - 2 * s, 12 * s, 9 * s, (120, 60, 30))
    for k in range(4):
        d.ell(x - 34 * s + k * 22 * s, y - 12 * s, 9 * s, 7 * s, (225, 50, 40))
        gloss(d, x - 36 * s + k * 22 * s, y - 15 * s, 3 * s, 2 * s, 170)
    for k in range(8):
        d.line([(x - 46 * s + k * 13 * s, y - 20 * s), (x - 40 * s + k * 13 * s, y - 8 * s)], (255, 200, 50), 4 * s)
    # front of the shell (bottom half), crispy and golden
    d.d.chord([(x - 74 * s) * K, (y - 62 * s) * K, (x + 74 * s) * K, (y + 66 * s) * K], 0, 180, fill=(220, 160, 60))
    d.d.chord([(x - 68 * s) * K, (y - 56 * s) * K, (x + 68 * s) * K, (y + 58 * s) * K], 0, 180, fill=(250, 200, 95))
    rnd = random.Random(4)
    for k in range(14):
        a = rnd.uniform(0.4, 2.7)
        d.ell(x + math.cos(a) * 50 * s, y + math.sin(a) * 44 * s, 3 * s, 3 * s, (215, 150, 60))
    gloss(d, x - 30 * s, y + 20 * s, 18 * s, 5 * s, 110)


def sushi(d, x, y, s=1.0):
    d.ell(x, y + 40 * s, 84 * s, 12 * s, (0, 0, 0, 60))
    # nigiri
    nx = x - 34 * s
    d.ell(nx, y + 18 * s, 40 * s, 18 * s, (235, 235, 228))
    d.ell(nx, y + 12 * s, 38 * s, 16 * s, (252, 252, 248))
    d.ell(nx, y - 4 * s, 44 * s, 17 * s, (240, 110, 70))
    for k in range(4):
        d.line([(nx - 30 * s + k * 16 * s, y - 16 * s), (nx - 22 * s + k * 16 * s, y + 8 * s)], (255, 190, 160), 4 * s)
    gloss(d, nx - 14 * s, y - 12 * s, 14 * s, 4 * s, 160)
    # maki
    mx = x + 40 * s
    d.ell(mx, y + 26 * s, 32 * s, 13 * s, (30, 45, 35))
    d.rect(mx - 32 * s, y - 6 * s, mx + 32 * s, y + 26 * s, (30, 45, 35))
    d.ell(mx, y - 6 * s, 32 * s, 13 * s, (250, 250, 245))
    d.ell(mx, y - 6 * s, 14 * s, 6 * s, (240, 110, 70))
    d.ell(mx + 8 * s, y - 4 * s, 6 * s, 3 * s, (110, 190, 80))
    d.ell(x + 2 * s, y + 34 * s, 14 * s, 6 * s, (130, 190, 80))


def coins(d, x, y, s=1.0):
    for k, (ox, oy) in enumerate(((-30, 26), (30, 26), (0, -8), (-14, -40), (18, -38))):
        cx, cy = x + ox * s, y + oy * s
        d.ell(cx, cy + 5 * s, 34 * s, 31 * s, (190, 135, 30))
        d.ell(cx, cy, 33 * s, 30 * s, (250, 205, 70))
        d.ell(cx, cy, 25 * s, 22 * s, (240, 185, 50))
        d.text(cx, cy, "$", 30 * s, (200, 145, 35))
        gloss(d, cx - 12 * s, cy - 14 * s, 9 * s, 4 * s, 170)


def any_food(d, x, y, s=1.0, t=0.0):
    d.ell(x, y + 40 * s, 80 * s, 20 * s, (235, 235, 240))
    foods = [pizza, burger, donut, ice_cream, taco, cookie, pancakes, cupcake]
    fn = foods[int(t * 4) % len(foods)]
    fn(d, x, y - 5 * s, s * 0.7)
    for k in range(4):
        a = t * 3 + k * 1.57
        d.text(x + math.cos(a) * 75 * s, y - 10 * s + math.sin(a) * 55 * s, "✦", 22 * s, (255, 240, 140))


ROUNDS = {
    "beat_2_a": ("WAFFLES", "+ SYRUP", waffle, "PANCAKES", "", pancakes, ((255, 205, 120), (240, 150, 80))),
    "beat_3_a": ("PIZZA", "", pizza, "BURGERS", "", burger, ((250, 120, 100), (200, 70, 70))),
    "beat_4_a": ("ICE CREAM", "", ice_cream, "DONUTS", "", donut, ((255, 190, 220), (190, 140, 230))),
    "beat_5_a": ("FRIES", "", fries, "NUGGETS", "", nuggets, ((255, 220, 100), (240, 160, 60))),
    "beat_6_a": ("HOT", "CHOCOLATE", hot_choc, "LEMONADE", "", lemonade, ((150, 220, 255), (90, 160, 230))),
    "beat_7_a": ("COOKIES", "", cookie, "CUPCAKES", "", cupcake, ((250, 200, 220), (220, 150, 190))),
    "beat_8_a": ("TACOS", "", taco, "SUSHI", "", sushi, ((140, 220, 170), (70, 160, 130))),
    "beat_9_a": ("GOLD", "COINS", coins, "ANY FOOD", "FOREVER", any_food, ((90, 70, 150), (40, 30, 90))),
}
MACHINE = {"A": (230, 70, 70), "B": (60, 120, 230)}


def food(d, fn, x, y, s, t):
    if fn in (hot_choc, any_food):
        fn(d, x, y, s, t=t)
    else:
        fn(d, x, y, s)


def dispenser(d, cx, cy, letter, l1, l2, fn, t, out_p):
    col = MACHINE[letter]
    w, h = 140, 300
    d.shadow(cx, cy + h + 10, 150, 22)
    d.rect(cx - w, cy - h, cx + w, cy + h, shade(col, 0.75), r=40)
    d.rect(cx - w + 10, cy - h + 6, cx + w - 10, cy + h - 10, col, r=36)
    d.rect(cx - w + 22, cy - h + 18, cx - w + 50, cy + h - 40, (255, 255, 255, 50), r=14)
    # sign
    d.rect(cx - w + 18, cy - h + 22, cx + w - 18, cy - h + 128, (255, 255, 255), r=20)
    fs = 34 if max(len(l1), len(l2)) <= 8 else 28
    if l2:
        d.text(cx, cy - h + 56, l1, fs, (40, 40, 50))
        d.text(cx, cy - h + 96, l2, fs - 6, (40, 40, 50))
    else:
        d.text(cx, cy - h + 75, l1, fs, (40, 40, 50))
    # window with stock
    d.rect(cx - w + 26, cy - h + 148, cx + w - 26, cy + 70, (200, 235, 250), r=20)
    d.ell(cx, cy - 40, 95, 95, (255, 255, 255, 90))  # soft glow behind the hero item
    food(d, fn, cx, cy - 30 + 6 * math.sin(t * 2.5), 0.95, t)
    d.rect(cx - w + 34, cy - h + 156, cx - w + 60, cy + 60, (255, 255, 255, 90), r=10)
    # button + chute
    pulse = 1 + 0.08 * math.sin(t * 8) if out_p <= 0 else 0.9
    d.ell(cx + 80, cy + 140, 34 * pulse, 34 * pulse, shade(col, 0.5))
    d.ell(cx + 80, cy + 134, 30 * pulse, 30 * pulse, (255, 230, 70))
    d.rect(cx - 95, cy + 180, cx + 35, cy + 270, (30, 30, 40), r=16)
    # letter badge
    d.ell(cx - 70, cy + 135, 36, 36, (255, 255, 255))
    d.text(cx - 70, cy + 135, letter, 46, col)
    # dispensed food pops out onto a plate in front
    if out_p > 0:
        q = ease(out_p / 0.35)
        d.ell(cx - 30, cy + h + 55, 95, 24, (245, 245, 250))
        d.ell(cx - 30, cy + h + 50, 75, 16, (230, 230, 238))
        bounce = abs(math.sin(out_p * 9)) * 40 * (1 - clamp(out_p))
        fy = cy + 230 + (h - 230 + 5) * q - bounce
        food(d, fn, cx - 30, fy, 0.95 + 0.15 * q, t)
        for k in range(6):
            a = k * 1.05 + t
            r_ = 60 + 60 * q
            d.text(cx - 30 + math.cos(a) * r_, fy + math.sin(a) * r_ * 0.6, "✦", 24, (255, 245, 150, int(255 * (1 - q * 0.5))))


def countdown_badge(d, x, y, n, frac):
    d.ell(x, y, 78, 78, (0, 0, 0, 150))
    d.d.arc([(x - 72) * K, (y - 72) * K, (x + 72) * K, (y + 72) * K], -90, -90 + 360 * (1 - frac),
            fill=(255, 230, 40), width=int(12 * K))
    d.text(x, y, str(n), 92 * (1 + 0.25 * (1 - ease(frac * 4))), (255, 255, 255), stroke=4)


def or_badge(d, x, y, t):
    sc = 1 + 0.06 * math.sin(t * 6)
    d.ell(x, y, 58 * sc, 58 * sc, (255, 230, 40))
    d.ell(x, y, 50 * sc, 50 * sc, (255, 200, 30))
    d.text(x, y, "OR", 44 * sc, (40, 30, 30))


def round_shot(sid):
    l1a, l2a, fa, l1b, l2b, fb, bg = ROUNDS[sid]

    def shot(d, t, T):
        c0 = T - COUNT
        slide = 1 - ease(t / 0.45)
        out_p = (t - (c0 + 3 * STEP)) if t > c0 + 3 * STEP else 0
        dispenser(d, LX - slide * 420, CY, "A", l1a, l2a, fa, t, out_p)
        dispenser(d, RX + slide * 420, CY, "B", l1b, l2b, fb, t + 0.5, out_p)
        if c0 <= t < c0 + 3 * STEP:
            k = int((t - c0) / STEP)
            countdown_badge(d, 360, 250, 3 - k, ((t - c0) % STEP) / STEP)
        elif t < c0:
            or_badge(d, 360, 250, t)
        else:
            label(d, "WHICH ONE?", 250, 50, fill=(255, 235, 80), p=out_p * 3)
        return bg
    return shot


def title(d, t, T):
    p = t / T
    for k, (x, col) in enumerate(((190, MACHINE["A"]), (530, MACHINE["B"]))):
        bob = 10 * math.sin(t * 3 + k)
        d.rect(x - 120, 560 + bob, x + 120, 1020 + bob, shade(col, 0.8), r=36)
        d.rect(x - 110, 566 + bob, x + 110, 1010 + bob, col, r=32)
        d.rect(x - 90, 600 + bob, x + 90, 820 + bob, (200, 235, 250), r=18)
        d.text(x, 710 + bob, "?", 120, shade(col, 0.8))
        d.ell(x + 60, 900 + bob, 28, 28, (255, 230, 70))
    sc = 0.7 + 0.3 * ease(p * 3)
    d.text(360, 260, "WHICH", 84 * sc, (255, 255, 255), stroke=6)
    d.text(360, 350, "DISPENSER", 84 * sc, (255, 235, 80), stroke=6)
    d.text(360, 440, "WOULD YOU CHOOSE?", 52 * sc, (255, 255, 255), stroke=5)
    return (80, 60, 160), (180, 90, 160)


def comment(d, t, T):
    p = t / T
    for k, (x, letter) in enumerate(((220, "A"), (500, "B"))):
        bob = 18 * math.sin(t * 5 + k * 1.6)
        d.ell(x, 640 + bob, 110, 110, MACHINE[letter])
        d.text(x, 640 + bob, letter, 120, (255, 255, 255), stroke=4)
    d.text(360, 330, "COMMENT", 80, (255, 255, 255), stroke=6)
    d.text(360, 420, "YOUR PICKS!", 70, (255, 235, 80), stroke=6)
    d.text(360, 880, "e.g. A B A A B B A B", 36, (255, 255, 255), stroke=3)
    return (80, 60, 160), (180, 90, 160)


def outro(d, t, T):
    d.text(360, 560, "FOLLOW", 96, (255, 255, 255), stroke=6)
    d.text(360, 670, "FOR MORE", 80, (255, 235, 80), stroke=6)
    d.text(360, 780, "CHOICES!", 80, (255, 235, 80), stroke=6)
    return (80, 60, 160), (180, 90, 160)


SHOTS = {"beat_1_a": title, "beat_10_a": comment, "outro": outro}
SHOTS.update({sid: round_shot(sid) for sid in ROUNDS})
