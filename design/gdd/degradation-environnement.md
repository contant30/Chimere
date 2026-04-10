# S04 — Dégradation d'environnement

> **Statut**: Approuvé  
> **Auteur**: ROM.CONTANT + agents  
> **Dernière mise à jour**: 2026-04-10  
> **Implémente le Pilier**: Pilier 3 — La pièce raconte

## Overview

S04 — Dégradation d'environnement est le système qui fait vieillir, casser et raconter la pièce à mesure que le joueur l'utilise comme arsenal. Il gère l'état de destruction des objets interactifs (S05), fait évoluer leurs représentations visuelles par stades, et génère des débris au stade final. S04 n'invente aucune donnée : il lit la définition des stades dans le catalogue (S05) et maintient uniquement l'état runtime (stade courant, dégâts cumulés, usages).

Techniquement, S04 se matérialise par un composant `DestructionTracker` attaché à chaque objet `RigidBody3D` interactif. Le tracker est la seule source de vérité de l'état de casse d'un objet pendant une run. Les systèmes qui produisent des impacts (S02) ou des collisions (futur) appellent le tracker via une interface minime : `receive_damage(amount, damage_type, impact_position)` et `register_use(use_kind)`. Quand un stade change, S04 met à jour le visuel (mesh/scène du stade) et publie un signal `destruction_stage_changed` pour la lisibilité (HUD/VFX en V1.0).

## Player Fantasy

Le joueur ne détruit pas une ressource abstraite, il détruit la pièce elle-même. Chaque choix (frapper avec une chaise plutôt que lancer une bouteille) écrit une trace visible : des meubles abîmés qui tiennent encore un peu, des objets qui éclatent et deviennent des débris inutilisables. La pièce devient un historique jouable : on peut “lire” la partie dans l'état des objets restants. C'est le pilier 3 au niveau mécanique : la salle n'est pas un décor neutre, c'est la mémoire de la session.

## Detailed Design

### Core Rules

1. **Propriétaire de l'état** : S04 est propriétaire de l'état runtime de destruction d'un objet (stade, dégâts cumulés, usages). S05 est propriétaire des seuils et des assets par stade.
2. **Lecture unique du catalogue** : `DestructionTracker` lit `catalogue_entry` une seule fois dans `_ready()` et n'effectue aucun lookup global.
3. **Deux voies de dégradation** :
   - **Dégâts reçus** : `receive_damage(amount)` ajoute à `_cumulative_damage`.
   - **Usages** : `register_use()` incrémente `_uses_in_stage` (frappes et lancers).
4. **Transition de stade** : une transition se déclenche si **au moins une** des conditions du stade courant est atteinte :
   - `_cumulative_damage >= damage_threshold[next_stage]` (si un seuil existe)
   - `_uses_in_stage >= uses_until_break[current_stage]` (si `uses_until_break != -1`)
5. **Reset d'usage** : à chaque transition de stade, `_uses_in_stage` est remis à 0. Les dégâts cumulés ne sont pas réinitialisés.
6. **Stade final** : quand l'objet atteint le dernier stade, il devient **cassé**. S04 instancie la scène de débris (`debris_scene_path`) à la position d'impact et applique un léger scatter (physique Jolt naturelle). Le node original de l'objet peut :
   - soit être remplacé par un “debris root” (recommended) ;
   - soit être désactivé (`collision_layer=0`, `visible=false`) et garder le debris instancié comme enfant.
7. **Objet cassé et saisie** : si `can_damage_when_broken == false`, alors un objet au stade final est non-saisissable (S02 refuse la saisie).

### State Model

`DestructionTracker` maintient :

- `_current_stage: int` (0..last)
- `_cumulative_damage: int` (0..∞)
- `_uses_in_stage: int` (0..∞)
- `_is_broken: bool` (true au dernier stade)

### Interactions with Other Systems

| Système | Direction | Interface |
|---|---|---|
| S05 — Catalogue objets | S04 ← S05 | Lecture de `catalogue_entry` (stades, seuils, assets) |
| S02 — Saisie/Lancer | S04 ← S02 | `register_use()` sur l'objet tenu après frappe/lancer ; `receive_damage()` sur la cible “cassable” |
| S06 — Dégâts | S04 ← S06 | S04 reçoit la valeur `final_damage` déjà calculée (via S02) |
| S13 — HUD | S04 → S13 | (V1.0) signal `destruction_stage_changed` pour feedback visuel |

### Formulas

**F1 — Dégâts cumulés**

```
cumulative_damage_next = cumulative_damage + final_damage
```

**F2 — Condition de transition (stade courant s)**

```
transition_if_damage = (damage_threshold[s+1] != -1) and (cumulative_damage >= damage_threshold[s+1])
transition_if_uses   = (uses_until_break[s] != -1) and (uses_in_stage >= uses_until_break[s])
transition = transition_if_damage or transition_if_uses
```

### Edge Cases

**EC-01 — Objet détruit pendant qu'il est porté**
Le tracker émet `broken(object)` lorsque le dernier stade est atteint. S02 écoute ce signal pour libérer l'objet et émettre `carry_interrupted(object)` (voir ADR-0001).

**EC-02 — Transition en vol**
Si un objet lancé casse pendant le vol (seuil atteint après un impact intermédiaire), le swap visuel est immédiat. Les débris sont générés à la **position de l'impact** qui a déclenché la casse (pas au point de départ du lancer).

**EC-03 — Double application**
Si un même événement déclenche à la fois `register_use()` et `receive_damage()` sur le même objet, c'est autorisé. Les deux voies sont cumulatives et la transition se déclenche si une condition est atteinte.

**EC-04 — Débris sans chemin**
Si `debris_scene_path` est vide/null, S04 ne crash pas : il désactive l'objet (visuel + collision) et log un `push_error()` en debug.

## Dependencies

### Upstream (S04 dépend de)

| Système | Ce que S04 consomme |
|---|---|
| S05 — Catalogue objets | StageData (seuils + uses + assets) |
| S02 — Saisie/Lancer | Appels `register_use()` et `receive_damage()` |

### Downstream (dépend de S04)

| Système | Ce que S04 fournit |
|---|---|
| S02 — Saisie/Lancer | Information “objet cassé/non-saisissable” via `can_damage_when_broken` + signal `broken` |
| S13 — HUD | (V1.0) événements de changement de stade |

## Tuning Knobs

Les knobs de S04 sont **dans S05** (données) :

- `damage_threshold[s]` : durée de vie en HP cumulés
- `uses_until_break[s]` : durée de vie en nombre d'usages
- `stage_mesh_paths` / `visual_scene` : lisibilité par stade
- `debris_scene_path` : densité visuelle des débris (via la scène)

S04 n'introduit pas de knobs runtime en MVP.

## Visual/Audio Requirements

- **Swap visuel instantané** au changement de stade (pas de tween).
- **Débris persistants** jusqu'au retry (S12). Aucun cleanup automatique.
- **Pas de VFX** MVP (VFX = S15 V1.0). En MVP, la lisibilité vient du mesh et des débris.

## UI Requirements

Pas d'UI dédiée. Le HUD (S13) peut, en V1.0, afficher un mini feedback d'état d'objet (optionnel).

## Acceptance Criteria

**AC-01** — Un objet avec `uses_until_break[0]=2` passe au stade 1 exactement au 2e usage.

**AC-02** — Un objet avec `damage_threshold[1]=12` passe au stade 1 quand `_cumulative_damage` atteint 12 (ni avant ni après).

**AC-03** — À la transition vers le dernier stade, la scène de débris est instanciée à la position d'impact, et l'objet original ne reste pas saisissable si `can_damage_when_broken=false`.

**AC-04** — Un objet cassé pendant qu'il est porté déclenche `carry_interrupted` (via l'intégration S02/S04) sans crash.

## Open Questions

| # | Question | Priorité | Résolution |
|---|---|---|---|
| OQ-01 | Collision world→objet : qui appelle `receive_damage()` quand un objet lancé touche un mur/sol ? (S02 via signal de collision, ou un script sur l'objet) | Haute | À décider au prototype S02/S04 (architecture collision) |
| OQ-02 | Représentation par stade : swap de mesh vs swap de scène (PackedScene) ? | Moyenne | À fixer en alignant S05 ↔ ADR-0004 avant implémentation |
| OQ-03 | Faut-il un “micro-feedback” MVP (son/flash) au moment où un objet casse ? | Basse | V1.0 (S14/S15) par défaut |
