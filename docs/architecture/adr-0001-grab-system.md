# ADR-0001: GrabSystem Architecture

## Status
Proposed

## Date
2026-04-09

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Godot 4.6.2 |
| **Domain** | Core / Physics |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `docs/engine-reference/godot/modules/physics.md`, `docs/engine-reference/godot/breaking-changes.md` |
| **Post-Cutoff APIs Used** | `RigidBody3D.freeze = true` + `freeze_mode = RigidBody3D.FREEZE_MODE_KINEMATIC` (API stable, confirmé 4.6) |
| **Verification Required** | Vérifier que `freeze_mode KINEMATIC` préserve la position sous Jolt en 4.6.2 ; vérifier que `apply_central_impulse()` produit un comportement cohérent sur Jolt |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | None |
| **Enables** | ADR-0002 (CharacterBody3D pattern — peut être rédigé en parallèle) |
| **Blocks** | Epic S02 — Saisie et lancer (ne peut pas commencer l'implémentation sans ce ADR Accepted) |
| **Ordering Note** | Doit être Accepted avant la création des stories S02 |

## Context

### Problem Statement
S02 (Saisie et lancer) nécessite un composant logiciel qui gère la machine à états
EMPTY_HANDS / CARRYING, orchestre les appels Jolt (`freeze`, `apply_central_impulse`),
et émet les signaux vers S08, S04 et S11. La décision architecturale est : où ce
composant doit-il vivre dans le scene tree, et comment reçoit-il ses dépendances ?

### Constraints
- GDScript uniquement (pas de C# ni GDExtension pour ce système)
- Le système doit être testable en isolation (coding standards : dependency injection over singletons)
- Un seul joueur — pas besoin de gestion multi-instance
- Jolt est le moteur physique actif (Godot 4.6 default)

### Requirements
- Doit gérer l'état EMPTY_HANDS / CARRYING de façon centralisée
- Doit lire les propriétés d'objet via S05 (catalogue)
- Doit émettre les signaux `grab_performed`, `throw_performed`, `melee_performed` consommés par S08, S04, S11
- Doit recevoir la direction du yaw caméra (S03) pour orienter le lancer
- Doit être instanciable sans le reste du scene tree (unit testing)

## Decision

**GrabSystem est un nœud `Node` enfant de la scène Player, dont les dépendances
externes sont injectées via propriétés `@export`.**

Il n'est pas un Autoload. Il n'accède pas à ses dépendances par chemin de nœud absolu.
Toute communication vers l'extérieur passe exclusivement par des signaux GDScript.

### Architecture Diagram

```
Player (CharacterBody3D)           ← S01
├── GrabSystem (Node)              ← ce composant
│     @export var camera_pivot: Node3D      ← injecté par Player scene
│     @export var catalogue: Resource       ← S05 ObjectCatalogue resource
│     var held_object: RigidBody3D          ← état interne
│     var state: GrabState                  ← EMPTY_HANDS | CARRYING
│     signal grab_performed(obj)
│     signal throw_performed(obj, impulse)
│     signal melee_performed(obj)
│     signal object_dropped(obj)
└── CameraPivot (Node3D)           ← S03 (référence injectée dans GrabSystem)

Listeners (s'abonnent aux signaux de GrabSystem) :
  EnemyHealth (S08) ──▶ melee_performed, throw_performed
  Degradation (S04) ──▶ melee_performed, throw_performed
  ScoreSystem (S11) ──▶ grab_performed, throw_performed, melee_performed
```

### Key Interfaces

```gdscript
class_name GrabSystem
extends Node

enum GrabState { EMPTY_HANDS, CARRYING }

@export var camera_pivot: Node3D      # Source du yaw pour le lancer
@export var catalogue: Resource       # ObjectCatalogue S05

signal grab_performed(object: RigidBody3D)
signal throw_performed(object: RigidBody3D, impulse: Vector3)
signal melee_performed(object: RigidBody3D)
signal object_dropped(object: RigidBody3D)

var state: GrabState = GrabState.EMPTY_HANDS
var held_object: RigidBody3D = null

func try_grab() -> void      # Cone check + saisie
func melee_strike() -> void  # Arc de frappe + emission signal
func throw_object() -> void  # apply_central_impulse + EMPTY_HANDS
func drop_object() -> void   # Dépôt sans dégâts
```

## Alternatives Considered

### Alternative A : Autoload Singleton (`GrabSystem` global)
- **Description** : `GrabSystem` enregistré comme Autoload, accessible via `GrabSystem.try_grab()` depuis n'importe quel nœud
- **Pros** : Accès simple sans injection ; pas de câblage de scène
- **Cons** : Couplage global implicite ; impossible à mocker en tests unitaires ; sémantiquement incorrect (le GrabSystem est player-specific, pas un service global)
- **Rejection Reason** : Viole le principe de testabilité des coding standards ("all public methods must be unit-testable via dependency injection") et crée une dépendance cachée que tout système peut appeler sans déclaration explicite

### Alternative B : Nœud enfant sans injection (accès par chemin absolu)
- **Description** : `GrabSystem` enfant du Player, accède à ses dépendances via `get_node("../CameraPivot")` ou `get_tree().get_first_node_in_group("camera")`
- **Pros** : Plus simple à câbler initialement
- **Cons** : Couplage aux chemins de nœuds — cassant dès que la structure de scène change ; impossible à tester hors scène complète
- **Rejection Reason** : Fragile face aux refactorings de scène ; même problème de testabilité que l'Autoload

## Consequences

### Positive
- GrabSystem est testable en isolation (injecter des mocks via @export)
- Les dépendances sont explicites et visibles dans l'éditeur Godot
- Le couplage est unidirectionnel : GrabSystem émet des signaux, les consumers s'abonnent — pas de références inverses
- Suit le pattern signal établi par S02 GDD (contrat de signaux, résolution de circularité)

### Negative
- Câblage @export à faire dans la scène Player (2-3 connexions manuelles dans l'éditeur)
- Les tests unitaires doivent instancier GrabSystem et injecter des doubles de test

### Risks
- **Risque** : `freeze_mode KINEMATIC` sous Jolt 4.6.2 pourrait avoir un comportement légèrement différent de GodotPhysics3D en edge cases (objets très légers, collisions simultanées)
  - **Mitigation** : Vérifier au premier prototype (sprint 1) avec les 3 objets les plus légers du catalogue S05

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| saisie-lancer.md | Porter : objet passe en mode kinematic, suit carry_offset | `try_grab()` appelle `held_object.freeze = true` + `freeze_mode = KINEMATIC` |
| saisie-lancer.md | Lancer : `apply_central_impulse()` dans direction yaw caméra | `throw_object()` lit `camera_pivot.global_rotation.y`, calcule impulse, appelle `apply_central_impulse()` |
| saisie-lancer.md | Signaux `grab_performed`, `throw_performed`, `melee_performed` | Définis comme signaux GDScript dans Key Interfaces |
| saisie-lancer.md | S02 responsable du cast float→int avant appel S06 | `melee_strike()` / `throw_object()` castent `catalogue.damage_base` en int avant d'émettre |
| deplacement-joueur.md | S01 gère le mouvement pendant CARRYING | GrabSystem ne touche pas à la vélocité Player ; S01 continue `move_and_slide()` indépendamment |

## Performance Implications
- **CPU** : Negligeable — le cone check est un raycast unique par frame en état EMPTY_HANDS ; aucun calcul en CARRYING (position fixe)
- **Memory** : Un nœud léger + 1 référence RigidBody3D — negligeable
- **Load Time** : Aucun impact
- **Network** : Sans objet (PC single-player)

## Migration Plan
Premier ADR du projet — pas de code existant à migrer.

## Validation Criteria
1. `GrabSystem` s'instancie sans erreur avec des mocks @export null (mode test)
2. `try_grab()` émet `grab_performed` avec le bon objet dans les tests unitaires
3. Au prototype : l'objet porté suit le joueur sans glisser ni traverser les murs
4. Au prototype : `apply_central_impulse()` produit une trajectoire cohérente sous Jolt 4.6.2

## Related Decisions
- ADR-0002 (à écrire) : CharacterBody3D + move_and_slide() kinematic pattern (S01)
- `design/gdd/saisie-lancer.md` — spécification de S02
- `design/gdd/deplacement-joueur.md` — S01, propriétaire du mouvement Player
