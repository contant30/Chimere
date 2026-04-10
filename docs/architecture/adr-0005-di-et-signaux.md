# ADR-0005 : Conventions d'injection de dependances (DI) et de signaux (GDScript)

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Godot 4.6.2 |
| **Domain** | Core / Scripting |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `docs/engine-reference/godot/deprecated-apis.md`, `.claude/docs/technical-preferences.md` |
| **Post-Cutoff APIs Used** | None |
| **Verification Required** | Verifier dans les premiers scripts que les connexions de signaux sont bien en Callable (pas string-based) et que les dependances sont injectees avant `_ready()` |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | None |
| **Enables** | Tous les systemes (S01..S13) — conventions transversales |
| **Blocks** | Toute implementation gameplay (stories) impliquant des dependances cross-node ou des signaux |
| **Ordering Note** | A accepter avant la redaction des stories, sinon on fige des patterns incoherents. |

## Context

### Problem Statement
Le projet repose sur un graphe de nodes (Godot) et des interactions par signaux (S03, S07, S08, S10, S11, S13, GrabSystem). Sans conventions explicites, on risque :
- des dependances cachees (Autoload / get_node absolu) qui cassent la testabilite ;
- des connexions string-based `connect("signal", ...)` (depreciees) difficiles a refactorer ;
- des cycles de dependances implicites entre systemes.

### Constraints
- GDScript uniquement
- Projet PC (pas de contraintes mobile)
- Testabilite prioritaire : dependances explicites, instanciation possible en isolation

### Requirements
- Les systemes doivent communiquer via signaux typés ou appels explicites injectes (pas via globals caches)
- Les connexions de signaux doivent etre refactor-friendly (Callable-based)
- Les dependances cross-node doivent etre visibles dans l'editeur (Inspector) quand pertinent

## Decision

**On standardise :**
1. **Injection de dependances** via `@export` (references de nodes/resources) pour les dependances cross-node.
2. **Communication inter-systemes** via **signaux GDScript typés** (quand c'est un event) et par appels directs seulement quand la relation est ownership/commande.
3. **Connexions de signaux** exclusivement en **Callable-based connect** (interdit : string-based connect).
4. **Aucun singleton (Autoload)** sans ADR dedie justifiant l'etat global.

### Key Interfaces (GDScript)

```gdscript
# DI (exemple)
@export var player: Node3D
@export var wave_manager: Node

func _ready() -> void:
    assert(player != null)

# Signal typé + connect Callable (exemples)
signal player_died()
signal player_hit(damage: int, damage_type: DamageCalculator.DamageType, current_hp: int)

func _ready() -> void:
    # BON : Callable-based
    player_died.connect(_on_player_died)

    # INTERDIT : string-based (deprecie)
    # connect("player_died", self, "_on_player_died")
```

### Implementation Guidelines
- DI :
  - Pour une dependance vers un node "pair" (ex: S11 -> S10 freeze/unfreeze) : `@export var camera_controller: Node` injecte dans la scene.
  - Pour une dependance vers une donnee statique (S05) : `@export var catalogue_entry: Resource` ou reference par objet.
  - Interdit : `get_tree().get_first_node_in_group(...)` comme mecanisme primaire d'acces (autorise uniquement en debug/outils).
- Signaux :
  - Nommage : `snake_case` au passe quand c'est un evenement (ex: `enemy_died`, `health_changed`) ; conforme `.claude/docs/technical-preferences.md`.
  - Les signaux traversant les systemes (S03<->S11, S07->S11/S13, S08->S03) doivent etre declares sur le proprietaire du cycle de vie de la donnee.
- Couplage :
  - Preferer "event out" (signal) plutot que "pull" (polling) entre systemes.
  - Limiter les appels directs aux relations d'orchestration (ex: S11 -> S10.freeze()).

## Alternatives Considered

### Alternative A : Autoloads pour tous les services (EventBus global)
- **Description** : un Autoload expose des signaux globaux ; tous les systemes publient/ecoutent via ce bus
- **Pros** : wiring simple ; decouplage apparent
- **Cons** : dependance globale implicite ; debug difficile ; tests plus fragiles (etat global)
- **Raison du rejet** : contraire au principe de dependances explicites ; risque de spaghetti event-driven.

### Alternative B : get_node absolu / groupes comme mecanisme principal
- **Description** : les systemes se trouvent via NodePath, groupes, ou `get_tree()`
- **Pros** : moins de cablage manuel
- **Cons** : fragile au refactor ; dependances invisibles ; erreurs runtime tardives
- **Raison du rejet** : la maintenance et la testabilite degradent vite, surtout en GDScript.

## Consequences

### Positive
- Refactor plus sur (Callable connect + signaux typés)
- Dependances explicites et visibles dans l'editeur
- Tests plus simples (injection de doubles via `@export` ou assignment directe)

### Negative
- Plus de cablage manuel dans les scenes
- Necessite une discipline de code review (interdire Autoloads et connect string-based)

## Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Les scenes oublient d'injecter une dependance `@export` | MEDIUM | HIGH | Assertions en `_ready()` + check-lists QA / scenes de test |
| Retour des patterns depreciees (connect string-based) | MEDIUM | MEDIUM | Regle de revue + grep CI plus tard |

## Validation Criteria
- [ ] Aucun `connect("...")` string-based dans `src/` (utiliser Callable)
- [ ] Toute dependance cross-node est soit `@export`, soit documentee par ADR (exception justifiee)
- [ ] Aucun Autoload ajoute sans ADR dedie

## GDD Requirements Addressed

Foundational — pas de requirement GDD direct. Contraint et debloque l'implementation des systemes en imposant DI + signaux coherents (notamment S03/S11, S07/S13, S08/S03, S10/S01, S02/S08/S04).

## Related Decisions
- ADR-0004 : Catalogue d'objets (S05) — injection `@export` par objet
