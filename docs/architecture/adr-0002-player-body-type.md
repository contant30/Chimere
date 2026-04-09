# ADR-0002: Player Body Type and Collision Layers

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
| **Post-Cutoff APIs Used** | `CharacterBody3D.move_and_slide()` (API stable), `collision_layer` / `collision_mask` bitmask integers (stable) |
| **Verification Required** | Vérifier que move_and_slide() ne génère aucun impulse sur RigidBody3D adjacent sous Jolt 4.6.2 ; vérifier le comportement du raycast GrabSystem avec collision_mask = 3 dans une scène peuplée |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | None |
| **Enables** | ADR-0001 (GrabSystem — collision_mask du raycast S02 dépend du layer 3 défini ici) |
| **Blocks** | Epic S01 — Déplacement joueur (ne peut pas commencer l'implémentation sans ce ADR Accepted) |
| **Ordering Note** | Doit être Accepted avant la création des stories S01 ; ADR-0001 peut être Accepted en parallèle |

## Context

### Problem Statement
S01 (Déplacement joueur) nécessite un corps physique pour le joueur. La scène contient
simultanément des RigidBody3D (objets saisissables — S02/S05) et des ennemis (S08).
Deux décisions doivent être tranchées : (1) quel type de corps physique pour le joueur,
(2) quel schéma de layers de collision pour isoler les interactions.

La contrainte critique de S01 (Core Rule 7) : le joueur **ne doit pas pousser** les
objets RigidBody3D en marchant dessus — le comportement naturel de `move_and_slide()`
est la contrainte, pas du code additionnel.

### Constraints
- GDScript uniquement (pas de C#)
- Jolt est le moteur physique actif (Godot 4.6 default)
- Le joueur ne doit pas pousser les objets en marchant (Core Rule 7, S01)
- Le GrabSystem (S02) doit pouvoir rayer uniquement les objets saisissables, pas le joueur ni les ennemis
- Les ennemis doivent bloquer le passage du joueur (collision player↔enemy active)
- Un seul joueur — pas de gestion multi-instance

### Requirements
- Mouvement déterministe et prévisible dans des salles ~10×10 m remplies d'objets
- Séparation propre des layers : le raycast S02 ne doit toucher que les objets (layer 3)
- Compatibilité avec GrabSystem : objets en mode KINEMATIC restent en layer 3
- Testable en isolation (pas de dépendance implicite à la structure de scène)

## Decision

**Le joueur utilise `CharacterBody3D` + `move_and_slide()`. La scène utilise un
schéma à 4 layers de collision.**

`move_and_slide()` ne génère pas d'impulse sur les RigidBody3D — il glisse le long
des surfaces. C'est le comportement voulu : aucun code de poussée ne doit être ajouté.

### Schéma de collision (4 layers)

```
Layer 1 — World :    StaticBody3D (murs, sol, plafond)
Layer 2 — Player :   CharacterBody3D (joueur)
Layer 3 — Objects :  RigidBody3D (objets saisissables — S05)
Layer 4 — Enemies :  CharacterBody3D / corps ennemis

Player  collision_layer = 2,   collision_mask = 1 | 3 | 4  (bloqué par world + objets + ennemis)
Objects collision_layer = 3,   collision_mask = 1 | 3 | 4  (rebondissent sur floor, se heurtent)
Enemies collision_layer = 4,   collision_mask = 1 | 3 | 4  (bloqués par tout)
World   collision_layer = 1,   collision_mask = 0           (statique, pas de détection active)
```

### Architecture Diagram

```
CharacterBody3D (Player)          layer=2, mask=1|3|4
├── GrabSystem (Node)             ─ S02 : raycast mask=3 seulement
│     PhysicsRayQueryParameters3D.collision_mask = 3
└── CameraPivot (Node3D)          ─ S03

RigidBody3D (Object)              layer=3, mask=1|3|4
  → freeze=true + KINEMATIC quand porté (S02)
  → layer=3 conservé même en état KINEMATIC

CharacterBody3D (Enemy)           layer=4, mask=1|3|4
StaticBody3D (World)              layer=1, mask=0
```

### Key Interfaces (GDScript)

```gdscript
# Player (CharacterBody3D) — dans Player.gd ou _ready()
collision_layer = 2
collision_mask  = 0b0000_1101  # 1 | 4 | 8 = layers 1, 3, 4

# Object (RigidBody3D) — dans object scene
collision_layer = 4            # layer 3 (bitmask bit 2, valeur 4)
collision_mask  = 0b0000_1101  # 1 | 4 | 8

# Enemy (CharacterBody3D) — dans enemy scene
collision_layer = 8            # layer 4 (bitmask bit 3, valeur 8)
collision_mask  = 0b0000_1101  # 1 | 4 | 8

# GrabSystem raycast (S02) — uniquement les objets
var query := PhysicsRayQueryParameters3D.create(origin, target)
query.collision_mask = 4  # layer 3 seulement (bitmask valeur 4)

# move_and_slide() — aucune modification ; pas de code de poussée
func _physics_process(delta: float) -> void:
    velocity = _compute_velocity(delta)
    move_and_slide()  # glisse le long des surfaces, ne pousse pas les RigidBody3D
```

> **Note bitmask** : En GDScript, `collision_layer` et `collision_mask` sont des
> entiers bitmask. Layer N correspond à la valeur `1 << (N-1)`.
> Layer 1 = 1, Layer 2 = 2, Layer 3 = 4, Layer 4 = 8.

## Alternatives Considered

### Alternative A : RigidBody3D pour le joueur
- **Description** : Joueur piloté par forces physiques ; mouvement via `apply_force()` ou `linear_velocity`
- **Pros** : Interactions physiques réalistes avec l'environnement
- **Cons** : Comportement imprévisible dans une scène dense d'objets ; difficile à contrôler précisément ; les mouvements de plateforme (saut, coyote time) sont notoirement difficiles avec RigidBody3D
- **Rejection Reason** : Incompatible avec les exigences de contrôle précis de S01 (coyote time, jump buffering) ; Jolt amplifie l'imprévisibilité dans des salles petites (10×10 m) avec de nombreux objets

### Alternative B : AnimatableBody3D
- **Description** : Corps animé déplacé par `move_and_collide()` ou transform direct
- **Pros** : Déplacement entièrement scriptable sans physique
- **Cons** : Pas conçu pour des personnages pilotés par l'input ; ne bénéficie pas des helpers de CharacterBody3D (is_on_floor, move_and_slide, etc.)
- **Rejection Reason** : Mauvais outil pour le cas d'usage ; CharacterBody3D est le standard Godot pour les personnages joueurs

### Alternative C : CharacterBody3D avec code de poussée ajouté
- **Description** : CharacterBody3D + move_and_slide(), mais avec un block de code qui applique un impulse aux RigidBody3D touchés pendant le déplacement
- **Pros** : Permet de pousser les objets avec le corps
- **Cons** : Contraire à la Core Rule 7 de S01 ; complique le système de saisie (le joueur pourrait "pousser" un objet qu'il essaie de saisir)
- **Rejection Reason** : Explicitement interdit par S01. La non-poussée est un comportement voulu, pas un manque à combler.

## Consequences

### Positive
- Mouvement joueur prévisible et contrôlable (CharacterBody3D est le standard Godot)
- Core Rule 7 respectée naturellement — aucun code additionnel requis
- Le raycast GrabSystem (mask=3) est totalement indépendant du mask de collision du joueur
- Les 4 layers sont suffisants pour le MVP ; extensibles sans breaking changes (layers 5-32 disponibles)
- Configuration inspectable dans l'éditeur Godot (Inspector → CollisionObject3D)

### Negative
- Pas d'interactions physiques entre joueur et environnement au corps à corps (pas de "pousse les caisses en marchant")
- Configuration des layers doit être reproductible dans chaque scène concernée (Player, Object, Enemy) — risque d'incohérence si fait manuellement

### Risks
- **Risque** : Un développeur pourrait ajouter du code de poussée RigidBody3D dans le mouvement player en pensant que c'est un bug
  - **Mitigation** : Forbidden pattern enregistré dans le registry (`player_body_impulse_coupling`) ; commentaire explicite dans Player.gd
- **Risque** : move_and_slide() sous Jolt 4.6.2 pourrait avoir un comportement légèrement différent de GodotPhysics3D sur des pentes ou collisions simultanées
  - **Mitigation** : Vérifier au premier prototype avec la géométrie de salle type (sol plat + murs droits = cas simple)

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| deplacement-joueur.md | Core Rule 1 : CharacterBody3D + move_and_slide() | Décision principale de cet ADR |
| deplacement-joueur.md | Core Rule 7 : le joueur ne pousse pas les RigidBody3D | move_and_slide() ne génère pas d'impulse — comportement naturel confirmé |
| deplacement-joueur.md | OQ-04 : ADR blocker pour kinematic pattern + collision layers | Cet ADR résout OQ-04 |
| saisie-lancer.md | GrabSystem raycast doit cibler uniquement les objets saisissables | collision_mask=4 (layer 3 seulement) sur PhysicsRayQueryParameters3D |
| saisie-lancer.md | Objets en KINEMATIC restent dans la scène physique | Layer 3 conservé même en freeze_mode KINEMATIC |

## Performance Implications
- **CPU** : CharacterBody3D + move_and_slide() est le pattern le plus optimisé de Godot pour les personnages ; negligeable
- **Memory** : Aucun impact (structure de nœud standard)
- **Load Time** : Aucun impact
- **Network** : Sans objet (PC single-player)

## Migration Plan
Premier ADR de mouvement du projet — pas de code existant à migrer.

## Validation Criteria
1. Le joueur se déplace sans pousser les objets RigidBody3D stationnaires (test manuel prototype)
2. `GrabSystem.try_grab()` ne détecte pas le joueur ni les ennemis dans le raycast (test unitaire avec mocks)
3. Les ennemis bloquent le passage du joueur (test manuel prototype)
4. Les objets lancés (throw_object) rebondissent sur le sol et les murs (layers 1) et heurtent les ennemis (layer 4)
5. `move_and_slide()` retourne `is_on_floor() == true` sur sol plat sous Jolt 4.6.2

## Related Decisions
- ADR-0001 : GrabSystem Architecture — utilise collision_mask=3 (layer 3) pour le raycast
- `design/gdd/deplacement-joueur.md` — S01, source des Core Rules et OQ-04
- `design/gdd/saisie-lancer.md` — S02, source de l'exigence de raycast isolé
