# ADR-0012 : S12 Retry (SceneTree.reload_current_scene)

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Godot 4.6.2 |
| **Domain** | Core / Lifecycle |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `design/gdd/retry-reinitialisation.md` |
| **Post-Cutoff APIs Used** | `SceneTree.reload_current_scene()` (stable) |
| **Verification Required** | Mesurer `scene_reload_time` et tenir le budget total <= 3s |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0011 (S11 orchestration) |
| **Enables** | MVP retry rapide |
| **Blocks** | Epic S12 — Retry / réinitialisation |
| **Ordering Note** | À accepter avant les stories S12 |

## Context

Le retry est un pilier de flow : après un game over, on doit revenir en jeu vite, sans écrans et sans state persistant implicite. Le risque principal est de créer un retry partiel (des nodes survivent, des timers restent actifs).

## Decision

1. S12 expose une seule méthode publique : `retry()`.
2. `retry()` appelle `get_tree().reload_current_scene()` (pas de reset manuel par système en MVP).
3. S12 ne s'auto-déclenche jamais : il est déclenché exclusivement par S11 après `RETRY_DELAY`.
4. Budget : `RETRY_DELAY + scene_reload_time <= 3.0 s` (MVP).

## Alternatives Considered

### Alternative A : Reset manuel par système
- **Pros** : plus fin
- **Cons** : fragile, oublis, “zombies” de timers/signaux
- **Raison du rejet** : MVP vise la robustesse via reload de scène

## Validation Criteria

- [ ] `retry()` recharge la scène courante sans crash
- [ ] Aucun état runtime (vagues, HP, objets cassés) ne persiste après retry
- [ ] Le budget total <= 3.0 s est respecté sur machine cible prototype

## GDD Requirements Addressed

| TR-ID | Requirement | ADR |
|---|---|---|
| TR-retry-reinitialisation-001..003 | API retry + déclenchement exclusif + budget | Décisions 1–4 |

## Related Decisions

- ADR-0011 : GameState FSM (déclencheur unique)
- `design/gdd/retry-reinitialisation.md`

