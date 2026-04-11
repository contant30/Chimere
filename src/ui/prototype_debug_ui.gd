class_name PrototypeDebugUi
extends CanvasLayer

@export_node_path("CharacterBody3D") var player_path: NodePath
@export_node_path("Node") var grab_system_path: NodePath

var player: PlayerController = null
var grab_system: GrabSystem = null
var _last_action_message: String = "-"
var _last_action_time_msec: int = 0

@onready var _status_label: Label = $StatusLabel
@onready var _reticle: Label = $Reticle
@onready var _hint_label: Label = $HintLabel


func _ready() -> void:
    player = get_node_or_null(player_path) as PlayerController
    grab_system = get_node_or_null(grab_system_path) as GrabSystem
    if grab_system != null and not grab_system.action_debug.is_connected(_on_action_debug):
        grab_system.action_debug.connect(_on_action_debug)


func _process(_delta: float) -> void:
    if player == null or grab_system == null:
        _status_label.text = "Sandbox indisponible"
        return
    var target_name: String = "aucune"
    if grab_system.get("held_object") != null:
        target_name = grab_system.held_object.object_label
    elif grab_system.get("_current_target") != null:
        target_name = grab_system.get("_current_target").object_label
    var action_text: String = _last_action_message
    if Time.get_ticks_msec() - _last_action_time_msec > 1800:
        action_text = "-"
    _status_label.text = "Cible: %s  |  En main: %s  |  %s" % [target_name, "oui" if grab_system.is_carrying() else "non", action_text]
    _reticle.text = "[x]" if grab_system.is_carrying() else "+"
    _hint_label.visible = not grab_system.is_carrying()


func _on_action_debug(message: String) -> void:
    _last_action_message = message
    _last_action_time_msec = Time.get_ticks_msec()
