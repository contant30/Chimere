# S10 — Caméra TPS

> **Statut**: In Review
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-10
> **Implémente le Pilier**: Pilier 2 — Le flow avant le challenge

## Overview

S10 — Caméra TPS est le système qui positionne et oriente la vue du joueur dans la pièce. Techniquement, il s'appuie sur un pivot de caméra (`Node3D`) enfant du personnage joueur, dont le yaw est contrôlé par l'input souris / stick droit, et dont la distance est gérée par un `SpringArm3D` qui évite le clipping dans les murs. Chaque frame, S10 expose un angle horizontal (`camera_yaw_radians`) que S01 utilise pour orienter le déplacement, et que S02 utilise pour calculer la direction des lancers. Pour le joueur, la caméra n'est pas un outil — c'est sa façon de lire l'espace : d'un coup d'œil, il voit les objets disponibles, les ennemis qui approchent, et l'état de dégradation de la pièce. Un bon positionnement de caméra n'est pas un avantage tactique conscient, c'est un réflexe invisible qui rend toutes les décisions possibles.

## Player Fantasy

Le joueur ne subit pas la caméra — il la dirige. Chaque rotation est un choix de mise en scène : tourner vers l'ennemi qui charge, c'est décider que ce sera le prochain plan d'action ; centrer la caméra sur la table encore intacte au milieu de la dévastation, c'est annoncer son prochain coup. La caméra transforme le brawler en performance : chaque partie est un plan-séquence improvisé dont le joueur est à la fois l'acteur et le cadreur. Le moment cible : la pièce à moitié détruite, deux ennemis qui convergent, une chaise encore debout entre eux. Le joueur tourne lentement la caméra, cadre la scène. Ce n'est plus de la survie — c'est une chorégraphie. L'expression personnelle ne passe pas seulement par le choix de l'objet : elle passe par l'angle depuis lequel on le voit. La caméra est l'outil qui rend chaque partie unique — pas le hasard, mais le regard.

*Pilier servi : Pilier 1 — "Tout est une arme." Le regard lui-même devient un outil tactique. Pilier 2 — "Le flow avant le challenge." Une caméra qui répond instantanément est la condition silencieuse de la fluidité.*

## Detailed Design

### Core Rules

1. **Yaw libre exclusif** : piloté uniquement par l'input joueur (souris/stick droit). Aucun recadrage automatique, soft-lock, ni Z-targeting en MVP.
2. **Pitch contraint** : plage [PITCH_MIN_DEG, PITCH_MAX_DEG] (défaut : −25°/+40°). Clamp dur aux bornes, sans spring-back. Pas de roll.
3. **SpringArm3D** : longueur CAMERA_DISTANCE (défaut : 4.0 m). Raccourcit sur obstacle automatiquement. Retour lissé à la sortie.
4. **Pivot à hauteur d'épaule** : CameraPivot à CAMERA_PIVOT_HEIGHT (défaut : 1.2 m) au-dessus de la base du CharacterBody3D. Fixe en MVP.
5. **FOV fixe** : CAMERA_FOV (défaut : 75°), constant, non animé en MVP.
6. **CARRYING** : comportement identique à EMPTY_HANDS + réticule de visée statique centré. Le réticule disparaît à la transition vers EMPTY_HANDS.
7. **Gel sur mort** : sur `player_died` (S07), gel immédiat de tout input et de tout signal. Expose `freeze()` / `unfreeze()` à S11. S10 ne connaît pas S11. Couplage unidirectionnel S11→S10.
8. **Signal yaw chaque frame** : `camera_yaw_changed(yaw: float)` émis à chaque `_process()`, même si la valeur est inchangée. Première émission à `_ready()` (0.0 rad).

### States and Transitions

| État | Condition d'entrée | Condition de sortie | Comportement |
|------|--------------------|---------------------|--------------|
| ACTIVE | Initialisation / `unfreeze()` | `player_died` reçu | Yaw + pitch mis à jour chaque frame, `camera_yaw_changed` émis, SpringArm actif |
| FROZEN | `player_died` reçu de S07 | `unfreeze()` appelé par S11 | Aucun input traité, aucune mise à jour de position, signal suspendu |

### Interactions with Other Systems

| Système | Direction | Interface |
|---------|-----------|-----------|
| S01 — Déplacement joueur | S10 → S01 | Émet `camera_yaw_changed(yaw: float)` chaque frame. S01 attend la première valeur avant de traiter les inputs de déplacement. |
| S02 — GrabSystem | S10 → S02 | GrabSystem lit `camera_pivot.global_rotation.y` directement sur le nœud CameraPivot injecté via `@export`. |
| S07 — Santé joueur | S07 → S10 | S07 émet `player_died`. S10 écoute ce signal → transition vers FROZEN. |
| S11 — Game loop | S11 → S10 | S11 appelle `freeze()` / `unfreeze()`. S10 n'a aucune référence sur S11. |

## Formulas

### F1 — Mise à jour du yaw (chaque frame)

```
yaw_new = yaw_current + input_x × YAW_SENSITIVITY × delta
```

| Variable | Description | Plage |
|----------|-------------|-------|
| `input_x` | Input horizontal brut : `InputEventMouseMotion.relative.x` (souris) ou stick droit axe X | souris : px/frame ; stick : [−1, 1] |
| `YAW_SENSITIVITY_MOUSE` | Sensibilité souris | rad/pixel, défaut : 0.003 |
| `YAW_SENSITIVITY_STICK` | Sensibilité stick | rad/s, défaut : 2.0 |
| `delta` | Temps frame (s) — appliqué uniquement pour le stick | ~0.016 s à 60 FPS |
| `yaw_new` | Yaw résultant, non borné (rotation libre 360°) | ℝ |

**Exemples :**
- Souris : `input_x = 50 px` → `Δyaw = 50 × 0.003 = 0.15 rad ≈ 8.6°`
- Stick : `input_x = 1.0, delta = 0.016 s` → `Δyaw = 1.0 × 2.0 × 0.016 = 0.032 rad ≈ 1.8°/frame`

---

### F2 — Mise à jour du pitch (chaque frame)

```
pitch_raw = pitch_current + input_y × YAW_SENSITIVITY × delta
pitch_new = clamp(pitch_raw, PITCH_MIN_DEG × π/180, PITCH_MAX_DEG × π/180)
```

| Variable | Description | Plage |
|----------|-------------|-------|
| `input_y` | Input vertical brut (même logique que `input_x`) | souris : px/frame ; stick : [−1, 1] |
| `PITCH_MIN_DEG` | Borne basse du pitch (regard vers le bas) | −25°, soit −0.436 rad |
| `PITCH_MAX_DEG` | Borne haute du pitch (regard vers le haut) | +40°, soit +0.698 rad |
| `pitch_new` | Pitch résultant, clampé dur aux bornes | [−0.436, +0.698] rad |

Clamp dur : aucune énergie résiduelle, aucun spring-back au-delà des bornes.

**Exemple :** `pitch_current = −0.40 rad, input_y = −5 px` → `pitch_raw = −0.415 rad` → dans la plage → `pitch_new = −0.415 rad`

---

### F3 — Longueur effective du SpringArm3D

Gérée nativement par Godot. La seule propriété configurée est :

```
spring_arm.spring_length = CAMERA_DISTANCE   # m, défaut : 4.0
```

Godot raccourcit `spring_length` jusqu'à `0` en cas d'obstacle et revient à la valeur nominale quand l'espace est libre. Aucune formule custom requise.

---

### F4 — Signal émis chaque frame

```
camera_yaw_changed.emit(yaw_current)   # float, rad
```

Valeur initiale émise à `_ready()` : `0.0 rad` (joueur face à +Z au spawn).

## Edge Cases

**EC-01 — Input souris pendant pause / menu**
Le jeu capture la souris (`Input.MOUSE_MODE_CAPTURED`). Si un menu s'ouvre (S11), S11 appelle `freeze()` → état FROZEN → tout input ignoré. Aucun traitement spécifique requis dans S10.

**EC-02 — Obstacle entre la caméra et le joueur**
SpringArm3D raccourcit automatiquement. Si `spring_length` atteint 0 (collision extrême), la caméra se superpose au pivot (vue FPS temporaire). Comportement accepté en MVP — aucune logique de compensation n'est ajoutée.

**EC-03 — Objet en vol traversant le rayon SpringArm**
Les objets en vol (S02, layer 3) doivent être exclus du masque de collision du SpringArm. Si le masque inclut layer 3 par erreur, la caméra raccourcit à chaque lancer — bug visuel. **À vérifier au prototype (risque MEDIUM identifié en feasibility check).**

**EC-04 — Pitch au spawn**
Pitch initial : `0.0 rad` (regard horizontal). Si la géométrie de la pièce est basse, le joueur peut ne pas voir le sol immédiatement — accepté, il ajuste manuellement.

**EC-05 — Mort pendant rotation rapide**
`player_died` reçu mid-frame : S10 passe en FROZEN immédiatement, le yaw est figé à la valeur courante. Pas de lerp de sortie, pas de cinématique — gel sec. S11 gère la suite.

**EC-06 — Stick non branché (input nul)**
`input_x = 0`, `input_y = 0` → `Δyaw = 0`, `Δpitch = 0`. Signal `camera_yaw_changed` émis avec la valeur inchangée (Règle 8). Comportement correct, aucun traitement spécial.

**EC-07 — Dépassement de pitch à bas framerate**
À très bas FPS, `delta` grand → `Δpitch` potentiellement plus grand. Le clamp dur (F2) absorbe tout dépassement. Aucun risque d'overshooting au-delà des bornes quelle que soit la durée de frame.

## Dependencies

### Upstream (S10 dépend de)

| Système | Ce que S10 consomme |
|---------|---------------------|
| S01 — Déplacement joueur | Nœud `CharacterBody3D` auquel `CameraPivot` est attaché (dépendance de scène — hiérarchie de nœuds). |
| S07 — Santé joueur | Signal `player_died` → déclenche la transition vers FROZEN. |

### Downstream (dépend de S10)

| Système | Ce que S10 fournit |
|---------|--------------------|
| S01 — Déplacement joueur | Signal `camera_yaw_changed(yaw: float)` — oriente le déplacement relatif à la caméra. |
| S02 — Saisie et lancer | Nœud `CameraPivot` injecté via `@export` — GrabSystem lit `global_rotation.y` pour la direction de lancer. |
| S11 — Game loop | API `freeze()` / `unfreeze()` — S11 contrôle l'état de la caméra sans couplage retour. |

### Dépendances de scène

- `CameraPivot` (Node3D) est enfant direct du nœud racine de la scène Player.
- `SpringArm3D` est enfant de `CameraPivot`.
- `Camera3D` est enfant de `SpringArm3D`.
- Cette hiérarchie est établie dans ADR-0001 (GrabSystem) et ADR-0002 (PlayerBodyType).

## Tuning Knobs

| # | Constante | Défaut | Plage sûre | Effet gameplay |
|---|-----------|--------|------------|----------------|
| 1 | `CAMERA_DISTANCE` | 4.0 m | [2.0, 6.0] | Distance caméra–pivot. Plus petit = vue plus proche, lisibilité ennemis réduite mais feeling plus intense. Plus grand = vue stratégique mais moins immersive. |
| 2 | `CAMERA_PIVOT_HEIGHT` | 1.2 m | [0.8, 1.6] | Hauteur de l'épaule. Trop bas = le sol occupe trop de champ. Trop haut = flottant, décroché du personnage. |
| 3 | `CAMERA_FOV` | 75° | [65°, 90°] | Champ de vision. Étroit = cinématique, mais désavantage de lecture spatiale. Large = lisible mais distorsion en bords. |
| 4 | `PITCH_MIN_DEG` | −25° | [−10°, −45°] | Limite basse du regard (vers le sol). Trop restrictif = frustration si objet au sol proche. Trop permissif = objets proches invisibles derrière la caméra. |
| 5 | `PITCH_MAX_DEG` | +40° | [+20°, +60°] | Limite haute du regard (vers le plafond). Trop restrictif = impossible de voir les objets hauts. Trop permissif = caméra sous le plancher si pivot trop bas. |
| 6 | `YAW_SENSITIVITY_MOUSE` | 0.003 rad/px | [0.001, 0.006] | Vitesse de rotation souris. Trop lent = lourd. Trop rapide = incontrôlable. À exposer dans les options d'accessibilité. |
| 7 | `YAW_SENSITIVITY_STICK` | 2.0 rad/s | [0.5, 4.0] | Vitesse de rotation stick. Trop lent = raideur. Trop rapide = overshooting. À exposer dans les options d'accessibilité, distinct de la sensibilité souris. |

## Visual/Audio Requirements

- **Réticule de visée** : cercle ou croix statique centré, affiché uniquement en état CARRYING. Couleur et taille à définir par l'Art Director (hors scope S10).
- **Pas de son propre à la caméra** : S10 ne déclenche aucun son. Les sons d'ambiance et de réverbération de pièce sont gérés par le système audio (hors scope S10).
- **Pas de post-process spécifique** : S10 n'active aucun effet de caméra (vignette, chromatic aberration, motion blur) en MVP.

## UI Requirements

- **Réticule CARRYING** : élément UI (CanvasLayer) affiché/masqué par S10 selon l'état CARRYING. Centré à l'écran, toujours face caméra, non affecté par le pitch ou le yaw.
- **Options de sensibilité** : `YAW_SENSITIVITY_MOUSE` et `YAW_SENSITIVITY_STICK` doivent être exposées dans le menu Options → Contrôles. Format : slider avec valeur affichée. Hors scope S10 (à designer dans le GDD UI/UX Options).

## Acceptance Criteria

**AC-01** — Le yaw tourne librement à 360° sans limitation ni recadrage automatique.

**AC-02** — Le pitch est bloqué à −25° vers le bas et +40° vers le haut ; aucune valeur hors plage n'est jamais atteinte, quelle que soit la vitesse d'input.

**AC-03** — Le SpringArm raccourcit quand la caméra entre en collision avec un mur et revient à `CAMERA_DISTANCE` quand l'espace est libre. Aucun clip de géométrie visible en gameplay normal.

**AC-04** — Le signal `camera_yaw_changed` est émis à chaque frame, y compris quand le joueur ne touche pas à la caméra. S01 reçoit la valeur correcte et oriente le déplacement en conséquence.

**AC-05** — Quand `player_died` est émis par S07, la caméra se fige immédiatement et ne répond plus à aucun input souris ou stick.

**AC-06** — `freeze()` / `unfreeze()` appelés par S11 font passer S10 en FROZEN / ACTIVE. Après `unfreeze()`, les inputs sont à nouveau traités normalement.

**AC-07** — En état CARRYING (S02), un réticule de visée statique centré est affiché. Il disparaît dès que le joueur lâche l'objet (transition vers EMPTY_HANDS).

**AC-08** — La sensibilité souris (`YAW_SENSITIVITY_MOUSE`) et la sensibilité stick (`YAW_SENSITIVITY_STICK`) sont des constantes distinctes, modifiables sans recompilation.

**AC-09** — Le layer 3 (objets en vol) est exclu du masque de collision du SpringArm3D : un objet lancé passant entre la caméra et le joueur ne provoque pas de raccourcissement du bras.

## Open Questions

**OQ-01** — SpringArm3D + Jolt Physics (layer 3) : vérifier au prototype que les objets en vol n'interfèrent pas avec le masque de collision du SpringArm. Risque MEDIUM identifié en feasibility check. Si problème confirmé, solution : exclure layer 3 du `collision_mask` du SpringArm3D.

**OQ-02** — Sensibilité pitch souris vs. yaw : utiliser la même constante `YAW_SENSITIVITY_MOUSE` pour les deux axes, ou introduire `PITCH_SENSITIVITY_MOUSE` distinct ? À trancher au prototype selon le ressenti (inversion naturelle y attendue par certains joueurs — option d'inversion à prévoir).
