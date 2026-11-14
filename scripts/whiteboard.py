"""
Whiteboard-doodle drawing kit for free_render shots.

Lines "draw themselves on" over time with a slight hand-drawn wobble, a marker pen
follows the newest stroke, and shapes can be tinted afterwards like a highlighter.

Typical use inside a shot function:

    b = Board(d, t, T)                     # one per frame
    b.circle(360, 600, 150, at=0.0, dur=0.3)
    b.fill_circle(360, 600, 150, YELLOW, at=0.3)
    b.write("THE MOON", 360, 300, 60, at=0.35)
    b.finish()                              # draws the pen at the newest stroke tip
"""
import math
import os
import random

from PIL import ImageFont

import free_render as fr

INK = (30, 32, 40)
BLUE, RED, YELLOW, GREEN, ORANGE = (60, 120, 220), (225, 60, 60), (255, 215, 60), (80, 180, 90), (245, 150, 50)
BOARD = ((250, 250, 246), (238, 238, 232))
HAND_FONT = next((p for p in ("/usr/share/fonts/opentype/comic-neue/ComicNeue-Bold.otf",)
                  if os.path.exists(p)), fr.FONT_B)
_hf = {}


def hand_font(size):
    size = int(size * fr.K)
    if size not in _hf:
        _hf[size] = ImageFont.truetype(HAND_FONT, size)
    return _hf[size]


def wobble(pts, amp=2.0, seed=0):
    rnd = random.Random(seed)
    return [(x + rnd.uniform(-amp, amp), y + rnd.uniform(-amp, amp)) for x, y in pts]


def circle_pts(cx, cy, rx, ry=None, n=48, a0=-100, sweep=370):
    ry = ry or rx
    return [(cx + math.cos(math.radians(a0 + sweep * k / n)) * rx,
             cy + math.sin(math.radians(a0 + sweep * k / n)) * ry) for k in range(n + 1)]


def partial(pts, f):
    """First fraction f (0..1) of a polyline, by length; returns (points, tip)."""
    if f <= 0 or len(pts) < 2:
        return [], None
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(seg) or 1
    want, acc, out = total * min(1.0, f), 0.0, [pts[0]]
    for i, L in enumerate(seg):
        if acc + L >= want:
            r = (want - acc) / (L or 1)
            tip = (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r)
            out.append(tip)
            return out, tip
        out.append(pts[i + 1])
        acc += L
    return out, pts[-1]


class Board:
    def __init__(self, d, t, T):
        self.d, self.t, self.T = d, t, T
        self.p = t / T if T else 1.0
        self.tip, self.tip_at = None, -1.0
        self._seed = 0

    def prog(self, at, dur):
        return fr.clamp((self.p - at) / dur) if dur > 0 else float(self.p >= at)

    def _note_tip(self, tip, f, at):
        if tip and 0 < f < 1 and at >= self.tip_at:
            self.tip, self.tip_at = tip, at

    def stroke(self, pts, at=0.0, dur=0.25, col=INK, w=6, amp=1.6):
        self._seed += 1
        f = self.prog(at, dur)
        shown, tip = partial(wobble(pts, amp, self._seed), f)
        if len(shown) >= 2:
            self.d.line(shown, col, w)
        self._note_tip(tip, f, at)
        return f

    def line(self, x0, y0, x1, y1, **kw):
        n = max(2, int(math.dist((x0, y0), (x1, y1)) / 25))
        return self.stroke([(x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n) for k in range(n + 1)], **kw)

    def circle(self, cx, cy, rx, ry=None, **kw):
        return self.stroke(circle_pts(cx, cy, rx, ry), **kw)

    def rect(self, x0, y0, x1, y1, **kw):
        return self.stroke([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0 - 4)], **kw)

    def arrow(self, x0, y0, x1, y1, at=0.0, dur=0.2, col=INK, w=6):
        f = self.line(x0, y0, x1, y1, at=at, dur=dur * 0.7, col=col, w=w)
        a = math.atan2(y1 - y0, x1 - x0)
        for s in (1, -1):
            self.line(x1, y1, x1 - math.cos(a + s * 0.5) * 30, y1 - math.sin(a + s * 0.5) * 30,
                      at=at + dur * 0.7, dur=dur * 0.3, col=col, w=w)
        return f

    def fill_circle(self, cx, cy, r, col, at=0.0, dur=0.15, alpha=170):
        f = self.prog(at, dur)
        if f > 0:
            self.d.ell(cx, cy, r * 0.96, r * 0.96, col + (int(alpha * f),))

    def fill_rect(self, x0, y0, x1, y1, col, at=0.0, dur=0.15, alpha=170):
        f = self.prog(at, dur)
        if f > 0:
            self.d.rect(x0, y0, x1, y1, col + (int(alpha * f),), r=10)

    def write(self, s, x, y, size, at=0.0, dur=0.2, col=INK):
        """Hand-lettered text revealed left-to-right."""
        f = self.prog(at, dur)
        if f <= 0:
            return
        n = max(1, int(round(len(s) * f)))
        full = hand_font(size).getlength(s) / fr.K
        x0 = x - full / 2
        part = s[:n]
        self.d.d.text((x0 * fr.K, y * fr.K), part, font=hand_font(size), fill=col, anchor="lm")
        tip = (x0 + hand_font(size).getlength(part) / fr.K, y + size * 0.3)
        self._note_tip(tip, f, at)

    def finish(self):
        """Draw the marker pen at the newest stroke tip (if something is being drawn)."""
        if not self.tip:
            return
        x, y = self.tip
        a = math.radians(-55)
        L = 170
        ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        nx, ny = -math.sin(a) * 15, math.cos(a) * 15
        self.d.poly([(x, y), (x + math.cos(a) * 28 + nx * 0.6, y + math.sin(a) * 28 + ny * 0.6),
                     (x + math.cos(a) * 28 - nx * 0.6, y + math.sin(a) * 28 - ny * 0.6)], INK)
        self.d.poly([(x + math.cos(a) * 28 + nx, y + math.sin(a) * 28 + ny), (ex + nx, ey + ny),
                     (ex - nx, ey - ny), (x + math.cos(a) * 28 - nx, y + math.sin(a) * 28 - ny)], (235, 235, 240))
        self.d.poly([(x + math.cos(a) * 28 + nx, y + math.sin(a) * 28 + ny),
                     (x + math.cos(a) * 70 + nx, y + math.sin(a) * 70 + ny),
                     (x + math.cos(a) * 70 - nx, y + math.sin(a) * 70 - ny),
                     (x + math.cos(a) * 28 - nx, y + math.sin(a) * 28 - ny)], INK)
