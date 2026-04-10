# ADR-0008 : S07/S08 Health contracts (receive_damage + signaux)

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Godot 4.6.2 |
| **Domain** | Core / Gameplay |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `design/gdd/sante-joueur.md`, `design/gdd/sante-ennemie.md`, `docs/architecture/adr-0003-damage-calculator.md` |
| **Post-Cutoff APIs Used** | Signaux GDScript typés (stable) |
| **Verification Required** | Valider en tests GUT que l'unicité de `*_died` tient en multi-hit même frame |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0003 (DamageType enum), ADR-0005 (signaux Callable) |
| **Enables** | S03 (compteur de morts), S11 (game over), S13 (HUD) |
| **Blocks** | Stories S07/S08 (sinon contrats divergents) |
| **Ordering Note** | À accepter avant S03/S07/S08/S13 |

## Context

Le projet a deux implémentations de “health” :
- S07 : joueur (singleton de session, i-frames).
- S08 : ennemi (multi-instancié, pas d'i-frames).

Ils doivent partager le même contrat entrant pour simplifier l'appelant (S02/S09) et centraliser le type `DamageType`.

## Decision

### 1) Interface entrante unifiée

S07 et S08 exposent la même méthode :

```gdscript
func receive_damage(amount: int, damage_type: DamageCalculator.DamageType) -> void
```

Règles communes :
- `amount` est un `int` (S06 garantit `>= 1`, mais 0 est traité comme no-op défensif).
- Si l'entité est déjà DEAD, l'appel est ignoré silencieusement.

### 2) Signaux sortants

S07 (joueur) :

```gdscript
signal player_hp_changed(current_hp: int, max_hp: int)      # vers S13
signal player_hit(damage: int, damage_type: DamageCalculator.DamageType, current_hp: int)  # vers S11/S13
signal player_died()                                       # vers S11
```

S08 (ennemi) :

```gdscript
signal enemy_hit(damage: int, damage_type: DamageCalculator.DamageType, current_hp: int)   # vers S15 (V1.0)
signal enemy_died(enemy: Node)                                                             # vers S03
```

### 3) Ownership

- S07 est l'unique propriétaire de `player_current_hp`.
- Chaque instance S08 est propriétaire de son `enemy_current_hp`.
- Aucun autre système ne modifie directement ces valeurs (voir ADR-0005 : pas d'écriture cross-système).

### 4) Consommateurs en MVP

- `player_died()` : consommé par S11 (FSM).
- `player_hp_changed/player_hit` : consommés par S13 (HUD) et optionnellement S11.
- `enemy_died(enemy)` : consommé par S03 (WaveManager) pour décrémenter `enemies_alive`.

Le “score” n'est pas un système MVP : aucun contrat S12 “Score” n'existe dans l'index.

## Alternatives Considered

### Alternative A : Deux signatures différentes (player vs enemy)
- **Pros** : plus “expressif”
- **Cons** : complexifie l'appelant et le typage, augmente les erreurs
- **Raison du rejet** : S02/S09 doivent appeler la même API

## Validation Criteria

- [ ] `receive_damage()` réduit `current_hp` et n'émet pas de signaux si `amount == 0`
- [ ] `*_died` est émis exactement une fois (idempotence en DEAD)
- [ ] S07 ignore les dégâts pendant les i-frames, S08 ne les ignore jamais

## GDD Requirements Addressed

| TR-ID | Requirement | ADR |
|---|---|---|
| TR-sante-joueur-001..003 | Contrats S07 (receive_damage + signaux + i-frames) | Décisions 1–4 |
| TR-sante-ennemie-001..003 | Contrats S08 (receive_damage + signaux + no i-frames) | Décisions 1–4 |

## Related Decisions

- ADR-0003 : DamageCalculator (DamageType)
- ADR-0005 : DI + signaux

