extends Node3D

func interaction_prompt() -> String:
	return "E  ·  Проверить квартиру 17"

func interact() -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player != null:
		player.show_event_message("Дверь заперта изнутри. За ней на секунду скрипнул пол.\nНужно найти другой путь или ключ.")
