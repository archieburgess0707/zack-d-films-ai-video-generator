"""Procedural scenes for the dispenser_choice short (rendered by scripts/free_render.py)."""
from free_render import *  # noqa: F401,F403
import free_render

STEP = free_render.COUNT_STEP
COUNT = 3.6          # must match beats.json "countdown"
LX, RX, CY = 190, 530, 620


# --------------------------------------------------------------------------- foods (centred on x, y; ~100px at s=1)
def waffle(d, x, y, s=1.0):
    d.rect(x - 55 * s, y - 55 * s, x + 55 * s, y + 55 * s, (215, 150, 60), r=14 * s)
    for k in range(4):
        o = -40 * s + k * 27 * s
        d.line([(x + o, y - 50 * s), (x + o, y + 50 * s)], (170, 110, 40), 6 * s)
        d.line([(x - 50 * s, y + o), (x + 50 * s, y + o)], (170, 110, 40), 6 * s)
    d.ell(x + 10 * s, y - 10 * s, 34 * s, 22 * s, (130, 60, 20, 210))
    d.ell(x + 20 * s, y + 18 * s, 10 * s, 16 * s, (130, 60, 20, 210))
    d.rect(x - 14 * s, y - 30 * s, x + 14 * s, y - 10 * s, (255, 240, 150), r=4 * s)


def pancakes(d, x, y, s=1.0):
    for k in range(4):
        yy = y + 40 * s - k * 22 * s
        d.ell(x, yy + 6 * s, 62 * s, 20 * s, (180, 115, 50))
        d.ell(x, yy, 62 * s, 20 * s, (235, 180, 100))
    d.ell(x, y - 26 * s, 50 * s, 14 * s, (140, 70, 25, 220))
    d.rect(x - 14 * s, y - 44 * s, x + 14 * s, y - 26 * s, (255, 240, 150), r=4 * s)


def pizza(d, x, y, s=1.0):
    d.poly([(x - 60 * s, y - 50 * s), (x + 60 * s, y - 50 * s), (x, y + 65 * s)], (250, 200, 80))
    d.rect(x - 64 * s, y - 64 * s, x + 64 * s, y - 42 * s, (200, 130, 60), r=10 * s)
    for px, py in ((-25, -25), (20, -20), (0, 15)):
        d.ell(x + px * s, y + py * s, 12 * s, 12 * s, (200, 50, 40))


def burger(d, x, y, s=1.0):
    d.d.chord([(x - 60 * s) * K, (y - 60 * s) * K, (x + 60 * s) * K, (y + 10 * s) * K], 180, 360, fill=(230, 160, 70))
    d.rect(x - 64 * s, y - 28 * s, x + 64 * s, y - 14 * s, (90, 190, 80), r=7 * s)
    d.rect(x - 62 * s, y - 16 * s, x + 62 * s, y + 2 * s, (250, 200, 60), r=4 * s)
    d.rect(x - 60 * s, y, x + 60 * s, y + 20 * s, (120, 70, 40), r=9 * s)
    d.rect(x - 58 * s, y + 18 * s, x + 58 * s, y + 38 * s, (230, 160, 70), r=9 * s)
    for k in range(4):
        d.ell(x - 30 * s + k * 20 * s, y - 45 * s, 3 * s, 2 * s, (255, 245, 220))


def ice_cream(d, x, y, s=1.0):
    d.poly([(x - 34 * s, y - 10 * s), (x + 34 * s, y - 10 * s), (x, y + 70 * s)], (220, 160, 80))
    d.line([(x - 20 * s, y), (x + 8 * s, y + 40 * s)], (180, 120, 50), 4 * s)
    d.line([(x + 20 * s, y), (x - 8 * s, y + 40 * s)], (180, 120, 50), 4 * s)
    d.ball(x, y - 30 * s, 40 * s, (250, 170, 200))
    d.ball(x, y - 70 * s, 30 * s, (255, 245, 225))
    d.ell(x, y - 106 * s, 9 * s, 9 * s, (220, 40, 50))


def donut(d, x, y, s=1.0):
    d.ell(x, y, 55 * s, 55 * s, (220, 170, 100))
    d.ell(x, y, 46 * s, 46 * s, (240, 120, 180))
    d.ell(x, y, 17 * s, 17 * s, (220, 170, 100))
    d.ell(x, y, 12 * s, 12 * s, (255, 255, 255, 0))
    cols = [(255, 240, 120), (120, 210, 255), (255, 255, 255), (120, 230, 140)]
    for k in range(8):
        a = k * 0.8
        d.line([(x + math.cos(a) * 28 * s, y + math.sin(a) * 28 * s),
                (x + math.cos(a + 0.25) * 34 * s, y + math.sin(a + 0.25) * 34 * s)], cols[k % 4], 5 * s)


def fries(d, x, y, s=1.0):
    for k in range(6):
        fx = x - 35 * s + k * 14 * s
        d.rect(fx - 6 * s, y - 70 * s + (k % 2) * 12 * s, fx + 6 * s, y, (250, 210, 80), r=3 * s)
    d.poly([(x - 50 * s, y - 30 * s), (x + 50 * s, y - 30 * s), (x + 38 * s, y + 55 * s), (x - 38 * s, y + 55 * s)],
           (225, 50, 45))
    d.ell(x, y + 10 * s, 14 * s, 14 * s, (255, 220, 60))


def nuggets(d, x, y, s=1.0):
    for nx, ny, r in ((-30, 10, 30), (25, 15, 28), (0, -25, 30)):
        d.ell(x + nx * s, y + ny * s, r * s * 1.15, r * s, (200, 130, 50))
        d.ell(x + nx * s - 4 * s, y + ny * s - 4 * s, r * s, r * s * 0.85, (235, 170, 80))
        for k in range(3):
            d.ell(x + (nx - 10 + k * 10) * s, y + (ny - 6 + (k % 2) * 8) * s, 3 * s, 3 * s, (190, 120, 45))


def hot_choc(d, x, y, s=1.0, t=0.0):
    d.rect(x - 45 * s, y - 40 * s, x + 45 * s, y + 50 * s, (230, 80, 80), r=14 * s)
    d.d.arc([(x + 30 * s) * K, (y - 20 * s) * K, (x + 75 * s) * K, (y + 30 * s) * K], 270, 90,
            fill=(230, 80, 80), width=int(12 * s * K))
    d.ell(x, y - 40 * s, 45 * s, 12 * s, (110, 60, 30))
    for k in range(3):
        d.ell(x - 18 * s + k * 18 * s, y - 46 * s, 9 * s, 7 * s, (255, 255, 255))
    for k in range(2):
        wob = 6 * s * math.sin(t * 4 + k)
        d.line([(x - 15 * s + k * 30 * s, y - 60 * s), (x - 15 * s + k * 30 * s + wob, y - 85 * s),
                (x - 15 * s + k * 30 * s - wob, y - 105 * s)], (255, 255, 255, 140), 6 * s)


def lemonade(d, x, y, s=1.0):
    d.poly([(x - 42 * s, y - 60 * s), (x + 42 * s, y - 60 * s), (x + 34 * s, y + 55 * s), (x - 34 * s, y + 55 * s)],
           (255, 245, 170, 230))
    d.poly([(x - 38 * s, y - 35 * s), (x + 38 * s, y - 35 * s), (x + 34 * s, y + 55 * s), (x - 34 * s, y + 55 * s)],
           (255, 225, 80))
    d.rect(x - 22 * s, y - 20 * s, x - 6 * s, y - 4 * s, (255, 255, 255, 180), r=3 * s)
    d.rect(x + 4 * s, y + 6 * s, x + 20 * s, y + 22 * s, (255, 255, 255, 180), r=3 * s)
    d.line([(x + 15 * s, y - 50 * s), (x + 35 * s, y - 95 * s)], (230, 60, 90), 7 * s)
    d.ell(x - 40 * s, y - 60 * s, 20 * s, 20 * s, (250, 220, 50))
    d.ell(x - 40 * s, y - 60 * s, 14 * s, 14 * s, (255, 245, 150))


def cookie(d, x, y, s=1.0):
    d.ell(x, y, 55 * s, 52 * s, (200, 140, 70))
    d.ell(x - 4 * s, y - 4 * s, 50 * s, 46 * s, (225, 170, 95))
    for cx, cy in ((-20, -15), (15, -22), (22, 12), (-10, 20), (2, -2)):
        d.ell(x + cx * s, y + cy * s, 7 * s, 6 * s, (90, 50, 25))


def cupcake(d, x, y, s=1.0):
    d.poly([(x - 42 * s, y), (x + 42 * s, y), (x + 32 * s, y + 55 * s), (x - 32 * s, y + 55 * s)], (120, 180, 240))
    for k in range(5):
        d.line([(x - 30 * s + k * 15 * s, y + 3 * s), (x - 24 * s + k * 12 * s, y + 52 * s)], (90, 150, 210), 4 * s)
    d.ball(x, y - 10 * s, 44 * s, (255, 190, 220))
    d.ball(x, y - 45 * s, 28 * s, (255, 205, 230))
    d.ell(x, y - 78 * s, 10 * s, 10 * s, (220, 40, 50))


def taco(d, x, y, s=1.0):
    d.d.chord([(x - 65 * s) * K, (y - 50 * s) * K, (x + 65 * s) * K, (y + 80 * s) * K], 180, 360, fill=(240, 190, 80))
    for k in range(6):
        d.ell(x - 45 * s + k * 18 * s, y - 40 * s - (k % 2) * 6 * s, 14 * s, 10 * s, (90, 190, 80))
    for k in range(4):
        d.ell(x - 30 * s + k * 20 * s, y - 28 * s, 9 * s, 7 * s, (220, 60, 50))
    d.d.chord([(x - 60 * s) * K, (y - 40 * s) * K, (x + 60 * s) * K, (y + 70 * s) * K], 180, 360, fill=(250, 205, 100))
    d.d.chord([(x - 60 * s) * K, (y - 40 * s) * K, (x + 60 * s) * K, (y + 70 * s) * K], 180, 360,
              fill=None, outline=(210, 160, 60), width=int(4 * s * K))


def sushi(d, x, y, s=1.0):
    for k, ox in enumerate((-36, 36)):
        cx = x + ox * s
        d.ell(cx, y + 18 * s, 34 * s, 14 * s, (40, 60, 45))
        d.rect(cx - 34 * s, y - 20 * s, cx + 34 * s, y + 18 * s, (40, 60, 45))
        d.ell(cx, y - 20 * s, 34 * s, 14 * s, (250, 250, 245))
        d.ell(cx, y - 20 * s, 15 * s, 7 * s, (250, 130, 90))


def coins(d, x, y, s=1.0):
    for k, (ox, oy) in enumerate(((-28, 20), (28, 20), (0, -18))):
        cx, cy = x + ox * s, y + oy * s
        d.ell(cx, cy + 4 * s, 34 * s, 32 * s, (200, 150, 40))
        d.ell(cx, cy, 32 * s, 30 * s, (250, 205, 70))
        d.text(cx, cy, "$", 34 * s, (200, 150, 40))


def any_food(d, x, y, s=1.0, t=0.0):
    d.ell(x, y + 30 * s, 70 * s, 20 * s, (235, 235, 240))
    foods = [pizza, burger, donut, ice_cream, taco, cookie]
    fn = foods[int(t * 4) % len(foods)]
    fn(d, x, y - 5 * s, s * 0.6)
    for k in range(4):
        a = t * 3 + k * 1.57
        d.text(x + math.cos(a) * 70 * s, y - 10 * s + math.sin(a) * 50 * s, "✦", 22 * s, (255, 240, 140))


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
    for k, (ox, oy) in enumerate(((-50, -70), (50, -60), (0, 10))):
        food(d, fn, cx + ox, cy + oy, 0.5, t + k)
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
        food(d, fn, cx - 30, fy, 0.85 + 0.15 * q, t)
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
