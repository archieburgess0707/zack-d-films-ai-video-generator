#!/usr/bin/env bash
# Render every shot of a Blender project to out/<project>/frames/<shot>/ (resumes: skips finished shots).
# Usage: blender/render_all.sh out/hole_through_earth blender/hole_earth.py [fps]
set -u
PROJ=$1; SCENE=$2; FPS=${3:-15}
python3 "$(dirname "$0")/shot_list.py" "$PROJ" | while read -r id dur; do
  dir="$PROJ/frames/$id"
  want=$(python3 -c "print(max(2, round($dur * $FPS)))")
  have=$(ls "$dir" 2>/dev/null | grep -c '^f_.*\.png$')
  if [ "$have" -ge "$want" ]; then echo "skip $id"; continue; fi
  mkdir -p "$dir"
  start=$(date +%s)
  EGL_PLATFORM=surfaceless blender -b -P "$SCENE" -- "$id" "$dur" "$dir" "$FPS" > "$dir.log" 2>&1 || echo "FAIL $id"
  echo "done $id ($want frames, $(( $(date +%s) - start ))s)"
done
echo ALL_DONE
