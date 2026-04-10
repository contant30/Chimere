# ADR-0013 : S13 HUD (CanvasLayer read-only + retry_requested)

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Godot 4.6.2 |
| **Domain** | Presentation / UI |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `design/gdd/hud.md` |
| **Post-Cutoff APIs Used** | `CanvasLayer` (stable) |
| **Verification Required** | Valider que l'UI reste indépendante de la caméra 3D (pas de coupling de nodes) |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0005 (signaux), ADR-0008 (player_hp_changed/player_hit), ADR-0010 (wave_started), ADR-0001 (GrabSystem signals) |
| **Enables** | S11 retry via UI |
| **Blocks** | Epic S13 — HUD |
| **Ordering Note** | À accepter avant les stories HUD (TR-hud-001..004) |

## Context

Le HUD doit être :
- lisible et stable (CanvasLayer),
- strictement read-only sur les systèmes gameplay,
- capable de déclencher un retry via S11 (seule sortie).

## Decision

1. **HUD = CanvasLayer**  
   Le HUD vit dans un `CanvasLayer` (pas parenté à la caméra 3D).

2. **Entrées via signaux**  
   Le HUD s'abonne à :
   - `player_hp_changed(current_hp, max_hp)` (S07)
   - `player_hit(damage, damage_type, current_hp)` (S07)
   - `wave_started(wave_number)` (S03)
   - signaux GrabSystem `grab_performed/throw_performed/melee_performed` (S02) pour la silhouette/état objet tenu

3. **Sortie unique**  
   Le HUD émet :

```gdscript
signal retry_requested()
```

Uniquement en GAME_OVER (S11 est responsable de filtrer/ignorer le reste).

## Alternatives Considered

### Alternative A : HUD “pull” (polling) de l'état
- **Pros** : simple
- **Cons** : couplage, état global implicite, latence
- **Raison du rejet** : event-driven (ADR-0005)

## Validation Criteria

- [ ] Le HUD se met à jour sans lire directement des singletons/nodes globaux
- [ ] `retry_requested()` est émis uniquement sur input retry en GAME_OVER
- [ ] Le HUD ne modifie aucune donnée gameplay (read-only)

## GDD Requirements Addressed

| TR-ID | Requirement | ADR |
|---|---|---|
| TR-hud-001..004 | CanvasLayer + signaux consommés + retry_requested | Décisions 1–3 |

## Related Decisions

- ADR-0011 : GameState FSM (consomme retry_requested)
- `design/gdd/hud.md`

