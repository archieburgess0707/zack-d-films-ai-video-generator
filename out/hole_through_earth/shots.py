"""Composite Blender-rendered frames (frames/<shot>/f_####.png at 15 fps) with 2D labels."""
import os

from free_render import *  # noqa: F401,F403

HERE_ = os.path.dirname(os.path.abspath(__file__))
RFPS = 15
_cache = {}

# (text, y, appear-at fraction of shot, size, colour)
LABELS = {
    "beat_1_a": [("38 MINUTES?!", 300, 0.55, 70, (255, 235, 80))],
    "beat_2_a": [("~12,700 km", 300, 0.4, 64, (255, 235, 80))],
    "beat_2_b": [("OF SOLID ROCK", 300, 0.1, 54, (255, 255, 255))],
    "beat_3_a": [("DEEPEST HOLE EVER", 280, 0.05, 46, (255, 255, 255)), ("ONLY ~12 km", 370, 0.4, 60, (255, 235, 80))],
    "beat_3_b": [("THAT'S A SCRATCH!", 300, 0.2, 54, (255, 235, 80))],
    "beat_4_a": [("THE MANTLE", 280, 0.1, 64, (255, 200, 120))],
    "beat_4_b": [("FLOWS LIKE TOFFEE", 280, 0.1, 50, (255, 255, 255))],
    "beat_5_a": [("LIQUID METAL", 280, 0.1, 60, (255, 200, 80))],
    "beat_5_b": [("AS HOT AS THE", 260, 0.2, 50, (255, 255, 255)), ("SUN'S SURFACE", 330, 0.3, 58, (255, 235, 80))],
    "beat_6_a": [("MAGIC HEAT-PROOF TUBE", 300, 0.2, 42, (170, 230, 255))],
    "beat_6_b": [("JUMP!", 320, 0.3, 90, (255, 235, 80))],
    "beat_7_a": [("FASTER...", 300, 0.1, 64, (255, 255, 255)), ("AND FASTER!", 380, 0.5, 64, (255, 235, 80))],
    "beat_7_b": [("ROCKET SPEED!", 300, 0.55, 62, (255, 235, 80))],
    "beat_8_a": [("WEIGHTLESS", 290, 0.15, 70, (255, 255, 255))],
    "beat_8_b": [("PULLED EQUALLY", 290, 0.15, 52, (255, 235, 80))],
    "beat_9_a": [("SLOWING DOWN...", 300, 0.15, 54, (255, 255, 255))],
    "beat_9_b": [("THE OTHER SIDE!", 300, 0.3, 58, (255, 235, 80))],
    "beat_10_a": [("WAIT... NO!", 300, 0.25, 70, (255, 120, 120))],
    "beat_10_b": [("A HUMAN YO-YO", 300, 0.2, 58, (255, 235, 80))],
    "beat_11_a": [("UK", 300, 0.05, 64, (255, 120, 120)), ("→ NEW ZEALAND", 380, 0.5, 52, (255, 235, 80))],
    "beat_11_b": [("SPLASH!", 300, 0.35, 80, (170, 230, 255))],
    "beat_12_a": [("WOULD YOU JUMP?", 300, 0.0, 62, (255, 235, 80))],
    "beat_12_b": [("WOULD YOU JUMP?", 300, 0.0, 62, (255, 235, 80))],
}


def frame_img(shot, t):
    d = os.path.join(HERE_, "frames", shot)
    if shot not in _cache:
        _cache[shot] = sorted(f for f in os.listdir(d) if f.startswith("f_") and f.endswith(".png"))
    files = _cache[shot]
    i = min(len(files) - 1, max(0, int(t * RFPS)))
    return Image.open(os.path.join(d, files[i])).convert("RGB").resize((W * K, H * K), Image.BILINEAR)


def make(shot):
    def fn(d, t, T):
        d.img.paste(frame_img(shot, t), (0, 0))
        p = t / T
        for text, y, at, size, col in LABELS.get(shot, []):
            if p >= at:
                q = ease((p - at) * T / 0.25)
                d.text(W / 2, y, text, size * (0.7 + 0.3 * q), col, stroke=6)
        if shot == "outro":
            d.text(W / 2, 860, "WHAT SHOULD I", 62, (255, 255, 255), stroke=5)
            d.text(W / 2, 950, "EXPLAIN NEXT?", 62, (255, 235, 80), stroke=5)
            d.text(W / 2, 1050, "COMMENT BELOW", 38, (255, 255, 255), stroke=3)
        return (0, 0, 0), (0, 0, 0)
    return fn


_ids = [f"beat_{i}_{ab}" for i in range(1, 13) for ab in "ab"] + ["outro"]
SHOTS = {s: make(s) for s in _ids}
