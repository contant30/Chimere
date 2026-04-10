# ADR-0011 : S11 GameState FSM (autorité + orchestration freeze/retry)

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Godot 4.6.2 |
| **Domain** | Core / Orchestration |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `design/gdd/gestionnaire-etat.md`, `design/gdd/sante-joueur.md`, `design/gdd/vagues-ennemis.md`, `design/gdd/retry-reinitialisation.md` |
| **Post-Cutoff APIs Used** | None |
| **Verification Required** | Valider que le sequencing freeze→retry tient en <3s au prototype |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0007 (Camera freeze), ADR-0010 (Wave contracts), ADR-0008 (player_died) |
| **Enables** | S12 (Retry wiring), S13 (HUD retry) |
| **Blocks** | Epic S11 — Gestionnaire d'état |
| **Ordering Note** | À accepter avant S12/S13 (wiring retry) |

## Context

S11 doit :
- être l'unique autorité de `current_state`,
- synchroniser les transitions déclenchées par S07 (mort) et S03 (vagues),
- geler les contrôles/caméra au game over,
- déclencher un retry rapide via S12.

Sans ADR, les responsabilités peuvent dériver (S03 tente de gérer le game over, ou S12 s'auto-déclenche).

## Decision

### 1) Autorité d'état

S11 est l'unique propriétaire de `current_state: GameState`.

Il publie :

```gdscript
signal game_state_changed(new_state: GameState)
```

### 2) Transitions (contrat MVP)

S11 écoute :
- `player_died()` (S07)
- `wave_started/wave_cleared/all_waves_complete` (S03)
- `retry_requested()` (S13)

S11 orchestre :
- `S10.freeze()` sur `GAME_OVER` (même frame que `player_died`)
- `S12.retry()` après `RETRY_DELAY` (<= 3s total budget, voir S12)

### 3) Pas de logique gameplay

S11 ne contient pas :
- de spawn (S03),
- de dégâts (S06),
- de health (S07/S08).

Il ne fait que router des événements et appeler les APIs d'orchestration (freeze/retry).

## Alternatives Considered

### Alternative A : WaveManager contrôle tout (y compris game over)
- **Pros** : moins de systèmes
- **Cons** : mélange d'autorité, circularité accrue, difficile à étendre
- **Raison du rejet** : séparation nette (S03 spawn, S11 orchestration)

## Validation Criteria

- [ ] `player_died` entraîne `game_state_changed(GAME_OVER)` et `freeze()` dans la même frame
- [ ] `retry_requested` ne fonctionne qu'en GAME_OVER
- [ ] Aucun système autre que S11 n'écrit `current_state`

## GDD Requirements Addressed

| TR-ID | Requirement | ADR |
|---|---|---|
| TR-gestionnaire-etat-001..004 | Autorité + transitions + pas de gameplay | Décisions 1–3 |

## Related Decisions

- ADR-0007 : Camera TPS (freeze/unfreeze)
- ADR-0012 : Retry wiring
- `design/gdd/gestionnaire-etat.md`

