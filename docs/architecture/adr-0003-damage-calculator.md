# ADR-0003 : DamageCalculator — Patron static func

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
| **References Consulted** | `docs/engine-reference/godot/VERSION.md` |
| **Post-Cutoff APIs Used** | `static func` + `class_name` (APIs stables depuis Godot 4.0 — aucun changement post-cutoff connu pour ce patron) |
| **Verification Required** | Confirmer que `static func` dans `class_name DamageCalculator extends RefCounted` ne déclenche pas d'instanciation implicite sous Godot 4.6.2 ; vérifier que `class_name` est résolu sans conflit avec d'autres scripts du projet |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | None |
| **Enables** | None (débloque des épics d'implémentation, pas d'autres ADRs) |
| **Blocks** | Epic S02 — Saisie et lancer · Epic S09 — IA ennemie (les deux appelants de DamageCalculator.calculate) |
| **Ordering Note** | Doit être Accepted avant les stories d'implémentation de S02 et S09 |

## Context

### Problem Statement
S06 (Système de dégâts, GDD Règle 1) définit une formule pure stateless :
`max(DAMAGE_MIN, floori(damage_base × stage_mult))`. Le GDD exige que S06 soit
centralisé en un seul endroit et non dupliqué dans chaque appelant. La décision
architecturale est : comment exposer cette fonction en GDScript — statique dans
une classe nommée, Autoload, ou inline dans chaque appelant ?

### Constraints
- GDScript uniquement (pas de C# ni GDExtension)
- La fonction doit être testable en isolation (coding standards : toutes les methodes
  publiques doivent etre testables en unitaire via injection de dependances — ici, appel direct sans scene)
- Deux appelants connus à ce stade : S02 (Saisie et lancer) et S09 (IA ennemie)
- DamageType enum doit être accessible aux appelants sans instanciation

### Requirements
- Appel depuis S02 : `DamageCalculator.calculate(damage_base, stage_mult, DamageType.MELEE)` ou `DamageType.THROW`
- Appel depuis S09 : `DamageCalculator.calculate(damage_base, 1.0, DamageType.ENEMY_MELEE)`
- Résultat de type `int` (jamais `float`) — S06 Règle 5
- Testable : un test unitaire peut appeler `DamageCalculator.calculate(5, 1.0, ...)` directement sans scène

## Decision

**DamageCalculator est implémenté comme `class_name DamageCalculator extends RefCounted`
avec une `static func calculate(...)`. Le type `DamageType` est défini comme enum dans
la même classe.**

Aucune instance n'est jamais créée. Les appelants invoquent directement
`DamageCalculator.calculate(...)`. La classe est chargée automatiquement par Godot
via `class_name` — aucune déclaration Autoload requise.

### Architecture Diagram

```
src/gameplay/damage/damage_calculator.gd
  class_name DamageCalculator
  extends RefCounted

  enum DamageType { MELEE, THROW, ENEMY_MELEE }
  static func calculate(damage_base, stage_mult, damage_type) -> int

Appelants :
  GrabSystem (S02) ──▶ DamageCalculator.calculate(base, mult, MELEE | THROW)
  EnemyAI    (S09) ──▶ DamageCalculator.calculate(base, 1.0, ENEMY_MELEE)

Tests unitaires :
  tests/unit/damage/damage_calculator_test.gd
  ─ appelle DamageCalculator.calculate() directement, sans scène
```

### Key Interfaces

```gdscript
class_name DamageCalculator
extends RefCounted

## Type d'impact — pass-through pour les systèmes de feedback (S14/S15).
## N'influence pas la formule mathématique (S06 Règle 3).
enum DamageType {
    MELEE,        ## Frappe directe avec objet tenu (S02)
    THROW,        ## Objet lancé en vol (S02)
    ENEMY_MELEE   ## Attaque directe ennemi (S09)
}

## Calcule les dégâts finaux appliqués à une cible.
##
## [param damage_base] Dégâts de base — int fourni par l'appelant (lu dans catalogue
##   S05 ou défini par l'ennemi S09). Ne jamais passer un float non casté : S02 est
##   responsable du cast floori() avant l'appel (S06 Règle 2, contrat de type).
## [param stage_mult]  Multiplicateur de stade — float lu dans StageData (S05).
##   Valeur fixe 1.0 pour les ennemis (S09). Range attendu : 0.3–2.0 (S05 catalogue).
## [param damage_type] Type d'impact — ignoré dans la formule, transmis pour le feedback.
## [return] int >= 1. Jamais zéro, jamais négatif (S06 DAMAGE_MIN = 1).
static func calculate(
    damage_base: int,
    stage_mult: float,
    damage_type: DamageType
) -> int:
    return max(1, floori(damage_base * stage_mult))
```

> **STATELESS** — Ne jamais ajouter de variable d'instance, de signal, ni d'état
> à cette classe. Tout besoin d'état autour des dégâts appartient à l'appelant
> (S02, S09) ou aux récepteurs (S07, S08). Voir forbidden pattern `damage_calculator_stateful`.

## Alternatives Considered

### Alternative A : Autoload singleton
- **Description** : `DamageCalculator` enregistré dans Project Settings → Autoloads.
  Accessible depuis n'importe quel script sans import explicite.
- **Pros** : Accès global sans `class_name` ; familier pour les développeurs venant
  d'autres moteurs
- **Cons** : Instancie un `Node` au démarrage du projet pour une fonction qui n'a
  pas d'état. Crée une dépendance implicite (tout script peut appeler
  `DamageCalculator.calculate()` sans que la dépendance soit déclarée).
- **Raison du rejet** : `static func` dans une `class_name` offre le meme acces
  global sans le coût d'un nœud instancié. Les Autoloads sont réservés aux
  systèmes avec état (SceneManager, AudioBus, etc.).

### Alternative B : Inline dans chaque appelant
- **Description** : S02 et S09 implémentent chacun `max(1, floori(damage_base * stage_mult))`
  localement dans leur propre script.
- **Pros** : Zéro dépendance externe ; lisible isolément
- **Cons** : Duplique la logique — si la formule change (ex. ajout d'un cap en V1.0),
  deux fichiers doivent être modifiés simultanément. Brise le principe de S06 Règle 1.
- **Raison du rejet** : S06 GDD Regle 1 exige explicitement une centralisation :
  "si le calibrage doit changer, la formule est le point d'entrée unique."

## Consequences

### Positive
- Un seul endroit à modifier si la formule change (S06 Règle 1 satisfaite)
- Testable directement sans scène (`DamageCalculator.calculate(5, 1.0, ...)`)
- `DamageType` enum colocalisé — les appelants importent un seul `class_name` pour
  avoir la fonction ET le type
- Aucun coût d'initialisation (pas de nœud instancié, pas d'Autoload)
- Aucun état à gérer ni à réinitialiser entre les tests

### Negative
- `class_name` impose un PascalCase sur le fichier source (`DamageCalculator.gd`
  ou `damage_calculator.gd` — les deux sont valides, snake_case recommandé pour
  cohérence avec les coding standards)
- Les tests unitaires doivent charger explicitement le fichier GDScript si Godot
  ne résout pas `class_name` en mode headless (à vérifier au premier sprint)

### Risks
- **Risque** : Un futur développeur ajoute un état ou un signal à DamageCalculator,
  cassant le modèle stateless.
  - **Mitigation** : Commentaire `## STATELESS` dans le fichier source +
    forbidden pattern enregistré dans le registry (`damage_calculator_stateful`).
- **Risque** : `static func` dans `extends RefCounted` déclenche un comportement
  inattendu sous Godot 4.6.2 (edge case peu probable mais post-cutoff).
  - **Mitigation** : Test unitaire au premier sprint (3 cas couvrent la formule
    complète). Si problème : passer à `extends Object` sans changer la signature.

## GDD Requirements Addressed

| Systeme GDD | Exigence | Comment cet ADR la satisfait |
|------------|-------------|--------------------------|
| systeme-degats.md | Règle 1 : fonction pure stateless, pas un nœud, pas de signaux | `static func` sans état ni nœud |
| systeme-degats.md | Règle 1 : `class_name DamageCalculator avec static func` suggéré | Implémente exactement le patron suggéré |
| systeme-degats.md | Règle 4 : `max(DAMAGE_MIN, floori(damage_base × stage_mult))` | Expression exacte dans le corps de la fonction |
| systeme-degats.md | Règle 5 : retourne un `int` unique | `-> int` dans la signature + `max(1, floori(...))` |
| saisie-lancer.md | S02 responsable du cast float→int avant appel S06 | `damage_base: int` dans la signature — le cast est côté appelant |

## Performance Implications
- **CPU** : Une opération arithmétique par appel (`floori` + `max`). Négligeable.
- **Memory** : Aucune instance créée. Aucun état alloué. Empreinte mémoire = 0.
- **Load Time** : Aucun impact (`class_name` résolu à la compilation par Godot).
- **Network** : Sans objet (PC single-player).

## Migration Plan
Première implémentation — aucun code existant à migrer.

## Validation Criteria
1. `DamageCalculator.calculate(5, 1.0, DamageCalculator.DamageType.MELEE)` → `5` (test unitaire)
2. `DamageCalculator.calculate(1, 0.3, DamageCalculator.DamageType.THROW)` → `1` (floor DAMAGE_MIN)
3. `DamageCalculator.calculate(15, 2.0, DamageCalculator.DamageType.THROW)` → `30` (max MVP)
4. `DamageCalculator.new()` n'est jamais appelé dans le projet (enforcement par code review)
5. Test unitaire passe en mode headless (`godot --headless --script`)

## Related Decisions
- ADR-0001 : GrabSystem Architecture — S02 (GrabSystem) est l'appelant principal
- ADR-0002 : Player Body Type — contextualise S01/S09 comme environnement des appelants
- `design/gdd/systeme-degats.md` — source de la formule et de l'exigence de centralisation
- `design/gdd/saisie-lancer.md` — S02, appelant principal (melee + throw)
- `design/gdd/ia-ennemie.md` — S09, second appelant (enemy_melee, stage_mult=1.0)
