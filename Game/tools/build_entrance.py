"""Initial standalone second level: a damp, narrow Soviet-era entrance."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
scene = r'''[gd_scene load_steps=10 format=3]

[ext_resource type="Script" path="res://scripts/player.gd" id="1"]
[ext_resource type="Script" path="res://scripts/door.gd" id="2"]
[ext_resource type="PackedScene" path="res://assets/models/Mailboxes.glb" id="3"]
[ext_resource type="PackedScene" path="res://assets/models/Radiator.glb" id="4"]
[ext_resource type="PackedScene" path="res://assets/models/FuseBox.glb" id="5"]
[ext_resource type="PackedScene" path="res://assets/models/Door_17.glb" id="6"]
[ext_resource type="Script" path="res://scripts/apartment_door.gd" id="7"]
[ext_resource type="PackedScene" path="res://assets/models/CIS_NoticeBoard.glb" id="8"]
[ext_resource type="PackedScene" path="res://assets/models/WallLamp.glb" id="9"]
[ext_resource type="PackedScene" path="res://assets/models/Crate.glb" id="10"]
[ext_resource type="PackedScene" path="res://assets/models/CIS_PanelFacade.glb" id="11"]
[ext_resource type="PackedScene" path="res://assets/models/StreetLamp.glb" id="12"]

[sub_resource type="Environment" id="Env"]
background_mode = 1
background_color = Color(0.008, 0.012, 0.012, 1)
ambient_light_source = 3
ambient_light_color = Color(0.18, 0.22, 0.18, 1)
ambient_light_energy = 0.24
fog_enabled = true
fog_density = 0.025

[sub_resource type="CapsuleShape3D" id="PlayerShape"]
radius = 0.27
height = 1.75

[sub_resource type="StandardMaterial3D" id="FloorMat"]
albedo_color = Color(0.12, 0.115, 0.09, 1)
roughness = 1.0

[sub_resource type="StandardMaterial3D" id="WallMat"]
albedo_color = Color(0.25, 0.27, 0.22, 1)
roughness = 1.0

[sub_resource type="BoxMesh" id="FloorMesh"]
material = SubResource("FloorMat")
size = Vector3(4, 0.16, 12.5)

[sub_resource type="BoxShape3D" id="FloorShape"]
size = Vector3(4, 0.16, 12.5)

[sub_resource type="BoxMesh" id="WallMesh"]
material = SubResource("WallMat")
size = Vector3(0.18, 7.5, 19)

[sub_resource type="BoxShape3D" id="WallShape"]
size = Vector3(0.18, 7.5, 19)

[sub_resource type="BoxShape3D" id="ApartmentDoorShape"]
size = Vector3(1.05, 2.1, 0.16)

[node name="EntranceLevel" type="Node3D"]

[node name="Environment" type="WorldEnvironment" parent="."]
environment = SubResource("Env")

[node name="Floor" type="StaticBody3D" parent="."]
position = Vector3(0, -0.08, -4.8)
[node name="Mesh" type="MeshInstance3D" parent="Floor"]
mesh = SubResource("FloorMesh")
[node name="Shape" type="CollisionShape3D" parent="Floor"]
shape = SubResource("FloorShape")

[node name="LeftWall" type="StaticBody3D" parent="."]
position = Vector3(-2, 3.75, -8)
[node name="Mesh" type="MeshInstance3D" parent="LeftWall"]
mesh = SubResource("WallMesh")
[node name="Shape" type="CollisionShape3D" parent="LeftWall"]
shape = SubResource("WallShape")

[node name="RightWall" type="StaticBody3D" parent="."]
position = Vector3(2, 3.75, -8)
[node name="Mesh" type="MeshInstance3D" parent="RightWall"]
mesh = SubResource("WallMesh")
[node name="Shape" type="CollisionShape3D" parent="RightWall"]
shape = SubResource("WallShape")

[node name="Mailboxes" parent="." instance=ExtResource("3")]
position = Vector3(-1.78, 0, -2.8)
rotation = Vector3(0, 1.5708, 0)
[node name="Radiator" parent="." instance=ExtResource("4")]
position = Vector3(1.78, 0, -4.2)
rotation = Vector3(0, -1.5708, 0)
[node name="FuseBox" parent="." instance=ExtResource("5")]
position = Vector3(-1.86, 1.1, -5.2)
rotation = Vector3(0, 1.5708, 0)

[node name="Apartment17" type="Node3D" parent="."]
position = Vector3(-1.5, 3.8, -16.6)
script = ExtResource("7")
[node name="Door" parent="Apartment17" instance=ExtResource("6")]
[node name="Handle" type="StaticBody3D" parent="Apartment17"]
[node name="Shape" type="CollisionShape3D" parent="Apartment17/Handle"]
position = Vector3(0.5, 1.05, 0.14)
shape = SubResource("ApartmentDoorShape")

[node name="BuzzingLamp" type="OmniLight3D" parent="."]
position = Vector3(0, 2.9, -5)
light_color = Color(0.72, 0.76, 0.56, 1)
light_energy = 1.2
omni_range = 5.0
[node name="ColdLamp" type="OmniLight3D" parent="."]
position = Vector3(-1, 6.7, -13)
light_color = Color(0.34, 0.47, 0.46, 1)
light_energy = 0.8
omni_range = 4.0

[node name="NoticeBoard" parent="." instance=ExtResource("8")]
position = Vector3(1.8, 0.75, -2.4)
rotation = Vector3(0, -1.5708, 0)
[node name="LandingLamp" parent="." instance=ExtResource("9")]
position = Vector3(-1.8, 5.5, -12.8)
rotation = Vector3(0, 1.5708, 0)
[node name="ForgottenCrate" parent="." instance=ExtResource("10")]
position = Vector3(-1.65, 3.8, -14.1)

[node name="Player" type="CharacterBody3D" parent="." groups=["player"]]
position = Vector3(0, 0.12, 0)
script = ExtResource("1")
floor_snap_length = 0.3
[node name="CollisionShape3D" type="CollisionShape3D" parent="Player"]
position = Vector3(0, 0.875, 0)
shape = SubResource("PlayerShape")
[node name="Head" type="Node3D" parent="Player"]
position = Vector3(0, 1.62, 0)
[node name="Camera3D" type="Camera3D" parent="Player/Head"]
current = true
fov = 76.0
[node name="Flashlight" type="SpotLight3D" parent="Player/Head/Camera3D"]
position = Vector3(0.16, -0.16, -0.12)
light_color = Color(0.91, 0.93, 0.79, 1)
light_energy = 4.5
spot_range = 14.0
spot_angle = 34.0
shadow_enabled = true
[node name="InteractRay" type="RayCast3D" parent="Player/Head/Camera3D"]
target_position = Vector3(0, 0, -2.4)
'''
scene += r'''
[sub_resource type="StandardMaterial3D" id="Stain"]
albedo_color = Color(0.075, 0.095, 0.078, 1)
roughness = 1.0

[sub_resource type="BoxMesh" id="LandingMesh"]
material = SubResource("FloorMat")
size = Vector3(1.7, 0.12, 11.85)

[sub_resource type="ConcavePolygonShape3D" id="StairRamp"]
data = PackedVector3Array(-1.8, 0.02, -6, -0.2, 0.02, -6, -0.2, 1.6, -10, -1.8, 0.02, -6, -0.2, 1.6, -10, -1.8, 1.6, -10, -1.8, 1.6, -10, 1.8, 1.6, -10, 1.8, 1.6, -11, -1.8, 1.6, -10, 1.8, 1.6, -11, -1.8, 1.6, -11, 0.2, 1.6, -10, 1.8, 1.6, -10, 1.8, 3.8, -6, 0.2, 1.6, -10, 1.8, 3.8, -6, 0.2, 3.8, -6)
backface_collision = true

[node name="StairRamp" type="StaticBody3D" parent="."]
[node name="Shape" type="CollisionShape3D" parent="StairRamp"]
shape = SubResource("StairRamp")

[node name="UpperLanding" type="MeshInstance3D" parent="."]
position = Vector3(-1, 3.74, -11.45)
mesh = SubResource("LandingMesh")

[sub_resource type="BoxShape3D" id="UpperShape"]
size = Vector3(1.7, 0.12, 11.85)
[node name="UpperCollider" type="StaticBody3D" parent="."]
position = Vector3(-1, 3.74, -11.45)
[node name="Shape" type="CollisionShape3D" parent="UpperCollider"]
shape = SubResource("UpperShape")

[sub_resource type="BoxMesh" id="TopConnector"]
material = SubResource("FloorMat")
size = Vector3(3.6, 0.12, 0.7)
[sub_resource type="BoxShape3D" id="TopConnectorShape"]
size = Vector3(3.6, 0.12, 0.7)
[node name="TopConnector" type="StaticBody3D" parent="."]
position = Vector3(0, 3.74, -5.5)
[node name="Mesh" type="MeshInstance3D" parent="TopConnector"]
mesh = SubResource("TopConnector")
[node name="Shape" type="CollisionShape3D" parent="TopConnector"]
shape = SubResource("TopConnectorShape")

[node name="FirstFlight" type="Node3D" parent="."]
'''
for i in range(11):
    height = (i + 1) * 1.6 / 11
    z = -6 - (i + .5) * 4 / 11
    scene += f'''
[sub_resource type="BoxMesh" id="StepMesh{i}"]
material = SubResource("FloorMat")
size = Vector3(1.5, {height:.4f}, 0.36)
[node name="Step{i:02d}" type="MeshInstance3D" parent="FirstFlight"]
position = Vector3(-1, {height/2:.4f}, {z:.4f})
mesh = SubResource("StepMesh{i}")
'''
for i in range(11):
    height = 1.6 + (i + 1) * 2.2 / 11
    z = -10 + (i + .5) * 4 / 11
    scene += f'''
[sub_resource type="BoxMesh" id="ReturnMesh{i}"]
material = SubResource("FloorMat")
size = Vector3(1.5, {height:.4f}, 0.36)
[node name="ReturnStep{i:02d}" type="MeshInstance3D" parent="FirstFlight"]
position = Vector3(1, {height/2:.4f}, {z:.4f})
mesh = SubResource("ReturnMesh{i}")
'''
scene += r'''
[sub_resource type="BoxMesh" id="CeilingMesh"]
material = SubResource("WallMat")
size = Vector3(4, 0.15, 19)
[node name="Ceiling" type="MeshInstance3D" parent="."]
position = Vector3(0, 7.35, -8)
mesh = SubResource("CeilingMesh")

[sub_resource type="BoxMesh" id="VestibuleCeilingMesh"]
material = SubResource("WallMat")
size = Vector3(3.8, 0.12, 6.1)
[node name="VestibuleCeiling" type="MeshInstance3D" parent="."]
position = Vector3(0, 3.65, -1.6)
mesh = SubResource("VestibuleCeilingMesh")

[sub_resource type="BoxMesh" id="DampMesh"]
material = SubResource("Stain")
size = Vector3(0.025, 0.62, 2.1)
[node name="DampLeft" type="MeshInstance3D" parent="."]
position = Vector3(-1.89, 0.31, -5)
mesh = SubResource("DampMesh")
[node name="DampRight" type="MeshInstance3D" parent="."]
position = Vector3(1.89, 1.8, -13.5)
mesh = SubResource("DampMesh")
'''
scene += r'''
[sub_resource type="StandardMaterial3D" id="OldPaint"]
albedo_color = Color(0.12, 0.19, 0.17, 1)
roughness = 1.0
[sub_resource type="StandardMaterial3D" id="RailPaint"]
albedo_color = Color(0.15, 0.17, 0.16, 1)
metallic = 0.3
[sub_resource type="BoxMesh" id="PaintBand"]
material = SubResource("OldPaint")
size = Vector3(0.025, 1.35, 18.2)
[node name="PaintBandLeft" type="MeshInstance3D" parent="."]
position = Vector3(-1.895, 0.68, -8)
mesh = SubResource("PaintBand")
[node name="PaintBandRight" type="MeshInstance3D" parent="."]
position = Vector3(1.895, 0.68, -8)
mesh = SubResource("PaintBand")
[sub_resource type="BoxMesh" id="RailMesh"]
material = SubResource("RailPaint")
size = Vector3(0.06, 0.06, 4.4)
[node name="FirstHandrail" type="MeshInstance3D" parent="."]
position = Vector3(-0.15, 1.65, -8)
rotation = Vector3(-0.38, 0, 0)
mesh = SubResource("RailMesh")
[node name="ReturnHandrail" type="MeshInstance3D" parent="."]
position = Vector3(0.15, 2.7, -8)
rotation = Vector3(0.5, 0, 0)
mesh = SubResource("RailMesh")
[sub_resource type="BoxMesh" id="DividerMesh"]
material = SubResource("WallMat")
size = Vector3(0.12, 2.3, 3.8)
[sub_resource type="BoxShape3D" id="DividerShape"]
size = Vector3(0.12, 2.3, 3.8)
[node name="StairDivider" type="StaticBody3D" parent="."]
position = Vector3(0, 1.15, -8)
[node name="Mesh" type="MeshInstance3D" parent="StairDivider"]
mesh = SubResource("DividerMesh")
[node name="Shape" type="CollisionShape3D" parent="StairDivider"]
shape = SubResource("DividerShape")
[sub_resource type="BoxMesh" id="PipeMesh"]
material = SubResource("RailPaint")
size = Vector3(0.045, 6.4, 0.045)
[node name="PipeLeft" type="MeshInstance3D" parent="."]
position = Vector3(-1.76, 3.2, -1.8)
mesh = SubResource("PipeMesh")
[node name="PipeRight" type="MeshInstance3D" parent="."]
position = Vector3(1.76, 3.2, -10.6)
mesh = SubResource("PipeMesh")
[sub_resource type="BoxMesh" id="BlindDoorMesh"]
material = SubResource("FloorMat")
size = Vector3(0.08, 2.05, 0.94)
[node name="Apartment18" type="MeshInstance3D" parent="."]
position = Vector3(-1.84, 4.83, -12)
mesh = SubResource("BlindDoorMesh")
[node name="Apartment19" type="MeshInstance3D" parent="."]
position = Vector3(-1.84, 4.83, -9)
mesh = SubResource("BlindDoorMesh")
[sub_resource type="BoxMesh" id="LandingRailMesh"]
material = SubResource("RailPaint")
size = Vector3(0.08, 1.05, 10.9)
[sub_resource type="BoxShape3D" id="LandingRailShape"]
size = Vector3(0.08, 1.05, 10.9)
[node name="LandingGuardrail" type="StaticBody3D" parent="."]
position = Vector3(-0.1, 4.32, -11.6)
[node name="Mesh" type="MeshInstance3D" parent="LandingGuardrail"]
mesh = SubResource("LandingRailMesh")
[node name="Shape" type="CollisionShape3D" parent="LandingGuardrail"]
shape = SubResource("LandingRailShape")
[sub_resource type="BoxMesh" id="UnderStairMesh"]
material = SubResource("WallMat")
size = Vector3(3.8, 3.62, 0.16)
[sub_resource type="BoxShape3D" id="UnderStairShape"]
size = Vector3(3.8, 3.62, 0.16)
[node name="UnderStairWall" type="StaticBody3D" parent="."]
position = Vector3(0, 1.81, -11.1)
[node name="Mesh" type="MeshInstance3D" parent="UnderStairWall"]
mesh = SubResource("UnderStairMesh")
[node name="Shape" type="CollisionShape3D" parent="UnderStairWall"]
shape = SubResource("UnderStairShape")
[sub_resource type="BoxMesh" id="BackWallMesh"]
material = SubResource("WallMat")
size = Vector3(4, 7.5, 0.16)
[sub_resource type="BoxShape3D" id="BackWallShape"]
size = Vector3(4, 7.5, 0.16)
[node name="BackWall" type="StaticBody3D" parent="."]
position = Vector3(0, 3.75, -16.85)
[node name="Mesh" type="MeshInstance3D" parent="BackWall"]
mesh = SubResource("BackWallMesh")
[node name="Shape" type="CollisionShape3D" parent="BackWall"]
shape = SubResource("BackWallShape")
'''
scene += r'''
[sub_resource type="BoxMesh" id="FrontSideMesh"]
material = SubResource("WallMat")
size = Vector3(1.3, 7.5, 0.2)
[sub_resource type="BoxShape3D" id="FrontSideShape"]
size = Vector3(1.3, 7.5, 0.2)
[node name="FrontLeft" type="StaticBody3D" parent="."]
position = Vector3(-1.35, 3.75, 1.45)
[node name="Mesh" type="MeshInstance3D" parent="FrontLeft"]
mesh = SubResource("FrontSideMesh")
[node name="Shape" type="CollisionShape3D" parent="FrontLeft"]
shape = SubResource("FrontSideShape")
[node name="FrontRight" type="StaticBody3D" parent="."]
position = Vector3(1.35, 3.75, 1.45)
[node name="Mesh" type="MeshInstance3D" parent="FrontRight"]
mesh = SubResource("FrontSideMesh")
[node name="Shape" type="CollisionShape3D" parent="FrontRight"]
shape = SubResource("FrontSideShape")

[sub_resource type="BoxMesh" id="WindowSillMesh"]
material = SubResource("WallMat")
size = Vector3(1.4, 0.95, 0.2)
[sub_resource type="BoxShape3D" id="WindowSillShape"]
size = Vector3(1.4, 0.95, 0.2)
[node name="WindowSill" type="StaticBody3D" parent="."]
position = Vector3(0, 0.475, 1.45)
[node name="Mesh" type="MeshInstance3D" parent="WindowSill"]
mesh = SubResource("WindowSillMesh")
[node name="Shape" type="CollisionShape3D" parent="WindowSill"]
shape = SubResource("WindowSillShape")
[sub_resource type="BoxMesh" id="WindowHeaderMesh"]
material = SubResource("WallMat")
size = Vector3(1.4, 4.55, 0.2)
[sub_resource type="BoxShape3D" id="WindowHeaderShape"]
size = Vector3(1.4, 4.55, 0.2)
[node name="WindowHeader" type="StaticBody3D" parent="."]
position = Vector3(0, 5.225, 1.45)
[node name="Mesh" type="MeshInstance3D" parent="WindowHeader"]
mesh = SubResource("WindowHeaderMesh")
[node name="Shape" type="CollisionShape3D" parent="WindowHeader"]
shape = SubResource("WindowHeaderShape")
[sub_resource type="StandardMaterial3D" id="WindowGlass"]
albedo_color = Color(0.32, 0.46, 0.52, 0.19)
transparency = 1
cull_mode = 2
[sub_resource type="QuadMesh" id="WindowPane"]
material = SubResource("WindowGlass")
size = Vector2(1.34, 1.95)
[node name="StairwellWindow" type="MeshInstance3D" parent="."]
position = Vector3(0, 1.925, 1.46)
mesh = SubResource("WindowPane")
[sub_resource type="BoxShape3D" id="WindowGlassShape"]
size = Vector3(1.34, 1.95, 0.05)
[node name="WindowBarrier" type="StaticBody3D" parent="."]
position = Vector3(0, 1.925, 1.46)
[node name="Shape" type="CollisionShape3D" parent="WindowBarrier"]
shape = SubResource("WindowGlassShape")
[sub_resource type="BoxMesh" id="WindowMullionMesh"]
material = SubResource("RailPaint")
size = Vector3(0.045, 2.0, 0.05)
[node name="WindowMullion" type="MeshInstance3D" parent="."]
position = Vector3(0, 1.93, 1.4)
mesh = SubResource("WindowMullionMesh")
[sub_resource type="BoxMesh" id="WindowCrossbarMesh"]
material = SubResource("RailPaint")
size = Vector3(1.4, 0.04, 0.05)
[node name="WindowCrossbar" type="MeshInstance3D" parent="."]
position = Vector3(0, 1.92, 1.4)
mesh = SubResource("WindowCrossbarMesh")

[sub_resource type="BoxMesh" id="OutsideGroundMesh"]
material = SubResource("FloorMat")
size = Vector3(14, 0.08, 12)
[node name="ViewToCourtyard" type="MeshInstance3D" parent="."]
position = Vector3(0, -0.06, 6.4)
mesh = SubResource("OutsideGroundMesh")
[node name="OutsideFacadeLeft" parent="." instance=ExtResource("11")]
position = Vector3(-3, 0, 9)
rotation = Vector3(0, 3.141593, 0)
[node name="OutsideFacadeMiddle" parent="." instance=ExtResource("11")]
position = Vector3(0, 0, 9)
rotation = Vector3(0, 3.141593, 0)
[node name="OutsideFacadeRight" parent="." instance=ExtResource("11")]
position = Vector3(3, 0, 9)
rotation = Vector3(0, 3.141593, 0)
[node name="OutsideLamp" parent="." instance=ExtResource("12")]
position = Vector3(-2.1, 0, 5.3)
[node name="OutsideMoonlight" type="OmniLight3D" parent="."]
position = Vector3(0, 4.5, 5.8)
light_color = Color(0.48, 0.61, 0.76, 1)
light_energy = 1.5
omni_range = 11.0
'''
# Godot requires all resources before the first node, including generated step meshes.
resource_blocks = re.findall(r'\[sub_resource[^\n]*\]\n.*?(?=\n\[|\Z)', scene, re.S)
scene = re.sub(r'\[sub_resource[^\n]*\]\n.*?(?=\n\[|\Z)', '', scene, flags=re.S)
first_node = scene.index('[node name=')
scene = scene[:first_node] + '\n\n'.join(resource_blocks) + '\n\n' + scene[first_node:]
(root / 'scenes' / 'entrance_level.tscn').write_text(scene)
print('Entrance level generated')
