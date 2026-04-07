# Catalogue d'objets

> **Statut** : Complet — en attente de revue
> **Auteur** : Game Designer + Systems Designer
> **Dernière mise à jour** : 2026-04-07
> **Implémente le pilier** : Pilier 1 — Tout est une arme

## Résumé

Le Catalogue d'objets est la source de vérité pour toutes les propriétés des objets interactifs de la pièce. Il définit, pour chaque objet : masse physique, paramètres Jolt, affordance d'interaction, et chaîne de destruction en plusieurs stades. Sans lui, S02 (Saisie/lancer) ne sait pas ce qu'il saisit, et S04 (Dégradation) ne sait pas comment un objet se brise.

> **Quick reference** — Layer: `Foundation` · Priority: `MVP` · Key deps: `None`

## Overview

Le Catalogue d'objets est un référentiel de données statiques : il énumère les 8 à 15 objets interactifs de la pièce et leur associe un ensemble complet de propriétés. Il n'exécute aucune logique à l'exécution — c'est une source de vérité lue par les autres systèmes.

Chaque entrée du catalogue définit quatre axes :

1. **Physique** — masse (kg), amortissement linéaire et angulaire, restitution Jolt
2. **Interaction** — portée de saisie, dégâts de mêlée de base, dégâts de lancer de base
3. **Destruction** — nombre de stades, seuils de déclenchement, mesh actif par stade
4. **Identité** — nom, catégorie visuelle (meuble / récipient / objet de bureau / autre)

S02 (Saisie/lancer) consulte le catalogue pour connaître les paramètres d'un objet au moment de sa saisie. S04 (Dégradation d'environnement) consulte le catalogue pour connaître la séquence de destruction d'un objet lorsqu'il subit des dégâts. Aucun autre système n'a besoin d'encoder ces valeurs.

## Player Fantasy

Le catalogue d'objets est invisible. Le joueur ne verra jamais une fiche technique, ne comparera jamais deux colonnes de chiffres. Pourtant, c'est le catalogue qui donne à chaque objet de la pièce son caractère propre — et c'est ce caractère que le joueur découvre, exploite, et dont il se souvient.

La player fantasy servie par ce système est indirecte mais fondamentale : **chaque objet raconte quelque chose par son comportement**. La chaise est loyale — elle encaisse plusieurs coups avant de céder. La bouteille est explosive — un seul impact, spectaculaire et définitif. Le livre est discret — il vole à plat, précis, presque silencieux. Ces personnalités émergent directement des valeurs du catalogue : masse, restitution, seuils de destruction. Sans catalogue rigoureux, les objets seraient génériques — et une pièce remplie d'objets génériques ne serait pas un arsenal, juste un décor.

Le joueur ressent le catalogue à travers deux piliers simultanément :

- **Pilier 1 (Tout est une arme)** : Les propriétés physiques distinctes de chaque objet rendent crédible la promesse que tout est utilisable. Si une lampe et un vase se comportaient de la même façon, le joueur sentirait que le système triche — que "tout est une arme" est un slogan, pas une réalité.
- **Pilier 3 (La pièce raconte)** : Les stades de destruction définis dans le catalogue sont les chapitres de cette narration. Quand la chaise passe de "intacte" à "cassée mais utilisable" puis à "débris", c'est l'histoire de la partie qui s'écrit dans l'environnement.

**Moments joueur que ce système rend possibles :**

- Le joueur découvre que la chaise ne casse pas au premier lancer — elle revient abîmée mais fonctionnelle. Il développe un réflexe : garder la chaise pour les situations difficiles, gaspiller les bouteilles sur les ennemis isolés. Ce choix tactique naît entièrement des données du catalogue.
- La pièce, en fin de partie, est méconnaissable. Les débris au sol ne sont pas aléatoires : chaque fragment est le reste d'un objet spécifique, brisé à un stade spécifique. Le joueur peut "lire" la bataille dans les restes. Cette lisibilité est le produit direct de la chaîne de destruction définie dans le catalogue.
- Un joueur qui recommence repère immédiatement les objets qu'il connaît. "La lampe est là — je sais qu'elle fait un bon arc." Cette reconnaissance est la preuve que les propriétés du catalogue ont été internalisées.

## Detailed Design

### Core Rules

Le catalogue est un ensemble de ressources GDScript statiques. Chaque objet interactif de la scène porte une référence directe à son entrée de catalogue via un `@export`. Aucune lookup globale n'existe à l'exécution.

**Règle 1 — Structure de données : `ObjectCatalogueEntry` (Resource)**

| Champ | Type | Unité | Consommateur |
|---|---|---|---|
| `id` | `StringName` | — | S02, S04 |
| `display_name` | `String` | — | S13 (HUD) |
| `category` | `enum Category` | — | S04, S13 |
| `mass_kg` | `float` | kg | S02 (Jolt) |
| `linear_damp` | `float` | — | S02 |
| `angular_damp` | `float` | — | S02 |
| `restitution` | `float` | 0.0–1.0 | S02 |
| `grab_range_m` | `float` | m | S02 |
| `melee_damage_base` | `int` | HP | S02 via S06 |
| `throw_damage_base` | `int` | HP | S02 via S06 |
| `throw_impulse_scale` | `float` | mult | S02 |
| `destruction_stages` | `Array[StageData]` | — | S04 |
| `stage_mesh_paths` | `Array[String]` | — | S04 |
| `debris_scene_path` | `String` | — | S04 |
| `can_damage_when_broken` | `bool` | — | S02, S04 |
| `sound_impact_key` | `StringName` | — | S14 (V1.0) |

**Règle 2 — Structure imbriquée : `StageData`**

Chaque stade de destruction est défini par :

| Champ | Type | Description |
|---|---|---|
| `damage_threshold` | `int` | Dégâts cumulés minimum pour déclencher ce stade |
| `uses_until_break` | `int` | Nombre d'utilisations (frappes + lancers) pour déclencher ce stade ; `-1` = illimité |
| `melee_dmg_mult` | `float` | Multiplicateur de dégâts mêlée à ce stade |
| `throw_dmg_mult` | `float` | Multiplicateur de dégâts lancer à ce stade |
| `is_final_stage` | `bool` | Vrai si c'est le dernier stade (débris ou disparition) |

**Règle 3 — Déclenchement de stade (logique OU)**

Un objet avance au stade suivant si **l'une ou l'autre** condition est vraie :
- `cumulative_damage ≥ stage_data[stade_suivant].damage_threshold`
- `uses_in_stage ≥ stage_data[stade_courant].uses_until_break`

Un lancer ET une frappe de mêlée comptent tous deux comme une utilisation pour `uses_until_break`.

**Règle 4 — Persistance des débris**

Quand un objet atteint son `is_final_stage`, la scène de débris définie dans `debris_scene_path` est instanciée à la position courante. Ces débris sont **permanents pour toute la durée de la partie** — ils ne disparaissent pas entre les vagues.

**Règle 5 — Interface sur chaque nœud d'objet interactif**

```gdscript
# Sur chaque RigidBody3D (objet interactif de la scène)
@export var catalogue_entry: ObjectCatalogueEntry  # assigné dans l'éditeur Godot

func get_grab_params() -> ObjectCatalogueEntry:
    return catalogue_entry
```

S02 et S04 lisent tous deux `catalogue_entry` depuis ce même nœud. Pas de duplication de données.

---

### States and Transitions

Chaque objet interactif possède un état de destruction courant géré par un composant `DestructionTracker` (propriété de S04). Le catalogue définit les seuils ; le tracker maintient l'état à l'exécution.

```
Stade 0 (intact)
    │
    ├─ [cumulative_damage ≥ threshold_1] OU [uses_in_stage ≥ uses_until_break_0]
    ▼
Stade 1 (endommagé)
    │
    ├─ [cumulative_damage ≥ threshold_2] OU [uses_in_stage ≥ uses_until_break_1]
    ▼
Stade N (final) ──► Spawn débris + désactiver mesh ──► État terminal (permanent)
```

- Nombre de stades : minimum 1, maximum 3 (recommandé)
- Transitions : unidirectionnelles — un objet ne revient jamais à un stade précédent
- Un objet au stade final ne peut plus recevoir de dégâts ni être saisi (sauf si `can_damage_when_broken = true`, auquel cas les débris restent ramassables)

---

### Interactions with Other Systems

**S02 — Saisie et lancer (consommateur lecture)**

S02 lit `catalogue_entry` au moment de la saisie pour obtenir :
- Paramètres Jolt (`mass_kg`, `linear_damp`, `angular_damp`, `restitution`)
- Portée de saisie (`grab_range_m`)
- Dégâts de base pour calcul via S06 (`melee_damage_base`, `throw_damage_base`, `throw_impulse_scale`)

S02 appelle `register_use()` sur le `DestructionTracker` de l'objet après chaque frappe ou lancer.

**S04 — Dégradation d'environnement (consommateur lecture + état)**

S04 lit `catalogue_entry` une seule fois à `_ready()` via son `DestructionTracker`. À chaque impact reçu (signal de S06), S04 appelle `receive_damage(amount)` sur le tracker. Le tracker compare `_cumulative_damage` aux seuils du catalogue et déclenche la transition de mesh si nécessaire.

```gdscript
# DestructionTracker — propriété de S04
var _entry: ObjectCatalogueEntry
var _current_stage: int = 0
var _cumulative_damage: int = 0
var _uses_in_stage: int = 0

func _ready() -> void:
    _entry = get_parent().catalogue_entry  # lecture unique à l'init

func receive_damage(amount: int) -> void:
    _cumulative_damage += amount
    _check_stage_transition()

func register_use() -> void:
    _uses_in_stage += 1
    _check_stage_transition()
```

**S06 — Système de dégâts (intermédiaire)**

S06 reçoit `melee_damage_base` ou `throw_damage_base` depuis S02 (qui les lit dans le catalogue) et applique ses propres modificateurs. Le catalogue fournit la valeur de base ; S06 produit la valeur finale transmise à S04/S08.

---

### Catalogue MVP (7 objets)

| Objet | Masse | Stades | Caractère |
|---|---|---|---|
| `chaise` | 6 kg | 3 | Loyale — encaisse plusieurs coups, reste utilisable brisée |
| `bouteille` | 0.8 kg | 2 | Explosive — un seul impact, spectaculaire et définitif |
| `lampe_bureau` | 1.5 kg | 3 | Versatile — bon arc de lancer, tient dans la durée |
| `livre` | 0.4 kg | 2 | Discret — vole à plat, précis, presque silencieux |
| `moniteur` | 5 kg | 2 | Massif — dégâts élevés, portée de saisie plus faible |
| `ordinateur_portable` | 2 kg | 2 | Fiable — équilibré lancer/mêlée |
| `mug_cafe` | 0.3 kg | 1 | Jetable — usage unique, sacrifice tactique |

### Catalogue V1.0 (7 objets supplémentaires)

`classeur`, `vase`, `lampadaire`, `corbeille_papier`, `agrafeuse`, `tabouret`, `thermos`

## Formulas

### F1 — Dégâts mêlée transmis à S06

```
melee_input_to_s06 = melee_damage_base × melee_dmg_mult[stade_courant]
```

| Symbole | Type | Plage | Description |
|---|---|---|---|
| `melee_damage_base` | `int` | 1–15 | Dégâts mêlée de base, définis dans `ObjectCatalogueEntry` |
| `melee_dmg_mult[s]` | `float` | 0.5–1.8 | Multiplicateur du stade courant `s`, défini dans `StageData` |
| `melee_input_to_s06` | `float` | 0.5–27.0 | Valeur transmise à S06 comme `base_damage` — S06 y applique ses propres modificateurs avant application aux HP |

Plafond absolu : aucun objet ne dépasse 12 HP par impact en conditions normales (seuil = HP max ennemi basique). S05 ne clamp pas — S06 est responsable du clamp final.

**Exemple — chaise au stade 1 (endommagée) :**
```
melee_damage_base    = 7
melee_dmg_mult[1]    = 0.9
melee_input_to_s06   = 7 × 0.9 = 6.3  →  S06 reçoit 6.3
```

---

### F2 — Dégâts lancer transmis à S06

```
throw_input_to_s06 = throw_damage_base × throw_dmg_mult[stade_courant]
```

| Symbole | Type | Plage | Description |
|---|---|---|---|
| `throw_damage_base` | `int` | 2–15 | Dégâts de lancer de base, définis dans `ObjectCatalogueEntry` |
| `throw_dmg_mult[s]` | `float` | 0.3–2.0 | Multiplicateur du stade courant. Peut dépasser 1.0 (objet plus dangereux brisé, ex : bouteille). Exception bouteille stade final : max 2.0 |
| `throw_input_to_s06` | `float` | 0.6–30.0 | Valeur transmise à S06 comme `base_damage` |

Note : `throw_impulse_scale` est un facteur de vitesse Jolt géré par S02. Il n'intervient pas dans le calcul des dégâts.

**Exemple — bouteille lancée au stade 1 (brisée en vol) :**
```
throw_damage_base    = 8
throw_dmg_mult[1]    = 1.5    ← bouteille explose à l'impact
throw_input_to_s06   = 8 × 1.5 = 12.0  →  near one-shot sur ennemi basique (12 HP)
```

---

### F3 — Transition de stade

```
should_advance_stage = (cumulative_damage ≥ damage_threshold[stade_suivant])
                    OR (uses_in_stage ≥ uses_until_break[stade_courant])
```

| Symbole | Type | Plage | Description |
|---|---|---|---|
| `cumulative_damage` | `int` | 0–∞ | Dégâts cumulés reçus depuis la création — jamais réinitialisé (Pilier 3) |
| `damage_threshold[s+1]` | `int` | 1–100 | Seuil de dégâts cumulés pour passer au stade `s+1` |
| `uses_in_stage` | `int` | 0–∞ | Utilisations (frappes + lancers) dans le stade courant — remis à 0 à chaque transition |
| `uses_until_break[s]` | `int` | -1–20 | Utilisations max dans le stade `s` avant transition. `-1` = cette condition désactivée |
| `should_advance_stage` | `bool` | — | Si `true` : S04 déclenche la transition de mesh |

**Sémantique de `-1` :** désactive la condition "usure". L'objet ne transite que par accumulation de dégâts. Exemple : le livre (`uses_until_break = -1` à tous les stades) ne se déchire que sous les impacts, pas à force d'être lancé.

**Exemple complet — chaise (3 stades) :**

Configuration :
```
Stade 0 (intact)     : damage_threshold =  0   uses_until_break = 4
Stade 1 (endommagée) : damage_threshold = 12   uses_until_break = 3
Stade 2 (débris)     : damage_threshold = 25   uses_until_break = -1  is_final_stage = true
```

Scénario A — transition par usure :
```
Utilisation 1 : frappe  → uses_in_stage = 1
Utilisation 2 : frappe  → uses_in_stage = 2
Utilisation 3 : lancer  → uses_in_stage = 3
Utilisation 4 : frappe  → uses_in_stage = 4
    → 4 ≥ uses_until_break[0]=4  →  TRANSITION stade 0→1
    → uses_in_stage remis à 0
```

Scénario B — transition par dégâts (chaise tenue comme bouclier) :
```
Coup ennemi : cumulative_damage += 6  →  6
Coup ennemi : cumulative_damage += 6  →  12
    → 12 ≥ damage_threshold[1]=12  →  TRANSITION stade 0→1
    (uses_in_stage = 0 — la condition OU suffit)
```

---

### F4 — Valeurs de référence MVP

**Hypothèse de calibrage :** ennemis basiques ~12 HP. Un objet "efficace" fait 2–3 frappes pour éliminer.

**Dégâts de base et vitesse de lancer :**

| Objet | `melee_damage_base` | `throw_damage_base` | `throw_impulse_scale` | Caractère |
|---|---|---|---|---|
| `mug_cafe` | 1 | 3 | 1.8 | Jetable — sacrifice tactique pur |
| `livre` | 1 | 4 | 1.6 | Discret — vole vite et à plat |
| `bouteille` | 2 | 8 | 1.3 | Explosive — lancer dominant (ratio 1:4) |
| `lampe_bureau` | 4 | 6 | 1.0 | Versatile — référence neutre |
| `ordinateur_portable` | 4 | 6 | 0.85 | Fiable — équilibré |
| `moniteur` | 6 | 9 | 0.55 | Massif — lent mais dévastateur |
| `chaise` | 7 | 10 | 0.45 | Loyale — meilleure arme mêlée et lancer |

**Règles de plafond :** `throw_impulse_scale` min = 0.4 (objet doit atteindre sa cible). Multiplicateurs de stade max = 1.8× (exception bouteille : 2.0× throw stade final).

**Multiplicateurs et seuils par stade :**

| Objet | Stade | `melee_dmg_mult` | `throw_dmg_mult` | `damage_threshold` | `uses_until_break` | `is_final` |
|---|---|---|---|---|---|---|
| `chaise` | 0 | 1.0 | 1.0 | 0 | 4 | false |
| `chaise` | 1 | 0.9 | 1.0 | 12 | 3 | false |
| `chaise` | 2 | 0.7 | 0.8 | 25 | -1 | **true** |
| `bouteille` | 0 | 1.0 | 1.0 | 0 | 2 | false |
| `bouteille` | 1 | 0.8 | 1.5 | 5 | -1 | **true** |
| `lampe_bureau` | 0 | 1.0 | 1.0 | 0 | 4 | false |
| `lampe_bureau` | 1 | 1.1 | 0.9 | 10 | 3 | false |
| `lampe_bureau` | 2 | 0.6 | 0.7 | 22 | -1 | **true** |
| `livre` | 0 | 1.0 | 1.0 | 0 | -1 | false |
| `livre` | 1 | 0.8 | 0.7 | 8 | -1 | **true** |
| `moniteur` | 0 | 1.0 | 1.0 | 0 | 2 | false |
| `moniteur` | 1 | 1.2 | 0.6 | 15 | -1 | **true** |
| `ordinateur_portable` | 0 | 1.0 | 1.0 | 0 | 3 | false |
| `ordinateur_portable` | 1 | 0.9 | 0.8 | 12 | -1 | **true** |
| `mug_cafe` | 0 | 1.0 | 1.0 | 0 | 1 | **true** |

**Notes de calibrage :**
- **Chaise** : `uses_until_break = 4` au stade 0 — 4 actions avant la première dégradation. `damage_threshold = 25` pour le stade final est difficile à atteindre offensivement, réservé aux situations où la chaise absorbe des coups ennemis.
- **Bouteille** : asymétrie mêlée/lancer intentionnelle (1:4). `throw_dmg_mult = 1.5` au stade final → 8×1.5 = 12 à S06, near one-shot. La promesse "explosive" est tenue.
- **Livre** : `uses_until_break = -1` à tous les stades — ne se dégrade que par les impacts reçus, jamais par le lancer. `throw_impulse_scale = 1.6` → trajectoire rapide et plate.
- **Mug** : `is_final_stage = true` dès le stade 0, `uses_until_break = 1` — une seule action (frappe ou lancer) le détruit.

> Ces valeurs sont des baselines de tuning. Elles seront recalibrées après implémentation de S08 (santé ennemie) et premiers playtests.

## Edge Cases

### EC-01 — Objet qui atteint le stade final en plein vol

**Situation** : Un objet est lancé par S02 et atteint son dernier stade de destruction pendant sa trajectoire (cumul de dégâts ou nombre d'usages atteint avant l'impact).

**Comportement** : Le mesh est mis à jour immédiatement (S04 swaps le mesh dès la transition de stade, même en vol). Les débris sont générés à la position d'impact — pas à la position de la transition — pour cohérence physique et pour éviter des débris flottants en milieu de vol.

---

### EC-02 — Lecture simultanée par S02 et S04

**Situation** : S02 lit `catalogue_entry` pour une saisie au même frame que S04 lit `catalogue_entry` pour calculer une transition de stade.

**Comportement** : Non-problème. GDScript est mono-thread. `ObjectCatalogueEntry` est un `Resource` immutable — aucune de ces lectures ne modifie les données. Il n'y a pas de race condition possible.

---

### EC-03 — Objet au stade final avec `can_damage_when_broken = false`

**Situation** : Un objet est à son stade final ET `can_damage_when_broken` vaut `false`. Le joueur tente de le saisir.

**Comportement** : S02 interroge `DestructionTracker.get_current_stage()` avant d'autoriser la saisie. Si l'objet est au stade final ET que `can_damage_when_broken` est `false`, S02 refuse la saisie. L'objet ne peut plus être utilisé en arme. Il reste dans la scène comme débris visuel (Pilier 3 — La pièce raconte).

---

### EC-04 — Les deux conditions de transition vraies au même frame

**Situation** : `cumulative_damage` atteint `damage_threshold` ET `uses_in_stage` atteint `uses_until_break` au même frame.

**Comportement** : `_check_stage_transition()` déclenche la transition une seule fois. La vérification `is_final_stage` sur le `StageData` courant est évaluée avant toute modification — si le stade courant est déjà final, la fonction retourne immédiatement (EC-08). Pas de double transition, pas de saut de stade.

---

### EC-05 — Debris spawné à une position occupée

**Situation** : Le debris_scene_path génère un RigidBody3D à une position déjà occupée par un autre objet physique (un autre debris, un ennemi, le sol).

**Comportement** : Jolt Physics gère la dépénétration nativement. Les corps rigides en chevauchement sont éjectés automatiquement dans la frame suivante. Aucune logique S05 ou S04 nécessaire.

---

### EC-06 — Objet à un seul stade, deux actions simultanées

**Situation** : Un objet avec un seul `StageData` (`is_final_stage = true` dès le stade 0) reçoit à la fois un appel `receive_damage()` et `register_use()` dans le même frame.

**Comportement** : S02 garantit une seule action par objet par frame (lancer OU frappe, pas les deux). En pratique, ce cas ne peut pas se produire avec le contrat de S02. La règle est documentée ici comme contrainte de S02, pas de S05.

---

### EC-07 — `catalogue_entry` non assigné (`null`)

**Situation** : Un RigidBody3D interactif est placé dans la scène sans que son `catalogue_entry` soit assigné dans l'éditeur.

**Comportement** : Au moment de la saisie, S02 vérifie que `catalogue_entry != null`. Si null : `push_error("catalogue_entry non assigné sur [node_name]")` dans la console, saisie annulée. Pas de crash. Le nœud est ignoré comme s'il était non-interactif.

---

### EC-08 — Stade final avec les deux seuils à `-1`

**Situation** : Un `StageData` avec `is_final_stage = true` a également `damage_threshold = -1` et `uses_until_break = -1` (configuration défensive — stade final indestructible).

**Comportement** : `_check_stage_transition()` vérifie `is_final_stage` en premier. Si `true`, la fonction retourne immédiatement sans évaluer les seuils. L'objet reste à ce stade indéfiniment. Configuration valide pour les objets qui doivent rester dans la scène jusqu'à la fin de la partie (Pilier 3).

## Dependencies

### Dépendances amont (S05 dépend de)

Aucune. S05 est un système Foundation — données statiques pures, sans dépendance d'exécution.

### Dépendances aval (systèmes qui dépendent de S05)

| Système | Ce qu'il lit | Interface |
|---------|-------------|-----------|
| **S02 — Saisie et lancer** | `mass_kg`, `grab_range_m`, `melee_damage_base`, `throw_damage_base`, `throw_impulse_scale`, `can_damage_when_broken` | `@export var catalogue_entry: ObjectCatalogueEntry` sur chaque RigidBody3D interactif |
| **S04 — Dégradation d'environnement** | `destruction_stages` (Array[StageData]), `stage_mesh_paths`, `debris_scene_path`, `can_damage_when_broken` | Même export — lu par `DestructionTracker._ready()` une seule fois à l'init |
| **S13 — HUD** | `display_name` | Même export — lu lors de la saisie pour afficher le nom de l'objet tenu |
| **S14 — Retour audio** (V1.0) | `sound_impact_key` | Même export — lu lors de l'impact pour déclencher le son approprié |

### Contrat d'interface

Chaque nœud `RigidBody3D` interactif de la scène expose :

```gdscript
@export var catalogue_entry: ObjectCatalogueEntry
```

Cette propriété est assignée dans l'éditeur Godot. S05 ne fournit aucune API de lookup global — chaque système lit directement `catalogue_entry` sur le nœud concerné. Si `catalogue_entry` est `null`, S02 refuse la saisie et enregistre une erreur (voir EC-07).

### Note sur la circularité

S05 est référencé par S02 et S04, qui sont eux-mêmes dans la liste des dépendances de S02. Il n'y a pas de circularité : S05 ne lit jamais S02 ni S04 — le flux de données est unidirectionnel (S05 → S02, S05 → S04).

## Tuning Knobs

Tous les champs `@export` de `ObjectCatalogueEntry` et `StageData` sont techniquement ajustables dans l'éditeur Godot. Les knobs ci-dessous sont ceux dont la variation a un impact gameplay observable et qui nécessitent une plage de sécurité documentée.

### Knobs de niveau objet (ObjectCatalogueEntry)

| Knob | Plage sûre | Effet d'une augmentation | Risque si hors plage |
|------|-----------|--------------------------|----------------------|
| `mass_kg` | 0.2 – 10.0 kg | L'objet est plus difficile à propulser, plus impactant visuellement | < 0.2 : comportement Jolt erratique (objet trop léger) ; > 10 : trajectoire quasi-nulle, peu satisfaisant |
| `linear_damp` | 0.0 – 3.0 | L'objet ralentit plus vite en vol (arc plus court) | > 3 : objet tombe à la verticale, lancer inutilisable |
| `angular_damp` | 0.0 – 5.0 | L'objet tourne moins en vol | > 5 : objet figé, perd son réalisme physique |
| `restitution` | 0.0 – 0.8 | L'objet rebondit plus après impact | > 0.8 : rebonds incontrôlables, débris envahissants |
| `grab_range_m` | 0.5 – 3.0 m | La saisie est possible depuis plus loin | > 3.0 : saisie à distance magique, casse l'immersion ; < 0.5 : trop difficile à saisir |
| `melee_damage_base` | 1 – 15 HP | Un coup de mêlée fait plus de dégâts | > 15 : un seul objet domine tout le catalogue, réduit la diversité tactique |
| `throw_damage_base` | 2 – 15 HP | Un lancer fait plus de dégâts | > 15 : même risque ; le lancer doit rester risqué (perte de l'objet) |
| `throw_impulse_scale` | 0.3 – 2.5 | L'objet est propulsé plus fort | > 2.5 : vitesse Jolt instable ; < 0.3 : lancer visuellement décevant |

### Knobs de niveau stade (StageData)

| Knob | Plage sûre | Effet d'une augmentation | Risque si hors plage |
|------|-----------|--------------------------|----------------------|
| `damage_threshold` | 0 – 50 HP | Le stade suivant est atteint plus tard (objet plus résistant) | > 50 : objet quasi-indestructible, perd son identité de ressource dépensable |
| `uses_until_break` | 1 – 10 (ou -1) | Le stade suivant est atteint après plus d'usages | > 10 : objet ne se brise jamais en pratique ; -1 = illimité (valeur sentinel, usage intentionnel) |
| `melee_dmg_mult` | 0.3 – 2.0 | Les dégâts de mêlée à ce stade sont multipliés | > 2.0 : dépasse le plafond de cohérence du catalogue (couplé à melee_damage_base) |
| `throw_dmg_mult` | 0.3 – 2.0 | Les dégâts de lancer à ce stade sont multipliés | > 2.0 : même risque |

### Knobs globaux de calibration

| Knob | Valeur de référence | Rôle |
|------|--------------------|----|
| HP ennemi basique | ~12 HP | Étalon de calibration — "efficace" = 2–3 frappes ou 1 lancer fort |
| Nombre de stades par objet MVP | 1–3 | 1 = consommable rapide ; 3 = outil durable (arc narratif) |
| Nombre d'objets dans la pièce (MVP) | 7 | Plancher de diversité tactique — en dessous, les choix deviennent triviaux |

### Priorité de tuning recommandée

1. `melee_damage_base` et `throw_damage_base` — calibrage direct sur l'étalon HP ennemi
2. `damage_threshold` et `uses_until_break` — durée de vie des objets, rythme de dégradation
3. `throw_impulse_scale` — qualité du ressenti Jolt (à ajuster par playtest)
4. `mass_kg`, `restitution` — comportement physique (à ajuster après proto physique S02)

## Visual/Audio Requirements

S05 ne produit aucun rendu lui-même. Il fournit les chemins et clés d'assets que S04 et S14 utilisent pour les effets visuels et sonores. Les exigences ci-dessous s'appliquent aux assets référencés par le catalogue.

### Assets visuels (par objet)

Chaque objet du catalogue requiert un asset visuel par stade de destruction défini dans `destruction_stages`.

**Convention de nommage des meshes :**

```
assets/art/objects/[id_objet]/[id_objet]_stage_[n].mesh
```

Exemples :
- `assets/art/objects/chaise/chaise_stage_0.mesh` (intact)
- `assets/art/objects/chaise/chaise_stage_1.mesh` (endommagé)
- `assets/art/objects/chaise/chaise_stage_2.mesh` (brisé)

Ces chemins sont listés dans `stage_mesh_paths: Array[String]` — l'index du tableau correspond au numéro de stade.

**Convention de nommage des scènes de débris :**

```
assets/art/objects/[id_objet]/[id_objet]_debris.tscn
```

Le chemin est stocké dans `debris_scene_path: String`. La scène de débris est une scène Godot autonome contenant les RigidBody3D de fragments. Elle est instanciée par S04 à la transition vers le stade final.

**Exigences minimales MVP (art bible §2 — lisibilité) :**
- Chaque mesh de stade doit avoir une silhouette identifiable à 5 m de distance caméra
- Le stade final doit être visuellement distinct du stade 0 (minimum : fragments visibles ou géométrie altérée)
- Les débris doivent rester reconnaissables comme fragments de l'objet parent (pas de géométrie générique)

### Assets audio (V1.0)

`sound_impact_key: StringName` est une clé symbolique (pas un chemin direct). S14 (Retour audio, V1.0) résout cette clé vers un `AudioStream` dans son propre système de mapping.

**Convention de nommage des clés :**

```
impact_[id_objet]_[stade]   # Exemple : impact_chaise_0, impact_bouteille_1
impact_[matière]             # Fallback générique : impact_bois, impact_verre, impact_metal
```

Pour le MVP : `sound_impact_key` est présent dans la structure mais non utilisé — S14 est hors scope MVP. La valeur peut rester vide (`&""`) sans conséquence.

### Catalogue MVP — chemins attendus

| Objet | Stades | Mesh paths | Debris scene |
|-------|--------|-----------|--------------|
| chaise | 3 | `chaise_stage_0/1/2.mesh` | `chaise_debris.tscn` |
| bouteille | 2 | `bouteille_stage_0/1.mesh` | `bouteille_debris.tscn` |
| lampe_bureau | 3 | `lampe_bureau_stage_0/1/2.mesh` | `lampe_bureau_debris.tscn` |
| livre | 2 | `livre_stage_0/1.mesh` | `livre_debris.tscn` |
| moniteur | 2 | `moniteur_stage_0/1.mesh` | `moniteur_debris.tscn` |
| ordinateur_portable | 2 | `ordinateur_portable_stage_0/1.mesh` | `ordinateur_portable_debris.tscn` |
| mug_cafe | 1 | `mug_cafe_stage_0.mesh` | `mug_cafe_debris.tscn` |

## Acceptance Criteria

Tous les critères ci-dessous doivent être vérifiables pass/fail par un QA tester ou un test automatisé GUT. S05 étant un système de données, les tests portent sur l'intégrité des données et sur le comportement correct des systèmes consommateurs lorsqu'ils lisent ces données.

### AC-01 — Intégrité de la structure de données

**Test** : Instancier un `ObjectCatalogueEntry` pour chaque objet MVP dans l'éditeur Godot. Vérifier que tous les champs obligatoires sont renseignés (non-null, non-zéro pour les valeurs qui doivent être > 0).

**Pass** : Les 7 entrées MVP sont configurées sans erreur dans l'éditeur. Aucun `push_error` au démarrage de la scène.

**Fail** : Un champ obligatoire est null ou zéro, ou un `push_error` apparaît en console au démarrage.

---

### AC-02 — Lecture par S02 (saisie)

**Test** : Placer la chaise dans la scène avec son `catalogue_entry` assigné. Saisir la chaise avec le joueur. Vérifier que les paramètres lus correspondent aux valeurs définies dans l'entrée catalogue (`grab_range_m`, `melee_damage_base`, `throw_damage_base`).

**Pass** : S02 lit les valeurs correctes. L'objet est saisissable dans la portée définie. Les dégâts infligés correspondent à F1/F2 × mult stade 0.

**Fail** : S02 lit des valeurs par défaut (0 ou null) au lieu des valeurs de l'entrée, ou l'objet n'est pas saisissable malgré un `catalogue_entry` valide.

---

### AC-03 — Lecture par S04 (destruction, transition de stade)

**Test** : Infliger à la chaise une quantité de dégâts cumulés égale à `damage_threshold` du stade 1 (valeur définie : 12 HP). Vérifier que le mesh passe à `chaise_stage_1.mesh`.

**Pass** : À 12 HP cumulés, le mesh est remplacé. Aucun stade n'est sauté.

**Fail** : Le mesh ne change pas, change trop tôt, ou saute un stade.

---

### AC-04 — Transition par nombre d'usages

**Test** : Utiliser la bouteille exactement 2 fois (`uses_until_break` stade 0 = 2) sans atteindre le seuil de dégâts. Vérifier que la bouteille passe au stade 1 après le 2e usage.

**Pass** : Transition au stade 1 exactement au 2e usage.

**Fail** : Transition avant 2 usages, après 2 usages, ou pas de transition.

---

### AC-05 — Objet non-saisissable au stade final (`can_damage_when_broken = false`)

**Test** : Amener le mug_café à son stade final (1 usage, `can_damage_when_broken = false`). Tenter de le saisir.

**Pass** : S02 refuse la saisie. Aucun crash. Le mug reste visible comme débris.

**Fail** : S02 saisit l'objet au stade final, ou le jeu crashe à la tentative.

---

### AC-06 — Comportement null-safe

**Test** : Placer un RigidBody3D dans la scène sans assigner son `catalogue_entry`. Tenter de le saisir.

**Pass** : `push_error` apparaît dans la console. La saisie est refusée. Aucun crash.

**Fail** : Crash, exception non gérée, ou saisie réussie d'un objet sans catalogue.

---

### AC-07 — Cohérence des formules de dégâts

**Test** : Pour la chaise au stade 0, vérifier que les dégâts de mêlée transmis à S06 = `melee_damage_base × melee_dmg_mult[0]` = 7 × 1.0 = 7 HP. Pour la bouteille au stade 1 (lancer), vérifier : 8 × 1.5 = 12 HP.

**Pass** : Les valeurs calculées correspondent aux formules F1/F2 pour ces cas.

**Fail** : Écart entre la valeur calculée et la valeur attendue.

---

### AC-08 — Persistance des débris (Pilier 3)

**Test** : Briser la bouteille. Attendre la fin de la vague suivante. Vérifier que les débris sont toujours présents dans la scène.

**Pass** : Les débris persistent jusqu'au retry (reset explicite de S12).

**Fail** : Les débris disparaissent entre vagues ou après un délai.

## Open Questions

### OQ-01 — Validation physique Jolt des impulse scales

**Question** : Les valeurs de `throw_impulse_scale` (0.45 pour la chaise, 1.8 pour le mug) sont-elles satisfaisantes en pratique avec Jolt Physics sur Godot 4.6 ?

**Dépend de** : Prototype S02 (semaine 1 — risque #1 du projet). Les valeurs actuelles sont des estimations raisonnées ; elles doivent être validées par sensation joueur, pas par calcul.

**Action** : Ajuster après le premier prototype physique. Si les objets lourds tombent à la verticale, augmenter l'impulse scale et/ou réduire `linear_damp`.

---

### OQ-02 — Nombre final d'objets (MVP vs V1.0)

**Question** : Le catalogue MVP contient 7 objets. Le game concept mentionne 8–15 objets pour V1.0. Quels 3–8 objets supplémentaires ont la plus grande valeur tactique ?

**Dépend de** : Playtests du prototype. Observer quels comportements manquent dans le catalogue MVP (ex. : besoin d'un objet à dégâts de zone ? d'un objet très rapide mais fragile ?).

**Valeur par défaut** : Le MVP à 7 objets est suffisant pour valider la boucle. Ne pas bloquer la conception de S02 sur ce point.

---

### OQ-03 — `grab_range_m` vs distance caméra TPS

**Question** : La portée de saisie doit-elle être calibrée en mètres monde ou en proportion de l'écran visible ? La caméra TPS (S10, pas encore conçue) peut changer la perception de la distance.

**Dépend de** : S10 (Caméra TPS). Une fois S10 conçu, vérifier que `grab_range_m` = 2.5 m est cohérent avec la distance visible à l'écran.

---

### OQ-04 — Format de `debris_scene_path` : chemin `res://`

**Question** : Les chemins dans `stage_mesh_paths` et `debris_scene_path` sont-ils des chemins `res://` Godot ou des chemins relatifs au dossier assets ?

**Décision provisoire** : Chemins `res://` (standard Godot pour les ressources dans l'éditeur). À confirmer avec le responsable art pipeline lors de la création des premiers assets.
