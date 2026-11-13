#!/usr/bin/env python3
"""
Free local narration with Kokoro TTS (no API key). Writes audio/narration.wav and
audio/timing.json (per-beat start/duration) used by scripts/free_render.py.

Model files (kokoro-v1.0.int8.onnx, voices-v1.0.bin) come from
https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0

Usage: python3 scripts/free_voice.py out/<project> --models <dir> [--voice af_heart] [--speed 1.15] [--pitch 1.03]

--pitch shifts pitch without changing timing (ffmpeg rubberband); a slight lift sounds more upbeat.
"""
import argparse, json, os, subprocess
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ap = argparse.ArgumentParser()
ap.add_argument("project_dir")
ap.add_argument("--models", required=True)
ap.add_argument("--voice", default="af_heart")
ap.add_argument("--speed", type=float, default=1.15)
ap.add_argument("--pitch", type=float, default=1.03)
a = ap.parse_args()

beats = json.load(open(os.path.join(a.project_dir, "beats.json")))["beats"]
k = Kokoro(os.path.join(a.models, "kokoro-v1.0.int8.onnx"), os.path.join(a.models, "voices-v1.0.bin"))
os.makedirs(os.path.join(a.project_dir, "audio"), exist_ok=True)
timing, parts, t = [], [], 0.0
for b in beats:
    samples, sr = k.create(b.get("tts_text", b["narration"]), voice=a.voice, speed=a.speed, lang="en-us")
    seg = np.concatenate([samples, np.zeros(int(sr * b.get("pause_after", 0.25)), dtype=samples.dtype)])
    dur = len(seg) / sr
    timing.append({"beat_id": b["beat_id"], "start": round(t, 3), "dur": round(dur, 3), "text": b["narration"]})
    parts.append(seg)
    t += dur
out = os.path.join(a.project_dir, "audio", "narration.wav")
sf.write(out, np.concatenate(parts), sr)
if a.pitch != 1.0:
    tmp = out + ".tmp.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", f"rubberband=pitch={a.pitch}", tmp], check=True)
    os.replace(tmp, out)
json.dump(timing, open(os.path.join(a.project_dir, "audio", "timing.json"), "w"), indent=1)
print(f"total {t:.1f}s")
for x in timing:
    print(f"  {x['beat_id']}: {x['dur']:.2f}s")
