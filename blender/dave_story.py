"""
Blender scenes for the 3-part "Dave Finds Out" story (clay 3D, Eevee).

  EGL_PLATFORM=surfaceless blender -b -P blender/dave_story.py -- <shot_id> <seconds> <out_dir> [fps] [--still]
"""
import math
import random
import sys

import bpy
import mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
SHOT, SECS, OUT = argv[0], float(argv[1]), argv[2]
FPS = int(argv[3]) if len(argv) > 3 and argv[3].isdigit() else 15
STILL = "--still" in argv
NF = max(2, int(round(SECS * FPS)))

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.eevee.taa_render_samples = 16
sc.eevee.use_bloom = True
sc.eevee.bloom_intensity = 0.04
sc.eevee.use_gtao = True
sc.eevee.use_soft_shadows = True
sc.render.resolution_x, sc.render.resolution_y = 720, 1280
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, NF
sc.view_settings.view_transform = "Standard"
sc.view_settings.exposure = -0.2

V = mathutils.Vector
_mats = {}


# --------------------------------------------------------------------------- basics
def mat(col, rough=0.55, emit=0.0, alpha=1.0, spec=0.4):
    k = (tuple(round(c, 3) for c in col), rough, emit, alpha)
    if k in _mats:
        return _mats[k]
    m = bpy.data.materials.new("m")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Specular IOR Level"].default_value = spec
    if emit:
        b.inputs["Emission Color"].default_value = (*col, 1)
        b.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        m.blend_method = "BLEND"
        m.shadow_method = "NONE"
    _mats[k] = m
    return m


def _fin(o, m, smooth=True):
    if smooth:
        for p in o.data.polygons:
            p.use_smooth = True
    o.data.materials.append(m)
    return o


def sphere(loc, r, col, seg=32, scale=None, **mk):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = _fin(bpy.context.object, mat(col, **mk))
    if scale:
        o.scale = scale
    return o


def cyl(loc, r, depth, col, rot=(0, 0, 0), verts=32, **mk):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    return _fin(bpy.context.object, mat(col, **mk))


def cone(loc, r1, r2, depth, col, rot=(0, 0, 0), **mk):
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    return _fin(bpy.context.object, mat(col, **mk))


def box(loc, size, col, bevel=0.05, rot=(0, 0, 0), **mk):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        m = o.modifiers.new("bev", "BEVEL")
        m.width = bevel
        m.segments = 3
    return _fin(o, mat(col, **mk), smooth=bool(bevel))


def torus(loc, R, r, col, rot=(0, 0, 0), **mk):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot)
    return _fin(bpy.context.object, mat(col, **mk))


def empty(loc=(0, 0, 0)):
    bpy.ops.object.empty_add(location=loc)
    return bpy.context.object


def par(child, p):
    child.parent = p
    return child


def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def anim(o, path, fn):
    for f in range(1, NF + 1):
        setattr(o, path, fn((f - 1) / (NF - 1)))
        o.keyframe_insert(path, frame=f)


def tsec(p):
    return p * SECS


def aim(o, look):
    o.rotation_euler = (V(look) - o.location).to_track_quat("-Z", "Y").to_euler()


def camera(loc, look, lens=40, move=None):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.data.lens = lens
    sc.camera = c
    aim(c, look)
    if move:
        a, b = V(loc), V(move)
        for f in range(1, NF + 1):
            p = ease((f - 1) / (NF - 1))
            c.location = a.lerp(b, p)
            aim(c, look)
            c.keyframe_insert("location", frame=f)
            c.keyframe_insert("rotation_euler", frame=f)
    return c


def area(loc, look, energy, size=4, col=(1, 1, 1)):
    bpy.ops.object.light_add(type="AREA", location=loc)
    l = bpy.context.object
    l.data.energy, l.data.size, l.data.color = energy, size, col
    aim(l, look)
    return l


def point(loc, energy, col=(1, 0.8, 0.5), radius=0.2):
    bpy.ops.object.light_add(type="POINT", location=loc)
    l = bpy.context.object
    l.data.energy, l.data.color, l.data.shadow_soft_size = energy, col, radius
    return l


def studio_lights(k=1.0, look=(0, 0, 1)):
    area((-4, -6, 6), look, 1200 * k, 5, (1, 0.95, 0.88))
    area((5, -3, 3), look, 500 * k, 3, (0.7, 0.8, 1))
    area((0, 4, 4), look, 500 * k, 4, (1, 0.9, 0.8))


def world(col, s=1.0):
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*col, 1)
    bg.inputs["Strength"].default_value = s


# --------------------------------------------------------------------------- characters
SKIN = (0.95, 0.68, 0.52)
CAST = {
    "dave": dict(top=(0.12, 0.38, 0.9), hair=(0.28, 0.17, 0.09), legs=(0.1, 0.1, 0.2), s=1.0, w=1.0),
    "brad": dict(top=(0.85, 0.15, 0.15), hair=(0.95, 0.78, 0.35), legs=(0.15, 0.15, 0.2), s=1.15, w=1.3),
    "chloe": dict(top=(0.95, 0.35, 0.6), hair=(0.55, 0.18, 0.08), legs=SKIN, s=0.95, w=0.9),
}
ARM_POSES = {  # (rx, ry) per arm; ry is mirrored per side
    "down": ((0, 0.12), (0, 0.12)), "up": ((0, 2.7), (0, 2.7)), "out": ((0, 1.5), (0, 1.5)),
    "phone": ((0, 0.12), (-1.25, 0.35)), "phone2": ((-1.25, 0.35), (-1.25, 0.35)),
    "hug": ((-1.35, 0.45), (-1.35, 0.45)), "point": ((0, 0.12), (-1.55, 0.0)),
    "hips": ((0, 0.75), (0, 0.75)), "behind": ((0.6, 0.2), (0.6, 0.2)), "magnify": ((0, 0.12), (-1.3, -0.1)),
    "shrug": ((0, 1.0), (0, 1.0)), "box": ((-1.45, 0.25), (-1.45, 0.25)),
}


class Person:
    def __init__(self, who, loc=(0, 0, 0), rz=0.0, arms="down", expr="smile"):
        c = CAST[who]
        self.who, s, w = who, c["s"], c["w"]
        self.s = s
        self.root = empty((0, 0, 0))
        R = self.root
        if who == "chloe":
            par(cone((0, 0, 0.9 * s), 0.46 * s, 0.2 * s, 0.85 * s, c["top"]), R)
            par(sphere((0, 0, 1.3 * s), 0.25 * s, c["top"], scale=(1.1, 0.9, 0.9)), R)
        else:
            par(cyl((0, 0, 0.95 * s), 0.3 * s * w, 0.75 * s, c["top"]), R)
            for z in (0.58, 1.32):
                par(sphere((0, 0, z * s), 0.3 * s * w, c["top"], scale=(1, 1, 0.55)), R)
        hz = 1.78 * s
        self.head = par(empty((0, 0, hz)), R)
        H = self.head
        par(sphere((0, 0, 0), 0.34 * s, SKIN, seg=48, rough=0.45, scale=(1.0, 1.0, 1.08 if who == "brad" else 1.0)), H)
        hair = c["hair"]
        par(sphere((0, 0.03 * s, 0.1 * s), 0.355 * s, hair, seg=48, scale=(1, 1, 0.78), rough=0.7), H)
        if who == "brad":
            par(sphere((0, -0.2 * s, 0.32 * s), 0.16 * s, hair, scale=(1.4, 1, 0.6), rough=0.7), H)
        if who == "chloe":
            par(sphere((0, 0.14 * s, -0.25 * s), 0.36 * s, hair, scale=(1.05, 0.75, 1.5), rough=0.7), H)
            par(sphere((0, -0.22 * s, 0.2 * s), 0.2 * s, hair, scale=(1.6, 0.6, 0.45), rough=0.7), H)
            for ex in (-0.2, 0.2):
                par(sphere((ex * s, -0.26 * s, -0.1 * s), 0.06 * s, (1.0, 0.55, 0.6), scale=(1, 0.5, 0.7)), H)
        # eyes
        self.pupils = []
        for ex in (-0.12, 0.12):
            par(sphere((ex * s, -0.29 * s, 0.03 * s), 0.075 * s, (1, 1, 1), rough=0.2), H)
            self.pupils.append(par(sphere((ex * s, -0.355 * s, 0.03 * s), 0.038 * s, (0.03, 0.03, 0.03), rough=0.2), H))
            if who == "chloe":
                for k in (-1, 0, 1):
                    par(cyl(((ex + k * 0.03) * s, -0.33 * s, 0.11 * s), 0.008 * s, 0.06 * s, (0.05, 0.05, 0.05),
                            rot=(0.3, k * 0.4, 0)), H)
        self.brows = [par(cyl((ex * s, -0.32 * s, 0.15 * s), 0.018 * s, 0.13 * s, (0.15, 0.09, 0.05) if who != "brad" else (0.6, 0.45, 0.15),
                              rot=(0, math.pi / 2, 0)), H) for ex in (-0.12, 0.12)]
        self.mouth_parts = []
        self.expr(expr)
        # arms
        self.arms = []
        for side in (-1, 1):
            piv = par(empty((side * (0.33 * w if who != "chloe" else 0.3) * s, 0, 1.3 * s)), R)
            par(cyl((0, 0, -0.3 * s), 0.085 * s, 0.56 * s, c["top"] if who != "chloe" else SKIN), piv)
            par(sphere((0, 0, -0.6 * s), 0.1 * s, SKIN, rough=0.45), piv)
            self.arms.append(piv)
        self.pose(arms)
        # legs
        self.legs = []
        for side in (-1, 1):
            piv = par(empty((side * 0.13 * s, 0, 0.62 * s)), R)
            par(cyl((0, 0, -0.3 * s), 0.1 * s, 0.6 * s, c["legs"]), piv)
            par(sphere((0, -0.06 * s, -0.6 * s), 0.12 * s, (0.95, 0.95, 0.95) if who != "chloe" else (0.9, 0.2, 0.3),
                       scale=(1, 1.4, 0.6)), piv)
            self.legs.append(piv)
        R.location = loc
        R.rotation_euler = (0, 0, rz)

    def expr(self, e):
        for o in self.mouth_parts:
            bpy.data.objects.remove(o)
        s, H = self.s, self.head
        mp = []
        if e in ("smile", "grin", "giggle"):
            mp.append(par(sphere((0, -0.31 * s, -0.15 * s), 0.09 * s, (0.45, 0.08, 0.1), scale=(1.4, 0.5, 0.55 if e == "smile" else 0.8)), H))
            if e != "smile":
                mp.append(par(sphere((0, -0.335 * s, -0.12 * s), 0.07 * s, (1, 1, 1), scale=(1.5, 0.4, 0.35)), H))
        elif e == "shock":
            mp.append(par(sphere((0, -0.31 * s, -0.16 * s), 0.08 * s, (0.4, 0.06, 0.08), scale=(0.9, 0.5, 1.2)), H))
        elif e in ("angry", "frown", "sad"):
            mp.append(par(sphere((0, -0.31 * s, -0.17 * s), 0.08 * s, (0.4, 0.06, 0.08), scale=(1.3, 0.5, 0.3)), H))
        else:
            mp.append(par(sphere((0, -0.31 * s, -0.15 * s), 0.06 * s, (0.4, 0.06, 0.08), scale=(1.3, 0.5, 0.3)), H))
        self.mouth_parts = mp
        tilt = {"angry": 0.35, "sad": -0.35, "shock": 0.0, "giggle": -0.15}.get(e, 0.0)
        lift = 0.06 if e in ("shock", "sad") else (-0.02 if e == "angry" else 0.0)
        for k, b in enumerate(self.brows):
            side = -1 if k == 0 else 1
            b.rotation_euler = (0, math.pi / 2 - side * tilt, 0)
            b.location.z = (0.15 + lift) * s

    def pose(self, name):
        for k, piv in enumerate(self.arms):
            side = -1 if k == 0 else 1
            rx, ry = ARM_POSES[name][k]
            piv.rotation_euler = (rx, side * ry, 0)

    def walk(self, speed=1.0, dist=(0, 0, 0), t0=0.0, t1=1.0):
        start = V(self.root.location)
        d = V(dist)
        for f in range(1, NF + 1):
            p = (f - 1) / (NF - 1)
            q = max(0.0, min(1.0, (p - t0) / max(1e-3, t1 - t0)))
            moving = t0 <= p <= t1
            ph = tsec(p) * 9 * speed
            self.root.location = start + d * q + V((0, 0, 0.04 * abs(math.sin(ph)) if moving else 0))
            self.root.keyframe_insert("location", frame=f)
            for k, leg in enumerate(self.legs):
                leg.rotation_euler = ((0.45 * math.sin(ph + k * math.pi)) if moving else 0, 0, 0)
                leg.keyframe_insert("rotation_euler", frame=f)

    def bob_head(self, amp=0.12, freq=6.0, axis=1):
        for f in range(1, NF + 1):
            r = [0, 0, 0]
            r[axis] = amp * math.sin(tsec((f - 1) / (NF - 1)) * freq)
            self.head.rotation_euler = r
            self.head.keyframe_insert("rotation_euler", frame=f)

    def wave(self, k=1):
        piv = self.arms[k]
        side = -1 if k == 0 else 1
        for f in range(1, NF + 1):
            piv.rotation_euler = (0, side * (2.4 + 0.35 * math.sin(tsec((f - 1) / (NF - 1)) * 9)), 0)
            piv.keyframe_insert("rotation_euler", frame=f)

    def look(self, dx):
        for p in self.pupils:
            p.location.x += dx * self.s

    def hand(self, k=1):
        return self.arms[k]

    def sit(self, seat_h=0.5):
        self.root.location.z = seat_h - 0.62 * self.s
        for leg in self.legs:
            leg.rotation_euler = (-1.45, 0, 0)

    def kneel(self):
        self.root.location.z -= 0.28 * self.s
        self.legs[0].rotation_euler = (-1.5, 0, 0)
        self.legs[1].rotation_euler = (1.2, 0, 0)


def held(person, obj_fn, k=1):
    """Attach an object (built at the origin) to a hand."""
    o = obj_fn()
    o.parent = person.arms[k]
    o.location = (0, -0.06 * person.s, -0.66 * person.s)
    return o


# --------------------------------------------------------------------------- props
def phone(glow=1.5):
    root = empty()
    par(box((0, 0, 0), (0.17, 0.03, 0.3), (0.05, 0.05, 0.07), bevel=0.02), root)
    par(box((0, -0.017, 0), (0.15, 0.005, 0.27), (0.5, 0.75, 1.0), bevel=0.0, emit=glow), root)
    root.rotation_euler = (math.radians(70), 0, 0)
    return root


def moustache(person):
    s = person.s
    m = empty((0, -0.33 * s, -0.07 * s))
    par(m, person.head)
    for side in (-1, 1):
        par(sphere((side * 0.07 * s, 0, 0), 0.06 * s, (0.15, 0.08, 0.04), scale=(1.6, 0.6, 0.6), rough=0.8), m)
    return m


def det_hat(person, col=(0.45, 0.32, 0.18)):
    s = person.s
    h = empty((0, 0, 0.26 * s))
    par(h, person.head)
    par(cyl((0, 0, 0), 0.5 * s, 0.03 * s, col), h)
    par(cyl((0, 0, 0.14 * s), 0.3 * s, 0.28 * s, col), h)
    par(cyl((0, 0, 0.05 * s), 0.305 * s, 0.06 * s, (0.12, 0.08, 0.05)), h)
    return h


def sunglasses(person):
    s = person.s
    g = empty((0, -0.36 * s, 0.03 * s))
    par(g, person.head)
    for ex in (-0.13, 0.13):
        par(cyl((ex * s, 0, 0), 0.1 * s, 0.03 * s, (0.02, 0.02, 0.02), rot=(math.pi / 2, 0, 0), rough=0.1), g)
    par(box((0, 0, 0.03 * s), (0.12 * s, 0.02 * s, 0.025 * s), (0.02, 0.02, 0.02), bevel=0), g)
    return g


def magnifier():
    root = empty()
    par(torus((0, 0, 0.2), 0.16, 0.025, (0.75, 0.6, 0.2), rot=(math.pi / 2, 0, 0), rough=0.3), root)
    par(cyl((0, 0, 0.2), 0.15, 0.01, (0.8, 0.9, 1.0), rot=(math.pi / 2, 0, 0), alpha=0.35, rough=0.05), root)
    par(cyl((0, 0, -0.05), 0.03, 0.3, (0.35, 0.2, 0.1)), root)
    return root


def tear(person, side=1, t0=0.0):
    s = person.s
    d = sphere((0, 0, 0), 0.04 * s, (0.5, 0.8, 1.0), alpha=0.85, rough=0.05)
    par(d, person.head)
    anim(d, "location", lambda p: (side * 0.14 * s, -0.33 * s, 0.0 - ((tsec(p) * 0.5 + t0) % 1.0) * 0.4 * s))
    return d


def pizza_hat(person):
    s = person.s
    h = empty((0, 0, 0.24 * s))
    par(h, person.head)
    par(sphere((0, 0, 0), 0.37 * s, (0.85, 0.12, 0.1), scale=(1, 1, 0.5)), h)
    par(cyl((0, -0.32 * s, -0.02 * s), 0.2 * s, 0.03 * s, (0.85, 0.12, 0.1), rot=(0.2, 0, 0)), h)
    return h


def pizza(loc=(0, 0, 0), r=0.5, bye=False):
    root = empty(loc)
    par(cyl((0, 0, 0), r, 0.06, (0.85, 0.55, 0.2)), root)
    par(cyl((0, 0, 0.03), r * 0.88, 0.02, (1.0, 0.8, 0.3)), root)
    random.seed(3)
    if not bye:
        for _ in range(9):
            a, d = random.uniform(0, 6.28), random.uniform(0, r * 0.7)
            par(cyl((math.cos(a) * d, math.sin(a) * d, 0.05), r * 0.11, 0.02, (0.75, 0.12, 0.08)), root)
    return root


def pizza_box(loc, open_=True):
    root = empty(loc)
    par(box((0, 0, 0), (1.1, 1.1, 0.12), (0.85, 0.75, 0.6), bevel=0.01), root)
    if open_:
        lid = par(box((0, 0.55, 0.55), (1.1, 0.04, 1.1), (0.85, 0.75, 0.6), bevel=0.01), root)
    return root


def ring_box(loc, open_p=None):
    root = empty(loc)
    par(box((0, 0, 0), (0.16, 0.16, 0.1), (0.75, 0.05, 0.12), bevel=0.02, rough=0.4), root)
    hinge = par(empty((0, 0.08, 0.05)), root)
    par(box((0, -0.08, 0.03), (0.16, 0.16, 0.06), (0.75, 0.05, 0.12), bevel=0.02, rough=0.4), hinge)
    if open_p:
        anim(hinge, "rotation_euler", lambda p: (-1.9 * ease((p - open_p) / 0.12) if p > open_p else 0, 0, 0))
    return root


def confetti(center, t_start, n=60, spread=2.2):
    random.seed(11)
    cols = [(1, 0.2, 0.3), (1, 0.85, 0.1), (0.2, 0.6, 1), (0.3, 0.9, 0.4), (1, 0.5, 0.1), (0.8, 0.3, 1)]
    for _ in range(n):
        c = box(center, (0.06, 0.01, 0.04), random.choice(cols), bevel=0, emit=0.3)
        v = V((random.uniform(-1, 1), random.uniform(-1, 0.4), random.uniform(0.6, 1.6))) * spread
        spin = random.uniform(5, 15)

        def pos(p, v=v):
            t = max(0.0, tsec(p) - t_start)
            if tsec(p) < t_start:
                return (center[0], center[1], -50)
            return (center[0] + v.x * t, center[1] + v.y * t, center[2] + v.z * t - 2.5 * t * t)
        anim(c, "location", pos)
        anim(c, "rotation_euler", lambda p, spin=spin: (tsec(p) * spin, tsec(p) * spin * 0.7, 0))


def plant(loc, s=1.0):
    cyl((loc[0], loc[1], 0.3 * s), 0.3 * s, 0.6 * s, (0.75, 0.4, 0.25))
    for k in range(7):
        a = k * 0.9
        sphere((loc[0] + math.cos(a) * 0.25 * s, loc[1] + math.sin(a) * 0.25 * s, (0.9 + 0.25 * (k % 3)) * s),
               0.35 * s, (0.2, 0.6, 0.25), scale=(1, 1, 1.3))


def tree(loc, s=1.0):
    cyl((loc[0], loc[1], 1.0 * s), 0.18 * s, 2.0 * s, (0.4, 0.25, 0.12), rough=0.8)
    for dx, dy, dz, r in ((0, 0, 2.6, 1.0), (-0.6, 0.2, 2.2, 0.7), (0.6, -0.1, 2.3, 0.75)):
        sphere((loc[0] + dx * s, loc[1] + dy * s, dz * s), r * s, (0.22, 0.62, 0.25), rough=0.7)


def table(loc, r=0.5, cloth=None, h=0.75):
    cyl((loc[0], loc[1], h / 2), 0.05, h, (0.25, 0.2, 0.18))
    cyl((loc[0], loc[1], h), r, 0.05, cloth or (0.55, 0.35, 0.2))
    if cloth:
        cyl((loc[0], loc[1], h - 0.15), r * 1.02, 0.3, cloth)


def chair(loc, rz=0.0, col=(0.55, 0.35, 0.2)):
    root = empty(loc)
    par(box((0, 0, 0.45), (0.45, 0.45, 0.06), col, bevel=0.02), root)
    par(box((0, 0.2, 0.75), (0.45, 0.06, 0.6), col, bevel=0.02), root)
    for x in (-0.18, 0.18):
        for y in (-0.18, 0.18):
            par(cyl((x, y, 0.22), 0.025, 0.45, (0.25, 0.2, 0.18)), root)
    root.rotation_euler = (0, 0, rz)
    return root


def candle(loc):
    cyl((loc[0], loc[1], loc[2] + 0.1), 0.03, 0.2, (0.95, 0.92, 0.85))
    sphere((loc[0], loc[1], loc[2] + 0.24), 0.03, (1.0, 0.75, 0.3), emit=8, scale=(1, 1, 1.6))
    point((loc[0], loc[1], loc[2] + 0.35), 15, (1, 0.7, 0.4))


# --------------------------------------------------------------------------- sets
def floor(col, r=25):
    cyl((0, 0, -0.02), r, 0.04, col, verts=64, rough=0.7)


def wall(y, col, w=30, h=8):
    box((0, y, h / 2), (w, 0.2, h), col, bevel=0)


def living_room(night=False):
    world((0.02, 0.02, 0.05) if night else (0.5, 0.6, 0.75), 0.35 if not night else 0.4)
    floor((0.5, 0.32, 0.18))
    wall(3.0, (0.85, 0.72, 0.55) if not night else (0.35, 0.3, 0.38))
    box((2.6, 2.85, 2.6), (1.8, 0.1, 1.6), (0.25, 0.35, 0.6) if night else (0.65, 0.85, 1.0), bevel=0, emit=0.35 if not night else 0.3)
    for dx in (-0.95, 0.95):
        box((2.6 + dx, 2.8, 2.6), (0.1, 0.12, 1.8), (0.95, 0.95, 0.95), bevel=0)
    # sofa
    box((0, 1.6, 0.35), (3.2, 1.1, 0.5), (0.85, 0.3, 0.2), bevel=0.12)
    box((0, 2.1, 0.9), (3.2, 0.35, 1.0), (0.8, 0.27, 0.18), bevel=0.12)
    for x in (-1.65, 1.65):
        box((x, 1.6, 0.6), (0.35, 1.1, 0.8), (0.8, 0.27, 0.18), bevel=0.12)
    cyl((0, -0.6, 0.02), 2.2, 0.02, (0.9, 0.85, 0.7))
    plant((-2.8, 2.2, 0), 0.9)
    cyl((2.6, 1.9, 0.75), 0.04, 1.5, (0.2, 0.2, 0.2))
    cone((2.6, 1.9, 1.55), 0.35, 0.2, 0.4, (1.0, 0.92, 0.75), emit=1.5 if night else 0.3)
    if night:
        point((2.6, 1.9, 1.4), 60, (1, 0.8, 0.5))
        area((-3, -5, 5), (0, 1, 1), 250, 5, (0.5, 0.6, 1.0))
    else:
        studio_lights(0.5, (0, 1.5, 1))


def cafe_exterior():
    world((0.45, 0.65, 0.95), 0.35)
    floor((0.62, 0.6, 0.58))
    box((0, 3.2, 3), (14, 0.4, 6), (0.95, 0.88, 0.75), bevel=0)
    for x in (-3.2, 3.2):
        box((x, 2.95, 1.8), (2.6, 0.1, 2.2), (1.0, 0.85, 0.55), bevel=0, emit=0.35)
    box((0, 2.95, 1.3), (1.4, 0.15, 2.6), (0.35, 0.2, 0.12), bevel=0.02)
    for k in range(10):
        box((-6.3 + k * 1.4, 2.4, 3.4), (1.4, 1.2, 0.08), (0.85, 0.15, 0.15) if k % 2 else (0.98, 0.98, 0.98),
            bevel=0, rot=(-0.35, 0, 0))
    box((0, 3.0, 4.4), (3.2, 0.1, 0.8), (0.2, 0.35, 0.25), bevel=0.02)
    table((-3.6, 1.2, 0), 0.45)
    chair((-4.3, 1.2, 0), math.pi / 2)
    table((3.8, 1.0, 0), 0.45)
    chair((4.5, 1.0, 0), -math.pi / 2)
    plant((-1.6, 2.4, 0), 0.7)
    plant((1.6, 2.4, 0), 0.7)
    studio_lights(0.55, (0, 1.5, 1))


def lamp_post(loc):
    cyl((loc[0], loc[1], 1.8), 0.07, 3.6, (0.15, 0.15, 0.18), rough=0.3)
    sphere((loc[0], loc[1], 3.7), 0.22, (1.0, 0.9, 0.6), emit=2)


def cafe_interior():
    world((0.3, 0.25, 0.2), 0.5)
    floor((0.42, 0.27, 0.16))
    wall(3.5, (0.3, 0.5, 0.4))
    box((-4.5, 0, 4), (0.2, 14, 8), (0.3, 0.5, 0.4), bevel=0)
    box((2.2, 2.6, 0.55), (3.5, 0.8, 1.1), (0.55, 0.32, 0.18), bevel=0.05)
    box((2.2, 2.6, 1.13), (3.6, 0.9, 0.06), (0.9, 0.88, 0.85), bevel=0.02)
    for x in (-2.2, 0.6):
        cyl((x, 0.5, 3.4), 0.01, 1.2, (0.1, 0.1, 0.1))
        cone((x, 0.5, 2.7), 0.35, 0.05, 0.3, (0.15, 0.4, 0.3))
        sphere((x, 0.5, 2.55), 0.1, (1, 0.85, 0.5), emit=5)
        point((x, 0.5, 2.4), 120, (1, 0.8, 0.5))
    studio_lights(0.6, (0, 1, 1))


def park():
    world((0.45, 0.65, 0.95), 0.35)
    floor((0.3, 0.62, 0.28))
    box((0, 0, 0.005), (2.2, 40, 0.02), (0.85, 0.78, 0.6), bevel=0)
    for x, y, s in ((-4, 6, 1.3), (4.5, 7, 1.5), (-6, 12, 1.2), (6, 2, 1.0)):
        tree((x, y, 0), s)
    studio_lights(0.55, (0, 0, 1))


def bush(loc, s=1.0):
    root = empty(loc)
    random.seed(7)
    for k in range(14):
        a, z = k * 2.4, random.uniform(0.3, 1.6)
        r = random.uniform(0.35, 0.5)
        par(sphere((math.cos(a) * 0.5 * s, math.sin(a) * 0.45 * s, z * s), r * s,
                   (0.18 + random.uniform(-0.04, 0.04), 0.55, 0.22), rough=0.8), root)
    return root


def bench(loc, rz=0.0):
    root = empty(loc)
    par(box((0, 0, 0.45), (1.8, 0.5, 0.08), (0.55, 0.35, 0.2), bevel=0.02), root)
    par(box((0, 0.22, 0.8), (1.8, 0.06, 0.5), (0.55, 0.35, 0.2), bevel=0.02), root)
    for x in (-0.8, 0.8):
        par(box((x, 0, 0.22), (0.08, 0.5, 0.45), (0.15, 0.15, 0.15), bevel=0.01), root)
    root.rotation_euler = (0, 0, rz)
    return root


def restaurant():
    world((0.05, 0.02, 0.02), 0.5)
    floor((0.3, 0.12, 0.1))
    wall(3.5, (0.45, 0.08, 0.1))
    for x in (-3, 3):
        box((x, 3.35, 2.4), (1.4, 0.1, 2.0), (0.9, 0.75, 0.4), bevel=0, emit=0.3)
    for x, y in ((-3.5, 1.5), (3.6, 1.2)):
        table((x, y, 0), 0.55, cloth=(0.95, 0.95, 0.93))
        candle((x, y, 0.78))
    table((0, 0.4, 0), 0.6, cloth=(0.95, 0.95, 0.93))
    candle((0.25, 0.5, 0.78))
    for k in range(3):
        sphere((-1.5 + k * 1.5, 1.0, 3.6), 0.15, (1, 0.85, 0.5), emit=6)
        point((-1.5 + k * 1.5, 1.0, 3.4), 180, (1, 0.75, 0.45))
    area((-3, -6, 5), (0, 0.5, 1), 500, 5, (1, 0.85, 0.7))


def front_door(open_at=None):
    world((0.02, 0.02, 0.06), 0.4)
    floor((0.45, 0.35, 0.28))
    for x0, x1 in ((-15, -0.72), (0.72, 15)):
        box(((x0 + x1) / 2, 0.2, 3), (x1 - x0, 0.2, 6), (0.85, 0.78, 0.65), bevel=0)
    box((0, 0.2, 4.3), (1.44, 0.2, 3.4), (0.85, 0.78, 0.65), bevel=0)
    point((0, 2.5, 2.5), 120, (1, 0.85, 0.65))
    root = empty((-0.7, 0.05, 0))
    par(box((0.7, 0, 1.25), (1.4, 0.12, 2.5), (0.55, 0.2, 0.12), bevel=0.02), root)
    par(sphere((1.2, -0.1, 1.2), 0.07, (0.95, 0.8, 0.3), rough=0.2), root)
    for x in (-0.8, 0.8):
        box((x, 0.1, 1.3), (0.15, 0.3, 2.7), (0.95, 0.95, 0.92), bevel=0.01)
    box((0, 0.1, 2.68), (1.75, 0.3, 0.15), (0.95, 0.95, 0.92), bevel=0.01)
    if open_at is not None:
        anim(root, "rotation_euler", lambda p: (0, 0, 1.7 * ease((p - open_at) / 0.2) if p > open_at else 0))
    point((0, -1.2, 2.8), 150, (1, 0.8, 0.5))
    area((-2, -6, 4), (0, 0, 1), 300, 4, (0.7, 0.75, 1.0))
    return root


def title_set(col=(0.95, 0.75, 0.3)):
    world(col, 0.45)
    floor(col)
    studio_lights(0.6)


# --------------------------------------------------------------------------- shots
def build(shot):
    S = shot
    if S == "outro":
        import re
        m = re.search(r"dave_part(\d)", OUT)
        S = f"outro_p{m.group(1) if m else 1}"
    # ------------------------------------------------ part 1
    if S == "p1_b1_a":
        living_room()
        d = Person("dave", (-0.55, 1.35, 0), 0, "down", "smile")
        c = Person("chloe", (0.55, 1.35, 0), 0, "down", "smile")
        d.sit(0.6)
        c.sit(0.6)
        d.root.rotation_euler = (0, 0, -0.25)
        c.root.rotation_euler = (0, 0, 0.25)
        camera((0, -6.5, 2.0), (0, 1.2, 1.3), 40, move=(0, -5.6, 1.9))
    elif S == "p1_b1_b":
        living_room()
        c = Person("chloe", (0, 1.0, 0.0), 0, "down", "grin")
        c.wave(1)
        camera((0, -2.6, 1.85), (0, 1.0, 1.55), 45)
    elif S == "p1_b2_a":
        living_room()
        d = Person("dave", (-0.9, 1.35, 0), 0.35, "down", "neutral")
        d.sit(0.6)
        d.look(0.04)
        c = Person("chloe", (0.9, 1.35, 0), -2.2, "phone", "giggle")
        c.sit(0.6)
        held(c, phone)
        c.bob_head(0.1, 10, 1)
        camera((-0.4, -5.6, 2.0), (0, 1.1, 1.3), 40)
    elif S == "p1_b3_a":
        living_room()
        c = Person("chloe", (0, 1.0, 0.0), 0.3, "phone", "giggle")
        held(c, phone)
        c.bob_head(0.12, 12, 1)
        camera((0.3, -2.4, 1.8), (0, 1.0, 1.5), 45)
    elif S == "p1_b4_a":
        living_room()
        d = Person("dave", (0, 1.0, 0.0), 0, "down", "frown")
        d.expr("angry")
        anim(d.root, "rotation_euler", lambda p: (-0.25 * ease(p / 0.4), 0, 0))
        camera((0, -2.6, 1.8), (0, 1.0, 1.55), 45, move=(0, -2.2, 1.75))
    elif S == "p1_b5_a":
        living_room()
        c = Person("chloe", (0, 1.0, 0.0), 0, "behind", "grin")
        held(c, phone, 1)
        c.look(0.04)
        camera((0, -2.8, 1.6), (0, 1.0, 1.3), 42)
    elif S == "p1_b6_a":
        living_room(night=True)
        table((0, -0.3, 0), 0.5)
        ph = phone(1.4)
        ph.location = (0, -0.35, 0.8)
        ph.rotation_euler = (0, 0, 0.3)
        anim(ph, "location", lambda p: (0.01 * math.sin(tsec(p) * 60) if 0.3 < p < 0.6 else 0, -0.35, 0.8))
        point((0, -0.4, 1.1), 12, (0.6, 0.8, 1.0))
        camera((0.6, -2.2, 1.7), (0, -0.35, 0.8), 40)
    elif S == "p1_b7_a":
        living_room(night=True)
        d = Person("dave", (0, 1.0, 0.0), 0, "phone", "shock")
        held(d, lambda: phone(1.2))
        point((0, 0.2, 1.5), 14, (0.5, 0.75, 1.0))
        camera((0, -2.4, 1.85), (0, 1.0, 1.65), 48, move=(0, -1.9, 1.8))
    elif S == "p1_b8_a":
        title_set((0.25, 0.22, 0.35))
        d = Person("dave", (0, 0.5, 0), 0, "magnify", "angry")
        det_hat(d)
        moustache(d)
        held(d, magnifier)
        anim(d.root, "rotation_euler", lambda p: (0, 0, 0.3 * math.sin(tsec(p) * 2)))
        point((1.5, -1.5, 3), 200, (1, 0.85, 0.5))
        camera((0, -4.4, 1.7), (0, 0.5, 1.3), 40, move=(0, -3.8, 1.6))
    elif S == "p1_b9_a":
        cafe_exterior()
        c = Person("chloe", (-0.35, 1.2, 0), math.pi / 2 - 0.2, "hug", "grin")
        b = Person("brad", (0.4, 1.2, 0), -math.pi / 2 + 0.2, "hug", "grin")
        camera((0, -6.0, 2.2), (0, 1.2, 1.4), 38, move=(0, -5.0, 2.0))
    elif S == "p1_b9_b":
        cafe_exterior()
        lamp_post((-1.3, -1.0))
        d = Person("dave", (-1.55, -0.65, 0), -0.6, "down", "angry")
        moustache(d)
        det_hat(d)
        Person("chloe", (2.6, 1.6, 0), math.pi / 2 - 0.2, "hug", "grin")
        Person("brad", (3.35, 1.6, 0), -math.pi / 2 + 0.2, "hug", "grin")
        anim(d.root, "location", lambda p: (-1.55 + 0.2 * ease(p / 0.4), -0.65, 0))
        camera((-3.2, -4.0, 1.9), (0.5, 0.8, 1.3), 38)
    elif S == "p1_b10_a":
        cafe_exterior()
        d = Person("dave", (0, -0.2, 0), 0, "hips", "angry")
        det_hat(d)
        m = moustache(d)
        anim(m, "location", lambda p: (0, -0.33 - 0.2 * ease((p - 0.5) / 0.3), -0.07 - 1.6 * ease((p - 0.5) / 0.3) ** 2))
        camera((0, -2.5, 1.85), (0, -0.2, 1.6), 45, move=(0, -2.1, 1.8))
    elif S in ("p1_b11_a", "p2_b12_a"):
        title_set((0.95, 0.6, 0.2) if S.startswith("p1") else (0.3, 0.6, 0.95))
        d = Person("dave", (0, 0.5, 0), 0.2, "hips", "angry")
        det_hat(d)
        sunglasses(d)
        camera((0, -4.2, 1.5), (0, 0.5, 1.2), 40)
    elif S in ("outro_p1", "outro_p2", "outro_p3"):
        title_set({"outro_p1": (0.95, 0.6, 0.2), "outro_p2": (0.3, 0.6, 0.95), "outro_p3": (0.9, 0.3, 0.45)}[S])
        if S == "outro_p3":
            d = Person("dave", (-0.55, 0.5, 0), 0.25, "down", "grin")
            b = Person("brad", (0.6, 0.5, 0), -0.25, "down", "grin")
            d.wave(0)
            b.wave(1)
            pizza_hat(d)
            pizza_hat(b)
        else:
            d = Person("dave", (0, 0.5, 0), 0, "down", "smile")
            d.wave(1)
        camera((0, -5.2, 1.4), (0, 0.5, 1.1), 40)
    # ------------------------------------------------ part 2
    elif S == "p2_b1_a":
        cafe_exterior()
        Person("chloe", (-0.35, 1.2, 0), math.pi / 2 - 0.2, "hug", "grin")
        Person("brad", (0.4, 1.2, 0), -math.pi / 2 + 0.2, "hug", "grin")
        camera((2.0, -5.0, 2.4), (0, 1.2, 1.3), 38, move=(1.2, -4.5, 2.2))
    elif S == "p2_b2_a":
        park()
        d = Person("dave", (1.6, 0.3, 0), 0, "down", "angry")
        bush((1.6, 0.3, 0), 1.0)
        c = Person("chloe", (-0.3, 5.0, 0), 0, "down", "smile")
        c.walk(1.0, (0, -7.5, 0))
        camera((4.5, -6.5, 2.4), (0.5, 0.5, 1.2), 38)
    elif S in ("p2_b3_a", "p2_b4_a"):
        park()
        d = Person("dave", (0, 0.3, 0), 0, "down", "frown" if S == "p2_b4_a" else "shock")
        bush((0, 0.3, 0), 1.0)
        random.seed(2)
        drops = []
        for k in range(40):
            dr = sphere((0, 0, -50), 0.045, (0.45, 0.75, 1.0), alpha=0.85, rough=0.05)
            x0, y0, ph = random.uniform(-0.8, 0.8), random.uniform(-0.6, 0.6), random.uniform(0, 1)
            if S == "p2_b3_a":
                anim(dr, "location", lambda p, x0=x0, y0=y0, ph=ph: ((x0, y0, 2.6 - ((tsec(p) * 1.3 + ph) % 1.0) * 2.6)
                                                                   if p > 0.3 else (0, 0, -50)))
            else:
                anim(dr, "location", lambda p, x0=x0, y0=y0, ph=ph: (x0 * 0.7, y0 - 0.5, 2.0 - ((tsec(p) * 0.6 + ph) % 1.0) * 2.0))
        if S == "p2_b3_a":
            can = empty((1.4, -0.2, 3.0))
            par(cyl((0, 0, 0), 0.3, 0.5, (0.2, 0.6, 0.35), rot=(0, 1.2, 0)), can)
            par(cyl((-0.45, 0, -0.25), 0.05, 0.6, (0.2, 0.6, 0.35), rot=(0, -0.6, 0)), can)
            anim(can, "location", lambda p: (1.4 + 2.5 * (1 - ease(p / 0.3)), -0.2, 3.0))
            camera((0, -5.5, 2.4), (0, 0.3, 1.4), 40)
        else:
            camera((0, -3.0, 1.9), (0, 0.3, 1.5), 45)
    elif S == "p2_b5_a":
        park()
        bench((0, 0.6, 0))
        d = Person("dave", (0, 0.45, 0), 0, "box", "neutral")
        d.sit(0.5)
        coat = cyl((0, 0.45, 0.82), 0.36, 0.95, (0.65, 0.5, 0.3))
        det_hat(d, (0.2, 0.18, 0.15))
        sunglasses(d)
        paper = box((0, -0.3, 1.45), (0.9, 0.03, 0.65), (0.95, 0.95, 0.9), bevel=0)
        for ex in (-0.12, 0.12):
            cyl((ex, -0.33, 1.6), 0.05, 0.03, (0.05, 0.05, 0.05), rot=(math.pi / 2, 0, 0))
        camera((0.8, -4.2, 1.5), (0, 0.4, 1.2), 40)
    elif S in ("p2_b6_a", "p2_b7_a"):
        park()
        bench((0, 0.6, 0))
        d = Person("dave", (0, 0.45, 0), 0, "down", "shock" if S == "p2_b7_a" else "neutral")
        d.sit(0.5)
        cyl((0, 0.45, 0.82), 0.36, 0.95, (0.65, 0.5, 0.3))
        det_hat(d, (0.2, 0.18, 0.15))
        sunglasses(d)
        bird = empty((0, 0, 0))
        par(sphere((0, 0, 0), 0.16, (0.55, 0.55, 0.6), scale=(1, 1.4, 1)), bird)
        par(sphere((0, -0.18, 0.12), 0.09, (0.45, 0.45, 0.55)), bird)
        par(cone((0, -0.28, 0.12), 0.03, 0.0, 0.08, (0.95, 0.7, 0.2), rot=(math.pi / 2, 0, 0)), bird)
        par(sphere((0.05, -0.24, 0.16), 0.02, (0.05, 0.05, 0.05)), bird)
        top = d.root.location.z + 2.3
        if S == "p2_b6_a":
            anim(bird, "location", lambda p: (2.5 * (1 - ease(p / 0.6)), 0.45, top + 0.16 + 1.5 * (1 - ease(p / 0.6))))
            camera((0.8, -4.2, 1.7), (0, 0.4, 1.5), 40)
        else:
            bird.location = (0, 0.45, top + 0.16)
            anim(bird, "rotation_euler", lambda p: (0, 0, 0.5 * math.sin(tsec(p) * 3)))
            camera((0, -2.6, 1.95), (0, 0.45, 1.85), 45)
    elif S == "p2_b8_a":
        cafe_interior()
        table((0.6, 1.2, 0), 0.5)
        chair((1.3, 1.2, 0), -math.pi / 2)
        c = Person("chloe", (1.3, 1.2, 0), math.pi / 2 + 0.3, "phone", "neutral")
        c.sit(0.48)
        held(c, phone)
        d = Person("dave", (-1.8, 0.3, 0), -0.5, "down", "angry")
        plant((-1.5, -0.1, 0), 1.25)
        camera((-1.0, -5.5, 2.0), (0, 0.8, 1.2), 36)
    elif S == "p2_b9_a":
        cafe_interior()
        c = Person("chloe", (0, 1.0, 0), 0.2, "phone", "frown")
        held(c, phone)
        c.expr("neutral")
        camera((0.3, -2.3, 1.75), (0, 1.0, 1.55), 48, move=(0.2, -2.0, 1.75))
    elif S == "p2_b10_a":
        cafe_interior()
        b = Person("brad", (-3.5, 0.3, 0), math.pi / 2 - 0.3, "phone", "sad")
        held(b, phone)
        tear(b, -1)
        tear(b, 1, 0.5)
        b.walk(0.8, (3.0, 0, 0), 0, 0.8)
        camera((0.5, -5.0, 2.0), (-1.0, 0.3, 1.5), 38)
    elif S == "p2_b11_a":
        cafe_interior()
        b = Person("brad", (0.55, 0.6, 0), -math.pi / 2 + 0.35, "phone", "sad")
        held(b, phone)
        tear(b, -1)
        tear(b, 1, 0.5)
        d = Person("dave", (-0.7, 0.6, 0), math.pi / 2 - 0.35, "down", "shock")
        camera((0, -4.2, 1.9), (0, 0.6, 1.6), 40, move=(0, -3.6, 1.9))
    # ------------------------------------------------ part 3
    elif S == "p3_b1_a":
        living_room()
        c = Person("chloe", (0, 1.0, 0), 0, "phone2", "grin")
        held(c, phone, 0)
        held(c, phone, 1)
        c.bob_head(0.15, 7, 2)
        camera((0, -2.9, 1.7), (0, 1.0, 1.4), 42)
    elif S == "p3_b2_a":
        cafe_interior()
        b = Person("brad", (0, 1.0, 0), 0, "hips", "angry")
        camera((0, -3.0, 2.0), (0, 1.0, 1.75), 42)
    elif S == "p3_b3_a":
        cafe_interior()
        d = Person("dave", (0, 1.0, 0), 0, "shrug", "shock")
        anim(d.root, "location", lambda p: (0, 1.0, 0.15 * abs(math.sin(tsec(p) * 6))))
        camera((0, -2.8, 1.8), (0, 1.0, 1.6), 44)
    elif S == "p3_b4_a":
        world((0.03, 0.02, 0.02), 0.3)
        floor((0.25, 0.18, 0.12))
        table((0, 0.6, 0), 0.7)
        candle((0, 0.55, 0.78))
        box((0.2, 0.75, 0.79), (0.6, 0.4, 0.01), (0.9, 0.88, 0.8), bevel=0)
        d = Person("dave", (-0.75, 0.6, 0.0), -0.4, "hips", "grin")
        b = Person("brad", (0.8, 0.6, 0.0), 0.4, "hips", "grin")
        d.expr("grin")
        b.expr("grin")
        for p_ in (d, b):
            for k, br in enumerate(p_.brows):
                side = -1 if k == 0 else 1
                br.rotation_euler = (0, math.pi / 2 - side * 0.45, 0)
        point((0, -0.4, 0.7), 60, (1, 0.6, 0.3))
        camera((0, -4.8, 1.7), (0, 0.6, 1.3), 34, move=(0, -4.3, 1.65))
    elif S == "p3_b5_a":
        living_room()
        c = Person("chloe", (0, 1.0, 0), 0, "phone2", "shock")
        for k in (0, 1):
            held(c, lambda: box((0, 0, 0), (0.35, 0.02, 0.25), (0.98, 0.95, 0.85), bevel=0.005), k)
        camera((0, -2.9, 1.7), (0, 1.0, 1.4), 42)
    elif S in ("p3_b6_a", "p3_b7_a", "p3_b8_a"):
        restaurant()
        chair((0, 1.1, 0), 0)
        c = Person("chloe", (0, 1.05, 0), 0, "down" if S == "p3_b6_a" else "shrug", "shock")
        c.sit(0.48)
        d = Person("dave", (-1.1, -0.2, 0), math.pi / 2 + 0.6, "box", "grin")
        b = Person("brad", (1.2, -0.2, 0), -math.pi / 2 - 0.6, "box", "grin")
        d.kneel()
        b.kneel()
        open_at = 0.15 if S == "p3_b8_a" else None
        for p_ in (d, b):
            rb = ring_box((0, 0, 0), open_at)
            rb.parent = p_.arms[1]
            rb.location = (0, -0.1 * p_.s, -0.66 * p_.s)
        if S == "p3_b8_a":
            confetti((0, 0.2, 1.1), 0.15 * SECS + 0.1, 80)
            camera((0, -5.2, 1.6), (0, 0.4, 1.0), 34)
        elif S == "p3_b7_a":
            c.bob_head(0.1, 14, 1)
            camera((0, -2.2, 1.8), (0, 1.0, 1.65), 46)
        else:
            camera((0, -6.2, 2.3), (0, 0.4, 1.0), 32, move=(0, -5.5, 2.1))
    elif S == "p3_b9_a":
        restaurant()
        d = Person("dave", (-0.6, 0.3, 0), 0.15, "hips", "grin")
        b = Person("brad", (0.65, 0.3, 0), -0.15, "hips", "grin")
        sunglasses(d)
        sunglasses(b)
        camera((0, -4.6, 1.6), (0, 0.3, 1.5), 36, move=(0, -4.0, 1.55))
    elif S == "p3_b10_a":
        restaurant()
        chair((0, 1.1, 0), 0)
        Person("chloe", (0, 1.05, 0), 0, "down", "sad").sit(0.48)
        d = Person("dave", (-0.4, -0.6, 0), 0, "out", "grin")
        b = Person("brad", (0.4, -0.6, 0), 0, "out", "grin")
        sunglasses(d)
        sunglasses(b)
        d.walk(0.9, (0, -2.5, 0))
        b.walk(0.9, (0, -2.5, 0))
        camera((0, -8.0, 2.2), (0, -0.5, 1.2), 32)
    elif S == "p3_b11_a":
        living_room(night=True)
        c = Person("chloe", (0, 1.35, 0), 0, "phone", "sad")
        c.sit(0.6)
        held(c, lambda: phone(1.2))
        point((0.3, 0.6, 1.4), 14, (0.5, 0.75, 1.0))
        camera((0, -3.4, 1.8), (0, 1.2, 1.4), 42)
    elif S == "p3_b12_a":
        front_door(open_at=0.15)
        d = Person("dave", (-0.42, -0.9, 0), math.pi, "box", "grin")
        b = Person("brad", (0.5, -0.9, 0), math.pi, "box", "grin")
        pizza_hat(d)
        pizza_hat(b)
        pizza_box((0.04, -0.35, 1.15), open_=False)
        pizza((0.04, -0.35, 1.22), 0.45, bye=True)
        point((0, -0.2, 2.0), 80, (1, 0.85, 0.6))
        camera((0.2, 3.6, 1.6), (0, -0.7, 1.4), 38)
    elif S == "p3_b13_a":
        title_set((0.25, 0.15, 0.12))
        pizza((0, 0, 0.5), 1.4, bye=True)
        area((0, -3, 6), (0, 0, 0.5), 40, 4, (1, 0.95, 0.85))
        camera((0, -2.4, 3.6), (0, 0, 0.5), 40)
    else:
        raise SystemExit(f"unknown shot {S}")


build(SHOT)
if STILL:
    sc.frame_set(max(1, int(NF * 0.6)))
    sc.render.filepath = f"{OUT}/still.png"
    bpy.ops.render.render(write_still=True)
else:
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = f"{OUT}/f_"
    bpy.ops.render.render(animation=True)
