class_name PlayerController
extends CharacterBody3D

@export_node_path("Node3D") var camera_pivot_path: NodePath
@export_node_path("Camera3D") var camera_path: NodePath
@export_node_path("Node") var grab_system_path: NodePath
@export_range(3.0, 8.0, 0.1) var move_speed: float = 5.0
@export_range(10.0, 40.0, 0.1) var acceleration: float = 35.0
@export_range(17.5, 50.0, 0.1) var friction: float = 25.0
@export_range(3.0, 6.0, 0.1) var jump_velocity: float = 4.5
@export_range(0.0, 1.0, 0.05) var air_control: float = 0.35
@export_range(4.0, 6.0, 1.0) var coyote_frames: int = 5
@export var mouse_sensitivity: float = 0.003
@export_range(-60.0, 0.0, 1.0) var pitch_min_deg: float = -25.0
@export_range(0.0, 80.0, 1.0) var pitch_max_deg: float = 40.0

var _gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity", 9.8)
var _camera_pitch: float = -0.35
var _camera_yaw: float = 0.0
var _coyote_timer: int = 0
var _inputs_enabled: bool = true
var camera_pivot: Node3D = null
var camera: Camera3D = null
var grab_system: GrabSystem = null


func _ready() -> void:
    camera_pivot = get_node_or_null(camera_pivot_path) as Node3D
    camera = get_node_or_null(camera_path) as Camera3D
    grab_system = get_node_or_null(grab_system_path) as GrabSystem
    collision_layer = CollisionLayers.PLAYER
    collision_mask = CollisionLayers.WORLD | CollisionLayers.OBJECTS | CollisionLayers.ENEMIES
    Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
    if camera_pivot != null:
        camera_pivot.rotation.x = _camera_pitch
    if grab_system != null:
        grab_system.player_body = self
        grab_system.camera_pivot = camera_pivot


func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseMotion and _inputs_enabled:
        _camera_yaw -= event.relative.x * mouse_sensitivity
        _camera_pitch = clamp(_camera_pitch - event.relative.y * mouse_sensitivity, deg_to_rad(pitch_min_deg), deg_to_rad(pitch_max_deg))
    elif event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
        var target_mode: Input.MouseMode = Input.MOUSE_MODE_VISIBLE if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED else Input.MOUSE_MODE_CAPTURED
        Input.set_mouse_mode(target_mode)


func _physics_process(delta: float) -> void:
    _update_camera_rig()
    _update_coyote_time()
    _handle_jump()
    _apply_gravity(delta)
    _apply_movement(delta)
    move_and_slide()
    _handle_actions()


func _update_camera_rig() -> void:
    rotation.y = _camera_yaw
    if camera_pivot != null:
        camera_pivot.rotation.x = _camera_pitch


func _update_coyote_time() -> void:
    if is_on_floor():
        _coyote_timer = coyote_frames
    elif _coyote_timer > 0:
        _coyote_timer -= 1


func _handle_jump() -> void:
    var can_jump: bool = is_on_floor() or _coyote_timer > 0
    if _inputs_enabled and Input.is_action_just_pressed("jump") and can_jump:
        velocity.y = jump_velocity
        _coyote_timer = 0


func _apply_gravity(delta: float) -> void:
    if not is_on_floor():
        velocity.y -= _gravity * delta


func _apply_movement(delta: float) -> void:
    if not _inputs_enabled:
        velocity.x = 0.0
        velocity.z = 0.0
        return
    var input_vector: Vector2 = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var planar_direction: Vector3 = (global_basis * Vector3(input_vector.x, 0.0, input_vector.y)).normalized()
    var accel: float = acceleration if is_on_floor() else acceleration * air_control
    if planar_direction != Vector3.ZERO:
        velocity.x = move_toward(velocity.x, planar_direction.x * move_speed, accel * delta)
        velocity.z = move_toward(velocity.z, planar_direction.z * move_speed, accel * delta)
    else:
        velocity.x = move_toward(velocity.x, 0.0, friction * delta)
        velocity.z = move_toward(velocity.z, 0.0, friction * delta)


func _handle_actions() -> void:
    if grab_system == null or not _inputs_enabled:
        return
    if Input.is_action_just_pressed("throw"):
        grab_system.throw_object()
        return
    if Input.is_action_just_pressed("grab"):
        grab_system.try_grab()
    if Input.is_action_just_pressed("drop"):
        grab_system.drop_object()
    if Input.is_action_just_pressed("melee"):
        grab_system.melee_strike()
