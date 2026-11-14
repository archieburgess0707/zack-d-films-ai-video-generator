"""Part 1 of "Dave Finds Out": Blender frames + 2D overlays (see out/dave_common/overlays.py)."""
import importlib.util
import os

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("dave_overlays", os.path.join(_here, "..", "dave_common", "overlays.py"))
_m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m)
SHOTS = _m.make_shots(_here, 1)
