class_name GrabbableObject
extends RigidBody3D

enum HighlightState {
	NONE,
	VALID,
	TOO_HEAVY,
}

enum UseKind {
	MELEE,
	THROW,
}

@export var catalog_entry: Resource
@export var object_label: String = "objet"
@export var mass_kg: float = 1.0
@export var grab_range_m: float = 2.2
@export var melee_damage_base: int = 4
@export var throw_damage_base: int = 6
@export var throw_impulse_scale: float = 1.0
@export var melee_dmg_mult: float = 1.0
@export var throw_dmg_mult: float = 1.0

var current_stage: int = 0
var uses_count: int = 0
var _armed_throw_damage: int = 0
var _throw_owner: Node3D = null
var _default_collision_mask: int = 0
var _default_collision_layer: int = 0
var _base_color: Color = Color(0.75, 0.75, 0.75, 1.0)

@onready var _impact_area: Area3D = $ImpactArea
@onready var _label: Label3D = get_node_or_null("Label3D") as Label3D
@onready var _mesh_instances: Array[MeshInstance3D] = _find_mesh_instances()


func _ready() -> void:
	add_to_group("grabbable")
	_apply_catalog_entry()
	_default_collision_layer = collision_layer
	_default_collision_mask = collision_mask
	if not _impact_area.body_entered.is_connected(_on_impact_area_body_entered):
		_impact_area.body_entered.connect(_on_impact_area_body_entered)
	_apply_highlight(HighlightState.NONE)


func get_melee_damage() -> int:
	return DamageCalculator.calculate(melee_damage_base, melee_dmg_mult, DamageCalculator.DamageType.MELEE)


func get_throw_damage() -> int:
	return DamageCalculator.calculate(throw_damage_base, throw_dmg_mult, DamageCalculator.DamageType.THROW)


func register_use(_use_kind: UseKind) -> void:
	uses_count += 1


func begin_carry() -> void:
	sleeping = false
	freeze = true
	freeze_mode = RigidBody3D.FREEZE_MODE_KINEMATIC
	linear_velocity = Vector3.ZERO
	angular_velocity = Vector3.ZERO
	collision_layer = CollisionLayers.OBJECTS
	collision_mask = CollisionLayers.ENEMIES
	_armed_throw_damage = 0
	_throw_owner = null
	_apply_highlight(HighlightState.NONE)


func end_carry() -> void:
	freeze = false
	sleeping = false
	collision_layer = _default_collision_layer
	collision_mask = _default_collision_mask


func arm_throw(throw_owner: Node3D, damage: int) -> void:
	_throw_owner = throw_owner
	_armed_throw_damage = damage


func set_highlight_state(state: HighlightState) -> void:
	_apply_highlight(state)


func _on_impact_area_body_entered(body: Node3D) -> void:
	if _armed_throw_damage <= 0:
		return
	if body == _throw_owner:
		return
	if body.has_method("receive_damage"):
		body.receive_damage(_armed_throw_damage, DamageCalculator.DamageType.THROW)
		_armed_throw_damage = 0


func _apply_highlight(state: HighlightState) -> void:
	var target_color := _base_color
	match state:
		HighlightState.VALID:
			target_color = Color(0.95, 0.95, 0.95, 1.0)
		HighlightState.TOO_HEAVY:
			target_color = Color(0.95, 0.3, 0.3, 1.0)
	for mesh_instance in _mesh_instances:
		var material := StandardMaterial3D.new()
		material.albedo_color = target_color
		material.roughness = 0.65
		mesh_instance.material_override = material


func _find_mesh_instances() -> Array[MeshInstance3D]:
	var result: Array[MeshInstance3D] = []
	for child in get_children():
		if child is MeshInstance3D:
			result.append(child)
	return result


func _apply_catalog_entry() -> void:
	var entry := catalog_entry as ObjectCatalogEntry
	if entry == null:
		return
	object_label = entry.display_name
	mass_kg = entry.mass_kg
	grab_range_m = entry.grab_range_m
	melee_damage_base = entry.melee_damage_base
	throw_damage_base = entry.throw_damage_base
	throw_impulse_scale = entry.throw_impulse_scale
	melee_dmg_mult = entry.melee_dmg_mult
	throw_dmg_mult = entry.throw_dmg_mult
	mass = mass_kg
	if _label != null:
		_label.text = object_label.capitalize()
