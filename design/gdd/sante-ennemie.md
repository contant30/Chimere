# Santé ennemie

> **Status**: In Design
> **Author**: Romain Contant + agents
> **Last Updated**: 2026-04-09
> **Implements Pillar**: Pilier 1 — Tout est une arme · Pilier 2 — Le flow avant le challenge

## Overview

S08 gère les points de vie de chaque ennemi individuellement. Chaque instance S08 est initialisée à `HP_ennemi_basique` (12) à l'apparition de l'ennemi et réinitialisée à chaque spawn — contrairement à S07, le HP ennemi ne persiste pas entre les vagues. S08 expose `receive_damage(amount: int, type: DamageType)`, le même contrat d'interface que S07, appelé par S02 (saisie/lancer) lorsque le joueur frappe ou projette un objet sur un ennemi. Les ennemis n'ont aucune fenêtre d'invincibilité — chaque coup est absorbé. Quand `current_hp` atteint zéro, S08 émet `enemy_died(enemy: Node)` vers S10 (gestion des vagues) et S12 (score), puis se retire de la scène. À chaque coup valide, S08 émet `enemy_hit(damage, type, current_hp)` vers S15 (VFX). Du point de vue joueur, S08 est la traduction directe du Pilier 1 — chaque objet saisi est une arme potentielle, et chaque ennemi est une résistance concrète : le nombre de coups pour l'abattre (calibré par KILL_FEEL_MAX ≤ 5) est la mesure tangible de la puissance de frappe.

## Player Fantasy

Aucune animation d'armure. Aucun clignotement d'invincibilité. Chaque impact est accusé réception — l'ennemi l'absorbe, visiblement, honnêtement. Le joueur n'a pas à négocier avec le système pour obtenir une confirmation ; il agit, l'ennemi réagit, le prochain temps suit naturellement. La mise à mort arrive en trois à cinq frappes — assez court pour que tuer un ennemi soit une phrase dans une séquence plus longue, pas une rencontre à part entière.

Les ennemis n'existent pas pour être battus. Ils existent pour donner forme au mouvement du joueur : pour tomber au bon moment dans la chorégraphie, pour transformer chaque objet ramassé en preuve de sa valeur. Un ennemi encore debout n'est pas un obstacle — c'est un temps musical qui n'est pas encore arrivé à sa résolution. Quand il tombe, ce n'est pas une victoire. C'est la clôture d'une mesure.

## Detailed Design

### Core Rules

1. **HP initial** : à chaque spawn, `current_hp` est initialisé à `HP_ennemi_basique` (12). Le HP ne persiste pas entre les spawns — chaque nouvelle instance repart à 12. Aucun reset() : la mort d'un ennemi est terminale pour cette instance.

2. **Interface de réception** : S08 expose `receive_damage(amount: int, type: DamageType)`. L'appelant est S02 (saisie/lancer) lors du contact d'un objet manié ou projeté. L'`amount` est un entier ≥ 1 (DAMAGE_MIN garanti par S06). S08 ne recalcule pas les dégâts.

3. **Aucune fenêtre d'invincibilité** : chaque appel à `receive_damage()` est traité immédiatement, sans délai ni protection temporaire. Les multi-hits en rafale s'accumulent tous.

4. **Réduction des HP** : `current_hp` est réduit de `amount` et clampé à 0 (`max(0, current_hp - amount)`).

5. **Signal sur coup valide** : après chaque réduction, S08 émet `enemy_hit(damage: int, type: DamageType, current_hp: int)` → S15 (VFX/audio feedback).

6. **Détection de mort** : si `current_hp == 0` après réduction, S08 émet `enemy_died(enemy: Node)` → S10 (gestion des vagues) et S12 (score), passe en état `DEAD`, puis appelle `queue_free()` pour retirer l'ennemi de la scène. Le retrait est immédiat — l'animation de mort est déléguée à S15 via le signal.

7. **Type unique en MVP** : tous les ennemis partagent `HP_ennemi_basique = 12`. Les variantes de HP arrivent post-prototype.

8. **stage_mult fixe** : `stage_mult = 1.0` pour les ennemis (décision registry). La difficulté par vague est gérée par le volume et le type d'ennemis, pas par le scaling de dégâts.

### States and Transitions

| État | Description | Transitions sortantes |
|---|---|---|
| `ALIVE` | Ennemi opérationnel, HP > 0 | → `DEAD` si `current_hp` atteint 0 |
| `DEAD` | HP = 0, signaux émis, `queue_free()` appelé | → aucune (instance retirée) |

Deux états, cycle de vie à sens unique. Pas de `reset()` exposé — un nouvel ennemi est une nouvelle instance.

### Interactions with Other Systems

| Système | Direction | Données | Interface |
|---|---|---|---|
| **S02** (Saisie/Lancer) | → S08 | `receive_damage(amount, type)` lors d'un contact d'objet | Appel direct sur le nœud EnemyHealth via `@export` injecté |
| **S06** (Dégâts) | → S08 via S02 | `amount: int` (DAMAGE_MIN=1 garanti) | Valeur calculée par S06, transmise par S02 |
| **S10** (Vagues) | ← S08 | `enemy_died(enemy: Node)` | Signal GDScript |
| **S12** (Score) | ← S08 | `enemy_died(enemy: Node)` | Signal GDScript |
| **S15** (VFX/Audio) | ← S08 | `enemy_hit(damage, type, current_hp)` | Signal GDScript |

S08 ne connaît aucun consommateur directement — il émet des signaux. Les connexions sont établies par S09 (IA ennemie, nœud parent) au moment du spawn via `connect()`. S09 héberge l'instance S08 et injecte ses dépendances, mais ne déclenche pas `receive_damage()` lui-même en MVP.

## Formulas

[To be designed]

## Edge Cases

[To be designed]

## Dependencies

[To be designed]

## Tuning Knobs

[To be designed]

## Visual/Audio Requirements

[To be designed]

## UI Requirements

[To be designed]

## Acceptance Criteria

[To be designed]

## Open Questions

[To be designed]
