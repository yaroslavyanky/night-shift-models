extends CharacterBody3D

const WALK_SPEED := 3.1
const RUN_SPEED := 5.0
const JUMP_SPEED := 5.2
const SENSITIVITY := 0.0022
@onready var head: Node3D = $Head
@onready var camera: Camera3D = $Head/Camera3D
@onready var flashlight: SpotLight3D = $Head/Camera3D/Flashlight
@onready var ray: RayCast3D = $Head/Camera3D/InteractRay
var hud: CanvasLayer
var hint: Label
var area_label: Label
var pause_panel: PanelContainer
var info_label: Label
var step_time := 0.0
var current_target: Node
var event_label: Label
var event_serial := 0
var jump_requested := false
var yard_actions: Dictionary = {}

func _ready() -> void:
	_build_hud()
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

func _build_hud() -> void:
	hud = CanvasLayer.new()
	add_child(hud)
	var root := Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud.add_child(root)
	# Subtle cheap-camera grime: edge darkening and slow monochrome grain, not a heavy horror filter.
	var film := ColorRect.new()
	film.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	film.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var shader := Shader.new()
	shader.code = "shader_type canvas_item; float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);} void fragment(){vec2 d=UV-vec2(.5); float v=smoothstep(.82,.18,length(d)*1.25); float g=(h(floor(UV*vec2(900.,540.))+TIME)-.5)*.045; COLOR=vec4(vec3(g), (1.-v)*.30);}" 
	var material := ShaderMaterial.new()
	material.shader = shader
	film.material = material
	root.add_child(film)
	area_label = Label.new()
	area_label.position = Vector2(34, 28)
	area_label.add_theme_font_size_override("font_size", 19)
	area_label.modulate = Color(0.82, 0.86, 0.78)
	root.add_child(area_label)
	var controls := Label.new()
	controls.text = "WASD  идти   ·   Shift  бежать   ·   Space  прыжок   ·   F  фонарь   ·   E  действие   ·   Esc  курсор"
	controls.add_theme_font_size_override("font_size", 15)
	controls.modulate = Color(0.69, 0.75, 0.71)
	controls.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_LEFT)
	controls.position = Vector2(34, -45)
	root.add_child(controls)
	var dot := ColorRect.new()
	dot.color = Color(0.84, 0.88, 0.77, 0.7)
	dot.mouse_filter = Control.MOUSE_FILTER_IGNORE
	dot.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	dot.position = Vector2(-2, -2)
	dot.size = Vector2(4, 4)
	root.add_child(dot)
	hint = Label.new()
	hint.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
	hint.position = Vector2(-300, -110)
	hint.size = Vector2(600, 36)
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.add_theme_font_size_override("font_size", 21)
	root.add_child(hint)
	event_label = Label.new()
	event_label.position = Vector2(34, 84)
	event_label.size = Vector2(620, 90)
	event_label.add_theme_font_size_override("font_size", 18)
	event_label.modulate = Color(0.91, 0.84, 0.62)
	event_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	root.add_child(event_label)
	pause_panel = PanelContainer.new()
	pause_panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	pause_panel.position = Vector2(-290, -135)
	pause_panel.size = Vector2(580, 270)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.04, 0.06, 0.065, 0.95)
	style.content_margin_left = 34
	style.content_margin_right = 34
	style.content_margin_top = 30
	style.content_margin_bottom = 30
	pause_panel.add_theme_stylebox_override("panel", style)
	root.add_child(pause_panel)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation", 18)
	pause_panel.add_child(column)
	var title := Label.new()
	title.text = "Тихая улица, 17"
	title.add_theme_font_size_override("font_size", 34)
	column.add_child(title)
	info_label = Label.new()
	info_label.text = "Ночной обход\n\nПоднимись к квартире 17." if get_parent().name == "EntranceLevel" else "Ночной обход\n\nОсмотри записку на столе, объявление на ларьке и щиток у гаража.\nПосле этого проверь второй подъезд."
	info_label.add_theme_font_size_override("font_size", 18)
	column.add_child(info_label)
	var start := Button.new()
	start.text = "Начать обход"
	start.custom_minimum_size.y = 44
	start.pressed.connect(_capture_mouse)
	column.add_child(start)

func _capture_mouse() -> void:
	pause_panel.hide()
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.physical_keycode:
			KEY_ESCAPE:
				Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
				pause_panel.show()
			KEY_F:
				flashlight.visible = not flashlight.visible
			KEY_E:
				if Input.mouse_mode == Input.MOUSE_MODE_CAPTURED and is_instance_valid(current_target):
					current_target.interact()
			KEY_SPACE:
				if Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
					jump_requested = true
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotate_y(-event.relative.x * SENSITIVITY)
		head.rotation.x = clampf(head.rotation.x - event.relative.y * SENSITIVITY, -1.35, 1.35)
	if event is InputEventMouseButton and event.pressed and not pause_panel.visible:
		_capture_mouse()

func _physics_process(delta: float) -> void:
	var active := Input.mouse_mode == Input.MOUSE_MODE_CAPTURED
	var move := Vector2.ZERO
	if active:
		move = Vector2(float(Input.is_physical_key_pressed(KEY_D)) - float(Input.is_physical_key_pressed(KEY_A)), float(Input.is_physical_key_pressed(KEY_S)) - float(Input.is_physical_key_pressed(KEY_W))).normalized()
	var direction := transform.basis * Vector3(move.x, 0, move.y)
	var speed := RUN_SPEED if Input.is_physical_key_pressed(KEY_SHIFT) else WALK_SPEED
	velocity.x = move_toward(velocity.x, direction.x * speed, delta * 18)
	velocity.z = move_toward(velocity.z, direction.z * speed, delta * 18)
	if not is_on_floor():
		velocity.y -= 18 * delta
	elif jump_requested:
		velocity.y = JUMP_SPEED
	else:
		velocity.y = -0.5
	jump_requested = false
	move_and_slide()
	if global_position.y < -8: global_position = Vector3(0, 1, 14)
	if move.length() > 0 and is_on_floor(): step_time += delta * speed * 2.2
	camera.position.y = lerpf(camera.position.y, sin(step_time) * 0.022 if move.length() > 0 else 0.0, delta * 10)
	current_target = null
	if ray.is_colliding():
		var target := ray.get_collider() as Node
		while target != null:
			if target.has_method("interact"):
				current_target = target
				break
			target = target.get_parent()
	hint.text = "E  ·  " + str(current_target.get("prompt")) if is_instance_valid(current_target) and active else ""
	area_label.text = "ТИХАЯ УЛИЦА, 17\n" + ("Подъезд 2 · лестничная площадка" if global_position.z < -14 else "Двор · ночной обход")
	if active and is_instance_valid(current_target):
		hint.text = current_target.interaction_prompt()
	else:
		hint.text = ""
	if global_position.z < -20:
		area_label.text = "Второй подъезд  /  лестничная площадка"
	elif global_position.z < -14.1:
		area_label.text = "Тихая улица, 17  /  второй подъезд"
	else:
		area_label.text = "Тихая улица, 17  /  двор"
	if get_parent().name == "EntranceLevel":
		area_label.text = "Подъезд 2  /  лестничная площадка" if global_position.y > 0.8 else "Подъезд 2  /  первый этаж"
	if yard_actions.size() < 3 and global_position.z > -14.1:
		area_label.text += "\nОсмотр двора: %d / 3" % yard_actions.size()

func record_yard_action(action_id: String, message: String) -> void:
	if not yard_actions.has(action_id):
		yard_actions[action_id] = true
	var suffix := "\nОсмотр двора: %d / 3" % yard_actions.size()
	if yard_actions.size() >= 3:
		suffix = "\nДвор осмотрен. Теперь проверь второй подъезд."
	show_event_message(message + suffix)

func show_event_message(message: String) -> void:
	event_serial += 1
	var serial := event_serial
	event_label.text = message
	await get_tree().create_timer(4.5).timeout
	if serial == event_serial:
		event_label.text = ""
