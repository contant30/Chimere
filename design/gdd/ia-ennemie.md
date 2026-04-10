# IA ennemie

> **Status**: In Review
> **Author**: Romain Contant + agents
> **Last Updated**: 2026-04-09
> **Implements Pillar**: Pilier 1 — Tout est une arme · Pilier 2 — Le flow avant le challenge

## Overview

S09 gère le comportement de chaque instance d'ennemi individuelle : navigation vers le joueur, gestion du cycle de vie de l'ennemi, et hébergement du sous-système de santé S08. Chaque ennemi est une scène autonome dont la racine est un `CharacterBody3D` (layer 4). À l'instanciation, S09 injecte les dépendances de S08 via `@export` et connecte les signaux sortants (`enemy_died`, `enemy_hit`) vers S10, S12 et S15 via `connect()`. En MVP, le comportement se résume à un seul verbe : se déplacer vers la position du joueur. S09 cible la position de S01 via `NavigationAgent3D`, calcule la vélocité de navigation chaque frame dans `_physics_process`, et appelle `move_and_slide()`. S09 n'attaque pas le joueur en MVP — les dégâts infligés au joueur (S07) sont reportés à une itération post-prototype. Le système est conçu pour être aussi simple que possible : un ennemi, un état, une direction. La complexité (multiples types, attaques, états secondaires) arrive après validation de la boucle de jeu.

## Player Fantasy

Les ennemis ne chassent pas — ils affluent. Leur avancée vers le joueur est une marée lente et régulière, un mouvement de fond qui donne au joueur le temps de saisir, de viser, de sentir le poids de chaque objet dans sa main. C'est cette pression constante, jamais brutale, qui transforme la pièce en instrument : sans elle, il n'y a pas de tempo. L'ennemi qui approche n'est pas une menace — c'est le métronome qui donne au joueur la permission de jouer.

## Detailed Design

### Core Rules

1. **Structure de l'ennemi** : chaque ennemi est une scène autonome dont la racine est un `CharacterBody3D` (layer 4, mask 1|3|4 — ADR-0002). La scène contient un nœud `EnemyHealth` (S08) et un `NavigationAgent3D`. S09 est le script attaché à la racine.

2. **Injection de dépendances au spawn** : le spawner (S10 ou SpawnManager) instancie l'ennemi (`instantiate()`), injecte les quatre dépendances via `@export` — `player: Node3D`, `wave_manager: Node`, `score_manager: Node`, `vfx_manager: Node` — puis appelle `add_child()`. `_ready()` se déclenche après l'injection et câble immédiatement les signaux de S08 vers S10, S12 et S15.

3. **Navigation vers le joueur** : S09 utilise `NavigationAgent3D` ciblant `player.global_position` à chaque frame de `_physics_process`. Le navmesh est baked sur la géométrie statique de la pièce (`StaticBody3D`) uniquement — les `RigidBody3D` ne sont pas des obstacles de navigation. La mise à jour de `target_position` est dédupliquée en interne par `NavigationAgent3D` (pas de recalcul si la cible n'a pas bougé de manière significative).

4. **Mouvement** : `ENEMY_MOVE_SPEED = 2.5 m/s`. Chaque frame : mise à jour de `target_position`, récupération de `get_next_path_position()`, calcul de `direction`, assignment de `velocity`, appel de `move_and_slide()`. Pas d'avoidance RVO2 en MVP — les collisions ennemi↔ennemi sont gérées par Jolt via la physique (collision_mask inclut layer 4). Ratio player/ennemi : 7 / 2.5 = 2.8× — le joueur peut toujours fuir, l'ennemi ne crée qu'une pression de position, jamais de poursuite irrattrapable.

5. **Distance d'arrêt** : `STOPPING_DISTANCE = 0.8 m` centre-à-centre. `target_desired_distance` du `NavigationAgent3D` est configuré à cette valeur. Quand l'ennemi est dans la stopping distance, il cesse de naviguer et reste en place. En MVP, **aucune attaque** — la pression est purement spatiale.

6. **Fallback si chemin introuvable (état STUCK)** : si `get_next_path_position()` retourne une position identique à la position courante pendant plus de `STUCK_THRESHOLD = 0.5 s`, l'ennemi entre en état `STUCK`. En STUCK : déplacement en ligne droite vers `player.global_position` à `STUCK_SPEED = 2.0 m/s` (Jolt gère les collisions avec les objets physiques en chemin). Retry `NavigationAgent3D.target_position` toutes les 0.5 s — quitte STUCK dès qu'un chemin est recalculé avec succès.

7. **Réception des dégâts** : S09 n'expose pas directement `receive_damage()`. S02 (saisie/lancer), lors d'une collision avec un ennemi (layer 4), récupère le nœud `EnemyHealth` via `get_node_or_null("%EnemyHealth")` sur le corps ennemi et appelle `receive_damage(amount, type)` directement. Le pattern exact de découverte de S08 depuis S02 est un open question délégué au GDD S02 / au prototype.

8. **Transition vers la mort** : S08 émet `enemy_died(enemy: Node)` quand `current_hp` atteint 0. S09 est connecté à ce signal et passe en état `DEAD` : `velocity = Vector3.ZERO`, `set_physics_process(false)`. S08 appelle `queue_free()` — l'ensemble du sous-arbre (S08 + S09 + NavigationAgent3D) est retiré de la scène. S09 ne déclenche pas `queue_free()` lui-même.

9. **Pas d'attaque en MVP** : S09 ne génère aucun appel vers S07 (santé joueur). Les dégâts infligés au joueur sont reportés post-prototype.

### States and Transitions

| État | Description | Transitions sortantes |
|---|---|---|
| `APPROACHING` | Navmesh actif, l'ennemi suit le chemin vers le joueur | → `STUCK` si bloqué > STUCK_THRESHOLD · → `DEAD` si enemy_died reçu |
| `STUCK` | Pas de chemin navmesh valide — ligne droite vers joueur | → `APPROACHING` si chemin recalculé · → `DEAD` si enemy_died reçu |
| `DEAD` | enemy_died reçu — physique stoppée, queue_free() en cours | → aucune (instance retirée) |

### Interactions with Other Systems

| Système | Direction | Données | Interface |
|---|---|---|---|
| **S01** (Déplacement joueur) | → S09 | `player.global_position` lu chaque frame | Référence Node3D injectée via `@export` |
| **S02** (Saisie/Lancer) | → S08 via S09 | `receive_damage(amount, type)` lors d'une collision d'objet sur layer 4 | `get_node_or_null("%EnemyHealth")` sur le corps ennemi, puis appel direct |
| **S08** (Santé ennemie) | S09 héberge S08 | `enemy_died(enemy)` → S09 passe DEAD · `enemy_hit(damage, type, hp)` → S15 | Signal GDScript |
| **S10** (Vagues) | S10 → S09 au spawn | Injection @export `wave_manager` · `enemy_died` → S10 | Instanciation + connect() dans `_ready()` |
| **S12** (Score) | ← S09/S08 | `enemy_died(enemy)` | Signal GDScript |
| **S15** (VFX/Audio) | ← S09/S08 | `enemy_hit(damage, type, current_hp)` | Signal GDScript |

S09 ne connaît pas ses consommateurs directement — les connexions sont établies dans `_ready()` sur la base des références injectées par le spawner.

## Formulas

### F1 — Vélocité de navigation

```
velocity = direction_to(get_next_path_position()) * ENEMY_MOVE_SPEED
```

Variables :
- `direction_to(...)` : Vector3 normalisé depuis `global_position` vers le prochain point du chemin
- `ENEMY_MOVE_SPEED` : float, 2.5 m/s (tuning knob)
- `velocity` : Vector3, transmis à `move_and_slide()`

### F2 — Détection d'état STUCK

```
STUCK si |get_next_path_position() - global_position| < PATH_EPSILON pendant > STUCK_THRESHOLD
```

Variables :
- `PATH_EPSILON` : float, 0.1 m — seuil de détection de non-progression
- `STUCK_THRESHOLD` : float, 0.5 s — durée de non-progression avant bascule STUCK

### F3 — Ratio de pression (vérification de calibration)

```
player_speed / ENEMY_MOVE_SPEED ≥ PRESSURE_RATIO_MIN
```

Variables :
- `player_speed` : 7.0 m/s (S01, tuning knob)
- `ENEMY_MOVE_SPEED` : 2.5 m/s (tuning knob)
- `PRESSURE_RATIO_MIN` : 2.0 — ratio minimum pour que le joueur puisse toujours fuir

Vérification MVP : `7.0 / 2.5 = 2.8 ≥ 2.0` ✓

Cette contrainte n'est pas exécutée en jeu — c'est une vérification de calibration. Si `ENEMY_MOVE_SPEED` dépasse `player_speed / PRESSURE_RATIO_MIN = 3.5 m/s`, le joueur ne peut plus garantir sa fuite. Pilier 2 cassé.

## Edge Cases

**EC-01 — Spawn sans dépendances injectées**
Le spawner appelle `add_child()` sans avoir injecté `player`, `wave_manager`, `score_manager` ou `vfx_manager`. → `_ready()` déclenche des assertions (`assert(player != null, ...)`). En debug build, l'assertion crashe immédiatement avec un message explicite. En release, l'assert est retiré — l'ennemi tente de lire `player.global_position` sur un null et génère une erreur GDScript à chaque frame. À prévenir par l'ordre d'initialisation dans le spawner.

**EC-02 — NavigationMesh absent ou non baked**
Le `NavigationRegion3D` de la scène n'a pas été baked (oubli en développement). → `get_next_path_position()` retourne `global_position` immédiatement (pas de chemin). L'ennemi détecte STUCK après `STUCK_THRESHOLD` et passe en ligne droite. Comportement dégradé acceptable — l'ennemi avance quand même vers le joueur.

**EC-03 — Joueur hors de portée du navmesh**
Le joueur se retrouve dans une zone non navigable (ex. : sur un objet physique empilé). → `NavigationAgent3D` ne trouve pas de chemin valide jusqu'à la destination exacte. Retour partiel possible (plus proche point navigable). Si aucun chemin : bascule STUCK. L'ennemi approche en ligne droite depuis l'extérieur de la zone.

**EC-04 — Deux receive_damage() dans la même frame, le deuxième arrive après queue_free()**
Cas documenté dans S08 (EC-01 de S08). → S08 gère cela (receive_damage ignoré en état DEAD). S09 reçoit `enemy_died` une seule fois (S08 garantit qu'il n'émet le signal qu'une fois). `set_physics_process(false)` dans S09 empêche tout traitement ultérieur.

**EC-05 — Ennemi atteint la stopping distance mais d'autres ennemis bloquent le chemin**
Plusieurs ennemis convergent vers le joueur simultanément. Le premier atteint la stopping distance et s'arrête ; les suivants sont bloqués par la collision physique (Jolt). → Les ennemis suivants entrent en STUCK si leur chemin est bloqué. En STUCK, ils poussent physiquement l'ennemi arrêté via `move_and_slide()`. Comportement acceptable — crée une pression cumulée réaliste. Si l'empilement devient trop chaotique au playtesting, activer RVO2 (voir Tuning Knobs).

**EC-06 — Ennemi tué pendant l'état STUCK**
`enemy_died` reçu pendant que l'ennemi est en ligne droite. → Transition normale vers DEAD : `velocity = Vector3.ZERO`, `set_physics_process(false)`. La détection d'état STUCK n'a pas d'effet sur la transition de mort.

**EC-07 — Scène déchargée pendant la navigation**
La scène est réinitialisée (S12 — Retry) alors que des ennemis naviguent. → `queue_free()` sur l'ensemble des ennemis via S12. S09 est libéré avant la prochaine frame — aucun traitement parasite. NavigationAgent3D et ses connexions sont détruits avec le nœud.

## Dependencies

### Dépendances entrantes (S09 dépend de)

| Système | Ce que S09 en attend |
|---|---|
| **S01 — Déplacement joueur** | Référence `player: Node3D` injectée au spawn. S09 lit `player.global_position` chaque frame pour cibler la navigation. |
| **S08 — Santé ennemie** | S09 héberge S08 comme nœud enfant. S09 connecte les signaux `enemy_died` et `enemy_hit` de S08 vers S10, S12, S15 dans `_ready()`. S08 appelle `queue_free()` à la mort de l'ennemi — S09 ne gère pas ce retrait lui-même. |
| **S10 — Gestion des vagues** (spawner) | Injecte les dépendances (`wave_manager`, `score_manager`, `vfx_manager`, `player`) avant `add_child()`. S10 (ou son SpawnManager délégué) est responsable du cycle de vie de l'instance S09. |

### Dépendances sortantes (systèmes qui dépendent de S09)

| Système | Ce qu'il reçoit de S09/S08 |
|---|---|
| **S03 — Vagues d'ennemis** | `enemy_died(enemy: Node)` via S08 → S03 comptabilise les morts pour la progression de vague. |
| **S10 — Gestion des vagues** | `enemy_died(enemy: Node)` via S08 → S10 met à jour le compteur de vague. |
| **S12 — Score** | `enemy_died(enemy: Node)` via S08 → S12 attribue les points. |
| **S15 — VFX/Audio** | `enemy_hit(damage, type, current_hp)` via S08 → S15 déclenche les feedbacks d'impact. |
| **S02 — Saisie/Lancer** | Détecte la collision avec la couche physique de S09 (layer 4) pour appeler `receive_damage()` sur S08. |

### Note sur la circularité apparente S09 ↔ S10

S10 (vagues) spawn les instances S09, et S09 émet `enemy_died` vers S10. Ce n'est pas une dépendance circulaire de conception : S10 ne dépend pas de S09 pour son initialisation — il reçoit seulement des événements de S09 après le spawn. Le contrat est unidirectionnel à l'exécution : S10 crée, S09 notifie.

## Tuning Knobs

| Constante | Valeur MVP | Plage sûre | Effet gameplay |
|---|---|---|---|
| `ENEMY_MOVE_SPEED` | 2.5 m/s | 1.5 – 3.5 m/s | Pression spatiale. En-dessous de 1.5 : trop peu de tension. Au-dessus de 3.5 : ratio F3 cassé (joueur ne peut plus fuir — Pilier 2 rompu). Contrainte dure : `ENEMY_MOVE_SPEED < player_speed / PRESSURE_RATIO_MIN`. |
| `STOPPING_DISTANCE` | 0.8 m | 0.5 – 1.5 m | Distance centre-à-centre à laquelle l'ennemi cesse de naviguer. En-dessous de 0.5 : les collisions Jolt créent des vibrations au contact. Au-dessus de 1.5 : l'ennemi s'arrête trop loin, la pression spatiale est perdue. |
| `STUCK_THRESHOLD` | 0.5 s | 0.2 – 1.0 s | Durée de non-progression avant bascule en mode ligne droite. En-dessous de 0.2 : bascules parasites lors des micro-ralentissements de navigation. Au-dessus de 1.0 : l'ennemi reste bloqué trop longtemps, la marée se rompt. |
| `STUCK_SPEED` | 2.0 m/s | 1.5 – 3.0 m/s | Vitesse en mode STUCK (ligne droite). Doit rester inférieure à `ENEMY_MOVE_SPEED` pour éviter qu'un ennemi bloqué soit plus rapide qu'un ennemi navigant. Valeur recommandée : 80 % de `ENEMY_MOVE_SPEED`. |
| `PATH_EPSILON` | 0.1 m | 0.05 – 0.2 m | Seuil de non-progression pour la détection STUCK. En-dessous de 0.05 : détection trop sensible (flottement numérique). Au-dessus de 0.2 : STUCK non détecté sur blocages réels. |
| `PRESSURE_RATIO_MIN` | 2.0 | 1.5 – 2.5 | Ratio minimum `player_speed / ENEMY_MOVE_SPEED`. Vérification de calibration, non exécutée en jeu. En-dessous de 1.5 : fuite du joueur non garantie. Au-dessus de 2.5 : pas de pression ressentie. |

**Contrainte de calibration (F3)** : Modifier `ENEMY_MOVE_SPEED` exige de re-vérifier `player_speed / ENEMY_MOVE_SPEED ≥ PRESSURE_RATIO_MIN`. Si `player_speed` change dans S01, ce ratio doit être recalculé.

## Visual/Audio Requirements

### Visuel

| Élément | Spécification |
|---|---|
| **Mesh ennemi** | Placeholder géométrique (capsule ou cube) en MVP — aucune exigence de mesh final. |
| **Indicateur de direction** | Aucun en MVP — la marée est uniforme, pas individuelle. |
| **Feedback de mort** | S15 gérera l'effet visuel (hors scope S09) — S09 émet seulement `enemy_died`. |
| **Feedback d'impact** | S15 gérera (hors scope S09) — S09/S08 émet `enemy_hit`. |

### Audio

| Élément | Spécification |
|---|---|
| **Son de déplacement** | Aucun en MVP — la pression est spatiale, pas sonore. |
| **Son d'impact** | Délégué à S15 via `enemy_hit`. |
| **Son de mort** | Délégué à S15 via `enemy_died`. |

*Note MVP : S09 ne génère aucun feedback visuel ou audio directement. Tous les effets sont délégués à S15 via les signaux de S08.*

## UI Requirements

S09 ne génère aucun élément d'interface utilisateur directement. En MVP :

- Pas de barre de vie au-dessus de l'ennemi — la santé de l'ennemi n'est pas visible par le joueur (Pilier 2 : le flow avant la lisibilité chiffrée).
- Pas d'indicateur de distance ou de marqueur de cible.
- Le feedback d'état de l'ennemi est exclusivement sensoriel (VFX/audio via S15), jamais affiché en HUD.

*Toute évolution vers une barre de vie ou un indicateur de santé visuelle est une décision post-MVP relevant de S15 et du GDD HUD.*

## Acceptance Criteria

**AC-01 — Navigation de base**
Un ennemi spawné dans la pièce avec navmesh baked atteint la stopping distance (`≤ 0.8 m`) du joueur stationnaire en moins de `room_diagonal / ENEMY_MOVE_SPEED` secondes. Pass : l'ennemi s'arrête dans la stopping distance. Fail : l'ennemi dépasse, passe à travers, ou ne se déplace pas.

**AC-02 — Ratio de pression**
Avec `ENEMY_MOVE_SPEED = 2.5 m/s` et `player_speed = 7.0 m/s`, le joueur peut traverser la pièce (~10 m) en moins de `10 / 7.0 ≈ 1.43 s`. L'ennemi parcourt la même distance en `10 / 2.5 = 4.0 s`. Pass : le joueur atteint le bord opposé avant que l'ennemi n'ait couvert la moitié de la distance. Fail : l'ennemi rattrape le joueur.

**AC-03 — Fallback STUCK**
Un obstacle bloquant le navmesh est placé entre l'ennemi et le joueur. Après `STUCK_THRESHOLD (0.5 s)` de non-progression, l'ennemi passe en ligne droite vers le joueur à `STUCK_SPEED (2.0 m/s)`. Pass : bascule détectée en 0.5–0.7 s, déplacement en ligne droite observable. Fail : l'ennemi reste immobile ou continue de tenter le navmesh indéfiniment.

**AC-04 — Retour depuis STUCK**
L'obstacle est retiré pendant que l'ennemi est en état STUCK. Dans `0.5 s` (retry interval), l'ennemi reprend la navigation navmesh. Pass : retour à `APPROACHING` observable (trajectoire redevient calculée). Fail : l'ennemi reste en ligne droite même après que le chemin est libre.

**AC-05 — Mort propre**
S08 est appelé avec des dégâts suffisants pour amener `current_hp` à 0. L'ennemi passe en état DEAD : `velocity = Vector3.ZERO`, `set_physics_process(false)`, puis `queue_free()`. Pass : l'instance est retirée de la scène, aucun mouvement parasite après la mort. Fail : l'ennemi continue de se déplacer, ou l'instance persiste en scène.

**AC-06 — Injection de dépendances**
Un ennemi spawné sans injection de `player` (simulation d'un spawner défaillant) déclenche une assertion en debug build avec message explicite. Pass : crash immédiat avec message `"EnemyAI: player not injected"`. Fail : erreur silencieuse ou crash sans message.

**AC-07 — Pas de traversée de murs**
Un ennemi naviguant vers le joueur ne traverse pas les `StaticBody3D` de la géométrie de salle. Pass : l'ennemi contourne via le navmesh ou s'arrête (STUCK). Fail : l'ennemi traverse la géométrie statique.

**AC-08 — Signal enemy_died émis une seule fois**
Deux `receive_damage()` arrivant dans la même frame amènent `current_hp` à 0 deux fois. Pass : `enemy_died` émis une seule fois (S08 garantit l'unicité — AC-05 de S08). Fail : `enemy_died` émis deux fois, double comptage score/vague.

**AC-09 — Collision ennemi↔ennemi gérée par Jolt**
Cinq ennemis convergent vers le même joueur stationnaire. Pass : les ennemis se compriment sans se traverser, Jolt gère les collisions via layer 4. Fail : les ennemis se chevauchent visuellement ou traversent leurs colliders respectifs.

## Open Questions

**OQ-01 — Pattern exact de découverte de S08 depuis S02**
S02 doit appeler `receive_damage(amount, type)` sur le nœud `EnemyHealth` (S08) enfant de S09. Le pattern `get_node_or_null("%EnemyHealth")` sur le corps ennemi est proposé, mais son exactitude dépend de la structure de scène finale. À valider au prototype S02. Si S08 n'est pas un unique scene-local (`%`), un fallback `find_child("EnemyHealth")` est envisageable mais moins robuste. → **Blocker prototype S02.**

**OQ-02 — Seuil d'activation RVO2**
Le mode STUCK avec collisions Jolt est le comportement MVP. Si le playtesting révèle un empilement chaotique gênant le gameplay (EC-05), `NavigationAgent3D.avoidance_enabled = true` peut être activé sans modifier l'architecture (le signal `velocity_computed` est déjà câblé). À évaluer après la première session de playtesting avec 5+ ennemis simultanés.

**OQ-03 — Navmesh rebake sur modification de la pièce**
En MVP, la pièce est statique et le navmesh est baked en éditeur. Si la conception introduit des pièces procédurales ou modifiables, un rebake runtime sera nécessaire (`NavigationRegion3D.bake_navigation_mesh()`). Décision à prendre avant implémentation S10 (spawning) si les pièces ne sont pas entièrement statiques.
