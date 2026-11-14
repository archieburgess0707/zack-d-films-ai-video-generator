"""
Shared compositor for the "Dave Finds Out" parts: puts Blender frames (frames/<shot>/f_####.png, 15 fps)
on screen and draws the 2D layer — phone notifications, speaker name tags, comedy labels, end cards.
Each part's shots.py calls make_shots(part_dir, part_number).
"""
import json
import os

from free_render import *  # noqa: F401,F403

RFPS = 15
SPEAKER_COL = {"Dave": (40, 110, 230), "Chloe": (235, 80, 150), "Brad": (215, 45, 45)}
YEL, WHITE = (255, 235, 80), (255, 255, 255)

# shot -> list of (text, y, appear-at fraction, size, colour)
LABELS = {
    "p1_b1_a": [("THIS IS DAVE", 300, 0.15, 56, YEL)],
    "p1_b2_a": [("WEIRD...", 300, 0.4, 64, YEL)],
    "p1_b8_a": [("DETECTIVE DAVE", 290, 0.2, 58, YEL)],
    "p1_b9_b": [("WHO IS HE?!", 290, 0.3, 64, (255, 120, 120))],
    "p1_b10_a": [("IT'S ON.", 300, 0.45, 80, (255, 120, 120))],
    "p1_b11_a": [("PART 2", 320, 0.1, 100, YEL), ("TOMORROW...", 430, 0.3, 64, WHITE)],
    "p2_b1_a": [("PREVIOUSLY...", 290, 0.0, 58, WHITE)],
    "p2_b2_a": [("OPERATION UNDERCOVER", 270, 0.15, 42, YEL), ("DAY 1", 350, 0.35, 56, WHITE)],
    "p2_b3_a": [("SPLOOSH!", 300, 0.45, 80, (140, 210, 255))],
    "p2_b5_a": [("DAY 2", 300, 0.05, 64, WHITE)],
    "p2_b6_a": [("COO!", 300, 0.6, 80, YEL)],
    "p2_b10_a": [("...CRYING?", 300, 0.5, 64, (140, 210, 255))],
    "p2_b12_a": [("PART 3", 320, 0.1, 100, YEL), ("TOMORROW...", 430, 0.3, 64, WHITE)],
    "p3_b1_a": [("DATING BOTH?!", 290, 0.3, 64, (255, 120, 120))],
    "p3_b4_a": [("THE PLAN", 290, 0.3, 70, YEL)],
    "p3_b5_a": [("SATURDAY NIGHT", 290, 0.0, 56, YEL)],
    "p3_b6_a": [("DOUBLE PROPOSAL?!", 290, 0.45, 54, YEL)],
    "p3_b10_a": [("*APPLAUSE*", 290, 0.1, 60, WHITE), ("BEST FRIENDS FOREVER", 370, 0.45, 42, YEL)],
}
OUTRO = {1: ("FOLLOW", "FOR PART 2"), 2: ("FOLLOW", "FOR PART 3"), 3: ("THE END", "FOLLOW FOR MORE")}


def heart(d, x, y, r, col=(235, 50, 80)):
    d.ell(x - r * 0.5, y, r * 0.55, r * 0.55, col)
    d.ell(x + r * 0.5, y, r * 0.55, r * 0.55, col)
    d.poly([(x - r * 1.02, y + r * 0.15), (x + r * 1.02, y + r * 0.15), (x, y + r * 1.15)], col)


def pizza_icon(d, x, y, r):
    d.poly([(x - r, y - r * 0.7), (x + r, y - r * 0.7), (x, y + r)], (250, 200, 80))
    d.rect(x - r * 1.05, y - r * 0.95, x + r * 1.05, y - r * 0.6, (210, 140, 60), r=6)
    for px, py in ((-0.35, -0.3), (0.3, -0.25), (0, 0.2)):
        d.ell(x + px * r, y + py * r, r * 0.17, r * 0.17, (200, 50, 40))


def notification(d, p, who, msg, y=520, show_heart=False):
    q = ease(p / 0.15)
    if q <= 0:
        return
    yy = y - 60 * (1 - q)
    d.rect(60, yy - 80, 660, yy + 80, (255, 255, 255, int(235 * q)), r=34)
    d.ell(140, yy, 46, 46, (255, 225, 190))
    pizza_icon(d, 140, yy, 30)
    d.text(210, yy - 30, who, 34, (30, 30, 40), anchor="lm")
    d.text(210, yy + 22, msg, 28, (80, 80, 95), anchor="lm")
    if show_heart:
        heart(d, 615, yy + 18, 20)


def photo_card(d, p):
    q = ease(p / 0.2)
    if q <= 0:
        return
    d.rect(200, 380, 520, 760, (255, 255, 255, int(240 * q)), r=30)
    d.rect(225, 405, 495, 660, (255, 205, 220), r=20)
    d.ell(360, 500, 70, 70, (240, 175, 135))
    d.d.chord([(360 - 76) * K, (500 - 85) * K, (360 + 76) * K, (500 + 40) * K], 180, 360, fill=(140, 50, 25))
    d.ell(335, 500, 8, 9, (30, 30, 30))
    d.ell(385, 500, 8, 9, (30, 30, 30))
    d.rect(300, 570, 420, 660, (240, 90, 150), r=30)
    d.text(330, 705, "my girlfriend", 30, (40, 40, 50))
    heart(d, 470, 700, 16)


def we_know_card(d, p):
    q = ease(p / 0.2)
    if q <= 0:
        return
    s = 0.6 + 0.4 * q
    d.rect(360 - 230 * s, 560 - 140 * s, 360 + 230 * s, 560 + 140 * s, (255, 250, 240), r=24)
    d.rect(360 - 215 * s, 560 - 125 * s, 360 + 215 * s, 560 + 125 * s, None, r=20, outline=(200, 160, 60), w=6)
    d.text(360, 560, "WE KNOW.", 96 * s, (30, 30, 40))


def bye_on_pizza(d, p):
    q = ease(p / 0.3)
    letters = "BYE"
    for i, ch in enumerate(letters):
        if q * 3 > i:
            d.text(250 + i * 110, 600, ch, 150, (190, 40, 30), stroke=4, sfill=(120, 20, 15))


def make_shots(part_dir, part):
    beats = json.load(open(os.path.join(part_dir, "beats.json")))["beats"]
    speaker = {}
    for b in beats:
        for s in b["shots"]:
            speaker[s["shot_id"]] = b.get("speaker", "Narrator")
    cache = {}

    def frame_img(shot, t):
        dd = os.path.join(part_dir, "frames", shot)
        if shot not in cache:
            cache[shot] = sorted(f for f in os.listdir(dd) if f.startswith("f_") and f.endswith(".png"))
        files = cache[shot]
        i = min(len(files) - 1, max(0, int(t * RFPS)))
        return Image.open(os.path.join(dd, files[i])).convert("RGB").resize((W * K, H * K), Image.BILINEAR)

    def make(shot):
        def fn(d, t, T):
            try:
                d.img.paste(frame_img(shot, t), (0, 0))
            except FileNotFoundError:
                pass
            p = t / T
            for text, y, at, size, col in LABELS.get(shot, []):
                if p >= at:
                    q = ease((p - at) * T / 0.25)
                    d.text(W / 2, y, text, size * (0.7 + 0.3 * q), col, stroke=6)
            if shot == "p1_b6_a":
                notification(d, p - 0.25, "Pizza Guy", "can't wait to see you tomorrow", show_heart=True)
            elif shot == "p2_b11_a":
                photo_card(d, p - 0.35)
            elif shot == "p3_b8_a":
                we_know_card(d, p - 0.35)
            elif shot == "p3_b11_a":
                notification(d, p - 0.3, "Pizza Guy", "your order is outside", y=480)
            elif shot == "p3_b13_a":
                bye_on_pizza(d, p)
            elif shot == "outro":
                a, b = OUTRO[part]
                d.text(W / 2, 330, a, 96, YEL if part == 3 else WHITE, stroke=6)
                d.text(W / 2, 440, b, 64, WHITE if part == 3 else YEL, stroke=5)
            who = speaker.get(shot, "Narrator")
            if who in SPEAKER_COL:
                tw = font(32).getlength(who.upper()) / K
                d.rect(W / 2 - tw / 2 - 22, 1062, W / 2 + tw / 2 + 22, 1106, SPEAKER_COL[who], r=22)
                d.text(W / 2, 1084, who.upper(), 32, WHITE)
            if shot == beats[0]["shots"][0]["shot_id"] and t < 2.5:
                d.rect(250, 150, 470, 220, (235, 40, 60), r=34)
                d.text(360, 185, f"PART {part}", 44, WHITE)
            return (0, 0, 0), (0, 0, 0)
        return fn

    ids = [s["shot_id"] for b in beats for s in b["shots"]] + ["outro"]
    return {s: make(s) for s in ids}
