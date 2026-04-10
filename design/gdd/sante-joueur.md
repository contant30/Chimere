# S07 — Santé joueur + game-over

> **Statut**: Approuvé
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-10
> **Implémente le Pilier**: Pilier 2 — Le flow avant le challenge

## Overview

S07 gère les points de vie (HP) du joueur dans une session de combat. Il reçoit les dégâts calculés par S06 sous forme d'entier (DAMAGE_MIN=1 garanti), réduit `current_hp`, et émet les signaux `player_hit` et `player_died` vers S11 (gestionnaire d'état) et S13 (HUD). Quand `current_hp` atteint zéro, S11 orchestre le game-over et le retry en moins de 3 secondes (Pilier 2 — Le flow avant le challenge). Du point de vue joueur, chaque coup est immédiat et lisible : la survie se joue par l'esquive et la maîtrise des objets, pas par des mécaniques de mitigation invisibles.

## Player Fantasy

Le joueur ne "meurt" pas — sa performance *s'arrête*. Chaque coup reçu est un hiatus dans la chorégraphie : le rythme accroche, le flux s'interrompt. Les HP ne sont pas une réserve de survie à gérer — ils sont la mesure de la fluidité maintenue. Perdre des HP, c'est entendre une fausse note dans le solo. La mort est la confirmation que la bande s'est arrêtée, pas un mur de punition.

Le retry immédiat est le rembobinage. Le joueur ne pense pas "j'ai échoué" — il pense "cette fois je n'aurai pas ce gap dans la séquence". Le retour sous 3 secondes (Pilier 2) n'est pas une concession d'accessibilité : c'est l'affirmation que chaque run est une tentative créative, pas un investissement à perdre.

La violence va dans un sens : le joueur l'inflige. Ce qui lui arrive est un *coût de la chorégraphie*, pas une agression narrative.

## Detailed Design

### Core Rules

1. **Santé initiale** : à chaque début de session de combat, `current_hp` est initialisé à `HP_JOUEUR_MAX` (20). La valeur ne se réinitialise pas entre les vagues — elle persiste jusqu'au game-over ou à la fin de la session.

2. **Réception des dégâts** : S07 expose `receive_damage(amount: int, damage_type: DamageCalculator.DamageType)`. L'appelant (S09 — IA ennemie, au contact) fournit un entier ≥ 1 (DAMAGE_MIN garanti par S06). En défensif : si `amount == 0`, l'appel est un no-op (aucun signal). S07 ne recalcule pas les dégâts.

3. **Invincibilité temporaire (I-frames)** : après avoir reçu un coup, le joueur est invincible pendant `I_FRAME_DURATION` (0,5 s). Tout appel à `receive_damage()` pendant cette fenêtre est ignoré silencieusement. Les I-frames s'appliquent indépendamment de `DamageCalculator.DamageType`.

4. **Réduction des HP** : si le joueur est en état `ALIVE` et hors I-frames, `current_hp` est réduit de `amount`. `current_hp` est clampé à 0 (ne devient jamais négatif).

5. **Émission des signaux** : après chaque réduction valide de HP, S07 émet :
   - `player_hp_changed(current_hp: int, max_hp: int)` → S13 (HUD, toujours)
   - `player_hit(damage: int, damage_type: DamageCalculator.DamageType, current_hp: int)` → S11, S13 (feedback visuel/audio)

6. **Détection de mort** : si `current_hp == 0` après réduction, S07 émet `player_died()` → S11 orchestre le game-over. S07 passe en état `DEAD` et ignore tout appel ultérieur à `receive_damage()`.

7. **Aucune régénération** : S07 ne propose pas de mécanisme de soin en MVP. HP ne remonte jamais pendant une session.

### States and Transitions

| État | Description | Transitions sortantes |
|---|---|---|
| `ALIVE` | Joueur opérationnel, HP > 0 | → `DEAD` si current_hp atteint 0 |
| `DEAD` | Joueur mort, HP = 0, signaux émis | → aucune (en MVP : retry = rechargement de scène, nouvelle instance) |

Deux états seulement. Pas d'état `LOW_HP`, `STUNNED`, ou `INVINCIBLE` en tant qu'état discret — les I-frames sont une variable interne booléenne, pas un état de la machine.

**Transition ALIVE → DEAD** : déclenchée uniquement par `receive_damage()` lorsque `current_hp` tombe à 0. Irréversible pendant la session en cours.

**Transition DEAD → ALIVE** : pas de transition intra-instance en MVP. Le retry (S12) recharge la scène, recréant une nouvelle instance de S07.

### Interactions with Other Systems

| Système | Direction | Données | Interface |
|---|---|---|---|
| **S06** (Dégâts) | → S07 | `amount: int` (sortie de damage_formula, DAMAGE_MIN=1) | Valeur passée par S09 à `receive_damage()` |
| **S09** (IA ennemie) | → S07 | `receive_damage(amount: int, damage_type: DamageCalculator.DamageType)` | Appel direct sur le nœud Player (contrat S07 exposé par la scène Player) |
| **S11** (État global) | ← S07 | `player_died()`, `player_hit(...)` | Signaux GDScript |
| **S13** (HUD) | ← S07 | `player_hp_changed(current_hp, max_hp)`, `player_hit(...)` | Signaux GDScript |

S07 ne connaît ni S11 ni S13 directement — il émet des signaux. S11 et S13 se connectent à S07 via @export ou via `connect()` au chargement de scène. S07 ne sait pas combien de listeners existent.

## Formulas

### F1 — Application des dégâts

```
current_hp_new = max(0, current_hp - amount)
```

Variables :
- `current_hp` : int, [0, HP_JOUEUR_MAX], état courant avant le coup
- `amount` : int, [DAMAGE_MIN, ∞), dégâts reçus (calculés par S06, garantis ≥ 1)
- `current_hp_new` : int, [0, HP_JOUEUR_MAX], état après le coup

Exemple — coup à 7 dégâts, joueur à 12 HP : `max(0, 12 − 7) = 5 HP`
Exemple — coup fatal à 15 dégâts, joueur à 8 HP : `max(0, 8 − 15) = 0 HP → player_died()`

### F2 — Fenêtre d'invincibilité

```
is_invincible = (time_since_last_hit < I_FRAME_DURATION)
```

Variables :
- `time_since_last_hit` : float, secondes écoulées depuis le dernier coup valide reçu
- `I_FRAME_DURATION` : float, 0,5 s (constante)
- `is_invincible` : bool, si vrai → `receive_damage()` ignoré

Plage effective : fenêtre de 0,0 à 0,5 s post-impact. Aucun calcul cumulatif — chaque coup valide remet le timer à 0.

### F3 — Détection seuil critique (usage S13)

```
is_low_hp = (current_hp <= HP_LOW_THRESHOLD)
```

Variables :
- `current_hp` : int, état courant
- `HP_LOW_THRESHOLD` : int, 6 (≤ 30 % de HP_JOUEUR_MAX=20)

S07 émet `player_hp_changed` à chaque changement ; S13 calcule `is_low_hp` localement pour déclencher le feedback visuel d'urgence. S07 ne connaît pas ce seuil.

## Edge Cases

**EC-01 — Dégâts reçus en état DEAD**
`receive_damage()` appelé alors que `current_hp == 0`. → Ignoré silencieusement. Aucun signal émis. S07 ne peut pas descendre sous 0.

**EC-02 — Dégâts supérieurs aux HP restants**
`amount > current_hp` (ex. 15 dégâts, 8 HP restants). → `current_hp` clampé à 0 via F1. `player_died()` émis. Le surplus de dégâts est perdu — pas de dégâts de "débordement".

**EC-03 — Appel receive_damage pendant les I-frames**
Coup reçu dans la fenêtre de 0,5 s. → Ignoré silencieusement. Timer I-frames non remis à zéro. Aucun signal `player_hit` émis.

**EC-04 — amount = 0 reçu**
S06 garantit DAMAGE_MIN=1, mais un appelant mal formé pourrait passer 0. → S07 traite normalement (F1 : `max(0, hp - 0) = hp`). Aucun changement de HP, aucun signal `player_hit` émis (pas de dégâts réels). `player_hp_changed` n'est pas émis non plus (HP inchangé).

**EC-05 — Deux ennemis frappent simultanément (même frame)**
Godot traite les signaux de physique séquentiellement dans `_physics_process`. Le premier `receive_damage()` est appliqué et démarre les I-frames. Le second arrive dans la même frame mais après le premier — les I-frames sont déjà actives, il est ignoré. Pas de dégâts doubles en une frame.

## Dependencies

### Dépendances entrantes (S07 dépend de)

| Système | Ce que S07 en attend |
|---|---|
| **S06 — Système de dégâts** | Fournit `amount: int` avec DAMAGE_MIN=1 garanti. S07 ne valide pas cette valeur — si S06 casse ce contrat, S07 peut recevoir 0. |
| **S09 — IA ennemie** | Appelle `receive_damage(amount, damage_type)` lors des contacts. S07 suppose que S09 peut tenter d'appeler chaque frame, et garantit l'équité via les I-frames. |

### Dépendances sortantes (systèmes qui dépendent de S07)

| Système | Ce qu'il reçoit de S07 |
|---|---|
| **S11 — Gestionnaire d'état** | `player_died()` — déclenche le game-over et orchestre le retry. `player_hit(damage, damage_type, current_hp)` — peut déclencher des effets de caméra ou de feedback global. |
| **S13 — HUD** | `player_hp_changed(current_hp, max_hp)` — met à jour l'affichage HP. `player_hit(damage, damage_type, current_hp)` — déclenche l'animation de dégât sur le HUD. |

### Note de circularité

S07 ← S09 ← S07 : S09 frappe le joueur (→ S07), mais S07 ne commande pas S09. Pas de circularité réelle — le flux est unidirectionnel au niveau des données.

## Tuning Knobs

| Knob | Valeur MVP | Plage sûre | Effet gameplay |
|---|---|---|---|
| `HP_JOUEUR_MAX` | 20 | [12, 30] | Nombre de coups encaissables avant mort. En dessous de 12 : un seul objet lourd one-shot (KILL_FEEL_MAX incompatible). Au-dessus de 30 : les combats durent trop longtemps, flow brisé. |
| `I_FRAME_DURATION` | 0,5 s | [0,2, 0,8] | Fenêtre d'invincibilité post-impact. En dessous de 0,2 : les multi-hits simultanés traversent la fenêtre, mort injuste. Au-dessus de 0,8 : le joueur peut ignorer plusieurs ennemis, difficulté effondrée. |
| `HP_LOW_THRESHOLD` | 6 | [4, 8] | Seuil déclenchant les feedbacks visuels d'urgence (S13). Doit rester ≤ 30 % de `HP_JOUEUR_MAX`. En dehors de cette plage : alerte trop tardive (< 4) ou trop précoce (> 8). |

## Visual/Audio Requirements

S07 ne possède aucun asset visuel ou audio. Il délègue entièrement via signaux.

| Signal émis | Consommateur | Réponse attendue |
|---|---|---|
| `player_hit(damage, damage_type, current_hp)` | S13 (HUD) | Flash rouge de l'écran, animation de la barre HP |
| `player_hit(damage, damage_type, current_hp)` | S11 | Shake de caméra (optionnel, calibré au prototype) |
| `player_died()` | S11 | Écran de game-over, gel des contrôles |
| `player_hp_changed(current_hp, max_hp)` | S13 | Mise à jour de la barre HP |

Aucun son ou particule attaché directement à S07.

## UI Requirements

S07 ne rend rien lui-même. S13 (HUD) consomme les signaux pour :

- Barre HP ou compteur numérique affichant `current_hp / HP_JOUEUR_MAX`
- Indicateur visuel d'urgence quand `current_hp ≤ HP_LOW_THRESHOLD` (calculé par S13)
- Animation de dégât sur l'élément HP à chaque `player_hit`

Spécification graphique complète dans `design/ux/hud.md` (à créer avec S13).

## Acceptance Criteria

**AC-01** — Quand le joueur commence une session, `current_hp == 20`. Vérifiable : log ou HUD au démarrage.

**AC-02** — `receive_damage(5, DamageCalculator.DamageType.ENEMY_MELEE)` depuis l'état ALIVE (hors I-frames) réduit `current_hp` de 5. Vérifiable : test unitaire sur le nœud S07 isolé.

**AC-03** — `receive_damage()` appelé moins de 0,5 s après un coup valide n'a aucun effet sur `current_hp`. Vérifiable : test unitaire avec timer simulé.

**AC-04** — `receive_damage()` appelé à exactement 0,5 s ou après est appliqué normalement. Vérifiable : test unitaire (boundary check).

**AC-05** — Quand `current_hp` atteint 0, le signal `player_died()` est émis exactement une fois. Vérifiable : test unitaire avec spy sur le signal.

**AC-06** — `receive_damage()` en état DEAD n'émet aucun signal et ne modifie pas `current_hp`. Vérifiable : test unitaire.

**AC-07** — Après un retry (S12 : rechargement de scène), une nouvelle instance de S07 démarre avec `current_hp == HP_JOUEUR_MAX` (20). Vérifiable : test d'intégration (reload scene) ou vérification au démarrage.

**AC-08** — `player_hp_changed(current_hp, max_hp)` est émis à chaque réduction valide de HP. Vérifiable : test unitaire avec spy.

**AC-09** — En jeu réel : recevoir un coup ne tue jamais instantanément sans possibilité de réaction quand le joueur a ≥ 2 HP (damage_base_min = 3, sauf si HP = 1 ou 2 — cas limites tolérés). Vérifiable : playtest manuel.

## Open Questions

**OQ-01 — Feedback caméra sur player_hit** : S11 doit-il déclencher un shake de caméra sur `player_hit` ? Décision reportée au prototype S07/S11 — risque de sur-saturation visuelle si les I-frames s'enchaînent.

**OQ-02 — Affichage HP numérique vs barre** : S13 doit choisir entre compteur (20/20) ou barre progressive. Décision déléguée à S13/HUD design — S07 émet les deux valeurs dans `player_hp_changed`.

**OQ-03 — Son de low-HP** : musique ou ambiance d'urgence quand `current_hp ≤ HP_LOW_THRESHOLD` ? Décision déléguée à S15 (Audio) — S07 ne sait pas que le seuil existe.
