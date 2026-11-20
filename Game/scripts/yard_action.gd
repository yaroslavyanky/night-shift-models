extends Node3D

@export var prompt := "E  ·  Осмотреть"
@export_multiline var message := "Здесь что-то есть."
@export var action_id := "yard_action"
@export_enum("inspect", "light_switch") var action_type := "inspect"

var switch_on := false

func interaction_prompt() -> String:
	if action_type == "light_switch":
		return "E  ·  Выключить дворовый свет" if switch_on else "E  ·  Включить дворовый свет"
	return prompt

func interact() -> void:
	var shown_message := message
	if action_type == "light_switch":
		switch_on = not switch_on
		for light in get_tree().get_nodes_in_group("yard_floodlights"):
			light.visible = switch_on
		shown_message = "Свет во дворе включён. В дальнем окне будто кто-то отошёл от занавески." if switch_on else "Свет во дворе снова погас."
	var player := get_tree().get_first_node_in_group("player")
	if player != null and player.has_method("record_yard_action"):
		player.record_yard_action(action_id, shown_message)
