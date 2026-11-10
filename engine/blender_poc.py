import bpy, math, os
from mathutils import Vector
# Clean scene
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes,bpy.data.curves,bpy.data.cameras,bpy.data.lights): pass
scene=bpy.context.scene
available_engines = {item.identifier for item in scene.render.bl_rna.properties['engine'].enum_items}\nscene.render.engine = 'BLENDER_EEVEE' if 'BLENDER_EEVEE' in available_engines else ('BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in available_engines else 'BLENDER_WORKBENCH')
scene.render.resolution_x=480; scene.render.resolution_y=854; scene.render.resolution_percentage=100
scene.render.fps=12; scene.frame_start=1; scene.frame_end=96
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.world.color=(0.025,0.035,0.06)
scene.view_settings.view_transform='Standard'
def mat(name,color,metal=0,rough=.45):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*color,1); p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
 return m
navy=mat('Midnight',(.018,.035,.075)); teal=mat('Electric teal',(.02,.55,.62),.25); skin=mat('Warm porcelain',(.92,.59,.39)); ink=mat('Ink',(.012,.018,.03)); gold=mat('Signal amber',(1,.48,.08),.25)
def cube(name,loc,scale,material,bevel=.12):
 bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o=bpy.context.object; o.name=name; o.dimensions=scale
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(material)
 if bevel:
  mod=o.modifiers.new('Soft manufactured edges','BEVEL'); mod.width=bevel; mod.segments=4
  o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
 return o
def sphere(name,loc,scale,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,radius=1,location=loc); o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material); bpy.ops.object.shade_smooth(); return o
# Stage, graphic backdrop and floor
cube('Backdrop',(0,0,0),(11,.3,18),navy,.2)
floor=cube('Stage floor',(0,0,-4.1),(11,8,.25),mat('Floor',(.035,.07,.11)),.08)
# camera
bpy.ops.object.camera_add(location=(0,-15,0)); cam=bpy.context.object; cam.rotation_euler=(math.radians(90),0,0); cam.data.type='ORTHO'; cam.data.ortho_scale=10.8; scene.camera=cam
def area(loc,power,size,color):
 bpy.ops.object.light_add(type='AREA',location=loc); l=bpy.context.object; l.data.energy=power; l.data.shape='DISK'; l.data.size=size; l.data.color=color; l.rotation_euler=(Vector((0,0,0))-l.location).to_track_quat('-Z','Y').to_euler()
area((4,-7,6),950,7,(.45,.85,1)); area((-5,-3,1),700,5,(1,.35,.12)); area((0,3,4),1100,4,(.1,.7,1))
# Character rig made from linked pivot empties and articulated parts
root=bpy.data.objects.new('CHARACTER_ROOT',None); scene.collection.objects.link(root)
def parent(o,p,loc=None):
 o.parent=p
 if loc is not None: o.location=loc
 return o
torso=parent(cube('Jacket',(0,0,0),(1.15,.62,1.65),teal,.28),root,(0,0,-.25))
head=parent(sphere('Head',(0,0,0),(.62,.52,.68),skin),root,(0,-.02,.95))
hair=parent(sphere('Hair',(0,0,0),(.64,.54,.34),ink),head,(0,-.02,.48))
# eyes and mouth on camera-facing side
for x in (-.22,.22): parent(sphere('Eye',(0,0,0),(.07,.045,.1),ink),head,(x,-.51,.03))
parent(sphere('Nose',(0,0,0),(.07,.07,.08),gold),head,(0,-.57,-.12))
# limbs with pivot objects
limbs=[]
for side in (-1,1):
 arm=bpy.data.objects.new('ARM_PIVOT',None); scene.collection.objects.link(arm); arm.parent=root; arm.location=(side*.68,0,.25)
 upper=parent(sphere('Sleeve',(0,0,0),(.22,.23,.62),teal),arm,(0,0,-.34)); upper.rotation_euler[1]=side*.12
 hand=parent(sphere('Glove',(0,0,0),(.19,.18,.2),skin),arm,(0,0,-.72))
 leg=bpy.data.objects.new('LEG_PIVOT',None); scene.collection.objects.link(leg); leg.parent=root; leg.location=(side*.32,0,-1.05)
 thigh=parent(sphere('Trouser',(0,0,0),(.25,.25,.55),ink),leg,(0,0,-.35))
 boot=parent(cube('Boot',(0,0,0),(.42,.55,.22),gold,.08),leg,(0,-.08,-.72))
 limbs.append((arm,leg,side))
# floating prop and target
prop=sphere('Floating glowing orb',(2,-.1,-1),(.36,.36,.36),gold)
# Title card text geometry
def txt(body,loc,size,material):
 c=bpy.data.curves.new('Title','FONT'); c.body=body; c.size=size; c.align_x='CENTER'; c.extrude=.006
 o=bpy.data.objects.new('Title',c); scene.collection.objects.link(o); o.location=loc; o.rotation_euler=(math.radians(90),0,0); o.data.materials.append(material); return o
title=txt('ONE BAD IDEA',(0,-.65,3.65),.48,teal)
subtitle=txt('A SILENT PHYSICAL COMEDY TEST',(0,-.65,3.12),.16,gold)
# animation keyframes: approach, leap, stumble/fall, recovery
def key(obj,frame,loc=None,rot=None):
 if loc is not None: obj.location=loc; obj.keyframe_insert(data_path='location',frame=frame)
 if rot is not None: obj.rotation_euler=rot; obj.keyframe_insert(data_path='rotation_euler',frame=frame)
for f,x in [(1,-2.8),(20,-1.8),(36,-.5),(52,.2),(68,.9),(84,1.1),(96,1.1)]: key(root,f,(x,0,0))
for arm,leg,side in limbs:
 for f,a in [(1,side*.1),(12,side*.75),(24,-side*.75),(36,side*.2),(48,side*1.1),(60,-side*.9),(72,side*.2),(84,side*.7),(96,0)]:
  key(arm,f,rot=(0,a,side*.12))
 for f,a in [(1,side*.05),(12,-side*.7),(24,side*.7),(36,0),(48,-side*.95),(60,side*.95),(72,0),(84,-side*.4),(96,0)]:
  key(leg,f,rot=(0,a,0))
for f,z in [(1,0),(25,0),(34,1.0),(42,1.0),(50,0),(58,-.75),(70,-.75),(82,0),(96,0)]:
 key(root,f,loc=({1:-2.8,25:-1.1,34:-.7,42:-.2,50:.1,58:.5,70:.9,82:1.1,96:1.1}[f],0,z))
for f,r in [(1,0),(48,0),(58,1.15),(70,1.15),(82,0),(96,0)]: key(root,f,rot=(0,r,0))
for f,loc in [(1,(2,-.1,-1)),(25,(2,-.1,-1)),(35,(.7,-.1,1.5)),(48,(.7,-.1,1.5)),(60,(2.5,-.1,-2.5)),(96,(2.5,-.1,-2.5))]:
 key(prop,f,loc=loc)
# camera slight push-in
for f,s in [(1,11.5),(96,10.2)]: cam.data.ortho_scale=s; cam.data.keyframe_insert(data_path='ortho_scale',frame=f)
# color management and output
scene.render.image_settings.file_format='PNG'
out=os.path.abspath('rendered/frame_'); os.makedirs('rendered',exist_ok=True); scene.render.filepath=out
scene.frame_set(1)
bpy.ops.render.render(animation=True)
