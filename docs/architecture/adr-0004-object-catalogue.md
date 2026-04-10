# ADR-0004 : Catalogue d'objets (S05) - Modele de donnees Resource + injection @export

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Godot 4.6.2 |
| **Domain** | Core / Donnees |
| **Knowledge Risk** | HIGH — post-LLM-cutoff (4.6 est post-training) |
| **References Consulted** | `docs/engine-reference/godot/VERSION.md` |
| **Post-Cutoff APIs Used** | None (Resources + @export sont stables) |
| **Verification Required** | Verifier en prototype que les Resources chargees via `@export` sont accessibles en headless (tests) et que les references ne sont jamais null en scene |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | None |
| **Enables** | ADR-0001 (GrabSystem), S04 (Degradation), S13 (HUD : silhouette) |
| **Blocks** | Epic S05 — Catalogue d'objets ; Epic S02 — Saisie et lancer ; Epic S04 — Degradation |
| **Ordering Note** | A accepter avant l'implementation de S02/S04. Les ADR qui lisent le catalogue (S02/S04) doivent dependre de celui-ci. |

## Context

### Problem Statement
S05 (Catalogue d'objets) est la source de verite des parametres par objet (physique, interaction, destruction). Sans une decision d'architecture sur le modele de donnees et le pattern d'acces, S02 (Saisie/lancer) et S04 (Degradation) risquent d'encoder des valeurs en dur, ou d'introduire un singleton global difficile a tester.

### Constraints
- GDScript uniquement (pas de C#, pas de GDExtension)
- Les donnees du catalogue sont statiques a runtime (pas d'ecriture pendant une run)
- Pas de lookup global implicite a runtime (pas d'Autoload catalogue)
- Chaque objet interactif doit etre testable / instanciable avec ses dependances explicites

### Requirements
- Un objet grabbable reference directement son entree de catalogue via `@export`
- S02 lit le catalogue a partir de l'objet tenu (pas via un registre global)
- S04 lit l'entree une seule fois a `_ready()` puis maintient son etat interne (cumul de degats / uses)
- Le modele de destruction multi-stades doit etre exprime en donnees (seuils, uses, reference visuelle par stade)

## Decision

**Le catalogue est represente par des Resources typées. Chaque objet interactif porte une reference directe a son `ObjectCatalogueEntry` via `@export`. Il n'existe pas de singleton/lookup global a runtime.**

### Architecture

```
Object (RigidBody3D) [scene d'objet]
  script: GrabbableObject.gd
  @export var catalogue_entry: ObjectCatalogueEntry
  @export var silhouette_texture: Texture2D (optionnel, pour S13)
  child: DestructionTracker (Node) [S04]
        lit catalogue_entry une seule fois en _ready()

Consommateurs :
  S02 GrabSystem -> lit held_object.catalogue_entry (parametres de saisie/degats/impulse)
  S04 Degradation -> DestructionTracker utilise catalogue_entry pour transitions de stade
  S13 HUD -> lit silhouette_texture (ou derive via catalogue_entry si on choisit de la stocker dedans)
```

### Key Interfaces (GDScript)

```gdscript
# docs d'interface — les fichiers seront crees dans src/ lors de l'implementation

class_name StageData
extends Resource

@export var damage_threshold: int = 0
@export var uses_until_break: int = -1
@export var melee_dmg_mult: float = 1.0
@export var throw_dmg_mult: float = 1.0
@export var is_final_stage: bool = false


class_name ObjectCatalogueEntry
extends Resource

@export var id: StringName
@export var display_name: String
@export var category: int  # enum Category (voir GDD S05)

# Physique (Jolt)
@export var mass_kg: float = 1.0
@export var linear_damp: float = 0.0
@export var angular_damp: float = 0.0
@export var restitution: float = 0.0

# Interaction (S02)
@export var grab_range_m: float = 2.0
@export var melee_damage_base: int = 1
@export var throw_damage_base: int = 1
@export var throw_impulse_scale: float = 1.0

# Destruction (S04)
@export var destruction_stages: Array[StageData] = []
@export var stage_mesh_paths: Array[String] = []
@export var debris_scene_path: String = ""
@export var can_damage_when_broken: bool = false

# Audio (S14, V1.0)
@export var sound_impact_key: StringName
```

### Implementation Guidelines
- Regle : **aucune valeur gameplay/physique n'est hardcodee** dans S02/S04 pour les objets ; tout provient de `catalogue_entry`.
- Regle : pas d'Autoload pour le catalogue. Le catalogue est "local" a l'objet via `@export`.
- Convention : tous les objets grabbables doivent exposer `catalogue_entry` sur le node racine de l'objet (pas sur un enfant).
- Validation editor : ajouter un check en debug (au premier sprint) qui log/asserte si `catalogue_entry == null` sur un objet grabbable.

## Alternatives Considered

### Alternative A : Catalogue global en Autoload (singleton)
- **Description** : une Resource ou un Node Autoload maintient un dictionnaire `id -> entry`, et les objets stockent seulement un `object_id`
- **Pros** : references legeres par objet ; edition centralisee
- **Cons** : dependance implicite globale ; testabilite reduite ; risque de lookup runtime + erreurs silencieuses (id manquant)
- **Raison du rejet** : le projet privilegie des dependances explicites injectees ; `@export` sur l'objet rend l'erreur visible en scene.

### Alternative B : Donnees en JSON/CSV chargees a runtime
- **Description** : charger un fichier de donnees au demarrage et construire les entries en code
- **Pros** : edition en dehors de Godot ; potentiellement plus simple pour des gros catalogues
- **Cons** : parsing runtime + risques d'erreurs de schema ; moins integra avec l'inspecteur Godot ; plus difficile a refactorer
- **Raison du rejet** : scope MVP petit (8-15 objets) ; l'edition dans l'inspecteur est plus rapide et plus robuste.

## Consequences

### Positive
- Dependances explicites : chaque objet declare son entree de catalogue
- Testabilite : S02/S04 peuvent etre testes avec des Resources de test injectees
- Pipeline Godot natif : tuning facile via l'inspecteur (pas d'etape de parsing)

### Negative
- Cablage a faire pour chaque scene d'objet (risque d'oubli)
- Doublons possibles si deux scenes referencent accidentellement la mauvaise entree

## Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| `catalogue_entry` non assignee sur un objet grabbable | MEDIUM | HIGH | Assertions/logs en debug + check liste dans un test de scene |
| Donnees incoherentes (seuils / uses / scenes visuelles manquantes) | MEDIUM | MEDIUM | Validation simple : verifier tailles de tableaux et valeurs >= 0 au chargement |

## Performance Implications
- **CPU** : negligeable (lecture de champs Resource)
- **Memory** : N entries Resource (8-15) + references. Negligeable.
- **Load Time** : depend du nombre de `visual_scene` referencees ; en MVP, rester minimal.

## Migration Plan
Premier ADR sur S05 — pas de migration.

## Validation Criteria
- [ ] Un objet grabbable instancie en scene a toujours une `catalogue_entry` non-null
- [ ] S02 peut lire `grab_range_m`, `melee_damage_base`, `throw_impulse_scale` depuis l'objet tenu sans lookup global
- [ ] S04 lit l'entree une seule fois en `_ready()` et les transitions de stade sont pilotables en modifiant les Resources

## GDD Requirements Addressed

| GDD Document | Systeme | Exigence | Comment cet ADR satisfait l'exigence |
|-------------|--------|-------------|--------------------------|
| `design/gdd/catalogue-objets.md` | S05 | Donnees statiques en Resources ; reference directe via `@export` ; pas de lookup global | Modele Resource + injection `@export` |
| `design/gdd/catalogue-objets.md` | S05/S04 | Destruction multi-stades pilotee par seuils/uses | `StageData` + `destruction_stages` |
| `design/gdd/saisie-lancer.md` | S02 | S02 lit les parametres au moment de la saisie | S02 lit via `held_object.catalogue_entry` |

## Related Decisions
- ADR-0001 : GrabSystem Architecture (consomme le catalogue)
- `design/gdd/catalogue-objets.md` — source de la structure de donnees
