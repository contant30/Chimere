class_name GrabSystem
extends Node

enum GrabState {
	EMPTY_HANDS,
	CARRYING,
}

signal grab_performed(object: RigidBody3D)
signal throw_performed(object: RigidBody3D, impulse: Vector3)
signal melee_performed(object: RigidBody3D)
signal object_dropped(object: RigidBody3D)
signal carry_interrupted(object: RigidBody3D)
signal action_debug(message: String)

@export_node_path("Node3D") var camera_pivot_path: NodePath
@export_node_path("Node3D") var carry_anchor_path: NodePath
@export_node_path("CharacterBody3D") var player_body_path: NodePath
@export var carry_offset: Vector3 = Vector3(0.0, 0.8, -1.2)
@export_range(5.0, 30.0, 0.5) var max_grab_mass_kg: float = 15.0
@export_range(30.0, 180.0, 1.0) var grab_cone_deg: float = 120.0
@export_range(4.0, 25.0, 0.1) var throw_impulse_base_n_s: float = 16.0
@export_range(-20.0, -5.0, 1.0) var throw_pitch_deg: float = -10.0
@export_range(0.08, 0.35, 0.01) var melee_arc_duration_s: float = 0.22
@export_range(15.0, 80.0, 1.0) var melee_arc_angle_deg: float = 55.0
@export_range(0.3, 1.2, 0.05) var melee_hitbox_radius_m: float = 0.8
@export_range(0.0, 0.3, 0.01) var grab_cooldown_s: float = 0.1

var state: GrabState = GrabState.EMPTY_HANDS
var held_object: GrabbableObject = null

var camera_pivot: Node3D = null
var carry_anchor: Node3D = null
var player_body: CharacterBody3D = null
var _current_target: GrabbableObject = null
var _last_grab_time_s: float = -1.0
var _melee_timer_s: float = 0.0
var _melee_origin_rotation: Basis
var _melee_origin_position: Vector3
var _melee_hit_targets: Array[Node3D] = []


func _ready() -> void:
	camera_pivot = get_node_or_null(camera_pivot_path) as Node3D
	carry_anchor = get_node_or_null(carry_anchor_path) as Node3D
	player_body = get_node_or_null(player_body_path) as CharacterBody3D


func _physics_process(delta: float) -> void:
	_update_candidate_target()
	_update_held_object_transform(delta)
	_update_melee_arc(delta)
	_flush_interrupted_hold()


func try_grab() -> void:
	if state != GrabState.EMPTY_HANDS:
		return
	if Time.get_ticks_msec() / 1000.0 - _last_grab_time_s < grab_cooldown_s:
		return
	var target: GrabbableObject = _find_best_candidate()
	if target == null:
		return
	if target.mass_kg > max_grab_mass_kg:
		return
	held_object = target
	held_object.begin_carry()
	held_object.global_transform = carry_anchor.global_transform.translated_local(carry_offset)
	state = GrabState.CARRYING
	_last_grab_time_s = Time.get_ticks_msec() / 1000.0
	emit_signal("grab_performed", held_object)
	emit_signal("action_debug", "Saisie: %s" % held_object.object_label)


func melee_strike() -> void:
	if held_object == null:
		emit_signal("action_debug", "Melee ignoree: aucun objet")
		return
	_melee_timer_s = melee_arc_duration_s
	_melee_origin_rotation = held_object.global_transform.basis
	_melee_origin_position = held_object.global_position
	_melee_hit_targets.clear()
	held_object.register_use(GrabbableObject.UseKind.MELEE)
	_apply_melee_damage()
	emit_signal("melee_performed", held_object)
	emit_signal("action_debug", "Melee: %s" % held_object.object_label)


func throw_object() -> void:
	if held_object == null:
		emit_signal("action_debug", "Lancer ignore: aucun objet")
		return
	var object: GrabbableObject = held_object
	var damage: int = object.get_throw_damage()
	var direction: Vector3 = _get_throw_direction()
	var impulse: Vector3 = direction * throw_impulse_base_n_s * object.throw_impulse_scale
	_release_held_object()
	object.arm_throw(player_body, damage)
	object.sleeping = false
	object.linear_velocity = direction * (throw_impulse_base_n_s * object.throw_impulse_scale / max(object.mass, 0.1))
	object.apply_central_impulse(impulse)
	object.register_use(GrabbableObject.UseKind.THROW)
	emit_signal("throw_performed", object, impulse)
	emit_signal("action_debug", "Lancer: %s" % object.object_label)


func drop_object() -> void:
	if held_object == null:
		emit_signal("action_debug", "Depot ignore: aucun objet")
		return
	var object: GrabbableObject = held_object
	_release_held_object()
	object.linear_velocity = Vector3.ZERO
	object.angular_velocity = Vector3.ZERO
	emit_signal("object_dropped", object)
	emit_signal("action_debug", "Depot: %s" % object.object_label)


func is_carrying() -> bool:
	return held_object != null


func _update_candidate_target() -> void:
	var next_target: GrabbableObject = _find_best_candidate()
	if next_target == _current_target:
		return
	if _current_target != null and _current_target != held_object:
		_current_target.set_highlight_state(GrabbableObject.HighlightState.NONE)
	_current_target = next_target
	if _current_target == null or _current_target == held_object:
		return
	var highlight_state: GrabbableObject.HighlightState = GrabbableObject.HighlightState.VALID
	if _current_target.mass_kg > max_grab_mass_kg:
		highlight_state = GrabbableObject.HighlightState.TOO_HEAVY
	_current_target.set_highlight_state(highlight_state)


func _find_best_candidate() -> GrabbableObject:
	if player_body == null or camera_pivot == null:
		return null
	var best_candidate: GrabbableObject = null
	var best_distance: float = INF
	var forward: Vector3 = -camera_pivot.global_basis.z
	forward.y = 0.0
	forward = forward.normalized()
	for node in get_tree().get_nodes_in_group("grabbable"):
		if not (node is GrabbableObject):
			continue
		var candidate: GrabbableObject = node
		if candidate == held_object:
			continue
		var to_object: Vector3 = candidate.global_position - player_body.global_position
		var horizontal_to_object: Vector3 = Vector3(to_object.x, 0.0, to_object.z)
		var distance: float = horizontal_to_object.length()
		if distance > candidate.grab_range_m:
			continue
		var direction: Vector3 = horizontal_to_object.normalized()
		if direction == Vector3.ZERO:
			continue
		var angle_deg: float = rad_to_deg(acos(clamp(forward.dot(direction), -1.0, 1.0)))
		if angle_deg > grab_cone_deg * 0.5:
			continue
		if distance < best_distance:
			best_distance = distance
			best_candidate = candidate
	return best_candidate


func _update_held_object_transform(delta: float) -> void:
	if held_object == null or carry_anchor == null:
		return
	var target_transform: Transform3D = carry_anchor.global_transform.translated_local(carry_offset)
	held_object.global_position = held_object.global_position.lerp(target_transform.origin, min(1.0, delta * 20.0))
	held_object.global_basis = target_transform.basis
	held_object.linear_velocity = Vector3.ZERO
	held_object.angular_velocity = Vector3.ZERO


func _update_melee_arc(delta: float) -> void:
	if held_object == null:
		return
	if _melee_timer_s <= 0.0:
		return
	_melee_timer_s = max(0.0, _melee_timer_s - delta)
	var progress: float = 1.0 - (_melee_timer_s / melee_arc_duration_s)
	var swing_curve: float = sin(progress * PI)
	var swing_angle: float = swing_curve * deg_to_rad(melee_arc_angle_deg)
	var forward_offset: Vector3 = -camera_pivot.global_basis.z * swing_curve * 0.95
	var upward_offset: Vector3 = Vector3.UP * swing_curve * 0.18
	held_object.global_basis = _melee_origin_rotation * Basis(Vector3.UP, swing_angle) * Basis(Vector3.RIGHT, -swing_angle * 0.35)
	held_object.global_position = _melee_origin_position + forward_offset + upward_offset


func _apply_melee_damage() -> void:
	if held_object == null:
		return
	var space_state: PhysicsDirectSpaceState3D = get_viewport().world_3d.direct_space_state
	var sphere: SphereShape3D = SphereShape3D.new()
	sphere.radius = melee_hitbox_radius_m
	var query: PhysicsShapeQueryParameters3D = PhysicsShapeQueryParameters3D.new()
	query.shape = sphere
	var center: Vector3 = carry_anchor.global_position + (-camera_pivot.global_basis.z * 1.2)
	query.transform = Transform3D(Basis.IDENTITY, center)
	query.collision_mask = CollisionLayers.ENEMIES
	query.exclude = [player_body.get_rid(), held_object.get_rid()]
	var results: Array[Dictionary] = space_state.intersect_shape(query)
	for result in results:
		var collider: Node3D = result.get("collider") as Node3D
		if collider == null:
			continue
		if _melee_hit_targets.has(collider):
			continue
		if collider.has_method("receive_damage"):
			collider.receive_damage(held_object.get_melee_damage(), DamageCalculator.DamageType.MELEE)
			_melee_hit_targets.append(collider)


func _flush_interrupted_hold() -> void:
	if held_object != null and not is_instance_valid(held_object):
		var interrupted: GrabbableObject = held_object
		held_object = null
		state = GrabState.EMPTY_HANDS
		emit_signal("carry_interrupted", interrupted)


func _release_held_object() -> void:
	if held_object == null:
		return
	held_object.end_carry()
	held_object.global_position = carry_anchor.global_position + (-camera_pivot.global_basis.z * 1.1)
	held_object = null
	state = GrabState.EMPTY_HANDS


func _get_throw_direction() -> Vector3:
	var direction: Vector3 = -camera_pivot.global_basis.z
	direction = direction.rotated(camera_pivot.global_basis.x.normalized(), deg_to_rad(throw_pitch_deg))
	return direction.normalized()
