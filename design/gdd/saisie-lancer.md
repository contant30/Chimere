# S02 — Saisie et lancer

> **Statut**: Approuvé
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-10
> **Implémente le Pilier**: Pilier 1 — Tout est une arme

## Vue d'ensemble

S02 — Saisie et lancer est le verbe principal du jeu : le joueur peut saisir tout objet `RigidBody3D` de la pièce, l'utiliser en frappe de mêlée ou le lancer sur un ennemi. C'est ce geste que le joueur répète en boucle pendant toute la partie — il est à la fois la mécanique offensive centrale et le moteur de la boucle de ressources (chaque objet utilisé est un objet brisé ou éloigné). Techniquement, S02 orchestre la couche physique Jolt : il gère l'état de saisie d'un objet (geler son `RigidBody3D` via `freeze = true` et `freeze_mode = KINEMATIC` et le porter à position fixe), la frappe de mêlée (collision de zone au contact), et le lancer (impulsion Jolt via `apply_central_impulse()` dans la direction du yaw caméra). S02 consulte S05 (Catalogue d'objets) pour connaître les propriétés de l'objet saisi (`mass_kg`, `grab_range_m`, `melee_damage_base`, `throw_damage_base`, `throw_impulse_scale`, et les multiplicateurs par stade) et appelle S06 (Système de dégâts) pour produire un montant entier transmis à S08 (santé ennemie) et à S04 (dégradation d'objets). La direction de lancer est fournie par S10 (Caméra TPS). La réussite de S02 est la condition sine qua non de la promesse du jeu : si le geste de saisir-frapper-lancer n'est pas satisfaisant à la première session de prototype, le projet s'arrête là.

## Fantasme joueur

Le joueur ne choisit pas une arme — il en attrape une. Choisir, c'est s'arrêter. Attraper, c'est réagir. Le système de saisie et lancer doit produire cette sensation d'automatisme intentionnel : le joueur sait ce qu'il fait, mais il le fait plus vite qu'il ne le formule. La main part avant la pensée. Le geste suivant commence avant que le précédent finisse.

Dans ce rythme ininterrompu, chaque objet impose sa propre physique. La chaise résiste un instant — elle est loyale, elle encaisse. La bouteille part trop vite — elle est sacrificielle. Le livre vole à plat, précis, presque silencieux. Le joueur n'apprend pas ces différences par une interface — il les découvre par le corps, dans le feu de l'action. Deux gestes identiques dans leur structure (saisir-utiliser), radicalement différents dans leur sensation. C'est ce qui rend la pièce vivante plutôt que générique.

Le moment cible : un ennemi approche par la gauche, un autre par la droite. Le joueur saisit la chaise à sa droite sans la regarder, frappe, la chaise éclate, sa main est déjà sur la bouteille. Il n'y a pas eu de pause. Pas de menu, pas de cooldown, pas de fenêtre d'attente. Le rythme est celui du joueur — jamais celui du système.

Et quand la pièce se vide, ce geste ne change pas. Le joueur n'a jamais l'arme idéale — il a l'arme disponible, et il la rend efficace. Ce n'est pas de l'improvisation par défaut : c'est l'expression d'une ingéniosité que le jeu reconnaît et récompense à chaque objet qui quitte la main.

**Alignement piliers** : Pilier 1 (tout est une arme) — la variété sensorielle confirme que chaque objet est distinct, pas interchangeable ; la promesse est tenue dans la main. Pilier 2 (le flow avant le challenge) — la boucle ne s'interrompt jamais : le système offre toujours un prochain geste, même en fin de partie.

## Design détaillé

### Règles principales

1. **Saisie** — Le joueur peut saisir tout `RigidBody3D` taggé `grabbable` dans un cône de `grab_range_m` (tiré de S05). Un seul objet peut être tenu à la fois. Si un objet est déjà tenu, l'input de saisie est ignoré.
2. **Porter** — L'objet saisi est gelé en kinematic et suit un point d'ancrage fixe devant le joueur (`carry_offset`). Sa vélocité Jolt est gelée. Les collisions de l'objet porté ne doivent pas bloquer le joueur (pas d'auto-poussée, pas de “marche arrière” forcée).
3. **Frappe de mêlée** — En portant, le joueur peut déclencher une frappe : l'objet effectue un court arc vers l'avant. Tout ennemi (S08) ou objet cassable (S04) dans la zone de contact reçoit un `final_damage` calculé par S06. L'objet n'est pas lâché après la frappe. Après chaque frappe (hit ou non), S02 enregistre une utilisation sur l'objet tenu (S04 `register_use(MELEE)`).
4. **Lancer** — Le joueur lâche l'objet avec `apply_central_impulse()` dans la direction du yaw caméra (S10) + léger angle vers le bas. L'objet repasse en mode dynamique. Au premier impact ennemi/cassable, S02 applique `final_damage` (S06) à la cible. Au moment du lâcher, S02 enregistre une utilisation sur l'objet tenu (S04 `register_use(THROW)`).
5. **Dépôt** — Le joueur peut poser l'objet sans force (vélocité nulle, redevient dynamic, reste au sol). Pas de dégâts.
6. **Objets lourds** — Si `mass_kg` > `max_grab_mass_kg` (tuning knob), l'objet ne peut pas être saisi. Feedback visuel : outline rouge au survol.

### États et transitions

```
EMPTY_HANDS
  → [input saisie + objet dans range + mass OK] → CARRYING

CARRYING
  → [input frappe]                              → CARRYING  (frappe, objet toujours tenu)
  → [input lancer]                              → EMPTY_HANDS + objet en vol
  → [input poser]                               → EMPTY_HANDS + objet au sol
  → [objet détruit pendant transport]           → EMPTY_HANDS
```

### Interactions avec les autres systèmes

| Système | Direction | Nature |
|---------|-----------|--------|
| S05 — Catalogue d'objets | S02 → S05 | Lit `mass_kg`, `grab_range_m`, `melee_damage_base`, `throw_damage_base`, `throw_impulse_scale`, et les `*_dmg_mult` par stade |
| S04 — Dégradation environnement | S02 ↔ S04 | Lit `current_stage` de l'objet tenu ; appelle `register_use(use_kind)` (arme tenue) et `receive_damage(amount, damage_type, impact_position)` (cible cassable) |
| S06 — Système de dégâts | S02 → S06 | Appelle `calculate(damage_base, stage_mult, damage_type)` pour produire `final_damage: int` |
| S08 — Santé ennemie | S02 → S08 | Appelle `receive_damage(amount: int, type: DamageType)` sur l'ennemi touché |
| S10 — Caméra TPS | S10 → S02 | Fournit le yaw via le `camera_pivot` injecté (ADR-0001) |
| S13 — HUD | S02 → S13 | Émet les signaux du GrabSystem (ADR-0001) : `grab_performed`, `throw_performed`, `carry_interrupted` |

## Formules

### 1. Impulsion de lancer

```
throw_impulse = throw_impulse_base_n_s × S05.throw_impulse_scale × throw_direction
```

- `throw_impulse_base_n_s` : tuning knob (Newton·seconde), valeur initiale **8 N·s**
- `S05.throw_impulse_scale` : multiplicateur par objet (catalogue)
- `throw_direction` : vecteur normalisé = yaw caméra (S10) + `throw_pitch_deg` vers le bas (**−10°**)

*Exemple : `throw_impulse_base_n_s=8`, `throw_impulse_scale=1.0`, `mass_kg=1` → vitesse initiale ~8 m/s (Jolt gère ensuite l'amortissement et les collisions).*

### 2. Dégâts transmis à S06

S02 ne calcule pas les dégâts — il prépare les paramètres et délègue :

```
tracker       = S04.destruction_tracker(held_object)  # composant sur l'objet tenu
current_stage = tracker.current_stage                 # int
entry         = held_object.catalogue_entry           # ressource S05
damage_base   = entry.melee_damage_base | entry.throw_damage_base
stage_mult    = entry.destruction_stages[current_stage].melee_dmg_mult | throw_dmg_mult
final_damage  = S06.calculate(int(damage_base), float(stage_mult), DamageType.MELEE | THROW)
```

*S02 garantit que `damage_base` est un int ≥ 1. `final_damage` est l'unique montant appliqué à S08/S04. La formule finale est dans S06.*

### 3. Détection de saisie (cone check)

```
can_grab = distance(player, object) ≤ grab_range_m
         AND angle(player_forward, dir_to_object) ≤ grab_cone_deg / 2
         AND object.mass_kg ≤ max_grab_mass_kg
```

- `grab_range_m` : lu depuis S05 (par type d'objet)
- `grab_cone_deg` : tuning knob global (**60°**)

## Cas limites

1. **Objet détruit pendant le transport** — Si S04 détruit l'objet pendant que le joueur le porte (explosion, collision externe), S02 passe immédiatement en `EMPTY_HANDS`. Aucun dégât n'est infligé au joueur.
2. **Deux objets à portée simultanément** — S02 cible l'objet le plus proche dans le cône. Pas de sélection manuelle MVP.
3. **Lancer vers un mur proche** — L'objet rebondit selon Jolt (restitution du `PhysicsMaterial`). S02 ne gère pas la trajectoire post-rebond ; S06 n'est déclenché qu'au premier contact ennemi/cassable.
4. **Frappe sans ennemi dans la zone** — L'arc de frappe se joue, pas de dégâts, l'objet reste en main. Pas d'état d'erreur.
5. **Objet hors-limites pendant le transport** — Si le joueur porte un objet et tombe dans un vide (hors pièce), l'objet est détruit silencieusement, `EMPTY_HANDS`.
6. **Input simultané frappe + lancer** — Priorité au lancer (input le plus "définitif"). La frappe est ignorée si les deux sont actifs dans la même frame.
7. **Objet trop lourd survolé** — Outline rouge affiché mais aucune action. Si le joueur appuie sur saisie, l'input est ignoré sans feedback sonore additionnel (pas de "bruit d'échec").
8. **Objet saisi qui passe dans un autre `RigidBody3D`** — La collision kinematic de l'objet porté est désactivée vs. le joueur et vs. les objets de l'environnement statique. Les ennemis restent collidables (la frappe de mêlée fonctionne par zone, pas par collision physique).

## Dépendances

### S02 dépend de

| Système | Ce que S02 consomme |
|---------|---------------------|
| S05 — Catalogue d'objets | `mass_kg`, `grab_range_m`, `melee_damage_base`, `throw_damage_base`, `throw_impulse_scale`, `StageData.{melee_dmg_mult, throw_dmg_mult}` |
| S04 — Dégradation environnement | `current_stage` de l'objet tenu ; interface `register_use()` et `receive_damage()` sur les objets cassables |
| S06 — Système de dégâts | Fonction `calculate(damage_base: int, stage_mult: float, damage_type: DamageType) -> int` |
| S10 — Caméra TPS | Yaw caméra (direction de lancer) via le `camera_pivot` injecté |

### Systèmes qui dépendent de S02

| Système | Ce que S02 fournit |
|---------|--------------------|
| S08 — Santé ennemie | Appel `receive_damage(amount, type)` sur contact (montant issu de S06) |
| S04 — Dégradation environnement | Appels `register_use()` (arme tenue) et `receive_damage(amount, type, impact_position)` (cible cassable) |
| S13 — HUD | Signaux GrabSystem (ADR-0001) : `grab_performed(object)`, `throw_performed(object, impulse)`, `carry_interrupted(object)` |

### Contrats d'événements (GrabSystem, ADR-0001)

S02 (implémenté par le GrabSystem, ADR-0001) émet des signaux d'état/interaction pour les consommateurs UI (S13) et futurs systèmes. Les signaux sont typés et connectés en Callable (ADR-0005). Les appels “commande” restent des appels directs (ex : `S08.receive_damage()`).

## Paramètres de réglage

| Knob | Valeur initiale | Plage sûre | Effet gameplay |
|------|----------------|------------|----------------|
| `carry_offset` | (0, 0.8, −1.2) m | y: 0.5–1.2 / z: −0.8–−1.5 | Position de l'objet porté devant le joueur |
| `max_grab_mass_kg` | 15 kg | 5–30 kg | Seuil au-delà duquel un objet est insaisissable |
| `grab_cone_deg` | 60° | 30°–90° | Largeur du cône de détection de saisie |
| `throw_impulse_base_n_s` | 8 N·s | 4–15 N·s | Impulsion de base du lancer (à multiplier par `throw_impulse_scale`) |
| `throw_pitch_deg` | −10° | −5°–−20° | Angle vers le bas du lancer (évite les tirs au plafond) |
| `melee_arc_duration_s` | 0.15 s | 0.08–0.25 s | Durée de l'arc de frappe de mêlée |
| `melee_arc_angle_deg` | 30° | 15°–60° | Amplitude angulaire de l'arc de frappe |
| `melee_hitbox_radius_m` | 0.5 m | 0.3–0.8 m | Rayon de la zone de contact frappe |
| `grab_cooldown_s` | 0.1 s | 0–0.3 s | Délai minimal entre deux saisies consécutives (anti-spam) |

## Exigences visuelles et audio

### Visuel

- **Outline de saisie** : objet grabbable dans le cône → outline blanc ; objet trop lourd → outline rouge. Pas d'outline hors cône.
- **Arc de frappe** : animation procédurale courte de l'objet (translation + rotation sur `melee_arc_duration_s`). Pas de VFX additionnel MVP.
- **Objet en vol** : aucun trail MVP. Rotation physique Jolt native (pas de spin forcé).
- **Impact** : flash blanc 1 frame sur l'ennemi touché (géré par S08). S02 n'a pas de responsabilité visuelle post-impact.

### Audio

- **Saisie** : son bref de "grab" (whoosh léger). Un son par type d'objet si le catalogue le permet, sinon un son générique.
- **Frappe de mêlée** : son d'impact (clé `sound_impact_key` du catalogue S05 si disponible, sinon générique). Son de swing avant l'impact.
- **Lancer** : son de release (effort, souffle). Son d'impact sur mur (géré par S04/Jolt).
- **Objet trop lourd** : silence (pas de son d'erreur — Règle 7 Edge Cases).
- **Pas d'audio 3D MVP** : tous les sons de S02 sont en 2D (pas de spatialisation). À revisiter en V1.0.

## Exigences UI

- **Réticule** : un point central fixe (dot). En état `CARRYING`, le réticule change de forme (croix ou anneau) pour indiquer qu'un objet est tenu. Pas d'HUD additionnel MVP.
- **Indicateur d'objet ciblé** : l'outline (Visual) fait office d'indicateur — pas de texte flottant, pas de tooltip MVP.
- **Pas de barre de "charge"** : le lancer n'a pas de charge variable MVP. L'input est binaire (appuyer = lancer à force fixe).
- **Icône de main** : aucune icône de main en HUD MVP. L'état CARRYING est communiqué uniquement par l'outline et le changement de réticule.

## Critères d'acceptation

| # | Critère | Type | Vérification |
|---|---------|------|--------------|
| AC-01 | Le joueur peut saisir un objet `grabbable` dans le cône en appuyant sur l'input saisie | Fonctionnel | Manuel : approcher un objet, appuyer, l'objet suit le joueur |
| AC-02 | Un seul objet peut être tenu à la fois — saisir un second objet n'a aucun effet | Fonctionnel | Manuel : tenir un objet, viser un second, appuyer → rien ne se passe |
| AC-03 | Un objet `mass_kg > max_grab_mass_kg` affiche un outline rouge et ne peut pas être saisi | Fonctionnel | Manuel : approcher objet lourd → outline rouge, input ignoré |
| AC-04 | La frappe de mêlée appelle `S08.receive_damage(final_damage, MELEE)` avec `final_damage = S06.calculate(melee_damage_base, melee_dmg_mult, MELEE)` | Fonctionnel | Playtest : frapper ennemi → HP ennemi réduit du montant attendu |
| AC-05 | Le lancer applique l'impulse dans la direction du yaw caméra + pitch de `throw_pitch_deg` | Fonctionnel | Manuel : lancer → trajectoire cohérente avec la caméra |
| AC-06 | L'objet lancé applique `S08.receive_damage(final_damage, THROW)` au premier contact ennemi (et `S04.receive_damage(...)` sur cassable) | Fonctionnel | Playtest : lancer sur ennemi → HP réduit du montant attendu |
| AC-07 | Le dépôt pose l'objet sans dégâts, joueur revient en `EMPTY_HANDS` | Fonctionnel | Manuel : tenir, déposer → objet au sol, pas de dégâts |
| AC-08 | Si l'objet est détruit pendant le transport, le joueur passe en `EMPTY_HANDS` sans crash | Robustesse | Test : forcer destruction d'un objet porté → pas d'erreur |
| AC-09 | Input simultané frappe + lancer → seul le lancer s'exécute | Fonctionnel | Test : déclencher les deux inputs dans la même frame |
| AC-10 | Les signaux GrabSystem (ADR-0001) `grab_performed(object)`, `throw_performed(object, impulse)`, `melee_performed(object)`, `object_dropped(object)`, `carry_interrupted(object)` sont émis aux bons moments | Intégration | Test unitaire : vérifier émission signal sur chaque action |
| AC-11 | `grab_cooldown_s` empêche deux saisies en rafale sous le seuil | Fonctionnel | Test : spam input saisie → deuxième saisie ignorée si < cooldown |

## Questions ouvertes

| # | Question | Priorité | Résolution |
|---|----------|----------|------------|
| OQ-01 | Le lancer doit-il avoir une charge variable (hold = plus de force) en V1.0 ? | Basse | À évaluer au prototype — MVP binaire |
| OQ-02 | L'outline doit-il être affiché pour tous les objets grabbables en permanence, ou uniquement dans le cône actif ? | Moyenne | À valider au playtest (lisibilité vs. pollution visuelle) |
| OQ-03 | Faut-il un son d'erreur distinct pour "objet trop lourd" vs. "rien dans le cône" ? | Basse | Décision au playtest audio |
| OQ-04 | La frappe de mêlée doit-elle lancer l'objet si l'ennemi est tué d'un coup (objet traverse la cible) ? | Moyenne | À décider avec S04/S08 — dépend du comportement de mort ennemi |
| OQ-05 | ADR à créer : pattern `GrabSystem` (autoload vs. nœud enfant du joueur) avant implémentation | Haute | **Résolu** — ADR-0001 (GrabSystem) Accepted le 2026-04-09 |
