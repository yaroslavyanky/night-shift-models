extends Node3D

var is_open := false
var moving := false

func interaction_prompt() -> String:
	return "E  ·  Закрыть дверь" if is_open else "E  ·  Открыть подъезд"

func interact() -> void:
	if moving: return
	moving = true
	is_open = not is_open
	var tween := create_tween()
	tween.tween_property(self, "rotation:y", deg_to_rad(-105.0) if is_open else 0.0, 0.6).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT)
	tween.finished.connect(func(): moving = false)
