# ADR-0009 : S09 Enemy scene contract (composition + DI + signaux)

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Godot 4.6.2 |
| **Domain** | Core / Enemies |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `design/gdd/ia-ennemie.md`, `design/gdd/sante-ennemie.md`, `docs/architecture/adr-0008-health-contracts.md` |
| **Post-Cutoff APIs Used** | `NavigationAgent3D` (stable) |
| **Verification Required** | Valider le fallback STUCK dans une salle encombrée (proto) |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0005 (DI + signaux), ADR-0008 (Health contracts) |
| **Enables** | S03 (WaveManager) |
| **Blocks** | Epic S09 — IA ennemie |
| **Ordering Note** | À accepter avant les stories S03/S09/S08 |

## Context

L'ennemi est un “bundle” de comportements : navigation/mouvement (S09) + points de vie (S08). Le spawner (S03) doit pouvoir instancier l'ennemi et injecter ses dépendances avant `_ready()`.

Les anciennes mentions “score_manager / vfx_manager” ne font pas partie du MVP (S15 = V1.0, pas de système Score dans l'index).

## Decision

### 1) Composition de scène

```
EnemyRoot (CharacterBody3D)            # collisions / déplacement
  ├─ EnemyAI (Node)                    # S09
  ├─ EnemyHealth (Node)                # S08
  └─ (optionnel) NavigationAgent3D      # selon implémentation S09
```

### 2) Dépendances injectées par le spawner (S03)

S03 injecte **avant** `add_child()` :

```gdscript
@export var player: Node3D
@export var wave_manager: Node  # S03
```

S09 est responsable de câbler les signaux de S08 vers S03 :

- `EnemyHealth.enemy_died(enemy)` → `WaveManager._on_enemy_died(enemy)`
- (V1.0) `EnemyHealth.enemy_hit(...)` → S15

### 3) Aucune dépendance globale

Interdits :
- Autoloads pour retrouver le player ou le wave manager
- `get_tree().get_first_node_in_group(...)` comme mécanisme primaire

## Alternatives Considered

### Alternative A : EnemyAI gère aussi le HP
- **Pros** : moins de nodes
- **Cons** : mélange responsabilités, casse les tests et le contrat unifié S07/S08
- **Raison du rejet** : S08 doit rester isolé, multi-instancié et testable

## Validation Criteria

- [ ] Un ennemi instancié sans `player` ou `wave_manager` échoue tôt (assert en debug)
- [ ] `enemy_died` est correctement relayé vers S03
- [ ] Aucun couplage par NodePath absolu dans S09/S08

## GDD Requirements Addressed

| TR-ID | Requirement | ADR |
|---|---|---|
| TR-ia-ennemie-001..004 | Composition + injection + fallback | Décisions 1–3 |

## Related Decisions

- ADR-0005 : DI + signaux
- ADR-0008 : Health contracts
- `design/gdd/ia-ennemie.md`

