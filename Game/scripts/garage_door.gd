extends Node3D

@onready var left_door: Node3D = $LeftDoor
@onready var right_door: Node3D = $RightDoor
@onready var blocker: CollisionShape3D = $Blocker/Shape
var open := false
var moving := false

func interaction_prompt() -> String:
	return "E  ·  Закрыть гараж" if open else "E  ·  Поднять дверь гаража"

func interact() -> void:
	if moving:
		return
	moving = true
	open = not open
	blocker.disabled = open
	var tween := create_tween()
	# Swing out toward the courtyard; the opposite signs would send panels into the garage shell.
	tween.parallel().tween_property(left_door, "rotation:y", deg_to_rad(-105.0) if open else 0.0, 0.65).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT)
	tween.parallel().tween_property(right_door, "rotation:y", deg_to_rad(105.0) if open else 0.0, 0.65).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT)
	tween.finished.connect(func(): moving = false)
