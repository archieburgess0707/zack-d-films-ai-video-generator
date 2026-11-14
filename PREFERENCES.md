# Channel preferences (for future sessions)

- **Style:** whiteboard doodle (`scripts/whiteboard.py`, example: `out/no_moon_whiteboard/`). Use `"font"` = Comic Neue and `"caption_style": "ink"` in beats.json (`apt-get install fonts-comic-neue`).
- **Voice:** Kokoro `af_heart`, speed 1.15, pitch 1.03 (defaults in `scripts/free_voice.py`).
- **No paid services:** everything is made free/locally (no MuAPI credit).
- **Don't make:** "Which dispenser would you choose?" style videos.
- **Length test running:** bees video kept under 60s vs Moon video over 60s; ask which got more views.
- **Blender (experimental 3D):** `apt-get install blender libegl1 libegl-mesa0 libgl1-mesa-dri libgbm1`; test scene `blender/test_earth_moon.py` (`EGL_PLATFORM=surfaceless blender -b -P ... -- out_prefix 60 --eevee`). ~5 s/frame on 4 CPUs, no GPU.
