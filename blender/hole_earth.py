"""
Blender scenes for the hole_through_earth short (clay 3D style, Eevee).

Run one shot:
  EGL_PLATFORM=surfaceless blender -b -P blender/hole_earth.py -- <shot_id> <seconds> <out_dir> [fps] [--still]
Writes <out_dir>/f_0001.png ... (or a single still at the middle of the shot with --still).
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
sc.eevee.bloom_intensity = 0.06
sc.eevee.use_gtao = True
sc.eevee.use_soft_shadows = True
sc.render.resolution_x, sc.render.resolution_y = 720, 1280
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, NF
sc.view_settings.view_transform = "Standard"   # bold, saturated cartoon colours
sc.view_settings.look = "None"
sc.view_settings.exposure = -0.3

# --------------------------------------------------------------------------- helpers
_mats = {}


def mat(name, col, rough=0.5, emit=0.0, alpha=1.0, spec=0.5):
    if name in _mats:
        return _mats[name]
    m = bpy.data.materials.new(name)
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
    _mats[name] = m
    return m


def smooth(o):
    for p in o.data.polygons:
        p.use_smooth = True


def sphere(loc, r, m, seg=64, name="s"):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.object
    o.name = name
    smooth(o)
    o.data.materials.append(m)
    return o


def cyl(loc, r, depth, m, rot=(0, 0, 0), verts=48, name="c"):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    smooth(o)
    o.data.materials.append(m)
    return o


def empty(loc=(0, 0, 0), name="e"):
    bpy.ops.object.empty_add(location=loc)
    o = bpy.context.object
    o.name = name
    return o


def parent(child, par):
    """Parent with child's current location treated as local to the parent."""
    child.parent = par


def key(o, path, frame, value):
    setattr(o, path, value)
    o.keyframe_insert(path, frame=frame)


def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def anim(o, path, fn, step=1):
    """Keyframe o.path = fn(p) for p in 0..1 across the shot."""
    for f in range(1, NF + 1, step):
        key(o, path, f, fn((f - 1) / (NF - 1)))
    key(o, path, NF, fn(1.0))


def camera(loc, look=(0, 0, 0), lens=50):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.data.lens = lens
    sc.camera = c
    aim(c, look)
    return c


def aim(c, look):
    d = mathutils.Vector(look) - c.location
    c.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def anim_cam(c, fn_loc, look_fn, step=1):
    for f in range(1, NF + 1, step):
        p = (f - 1) / (NF - 1)
        c.location = fn_loc(p)
        aim(c, look_fn(p))
        c.keyframe_insert("location", frame=f)
        c.keyframe_insert("rotation_euler", frame=f)


def lights(strength=0.7, warm=True):
    bpy.ops.object.light_add(type="AREA", location=(-4, -5, 5))
    k = bpy.context.object
    k.data.energy = 1800 * strength
    k.data.size = 5
    k.data.color = (1.0, 0.95, 0.88) if warm else (1, 1, 1)
    aim(k, (0, 0, 0))
    bpy.ops.object.light_add(type="AREA", location=(5, 3, 2))
    r = bpy.context.object
    r.data.energy = 900 * strength
    r.data.size = 3
    r.data.color = (0.55, 0.75, 1.0)
    aim(r, (0, 0, 0))
    bpy.ops.object.light_add(type="AREA", location=(0, -6, -3))
    f = bpy.context.object
    f.data.energy = 300 * strength
    f.data.size = 6
    aim(f, (0, 0, 0))


def world(col=(0.012, 0.014, 0.05), strength=1.0):
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*col, 1)
    bg.inputs["Strength"].default_value = strength


def stars(n=250, r=40):
    random.seed(9)
    m = mat("star", (1, 1, 1), emit=6)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.05)
    base = bpy.context.object
    base.data.materials.append(m)
    for _ in range(n):
        v = mathutils.Vector((random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1))).normalized() * r
        o = base.copy()
        o.location = v
        o.scale = [random.uniform(0.5, 2.0)] * 3
        sc.collection.objects.link(o)
    bpy.data.objects.remove(base)


# --------------------------------------------------------------------------- Earth
OCEAN = (0.04, 0.28, 0.85)
LAND = (0.15, 0.62, 0.22)
CRUST = (0.45, 0.32, 0.22)
MANTLE = (0.85, 0.28, 0.07)
OUTER = (1.0, 0.42, 0.05)
INNER = (1.0, 0.75, 0.2)


def land_blobs(par, r=1.0, cut=False, seed=2):
    random.seed(seed)
    m = mat("land", LAND, 0.6)
    for k in range(11):
        th, ph = random.uniform(0, 2 * math.pi), random.uniform(-1.1, 1.1)
        v = mathutils.Vector((math.cos(th) * math.cos(ph), math.sin(th) * math.cos(ph), math.sin(ph)))
        if cut and v.x > -0.15 and v.y < 0.15:
            continue
        b = sphere(v * r * 0.94, random.uniform(0.2, 0.36) * r, m, seg=32, name="land")
        b.scale = (1, 1, 0.42)
        b.rotation_mode = "QUATERNION"
        b.rotation_quaternion = mathutils.Vector((0, 0, 1)).rotation_difference(v)
        parent(b, par)


def cutter(r, eps=0.0):
    """Box removing the front-right quarter (x>eps, y<-eps) of anything it cuts."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(r * 1.5 + eps, -r * 1.5 - eps, 0))
    c = bpy.context.object
    c.scale = (r * 3, r * 3, r * 3.2)
    c.hide_render = True
    c.hide_viewport = True
    return c


def boolean_cut(o, c):
    mod = o.modifiers.new("cut", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = c
    mod.solver = "EXACT"


def earth_whole(r=1.0):
    root = empty(name="earth")
    o = sphere((0, 0, 0), r, mat("ocean", OCEAN, 0.3, spec=0.7), seg=96, name="ocean")
    parent(o, root)
    land_blobs(root, r)
    return root


def earth_cutaway(r=1.0, tunnel=False, tube=False, glow_line=0.0):
    root = empty(name="earth")
    layers = [(r, mat("ocean", OCEAN, 0.3, spec=0.7)), (r * 0.985, mat("crust", CRUST, 0.8)),
              (r * 0.955, mat("mantle", MANTLE, 0.55, emit=0.12)), (r * 0.546, mat("outer", OUTER, 0.35, emit=0.7)),
              (r * 0.19, mat("inner", INNER, 0.3, emit=1.6))]
    for k, (rad, m) in enumerate(layers):
        o = sphere((0, 0, 0), rad, m, seg=96, name="layer")
        # each inner layer's cut face sits a hair closer to the camera, so faces never overlap (no stripes)
        boolean_cut(o, cutter(r, 0.006 * k))
        parent(o, root)
    land_blobs(root, r, cut=True)
    if tunnel or tube:
        t = cyl((0.035 * r, -0.035 * r, 0), 0.035 * r, 2.06 * r, mat("tube", (0.75, 0.9, 1.0), 0.05, emit=0.8 if tube else 0.0,
                                                  alpha=0.6 if tube else 1.0), name="tube")
        if not tube:
            t.data.materials[0] = mat("tunnel", (0.02, 0.02, 0.03), 0.9)
        parent(t, root)
    if glow_line:
        g = cyl((0.04 * r, -0.04 * r, 0), 0.014 * r, 2.1 * r, mat("line", (1.0, 0.85, 0.2), emit=12), name="line")
        parent(g, root)
    return root


def dot(r=0.06):
    return sphere((0.04, -0.04, 1.05), r, mat("dot", (1.0, 0.25, 0.2), 0.3, emit=4), seg=24, name="dot")


# --------------------------------------------------------------------------- character
SKIN = (0.95, 0.68, 0.5)
HOODIE = (0.12, 0.38, 0.9)
PANTS = (0.1, 0.1, 0.18)


def character(loc=(0, 0, 0), s=1.0, arms="down"):
    root = empty((0, 0, 0), name="hero")
    body = cyl((0, 0, 0.95 * s), 0.3 * s, 0.75 * s, mat("hoodie", HOODIE, 0.6), name="body")
    for z in (0.58, 1.32):
        cap = sphere((0, 0, z * s), 0.3 * s, mat("hoodie", HOODIE, 0.6), seg=32, name="cap")
        cap.scale = (1, 1, 0.55)
        parent(cap, root)
    parent(body, root)
    head = sphere((0, 0, 1.78 * s), 0.34 * s, mat("skin", SKIN, 0.45), seg=48, name="head")
    parent(head, root)
    hair = sphere((0, 0.02 * s, 1.88 * s), 0.35 * s, mat("hair", (0.28, 0.17, 0.09), 0.7), seg=48, name="hair")
    hair.scale = (1.0, 1.0, 0.75)
    parent(hair, root)
    for ex in (-0.12, 0.12):
        e = sphere((ex * s, -0.3 * s, 1.8 * s), 0.07 * s, mat("eye", (1, 1, 1), 0.2), seg=24, name="eye")
        parent(e, root)
        p = sphere((ex * s, -0.36 * s, 1.8 * s), 0.035 * s, mat("pupil", (0.02, 0.02, 0.02), 0.2), seg=16, name="pupil")
        parent(p, root)
    mouth = sphere((0, -0.31 * s, 1.64 * s), 0.05 * s, mat("mouth", (0.45, 0.08, 0.08), 0.5), seg=16, name="mouth")
    mouth.scale = (1.4, 0.6, 0.8)
    parent(mouth, root)
    for lx in (-0.13, 0.13):
        leg = cyl((lx * s, 0, 0.3 * s), 0.11 * s, 0.6 * s, mat("pants", PANTS, 0.7), name="leg")
        parent(leg, root)
        shoe = sphere((lx * s, -0.06 * s, 0.02 * s), 0.13 * s, mat("shoe", (0.95, 0.95, 0.95), 0.5), seg=24, name="shoe")
        shoe.scale = (1, 1.4, 0.6)
        parent(shoe, root)
    arm_objs = []
    for side in (-1, 1):
        piv = empty((side * 0.33 * s, 0, 1.3 * s), name="shoulder")
        parent(piv, root)
        a = cyl((0, 0, -0.32 * s), 0.09 * s, 0.6 * s, mat("hoodie", HOODIE, 0.6), name="arm")
        parent(a, piv)
        h = sphere((0, 0, -0.64 * s), 0.1 * s, mat("skin", SKIN, 0.45), seg=24, name="hand")
        parent(h, piv)
        piv.rotation_euler = (0, side * {"down": 0.15, "up": 2.7, "out": 1.5}[arms], 0)
        arm_objs.append(piv)
    root.location = loc
    return root, arm_objs


def wave(arms, side=1, speed=8.0):
    a = arms[0 if side < 0 else 1]
    for f in range(1, NF + 1):
        t = (f - 1) / FPS
        a.rotation_euler = (0, side * (2.5 + 0.35 * math.sin(t * speed)), 0)
        a.keyframe_insert("rotation_euler", frame=f)


# --------------------------------------------------------------------------- sets
def ground(col=(0.3, 0.68, 0.3), hole=True, r=30):
    g = cyl((0, 0, -0.05), r, 0.1, mat("ground" + str(col), col, 0.85), verts=96, name="ground")
    if hole:
        cyl((0, 0, 0.005), 0.9, 0.02, mat("hole", (0.0, 0.0, 0.0), 1.0), verts=64, name="hole")
        bpy.ops.mesh.primitive_torus_add(major_radius=0.95, minor_radius=0.09, location=(0, 0, 0.03))
        t = bpy.context.object
        smooth(t)
        t.data.materials.append(mat("rim", (0.45, 0.3, 0.18), 0.8))
    random.seed(4)
    for _ in range(14):
        a, d = random.uniform(0, 6.28), random.uniform(3, 9)
        rock = sphere((math.cos(a) * d, math.sin(a) * d, 0), random.uniform(0.15, 0.4), mat("rock", (0.55, 0.55, 0.58), 0.8),
                      seg=16, name="rock")
        rock.scale = (1, 1, 0.6)
    return g


def tree(loc, s=1.0):
    cyl((loc[0], loc[1], 0.9 * s), 0.14 * s, 1.8 * s, mat("trunk", (0.4, 0.25, 0.12), 0.8))
    for dx, dy, dz, r in ((0, 0, 2.3, 0.9), (-0.5, 0.2, 1.9, 0.6), (0.5, -0.1, 2.0, 0.65)):
        sphere((loc[0] + dx * s, loc[1] + dy * s, dz * s), r * s, mat("leaf", (0.2, 0.62, 0.25), 0.7), seg=32)


def sky_world():
    world((0.35, 0.55, 0.9), 0.5)


def jump_into_hole(hero, start=(-1.6, 0, 0), t_jump=0.35, t_end=0.75):
    def loc(p):
        if p < t_jump:
            return mathutils.Vector(start)
        q = (p - t_jump) / (t_end - t_jump)
        x = start[0] * (1 - min(1, q * 1.6))
        z = 1.2 * math.sin(min(1, q * 1.6) * math.pi * 0.6) if q < 0.62 else 1.2 * math.sin(0.6 * math.pi) - (q - 0.62) * 9
        return mathutils.Vector((x, 0, z))
    anim(hero, "location", loc)


# --------------------------------------------------------------------------- shots
def shot_earth_spin(push=True, look_z=0.0):
    world()
    stars()
    lights()
    e = earth_whole()
    anim(e, "rotation_euler", lambda p: (0.35, 0, p * 1.2))
    camera((0, -6.2, 0.4), (0, 0, look_z), 50)
    if push:
        anim_cam(sc.camera, lambda p: (0, -6.2 + 1.6 * ease(p), 0.4), lambda p: (0, 0, 0))


def cut_view(cam=(2.3, -5.0, 1.5), look=(0, 0, 0), lens=58):
    world()
    stars()
    lights(0.8)
    return camera(cam, look, lens)


def build(shot):
    if shot == "beat_1_a":
        shot_earth_spin()
    elif shot in ("beat_1_b", "beat_6_b"):
        sky_world()
        lights(0.45)
        ground()
        tree((4, 4, 0), 1.2)
        tree((-5, 6, 0), 1.0)
        hero, arms = character((-1.6, 0, 0), 0.8, "up")
        hero.rotation_euler = (0, 0, math.radians(90))
        jump_into_hole(hero)
        camera((2.5, -7.5, 3.8), (-0.3, 0, 0.6), 40)
    elif shot == "beat_2_a":
        cut_view()
        earth_cutaway(glow_line=1)
        line = bpy.data.objects["line"]
        anim(line, "scale", lambda p: (1, 1, max(0.001, ease(p / 0.6))))
    elif shot == "beat_2_b":
        cut_view()
        e = earth_cutaway(glow_line=1)
        anim(e, "rotation_euler", lambda p: (0, 0, -0.25 + 0.5 * p))
    elif shot == "beat_3_a":
        sky_world()
        lights(0.45)
        ground((0.42, 0.36, 0.28), hole=False)
        cap = cyl((0, 0, 0.12), 0.35, 0.24, mat("rust", (0.45, 0.2, 0.08), 0.75, spec=0.3), name="cap")
        for k in range(8):
            a = k * math.pi / 4
            sphere((math.cos(a) * 0.28, math.sin(a) * 0.28, 0.25), 0.03, mat("bolt", (0.3, 0.3, 0.32), 0.4), seg=12)
        cyl((0, 0, 0.26), 0.22, 0.06, mat("rust", (0.45, 0.2, 0.08), 0.75, spec=0.3))
        camera((1.2, -1.8, 1.4), (0, 0, 0.1), 40)
        anim_cam(sc.camera, lambda p: (1.2 - 0.3 * p, -1.8 + 0.3 * p, 1.4 - 0.2 * p), lambda p: (0, 0, 0.1))
    elif shot == "beat_3_b":
        shot_earth_spin(push=False)
        m = sphere((0, -1.0, 0.25), 0.03, mat("dot", (1.0, 0.25, 0.2), 0.3, emit=4), seg=16)
        parent(m, bpy.data.objects["earth"])
    elif shot in ("beat_4_a", "beat_4_b"):
        c = cut_view((1.6, -1.6, 0.9) if shot == "beat_4_a" else (1.5, -1.8, 0.6), (0.35, -0.35, 0.3), 40)
        earth_cutaway()
        a, b = ((1.8, -2.0, 1.0), (1.5, -1.8, 0.8)) if shot == "beat_4_a" else ((1.5, -1.8, 0.6), (1.3, -1.6, 0.45))
        anim_cam(c, lambda p: tuple(a[i] + (b[i] - a[i]) * p for i in range(3)), lambda p: (0.3, -0.3, 0.3))
    elif shot == "beat_5_a":
        c = cut_view((1.3, -1.3, 0.8), (0.2, -0.2, 0.15), 40)
        earth_cutaway()
        anim_cam(c, lambda p: (1.3 - 0.3 * p, -1.3 + 0.3 * p, 0.8 - 0.2 * p), lambda p: (0.15, -0.15, 0.1))
    elif shot == "beat_5_b":
        c = cut_view((0.95, -0.95, 0.4), (0.0, 0.0, 0.0), 40)
        earth_cutaway()
        anim_cam(c, lambda p: (0.95 - 0.2 * p, -0.95 + 0.2 * p, 0.4 - 0.1 * p), lambda p: (0, 0, 0))
    elif shot == "beat_6_a":
        cut_view()
        earth_cutaway(tube=True)
        t = bpy.data.objects["tube"]
        anim(t, "scale", lambda p: (1, 1, max(0.001, ease(p / 0.7))))
    elif shot == "beat_7_a":
        world((0.02, 0.03, 0.06))
        lights(0.7)
        hero, arms = character((0, 0, 0), 1.0, "up")
        hero.rotation_euler = (math.radians(180), 0, 0)
        hero.location = (0, 0, 1.0)
        ring_m = mat("ring", (0.6, 0.85, 1.0), 0.2, emit=3)
        rings = []
        for k in range(12):
            bpy.ops.mesh.primitive_torus_add(major_radius=1.6, minor_radius=0.03, location=(0, 0, -4 + k * 2.0))
            rg = bpy.context.object
            rg.data.materials.append(ring_m)
            rings.append(rg)
        for k, rg in enumerate(rings):
            base = -4 + k * 2.0
            anim(rg, "location", lambda p, b=base: (0, 0, (b + p * 60) % 24 - 6))
        cyl((0, 0, 0), 1.65, 30, mat("tubewall", (0.5, 0.75, 1.0), 0.1, alpha=0.25), verts=64)
        camera((0, -6.5, -1.5), (0, 0, 0.2), 32)
        anim(hero, "rotation_euler", lambda p: (math.radians(180), 0, p * 3))
    elif shot in ("beat_7_b", "beat_9_a", "beat_10_b"):
        cut_view((2.6, -5.4, 0.8), (0, 0, 0), 55)
        earth_cutaway(tube=True)
        d = dot(0.07)
        if shot == "beat_7_b":
            fn = lambda p: (0.04, -0.04, 1.0 * math.cos(ease(p) * math.pi / 2))
        elif shot == "beat_9_a":
            fn = lambda p: (0.04, -0.04, -1.0 * math.sin(ease(p) * math.pi / 2))
        else:
            fn = lambda p: (0.04, -0.04, math.cos(p * 2 * math.pi * 1.5))
        anim(d, "location", fn)
    elif shot == "beat_8_a":
        world((0.05, 0.02, 0.0), 1)
        sphere((0, 4, 0), 3.0, mat("corebg", (1.0, 0.6, 0.15), 0.3, emit=1.5), seg=64)
        lights(0.6)
        hero, arms = character((0, 0, -1.0), 1.0, "out")
        anim(hero, "rotation_euler", lambda p: (0.3 * math.sin(p * 4), 0.2 * math.cos(p * 3), p * 1.2))
        anim(hero, "location", lambda p: (0, 0, -1.0 + 0.12 * math.sin(p * 6)))
        camera((0, -6, 0.3), (0, 0, 0), 45)
    elif shot == "beat_8_b":
        cut_view((2.3, -5.0, 1.5), (0, 0, 0), 58)
        earth_cutaway(tube=True)
        dot(0.07).location = (0.04, -0.04, 0)
        arrow_m = mat("arrow", (1.0, 0.85, 0.2), 0.3, emit=3)
        for k in range(8):
            a = k * math.pi / 4
            v = mathutils.Vector((math.cos(a) * 0.45, -0.25, math.sin(a) * 0.45))
            bpy.ops.mesh.primitive_cone_add(radius1=0.06, depth=0.18, location=v)
            cone = bpy.context.object
            cone.data.materials.append(arrow_m)
            cone.rotation_mode = "QUATERNION"
            cone.rotation_quaternion = mathutils.Vector((0, 0, 1)).rotation_difference(-v)
    elif shot in ("beat_9_b", "beat_11_b"):
        if shot == "beat_9_b":
            sky_world()
            lights(0.45)
            ground((0.85, 0.75, 0.5))
            for x, y in ((4, 5), (-4, 6)):
                cyl((x, y, 1.2), 0.12, 2.4, mat("trunk", (0.4, 0.25, 0.12), 0.8))
                for k in range(5):
                    a = k * 1.26
                    leaf = sphere((x + math.cos(a) * 0.6, y + math.sin(a) * 0.6, 2.4), 0.5, mat("leaf", (0.2, 0.62, 0.25), 0.7), seg=24)
                    leaf.scale = (1.4, 0.5, 0.2)
                    leaf.rotation_euler = (0, 0, a)
        else:
            world((0.35, 0.6, 0.9), 0.55)
            lights(0.45)
            cyl((0, 0, -0.05), 40, 0.1, mat("sea", (0.05, 0.35, 0.75), 0.15, spec=0.9), verts=96)
            random.seed(5)
            for k in range(14):
                a = k * 2 * math.pi / 14
                dr = sphere((0, 0, 0), random.uniform(0.08, 0.16), mat("drop", (0.7, 0.88, 1.0), 0.1, alpha=0.8), seg=16)
                anim(dr, "location", lambda p, a=a: (math.cos(a) * (0.6 + 1.6 * p), math.sin(a) * (0.6 + 1.6 * p),
                                                     max(0.0, 2.2 * p - 3.2 * p * p) + 0.1))
        hero, arms = character((0, 0, -3), 0.8, "up")
        anim(hero, "location", lambda p: (0, 0, -3 + 3.6 * math.sin(min(1, p / 0.55) * math.pi / 2)
                                          - (0 if p < 0.55 else 0.6 * ease((p - 0.55) / 0.45))))
        camera((2.5, -7.5, 3.0), (0, 0, 1.0), 40)
    elif shot == "beat_10_a":
        sky_world()
        lights(0.45)
        ground((0.85, 0.75, 0.5))
        hero, arms = character((0, 0, 0.6), 0.8, "up")
        anim(hero, "location", lambda p: (0, 0, 0.6 + 0.3 * math.sin(min(1, p / 0.25) * math.pi) - 6 * ease((p - 0.3) / 0.5)))
        camera((2.5, -7.5, 3.8), (0, 0, 0.6), 40)
    elif shot == "beat_11_a":
        world()
        stars()
        lights()
        e = earth_whole()
        uk = sphere((0, 0, 0), 0.05, mat("ukpin", (1.0, 0.2, 0.2), 0.3, emit=5), seg=16)
        nz = sphere((0, 0, 0), 0.05, mat("nzpin", (1.0, 0.85, 0.2), 0.3, emit=5), seg=16)
        lat, lon = math.radians(54), math.radians(-2)
        v = mathutils.Vector((math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)))
        uk.location = v * 1.02
        nz.location = -v * 1.02
        parent(uk, e)
        parent(nz, e)
        # start with the UK facing the camera, then spin half a turn to show the far side
        base = math.atan2(v.x, -v.y) * 0
        anim(e, "rotation_euler", lambda p: (0, 0, math.radians(-90) + math.pi * ease(p)))
        camera((0, -6.0, 1.2), (0, 0, 0.2), 50)
    elif shot in ("beat_12_a", "beat_12_b"):
        world()
        stars()
        lights()
        e = earth_whole(1.6)
        e.location = (0, 0, -1.6)
        anim(e, "rotation_euler", lambda p: (0, p * 0.6, 0))
        hero, arms = character((0, 0, 0), 0.55, "down")
        wave(arms, 1)
        camera((0.8, -5.0, 1.6), (0, 0, 0.6), 45)
        anim_cam(sc.camera, lambda p: (0.8 + 1.2 * p, -5.0 + 0.4 * p, 1.6), lambda p: (0, 0, 0.6))
    elif shot == "outro":
        shot_earth_spin(push=False)
    else:
        raise SystemExit(f"unknown shot {shot}")


build(SHOT)
if STILL:
    sc.frame_set(NF // 2)
    sc.render.filepath = f"{OUT}/still.png"
    bpy.ops.render.render(write_still=True)
else:
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = f"{OUT}/f_"
    bpy.ops.render.render(animation=True)
