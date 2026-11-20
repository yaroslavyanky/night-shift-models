extends SceneTree

func _initialize() -> void:
	call_deferred("check")

func check() -> void:
	var level: PackedScene = load("res://scenes/entrance_level.tscn")
	assert(level != null)
	var map := level.instantiate()
	root.add_child(map)
	var player: CharacterBody3D = map.get_node("Player")
	player.set_physics_process(false)
	for i in range(12): await physics_frame
	var space := player.get_world_3d().direct_space_state
	for endpoints in [[Vector3(-0.7, 1, -8), Vector3(0.7, 1, -8)], [Vector3(-0.6, 4.3, -12), Vector3(0.6, 4.3, -12)]]:
		var query := PhysicsRayQueryParameters3D.create(endpoints[0], endpoints[1])
		query.exclude = [player.get_rid()]
		assert(not space.intersect_ray(query).is_empty(), "Missing stair partition or landing guardrail")
	var void_query := PhysicsRayQueryParameters3D.create(Vector3(0, 2.5, -10.5), Vector3(0, 2.5, -11.5))
	assert("UnderStairWall" in space.intersect_ray(void_query).collider.name, "Half landing still opens onto the void")
	var window_query := PhysicsRayQueryParameters3D.create(Vector3(0, 1.9, 0), Vector3(0, 1.9, 3))
	assert("WindowBarrier" in space.intersect_ray(window_query).collider.name, "Window glass has no collision")
	var back_query := PhysicsRayQueryParameters3D.create(Vector3(-1, 4.8, -16.72), Vector3(-1, 4.8, -17.2))
	assert("BackWall" in space.intersect_ray(back_query).collider.name, "Empty space remains behind apartment 17")
	for target in [Vector2(-1, -5.8), Vector2(-1, -10.5), Vector2(1, -10.5), Vector2(1, -5.8), Vector2(-1, -5.6), Vector2(-1, -14.2)]:
		var reached := false
		for i in range(420):
			var offset := Vector2(target.x - player.position.x, target.y - player.position.z)
			if offset.length() < 0.18:
				reached = true
				break
			var direction := offset.normalized()
			player.velocity = Vector3(direction.x * 2.5, -1 if player.is_on_floor() else player.velocity.y - 0.3, direction.y * 2.5)
			player.move_and_slide()
			await physics_frame
		assert(reached, "Entrance route blocked at " + str(player.position) + " toward " + str(target))
	assert(player.position.y > 3.6, "Upper landing not reached: " + str(player.position))
	assert(map.get_node("Apartment17").has_method("interact"))
	print("ENTRANCE CHECK PASSED: upper landing reached at ", player.position)
	quit(0)
