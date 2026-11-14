#!/usr/bin/env python3
"""
Small MuAPI helper (keys are injected by the session proxy — no key in code).

  python3 scripts/muapi_gen.py image  "<prompt>" out.jpg [--ref URL ...]
  python3 scripts/muapi_gen.py video  <image_url> "<prompt>" out.mp4 [--model veo3.1-fast-image-to-video]

Every call prints the job's cost so spending stays visible.
"""
import json
import sys
import time
import urllib.request

BASE = "https://api.muapi.ai/api/v1"
H = {"x-api-key": "proxy-injected", "Content-Type": "application/json"}


def _post(endpoint, payload):
    req = urllib.request.Request(f"{BASE}/{endpoint}", data=json.dumps(payload).encode(), headers=H)
    try:
        return json.load(urllib.request.urlopen(req, timeout=90))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{endpoint}: HTTP {e.code} {e.read().decode()[:300]}")


def _poll(rid, wait=900):
    end = time.time() + wait
    d = {}
    while time.time() < end:
        req = urllib.request.Request(f"{BASE}/predictions/{rid}/result", headers=H)
        d = json.load(urllib.request.urlopen(req, timeout=60))
        if d.get("status") in ("completed", "succeeded", "failed"):
            return d
        time.sleep(5)
    raise RuntimeError(f"timed out waiting for {rid}")


def run(endpoint, payload):
    d = _post(endpoint, payload)
    rid = d.get("request_id") or d.get("id")
    res = _poll(rid) if rid else d
    if res.get("status") == "failed":
        raise RuntimeError(f"{endpoint} failed: {res.get('error')}")
    cost = (res.get("cost") or {}).get("amount_usd")
    outs = res.get("outputs") or [res.get("output") or res.get("url")]
    print(f"[{endpoint}] cost ${cost} -> {outs[0]}", flush=True)
    return outs[0], cost


def download(url, path):
    with urllib.request.urlopen(url, timeout=300) as r, open(path, "wb") as f:
        f.write(r.read())


def image(prompt, out, refs=None):
    if refs:
        url, cost = run("nano-banana-2-edit", {"prompt": prompt, "images_list": refs, "aspect_ratio": "9:16"})
    else:
        url, cost = run("nano-banana-2", {"prompt": prompt, "aspect_ratio": "9:16"})
    download(url, out)
    return url, cost


def video(image_url, prompt, out, model="veo3.1-fast-image-to-video", extra=None):
    payload = {"image_url": image_url, "prompt": prompt, "aspect_ratio": "9:16"}
    payload.update(extra or {})
    url, cost = run(model, payload)
    download(url, out)
    return url, cost


if __name__ == "__main__":
    a = sys.argv[1:]
    refs = [a[i + 1] for i, x in enumerate(a) if x == "--ref"]
    model = next((a[i + 1] for i, x in enumerate(a) if x == "--model"), "veo3.1-fast-image-to-video")
    if a[0] == "image":
        image(a[1], a[2], refs or None)
    elif a[0] == "video":
        video(a[1], a[2], a[3], model)
