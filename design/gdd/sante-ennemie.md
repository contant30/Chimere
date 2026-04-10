# S08 — Santé ennemie

> **Statut**: Approuvé
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-10
> **Implémente le Pilier**: Pilier 1 — Tout est une arme · Pilier 2 — Le flow avant le challenge

## Overview

S08 gère les points de vie de chaque ennemi individuellement. Chaque instance S08 est initialisée à `HP_ennemi_basique` (12) à l'apparition de l'ennemi et réinitialisée à chaque spawn — contrairement à S07, le HP ennemi ne persiste pas entre les vagues. S08 expose `receive_damage(amount: int, damage_type: DamageCalculator.DamageType)`, le même contrat d'interface que S07 (ADR-0008), appelé par S02 (saisie/lancer) lorsque le joueur frappe ou projette un objet sur un ennemi. Les ennemis n'ont aucune fenêtre d'invincibilité — chaque coup est absorbé. Quand `current_hp` atteint zéro, S08 émet `enemy_died(enemy: Node)` vers S03 (vagues d'ennemis), puis se retire de la scène. À chaque coup valide, S08 émet `enemy_hit(damage, damage_type, current_hp)` vers S15 (VFX/Audio, V1.0). Du point de vue joueur, S08 est la traduction directe du Pilier 1 — chaque objet saisi est une arme potentielle, et chaque ennemi est une résistance concrète : le nombre de coups pour l'abattre (calibré par KILL_FEEL_MAX ≤ 5) est la mesure tangible de la puissance de frappe.

## Player Fantasy

Aucune animation d'armure. Aucun clignotement d'invincibilité. Chaque impact est accusé réception — l'ennemi l'absorbe, visiblement, honnêtement. Le joueur n'a pas à négocier avec le système pour obtenir une confirmation ; il agit, l'ennemi réagit, le prochain temps suit naturellement. La mise à mort arrive en trois à cinq frappes — assez court pour que tuer un ennemi soit une phrase dans une séquence plus longue, pas une rencontre à part entière.

Les ennemis n'existent pas pour être battus. Ils existent pour donner forme au mouvement du joueur : pour tomber au bon moment dans la chorégraphie, pour transformer chaque objet ramassé en preuve de sa valeur. Un ennemi encore debout n'est pas un obstacle — c'est un temps musical qui n'est pas encore arrivé à sa résolution. Quand il tombe, ce n'est pas une victoire. C'est la clôture d'une mesure.

## Detailed Design

### Core Rules

1. **HP initial** : à chaque spawn, `current_hp` est initialisé à `HP_ennemi_basique` (12). Le HP ne persiste pas entre les spawns — chaque nouvelle instance repart à 12. Aucun reset() : la mort d'un ennemi est terminale pour cette instance.

2. **Interface de réception** : S08 expose `receive_damage(amount: int, damage_type: DamageCalculator.DamageType)`. L'appelant est S02 (saisie/lancer) lors du contact d'un objet manié ou projeté. L'`amount` est un entier ≥ 1 (DAMAGE_MIN garanti par S06). En défensif : si `amount == 0`, l'appel est un no-op (aucun signal). S08 ne recalcule pas les dégâts.

3. **Aucune fenêtre d'invincibilité** : chaque appel à `receive_damage()` est traité immédiatement, sans délai ni protection temporaire. Les multi-hits en rafale s'accumulent tous.

4. **Réduction des HP** : `current_hp` est réduit de `amount` et clampé à 0 (`max(0, current_hp - amount)`).

5. **Signal sur coup valide** : après chaque réduction, S08 émet `enemy_hit(damage: int, damage_type: DamageCalculator.DamageType, current_hp: int)` → S15 (VFX/audio feedback).

6. **Détection de mort** : si `current_hp == 0` après réduction, S08 émet `enemy_died(enemy: Node)` → S03 (vagues d'ennemis), passe en état `DEAD`, puis appelle `queue_free()` pour retirer l'ennemi de la scène. Le retrait est immédiat — l'animation de mort est déléguée à S15 (V1.0) via le signal.

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
| **S02** (Saisie/Lancer) | → S08 | `receive_damage(amount, damage_type)` lors d'un contact d'objet | Appel direct sur le composant `EnemyHealth` de l'ennemi touché (pattern exact validé au prototype S02) |
| **S06** (Dégâts) | → S08 via S02 | `amount: int` (DAMAGE_MIN=1 garanti) | Valeur calculée par S06, transmise par S02 |
| **S03** (Vagues) | ← S08 | `enemy_died(enemy: Node)` | Signal GDScript |
| **S15** (VFX/Audio, V1.0) | ← S08 | `enemy_hit(damage, damage_type, current_hp)` | Signal GDScript |

S08 ne connaît aucun consommateur directement — il émet des signaux. Les connexions sont établies par S09 (IA ennemie, nœud parent) au moment du spawn via `connect()` (Callable-based, ADR-0005). S09 héberge l'instance S08, mais S08 n'a pas de dépendances injectées en MVP.

## Formulas

### F1 — Application des dégâts

```
current_hp_new = max(0, current_hp - amount)
```

Variables :
- `current_hp` : int, [0, HP_ennemi_basique], état courant avant le coup
- `amount` : int, [DAMAGE_MIN, ∞), dégâts reçus (calculés par S06, garantis ≥ 1)
- `current_hp_new` : int, [0, HP_ennemi_basique], état après le coup

Exemple — coup à 5 dégâts, ennemi à 8 HP : `max(0, 8 − 5) = 3 HP`
Exemple — coup fatal à 7 dégâts, ennemi à 4 HP : `max(0, 4 − 7) = 0 HP → enemy_died()`

### F2 — Contrainte KILL_FEEL_MAX (vérification de calibration)

```
ceil(HP_ennemi_basique / damage_base_min) ≤ KILL_FEEL_MAX
```

Variables :
- `HP_ennemi_basique` : int, 12 — HP de départ de chaque ennemi
- `damage_base_min` : int, 3 — dégâts de l'objet le plus léger du catalogue (S05/S06)
- `KILL_FEEL_MAX` : int, 5 — nombre de coups maximum acceptable pour tuer un ennemi standard

Vérification MVP : `ceil(12 / 3) = 4 ≤ 5` ✓

Cette formule n'est pas exécutée en jeu — c'est une contrainte de calibration à vérifier lors de tout ajustement de `HP_ennemi_basique` ou `damage_base_min`. Si la contrainte est violée, le combat perd sa fluidité (Pilier 2).

## Edge Cases

**EC-01 — Dégâts reçus en état DEAD**
`receive_damage()` appelé après que `current_hp == 0` (ex. deux objets touchent l'ennemi dans la même frame). → Ignoré silencieusement. Aucun signal émis. `queue_free()` a déjà été déclenché ou est en cours — l'instance n'existe plus dans la frame suivante.

**EC-02 — Dégâts supérieurs aux HP restants**
`amount > current_hp` (ex. 10 dégâts, ennemi à 4 HP). → `current_hp` clampé à 0 via F1. `enemy_died()` émis. Le surplus de dégâts est perdu.

**EC-03 — Deux objets touchent l'ennemi dans la même frame**
Godot/Jolt traite les collisions séquentiellement dans `_physics_process`. Le premier `receive_damage()` est appliqué ; si l'ennemi survit, le second est aussi appliqué dans la même frame. Si le premier tue l'ennemi (`current_hp == 0`), le second appel arrive en état DEAD et est ignoré (EC-01). Pas de double mort, pas de double signal.

**EC-04 — amount = 0 reçu**
S06 garantit DAMAGE_MIN=1, mais un appelant mal formé pourrait passer 0. → No-op défensif : aucun changement de HP, aucun signal `enemy_hit`, aucune mort.

**EC-05 — enemy_died émis avant que S03 soit connecté**
Si un ennemi meurt avant que ses signaux soient connectés au spawn (bug de séquencement). → Le signal est émis mais n'a aucun listener — GDScript ignore silencieusement les signaux sans listener. S03 ne comptabilise pas la mort. À prévenir par l'ordre d'initialisation dans S09.

**EC-06 — Ennemi tué pendant une vague en transition**
S03 déclenche une transition de vague au même moment qu'un `enemy_died()` arrive. → S08 émet le signal sans connaissance du contexte vague. S03 est responsable de gérer les signaux tardifs en transition (décision déléguée à S03).

## Dependencies

### Dépendances entrantes (S08 dépend de)

| Système | Ce que S08 en attend |
|---|---|
| **S06 — Système de dégâts** | Fournit `amount: int` avec DAMAGE_MIN=1 garanti. S08 ne valide pas cette valeur. |
| **S02 — Saisie et lancer** | Appelle `receive_damage(amount, damage_type)` lors du contact d'un objet manié ou projeté. S02 est responsable de la conversion float→int avant l'appel (décision S06). |
| **S09 — IA ennemie** | Héberge l'instance S08 comme nœud enfant et établit les connexions de signaux (S03, S15) via `connect()` (Callable-based). |

### Dépendances sortantes (systèmes qui dépendent de S08)

| Système | Ce qu'il reçoit de S08 |
|---|---|
| **S03 — Vagues d'ennemis** | `enemy_died(enemy: Node)` — déclenche le comptage des morts et la progression de vague. |
| **S15 — VFX/Audio (V1.0)** | `enemy_hit(damage, damage_type, current_hp)` — déclenche les feedbacks visuels et sonores sur impact. |

### Note de symétrie avec S07

S08 et S07 partagent le même contrat d'interface entrant (`receive_damage(amount: int, damage_type: DamageCalculator.DamageType)`) mais divergent sur trois points : (1) S08 n'a pas de I-frames ; (2) S08 ne s'auto-réinitialise pas (cycle de vie terminé par `queue_free()`) ; (3) S08 est multi-instancié (un par ennemi vivant) alors que S07 est singleton de session.

## Tuning Knobs

| Knob | Valeur MVP | Plage sûre | Effet gameplay |
|---|---|---|---|
| `HP_ennemi_basique` | 12 | [6, 20] | HP de départ de chaque ennemi. En dessous de 6 : l'objet le plus lourd one-shot à distance, récompense la chance plus que la précision. Au-dessus de 20 : KILL_FEEL_MAX violé (`ceil(20/3)=7 > 5`), le combat traîne et le flow se brise. Toute modification doit revalider F2. |
| `KILL_FEEL_MAX` | 5 | [3, 7] | Nombre de coups maximum pour tuer un ennemi avec l'objet le plus léger. En dessous de 3 : les ennemis meurent trop vite, le joueur n'a pas le temps de lire la séquence. Au-dessus de 7 : le combat s'enlise. Contrainte de calibration, pas une variable runtime. |

## Visual/Audio Requirements

S08 ne possède aucun asset visuel ou audio. Il délègue entièrement via signaux.

| Signal émis | Consommateur | Réponse attendue |
|---|---|---|
| `enemy_hit(damage, type, current_hp)` | S15 (VFX/Audio) | Particules d'impact, son de coup, réaction physique de l'ennemi |
| `enemy_died(enemy: Node)` | S15 (VFX/Audio) | Animation de mort, son de mort, effets de destruction |
| `enemy_died(enemy: Node)` | S03 | Mise à jour compteur vague (aucun effet visuel direct) |

## UI Requirements

S08 ne rend rien lui-même. Aucun affichage de HP ennemi n'est prévu en MVP — les ennemis n'ont pas de barre de vie visible. Le feedback de progression vers la mort passe uniquement par les réactions visuelles de S15 (animation d'impact, comportement physique de l'ennemi).

## Acceptance Criteria

**AC-01** — Quand un ennemi spawn, `current_hp == 12`. Vérifiable : log ou assertion au `_ready()` de S08.

**AC-02** — `receive_damage(5, THROW)` depuis l'état ALIVE réduit `current_hp` de 5. Vérifiable : test unitaire sur le nœud S08 isolé.

**AC-03** — Deux appels successifs à `receive_damage()` dans la même frame s'accumulent (pas de protection). Vérifiable : test unitaire — deux appels de 4 dégâts sur un ennemi à 12 HP → `current_hp == 4`.

**AC-04** — Quand `current_hp` atteint 0, le signal `enemy_died(enemy)` est émis exactement une fois. Vérifiable : test unitaire avec spy sur le signal.

**AC-05** — `receive_damage()` en état DEAD n'émet aucun signal et ne modifie pas `current_hp`. Vérifiable : test unitaire.

**AC-06** — `enemy_hit(damage, type, current_hp)` est émis à chaque réduction valide de HP. Vérifiable : test unitaire avec spy.

**AC-07** — Un ennemi à `HP_ennemi_basique = 12` est tué en au plus 4 coups avec `damage_base_min = 3` (`ceil(12/3) = 4 ≤ KILL_FEEL_MAX = 5`). Vérifiable : test unitaire — 4 appels `receive_damage(3, THROW)` → `enemy_died()` émis.

**AC-08** — Une nouvelle instance d'ennemi (après respawn) démarre toujours à `current_hp == 12`, indépendamment du HP de l'instance précédente. Vérifiable : test unitaire — instancier deux fois, vérifier HP initial de chacune.

## Open Questions

**OQ-01 — Feedback visuel de HP restant sans barre de vie** : Comment le joueur sait-il qu'un ennemi est proche de la mort sans barre de vie visible ? Décision déléguée à S15 (VFX) — candidates : animation de boiterie, changement de couleur/matériau, particules progressives. À valider au prototype S08/S15.

**OQ-02 — Variantes de HP post-MVP** : Quels types d'ennemis auront des HP différents ? (`HP_ennemi_lourd`, `HP_ennemi_rapide`.) Décision reportée après le prototype — le registre devra être mis à jour et F2 revalidée pour chaque variant.

**OQ-03 — enemy_died : passer l'entité complète ou juste un ID ?** : Le signal passe actuellement `enemy: Node`. Si S03 a besoin de données supplémentaires (type d'ennemi, position), faudra-t-il enrichir la signature ? Décision reportée à la conception de S03.
