#!/usr/bin/env python3
"""
ElevenLabs narration (key injected by the session proxy). Same outputs as free_voice.py:
audio/narration.wav and audio/timing.json, so scripts/free_render.py can use it unchanged.

Per beat in beats.json:
  "narration"   caption text (plain)
  "tts_text"    optional text sent to ElevenLabs (may include v3 tags like [sighs], [giggles])
  "el_voice"    ElevenLabs voice_id
  "pause_after" seconds of silence after the line (default 0.25)

Usage: python3 scripts/eleven_voice.py out/<project> [--model eleven_v3]
"""
import argparse, io, json, os, subprocess, urllib.request

import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("project_dir")
ap.add_argument("--model", default="eleven_v3")
a = ap.parse_args()

SR = 44100
beats = json.load(open(os.path.join(a.project_dir, "beats.json")))["beats"]
os.makedirs(os.path.join(a.project_dir, "audio", "lines"), exist_ok=True)


def tts(voice, text):
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
        data=json.dumps({"text": text, "model_id": a.model}).encode(),
        headers={"xi-api-key": "proxy-injected", "Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=180).read()


def mp3_to_mono(data):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "f32le", "-ac", "1", "-ar", str(SR), "pipe:1"],
                         input=data, capture_output=True, check=True).stdout
    return np.frombuffer(pcm, dtype=np.float32)


timing, parts, t = [], [], 0.0
for b in beats:
    cache = os.path.join(a.project_dir, "audio", "lines", f"{b['beat_id']}.mp3")
    text = b.get("tts_text", b["narration"])
    key = os.path.join(a.project_dir, "audio", "lines", f"{b['beat_id']}.txt")
    if os.path.exists(cache) and os.path.exists(key) and open(key).read() == f"{b['el_voice']}|{text}":
        data = open(cache, "rb").read()          # reuse: don't spend characters twice
    else:
        data = tts(b["el_voice"], text)
        open(cache, "wb").write(data)
        open(key, "w").write(f"{b['el_voice']}|{text}")
    samples = mp3_to_mono(data)
    seg = np.concatenate([samples, np.zeros(int(SR * b.get("pause_after", 0.25)), dtype=np.float32)])
    dur = len(seg) / SR
    timing.append({"beat_id": b["beat_id"], "start": round(t, 3), "dur": round(dur, 3), "text": b["narration"]})
    parts.append(seg)
    t += dur
sf.write(os.path.join(a.project_dir, "audio", "narration.wav"), np.concatenate(parts), SR)
json.dump(timing, open(os.path.join(a.project_dir, "audio", "timing.json"), "w"), indent=1)
print(f"total {t:.1f}s")
for x in timing:
    print(f"  {x['beat_id']}: {x['dur']:.2f}s")
