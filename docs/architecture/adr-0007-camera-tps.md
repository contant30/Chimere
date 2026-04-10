# ADR-0007 : S10 Camera TPS (pivot + SpringArm + yaw signal + freeze)

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Godot 4.6.2 |
| **Domain** | Core / Camera |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `design/gdd/camera-tps.md` |
| **Post-Cutoff APIs Used** | `SpringArm3D` (stable), signaux Callable-based |
| **Verification Required** | Vérifier au prototype que le SpringArm évite le clipping sur une salle ~10×10 m |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0005 (DI + signaux Callable) |
| **Enables** | S01 (déplacement orienté caméra), S02 (direction de lancer) |
| **Blocks** | Epic S10 — Caméra TPS |
| **Ordering Note** | À accepter avant les stories S10, et avant l'implémentation S01/S02 qui consomment le yaw |

## Context

Plusieurs systèmes dépendent d'un “yaw caméra” stable et disponible très tôt :
- S01 oriente le déplacement relatif à la caméra.
- S02 aligne les lancers sur la direction caméra.
- S11 doit pouvoir geler/dégeler la caméra au game over / retry.

Sans contrat unique, on risque des intégrations cassantes (S01 lit un node path différent de S02, ou le yaw n'est pas émis au `_ready()`).

## Decision

1. **Architecture de scène**

```
Player (CharacterBody3D)
  └─ CameraPivot (Node3D)           # yaw + pitch
      └─ SpringArm3D               # anti-clipping murs
          └─ Camera3D
```

2. **Signal yaw chaque frame**
S10 émet :

```gdscript
signal camera_yaw_changed(yaw_radians: float)
```

- Émis à chaque `_process()` en état ACTIVE, même si la valeur ne change pas.
- Première émission à `_ready()` (valeur initiale `0.0`).

3. **Freeze / unfreeze**
S10 expose une API minimale :

```gdscript
func freeze() -> void
func unfreeze() -> void
```

- En `FROZEN` : aucun input, aucun update, aucun `camera_yaw_changed`.
- S10 écoute `player_died()` (S07) pour freezer immédiatement.
- S11 appelle `unfreeze()` au retry (S12).

4. **Accès par injection (pas de NodePath)**
S02 lit la direction via le node `camera_pivot` injecté :

```gdscript
@export var camera_pivot: Node3D
# usage: camera_pivot.global_rotation.y
```

## Alternatives Considered

### Alternative A : “Pull” du yaw par variable globale
- **Pros** : simple
- **Cons** : dépendance globale implicite, casse la testabilité
- **Raison du rejet** : contraire à ADR-0005

### Alternative B : RayCast/Camera comme source de direction pour tout
- **Pros** : unifie la logique
- **Cons** : couplage fort, difficile à tester
- **Raison du rejet** : S01/S02 consomment un simple yaw, pas une caméra complète

## Validation Criteria

- [ ] `camera_yaw_changed` est émis à `_ready()` puis à chaque frame en ACTIVE
- [ ] `freeze()` arrête immédiatement les updates + signaux
- [ ] `unfreeze()` réactive les updates + signaux sans reset du yaw

## GDD Requirements Addressed

| TR-ID | Requirement | ADR |
|---|---|---|
| TR-camera-tps-003 | `camera_yaw_changed` émis chaque frame + au `_ready()` | Décision 2 |
| TR-camera-tps-004 | API `freeze()/unfreeze()` + freeze sur `player_died` | Décision 3 |

## Related Decisions

- ADR-0005 : Conventions DI + signaux
- `design/gdd/camera-tps.md`

