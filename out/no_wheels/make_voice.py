"""Free local narration for the no_wheels short using Kokoro TTS (no API key)."""
import json, sys, os
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

model_dir, voice = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "am_michael")
here = os.path.dirname(os.path.abspath(__file__))
beats = json.load(open(os.path.join(here, "beats.json")))["beats"]
k = Kokoro(os.path.join(model_dir, "kokoro-v1.0.int8.onnx"), os.path.join(model_dir, "voices-v1.0.bin"))
timing, parts, t = [], [], 0.0
for b in beats:
    samples, sr = k.create(b["narration"], voice=voice, speed=1.1, lang="en-us")
    gap = np.zeros(int(sr * 0.25), dtype=samples.dtype)
    seg = np.concatenate([samples, gap])
    dur = len(seg) / sr
    timing.append({"beat_id": b["beat_id"], "start": round(t, 3), "dur": round(dur, 3), "text": b["narration"]})
    parts.append(seg); t += dur
sf.write(os.path.join(here, "audio", "narration.wav"), np.concatenate(parts), sr)
json.dump(timing, open(os.path.join(here, "audio", "timing.json"), "w"), indent=1)
print(f"total {t:.1f}s"); [print(x["beat_id"], x["dur"]) for x in timing]
