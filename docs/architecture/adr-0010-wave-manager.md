# ADR-0010 : S03 WaveManager (spawn + contracts enemy_died + signaux S11)

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Godot 4.6.2 |
| **Domain** | Core / Waves |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `design/gdd/vagues-ennemis.md`, `docs/architecture/adr-0009-enemy-scene-contract.md` |
| **Post-Cutoff APIs Used** | None |
| **Verification Required** | Valider que l'instanciation + injection avant `add_child()` est respectée partout |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0005 (DI + signaux), ADR-0009 (Enemy contract) |
| **Enables** | ADR-0011 (FSM S11) |
| **Blocks** | Epic S03 — Vagues d'ennemis |
| **Ordering Note** | À accepter avant S11 (contrat S03↔S11) |

## Context

S03 orchestre le combat (vagues) et doit :
- démarrer uniquement sur `GameState.COMBAT` (signal S11),
- instancier les ennemis en respectant le contrat DI,
- compter les morts via `enemy_died`.

Le contrat S03↔S11 est critique pour éviter la circularité (voir TR-systems-index-001).

## Decision

### 1) S03 est l'autorité du spawn et du compteur `enemies_alive`

- S03 maintient `enemies_alive: int` (source de vérité).
- S03 décrémente **uniquement** sur `EnemyHealth.enemy_died(enemy)`.

### 2) Contrat de signaux (S03 → S11/S13)

S03 publie :

```gdscript
signal wave_started(wave_number: int)
signal wave_cleared(wave_number: int)
signal all_waves_complete()
```

### 3) Contrat d'entrée (S11 → S03)

S03 écoute :

```gdscript
signal game_state_changed(new_state: GameState)  # publié par S11
```

Le spawn démarre uniquement quand `new_state == GameState.COMBAT`.

### 4) Injection des ennemis

Pour chaque ennemi instancié, S03 injecte avant `add_child()` :
- `player` (Node3D)
- `wave_manager` (self)

## Alternatives Considered

### Alternative A : Les ennemis s'auto-enregistrent dans S03
- **Pros** : moins de wiring au spawn
- **Cons** : dépendances cachées, difficile à tester, ordre d'init fragile
- **Raison du rejet** : DI explicite (ADR-0005)

## Validation Criteria

- [ ] Sur `game_state_changed(COMBAT)`, S03 démarre exactement une vague
- [ ] `enemy_died` décrémente `enemies_alive` et déclenche `wave_cleared` à 0
- [ ] Aucune vague ne spawne hors COMBAT

## GDD Requirements Addressed

| TR-ID | Requirement | ADR |
|---|---|---|
| TR-vagues-ennemis-001..004 | Structure vagues + spawn + signaux | Décisions 1–4 |
| TR-systems-index-001 | Contrat S03↔S11 (signal-based) | Décisions 2–3 |

## Related Decisions

- ADR-0011 : FSM S11 (consomme wave_* et publie game_state_changed)
- `design/gdd/vagues-ennemis.md`

