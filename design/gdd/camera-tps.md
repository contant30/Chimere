# S10 — Caméra TPS

> **Statut**: Approuvé
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-10
> **Implémente le Pilier**: Pilier 2 — Le flow avant le challenge

## Vue d'ensemble

S10 — Caméra TPS est le système qui positionne et oriente la vue du joueur dans la pièce. Techniquement, il s'appuie sur un pivot de caméra (`Node3D`) enfant du personnage joueur, dont le yaw/pitch sont contrôlés par l'input souris / stick droit, et dont la distance est gérée par un `SpringArm3D` pour éviter le clipping sur la géométrie statique.

S10 expose un angle horizontal `camera_yaw_radians` (radians) que :
- S01 consomme via un cache local mis à jour au signal (pas besoin d'un signal par frame).
- S02 consomme indirectement : le GrabSystem lit `camera_pivot.global_rotation.y` sur le nœud pivot injecté (ADR-0001).

## Fantasy joueur

Le joueur ne subit pas la caméra — il la dirige. Chaque rotation est un choix de mise en scène : tourner vers l'ennemi qui charge, c'est décider que ce sera le prochain plan d'action ; centrer la caméra sur la table encore intacte au milieu de la dévastation, c'est annoncer son prochain coup. La caméra transforme le brawler en performance : chaque partie est un plan-séquence improvisé dont le joueur est à la fois l'acteur et le cadreur. Le moment cible : la pièce à moitié détruite, deux ennemis qui convergent, une chaise encore debout entre eux. Le joueur tourne lentement la caméra, cadre la scène. Ce n'est plus de la survie — c'est une chorégraphie. L'expression personnelle ne passe pas seulement par le choix de l'objet : elle passe par l'angle depuis lequel on le voit. La caméra est l'outil qui rend chaque partie unique — pas le hasard, mais le regard.

*Pilier servi : Pilier 1 — "Tout est une arme." Le regard lui-même devient un outil tactique. Pilier 2 — "Le flow avant le challenge." Une caméra qui répond instantanément est la condition silencieuse de la fluidité.*

## Conception détaillée

### Règles cœur

1. **Yaw libre** : piloté uniquement par l'input joueur (souris/stick droit). Aucun recadrage automatique, soft-lock, ni Z-targeting en MVP.
2. **Pitch contraint** : plage [`PITCH_MIN_DEG`, `PITCH_MAX_DEG`] (défaut : −25° / +40°). Clamp dur aux bornes, sans spring-back. Pas de roll.
3. **SpringArm3D anti-clipping (géométrie statique uniquement)** :
   - `spring_length = CAMERA_DISTANCE` (défaut : 4.0 m).
   - `collision_mask = 1` (Layer 1 — World, cf. ADR-0002).
   - Conséquence : les objets (layer 3) et les ennemis (layer 4) **ne** raccourcissent **jamais** le bras (pas de jitter caméra).
4. **Pivot à hauteur d'épaule** : `CameraPivot` à `CAMERA_PIVOT_HEIGHT` (défaut : 1.2 m) au-dessus de la base du `CharacterBody3D`. Fixe en MVP.
5. **FOV fixe** : `CAMERA_FOV` (défaut : 75°), constant, non animé en MVP.
6. **Gel / dégel** :
   - S10 expose `freeze()` / `unfreeze()` ; ces appels sont **idempotents**.
   - S10 **ne** s'abonne **pas** à `player_died`. Sur mort, S07 → S11, puis S11 appelle `freeze()` sur S10 (contrat S11).
   - En état gelé : aucun input caméra, aucune mise à jour yaw/pitch, aucun signal émis.
7. **Contrat `camera_yaw_changed` (sémantique “changed”, testable)** :
   - `signal camera_yaw_changed(yaw_radians: float)` (radians).
   - Émis une première fois à `_ready()` avec `camera_yaw_radians` initial (défaut : `0.0`).
   - Émis ensuite **uniquement** quand `abs(yaw_new - yaw_old) >= YAW_SIGNAL_EPSILON_RAD`.
   - Jamais émis en état gelé.

### États et transitions

| État | Condition d'entrée | Condition de sortie | Comportement |
|------|--------------------|---------------------|--------------|
| ACTIVE | `_ready()` / `unfreeze()` | `freeze()` appelé | Yaw + pitch mis à jour, `camera_yaw_changed` émis uniquement sur changement, SpringArm actif |
| FROZEN | `freeze()` appelé (par S11) | `unfreeze()` appelé (par S11) | Aucun input traité, aucune mise à jour yaw/pitch, aucun signal émis |

### Interactions avec les autres systèmes

| Système | Direction | Interface |
|---------|-----------|-----------|
| S01 — Déplacement joueur | S10 → S01 | S01 se connecte à `camera_yaw_changed(yaw_radians)` et met en cache un yaw local (défaut `0.0` si jamais connecté). |
| S02 — Saisie et lancer | S10 → S02 | Le GrabSystem lit `camera_pivot.global_rotation.y` directement sur le nœud `CameraPivot` injecté via `@export` (ADR-0001). |
| S11 — Gestionnaire d'état | S11 → S10 | S11 appelle `freeze()` / `unfreeze()` (ex : S07 émet `player_died` → S11 passe GAME_OVER → freeze). S10 n'a aucune référence sur S11. |

## Formules

### F1 — Mise à jour du yaw (souris / stick)

```
# Souris (événement) :
yaw_new = yaw_current + (-mouse_dx_px) * YAW_SENSITIVITY_MOUSE

# Stick (par frame) :
yaw_new = yaw_current + stick_x * YAW_SENSITIVITY_STICK * delta
```

| Variable | Description | Plage |
|----------|-------------|-------|
| `mouse_dx_px` | `InputEventMouseMotion.relative.x` | px/événement |
| `stick_x` | Axe X stick droit | [−1, 1] |
| `YAW_SENSITIVITY_MOUSE` | Sensibilité yaw souris | rad/pixel, défaut : 0.003 |
| `YAW_SENSITIVITY_STICK` | Sensibilité yaw stick | rad/s, défaut : 2.0 |
| `delta` | Temps frame (s) — appliqué uniquement pour le stick | ~0.016 s à 60 FPS |
| `yaw_new` | Yaw résultant, non borné (rotation libre 360°) | ℝ |

**Exemples :**
- Souris : `mouse_dx_px = 50 px` → `Δyaw = 50 × 0.003 = 0.15 rad ≈ 8.6°`
- Stick : `stick_x = 1.0, delta = 0.016 s` → `Δyaw = 1.0 × 2.0 × 0.016 = 0.032 rad ≈ 1.8°/frame`

---

### F2 — Mise à jour du pitch (souris / stick)

```
pitch_raw =
  pitch_current
  + (-mouse_dy_px) * PITCH_SENSITIVITY_MOUSE
  + stick_y * PITCH_SENSITIVITY_STICK * delta

pitch_new = clamp(pitch_raw, PITCH_MIN_DEG × π/180, PITCH_MAX_DEG × π/180)
```

| Variable | Description | Plage |
|----------|-------------|-------|
| `mouse_dy_px` | `InputEventMouseMotion.relative.y` | px/événement |
| `stick_y` | Axe Y stick droit | [−1, 1] |
| `PITCH_SENSITIVITY_MOUSE` | Sensibilité pitch souris | rad/pixel, défaut : 0.003 (MVP = yaw) |
| `PITCH_SENSITIVITY_STICK` | Sensibilité pitch stick | rad/s, défaut : 2.0 (MVP = yaw) |
| `PITCH_MIN_DEG` | Borne basse du pitch (regard vers le bas) | −25°, soit −0.436 rad |
| `PITCH_MAX_DEG` | Borne haute du pitch (regard vers le haut) | +40°, soit +0.698 rad |
| `pitch_new` | Pitch résultant, clampé dur aux bornes | [−0.436, +0.698] rad |

Clamp dur : aucune énergie résiduelle, aucun spring-back au-delà des bornes.

**Exemple :** `pitch_current = −0.40 rad, input_y = −5 px` → `pitch_raw = −0.415 rad` → dans la plage → `pitch_new = −0.415 rad`

---

### F3 — Configuration du SpringArm3D

Gérée nativement par Godot. Les propriétés configurées pour le MVP :

```
spring_arm.spring_length = CAMERA_DISTANCE   # m, défaut : 4.0
spring_arm.collision_mask = 1                # layer 1 uniquement (World), cf. ADR-0002
```

Godot raccourcit la longueur effective en cas d'obstacle et revient à la valeur nominale quand l'espace est libre. Aucune formule custom requise.

---

### F4 — Émission de `camera_yaw_changed` (sur changement)

```
if abs(yaw_new - yaw_old) >= YAW_SIGNAL_EPSILON_RAD:
  camera_yaw_changed.emit(yaw_new)   # float, rad
```

Valeur initiale émise à `_ready()` : `0.0 rad` (joueur face à +Z au spawn).

## Cas limites

**EC-01 — Input souris pendant pause / menu**
Le jeu capture la souris (`Input.MOUSE_MODE_CAPTURED`). Si un menu s'ouvre, S11 appelle `freeze()` → état FROZEN → tout input caméra ignoré.

**EC-02 — Obstacle statique entre la caméra et le joueur**
Le SpringArm raccourcit automatiquement. Si la longueur effective atteint 0 (collision extrême), la caméra se superpose au pivot (vue FPS temporaire). Comportement accepté en MVP.

**EC-03 — Objet en vol traversant le rayon du SpringArm**
Les objets (layer 3) et ennemis (layer 4) ne sont pas dans le `collision_mask` (Règle 3). Un objet lancé entre la caméra et le pivot ne doit donc jamais raccourcir le bras.

**EC-04 — Pitch au spawn**
Pitch initial : `0.0 rad` (regard horizontal). Si la géométrie de la pièce est basse, le joueur peut ne pas voir le sol immédiatement — accepté, il ajuste manuellement.

**EC-05 — Freeze pendant rotation rapide**
`freeze()` appelé mid-frame : S10 passe en FROZEN immédiatement, le yaw/pitch sont figés à la valeur courante. Pas de cinématique — gel sec. S11 gère la suite.

**EC-06 — Input nul**
`Δyaw = 0`, `Δpitch = 0` → aucun signal n'est émis (Règle 7), mais les valeurs internes restent valides.

**EC-07 — Dépassement de pitch à bas framerate**
À très bas FPS, `delta` grand → `Δpitch` potentiellement plus grand. Le clamp dur (F2) absorbe tout dépassement. Aucun risque d'overshooting au-delà des bornes quelle que soit la durée de frame.

## Dépendances

### Amont (S10 dépend de)

| Système | Ce que S10 consomme |
|---------|---------------------|
| S01 — Déplacement joueur | Nœud `CharacterBody3D` auquel `CameraPivot` est attaché (dépendance de scène — hiérarchie de nœuds). |
| ADR-0002 | Schéma de layers de collision (World=layer 1) pour configurer le SpringArm (`collision_mask = 1`). |

### Aval (dépend de S10)

| Système | Ce que S10 fournit |
|---------|--------------------|
| S01 — Déplacement joueur | Signal `camera_yaw_changed(yaw_radians: float)` — S01 met en cache la dernière valeur reçue. |
| S02 — Saisie et lancer | Nœud `CameraPivot` injecté via `@export` — le GrabSystem lit `global_rotation.y` pour la direction de lancer (ADR-0001). |
| S11 — Gestionnaire d'état | API `freeze()` / `unfreeze()` — S11 contrôle l'état de la caméra sans couplage retour. |

### Note S07 (dépendance transitive)

S07 n'est pas une dépendance directe de S10 : S07 émet `player_died` vers S11, et S11 orchestre ensuite le gel via `freeze()`.

### Dépendances de scène

- `CameraPivot` (Node3D) est enfant direct du nœud racine de la scène Player.
- `SpringArm3D` est enfant de `CameraPivot`.
- `Camera3D` est enfant de `SpringArm3D`.
- Cette hiérarchie est cohérente avec ADR-0001 (injection `camera_pivot`) et ADR-0002 (layers).

## Paramètres de tuning

| # | Constante | Défaut | Plage sûre | Effet gameplay |
|---|-----------|--------|------------|----------------|
| 1 | `CAMERA_DISTANCE` | 4.0 m | [2.0, 6.0] | Distance caméra–pivot. Plus petit = vue plus proche, lisibilité ennemis réduite mais feeling plus intense. Plus grand = vue stratégique mais moins immersive. |
| 2 | `CAMERA_PIVOT_HEIGHT` | 1.2 m | [0.8, 1.6] | Hauteur de l'épaule. Trop bas = le sol occupe trop de champ. Trop haut = flottant, décroché du personnage. |
| 3 | `CAMERA_FOV` | 75° | [65°, 90°] | Champ de vision. Étroit = cinématique, mais désavantage de lecture spatiale. Large = lisible mais distorsion en bords. |
| 4 | `PITCH_MIN_DEG` | −25° | [−10°, −45°] | Limite basse du regard (vers le sol). Trop restrictif = frustration si objet au sol proche. Trop permissif = objets proches invisibles derrière la caméra. |
| 5 | `PITCH_MAX_DEG` | +40° | [+20°, +60°] | Limite haute du regard (vers le plafond). Trop restrictif = impossible de voir les objets hauts. Trop permissif = caméra sous le plancher si pivot trop bas. |
| 6 | `YAW_SENSITIVITY_MOUSE` | 0.003 rad/px | [0.001, 0.006] | Vitesse de rotation souris. Trop lent = lourd. Trop rapide = incontrôlable. À exposer dans les options d'accessibilité. |
| 7 | `YAW_SENSITIVITY_STICK` | 2.0 rad/s | [0.5, 4.0] | Vitesse de rotation stick. Trop lent = raideur. Trop rapide = overshooting. À exposer dans les options d'accessibilité, distinct de la sensibilité souris. |
| 8 | `PITCH_SENSITIVITY_MOUSE` | 0.003 rad/px | [0.001, 0.006] | En MVP, identique à `YAW_SENSITIVITY_MOUSE` (simplicité). Peut diverger en V1.0 selon le ressenti. |
| 9 | `PITCH_SENSITIVITY_STICK` | 2.0 rad/s | [0.5, 4.0] | En MVP, identique à `YAW_SENSITIVITY_STICK`. |
| 10 | `YAW_SIGNAL_EPSILON_RAD` | 0.0001 rad | [0.00001, 0.001] | Seuil minimal de changement avant émission de `camera_yaw_changed` (évite le bruit numérique). |

## Exigences visuelles / audio

Aucune : S10 ne déclenche aucun son ni VFX et n'applique aucun post-process en MVP.

## Exigences UI

Aucune UI propre : le réticule et les options de contrôles appartiennent au HUD/Options (S13 / UX). S10 ne contient pas de logique de `CanvasLayer`.

## Critères d'acceptation

| # | Critère | Vérification |
|---|--------|--------------|
| AC-S10-01 | Yaw 360° libre | Manuel : tourner en continu, aucune limite ni recadrage. |
| AC-S10-02 | Pitch clamp | Test (GUT) : envoyer un input extrême, vérifier `pitch ∈ [min,max]` strictement. |
| AC-S10-03 | SpringArm anti-clipping sur World uniquement | Intégration : mur (layer 1) entre pivot et caméra → bras raccourcit ; objet (layer 3) entre pivot et caméra → pas de raccourcissement. |
| AC-S10-04 | Contrat `camera_yaw_changed` | Test (GUT) : émission à `_ready()` puis émission uniquement quand `abs(Δyaw) >= epsilon` ; aucune émission en FROZEN. |
| AC-S10-05 | `freeze()` / `unfreeze()` | Test (GUT) : freeze stoppe l'évolution yaw/pitch ; unfreeze reprend ; appels multiples sans effet secondaire. |
| AC-S10-06 | Sensibilités distinctes par device | Test (config) : `*_MOUSE` et `*_STICK` sont des constantes séparées, modifiables via settings/projet sans changement de code. |

## Questions ouvertes

**OQ-S10-01** — Inversion axe Y (pitch) : exposer une option “Inverser Y” dans les contrôles (hors scope S10), ou fixer une convention MVP ?

**OQ-S10-02** — Sensibilités yaw vs pitch : le MVP utilise des valeurs identiques pour simplicité (Knobs 6–9). Valider au prototype si pitch doit être plus lent/rapide (sinon divergence V1.0).
