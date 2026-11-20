extends Node3D

var travelling := false

func interaction_prompt() -> String:
	return "E  ·  Войти в лестничную клетку"

func interact() -> void:
	if travelling:
		return
	travelling = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	get_tree().call_deferred("change_scene_to_file", "res://scenes/entrance_level.tscn")
