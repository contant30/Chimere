# ADR-0006 : S01 Jump + Gravity (coyote time, ordre d'application)

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Godot 4.6.2 |
| **Domain** | Core / Movement |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `design/gdd/deplacement-joueur.md` |
| **Post-Cutoff APIs Used** | `CharacterBody3D.move_and_slide()` (API stable) |
| **Verification Required** | Valider au prototype que l'ordre saut→gravité n'introduit pas d'artefact Jolt sur 1 frame |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0002 (Player Body Type) |
| **Enables** | Aucun |
| **Blocks** | Epic S01 — Déplacement joueur |
| **Ordering Note** | À accepter avant les stories S01 (TR-deplacement-joueur-003/004) |

## Context

Le GDD S01 exige deux comportements qui doivent être fixés comme décisions d'implémentation :
- **Coyote time** en frames (4–6 frames @ 60 FPS) et consommation immédiate au saut.
- **Gravité** appliquée manuellement (`velocity.y -= GRAVITY * delta`), en lisant la valeur depuis `ProjectSettings`.

Sans cadrage, deux implémentations “raisonnables” peuvent diverger (timer en secondes vs frames, gravité avant le saut vs après), ce qui casse les tests et la sensation.

## Decision

1. **Coyote time en frames**  
   - On maintient `coyote_timer_frames: int`.
   - Au sol : `coyote_timer_frames = COYOTE_FRAMES` à chaque frame où `is_on_floor() == true`.
   - En l'air : `coyote_timer_frames = max(0, coyote_timer_frames - 1)` à chaque `_physics_process`.
   - Le saut est autorisé si `is_on_floor()` **ou** `coyote_timer_frames > 0`.
   - Lors d'un saut validé : `coyote_timer_frames = 0` (consommation immédiate).

2. **Ordre d'application saut → gravité**  
   Dans `_physics_process(delta)` :
   - Traiter l'input de saut **avant** d'appliquer la gravité.
   - Puis appliquer la gravité uniquement si `!is_on_floor()`.

3. **Source et application de la gravité**  
   - `GRAVITY` provient de `ProjectSettings.get("physics/3d/default_gravity")` (S01 ne hard-code pas 9.8).
   - Gravité appliquée manuellement : `velocity.y -= GRAVITY * delta`.
   - Si `is_on_floor()` et `velocity.y < 0`, on clamp à `0` (évite l'accumulation).

### Key Interface (pseudocode)

```gdscript
var coyote_timer_frames: int = 0
var GRAVITY: float = ProjectSettings.get("physics/3d/default_gravity")

func _physics_process(delta: float) -> void:
    if is_on_floor():
        coyote_timer_frames = COYOTE_FRAMES
    elif coyote_timer_frames > 0:
        coyote_timer_frames -= 1

    var can_jump := is_on_floor() or coyote_timer_frames > 0
    if Input.is_action_just_pressed("jump") and can_jump:
        velocity.y = JUMP_VELOCITY
        coyote_timer_frames = 0

    if not is_on_floor():
        velocity.y -= GRAVITY * delta
    elif velocity.y < 0:
        velocity.y = 0

    move_and_slide()
```

## Alternatives Considered

### Alternative A : Coyote time en secondes
- **Pros** : indépendant du framerate
- **Cons** : diverge du GDD (frames), rend les tests et le tuning moins directs
- **Raison du rejet** : la spec MVP est explicitement en frames, et `_physics_process` est stable à 60 FPS dans la cible prototype

### Alternative B : Gravité avant le saut
- **Pros** : simple à écrire
- **Cons** : peut “manger” une partie de l'impulsion de saut sur la première frame (artefact perceptible)
- **Raison du rejet** : S01 documente explicitement “Saut (avant gravité)”

## Consequences

### Positive
- S01 est déterministe et conforme aux formules/tests du GDD
- Le tuning (COYOTE_FRAMES) est directement interprétable

### Negative
- Le coyote time dépend implicitement de la cadence de `_physics_process` (assumée 60 FPS)

## Validation Criteria

- [ ] Un saut peut être déclenché dans les 4–6 frames après avoir quitté un rebord
- [ ] Un second saut en AIRBORNE après consommation est refusé
- [ ] Après 0.5 s en AIRBORNE, `velocity.y < 0` (gravité appliquée)

## GDD Requirements Addressed

| TR-ID | Requirement | ADR |
|---|---|---|
| TR-deplacement-joueur-003 | Saut unique + coyote time (frames) | Décision 1 |
| TR-deplacement-joueur-004 | Gravité manuelle depuis ProjectSettings | Décision 3 |

## Related Decisions

- ADR-0002 : Player Body Type and Collision Layers
- `design/gdd/deplacement-joueur.md`

