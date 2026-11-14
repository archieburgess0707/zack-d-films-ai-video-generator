"""Blender test scene: clay-style Earth + Moon. Run: blender -b -P blender/test_earth_moon.py -- out.png [frames]"""
import bpy, math, sys, random

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = argv[0] if argv else "/tmp/test.png"
frames = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else 1

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE" if "--eevee" in argv else "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 64
sc.cycles.use_denoising = False  # distro build lacks OpenImageDenoise
sc.render.resolution_x, sc.render.resolution_y = 720, 1280
sc.render.fps = 30
sc.frame_start, sc.frame_end = 1, frames

def mat(name, col, rough=0.55, sss=0.0, emit=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = rough
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = 3.0
    return m

def sphere(name, loc, r, m, seg=96):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.object; o.name = name
    bpy.ops.object.shade_smooth(); o.data.materials.append(m)
    return o

earth = sphere("Earth", (0, 0, 0), 1.0, mat("ocean", (0.05, 0.25, 0.8), 0.35))
random.seed(2)
land = mat("land", (0.12, 0.6, 0.2), 0.6, sss=0.1)
for k in range(9):
    th, ph = random.uniform(0, 6.28), random.uniform(-1.0, 1.0)
    p = (math.cos(th) * math.cos(ph) * 0.93, math.sin(th) * math.cos(ph) * 0.93, math.sin(ph) * 0.93)
    blob = sphere(f"land{k}", p, random.uniform(0.18, 0.34), land, seg=48)
    blob.scale = (1.0, 1.0, 0.45)
    blob.rotation_mode = "QUATERNION"
    blob.rotation_quaternion = (0, 0, 0, 1)
    import mathutils
    blob.rotation_quaternion = mathutils.Vector((0, 0, 1)).rotation_difference(mathutils.Vector(p).normalized())
    blob.parent = earth
moon = sphere("Moon", (1.6, -0.8, 1.9), 0.35, mat("moon", (0.75, 0.75, 0.78), 0.8))
for k in range(6):
    th, ph = random.uniform(0, 6.28), random.uniform(-1.2, 1.2)
    p = (math.cos(th) * math.cos(ph) * 0.34, math.sin(th) * math.cos(ph) * 0.34, math.sin(ph) * 0.34)
    c = sphere(f"crater{k}", (1.6 + p[0], -0.8 + p[1], 1.9 + p[2]), random.uniform(0.04, 0.08), mat(f"cr{k}", (0.55, 0.55, 0.58), 0.9), seg=24)
    c.parent = moon

earth.rotation_euler = (0, 0, 0)
earth.keyframe_insert("rotation_euler", frame=1)
earth.rotation_euler = (0, 0, math.radians(40 * frames / 30))
earth.keyframe_insert("rotation_euler", frame=max(2, frames))

bpy.ops.object.camera_add(location=(1.1, -7.5, 0.3), rotation=(math.radians(88), 0, math.radians(0)))
cam = bpy.context.object; sc.camera = cam; cam.data.lens = 40
bpy.ops.object.light_add(type="AREA", location=(-4, -4, 4)); key = bpy.context.object
key.data.energy = 1500; key.data.size = 4; key.rotation_euler = (math.radians(50), 0, math.radians(-45))
bpy.ops.object.light_add(type="AREA", location=(4, 2, 2)); rim = bpy.context.object
rim.data.energy = 600; rim.data.color = (0.5, 0.7, 1.0); rim.rotation_euler = (math.radians(70), 0, math.radians(120))

w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.01, 0.012, 0.04, 1)
sc.view_settings.view_transform = "AgX" if "AgX" in [i.identifier for i in sc.view_settings.bl_rna.properties["view_transform"].enum_items] else "Filmic"

sc.render.filepath = out
if frames == 1:
    bpy.ops.render.render(write_still=True)
else:
    sc.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(animation=True)
