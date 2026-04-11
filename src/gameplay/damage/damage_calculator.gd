class_name DamageCalculator
extends RefCounted

enum DamageType {
    MELEE,
    THROW,
    ENEMY_MELEE,
}

static func calculate(damage_base: int, stage_mult: float, _damage_type: DamageType) -> int:
    return max(1, floori(damage_base * stage_mult))
