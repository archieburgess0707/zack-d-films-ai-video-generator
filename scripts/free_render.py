#!/usr/bin/env python3
"""
Free, no-API renderer for Zack D Director projects (no MuAPI key needed).

Each project provides `out/<project>/shots.py`, which does
`from free_render import *` and defines SHOTS = {shot_id: fn(d, t, T) -> (bg_top, bg_bottom)}
plus an "outro" entry. This engine syncs the shots and word-by-word captions to
the narration timing from scripts/free_voice.py, synthesizes a light music bed
and whoosh/thud sound effects, and encodes final.mp4 with ffmpeg.

Usage:
  python3 scripts/free_render.py out/<project>              # full render
  python3 scripts/free_render.py out/<project> 1.5 12 30    # preview stills at those seconds
"""
import json, math, os, random, subprocess, sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = None        # project directory, set in main()
SHOTS = {}         # filled from the project's shots.py
HEADER = ""
W, H, FPS, K = 720, 1280, 30, 2          # K = supersampling factor
OUTRO = 3.5
COUNT_STEP = 0.9   # seconds per countdown number (3, 2, 1) before the reveal
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fonts = {}


def font(size):
    size = int(size * K)
    if size not in _fonts:
        _fonts[size] = ImageFont.truetype(FONT_B, size)
    return _fonts[size]


def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def clamp(p):
    return max(0.0, min(1.0, p))


def mix(c1, c2, p):
    return tuple(int(a + (b - a) * clamp(p)) for a, b in zip(c1, c2))


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


# --------------------------------------------------------------------------- drawing helpers
class D:
    def __init__(self, img):
        self.img = img
        self.d = ImageDraw.Draw(img, "RGBA")

    def rect(self, x0, y0, x1, y1, fill, r=0, outline=None, w=0):
        box = [x0 * K, y0 * K, x1 * K, y1 * K]
        if r:
            self.d.rounded_rectangle(box, r * K, fill=fill, outline=outline, width=int(w * K))
        else:
            self.d.rectangle(box, fill=fill, outline=outline, width=int(w * K))

    def ell(self, cx, cy, rx, ry, fill, outline=None, w=0):
        self.d.ellipse([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K],
                       fill=fill, outline=outline, width=int(w * K))

    def poly(self, pts, fill):
        self.d.polygon([(x * K, y * K) for x, y in pts], fill=fill)

    def line(self, pts, fill, w):
        self.d.line([(x * K, y * K) for x, y in pts], fill=fill, width=max(1, int(w * K)), joint="curve")

    def text(self, x, y, s, size, fill=(255, 255, 255), anchor="mm", stroke=0, sfill=(0, 0, 0)):
        self.d.text((x * K, y * K), s, font=font(size), fill=fill, anchor=anchor,
                    stroke_width=int(stroke * K), stroke_fill=sfill)

    def shadow(self, cx, cy, rx, ry=None, a=90):
        self.ell(cx, cy, rx, ry or rx * 0.18, (0, 0, 0, a))

    def ball(self, cx, cy, r, c):
        """Shaded sphere-ish circle for a clay/3D feel."""
        self.ell(cx, cy, r, r, shade(c, 0.7))
        self.ell(cx - r * 0.08, cy - r * 0.08, r * 0.9, r * 0.9, c)
        self.ell(cx - r * 0.35, cy - r * 0.38, r * 0.28, r * 0.2, (255, 255, 255, 110))


_bg_cache = {}


def gradient(top, bottom):
    key = (top, bottom)
    if key not in _bg_cache:
        col = np.linspace(0, 1, H * K)[:, None]
        arr = (np.array(top)[None, :] * (1 - col) + np.array(bottom)[None, :] * col).astype(np.uint8)
        arr = np.repeat(arr[:, None, :], W * K, axis=1)
        _bg_cache[key] = Image.fromarray(arr, "RGB")
    return _bg_cache[key].copy()


# --------------------------------------------------------------------------- props
SKIN, HOODIE, HAIR = (240, 196, 160), (52, 120, 220), (90, 60, 40)
CAR_RED = (226, 58, 52)


def wheel(d, cx, cy, r, ang, s=1.0):
    if s <= 0.02:
        return
    r *= s
    d.ell(cx, cy, r, r, (34, 34, 40))
    d.ell(cx, cy, r * 0.58, r * 0.58, (190, 195, 205))
    d.ell(cx, cy, r * 0.2, r * 0.2, (120, 125, 135))
    for k in range(5):
        a = ang + k * 2 * math.pi / 5
        d.line([(cx, cy), (cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55)], (120, 125, 135), r * 0.12)


def car(d, x, ground, sc=1.0, wheel_s=1.0, drop=0.0, ang=0.0, color=CAR_RED):
    """Side-view hatchback. `drop` lowers the body toward the ground (0..1)."""
    wr = 34 * sc
    body_bottom = ground - wr * 0.9 * (1 - drop) - 4 * sc * drop
    d.shadow(x, ground + 4, 170 * sc, 16 * sc)
    bw, bh = 330 * sc, 80 * sc
    y0 = body_bottom - bh
    d.rect(x - bw / 2 + 30 * sc, y0 - 70 * sc, x + bw / 2 - 70 * sc, y0 + 20 * sc, shade(color, 0.85), r=34 * sc)
    d.rect(x - bw / 2 + 52 * sc, y0 - 54 * sc, x - 6 * sc, y0 + 4 * sc, (160, 215, 245), r=14 * sc)
    d.rect(x + 6 * sc, y0 - 54 * sc, x + bw / 2 - 92 * sc, y0 + 4 * sc, (160, 215, 245), r=14 * sc)
    d.rect(x - bw / 2, y0, x + bw / 2, body_bottom, color, r=30 * sc)
    d.rect(x - bw / 2 + 10 * sc, y0 + 8 * sc, x + bw / 2 - 10 * sc, y0 + 22 * sc, (255, 255, 255, 70), r=7 * sc)
    d.ell(x + bw / 2 - 16 * sc, y0 + 30 * sc, 12 * sc, 9 * sc, (255, 240, 170))
    for wx in (x - bw / 2 + 70 * sc, x + bw / 2 - 70 * sc):
        d.ell(wx, body_bottom - 4 * sc, wr * 1.15, wr * 1.0, shade(color, 0.45))
        wheel(d, wx, ground - wr, wr, ang, wheel_s)


def person(d, x, ground, sc=1.0, mood="neutral", arms="down", lean=0.0, hoodie=HOODIE):
    """mood: neutral, shock, happy, strain, tired, sleep."""
    d.shadow(x, ground + 2, 60 * sc, 12 * sc)
    hip = ground - 95 * sc
    for dx in (-16, 16):
        d.line([(x + dx * sc, hip), (x + dx * sc + lean * 20 * sc, ground - 6 * sc)], (40, 45, 70), 22 * sc)
        d.ell(x + dx * sc + lean * 20 * sc + 6 * sc, ground - 6 * sc, 17 * sc, 9 * sc, (30, 30, 35))
    tx = x - lean * 30 * sc
    d.rect(tx - 48 * sc, hip - 120 * sc, tx + 48 * sc, hip + 6 * sc, hoodie, r=34 * sc)
    d.rect(tx - 40 * sc, hip - 112 * sc, tx - 18 * sc, hip - 10 * sc, (255, 255, 255, 40), r=10 * sc)
    sh = hip - 100 * sc
    if arms == "up":
        hands = [(tx - 70 * sc, sh - 95 * sc), (tx + 70 * sc, sh - 95 * sc)]
    elif arms == "forward":
        hands = [(tx + 85 * sc, sh + 25 * sc), (tx + 90 * sc, sh + 40 * sc)]
    elif arms == "shock":
        hands = [(tx - 30 * sc, sh - 70 * sc), (tx + 30 * sc, sh - 70 * sc)]
    else:
        hands = [(tx - 62 * sc, sh + 85 * sc), (tx + 62 * sc, sh + 85 * sc)]
    for side, hnd in zip((-1, 1), hands):
        d.line([(tx + side * 42 * sc, sh), hnd], shade(hoodie, 0.85), 22 * sc)
        d.ell(hnd[0], hnd[1], 13 * sc, 13 * sc, SKIN)
    hx, hy = tx + lean * 10 * sc, sh - 62 * sc
    d.ball(hx, hy, 52 * sc, SKIN)
    d.d.chord([(hx - 54 * sc) * K, (hy - 58 * sc) * K, (hx + 54 * sc) * K, (hy + 30 * sc) * K], 180, 360, fill=HAIR)
    ey = hy + 4 * sc
    for ex in (-18, 18):
        if mood == "sleep":
            d.d.arc([(hx + (ex - 9) * sc) * K, (ey - 6 * sc) * K, (hx + (ex + 9) * sc) * K, (ey + 6 * sc) * K],
                    10, 170, fill=(40, 30, 30), width=int(3 * sc * K))
            continue
        r = 9 if mood == "shock" else 7
        d.ell(hx + ex * sc, ey, r * sc, r * sc * 1.2, (255, 255, 255))
        d.ell(hx + ex * sc, ey + 1 * sc, 4.5 * sc, 5 * sc, (30, 30, 40))
        if mood == "tired":  # heavy eyelids + dark circles
            d.rect(hx + (ex - 10) * sc, ey - 10 * sc, hx + (ex + 10) * sc, ey + 1 * sc, shade(SKIN, 0.92))
            d.d.arc([(hx + (ex - 10) * sc) * K, (ey + 2 * sc) * K, (hx + (ex + 10) * sc) * K, (ey + 14 * sc) * K],
                    20, 160, fill=(150, 110, 140), width=int(3 * sc * K))
    if mood == "shock":
        d.ell(hx, hy + 30 * sc, 9 * sc, 12 * sc, (90, 30, 30))
    elif mood == "happy":
        d.d.arc([(hx - 18 * sc) * K, (hy + 12 * sc) * K, (hx + 18 * sc) * K, (hy + 36 * sc) * K], 10, 170,
                fill=(90, 30, 30), width=int(5 * sc * K))
    elif mood in ("tired", "sleep"):
        d.ell(hx, hy + 30 * sc, 6 * sc, 4 * sc, (90, 30, 30))
    elif mood == "strain":
        d.line([(hx - 14 * sc, hy + 28 * sc), (hx + 14 * sc, hy + 26 * sc)], (90, 30, 30), 5 * sc)
        d.ell(hx + 40 * sc, hy - 20 * sc, 6 * sc, 9 * sc, (120, 190, 255))
    else:
        d.line([(hx - 12 * sc, hy + 28 * sc), (hx + 12 * sc, hy + 28 * sc)], (90, 30, 30), 5 * sc)
    return hands


def gear_pts(cx, cy, r, teeth, ang):
    pts = []
    n = teeth * 4
    for i in range(n):
        a = ang + i * 2 * math.pi / n
        rr = r if (i % 4) in (0, 1) else r * 0.82
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def gear(d, cx, cy, r, teeth, ang, c, alpha=255):
    if alpha <= 3:
        return
    col = c + (int(alpha),)
    d.poly(gear_pts(cx + 4, cy + 6, r, teeth, ang), (0, 0, 0, int(alpha * 0.35)))
    d.poly(gear_pts(cx, cy, r, teeth, ang), col)
    d.ell(cx, cy, r * 0.62, r * 0.62, shade(c, 1.15) + (int(alpha),))
    d.ell(cx, cy, r * 0.18, r * 0.18, (40, 40, 50, int(alpha)))


def sparks(d, x, y, t, n=14, seed=1, spread=120, col=(255, 210, 90)):
    rnd = random.Random(seed + int(t * 12))
    for _ in range(n):
        a = rnd.uniform(math.pi * 1.05, math.pi * 1.95)
        L = rnd.uniform(15, spread)
        sx, sy = x + rnd.uniform(-30, 30), y
        d.line([(sx, sy), (sx + math.cos(a) * L, sy + math.sin(a) * L)], col, rnd.uniform(2, 5))


def ground_scene(d, horizon=880, sky=None, road=(70, 72, 82)):
    d.rect(0, horizon, W, H, road)
    d.rect(0, horizon, W, horizon + 10, shade(road, 1.3))
    for i in range(6):
        d.rect(i * 140 + 20, horizon + 70, i * 140 + 100, horizon + 82, (230, 220, 120))


def label(d, s, y=230, size=46, fill=(255, 255, 255), bg=(0, 0, 0, 150), p=1.0):
    if p <= 0:
        return
    sc = 0.6 + 0.4 * ease(p * 3)
    tw = font(size * sc).getlength(s) / K
    d.rect(W / 2 - tw / 2 - 24, y - size * sc * 0.8, W / 2 + tw / 2 + 24, y + size * sc * 0.8, bg, r=18)
    d.text(W / 2, y, s, size * sc, fill, stroke=3)


def stamp(d, s, y, p, col=(235, 50, 50)):
    if p <= 0:
        return
    sc = 1.8 - 0.8 * ease(p * 4)
    tw = font(64 * sc).getlength(s) / K
    d.rect(W / 2 - tw / 2 - 26, y - 52 * sc, W / 2 + tw / 2 + 26, y + 52 * sc, None, r=14, outline=col, w=8 * sc)
    d.text(W / 2, y, s, 64 * sc, col)


# --------------------------------------------------------------------------- shots

# --------------------------------------------------------------------------- timeline
def build_timeline():
    beats = json.load(open(os.path.join(HERE, "beats.json")))["beats"]
    timing = {x["beat_id"]: x for x in json.load(open(os.path.join(HERE, "audio", "timing.json")))}
    shots, words = [], []
    for b in beats:
        tm = timing[b["beat_id"]]
        # optional per-shot "share" of the beat (default: equal split) to land cuts on the right words
        shares = [s.get("share") for s in b["shots"]]
        rest = 1 - sum(x for x in shares if x)
        free = sum(1 for x in shares if not x)
        shares = [x if x else rest / free for x in shares]
        st = tm["start"]
        for s, sh in zip(b["shots"], shares):
            shots.append({"id": s["shot_id"], "start": st, "dur": tm["dur"] * sh,
                          "impact": s.get("zoom_impact", False)})
            st += tm["dur"] * sh
        ws = b["narration"].split()
        speak = tm["dur"] - b.get("pause_after", 0.25)
        weights = [len(w) + 2 for w in ws]
        tot, acc = sum(weights), 0
        group = []
        for i, w in enumerate(ws):
            st = tm["start"] + speak * acc / tot
            acc += weights[i]
            words.append({"w": w, "start": st, "end": tm["start"] + speak * acc / tot, "beat": b["beat_id"]})
    narr_end = shots[-1]["start"] + shots[-1]["dur"]
    shots.append({"id": "outro", "start": narr_end, "dur": OUTRO, "impact": True})
    # caption chunks of up to 3 words, never crossing a beat
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) == 3 or cur[-1]["beat"] != w["beat"] or cur[-1]["w"][-1] in ".,:?!"):
            chunks.append(cur); cur = []
        cur.append(w)
    chunks.append(cur)
    return shots, chunks, narr_end + OUTRO


def draw_caption(d, chunks, T):
    for ch in chunks:
        if ch[0]["start"] <= T < ch[-1]["end"] + 0.05:
            texts = [w["w"].upper() for w in ch]
            size = 58
            gap = font(size).getlength(" ") / K
            widths = [font(size).getlength(s) / K for s in texts]
            total = sum(widths) + gap * (len(texts) - 1)
            if total > W - 60:
                size = size * (W - 60) / total
                widths = [x * (W - 60) / total for x in widths]; gap *= (W - 60) / total; total = W - 60
            x = W / 2 - total / 2
            pop = 1 + 0.12 * (1 - ease((T - ch[0]["start"]) / 0.12))
            for w, s, wd in zip(ch, texts, widths):
                active = w["start"] <= T < w["end"] + 0.05
                d.text(x + wd / 2, 1150, s, size * (pop if active else 1),
                       (255, 230, 40) if active else (255, 255, 255), stroke=6)
                x += wd + gap
            return


SHOTS_TL, CHUNKS, TOTAL = None, None, None
BG = {}


def load_project(project_dir):
    global HERE, SHOTS, HEADER
    import importlib.util
    HERE = os.path.abspath(project_dir)
    spec = importlib.util.spec_from_file_location("project_shots", os.path.join(HERE, "shots.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    SHOTS = mod.SHOTS
    data = json.load(open(os.path.join(HERE, "beats.json")))
    HEADER = data.get("header", data.get("topic", "")).upper()
    global OUTRO
    OUTRO = float(data.get("outro_sec", OUTRO))  # optional per-project end-card length


def init():
    global SHOTS_TL, CHUNKS, TOTAL
    SHOTS_TL, CHUNKS, TOTAL = build_timeline()


def render(fi):
    T = fi / FPS
    shot = SHOTS_TL[-1]
    for s in SHOTS_TL:
        if s["start"] <= T < s["start"] + s["dur"]:
            shot = s
            break
    t = T - shot["start"]
    if shot["id"] not in BG:  # backgrounds are constant per shot; learn once
        BG[shot["id"]] = SHOTS[shot["id"]](D(Image.new("RGB", (W * K, H * K))), 0.0, shot["dur"])
    bg = BG[shot["id"]]
    img = gradient(*bg)
    d = D(img)
    SHOTS[shot["id"]](d, t, shot["dur"])
    d.rect(0, 40, W, 130, (0, 0, 0, 110))
    hs = min(34, 34 * (W - 50) / (font(34).getlength(HEADER) / K))  # shrink long titles to fit
    d.text(W / 2, 86, HEADER, hs, (255, 255, 255), stroke=3)
    draw_caption(d, CHUNKS, T)
    img = img.reduce(K)
    # slow push-in on every shot + punch zoom/shake on impact shots
    z = 1 + 0.04 * (t / shot["dur"])
    dx = dy = 0
    if shot["impact"] and t < 0.45:
        z += 0.08 * (1 - t / 0.45)
        dx, dy = math.sin(fi * 2.1) * 10 * (1 - t / 0.45), math.cos(fi * 1.7) * 10 * (1 - t / 0.45)
    cw, chh = W / z, H / z
    x0, y0 = (W - cw) / 2 + dx, (H - chh) / 2 + dy
    img = img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + chh))
    if t < 0.12:  # quick flash on every cut
        img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.55 * (1 - t / 0.12))
    return img.tobytes()


# --------------------------------------------------------------------------- audio
def make_audio(total, out_path):
    narr, sr = sf.read(os.path.join(HERE, "audio", "narration.wav"))
    n = int(total * sr)
    tt = np.arange(n) / sr
    music = np.zeros(n)
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [261.63, 329.63, 392.0], [196.0, 246.94, 293.66]]
    bar = 2.0
    for i in range(int(total / bar) + 1):
        a, b = int(i * bar * sr), min(n, int((i + 1) * bar * sr))
        seg = tt[a:b] - i * bar
        env = np.minimum(1, seg / 0.3) * np.exp(-seg * 0.6)
        for f in chords[i % 4]:
            music[a:b] += np.sin(2 * np.pi * f * seg) * env * 0.05 + np.sin(2 * np.pi * f / 2 * seg) * env * 0.04
        for k in range(4):  # soft pulse
            s0 = a + int(k * 0.5 * sr)
            L = min(int(0.12 * sr), n - s0)
            if L > 0:
                music[s0:s0 + L] += np.sin(2 * np.pi * chords[i % 4][0] / 4 * np.arange(L) / sr) * np.exp(-np.arange(L) / sr * 30) * 0.18
    sfx = np.zeros(n)
    rng = np.random.default_rng(0)
    shots, _, _ = build_timeline()
    for s in shots[1:]:
        a = int(max(0, s["start"] - 0.12) * sr)
        L = min(int(0.3 * sr), n - a)
        noise = rng.standard_normal(L)
        noise = np.convolve(noise, np.ones(30) / 30, mode="same")
        sfx[a:a + L] += noise * np.sin(np.linspace(0, np.pi, L)) * 0.5
        if s["impact"]:
            a = int(s["start"] * sr)
            L = min(int(0.4 * sr), n - a)
            x = np.arange(L) / sr
            sfx[a:a + L] += np.sin(2 * np.pi * (90 - 50 * x) * x) * np.exp(-x * 9) * 0.6
    # countdown beats: 3 ticks then a "ding" (beat["countdown"] = seconds before beat end it starts)
    beats = json.load(open(os.path.join(HERE, "beats.json")))["beats"]
    timing = {x["beat_id"]: x for x in json.load(open(os.path.join(HERE, "audio", "timing.json")))}
    for b in beats:
        if not b.get("countdown"):
            continue
        end = timing[b["beat_id"]]["start"] + timing[b["beat_id"]]["dur"]
        c0 = end - b["countdown"]
        for k in range(4):
            a = int((c0 + k * COUNT_STEP) * sr)
            L = min(int((0.5 if k == 3 else 0.08) * sr), n - a)
            if L <= 0:
                continue
            x = np.arange(L) / sr
            if k < 3:
                sfx[a:a + L] += np.sin(2 * np.pi * 1600 * x) * np.exp(-x * 60) * 0.9
            else:
                sfx[a:a + L] += (np.sin(2 * np.pi * 1318.5 * x) + 0.5 * np.sin(2 * np.pi * 1975.5 * x)) * np.exp(-x * 5) * 0.7
    voice = np.zeros(n)
    voice[:min(n, len(narr))] = narr[:n]
    duck = 1 - 0.55 * (np.convolve(np.abs(voice) > 0.02, np.ones(sr // 4) / (sr // 4), mode="same") > 0.05)
    mixd = voice * 1.1 + music * duck * 0.9 + sfx * 0.35
    mixd /= max(1.0, np.abs(mixd).max() / 0.95)
    sf.write(out_path, mixd.astype(np.float32), sr)


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    load_project(sys.argv[1])
    init()
    nframes = int(round(TOTAL * FPS))
    audio = os.path.join(HERE, "audio", "mix.wav")
    make_audio(TOTAL, audio)
    out = os.path.join(HERE, "final.mp4")
    if len(sys.argv) > 2:  # preview stills
        for s in sys.argv[2:]:
            fi = int(float(s) * FPS)
            Image.frombytes("RGB", (W, H), render(fi)).save(os.path.join(HERE, f"preview_{s}.png"))
        return
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out],
                          stdin=subprocess.PIPE)
    with Pool(os.cpu_count(), initializer=init) as pool:
        for i, frame in enumerate(pool.imap(render, range(nframes), chunksize=8)):
            ff.stdin.write(frame)
            if i % 300 == 0:
                print(f"frame {i}/{nframes}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("wrote", out, f"{TOTAL:.1f}s")


if __name__ == "__main__":
    main()
