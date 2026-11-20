"""Builds an editable Godot scene from the original Night Shift art kit."""
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1]
MODELS=sorted(p.stem for p in (ROOT/'assets/models').glob('*.glb'))
ext={n:i+5 for i,n in enumerate(MODELS)}
lines=['[gd_scene load_steps=100 format=3]', '', '[ext_resource type="Script" path="res://scripts/player.gd" id="1"]','[ext_resource type="Script" path="res://scripts/door.gd" id="2"]','[ext_resource type="Script" path="res://scripts/yard_action.gd" id="3"]','[ext_resource type="Script" path="res://scripts/garage_door.gd" id="4"]','[ext_resource type="Script" path="res://scripts/level_exit.gd" id="exit"]','[ext_resource type="Texture2D" path="res://assets/textures/missing-poster.png" id="poster"]']
for n in MODELS:lines.append(f'[ext_resource type="PackedScene" path="res://assets/models/{n}.glb" id="{ext[n]}"]')
for i,n in enumerate(['asphalt','soil','concrete']):lines.append(f'[ext_resource type="Texture2D" path="res://assets/textures/{n}.png" id="tex{i}"]')
lines+=['''
[sub_resource type="Environment" id="Environment"]
background_mode = 1
background_color = Color(0.018, 0.025, 0.035, 1)
background_energy_multiplier = 0.5
ambient_light_source = 3
ambient_light_color = Color(0.26, 0.32, 0.4, 1)
ambient_light_energy = 0.42
reflected_light_source = 2
tonemap_mode = 2
fog_enabled = true
fog_light_color = Color(0.06, 0.08, 0.1, 1)
fog_light_energy = 0.22
fog_density = 0.011

[sub_resource type="CapsuleShape3D" id="PlayerShape"]
radius = 0.27
height = 1.75

[sub_resource type="StandardMaterial3D" id="Grass"]
albedo_color = Color(0.14, 0.19, 0.13, 1)
roughness = 1.0

[sub_resource type="StandardMaterial3D" id="Wall"]
albedo_color = Color(0.32, 0.36, 0.31, 1)
roughness = 1.0

[sub_resource type="StandardMaterial3D" id="Roof"]
albedo_color = Color(0.09, 0.12, 0.13, 1)
roughness = 1.0

[sub_resource type="StandardMaterial3D" id="WarmWindow"]
albedo_color = Color(0.45, 0.3, 0.13, 1)
emission_enabled = true
emission = Color(0.78, 0.48, 0.2, 1)
emission_energy_multiplier = 0.65

[sub_resource type="StandardMaterial3D" id="GarageShutter"]
albedo_color = Color(0.12, 0.13, 0.13, 1)
metallic = 0.25
roughness = 0.75

[sub_resource type="StandardMaterial3D" id="Poster"]
albedo_texture = ExtResource("poster")
roughness = 1.0
cull_mode = 2

[sub_resource type="StandardMaterial3D" id="WallGrime"]
albedo_color = Color(0.13, 0.16, 0.13, 1)
roughness = 1.0
''']
for i,n in enumerate(['Asphalt','Soil','Concrete']):lines.append(f'''[sub_resource type="StandardMaterial3D" id="{n}"]
albedo_texture = ExtResource("tex{i}")
uv1_triplanar = true
uv1_scale = Vector3(0.5, 0.5, 0.5)
texture_filter = 2
roughness = 1.0
''')
resources=[];nodes=['[node name="TikhayaStreet" type="Node3D"]']
count=0

def vec(v):return 'Vector3('+', '.join(f'{x:.6f}' for x in v)+')'
def group(name):nodes.append(f'[node name="{name}" type="Node3D" parent="."]')
def instance(name,pos,yaw=0,parent='Props',scale=None):
 global count
 count+=1;node=f'{name}_{count}'
 nodes.append(f'[node name="{node}" parent="{parent}" instance=ExtResource("{ext[name]}")]\nposition = {vec(pos)}\nrotation = {vec((0,math.radians(yaw),0))}')
 if scale:nodes.append('scale = '+vec(scale))
 return f'{parent}/{node}'
def box(name,pos,size,mat='Concrete',parent='Collision',collision=True,angle=0):
 global count
 count+=1;rid=f'b{count}';node=f'{name}_{count}'
 resources.append(f'[sub_resource type="BoxMesh" id="m{rid}"]\nmaterial = SubResource("{mat}")\nsize = {vec(size)}')
 if collision:
  resources.append(f'[sub_resource type="BoxShape3D" id="s{rid}"]\nsize = {vec(size)}')
  nodes.append(f'[node name="{node}" type="StaticBody3D" parent="{parent}"]\nposition = {vec(pos)}\nrotation = {vec((angle,0,0))}')
  nodes.append(f'[node name="Mesh" type="MeshInstance3D" parent="{parent}/{node}"]\nmesh = SubResource("m{rid}")')
  nodes.append(f'[node name="Shape" type="CollisionShape3D" parent="{parent}/{node}"]\nshape = SubResource("s{rid}")')
 else:nodes.append(f'[node name="{node}" type="MeshInstance3D" parent="{parent}"]\nposition = {vec(pos)}\nrotation = {vec((angle,0,0))}\nmesh = SubResource("m{rid}")')
def invisible_box(name,pos,size,parent='Collision'):
 global count
 count+=1;rid=f's{count}';resources.append(f'[sub_resource type="BoxShape3D" id="{rid}"]\nsize = {vec(size)}')
 nodes.append(f'[node name="{name}_{count}" type="StaticBody3D" parent="{parent}"]\nposition = {vec(pos)}')
 nodes.append(f'[node name="Shape" type="CollisionShape3D" parent="{parent}/{name}_{count}"]\nshape = SubResource("{rid}")')
def light(name,pos,energy=3,radius=9,color=(1,.68,.38),parent='Lighting'):
 global count
 count+=1;nodes.append(f'[node name="{name}_{count}" type="OmniLight3D" parent="{parent}"]\nposition = {vec(pos)}\nlight_color = Color({color[0]}, {color[1]}, {color[2]}, 1)\nlight_energy = {energy}\nomni_range = {radius}\nshadow_enabled = true\nshadow_bias = 0.08')
def yard_action(name,pos,size,prompt,message,action_id,action_type='inspect',parent='Props'):
 global count
 count+=1;rid=f'ya{count}'
 resources.append(f'[sub_resource type="BoxShape3D" id="{rid}"]\nsize = {vec(size)}')
 nodes.append(f'[node name="{name}" type="Node3D" parent="{parent}"]\nposition = {vec(pos)}\nscript = ExtResource("3")\nprompt = "{prompt}"\nmessage = "{message}"\naction_id = "{action_id}"\naction_type = "{action_type}"')
 nodes.append(f'[node name="Body" type="StaticBody3D" parent="{parent}/{name}"]')
 nodes.append(f'[node name="Shape" type="CollisionShape3D" parent="{parent}/{name}/Body"]\nshape = SubResource("{rid}")')
def garage_door(name,x):
 global count
 count+=1; shape=f'gs{count}'
 resources.append(f'[sub_resource type="BoxShape3D" id="{shape}"]\nsize = Vector3(2.8, 2.5, 0.18)')
 nodes.append(f'[node name="{name}" type="Node3D" parent="Props"]\nposition = Vector3({x}, 0, 14.1)\nrotation = Vector3(0, 3.141593, 0)\nscript = ExtResource("4")')
 nodes.append(f'[node name="LeftDoor" parent="Props/{name}" instance=ExtResource("{ext["CIS_GarageDoorLeft"]}")]\nposition = Vector3(-1.57, 0, 2.64)')
 nodes.append(f'[node name="RightDoor" parent="Props/{name}" instance=ExtResource("{ext["CIS_GarageDoorRight"]}")]\nposition = Vector3(1.57, 0, 2.64)')
 nodes.append(f'[node name="Blocker" type="StaticBody3D" parent="Props/{name}"]')
 nodes.append(f'[node name="Shape" type="CollisionShape3D" parent="Props/{name}/Blocker"]\nposition = Vector3(0, 1.25, 2.64)\nshape = SubResource("{shape}")')
def poster(name,pos,width,height,yaw=0,parent='Props'):
 global count
 count+=1; rid=f'poster{count}'
 resources.append(f'[sub_resource type="QuadMesh" id="{rid}"]\nmaterial = SubResource("Poster")\nsize = Vector2({width}, {height})')
 nodes.append(f'[node name="{name}" type="MeshInstance3D" parent="{parent}"]\nposition = {vec(pos)}\nrotation = Vector3(0, {math.radians(yaw)}, 0)\nmesh = SubResource("{rid}")')
for name in ['Architecture','Props','Collision','Lighting','Entrance','Playground']:group(name)
nodes.append('[node name="WorldEnvironment" type="WorldEnvironment" parent="Lighting"]\nenvironment = SubResource("Environment")')
nodes.append('[node name="Moon" type="DirectionalLight3D" parent="Lighting"]\nrotation_degrees = Vector3(-43, -28, 0)\nlight_color = Color(0.42, 0.54, 0.7, 1)\nlight_energy = 0.42\nshadow_enabled = true\ndirectional_shadow_max_distance = 52.0')
# Ground and actual perimeter prevent leaving the prototype.
box('CourtyardGround',(0,-.22,1),(34,.4,36),'Asphalt')
box('NorthBuildingBack',(-8.25,5.6,-14.2),(13.5,11.2,.4),'Wall')
box('NorthBuildingBack',(8.25,5.6,-14.2),(13.5,11.2,.4),'Wall')
box('NorthHeader',(0,7,-14.2),(3,8.4,.4),'Wall')
for side in [-1,1]:
 box('BuildingSide',(side*15.2,5.6,1),(.4,11.2,30.5),'Wall')
 for z in range(-12,16,3):
  for floor in range(4):instance('CIS_PanelFacade',(side*15,floor*2.8,z),90 if side<0 else -90,'Architecture')
 for x in [-12,-9,-6,-3,3,6,9,12]:
  if x*side<0:continue
  for floor in range(4):instance('CIS_PanelFacade',(x,floor*2.8,-14),parent='Architecture')
# Facade above the door bay.
for floor in range(1,4):instance('CIS_PanelFacade',(0,floor*2.8,-14),parent='Architecture')
for x,y in [(-9,2.8),(-3,5.6),(6,2.8),(12,8.4)]:instance('CIS_GlazedBalcony',(x,y,-14),0,'Architecture')
# Place light on the recessed glazing, behind the frame and mullions of each 3 m bay.
for x,floor in [(-6,2),(3,1),(9,0)]:
 box('LitWindow',(x,floor*2.8+1.62,-13.992),(1.27,1.22,.012),'WarmWindow','Architecture',False)
# Dark damp streaks climb from the ground at irregular intervals; none cover the glazing.
for x,w,h in [(-12.5,.38,.84),(-10.4,.7,.53),(-7.6,.42,1.07),(-4.4,.55,.7),(4.2,.48,.93),(7.4,.65,.62),(10.7,.38,1.1)]:
 box('WallDamp',(x,h/2,-13.862),(w,h,.012),'WallGrime','Architecture',False)
for x in [-12.2,-8.7,-5.3,5.8,9.4,12.1]:
 box('WallDrip',(x,2.15,-13.855),(.12,.36,.012),'WallGrime','Architecture',False)
# Walkways and overgrown rectangles; curbs are low enough for walking.
for x in [-13.3,13.3]:box('Walkway',(x,-.005,1),(2.9,.08,30),'Concrete')
box('EntryWalk',(0,-.005,-10.5),(3,.08,7),'Concrete')
for x in [-6,6]:
 # Visual-only soil and curbs: the courtyard ground underneath supplies one clean floor collider.
 box('GrassBed',(x,-.045,-2),(7,.09,9),'Soil',collision=False)
 for edge in [-1,1]:box('Curb',(x+edge*3.55,.035,-2),(.1,.09,9.2),'Concrete',collision=False)
 for z in [-6.55,2.55]:box('Curb',(x,.035,z),(7.2,.09,.1),'Concrete',collision=False)
# South enclosure, gate opening and garage row.
for x in [-13.5,-10.7,-7.9,7.9,10.7,13.5]:instance('CIS_ConcreteFence',(x,0,18),180,'Architecture')
invisible_box('SouthFenceLeft',(-9,1,18),(12,2,.2));invisible_box('SouthFenceRight',(9,1,18),(12,2,.2))
box('GateLeft',(-2.1,1,18),(2.2,2,.18),'Roof');box('GateRight',(2.1,1,18),(2.2,2,.18),'Roof')
box('GateClosed',(0,1,18),(2,2,.18),'Roof')
for x in [-9,-5.6]:
 instance('CIS_GarageShell',(x,0,14.1),180,'Architecture')
 garage_door('GarageDoorLeft' if x < -7 else 'GarageDoorRight',x)
 # Readable only when the doors swing open: concrete floor, rear wall, abandoned crates and a weak work bulb.
 box('GarageFloor',(x,.02,14.2),(2.95,.08,5.0),'Concrete','Architecture',False)
 box('GarageBack',(x,1.25,16.62),(3.0,2.5,.12),'Roof','Architecture',False)
 # Real structural collision: walls and back stay solid, only the door opening is released.
 invisible_box('GarageSide',(x-1.55,1.25,14.15),(.15,2.5,5.1))
 invisible_box('GarageSide',(x+1.55,1.25,14.15),(.15,2.5,5.1))
 invisible_box('GarageBack',(x,1.25,16.55),(3.1,2.5,.18))
 instance('Crate',(x-.62,0,15.25),parent='Props');instance('Crate',(x+.42,0,15.7),parent='Props')
 light('GarageBulb',(x,2.15,15.5),.5,2.4,(.7,.63,.4))
instance('CIS_Kiosk',(10.5,0,13.8),-22,'Architecture');invisible_box('Kiosk',(10.5,1.25,13.8),(3.15,2.6,2.5))
# Play area is deliberately off the main route.
instance('CIS_Sandbox',(6,0,-1),parent='Playground');invisible_box('Sandbox',(6,.16,-1),(2.6,.32,2.6))
instance('CIS_PullUpBars',(8.8,0,-4),90,'Playground')
for z in [-5.2,-4,-2.8]:invisible_box('BarPost',(8.8,1.1,z),(.12,2.2,.12))
instance('CIS_CourtyardTable',(-6,0,-2),parent='Props');invisible_box('CourtyardTable',(-6,.4,-2),(1.55,.8,1.85))
# A paper clue on the table, raised so the interaction ray can find it easily.
box('YardNote',(-6,.84,-2),(0.34,.025,.48),'WarmWindow','Props',False,math.radians(-4))
yard_action('TableNote',(-6,.95,-2),(1.5,.55,1.8),'E  ·  Прочитать записку','На обороте квитанции: «Не включай свет после полуночи».','note')
for p in [(-3.1,0,5),(3.1,0,5),(-2,0,-7),(2,0,-7)]:instance('CIS_TirePlanter',p);invisible_box('Tire',(p[0],.15,p[2]),(.8,.3,.8))
for x,z,yaw in [(-11.5,-6,90),(11.5,5,-90)]:
 instance('Bench',(x,0,z),yaw);invisible_box('Bench',(x,.45,z),(.55,.9,1.65))
for x,z in [(-11,9),(11,-9),(-11,-10)]:
 instance('StreetLamp',(x,0,z));light('StreetLight',(x,3.65,z+.8),1.75,9,(.94,.75,.52))
 invisible_box('LampPost',(x,1.8,z),(.18,3.6,.18))
for x,z in [(12,10),(12.5,8.5)]:instance('Dumpster',(x,0,z));invisible_box('Dumpster',(x,.65,z),(1.8,1.3,1.15))
for x,z in [(-2,10),(4,8),(-10,-9)]:instance('Manhole',(x,.01,z))
for x in [-1.6,1.6]:instance('Bollard',(x,0,12));invisible_box('Bollard',(x,.4,12),(.2,.8,.2))
instance('TrafficCone',(9,0,10));instance('Crate',(8.8,0,12));invisible_box('Crate',(8.8,.25,12),(.65,.5,.6))
# The electrical box is bolted to the side wall of the left garage, never to a window or free-standing wall.
instance('FuseBox',(-10.66,1.05,14.2),90,'Props')
yard_action('YardLightSwitch',(-10.35,1.15,14.2),(.65,1.3,.9),'E  ·  Включить дворовый свет','', 'light', 'light_switch')
nodes.append('[node name="YardFloodlight" type="OmniLight3D" parent="Lighting" groups=["yard_floodlights"]]\nposition = Vector3(0, 5.8, 1)\nlight_color = Color(0.58, 0.72, 0.9, 1)\nlight_energy = 4.2\nomni_range = 19.0\nshadow_enabled = true\nvisible = false')
# Kiosk rear wall faces into the yard; keep the original image's 1295:1215 proportions.
poster('MissingPoster',(10.845,1.44,12.929),1.38,1.295,158)
yard_action('GaragePoster',(10.845,1.44,12.69),(1.55,1.55,.4),'E  ·  Прочитать объявление','На ларьке приклеено объявление: «ТЫ ЕГО ВИДЕЛ?»','poster')
# Playable vestibule behind the north facade.
box('LobbyFloor',(0,-.05,-17.6),(3.1,.1,7.2),'Concrete','Entrance')
for x in [-1.55,1.55]:box('LobbyWall',(x,1.8,-18.3),(.2,3.6,8.5),'Wall','Entrance')
box('LobbyCeiling',(0,3.5,-18),(3.3,.16,8),'Roof','Entrance')
for x in [-1.03,1.03]:box('DoorwaySide',(x,1.4,-14),(.94,2.8,.25),'Wall','Entrance')
box('DoorwayLintel',(0,2.51,-14),(1.16,.58,.25),'Wall','Entrance')
instance('CIS_EntranceCanopy',(0,2.7,-13.6),parent='Entrance')
instance('CIS_EntrySign',(1.1,2.15,-13.83),parent='Entrance');instance('CIS_Intercom',(.89,1.4,-13.8),parent='Entrance')
instance('CIS_NoticeBoard',(-1.05,.8,-13.83),parent='Entrance')
nodes.append('[node name="EntryDoor" type="Node3D" parent="Entrance"]\nposition = Vector3(-0.48, 0, -14)\nscript = ExtResource("2")')
instance('CIS_EntranceDoor',(0,0,0),parent='Entrance/EntryDoor')
invisible_box('DoorCollider',(.48,1.07,0),(.96,2.14,.09),'Entrance/EntryDoor')
instance('Mailboxes',(-1.4,.8,-16),90,'Entrance');instance('Radiator',(1.36,0,-17),-90,'Entrance')
instance('FuseBox',(-1.35,1.1,-18.4),90,'Entrance')
for z in [-15.2,-19]:
 instance('WallLamp',(0,2.6,z),parent='Entrance');light('LobbyLamp',(0,2.5,z),2.1,5,(.87,.8,.52))
# Stair geometry uses a smooth ramp collider for CharacterBody3D traversal.
for i in range(9):box('StairStep',(0,(i+1)*.14/2,-19.6-i*.28),(2.5,(i+1)*.14,.28),'Concrete','Entrance',False)
# Trimesh ramp: precise top surface, no tall collision lip at the first step.
resources.append('[sub_resource type="ConcavePolygonShape3D" id="StairRamp"]\ndata = PackedVector3Array(-1.25, 0.02, -19.46, 1.25, 0.02, -19.46, 1.25, 1.26, -21.98, -1.25, 0.02, -19.46, 1.25, 1.26, -21.98, -1.25, 1.26, -21.98, -1.25, 1.26, -21.98, 1.25, 1.26, -21.98, 1.25, 1.26, -23.4, -1.25, 1.26, -21.98, 1.25, 1.26, -23.4, -1.25, 1.26, -23.4)\nbackface_collision = true')
nodes.append('[node name="StairRamp" type="StaticBody3D" parent="Entrance"]\n[node name="Shape" type="CollisionShape3D" parent="Entrance/StairRamp"]\nshape = SubResource("StairRamp")')
box('Landing',(0,1.2,-22.7),(3,.12,1.5),'Concrete','Entrance',False)
box('LandingBack',(0,1.7,-23.5),(3.3,3.4,.2),'Wall','Entrance')
box('RearCeiling',(0,3.5,-22),(3.3,.1,3),'Roof','Entrance')
instance('DoorFrame',(0,1.27,-23.3),parent='Entrance')
nodes.append('[node name="StairwellExit" type="Node3D" parent="Entrance"]\nposition = Vector3(-0.55, 1.27, -23.3)\nscript = ExtResource("exit")')
instance('Door_17',(0,0,0),parent='Entrance/StairwellExit')
invisible_box('DoorHandle',(.52,1.05,.14),(1.05,2.1,.18),'Entrance/StairwellExit')
light('LandingLight',(0,3.2,-22.4),1.3,4,(.65,.76,.7))
# Spawn faces the entrance; the whole map is available for editing in Scene dock.
nodes.append('''[node name="Player" type="CharacterBody3D" parent="." groups=["player"]]
position = Vector3(0, 0.12, 14)
script = ExtResource("1")
floor_snap_length = 0.3
floor_max_angle = 0.65

[node name="CollisionShape3D" type="CollisionShape3D" parent="Player"]
position = Vector3(0, 0.875, 0)
shape = SubResource("PlayerShape")

[node name="Head" type="Node3D" parent="Player"]
position = Vector3(0, 1.62, 0)

[node name="Camera3D" type="Camera3D" parent="Player/Head"]
current = true
fov = 76.0
near = 0.04
far = 120.0

[node name="Flashlight" type="SpotLight3D" parent="Player/Head/Camera3D"]
position = Vector3(0.16, -0.16, -0.12)
light_color = Color(0.91, 0.93, 0.79, 1)
light_energy = 5.0
spot_range = 18.0
spot_angle = 34.0
spot_attenuation = 0.75
spot_angle_attenuation = 1.4
shadow_enabled = true

[node name="InteractRay" type="RayCast3D" parent="Player/Head/Camera3D"]
target_position = Vector3(0, 0, -2.4)
collision_mask = 1
''')
# load_steps is a hint; calculate it rather than leaving the preliminary value.
lines[0]=f'[gd_scene load_steps={len(MODELS)+5+len(resources)+10} format=3]'
(ROOT/'scenes/courtyard.tscn').write_text('\n\n'.join(lines+resources+nodes)+'\n')
print('Map generated:',count,'objects')
