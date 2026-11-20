extends SceneTree

func _initialize() -> void:
	call_deferred("check")

func check() -> void:
	var packed: PackedScene = load("res://scenes/courtyard.tscn")
	var courtyard: Node = packed.instantiate()
	root.add_child(courtyard)
	current_scene = courtyard
	var exit_door: Node = courtyard.get_node("Entrance/StairwellExit")
	assert(exit_door.has_method("interact"))
	exit_door.interact()
	for i in range(5): await process_frame
	assert(current_scene != null and current_scene.name == "EntranceLevel", "Scene transition did not reach entrance")
	assert(current_scene.get_node("Apartment17").has_method("interact"))
	print("TRANSITION CHECK PASSED: courtyard to entrance level")
	quit(0)
