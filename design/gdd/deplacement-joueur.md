# S01 — Déplacement joueur

> **Statut**: Approuvé
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-10
> **Implémente le Pilier**: Pilier 2 — Le flow avant le challenge

## Overview

S01 — Déplacement joueur est le système de mouvement du personnage joueur dans la pièce. Il gère le déplacement libre en 3D (8 directions), l'accélération, la décélération et la gestion des collisions avec l'environnement et les objets physiques. Techniquement, il s'appuie sur un `CharacterBody3D` cinématique avec `move_and_slide()` — entièrement indépendant de la simulation physique Jolt des objets, ce qui garantit un contrôle prévisible même en présence de nombreux corps rigides actifs. Pour le joueur, ce système est le socle de toute improvisation : se repositionner pour saisir l'objet suivant, rompre l'angle d'attaque d'un ennemi, survivre à un débordement en retraite rapide. Un déplacement fluide et réactif est la condition silencieuse de la fantasy du jeu.

## Player Fantasy

Le joueur ne pense jamais à ses jambes. Il pense à la chaise dans le coin, à l'ennemi qui approche par la gauche, à l'objet qu'il vient de lancer. Le déplacement est invisible parce qu'il est parfaitement réactif — à tout moment, le joueur peut pivoter, reculer, contourner sans friction. La fantasy n'est pas "je me déplace bien" : c'est *"je suis toujours au bon endroit"*. Comme un personnage de film d'action qui n'hésite jamais — qui n'est jamais coincé dans un angle mort, jamais trop loin du prochain objet, jamais pris par surprise parce qu'il n'a pas pu se retourner assez vite. Le déplacement est la condition silencieuse de l'improvisation fluide.

## Detailed Design

### Core Rules

1. **Déplacement 8 directions** : Le joueur se déplace dans les 8 directions cardinales et diagonales via les inputs WASD / stick analogique gauche. Les diagonales utilisent la longueur du vecteur d'input clamped à 1.0 (`input_vec.limit_length(1.0)`).
2. **Orientation vers la caméra** : Le personnage fait toujours face à la direction horizontale de la caméra (yaw). Le déplacement latéral (strafe) et arrière sont possibles sans rotation du personnage. La direction de la caméra est fournie par S10.
3. **Vitesse unique** : Une seule vitesse de déplacement au sol — pas de marche/sprint. Le personnage est toujours en mouvement "rapide" pour maintenir le rythme. *Risque prototype #2 : valider que la vitesse unique ne génère pas de survitesse incontrôlable lors d'interactions S02 (voir OQ-03). Si nécessaire, une solution de grab-assist appartient à S02, pas à S01.*
4. **Accélération / Décélération** : Le déplacement utilise une accélération linéaire à l'entrée et une décélération par friction à la sortie. Le personnage s'arrête nettement — pas d'inertie persistante. Valeurs tunables (voir Tuning Knobs).
5. **Saut simple + coyote time** : Le joueur peut sauter une fois depuis le sol (espace / bouton A gamepad). Fonction utilitaire uniquement — passer par-dessus des objets renversés. Pas de double-saut. Le saut applique une vélocité verticale instantanée ; la gravité gère la descente. **Coyote time :** si le joueur quitte un rebord sans sauter, une fenêtre de `COYOTE_FRAMES` (4–6 frames, ~83–100 ms à 60 fps) permet quand même de déclencher le saut. Passé ce délai, le saut est refusé.
6. **Gravité** : La gravité est appliquée manuellement chaque frame (`velocity.y -= GRAVITY * delta`) pour contrôle total. La valeur par défaut provient de `ProjectSettings.get("physics/3d/default_gravity")`.
7. **Collision avec objets physiques** : Le joueur ne pousse pas les `RigidBody3D` Jolt en marchant — il les contourne ou les enjambe (saut). Contrat comportemental : le joueur ne doit pas déplacer les corps rigides par collision passive. La configuration précise des layers de collision est définie dans l'ADR OQ-04. L'interaction intentionnelle avec les objets est responsabilité de S02.
8. **Aucune pente** : La pièce est plate. `floor_max_angle` reste à la valeur Godot par défaut (45°) pour gérer les micro-inclinaisons des débris.
9. **Interaction S02 en état AIRBORNE** : Le joueur peut déclencher la saisie ou le lancer (S02) pendant l'état AIRBORNE. S01 expose `global_position` et `velocity` à S02 quel que soit l'état courant. La direction de lancer utilise le yaw caméra (S10), pas le vecteur de vélocité courante.

### States and Transitions

| État | Condition d'entrée | Condition de sortie | Comportement |
|------|-------------------|---------------------|--------------|
| **IDLE** | Aucun input de déplacement, `is_on_floor()` | Input de déplacement détecté / saut | Personnage immobile, friction maximale |
| **MOVING** | Input de déplacement, `is_on_floor()` | Input relâché / saut / chute | Déplacement à `MOVE_SPEED`, accélération appliquée |
| **AIRBORNE** | `!is_on_floor()` (saut, chute d'un rebord, ou coyote time expiré) | `is_on_floor()` (atterrissage) | Gravité appliquée, accélération réduite (`ACCELERATION × AIR_CONTROL`), friction pleine en l'air |

*Note : Il n'y a pas d'état "MORT" dans S01. La mort est gérée par S07 ; S07 émet `player_died`, S01 écoute ce signal et désactive le traitement des inputs.*

### Interactions with Other Systems

| Système | Direction | Interface |
|---------|-----------|-----------|
| **S10 — Caméra TPS** | S10 → S01 | S10 fournit la direction horizontale (yaw) de la caméra. S01 l'utilise pour orienter les inputs de déplacement dans l'espace monde. **Contrat d'initialisation :** S01 ne traite pas les inputs de déplacement avant d'avoir reçu au moins une valeur de yaw de S10. Valeur de repli : `0.0` (sécurité uniquement). |
| **S02 — Saisie et lancer** | S01 → S02 | S01 expose `global_position` et `velocity` du joueur — utilisées par S02 pour calculer l'origine et l'impulsion du lancer. **Contrat AIRBORNE :** S02 peut être déclenché en état AIRBORNE ; la direction de lancer est toujours dérivée du yaw caméra (S10), jamais du vecteur `velocity`. |
| **S07 — Santé joueur** | S07 → S01 | S07 émet `player_died` ; S01 écoute ce signal et désactive les inputs de déplacement. |
| **S09 — IA ennemie** | S01 → S09 | S09 lit `player.global_position` pour la navigation vers le joueur. Exposition automatique via le nœud. |

## Formulas

### F1 — Vecteur de déplacement monde

Le vecteur d'input 2D est converti en direction 3D orientée par le yaw de la caméra.

```gdscript
input_vec = Vector2(Input.get_axis("move_left", "move_right"),
                    Input.get_axis("move_forward", "move_back"))
input_vec = input_vec.limit_length(1.0)

cam_yaw_basis = Basis(Vector3.UP, camera_yaw_radians)
direction = cam_yaw_basis * Vector3(input_vec.x, 0, input_vec.y)
```

**Variables :**

| Variable | Symbole | Type | Plage | Description |
|----------|---------|------|-------|-------------|
| Input horizontal | `input_vec.x` | float | −1.0 à 1.0 | Axe gauche/droite |
| Input vertical | `input_vec.y` | float | −1.0 à 1.0 | Axe avant/arrière |
| Yaw caméra | `camera_yaw_radians` | float | −π à π | Rotation horizontale fournie par S10 |
| Direction monde | `direction` | Vector3 | magnitude 0.0–1.0 | Direction normalisée en espace monde |

**Output :** Vector3 normalisé (magnitude 0.0 = immobile, 1.0 = pleine vitesse), composante Y toujours 0.

---

### F2 — Application de la vélocité (par frame)

```gdscript
# Coyote time — reset au sol, décompte dans le vide
if is_on_floor():
    coyote_timer = COYOTE_FRAMES
elif coyote_timer > 0:
    coyote_timer -= 1

# Saut (avant gravité — évite un artefact Jolt d'une frame)
var can_jump := is_on_floor() or coyote_timer > 0
if Input.is_action_just_pressed("jump") and can_jump:
    velocity.y = JUMP_VELOCITY
    coyote_timer = 0  # consommer le coyote time immédiatement

# Gravité
if not is_on_floor():
    velocity.y -= GRAVITY * delta

# Déplacement horizontal
var accel := ACCELERATION if is_on_floor() else ACCELERATION * AIR_CONTROL
if direction.length() > 0.0:
    velocity.x = move_toward(velocity.x, direction.x * MOVE_SPEED, accel * delta)
    velocity.z = move_toward(velocity.z, direction.z * MOVE_SPEED, accel * delta)
else:
    velocity.x = move_toward(velocity.x, 0.0, FRICTION * delta)
    velocity.z = move_toward(velocity.z, 0.0, FRICTION * delta)

move_and_slide()
```

**Variables :**

| Variable | Symbole | Type | Plage | Description |
|----------|---------|------|-------|-------------|
| Vitesse max | `MOVE_SPEED` | float | 3.0–8.0 m/s | Vitesse cible au sol (voir Tuning Knobs) |
| Accélération | `ACCELERATION` | float | 10.0–40.0 m/s² | Taux de montée en vitesse |
| Friction | `FRICTION` | float | 17.5–50.0 m/s² | Taux de décélération. Contrainte de couplage : `FRICTION ≥ MOVE_SPEED / 18` (garantit l'arrêt en ≤ 0.3 s à toute vitesse dans la plage). La friction n'est PAS réduite en l'air. |
| Gravité | `GRAVITY` | float | 9.8 m/s² | Valeur projet par défaut (Jolt) |
| Vélocité saut | `JUMP_VELOCITY` | float | 3.0–6.0 m/s | Impulsion verticale initiale |
| Contrôle aérien | `AIR_CONTROL` | float | 0.0–1.0 | Multiplicateur sur ACCELERATION en l'air uniquement |
| Coyote frames | `COYOTE_FRAMES` | int | 4–6 frames | Fenêtre de saut après avoir quitté un rebord sans sauter |

**Output :** `velocity` appliqué via `move_and_slide()`. La position résultante est exposée via `global_position`.

**Exemple :** `MOVE_SPEED=5.0`, input plein avant, `ACCELERATION=35.0`, `delta=0.016` :
`velocity.z = move_toward(0, -5.0, 35.0 × 0.016) = -0.56 m/s` (première frame — pleine vitesse atteinte en ~0.14 s)

---

### F3 — Hauteur de saut (co-calibration JUMP_VELOCITY / GRAVITY)

```
h_max = JUMP_VELOCITY² / (2 × GRAVITY)
```

**Exemple :** `JUMP_VELOCITY=4.5`, `GRAVITY=9.8` → `h_max = 4.5² / (2 × 9.8) = 20.25 / 19.6 ≈ 1.03 m`

Modifier l'un sans recalibrer l'autre produit une hauteur de saut inattendue. Utiliser cette formule pour vérifier que la hauteur couvre les objets renversés les plus hauts (~0.8–1.0 m).

---

### F4 — Volume sonore atterrissage

Volume normalisé basé sur la vélocité verticale d'impact.

```gdscript
var landing_volume := clamp(
    (abs(velocity_at_impact.y) - LANDING_SOUND_MIN) / (LANDING_SOUND_MAX - LANDING_SOUND_MIN),
    0.0, 1.0
)
```

**Variables :**

| Variable | Symbole | Type | Plage MVP | Description |
|----------|---------|------|-----------|-------------|
| Vélocité d'impact | `velocity_at_impact.y` | float | 0.0–20.0 m/s | Composante Y négative à l'atterrissage (valeur absolue utilisée) |
| Seuil bas | `LANDING_SOUND_MIN` | float | 1.0 m/s | En dessous : son silencieux |
| Seuil haut | `LANDING_SOUND_MAX` | float | 8.0 m/s | Au-dessus : volume maximal (1.0) |

**Exemple :** chute libre depuis h=1.03 m → `velocity_at_impact.y ≈ 4.5 m/s` → `landing_volume = (4.5 - 1.0) / (8.0 - 1.0) ≈ 0.50`

## Edge Cases

- **Si le joueur appuie sur Saut en étant AIRBORNE (coyote time expiré)** : l'input est ignoré. `is_on_floor()` est false et `coyote_timer == 0` — la condition de saut n'est pas remplie, aucune vélocité n'est ajoutée. Pas de double-saut.
- **Si le joueur saute pendant la fenêtre coyote time** : `coyote_timer > 0` et `!is_on_floor()` — le saut est autorisé, `coyote_timer` est immédiatement mis à 0 pour empêcher un second saut dans la même chute.
- **Si le joueur tombe d'un rebord** (transition MOVING → AIRBORNE sans saut) : `coyote_timer` commence à décrémenter depuis `COYOTE_FRAMES`. La gravité s'applique dès la première frame hors sol.
- **Si le joueur est coincé entre un `RigidBody3D` Jolt et un mur** : `move_and_slide()` résout la collision — le joueur glisse le long de la surface la plus proche. Le joueur ne pousse pas activement les objets physiques.
- **Si le joueur est mort (`player_died` reçu)** : S01 désactive le traitement des inputs et gèle `velocity` à `Vector3.ZERO`. Le personnage reste à sa position, la physique Jolt continue sur les objets environnants.
- **Si le vecteur d'input est exactement (0, 0)** : `direction.length() == 0.0` — la branche friction est prise, `velocity.x` et `velocity.z` convergent vers 0 via `move_toward`. Pas de division par zéro.
- **Si `camera_yaw_radians` n'est pas encore fourni par S10** (initialisation) : S01 n'applique pas d'inputs de déplacement jusqu'à la première mise à jour de S10 (frame 1 en conditions normales). Le yaw reste à `0.0` en attente.
- **Si `GRAVITY` est 0** (valeur projet invalide) : le joueur flotte après un saut. Non géré dans S01 — configuration projet incorrecte, à détecter en QA via AC-S01-07.
- **Si `FRICTION` < `MOVE_SPEED / 18`** (violation de la contrainte de couplage) : la distance de freinage dépasse 0.3 s à vitesse max — AC-S01-04 échoue. Respecter `FRICTION ≥ MOVE_SPEED / 18` lors du tuning.

## Dependencies

### Dépendances amont (ce dont S01 a besoin)

| Système | Nature | Interface attendue |
|---------|--------|--------------------|
| **S10 — Caméra TPS** | Soft (S01 fonctionne sans S10 avec yaw=0.0) | S10 expose `camera_yaw_radians: float` mis à jour chaque frame |

### Dépendances aval (systèmes qui dépendent de S01)

| Système | Nature | Ce qu'ils consomment |
|---------|--------|----------------------|
| **S02 — Saisie et lancer** | Hard | `global_position: Vector3`, `velocity: Vector3` — accessibles en tout état (y compris AIRBORNE) |
| **S09 — IA ennemie** | Hard | `global_position: Vector3` (cible de navigation) |
| **S10 — Caméra TPS** | Hard | Nœud joueur (`CharacterBody3D`) à suivre |
| **S07 — Santé joueur** | Hard | S07 est monté sur le même nœud joueur ; émet `player_died` sur lequel S01 est abonné |
| **S13 — HUD** | Soft | Position joueur (optionnel, indicateur d'objet tenu) |

*Note : S02, S09, S10 ne peuvent pas fonctionner sans S01 — dépendances hard. S07 partage le nœud joueur et n'est pas une dépendance directe de S01 — c'est S01 qui écoute S07.*

## Tuning Knobs

| Knob | Variable | Valeur MVP | Plage sûre | Trop haut | Trop bas | Note |
|------|----------|-----------|------------|-----------|----------|------|
| Vitesse de déplacement | `MOVE_SPEED` | 5.0 m/s | 3.0–8.0 | Traverse la pièce trop vite, difficile de cibler | Le joueur se sent lent et engourdi | Point de départ : pièce ~10×10 m, traversée en ~2 s |
| Accélération | `ACCELERATION` | 35.0 m/s² | 10.0–40.0 | Départ immédiat — perd la sensation de poids | Démarrage mou, latence perçue | Pleine vitesse en ~0.14 s avec MVP. Interagit avec AIR_CONTROL. |
| Friction (décélération) | `FRICTION` | 25.0 m/s² | 17.5–50.0 | Arrêt brutal | Glissement, perte de précision | Contrainte : `FRICTION ≥ MOVE_SPEED / 18`. FRICTION > ACCELERATION recommandé pour arrêt net. |
| Vélocité de saut | `JUMP_VELOCITY` | 4.5 m/s | 3.0–6.0 | Sauts excessivement hauts | Saut trop bas, ne passe pas les objets | Co-calibrer avec GRAVITY via F3 : `h = JUMP_VELOCITY² / (2 × GRAVITY)` |
| Gravité | `GRAVITY` | 9.8 m/s² | 9.8–20.0 | Chute très violente | Le joueur flotte | Valeur projet par défaut Jolt. Co-calibrer avec JUMP_VELOCITY. |
| Contrôle aérien | `AIR_CONTROL` | 0.35 | 0.0–1.0 | Plein contrôle aérien (pas de poids) | Aucun contrôle (trop rigide) | Multiplicateur sur ACCELERATION uniquement. FRICTION non réduite en l'air. |
| Coyote frames | `COYOTE_FRAMES` | 5 frames | 4–6 frames | Saut "magique" perçu dans le vide | Fenêtre trop courte, coyote time inutile | ~83–100 ms à 60 fps |
| Seuil son atterrissage bas | `LANDING_SOUND_MIN` | 1.0 m/s | 0.5–2.0 | Son joue trop facilement | Atterrissages légers silencieux inattendus | Voir F4 |
| Seuil son atterrissage haut | `LANDING_SOUND_MAX` | 8.0 m/s | 5.0–15.0 | Volume max difficile à atteindre | Volume maximal atteint trop tôt | Voir F4 |

*Interactions : augmenter `MOVE_SPEED` sans augmenter `FRICTION` allonge la distance de freinage (contrainte : `FRICTION ≥ MOVE_SPEED / 18`). Augmenter `GRAVITY` sans augmenter `JUMP_VELOCITY` raccourcit la hauteur de saut (voir F3).*

## Visual/Audio Requirements

**Visual :**
- Animation de déplacement : cycle de run fluide (vitesse unique — pas d'animation marche séparée). Strafes gauche/droite et arrière avec inclinaison légère du torse.
- Animation idle : posture de vigilance active — personnage prêt à bondir, jamais au repos total.
- Animation de saut : phase atterrissage (absorption au sol). Phase décollage (accroupi bref 1–2 frames) et phase apogée (corps tendu) sont **cosmétiques uniquement** — elles n'affectent pas la vélocité et ne bloquent pas le saut.
- Pas d'animation de mort dans S01 — responsabilité de S07.

**Audio :**
- Sons de pas au sol, déclenchés par S01 à chaque foulée. Deux variantes : sol lisse / débris (état S04).
- Son d'atterrissage après saut. Volume calculé via F4 (paramètres `LANDING_SOUND_MIN`, `LANDING_SOUND_MAX`).
- Aucun son de saut ou de déplacement en état AIRBORNE.

*📌 Ces spécifications sont des intentions de design. Les assets détaillés sont produits via `/asset-spec system:deplacement-joueur` après approbation de l'art bible.*

## UI Requirements

S01 n'a pas d'interface utilisateur propre. La position du joueur est consommée indirectement par S13 (HUD) pour l'indicateur d'objet tenu.

## Acceptance Criteria

| # | AC | Condition | Résultat attendu |
|---|-----|-----------|-----------------|
| AC-S01-01 | Déplacement 8 directions | GIVEN le joueur en IDLE, WHEN chacun des 6 inputs suivants à fond : diagonale avant-droite, avant-gauche, arrière-droite, arrière-gauche, arrière seul, strafe gauche seul, THEN le personnage se déplace dans la direction correcte et `velocity.xz.length()` ≤ `MOVE_SPEED` | Test GUT paramétré : 6 scenarios, vérifier `velocity.normalized()` · `direction_attendue` ≥ 0.99 |
| AC-S01-02 | Orientation vers caméra | GIVEN la caméra pointant à yaw=π/2 (90°), WHEN input "avant" pressé, THEN le personnage se déplace à 90° de l'axe monde Z | Test GUT : appliquer `camera_yaw_radians=PI/2`, input (0,−1), vérifier `direction.x` ≈ 1.0 ± 0.01 |
| AC-S01-03 | Accélération mesurable | GIVEN IDLE, input plein avant, WHEN 0.25 s s'écoule, THEN `velocity.length()` > 0.0 et < `MOVE_SPEED` (accélération en cours). WHEN 1.0 s s'écoule, THEN `velocity.length()` ≈ `MOVE_SPEED` (±0.1) | Test GUT chronométré : vérifier la valeur à t=0.25 s puis t=1.0 s |
| AC-S01-04 | Arrêt net | GIVEN MOVING à pleine vitesse, WHEN input relâché, THEN `velocity.xz` atteint (0,0) en moins de 0.3 s (FRICTION=25) | Test GUT : compter les frames jusqu'à `velocity.length() < 0.01` |
| AC-S01-05 | Saut depuis le sol | GIVEN IDLE ou MOVING, `is_on_floor()` true, WHEN touche Saut pressée, THEN `velocity.y` = `JUMP_VELOCITY` (valeur configurée), état passe à AIRBORNE | Test GUT : vérifier `velocity.y == JUMP_VELOCITY` à la frame suivante |
| AC-S01-06 | Pas de double-saut | GIVEN AIRBORNE (coyote time expiré, `coyote_timer == 0`), WHEN touche Saut pressée, THEN aucune vélocité supplémentaire — `velocity.y` frame N+1 < `velocity.y` frame N | Test GUT : vérifier `velocity.y` décroît après tentative de saut en AIRBORNE |
| AC-S01-07 | Gravité appliquée | GIVEN AIRBORNE après saut, WHEN 0.5 s s'écoule, THEN `velocity.y` < 0 (descente confirmée) | Test GUT : simuler 30 frames, vérifier `velocity.y < 0` |
| AC-S01-08 | Désactivation à la mort | GIVEN mort (`player_died` émis), WHEN input de déplacement envoyé, THEN `velocity` reste à `Vector3.ZERO` | Test GUT : émettre signal, appliquer input, vérifier `velocity == Vector3.ZERO` |
| AC-S01-09 | Collision glissante | GIVEN un `RigidBody3D` contre un mur, WHEN joueur se déplace vers eux, THEN `move_and_slide()` fait glisser le joueur — pas de blocage complet | Test de scène de collision (intégration) |
| AC-S01-10 | Stabilité sans input | GIVEN aucun input, WHEN 600 frames s'exécutent (10 s), THEN aucune erreur GDScript et `velocity.xz.length() < 0.01` | Test GUT automatisé : 600 frames, assert `get_error_count() == 0` et `velocity.length() < 0.01` |
| AC-S01-11 | Contrôle aérien réduit | GIVEN état AIRBORNE (coyote time expiré), WHEN input plein avant pendant 1 frame, THEN `delta_velocity.x` mesurée ≈ `ACCELERATION × AIR_CONTROL × delta` (±5 %) — strictement inférieure à l'accélération au sol | Test GUT : mesurer `delta_velocity.x` sur 1 frame en AIRBORNE vs au sol, vérifier ratio ≈ `AIR_CONTROL` ± 0.05 |

## Open Questions

| # | Question | Owner | Statut | Décision |
|---|----------|-------|--------|----------|
| OQ-01 | Coyote time ? | Design | **FERMÉ** | **OUI** — `COYOTE_FRAMES` = 4–6 frames (~83–100 ms à 60 fps). Intégré dans F2, Detailed Rules et Tuning Knobs. |
| OQ-02 | Son de pas : déclenchement par timer ou par événement d'animation (footstep IK) ? | Technique | Ouvert | Décision requise avant implémentation S14 |
| OQ-03 | Taille de pièce ~10×10 m — `MOVE_SPEED=5.0` traverse en ~2 s. **Risque prototype #1** : valider la taille au prototype. **Risque prototype #2** (vitesse unique) : valider que la vitesse unique ne génère pas de survitesse incontrôlable lors d'interactions S02. Si nécessaire, solution de grab-assist côté S02, pas S01. | Design | Ouvert | Décision requise avant implémentation S01 |
| OQ-04 | ADR pour `CharacterBody3D` + `move_and_slide()` — documenter le choix kinematic vs dynamic et la configuration de layers de collision pour la non-poussée des `RigidBody3D`. | Technique | Ouvert | **BLOQUANT avant implémentation S01** |
