"""
"Style v2" look test for the Dave story: Pixar-ish characters, depth of field, richer lighting & set.
  EGL_PLATFORM=surfaceless blender -b -P blender/style_v2.py -- <out.png>
"""
import math
import sys

import bpy
import mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
V = mathutils.Vector

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
ee = sc.eevee
ee.taa_render_samples = 48
ee.use_gtao = True
ee.gtao_distance = 0.6
ee.use_bloom = True
ee.bloom_intensity = 0.03
ee.use_soft_shadows = True
ee.use_ssr = True
ee.shadow_cube_size = "2048"
ee.shadow_cascade_size = "2048"
sc.render.resolution_x, sc.render.resolution_y = 720, 1280
sc.view_settings.view_transform = "Standard"
try:
    sc.view_settings.look = "Filmic - High Contrast"
except TypeError:
    try:
        sc.view_settings.look = "High Contrast"
    except TypeError:
        pass
sc.view_settings.exposure = -0.55

_m = {}


def mat(col, rough=0.5, sss=0.0, emit=0.0, spec=0.5, noise=None, coat=0.0):
    k = (tuple(round(c, 3) for c in col), rough, sss, emit, noise, coat)
    if k in _m:
        return _m[k]
    m = bpy.data.materials.new("m")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Specular IOR Level"].default_value = spec
    if coat:
        b.inputs["Coat Weight"].default_value = coat
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (1.0, 0.35, 0.2)
        b.inputs["Subsurface Scale"].default_value = 0.08
    if emit:
        b.inputs["Emission Color"].default_value = (*col, 1)
        b.inputs["Emission Strength"].default_value = emit
    if noise:  # (scale, contrast colour) -> subtle procedural variation (wood grain, fabric)
        scale, col2, stretch = noise
        tc = nt.nodes.new("ShaderNodeTexCoord")
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = stretch
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = scale
        nz.inputs["Detail"].default_value = 6
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = (*col, 1)
        ramp.color_ramp.elements[1].color = (*col2, 1)
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
        nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    _m[k] = m
    return m


def fin(o, m, subd=0):
    for p in o.data.polygons:
        p.use_smooth = True
    o.data.materials.append(m)
    if subd:
        md = o.modifiers.new("sub", "SUBSURF")
        md.levels = md.render_levels = subd
    return o


def sphere(loc, r, m, scale=(1, 1, 1), seg=48, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc, rotation=rot)
    o = fin(bpy.context.object, m)
    o.scale = scale
    return o


def capsule(a, b, r, m, r2=None):
    """Smooth tube from point a to b (limbs, torso)."""
    a, b = V(a), V(b)
    d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = V((0, 0, 1)).rotation_difference(d)
    fin(o, m)
    if r2:
        for v in o.data.vertices:
            if v.co.z > 0:
                v.co.x *= r2 / r
                v.co.y *= r2 / r
    sphere(a, r, m)
    sphere(b, r2 or r, m)
    return o


def rbox(loc, size, m, bevel=0.08, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    bv = o.modifiers.new("b", "BEVEL")
    bv.width, bv.segments = bevel, 4
    return fin(o, m)


def cyl(loc, r, h, m, rot=(0, 0, 0), verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    return fin(bpy.context.object, m)


def torus(loc, R, r, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot)
    return fin(bpy.context.object, m)


def area(loc, look, e, size, col):
    bpy.ops.object.light_add(type="AREA", location=loc)
    l = bpy.context.object
    l.data.energy, l.data.size, l.data.color = e, size, col
    l.rotation_euler = (V(look) - V(loc)).to_track_quat("-Z", "Y").to_euler()
    return l


# --------------------------------------------------------------------------- characters (big-head, big-eye style)
SKIN = (0.95, 0.55, 0.38)


def eye(c, s, iris):
    sphere(c, 0.105 * s, mat((0.97, 0.97, 0.97), 0.15, coat=0.6), scale=(1, 0.75, 1.1))
    sphere(c + V((0, -0.06 * s, -0.005 * s)), 0.062 * s, mat(iris, 0.2, coat=0.8), scale=(1, 0.45, 1.05))
    sphere(c + V((0, -0.09 * s, -0.005 * s)), 0.032 * s, mat((0.01, 0.01, 0.01), 0.1), scale=(1, 0.4, 1.05))
    sphere(c + V((0.025 * s, -0.105 * s, 0.03 * s)), 0.014 * s, mat((1, 1, 1), 0.1, emit=4))


def character(who, x, y, sit=False, rz=0.0, mood="smile"):
    s = 1.0
    root_objs_before = set(bpy.data.objects)
    if who == "dave":
        top, hair, iris, legs = (0.12, 0.36, 0.85), (0.3, 0.17, 0.08), (0.35, 0.22, 0.1), (0.13, 0.15, 0.25)
    else:
        top, hair, iris, legs = (0.95, 0.4, 0.62), (0.6, 0.2, 0.08), (0.15, 0.45, 0.25), SKIN
    hip_z = 0.62 if sit else 0.75
    # legs
    for side in (-1, 1):
        hx = side * 0.13
        if sit:
            capsule((hx, 0, hip_z), (hx, -0.42, hip_z), 0.1, mat(legs, 0.7))
            capsule((hx, -0.42, hip_z), (hx, -0.45, 0.12), 0.09, mat(legs, 0.7))
            sphere((hx, -0.5, 0.07), 0.1, mat((0.95, 0.95, 0.95) if who == "dave" else (0.85, 0.15, 0.3), 0.4), scale=(1, 1.5, 0.65))
        else:
            capsule((hx, 0, hip_z), (hx, 0, 0.12), 0.1, mat(legs, 0.7))
            sphere((hx, -0.05, 0.07), 0.1, mat((0.95, 0.95, 0.95), 0.4), scale=(1, 1.5, 0.65))
    # torso
    tm = mat(top, 0.75, noise=(60, tuple(c * 0.88 for c in top), (1, 1, 1)))
    if who == "dave":
        capsule((0, 0, hip_z + 0.12), (0, 0, hip_z + 0.62), 0.27, tm, r2=0.24)
        torus((0, 0.02, hip_z + 0.82), 0.2, 0.07, tm, rot=(0.25, 0, 0))   # hood around the neck
        for side in (-1, 1):
            capsule((side * 0.07, -0.25, hip_z + 0.62), (side * 0.08, -0.27, hip_z + 0.38), 0.012, mat((0.95, 0.95, 0.95), 0.4))
        rbox((0, -0.24, hip_z + 0.2), (0.3, 0.06, 0.14), tm, bevel=0.03)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.42, radius2=0.22, depth=0.62, location=(0, 0, hip_z + 0.2))
        fin(bpy.context.object, tm)
        capsule((0, 0, hip_z + 0.45), (0, 0, hip_z + 0.65), 0.22, tm)
    # arms (resting)
    for side in (-1, 1):
        sh = V((side * 0.3, 0, hip_z + 0.6))
        el = sh + V((side * 0.1, -0.05, -0.27))
        wr = el + V((side * 0.02, -0.17, -0.06)) if sit else el + V((side * 0.03, 0, -0.25))
        capsule(sh, el, 0.075, tm if who == "dave" else mat(SKIN, 0.45, sss=0.4))
        capsule(el, wr, 0.07, tm if who == "dave" else mat(SKIN, 0.45, sss=0.4))
        sphere(wr + V((0, -0.02, -0.04)), 0.075, mat(SKIN, 0.45, sss=0.4), scale=(0.9, 1.0, 1.2))
    # head
    hz = hip_z + 1.12
    skin = mat(SKIN, 0.42, sss=0.15)
    sphere((0, 0, hz), 0.42, skin, scale=(1.0, 0.95, 0.98), seg=64)
    sphere((0, -0.02, hz - 0.12), 0.39, skin, scale=(1.0, 0.95, 0.85))                  # soft jaw, blends into head
    sphere((0, -0.4, hz - 0.06), 0.06, skin, scale=(1, 0.9, 0.85))                     # nose
    for side in (-1, 1):
        sphere((side * 0.41, 0.02, hz - 0.04), 0.08, skin, scale=(0.5, 1, 1.2))           # ears
        eye(V((side * 0.15, -0.34, hz + 0.06)), 1.0, iris)
        # eyelid hint
        sphere((side * 0.15, -0.33, hz + 0.13), 0.1, skin, scale=(1.05, 0.7, 0.4))
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.022, depth=0.15, location=(side * 0.15, -0.38, hz + 0.25),
                                            rotation=(0, math.pi / 2 + side * (0.15 if mood != "angry" else -0.3), 0))
        fin(bpy.context.object, mat(tuple(c * 0.7 for c in hair), 0.8))
        if who == "chloe":
            sphere((side * 0.26, -0.3, hz - 0.12), 0.07, mat((1.0, 0.5, 0.55), 0.5), scale=(1, 0.4, 0.7))
            for k in (-1, 0, 1):
                bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.008, depth=0.07,
                                                    location=(side * 0.15 + k * 0.035, -0.41, hz + 0.16),
                                                    rotation=(0.5, k * 0.4, 0))
                fin(bpy.context.object, mat((0.03, 0.03, 0.03), 0.5))
    # mouth
    mouth = mat((0.55, 0.12, 0.13), 0.4)
    if mood == "smile":
        import bmesh
        sm = torus((0, -0.36, hz - 0.13), 0.085, 0.02, mouth, rot=(math.pi / 2 + 0.25, 0, 0))
        bm = bmesh.new()
        bm.from_mesh(sm.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0.005], context="VERTS")
        bm.to_mesh(sm.data)
        bm.free()
    else:
        sphere((0, -0.37, hz - 0.17), 0.06, mouth, scale=(1.3, 0.4, 0.5))
    # hair
    hm = mat(hair, 0.55, noise=(40, tuple(c * 0.75 for c in hair), (1, 1, 3)), coat=0.2)
    if who == "dave":
        sphere((0, 0.04, hz + 0.12), 0.44, hm, scale=(1.0, 1.0, 0.75))
        sphere((-0.05, -0.27, hz + 0.3), 0.2, hm, scale=(1.9, 0.75, 0.6), rot=(0.3, -0.2, 0.15))
        sphere((0.2, -0.2, hz + 0.36), 0.13, hm, scale=(1.4, 0.8, 0.6), rot=(0.4, 0.3, -0.3))
    else:
        sphere((0, 0.05, hz + 0.12), 0.45, hm, scale=(1.02, 1.0, 0.78))
        sphere((0, 0.18, hz - 0.3), 0.44, hm, scale=(1.08, 0.7, 1.35))
        for side in (-1, 1):
            capsule((side * 0.36, -0.05, hz + 0.05), (side * 0.38, -0.02, hz - 0.55), 0.11, hm, r2=0.08)
        sphere((0.08, -0.32, hz + 0.28), 0.2, hm, scale=(1.6, 0.6, 0.55), rot=(0, 0.25, 0))
    # group everything new under an empty to place it
    new = [o for o in bpy.data.objects if o not in root_objs_before]
    bpy.ops.object.empty_add(location=(0, 0, 0))
    root = bpy.context.object
    for o in new:
        o.parent = root
    root.location = (x, y, 0)
    root.rotation_euler = (0, 0, rz)
    return root


# --------------------------------------------------------------------------- set: cosy living room
w = bpy.data.worlds.new("w")
sc.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.55, 0.6, 0.7, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.25

wood = mat((0.36, 0.18, 0.08), 0.45, noise=(3, (0.24, 0.11, 0.04), (1, 12, 1)), coat=0.3)
rbox((0, 0, -0.05), (16, 16, 0.1), wood, bevel=0.0)
wallm = mat((0.85, 0.6, 0.38), 0.85, noise=(30, (0.78, 0.53, 0.32), (1, 1, 1)))
rbox((0, 2.7, 2.5), (16, 0.2, 5.0), wallm, bevel=0)
rbox((0, 2.58, 0.08), (16, 0.06, 0.16), mat((0.95, 0.93, 0.88), 0.4), bevel=0.01)
# window with curtains
rbox((2.5, 2.58, 2.0), (1.6, 0.04, 1.5), mat((0.75, 0.88, 1.0), 0.1, emit=1.2), bevel=0)
for dx in (-0.82, 0.82):
    rbox((2.5 + dx, 2.55, 2.0), (0.08, 0.08, 1.62), mat((0.97, 0.97, 0.95), 0.4), bevel=0.01)
    rbox((2.5 + dx * 1.25, 2.45, 1.8), (0.45, 0.12, 2.4), mat((0.75, 0.25, 0.2), 0.9, noise=(25, (0.6, 0.18, 0.14), (1, 1, 6))), bevel=0.05)
# picture frames
for x, col in ((-1.2, (0.3, 0.55, 0.75)), (-0.2, (0.9, 0.7, 0.3))):
    rbox((x, 2.58, 2.4), (0.7, 0.05, 0.55), mat((0.15, 0.1, 0.07), 0.4), bevel=0.01)
    rbox((x, 2.55, 2.4), (0.58, 0.02, 0.43), mat(col, 0.6), bevel=0)
# bookshelf
rbox((-2.9, 2.35, 1.1), (1.2, 0.45, 2.2), mat((0.5, 0.3, 0.16), 0.5, noise=(4, (0.4, 0.22, 0.1), (1, 10, 1))), bevel=0.02)
import random
random.seed(4)
for row in range(4):
    x0 = -3.42
    while x0 < -2.4:
        wdt = random.uniform(0.06, 0.12)
        hgt = random.uniform(0.28, 0.4)
        rbox((x0 + wdt / 2, 2.15, 0.25 + row * 0.5 + hgt / 2), (wdt, 0.3, hgt),
             mat(random.choice([(0.7, 0.2, 0.2), (0.2, 0.4, 0.7), (0.85, 0.7, 0.3), (0.25, 0.55, 0.35), (0.9, 0.9, 0.85)]), 0.6),
             bevel=0.008)
        x0 += wdt + 0.01
# sofa
sofa = mat((0.2, 0.42, 0.42), 0.9, noise=(40, (0.16, 0.35, 0.35), (1, 1, 1)))
rbox((0, 1.75, 0.3), (3.0, 1.0, 0.42), sofa, bevel=0.14)
rbox((0, 2.2, 0.85), (3.0, 0.35, 0.95), sofa, bevel=0.16)
for x in (-1.6, 1.6):
    rbox((x, 1.75, 0.55), (0.35, 1.05, 0.75), sofa, bevel=0.15)
for x in (-0.65, 0.65):
    rbox((x, 1.78, 0.62), (1.25, 0.85, 0.22), mat((0.24, 0.48, 0.48), 0.9), bevel=0.1)
for x, col in ((-1.25, (0.95, 0.75, 0.3)), (1.2, (0.9, 0.45, 0.4))):
    rbox((x, 2.0, 0.95), (0.45, 0.18, 0.42), mat(col, 0.9), bevel=0.08, rot=(0.25, 0, 0.15 * (1 if x > 0 else -1)))
# rug, coffee table, plant, lamp
cyl((0, 0.3, 0.012), 2.0, 0.02, mat((0.75, 0.3, 0.25), 0.95, noise=(80, (0.65, 0.24, 0.2), (1, 1, 1))))
rbox((0, 0.35, 0.38), (1.4, 0.7, 0.07), mat((0.55, 0.33, 0.18), 0.35, coat=0.5), bevel=0.03)
for x in (-0.6, 0.6):
    for y in (0.1, 0.6):
        cyl((x, y, 0.18), 0.035, 0.36, mat((0.3, 0.18, 0.1), 0.4))
cyl((0.35, 0.4, 0.47), 0.07, 0.12, mat((0.95, 0.95, 0.95), 0.2, coat=0.6))
cyl((2.4, 1.9, 0.3), 0.28, 0.6, mat((0.85, 0.5, 0.35), 0.5))
for k in range(9):
    a = k * 0.7
    sphere((2.4 + math.cos(a) * 0.2, 1.9 + math.sin(a) * 0.2, 0.9 + (k % 3) * 0.22), 0.3, mat((0.2, 0.55, 0.25), 0.6),
           scale=(0.6, 0.6, 1.4), rot=(math.cos(a) * 0.4, math.sin(a) * 0.4, 0))

# characters
character("dave", -0.5, 1.45, sit=True, rz=-0.2, mood="smile")
character("chloe", 0.55, 1.45, sit=True, rz=0.2, mood="smile")

# lights: warm key, cool rim, soft fill, window glow
area((-3, -3, 4.5), (0, 1.5, 1.2), 900, 3, (1.0, 0.86, 0.7))
area((3.5, 3.5, 3.5), (0, 1.5, 1.3), 700, 2, (0.6, 0.75, 1.0))
area((0, -5, 1.5), (0, 1.5, 1.0), 200, 6, (1.0, 0.95, 0.9))
area((2.5, 2.2, 2.0), (0, 0, 1.0), 150, 1.5, (0.8, 0.9, 1.0))

# camera with depth of field
bpy.ops.object.camera_add(location=(0.3, -4.2, 1.75))
cam = bpy.context.object
cam.data.lens = 42
cam.rotation_euler = (V((0, 1.45, 1.35)) - cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = (V((0, 1.4, 1.5)) - cam.location).length
cam.data.dof.aperture_fstop = 0.9
sc.camera = cam

sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
