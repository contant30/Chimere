# S01 — Déplacement joueur

> **Statut**: In Design
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-08
> **Implémente le Pilier**: Pilier 2 — Le flow avant le challenge

## Overview

S01 — Déplacement joueur est le système de mouvement du personnage joueur dans la pièce. Il gère le déplacement libre en 3D (8 directions), l'accélération, la décélération et la gestion des collisions avec l'environnement et les objets physiques. Techniquement, il s'appuie sur un `CharacterBody3D` cinématique avec `move_and_slide()` — entièrement indépendant de la simulation physique Jolt des objets, ce qui garantit un contrôle prévisible même en présence de nombreux corps rigides actifs. Pour le joueur, ce système est le socle de toute improvisation : se repositionner pour saisir l'objet suivant, rompre l'angle d'attaque d'un ennemi, survivre à un débordement en retraite rapide. Un déplacement fluide et réactif est la condition silencieuse de la fantasy du jeu.

## Player Fantasy

Le joueur ne pense jamais à ses jambes. Il pense à la chaise dans le coin, à l'ennemi qui approche par la gauche, à l'objet qu'il vient de lancer. Le déplacement est invisible parce qu'il est parfaitement réactif — à tout moment, le joueur peut pivoter, reculer, contourner sans friction. La fantasy n'est pas "je me déplace bien" : c'est *"je suis toujours au bon endroit"*. Comme un personnage de film d'action qui n'hésite jamais — qui n'est jamais coincé dans un angle mort, jamais trop loin du prochain objet, jamais pris par surprise parce qu'il n'a pas pu se retourner assez vite. Le déplacement est la condition silencieuse de l'improvisation fluide.

## Detailed Design

### Core Rules

1. **Déplacement 8 directions** : Le joueur se déplace dans les 8 directions cardinales et diagonales via les inputs WASD / stick analogique gauche. Les diagonales utilisent la longueur du vecteur d'input clamped à 1.0 (`input_vector.limit_length(1.0)`).
2. **Orientation vers la caméra** : Le personnage fait toujours face à la direction horizontale de la caméra (yaw). Le déplacement latéral (strafe) et arrière sont possibles sans rotation du personnage. La direction de la caméra est fournie par S10.
3. **Vitesse unique** : Une seule vitesse de déplacement au sol — pas de marche/sprint. Le personnage est toujours en mouvement "rapide" pour maintenir le rythme.
4. **Accélération / Décélération** : Le déplacement utilise une accélération linéaire à l'entrée et une décélération par friction à la sortie. Le personnage s'arrête nettement — pas d'inertie persistante. Valeurs tunables (voir Tuning Knobs).
5. **Saut simple** : Le joueur peut sauter une fois depuis le sol (espace / bouton A gamepad). Fonction utilitaire uniquement — passer par-dessus des objets renversés. Pas de double-saut. Le saut applique une vélocité verticale instantanée ; la gravité gère la descente.
6. **Gravité** : La gravité est appliquée manuellement chaque frame (`velocity.y -= gravity * delta`) pour contrôle total. La valeur par défaut provient de `ProjectSettings.get("physics/3d/default_gravity")`.
7. **Collision avec objets physiques** : Le joueur ne pousse pas les `RigidBody3D` Jolt en marchant — il les contourne ou les enjambe (saut). L'interaction intentionnelle avec les objets est responsabilité de S02.
8. **Aucune pente** : La pièce est plate. `floor_max_angle` reste à la valeur Godot par défaut (45°) pour gérer les micro-inclinaisons des débris.

### States and Transitions

| État | Condition d'entrée | Condition de sortie | Comportement |
|------|-------------------|---------------------|--------------|
| **IDLE** | Aucun input de déplacement, `is_on_floor()` | Input de déplacement détecté / saut | Personnage immobile, friction maximale |
| **MOVING** | Input de déplacement, `is_on_floor()` | Input relâché / saut / chute | Déplacement à `MOVE_SPEED`, accélération appliquée |
| **AIRBORNE** | `!is_on_floor()` (saut ou chute d'un rebord) | `is_on_floor()` (atterrissage) | Gravité appliquée, contrôle aérien réduit (voir Tuning Knobs) |

*Note : Il n'y a pas d'état "MORT" dans S01. La mort est gérée par S07 ; S07 émet `player_died`, S01 écoute ce signal et désactive le traitement des inputs.*

### Interactions with Other Systems

| Système | Direction | Interface |
|---------|-----------|-----------|
| **S10 — Caméra TPS** | S10 → S01 | S10 fournit la direction horizontale (yaw) de la caméra. S01 l'utilise pour orienter les inputs de déplacement dans l'espace monde. |
| **S02 — Saisie et lancer** | S01 → S02 | S01 expose `global_position` et `velocity` du joueur — utilisées par S02 pour calculer l'origine et l'impulsion du lancer. |
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
# Déplacement horizontal
if direction.length() > 0.0:
    velocity.x = move_toward(velocity.x, direction.x * MOVE_SPEED, ACCELERATION * delta)
    velocity.z = move_toward(velocity.z, direction.z * MOVE_SPEED, ACCELERATION * delta)
else:
    velocity.x = move_toward(velocity.x, 0.0, FRICTION * delta)
    velocity.z = move_toward(velocity.z, 0.0, FRICTION * delta)

# Gravité
if not is_on_floor():
    velocity.y -= GRAVITY * delta

# Saut
if Input.is_action_just_pressed("jump") and is_on_floor():
    velocity.y = JUMP_VELOCITY

move_and_slide()
```

**Variables :**

| Variable | Symbole | Type | Plage | Description |
|----------|---------|------|-------|-------------|
| Vitesse max | `MOVE_SPEED` | float | 3.0–10.0 m/s | Vitesse cible au sol (voir Tuning Knobs) |
| Accélération | `ACCELERATION` | float | 10.0–40.0 m/s² | Taux de montée en vitesse |
| Friction | `FRICTION` | float | 15.0–50.0 m/s² | Taux de décélération |
| Gravité | `GRAVITY` | float | 9.8 m/s² | Valeur projet par défaut (Jolt) |
| Vélocité saut | `JUMP_VELOCITY` | float | 3.0–6.0 m/s | Impulsion verticale initiale |
| Contrôle aérien | `AIR_CONTROL` | float | 0.0–1.0 | Multiplicateur sur ACCELERATION en l'air |

**Output :** `velocity` appliqué via `move_and_slide()`. La position résultante est exposée via `global_position`.

**Exemple :** `MOVE_SPEED=5.0`, input plein avant, `ACCELERATION=20.0`, `delta=0.016` :
`velocity.z = move_toward(0, -5.0, 20.0 × 0.016) = -0.32 m/s` (première frame — pleine vitesse atteinte en ~0.25 s)

## Edge Cases

- **Si le joueur appuie sur Saut en étant AIRBORNE** : l'input est ignoré. `is_on_floor()` est false — la condition de saut n'est pas remplie, aucune vélocité n'est ajoutée. Pas de double-saut.
- **Si le joueur tombe d'un rebord** (transition MOVING → AIRBORNE sans saut) : la gravité s'applique immédiatement. `is_on_floor()` passe à false à la première frame hors sol.
- **Si le joueur est coincé entre un `RigidBody3D` Jolt et un mur** : `move_and_slide()` résout la collision — le joueur glisse le long de la surface la plus proche. Le joueur ne pousse pas activement les objets physiques.
- **Si le joueur est mort (`player_died` reçu)** : S01 désactive le traitement des inputs et gèle `velocity` à `Vector3.ZERO`. Le personnage reste à sa position, la physique Jolt continue sur les objets environnants.
- **Si le vecteur d'input est exactement (0, 0)** : `direction.length() == 0.0` — la branche friction est prise, `velocity.x` et `velocity.z` convergent vers 0 via `move_toward`. Pas de division par zéro.
- **Si `camera_yaw_radians` n'est pas encore fourni par S10** (initialisation) : S01 utilise `0.0` comme yaw par défaut — le joueur se déplace selon l'axe monde Z. Ce cas disparaît dès que S10 est actif.
- **Si `GRAVITY` est 0** (valeur projet invalide) : le joueur flotte après un saut. Non géré dans S01 — configuration projet incorrecte, à détecter en QA via AC-S01-07.

## Dependencies

### Dépendances amont (ce dont S01 a besoin)

| Système | Nature | Interface attendue |
|---------|--------|--------------------|
| **S10 — Caméra TPS** | Soft (S01 fonctionne sans S10 avec yaw=0.0) | S10 expose `camera_yaw_radians: float` mis à jour chaque frame |

### Dépendances aval (systèmes qui dépendent de S01)

| Système | Nature | Ce qu'ils consomment |
|---------|--------|----------------------|
| **S02 — Saisie et lancer** | Hard | `global_position: Vector3`, `velocity: Vector3` |
| **S09 — IA ennemie** | Hard | `global_position: Vector3` (cible de navigation) |
| **S10 — Caméra TPS** | Hard | Nœud joueur (`CharacterBody3D`) à suivre |
| **S07 — Santé joueur** | Hard | S07 est monté sur le même nœud joueur ; émet `player_died` sur lequel S01 est abonné |
| **S13 — HUD** | Soft | Position joueur (optionnel, indicateur d'objet tenu) |

*Note : S02, S09, S10 ne peuvent pas fonctionner sans S01 — dépendances hard. S07 partage le nœud joueur et n'est pas une dépendance directe de S01 — c'est S01 qui écoute S07.*

## Tuning Knobs

| Knob | Variable | Valeur MVP | Plage sûre | Trop haut | Trop bas | Note |
|------|----------|-----------|------------|-----------|----------|------|
| Vitesse de déplacement | `MOVE_SPEED` | 5.0 m/s | 3.0–8.0 | Traverse la pièce trop vite, difficile de cibler | Le joueur se sent lent et engourdi | Point de départ : pièce ~10×10 m, traversée en ~2 s |
| Accélération | `ACCELERATION` | 20.0 m/s² | 10.0–40.0 | Départ immédiat — perd la sensation de poids | Démarrage mou, latence perçue | Interagit avec FRICTION |
| Friction (décélération) | `FRICTION` | 25.0 m/s² | 15.0–50.0 | Arrêt brutal | Glissement, perte de précision | FRICTION > ACCELERATION recommandé pour arrêt net |
| Vélocité de saut | `JUMP_VELOCITY` | 4.5 m/s | 3.0–6.0 | Sauts excessivement hauts | Saut trop bas, ne passe pas les objets | Calibrer avec GRAVITY |
| Gravité | `GRAVITY` | 9.8 m/s² | 9.8–20.0 | Chute très violente | Le joueur flotte | Valeur projet par défaut Jolt |
| Contrôle aérien | `AIR_CONTROL` | 0.6 | 0.0–1.0 | Plein contrôle aérien (pas de poids) | Aucun contrôle (trop rigide) | Multiplicateur sur ACCELERATION en état AIRBORNE |

*Interactions : augmenter `MOVE_SPEED` sans augmenter `FRICTION` allonge la distance de freinage. Augmenter `GRAVITY` sans augmenter `JUMP_VELOCITY` raccourcit la hauteur de saut.*

## Visual/Audio Requirements

**Visual :**
- Animation de déplacement : cycle de run fluide (vitesse unique — pas d'animation marche séparée). Strafes gauche/droite et arrière avec inclinaison légère du torse.
- Animation idle : posture de vigilance active — personnage prêt à bondir, jamais au repos total.
- Animation de saut : phase décollage (accroupi 1–2 frames), phase apogée (corps tendu), phase atterrissage (absorption au sol).
- Pas d'animation de mort dans S01 — responsabilité de S07.

**Audio :**
- Sons de pas au sol, déclenchés par S01 à chaque foulée. Deux variantes : sol lisse / débris (état S04).
- Son d'atterrissage après saut. Volume proportionnel à la hauteur de chute.
- Aucun son de saut ou de déplacement en état AIRBORNE.

*📌 Ces spécifications sont des intentions de design. Les assets détaillés sont produits via `/asset-spec system:deplacement-joueur` après approbation de l'art bible.*

## UI Requirements

S01 n'a pas d'interface utilisateur propre. La position du joueur est consommée indirectement par S13 (HUD) pour l'indicateur d'objet tenu.

## Acceptance Criteria

| # | AC | Condition | Résultat attendu |
|---|-----|-----------|-----------------|
| AC-S01-01 | Déplacement 8 directions | GIVEN le joueur en IDLE, WHEN input diagonale avant-droite à fond, THEN le personnage se déplace vers l'avant-droite, magnitude input ≤ 1.0 | Vérifié visuellement + debug `velocity` |
| AC-S01-02 | Orientation vers caméra | GIVEN la caméra pointant vers Z+90°, WHEN input "avant" pressé, THEN le personnage se déplace à 90° de l'axe monde Z | Vérifié en rotation caméra de 90° |
| AC-S01-03 | Vitesse maximale atteinte | GIVEN MOVING, input plein avant, WHEN 1.0 s s'écoule, THEN `velocity.length()` ≈ `MOVE_SPEED` (±0.1) | Test chronométré, valeur debuggée |
| AC-S01-04 | Arrêt net | GIVEN MOVING à pleine vitesse, WHEN input relâché, THEN `velocity.xz` atteint (0,0) en moins de 0.3 s (FRICTION=25) | Test chronométré |
| AC-S01-05 | Saut depuis le sol | GIVEN IDLE ou MOVING, `is_on_floor()` true, WHEN touche Saut pressée, THEN `velocity.y` = `JUMP_VELOCITY` (4.5), état passe à AIRBORNE | Vérifié via debug `velocity.y` |
| AC-S01-06 | Pas de double-saut | GIVEN AIRBORNE, WHEN touche Saut pressée, THEN aucune vélocité supplémentaire — `velocity.y` continue sa décroissance gravitationnelle | Vérifié debug `velocity.y` |
| AC-S01-07 | Gravité appliquée | GIVEN AIRBORNE après saut, WHEN 0.5 s s'écoule, THEN `velocity.y` < 0 (descente confirmée) | Test de valeur à mi-arc |
| AC-S01-08 | Désactivation à la mort | GIVEN mort (`player_died` émis), WHEN input de déplacement envoyé, THEN `velocity` reste à `Vector3.ZERO` | Test signal + input forcé |
| AC-S01-09 | Collision glissante | GIVEN un `RigidBody3D` contre un mur, WHEN joueur se déplace vers eux, THEN `move_and_slide()` fait glisser le joueur — pas de blocage complet | Test de scène de collision |
| AC-S01-10 | Stabilité sans input | GIVEN aucun input, WHEN 600 frames s'exécutent (10 s), THEN aucune erreur GDScript, `velocity.xz` converge vers 0 | Test de stabilité automatisé |

## Open Questions

| # | Question | Owner | Décision requise avant |
|---|----------|-------|------------------------|
| OQ-01 | Coyote time ? — Permettre un saut bref (2–3 frames) après avoir quitté un rebord sans sauter. Améliore le feel mais ajoute de la complexité. | Design | Prototype S01 |
| OQ-02 | Son de pas : déclenchement par timer ou par événement d'animation (footstep IK) ? | Technique | Implémentation S14 |
| OQ-03 | La taille de la pièce est estimée à ~10×10 m — `MOVE_SPEED=5.0` traverse en ~2 s. À valider au prototype. | Design | Prototype S01 |
| OQ-04 | ADR pour `CharacterBody3D` + `move_and_slide()` — documenter le choix kinematic vs dynamic avant implémentation S01. | Technique | Avant implémentation S01 |
