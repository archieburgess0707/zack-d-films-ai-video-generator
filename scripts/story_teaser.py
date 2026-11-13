#!/usr/bin/env python3
"""
Turn a short clip into a "watch more on my profile" teaser for TikTok/Instagram Stories.

Adds a banner over the clip, then a ~4s end card (blurred last frame, "what happens next?",
bouncing arrow toward the profile picture in the top-left) with a riser + ding sound.

Usage: python3 scripts/story_teaser.py input.mov output.mp4 [--end 4.0]
"""
import argparse, math, os, subprocess, sys, tempfile

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 720, 1280, 30
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
YELLOW, WHITE = (255, 230, 40), (255, 255, 255)


def f(size):
    return ImageFont.truetype(FONT, int(size))


def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def pill(draw, cx, cy, text, size, fill=(235, 40, 60), fg=WHITE):
    tw = draw.textlength(text, font=f(size))
    draw.rounded_rectangle([cx - tw / 2 - 28, cy - size * 0.85, cx + tw / 2 + 28, cy + size * 0.85],
                           radius=size * 0.85, fill=fill)
    draw.text((cx, cy), text, font=f(size), fill=fg, anchor="mm")


def banner_png(path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pill(d, W / 2, 178, "FULL VIDEO ON MY PROFILE", 32)
    img.save(path)


def arrow(d, x, y, s, col):
    """Arrow pointing up-left with its tip at (x, y)."""
    a = math.radians(225)
    tail = (x - math.cos(a) * 150 * s, y - math.sin(a) * 150 * s)
    d.line([tail, (x - math.cos(a) * 40 * s, y - math.sin(a) * 40 * s)], fill=col, width=int(26 * s))
    left, right = a + math.radians(155), a - math.radians(155)
    d.polygon([(x, y), (x + math.cos(left) * 75 * s, y + math.sin(left) * 75 * s),
               (x + math.cos(right) * 75 * s, y + math.sin(right) * 75 * s)], fill=col)


def end_frames(last_frame, dur):
    bg = last_frame.convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(18))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.55)
    n = int(dur * FPS)
    for i in range(n):
        t = i / FPS
        img = bg.copy()
        d = ImageDraw.Draw(img)
        p1 = ease(t / 0.35)
        if p1 > 0:
            d.text((W / 2, 470), "WHAT HAPPENS", font=f(70 * (0.7 + 0.3 * p1)), fill=WHITE, anchor="mm",
                   stroke_width=5, stroke_fill=(0, 0, 0))
            d.text((W / 2, 560), "NEXT?", font=f(96 * (0.7 + 0.3 * p1)), fill=YELLOW, anchor="mm",
                   stroke_width=6, stroke_fill=(0, 0, 0))
        p2 = ease((t - 0.5) / 0.35)
        if p2 > 0:
            pulse = 1 + 0.05 * math.sin(t * 7)
            pill(d, W / 2, 760, "WATCH THE FULL VIDEO", 44 * pulse * (0.8 + 0.2 * p2))
            d.text((W / 2, 850), "ON MY PROFILE", font=f(52 * pulse), fill=WHITE, anchor="mm",
                   stroke_width=5, stroke_fill=(0, 0, 0))
        p3 = ease((t - 0.9) / 0.3)
        if p3 > 0:
            bob = 18 * math.sin(t * 8)
            arrow(d, 150 - bob, 230 - bob, 1.0, YELLOW)
            d.text((300, 330), "TAP MY PROFILE PIC", font=f(34), fill=YELLOW, anchor="lm",
                   stroke_width=4, stroke_fill=(0, 0, 0))
        yield img.tobytes()


def end_audio(path, dur, sr=48000):
    n = int(dur * sr)
    t = np.arange(n) / sr
    riser = np.random.default_rng(1).standard_normal(n)
    riser = np.convolve(riser, np.ones(40) / 40, mode="same") * np.clip(1 - t / 0.6, 0, 1) * 0.25
    ding = np.zeros(n)
    s0 = int(0.5 * sr)
    tt = t[: n - s0]
    ding[s0:] = (np.sin(2 * np.pi * 1318.5 * tt) * 0.35 + np.sin(2 * np.pi * 1975.5 * tt) * 0.15) * np.exp(-tt * 4)
    pad = np.zeros(n)
    for k, fr in enumerate((261.63, 329.63, 392.0)):
        pad += np.sin(2 * np.pi * fr * t) * 0.05
    pad *= np.clip(t / 0.4, 0, 1) * np.clip((dur - t) / 0.6, 0, 1)
    mix = riser + ding + pad
    sf.write(path, np.stack([mix, mix], axis=1).astype(np.float32), sr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--end", type=float, default=4.0)
    a = ap.parse_args()
    tmp = tempfile.mkdtemp()
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", a.input]).decode())
    last = os.path.join(tmp, "last.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", a.input, "-frames:v", "1",
                    "-vf", f"scale={W}:{H}", last], check=True)
    banner = os.path.join(tmp, "banner.png")
    banner_png(banner)
    endv, enda = os.path.join(tmp, "end.mp4"), os.path.join(tmp, "end.wav")
    end_audio(enda, a.end)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", enda, "-c:v", "libx264", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-ar", "48000", "-shortest", endv], stdin=subprocess.PIPE)
    for fr in end_frames(Image.open(last), a.end):
        ff.stdin.write(fr)
    ff.stdin.close()
    ff.wait()
    fade = max(0.0, dur - 0.4)
    graph = (f"[0:v]scale={W}:{H},fps={FPS},setsar=1[c];[c][1:v]overlay=0:0:enable='gte(t,0.6)'[cv];"
             f"[0:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=out:st={fade:.2f}:d=0.4[ca];"
             f"[2:v]setsar=1[ev];[2:a]aresample=48000,aformat=channel_layouts=stereo[ea];"
             f"[cv][ca][ev][ea]concat=n=2:v=1:a=1[v][a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.input, "-loop", "1", "-t", f"{dur:.3f}", "-i", banner,
                    "-i", endv, "-filter_complex", graph, "-map", "[v]", "-map", "[a]", "-c:v", "libx264",
                    "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
                    a.output], check=True)
    print("wrote", a.output)


if __name__ == "__main__":
    main()
