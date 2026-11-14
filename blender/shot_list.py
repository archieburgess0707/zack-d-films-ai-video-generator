"""Print shot_id and duration (s) for a project, using the same timing as free_render."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import free_render as fr
fr.HERE = os.path.abspath(sys.argv[1])
shots, _, _ = fr.build_timeline()
for s in shots:
    print(s["id"], f"{s['dur']:.3f}")
