extends SceneTree

func _initialize() -> void:
	call_deferred("check_map")

func check_map() -> void:
	var scene: PackedScene = load("res://scenes/courtyard.tscn")
	assert(scene != null)
	var map := scene.instantiate()
	root.add_child(map)
	var player: CharacterBody3D = map.get_node("Player")
	player.set_physics_process(false)
	for i in range(3): await physics_frame
	var space := player.get_world_3d().direct_space_state
	for point in [Vector3(0,3,14), Vector3(0,3,-10), Vector3(0,3,-17)]:
		var query := PhysicsRayQueryParameters3D.create(point, point - Vector3(0,6,0))
		query.exclude = [player.get_rid()]
		assert(not space.intersect_ray(query).is_empty(), "Missing floor at " + str(point))
	# Grass beds are visual-only; the shared courtyard ground must remain the walkable surface.
	for point in [Vector3(-4, 3, -5), Vector3(4, 3, -5)]:
		var grass_query := PhysicsRayQueryParameters3D.create(point, point - Vector3(0, 6, 0))
		grass_query.exclude = [player.get_rid()]
		var grass_hit := space.intersect_ray(grass_query)
		assert(not grass_hit.is_empty(), "Missing walkable floor under grass at " + str(point))
		assert("CourtyardGround" in grass_hit.collider.name, "Unexpected grass collision: " + grass_hit.collider.name)
	# The first location exposes three usable yard actions.
	for action_path in ["Props/TableNote", "Props/GaragePoster", "Props/YardLightSwitch"]:
		var action := map.get_node(action_path)
		assert(action.has_method("interact"), "Missing interaction at " + action_path)
		action.interact()
	assert(player.yard_actions.size() == 3, "Yard actions did not update the objective")
	assert(map.get_node("Lighting/YardFloodlight").visible, "Yard light switch did not activate the floodlight")
	var garage := map.get_node("Props/GarageDoorLeft")
	garage.interact()
	await create_timer(0.8).timeout
	assert(garage.open and absf(garage.left_door.rotation.y) > 1.0, "Garage doors did not swing open")
	# Exercise the real player jump once after settling on the spawn floor.
	player.global_position = Vector3(0, 0.12, 14)
	player.velocity = Vector3.ZERO
	player.set_physics_process(true)
	for i in range(10): await physics_frame
	var settled_y := player.global_position.y
	player.jump_requested = true
	for i in range(8): await physics_frame
	assert(player.global_position.y > settled_y + 0.2, "Player jump did not leave the ground")
	player.set_physics_process(false)
	player.global_position = Vector3(0, 0.12, 14)
	player.velocity = Vector3.ZERO
	var door := map.get_node("Entrance/EntryDoor")
	assert(door.has_method("interact"))
	# Move using actual CharacterBody collisions, from spawn all the way up the stair.
	door.rotation.y = deg_to_rad(-105.0)
	for frame in range(850):
		await physics_frame
		player.velocity = Vector3(0, -1 if player.is_on_floor() else player.velocity.y - 0.3, -3.1)
		player.move_and_slide()
		if player.position.z < -22.1: break
	assert(player.position.z < -22.1, "Route blocked at " + str(player.position))
	assert(player.position.y > 1.1, "Stairs did not raise the player: " + str(player.position))
	door.interact()
	await create_timer(0.75).timeout
	assert(absf(door.rotation.y - deg_to_rad(-105.0)) < .01)
	door.interact()
	await create_timer(0.75).timeout
	assert(absf(door.rotation.y) < .01)
	print("MAP CHECK PASSED: scene, spawn floors, doorway route, stair climb, door toggle. Final player position: ", player.position)
	quit(0)
