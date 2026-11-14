"""Lemon story compositor: plays each AI video clip (frames/<clip>/f_####.png, 24 fps) with 2D overlays."""
import json
import os

from free_render import *  # noqa: F401,F403

HERE_ = os.path.dirname(os.path.abspath(__file__))
RFPS = 24
YEL, WHITE = (255, 235, 80), (255, 255, 255)
SPEAKER_COL = {"Lenny": (225, 185, 20), "Sophie": (225, 50, 70)}
LABELS = {
    "c2": [("*SOUR FACE*", 290, 0.35, 56, YEL)],
    "c4": [("HEATWAVE!", 300, 0.15, 90, (255, 140, 60))],
    "c5": [("BESTIE?!", 300, 0.4, 80, (255, 120, 150))],
    "c6": [("FULLY BOOKED", 300, 0.45, 66, YEL)],
}
beats = json.load(open(os.path.join(HERE_, "beats.json")))["beats"]
timing = {t["beat_id"]: t for t in json.load(open(os.path.join(HERE_, "audio", "timing.json")))}
SPEAKER = {b["shots"][0]["shot_id"]: b["speaker"] for b in beats}
_cache = {}


def frame(clip, t):
    d = os.path.join(HERE_, "frames", clip)
    if clip not in _cache:
        _cache[clip] = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    files = _cache[clip]
    i = min(len(files) - 1, max(0, int(t * RFPS)))
    return Image.open(os.path.join(d, files[i])).convert("RGB").resize((W * K, H * K), Image.BILINEAR)


def make(shot):
    def fn(d, t, T):
        if shot == "outro":   # keep the last clip playing under the end card
            d.img.paste(frame("c7", t + timing[beats[-1]["beat_id"]]["dur"]), (0, 0))
            d.rect(0, 380, W, 700, (0, 0, 0, 120))
            d.text(W / 2, 470, "FOLLOW", 96, WHITE, stroke=6)
            d.text(W / 2, 590, "FOR MORE FRUIT DRAMA", 46, YEL, stroke=5)
            return (0, 0, 0), (0, 0, 0)
        d.img.paste(frame(shot, t), (0, 0))
        p = t / T
        for text, y, at, size, col in LABELS.get(shot, []):
            if p >= at:
                q = ease((p - at) * T / 0.25)
                d.text(W / 2, y, text, size * (0.7 + 0.3 * q), col, stroke=6)
        who = SPEAKER.get(shot)
        if who in SPEAKER_COL:
            tw = font(32).getlength(who.upper()) / K
            d.rect(W / 2 - tw / 2 - 22, 1062, W / 2 + tw / 2 + 22, 1106, SPEAKER_COL[who], r=22)
            d.text(W / 2, 1084, who.upper(), 32, WHITE)
        return (0, 0, 0), (0, 0, 0)
    return fn


SHOTS = {s: make(s) for s in [b["shots"][0]["shot_id"] for b in beats] + ["outro"]}
