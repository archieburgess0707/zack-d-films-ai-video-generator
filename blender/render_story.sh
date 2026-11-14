#!/usr/bin/env bash
# Render all three "Dave Finds Out" parts back to back (resumable).
cd "$(dirname "$0")/.."
for n in 1 2 3; do
  echo "=== part $n"
  blender/render_all.sh out/dave_part$n blender/dave_story.py 15
done
echo STORY_DONE
