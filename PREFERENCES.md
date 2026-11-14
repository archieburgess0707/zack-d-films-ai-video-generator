# Channel preferences (for future sessions)

- **Style:** whiteboard doodle (`scripts/whiteboard.py`, example: `out/no_moon_whiteboard/`). Use `"font"` = Comic Neue and `"caption_style": "ink"` in beats.json (`apt-get install fonts-comic-neue`).
- **Voice:** Kokoro `af_heart`, speed 1.15, pitch 1.03 (defaults in `scripts/free_voice.py`).
- **No paid services:** everything is made free/locally (no MuAPI credit).
- **Don't make:** "Which dispenser would you choose?" style videos.
- **Length test running:** bees video kept under 60s vs Moon video over 60s; ask which got more views.
- **Blender (experimental 3D):** `apt-get install blender libegl1 libegl-mesa0 libgl1-mesa-dri libgbm1`; test scene `blender/test_earth_moon.py` (`EGL_PLATFORM=surfaceless blender -b -P ... -- out_prefix 60 --eevee`). ~5 s/frame on 4 CPUs, no GPU.

## Posted to TikTok
- What if you stopped sleeping? (`out/no_sleep`)
- What if the internet shut down? (`out/internet_shutdown`)
- What if Earth stopped spinning? (`out/earth_stops_spinning`)
- Early results (first 3 videos): ~30 likes total, 0 followers.

## Ready, not yet posted
- Hole through the Earth — 3D Blender (`out/hole_through_earth`) — recommended next
- Moon — whiteboard (`out/no_moon_whiteboard`) and cartoon (`out/no_moon`)
- Bees — under 60s length test (`out/no_bees`)
- No wheels (`out/no_wheels`)

## Setup
- Cloud environment **zack-d-films-ai-video-generator** installs Blender, Mesa EGL, Comic Neue and Kokoro on start.
  Voice models live in `/opt/kokoro` → `python3 scripts/free_voice.py out/<project> --models /opt/kokoro`.
- MuAPI key is saved on the Default environment only; account balance was $0 (user doesn't want to pay).
- Next direction (user's idea): AI "fruit drama" style storylines made with an AI video app (Kling / Dreamina) — Claude writes scripts, character sheets and shot prompts; user generates clips and edits in CapCut. Label AI content on TikTok.
- 3D Blender "Dave Finds Out" story: Parts 1–2 finished, Part 3 stopped — user felt the visuals weren't good enough. Upgraded look test: `blender/style_v2.py`.
