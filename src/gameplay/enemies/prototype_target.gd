class_name PrototypeTarget
extends CharacterBody3D

@export var max_hp: int = 20
@export var knockback_decay: float = 14.0

var current_hp: int = 20
var _flash_timer: float = 0.0
var _base_material: Material = null
var _knockback_velocity: Vector3 = Vector3.ZERO

@onready var _mesh: MeshInstance3D = $MeshInstance3D
@onready var _label: Label3D = $Label3D


func _ready() -> void:
    collision_layer = CollisionLayers.ENEMIES
    collision_mask = CollisionLayers.WORLD | CollisionLayers.OBJECTS | CollisionLayers.PLAYER | CollisionLayers.ENEMIES
    current_hp = max_hp
    _base_material = _mesh.material_override
    _refresh_label()


func _physics_process(delta: float) -> void:
    if _knockback_velocity.length() > 0.01:
        velocity.x = _knockback_velocity.x
        velocity.z = _knockback_velocity.z
        move_and_slide()
        _knockback_velocity = _knockback_velocity.lerp(Vector3.ZERO, min(1.0, knockback_decay * delta))
    else:
        velocity.x = 0.0
        velocity.z = 0.0
    if _flash_timer > 0.0:
        _flash_timer = max(0.0, _flash_timer - delta)
        if _flash_timer == 0.0:
            _mesh.material_override = _base_material

    if Input.is_action_just_pressed("reset_dummy"):
        reset_dummy()


func receive_damage(amount: int, _damage_type: DamageCalculator.DamageType) -> void:
    current_hp = max(0, current_hp - amount)
    _flash_timer = 0.12
    var material := StandardMaterial3D.new()
    material.albedo_color = Color(1.0, 0.25, 0.25, 1.0)
    _mesh.material_override = material
    _knockback_velocity = Vector3(0.0, 0.0, 2.2 + float(amount) * 0.12)
    _refresh_label()


func _refresh_label() -> void:
    if current_hp <= 0:
        _label.text = "Dummy KO - T pour reset"
    else:
        _label.text = "Dummy HP: %d/%d" % [current_hp, max_hp]


func reset_dummy() -> void:
    current_hp = max_hp
    _flash_timer = 0.0
    _knockback_velocity = Vector3.ZERO
    _mesh.material_override = _base_material
    _refresh_label()
