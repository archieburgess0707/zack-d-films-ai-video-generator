"""Procedural scenes for dispenser_choice_2 (Part 2) — reuses the Part 1 machines and foods."""
import importlib.util
import os

from free_render import *  # noqa: F401,F403

_spec = importlib.util.spec_from_file_location(
    "dispenser_1", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dispenser_choice", "shots.py"))
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
gloss, drip = M.gloss, M.drip


# --------------------------------------------------------------------------- new foods
def popcorn(d, x, y, s=1.0):
    rnd = random.Random(7)
    for _ in range(26):
        px, py = x + rnd.uniform(-48, 48) * s, y - 40 * s + rnd.uniform(-38, 14) * s
        r = rnd.uniform(11, 16) * s
        d.ell(px, py, r, r * 0.9, (250, 240, 210))
        d.ell(px - r * 0.3, py - r * 0.3, r * 0.6, r * 0.5, (255, 252, 240))
        if rnd.random() < 0.35:
            d.ell(px + r * 0.3, py + r * 0.2, r * 0.35, r * 0.3, (245, 205, 90))
    d.poly([(x - 56 * s, y - 20 * s), (x + 56 * s, y - 20 * s), (x + 42 * s, y + 70 * s), (x - 42 * s, y + 70 * s)],
           (255, 255, 255))
    for k in range(4):
        x0 = x - 48 * s + k * 28 * s
        d.poly([(x0, y - 20 * s), (x0 + 14 * s, y - 20 * s), (x0 + 11 * s, y + 70 * s), (x0 - 1 * s, y + 70 * s)],
               (225, 45, 50))
    gloss(d, x - 30 * s, y + 10 * s, 6 * s, 30 * s, 80)


def hot_dog(d, x, y, s=1.0):
    d.ell(x, y + 40 * s, 84 * s, 13 * s, (0, 0, 0, 60))
    d.rect(x - 80 * s, y - 6 * s, x + 80 * s, y + 38 * s, (215, 150, 70), r=22 * s)
    d.rect(x - 92 * s, y - 24 * s, x + 92 * s, y + 8 * s, (175, 60, 40), r=16 * s)
    d.rect(x - 90 * s, y - 26 * s, x + 88 * s, y + 0 * s, (210, 85, 55), r=13 * s)
    gloss(d, x - 30 * s, y - 18 * s, 40 * s, 4 * s, 140)
    pts = [(x - 70 * s + k * 10 * s, y - 14 * s + 6 * s * math.sin(k * 1.3)) for k in range(15)]
    d.line(pts, (255, 210, 40), 7 * s)
    d.rect(x - 78 * s, y + 2 * s, x + 78 * s, y + 40 * s, (235, 175, 90), r=20 * s)
    gloss(d, x - 40 * s, y + 14 * s, 30 * s, 5 * s, 100)


def milkshake(d, x, y, s=1.0):
    d.ell(x, y + 72 * s, 40 * s, 9 * s, (0, 0, 0, 60))
    d.poly([(x - 42 * s, y - 40 * s), (x + 42 * s, y - 40 * s), (x + 26 * s, y + 70 * s), (x - 26 * s, y + 70 * s)],
           (140, 80, 45))
    d.poly([(x - 42 * s, y - 40 * s), (x - 10 * s, y - 40 * s), (x - 14 * s, y + 70 * s), (x - 26 * s, y + 70 * s)],
           (165, 100, 60))
    for dx, L in ((-30, 30), (6, 46), (28, 22)):
        drip(d, x + dx * s, y - 40 * s, L * s, 10 * s, (90, 45, 20))
    for k, (wy, wr) in enumerate(((-52, 46), (-76, 34), (-96, 20))):
        d.ell(x, y + wy * s, wr * s, wr * s * 0.55, (255, 252, 246))
        d.ell(x - wr * 0.3 * s, y + (wy - 4) * s, wr * 0.45 * s, wr * 0.2 * s, (255, 255, 255))
    d.ell(x, y - 98 * s, 24 * s, 7 * s, (90, 45, 20, 220))
    d.line([(x + 14 * s, y - 70 * s), (x + 36 * s, y - 140 * s)], (235, 70, 100), 9 * s)
    d.ball(x - 2 * s, y - 116 * s, 12 * s, (210, 20, 40))


def cake(d, x, y, s=1.0):
    d.ell(x, y + 60 * s, 80 * s, 13 * s, (0, 0, 0, 60))
    front = [(x - 70 * s, y - 20 * s), (x + 50 * s, y - 40 * s), (x + 50 * s, y + 55 * s), (x - 70 * s, y + 60 * s)]
    d.poly(front, (110, 60, 35))
    for k in range(2):
        yy = y + (0 + k * 28) * s
        d.poly([(x - 70 * s, yy), (x + 50 * s, yy - 18 * s), (x + 50 * s, yy - 10 * s), (x - 70 * s, yy + 8 * s)],
               (250, 220, 200))
    d.poly([(x + 50 * s, y - 40 * s), (x + 80 * s, y - 20 * s), (x + 80 * s, y + 52 * s), (x + 50 * s, y + 55 * s)],
           (85, 45, 25))
    d.poly([(x - 76 * s, y - 24 * s), (x + 44 * s, y - 52 * s), (x + 86 * s, y - 26 * s), (x - 30 * s, y - 2 * s)],
           (95, 50, 28))
    for dx, L in ((-56, 22), (-20, 32), (20, 18)):
        drip(d, x + dx * s, y - 20 * s + dx * 0.15 * s, L * s, 10 * s, (95, 50, 28))
    gloss(d, x, y - 30 * s, 36 * s, 6 * s, 110)
    d.ball(x + 10 * s, y - 52 * s, 13 * s, (210, 20, 40))
    d.line([(x + 10 * s, y - 62 * s), (x + 20 * s, y - 82 * s)], (90, 60, 30), 3 * s)


def watermelon(d, x, y, s=1.0):
    d.ell(x, y + 50 * s, 80 * s, 12 * s, (0, 0, 0, 60))
    d.d.chord([(x - 80 * s) * K, (y - 70 * s) * K, (x + 80 * s) * K, (y + 90 * s) * K], 0, 180, fill=(60, 140, 60))
    d.d.chord([(x - 72 * s) * K, (y - 62 * s) * K, (x + 72 * s) * K, (y + 76 * s) * K], 0, 180, fill=(235, 250, 200))
    d.d.chord([(x - 64 * s) * K, (y - 56 * s) * K, (x + 64 * s) * K, (y + 66 * s) * K], 0, 180, fill=(240, 70, 80))
    for k in range(7):
        a = 0.35 + k * 0.4
        d.ell(x + math.cos(a) * 38 * s, y + 5 * s + math.sin(a) * 34 * s, 4 * s, 6 * s, (40, 30, 30))
    gloss(d, x - 20 * s, y + 18 * s, 22 * s, 6 * s, 90)


def cash(d, x, y, s=1.0):
    for k in range(5):
        yy = y + 40 * s - k * 16 * s
        d.rect(x - 74 * s, yy - 22 * s, x + 74 * s, yy + 22 * s, (60, 140, 70), r=6 * s)
        d.rect(x - 70 * s, yy - 26 * s, x + 70 * s, yy + 16 * s, (130, 200, 120), r=6 * s)
        d.ell(x, yy - 5 * s, 16 * s, 14 * s, (90, 160, 90))
        d.text(x, yy - 5 * s, "$", 22 * s, (230, 255, 230))
    d.rect(x - 14 * s, y - 50 * s, x + 14 * s, y + 70 * s, (240, 220, 120), r=4 * s)
    d.text(x, y - 110 * s, "$1,000", 34 * s, (40, 120, 50), stroke=3, sfill=(255, 255, 255))


def free_pizza(d, x, y, s=1.0, t=0.0):
    M.pizza(d, x, y, s * 0.9)
    d.rect(x - 64 * s, y + 66 * s, x + 64 * s, y + 98 * s, (255, 255, 255), r=12 * s)
    d.text(x, y + 82 * s, "FOREVER", 22 * s, (220, 50, 50))


M.ROUNDS = {
    "beat_2_a": ("POPCORN", "", popcorn, "FRIES", "", M.fries, ((255, 220, 120), (240, 170, 70))),
    "beat_3_a": ("HOT DOGS", "", hot_dog, "BURGERS", "", M.burger, ((250, 140, 110), (210, 80, 70))),
    "beat_4_a": ("CHOCOLATE", "MILKSHAKE", milkshake, "HOT", "CHOCOLATE", M.hot_choc, ((200, 160, 230), (140, 100, 200))),
    "beat_5_a": ("CHOCOLATE", "CAKE", cake, "CUPCAKES", "", M.cupcake, ((250, 200, 220), (220, 150, 190))),
    "beat_6_a": ("WATERMELON", "", watermelon, "ICE CREAM", "", M.ice_cream, ((150, 225, 170), (80, 170, 120))),
    "beat_7_a": ("PANCAKES", "", M.pancakes, "DONUTS", "", M.donut, ((255, 205, 130), (240, 150, 90))),
    "beat_8_a": ("SUSHI", "", M.sushi, "PIZZA", "", M.pizza, ((140, 210, 240), (70, 140, 200))),
    "beat_9_a": ("$1,000", "RIGHT NOW", cash, "FREE PIZZA", "FOR LIFE", free_pizza, ((90, 70, 150), (40, 30, 90))),
}

BG = ((40, 120, 140), (90, 60, 160))


def title(d, t, T):
    p = t / T
    for k, (x, col) in enumerate(((190, M.MACHINE["A"]), (530, M.MACHINE["B"]))):
        bob = 10 * math.sin(t * 3 + k)
        d.rect(x - 120, 600 + bob, x + 120, 1040 + bob, shade(col, 0.8), r=36)
        d.rect(x - 110, 606 + bob, x + 110, 1030 + bob, col, r=32)
        d.rect(x - 90, 640 + bob, x + 90, 860 + bob, (200, 235, 250), r=18)
        d.text(x, 750 + bob, "?", 120, shade(col, 0.8))
        d.ell(x + 60, 940 + bob, 28, 28, (255, 230, 70))
    sc = 0.7 + 0.3 * ease(p * 3)
    d.text(360, 230, "WHICH", 80 * sc, (255, 255, 255), stroke=6)
    d.text(360, 320, "DISPENSER?", 80 * sc, (255, 235, 80), stroke=6)
    pulse = 1 + 0.08 * math.sin(t * 7)
    d.rect(250, 400, 470, 480, (235, 40, 60), r=40)
    d.text(360, 440, "PART 2", 50 * pulse, (255, 255, 255))
    d.text(360, 545, "EVEN HARDER!", 40 * sc, (255, 255, 255), stroke=4)
    return BG


def comment(d, t, T):
    for k, (x, letter) in enumerate(((220, "A"), (500, "B"))):
        bob = 18 * math.sin(t * 5 + k * 1.6)
        d.ell(x, 640 + bob, 110, 110, M.MACHINE[letter])
        d.text(x, 640 + bob, letter, 120, (255, 255, 255), stroke=4)
    d.text(360, 330, "COMMENT", 80, (255, 255, 255), stroke=6)
    d.text(360, 420, "YOUR PICKS!", 70, (255, 235, 80), stroke=6)
    d.text(360, 880, "WHAT SHOULD", 46, (255, 255, 255), stroke=4)
    d.text(360, 940, "PART 3 BE?", 46, (255, 235, 80), stroke=4)
    return BG


def outro(d, t, T):
    d.text(360, 560, "FOLLOW", 96, (255, 255, 255), stroke=6)
    d.text(360, 670, "FOR PART 3", 80, (255, 235, 80), stroke=6)
    return BG


SHOTS = {"beat_1_a": title, "beat_10_a": comment, "outro": outro}
SHOTS.update({sid: M.round_shot(sid) for sid in M.ROUNDS})
