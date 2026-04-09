# Système de dégâts

> **Statut** : Révisé — en attente de re-review
> **Auteur** : Game Designer + Systems Designer
> **Dernière mise à jour** : 2026-04-08 (révision post-re-review — 5 bloquants corrigés)
> **Implémente le pilier** : Pilier 1 — Tout est une arme · Pilier 2 — Le flow avant le challenge

## Overview

Le Système de dégâts est une formule de calcul pure et stateless. Il reçoit des paramètres en entrée (dégâts de base d'un objet, multiplicateur de stade, type d'action), produit un entier en sortie, et ne maintient aucun état propre. Il n'est pas un nœud, pas un singleton actif — c'est un contrat mathématique que S02 (Saisie/lancer) appelle chaque fois qu'un objet frappe une cible, et dont S07 (Santé joueur) et S08 (Santé ennemie) consomment le résultat.

Son rôle est de centraliser la sémantique des dégâts en un seul endroit : si le calibrage doit changer — un objet qui fait trop mal, des ennemis trop résistants — la formule est le point d'entrée unique. Sans lui, chaque système calculerait ses propres dégâts de manière incohérente.

> **Quick reference** — Layer: `Foundation` · Priority: `MVP` · Key deps: `None`

## Player Fantasy

Le joueur n'a pas besoin de calculer. Il saisit, frappe ou lance, et le résultat est immédiatement lisible dans la réaction de l'ennemi — un objet lourd frappe franchement, un objet léger bronche à peine. Cette cohérence est immédiate et intuitive : l'objet qu'il a choisi se comporte comme il l'imaginait. Le système de dégâts fonctionne en arrière-plan pour que chaque action se sente juste — assez puissante pour maintenir le rythme, jamais si faible qu'elle brise le flow. Le joueur ne pense pas en termes de dommages mais en termes de mouvement : *est-ce que je peux enchaîner avec l'objet suivant ?* Le système de dégâts existe pour que la réponse soit presque toujours "oui".

## Detailed Design

### Core Rules

**Règle 1 — Nature du système**
S06 est une fonction pure stateless. Elle n'est pas un nœud, n'émet pas de signaux, et ne maintient aucune donnée entre deux appels. Deux appels identiques produisent toujours le même résultat.
*→ La structure d'implémentation technique (`class_name DamageCalculator` avec `static func`) fera l'objet d'un ADR.*

**Règle 2 — Paramètres d'entrée**
S06 accepte exactement trois paramètres :
- `damage_base : int` — dégâts de base fournis par l'appelant (lu dans le catalogue par S02, ou défini par l'ennemi via S09)
- `stage_mult : float` — multiplicateur du stade courant, fourni par l'appelant (`1.0` pour les ennemis)
- `damage_type : DamageType` — type d'impact (enum, voir ci-dessous)

S06 ne lit jamais le catalogue d'objets directement. C'est l'appelant qui résout les paramètres avant l'appel.

> **Contrat de type :** Si le catalogue retourne un `float` pour `damage_base` (ex : objet à stade dégradé avec valeur fractionnaire), S02 applique `floori()` avant l'appel pour garantir que `damage_base` est bien un `int`. S06 ne reçoit jamais de `float` pour ce paramètre — la responsabilité de conversion appartient à l'appelant.

**Règle 3 — Types de dégâts (`DamageType`)**
| Valeur | Origine | Utilisé par |
|--------|---------|-------------|
| `MELEE` | Frappe directe avec l'objet tenu | S02 |
| `THROW` | Objet lancé en vol qui percute | S02 |
| `ENEMY_MELEE` | Attaque directe d'un ennemi | S09 |

Le `DamageType` n'influence pas la formule mathématique (mêmes règles pour les trois). Il est transmis en sortie pour permettre au feedback (S14 audio, S15 VFX) de jouer le bon effet selon l'origine.

**Règle 4 — Formule de calcul**
Pour tous les types :
```
final_damage = max(DAMAGE_MIN, floori(damage_base × stage_mult))
```
- `DAMAGE_MIN = 1` — garantit qu'aucune action du joueur ne produit 0 dégâts (toute frappe doit être observable)
- `floori()` retourne un `int` natif en GDScript 4.x (arrondi vers le bas — `roundi()` est proscrit ici car il surchargerait les valeurs `.5+`)
- Pas de `DAMAGE_CAP` pour le MVP ; valeur théorique maximum : `floori(15 × 2.0) = 30` — documenté dans Tuning Knobs

**Règle 5 — Sortie**
S06 retourne un `int` unique : les points de dégâts à soustraire à la cible. Il ne retourne pas de struct, ne déclenche aucun événement. La cible est entièrement responsable de la réception et de l'application.

**Règle 6 — Un appel par contact résolu**
S06 est appelé exactement une fois par contact physique résolu. Si un objet lancé touche plusieurs ennemis, S02 appelle S06 une fois par ennemi touché. S06 ignore le contexte multi-cible.

**Règle 7 — Autorité de multiplication**

S02 transmet `damage_base` et `stage_mult` comme valeurs **brutes**, exactement telles qu'elles sont lues dans le catalogue (S05) ou les données de stade. S02 n'applique aucune pré-multiplication avant l'appel. S06 est le seul système qui exécute `damage_base × stage_mult`. Tout autre appelant (S09) respecte la même règle : pas de pré-multiplication côté appelant. Toute valeur d'entrée déjà multipliée produirait un résultat erroné par double-application.

**Règle 8 — La vitesse physique n'influence pas les dégâts**
La `LinearVelocity` Jolt de l'objet lancé N'EST PAS un paramètre de S06. Un lancer à 2 m/s produit le même `final_damage` qu'un lancer à 20 m/s, à `damage_base` égal. Cette décision est délibérée : le ressenti de puissance est porté par les valeurs `damage_base` distinctes du catalogue (S05) et le retour sensoriel (S14/S15), non par la cinématique de l'objet. Incorporer la vitesse dans la formule introduirait une dépendance sur le moteur physique, rendrait le calibrage imprévisible, et briserait le modèle stateless de S06.
*→ Si cette décision est révisée en V1.0, le changement affecte la signature de S06 — breaking change pour S02 et S09.*

### States and Transitions

S06 est explicitement stateless par décision de conception. Il n'y a aucune variable d'instance, aucun historique d'appels, aucun mode actif/inactif.

L'état est localisé dans les systèmes qui en ont la responsabilité légitime :
- État de destruction de l'objet : `DestructionTracker` (propriété de S04)
- État de santé de la cible : S07 (joueur) ou S08 (ennemi)
- État de la saisie courante : S02

S06 ne doit jamais devenir stateful. Si une future mécanique nécessite un bonus de dégâts temporaire, cet état appartient au système qui gère ce bonus — S06 reçoit simplement un `stage_mult` ajusté en entrée.

### Interactions with Other Systems

**Qui appelle S06 :**
| Appelant | Quand | Paramètres transmis |
|----------|-------|---------------------|
| S02 — Saisie/lancer | Collision résolue : frappe mêlée ou impact de lancer | `damage_base` = `melee_damage_base` ou `throw_damage_base` du catalogue · `stage_mult` = `stage_data[current_stage].melee_dmg_mult` ou `.throw_dmg_mult` · `damage_type` = `MELEE` ou `THROW` |
| S09 — IA ennemie | Ennemi frappe le joueur | `damage_base` = `enemy.attack_damage` · `stage_mult` = `1.0` · `damage_type` = `ENEMY_MELEE` |

**Qui reçoit l'output de S06 :**
| Récepteur | Via | Ce qu'il en fait |
|-----------|-----|-----------------|
| S08 — Santé ennemie | S02 → `Enemy.receive_damage(amount, type)` | Décrémente HP · déclenche mort si HP ≤ 0 · notifie S15 (VFX) |
| S07 — Santé joueur | S09 → `PlayerHealth.receive_damage(amount, type)` | Décrémente HP · déclenche game-over si HP ≤ 0 · notifie S13 (HUD) |
| S04 — Dégradation | S02 → `DestructionTracker.receive_damage(amount)` | Accumule `cumulative_damage` · évalue transitions de stade |

**Flux d'un impact mêlée :**
```
S02 détecte collision
    │
    ├─ lit catalogue_entry.melee_damage_base              → damage_base
    ├─ lit stage_data[current_stage].melee_dmg_mult       → stage_mult
    │
    ▼
S06.calculate(damage_base, stage_mult, MELEE) → int final_damage
    │
    ├─► S08.receive_damage(final_damage, MELEE)             # ennemi perd des HP
    └─► S04.DestructionTracker.receive_damage(final_damage) # objet se dégrade
```

S02 appelle S06 une seule fois par impact, puis distribue le résultat. S06 n'est jamais appelé deux fois pour le même impact.

## Formulas

**`DamageType` (enum)**
```
MELEE       # frappe directe
THROW       # impact de lancer
ENEMY_MELEE # attaque ennemie
```

**Paramètres**

| Paramètre | Type | Source | Plage MVP |
|-----------|------|--------|-----------|
| `damage_base` | `int` | Catalogue S05 (joueur) ou définition ennemie S09 | 1 – 15 |
| `stage_mult` | `float` | `stage_data[current_stage]` (S05) ou `1.0` (ennemi) | 0.5 – 2.0 |
| `damage_type` | `DamageType` | Appelant | — |

**Constante**

| Constante | Valeur | Rôle |
|-----------|--------|------|
| `DAMAGE_MIN` | `1` | Plancher : toute frappe inflige au moins 1 dégât |

**Formule principale**
```
final_damage = max(DAMAGE_MIN, floori(damage_base × stage_mult))
```

**Plage de sortie (MVP)**

| Cas | `damage_base` | `stage_mult` | `final_damage` |
|-----|--------------|-------------|---------------|
| Minimum absolu | 1 | 0.5 | `max(1, floori(0.5))` = **1** |
| Objet léger, stade normal | 3 | 1.0 | `max(1, 3)` = **3** |
| Objet moyen, stade normal | 7 | 1.0 | **7** |
| Objet lourd, stade normal | 12 | 1.0 | **12** |
| Objet lourd, stade renforcé | 12 | 1.5 | `floori(18.0)` = **18** |
| Objet maximum, stade maximum | 15 | 2.0 | `floori(30.0)` = **30** (max théorique MVP) |
| Ennemi frappe joueur | 3 | 1.0 | **3** (exemple type) |

> **Note calibration** : avec des ennemis à ~12 HP (baseline S05), un objet à `damage_base = 7` et `stage_mult = 1.0` nécessite 2 frappes mêlée pour tuer — cohérent avec la cible "2–3 hits mêlée".

## Edge Cases

**1 — `damage_base = 0` ou négatif**
Impossible en pratique (catalogue S05 garantit `melee_damage_base ≥ 1`). Si cela arrive malgré tout, `max(DAMAGE_MIN, floori(0 × n))` = `max(1, 0)` = **1** — le plancher protège l'appel. Aucune assertion supplémentaire requise pour le MVP.

**2 — `stage_mult = 0.0`**
Résultat : `floori(damage_base × 0.0)` = `0` → clamped à **1** par `DAMAGE_MIN`. Autorisé comme valeur de paramètre ; S06 produit toujours au moins 1.

**3 — `stage_mult` très élevé (dépassement volontaire ou bug)**
Pas de cap MVP. `floori(15 × 10.0)` = **150**. Si ce cas se produit en jeu (bug dans les données de stade), S07/S08 clampent à 0 HP — mort instantanée. La responsabilité du cap appartient aux données de stade (Tuning Knob), pas à S06.

**4 — Appel avec `damage_type` invalide**
GDScript émet une erreur de type statique si l'enum est incorrect. S06 suppose que l'appelant transmet un `DamageType` valide — pas de guard clause nécessaire.

**5 — Multi-cible (objet lancé qui traverse plusieurs ennemis)**
S06 est appelé une fois par cible. S02 est responsable de l'itération. S06 ne voit jamais le contexte multi-cible — chaque appel est indépendant.

**6 — Cible déjà à 0 HP**
S06 ne connaît pas l'état de santé de la cible. Il retourne un dégât valide même si la cible est déjà morte. C'est S07 ou S08 qui gère l'état "déjà mort" (idempotence de `receive_damage`).

**7 — Appel pendant l'état game-over ou victoire**
S11 (gestionnaire d'état) est responsable de désactiver la physique / les collisions dans ces états. S06 peut techniquement être appelé — il retourne un int valide — mais S07/S08 ignorent les appels si leur système est inactif. S06 n'a pas besoin de connaître l'état du jeu.

## Dependencies

**Upstream (S06 dépend de) :**
Aucun. S06 est Foundation layer, sans dépendance sur d'autres systèmes. Les paramètres sont fournis par l'appelant au moment de l'appel.

**Downstream (systèmes qui dépendent de S06) :**

| Système | Nature de la dépendance |
|---------|------------------------|
| S02 — Saisie/lancer | Appelle S06 à chaque impact résolu pour obtenir `final_damage` avant de notifier S08 et S04 |
| S07 — Santé joueur | Reçoit `final_damage` (int) via S09 → `PlayerHealth.receive_damage(amount, type)` |
| S08 — Santé ennemie | Reçoit `final_damage` (int) via S02 → `Enemy.receive_damage(amount, type)` |
| S09 — IA ennemie | Appelle S06 quand un ennemi frappe le joueur, passe le résultat à S07 |
| S04 — Dégradation | Reçoit `final_damage` (int) via S02 → `DestructionTracker.receive_damage(amount)` |
| S14 — Retour audio | Reçoit `damage_type` pour jouer le bon son d'impact (V1.0) |
| S15 — Retour visuel | Reçoit `damage_type` pour déclencher le bon VFX (V1.0) |

**Interface contractuelle :**
S06 expose une seule fonction avec une signature stable : `calculate(damage_base: int, stage_mult: float, damage_type: DamageType) -> int`. Tout changement de cette signature est un breaking change pour S02 et S09.

## Tuning Knobs

| Knob | Valeur initiale | Plage sûre | Effet gameplay |
|------|----------------|-----------|----------------|
| `DAMAGE_MIN` | `1` | `1` (ne pas descendre en dessous) | Plancher absolu — garantit l'observabilité de toute frappe. Monter au-delà de 1 rend les objets faibles moins distincts. |
| `damage_base` (par objet) | 3 – 15 selon l'objet | Calibré via S05 | Rythme de kill : trop bas = frustrant, trop haut = trivial. Baseline : ennemi ~12 HP, objet moyen = 7. |
| `melee_dmg_mult` (par stade) | 0.5 – 2.0 | 0.25 – 3.0 | Montée en puissance en cours de vague. Dépasser 2.0 risque de rendre les fins de vague triviales. |
| `throw_dmg_mult` (par stade) | 0.75 – 2.0 | 0.25 – 3.0 | Identique à mêlée mais pour les lancers. Peut diverger de `melee_dmg_mult` pour renforcer l'intérêt stratégique des lancers. |
| `KILL_FEEL_MAX` | `5` | 3 – 7 | Contrainte de calibration : tout objet du catalogue doit tuer un ennemi standard en ≤ 5 frappes à `stage_mult = 1.0`. Implique `HP_ennemi ≤ KILL_FEEL_MAX × damage_base_min`, où `damage_base_min = 3` (l'objet le plus léger du catalogue S05, ex : livre ou bouteille) → `HP_ennemi ≤ 15`. Compatible avec la baseline 12 HP. La plage théorique `damage_base ≥ 1` s'applique aux valeurs de paramètre brutes — la contrainte KILL_FEEL_MAX s'applique aux objets réels du catalogue. Si cette contrainte est violée lors du calibrage S05, ajuster `damage_base` des objets légers ou le `HP_ennemi` de base. Violation = Pilier 2 brisé. |

> Les valeurs de `damage_base` et `stage_mult` sont définies et modifiables dans S05 (catalogue d'objets). `DAMAGE_MIN` et `KILL_FEEL_MAX` sont les constantes de calibration appartenant en propre à S06.

## Visual/Audio Requirements

S06 est une formule pure — il n'a aucune exigence visuelle ou audio propre. C'est le `DamageType` qu'il retourne (en plus du `final_damage`) qui informe les systèmes de feedback :

- **S15 (VFX)** — utilise `damage_type` pour choisir le bon effet d'impact (éclat mêlée vs. impact de lancer vs. coup ennemi)
- **S14 (Audio)** — utilise `damage_type` pour jouer le bon son (V1.0)

S06 n'a pas à connaître ces systèmes. Il n'émet pas de signaux, ne référence pas S14 ou S15. La chaîne de notification est : `S02/S09 → S08/S07 → S15/S14`. S06 fournit les données, les systèmes aval décident du feedback.

## UI Requirements

S06 n'a aucune exigence UI directe. Il ne produit pas d'affichage. Les systèmes UI concernés reçoivent les données via leurs propres systèmes sources :

- **S13 (HUD)** — affiche les HP du joueur ; alimenté par S07, pas S06
- Pas de chiffres de dégâts flottants pour le MVP (décision par défaut — la lisibilité passe par la réaction de l'ennemi, pas par des nombres à l'écran)

Si des chiffres de dégâts flottants sont ajoutés en V1.0 ou polish, c'est S15 (VFX) qui les affiche en recevant `final_damage` de S02 — S06 n'a toujours rien à implémenter.

## Acceptance Criteria

**AC-S06-01 — Formule correcte**
Étant donné `damage_base = 7`, `stage_mult = 1.0`, `damage_type = MELEE`, le résultat est exactement `7`. *(test unitaire)*

**AC-S06-02 — Plancher DAMAGE_MIN**
Étant donné `damage_base = 1`, `stage_mult = 0.0`, le résultat est `1` (jamais `0`). *(test unitaire)*

**AC-S06-03 — Arrondi vers le bas**
Étant donné `damage_base = 7`, `stage_mult = 1.5`, le résultat est `10` (`floori(10.5)` = 10, pas 11). *(test unitaire)*

**AC-S06-04 — Multiplicateur de stade**
Étant donné `damage_base = 12`, `stage_mult = 2.0`, le résultat est `24`. *(test unitaire)*

**AC-S06-05 — Symétrie ennemie**
Étant donné `damage_base = 3`, `stage_mult = 1.0`, `damage_type = ENEMY_MELEE`, le résultat est `3` — même formule, même résultat que pour MELEE. *(test unitaire)*

**AC-S06-06 — Absence d'état inter-appels**
Étant donné trois appels séquentiels : `calculate(7, 1.0, MELEE)` → `calculate(3, 1.5, THROW)` → `calculate(7, 1.0, MELEE)`, le 3ème résultat est identique au 1er (`7`). Ce pattern prouve l'absence d'état entre appels — un système stateful dont l'état aurait été modifié par le 2ème appel échouerait ce test. *(test unitaire)*

**AC-S06-07 — Calibration arithmétique**
Étant donné `damage_base = 7`, `stage_mult = 1.0`, la formule retourne exactement `7`. Par arithmétique pure : 12 HP / 7 → 2 frappes (7+7 = 14 ≥ 12). La cible 2–3 frappes est validée par le calcul, indépendamment de S05/S08. *(test unitaire — vérification arithmétique)*

**AC-S06-08 — DamageType accepté par la signature**
Étant donné `damage_base = 5`, `stage_mult = 1.0`, `damage_type = THROW`, la fonction retourne `5` sans erreur — `DamageType` n'affecte pas le calcul. La propagation de `damage_type` aux récepteurs (S08, S07) est testée dans les ACs de S02. *(test unitaire)*

**AC-S06-09 — Couverture THROW avec troncature**
Étant donné `damage_base = 6`, `stage_mult = 1.2`, `damage_type = THROW`, le résultat est `7` (`floori(7.2)` = 7, pas 8). Confirme que THROW utilise la même formule que MELEE et ENEMY_MELEE, et valide la troncature sur le type THROW spécifiquement. *(test unitaire)*

## Open Questions

**OQ-01 — ADR `DamageCalculator`**
La structure d'implémentation (`class_name DamageCalculator` avec `static func`, ou autre pattern) doit être formalisée dans un ADR avant que S02 et S09 commencent à appeler S06. Sans ADR, chaque développeur peut interpréter "stateless" différemment.
*Priorité : haute — résoudre avant l'implémentation de S02.*

**OQ-02 — `damage_type` dans la signature de `receive_damage`**
Le contrat actuel passe `damage_type` à `Enemy.receive_damage(amount, type)` et `PlayerHealth.receive_damage(amount, type)`. S07 et S08 n'ont pas encore été conçus — il faut confirmer que leurs signatures acceptent ce deuxième paramètre.
*Priorité : moyenne — à valider lors de la conception de S07 et S08.*
