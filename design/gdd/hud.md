# S13 — HUD

> **Status**: In Review
> **Author**: Romain Contant + agents
> **Last Updated**: 2026-04-10
> **Implements Pillar**: Pilier 2 — Le flow avant le challenge

## Overview

S13 — HUD est la couche de traduction entre l'état interne du jeu et le regard périphérique du joueur. Il consomme les signaux publiés par S07 (`player_hp_changed`, `player_hit`), S03 (`wave_started`), et les signaux du `GrabSystem` ADR-0001 (`grab_performed`, `throw_performed`) pour maintenir en temps réel trois indicateurs permanents : une barre de vie (bas gauche), un compteur de vague (haut centre), et une silhouette de l'objet tenu (bas droite). Implémenté comme un `CanvasLayer` indépendant de la caméra 3D, S13 ne vit pas dans la scène de jeu — il la lit. Toutes les règles visuelles (formes, couleurs, typographie, timings d'animation) sont définies dans l'art bible §7 et s'appliquent sans exception. Un HUD qui réussit son rôle est invisible : le joueur sait combien de HP il lui reste, quelle vague est en cours, et quel objet il tient — sans jamais avoir eu à le chercher activement.

## Player Fantasy

Le HUD est le souffleur de la performance. Au théâtre, le souffleur est invisible depuis la salle — et l'acteur ne l'entend que quand il en a besoin. Le HUD fonctionne de la même façon : la barre de HP murmure "tu ralentis" quand elle descend ; le compteur de vague souffle "respire — la suivante arrive" ; la silhouette de l'objet tenu confirme "oui, c'est bien ça dans ta main".

Le moment cible : le joueur enchaîne trois lancers parfaits, la vague se vide. À aucun moment il n'a consulté le HUD. Mais quand il relève le regard entre deux vagues et que le compteur affiche "2/3", l'information est là — elle l'attendait. Le HUD n'interrompt jamais la phrase. Il attend la virgule.

*Pilier servi : Pilier 2 — "Le flow avant le challenge." Un HUD qui se lit périphériquement pendant le combat est invisible — c'est l'objectif.*

## Detailed Design

### Core Rules

**Élément 1 — HP Bar**

1. **Initialisation.** À la réception du premier `player_hp_changed(current_hp, max_hp)` (ou à `_ready()`), la barre est initialisée avec `fill_ratio = current_hp / max_hp`. Si le signal n'a pas encore été reçu à l'entrée de la scène, la barre affiche `fill_ratio = 1.0` (pleine) jusqu'à la première réception.

2. **Position et dimensions.** La barre est ancrée en bas à gauche du viewport (`anchor = (0, 1)`). Marges : 24 px depuis le bord gauche, 24 px depuis le bord bas. Dimensions : 160 × 14 px. Ces valeurs sont des tuning knobs (`HP_BAR_WIDTH = 160`, `HP_BAR_HEIGHT = 14`), jamais hardcodées.

3. **Construction visuelle.** Implémentée comme deux `ColorRect` superposés (fond + remplissage), ou `TextureProgressBar` avec `fill_mode = LEFT_TO_RIGHT`. Le fond : `StyleBoxFlat`, blanc (L100%) à alpha 20%. Le remplissage : `StyleBoxFlat`, couleur selon l'état. Aucun `border_radius`. Aucune texture, aucun dégradé.

4. **Mise à jour du fill ratio.** À chaque `player_hp_changed(current_hp, max_hp)`, calculer `fill_ratio = float(current_hp) / float(max_hp)`, clampé à `[0.0, 1.0]`. Appliquer immédiatement : `fill_rect.size.x = HP_BAR_WIDTH * fill_ratio`. Aucun tween sur la largeur.

5. **États de couleur.**
   - **NORMAL** (`current_hp > HP_LOW_THRESHOLD`, i.e. > 6) : remplissage blanc (L100%).
   - **ALERT** (`current_hp ≤ HP_LOW_THRESHOLD`, i.e. ≤ 6) : remplissage orange alert (H28°/S85%/L55%).
   Transition de couleur instantanée (aucune interpolation) à chaque `player_hp_changed`.

6. **Hit flash.** À chaque `player_hit(damage, type, current_hp)` reçu depuis S07, un `ColorRect` overlay (160 × 14 px, orange alert) exécute la séquence suivante via `Tween` :
   - Fade-in : alpha 0 → 1 en 80 ms (linéaire).
   - Hold : alpha 1 pendant 80 ms.
   - Fade-out : alpha 1 → 0 en 280 ms (linéaire).
   - Durée totale : **440 ms** (art bible §7.6).
   L'overlay est un enfant du conteneur HP bar, rendu au-dessus du remplissage. Il n'affecte ni le fill ratio ni la couleur d'état. Si un second `player_hit` arrive pendant un flash en cours, le tween actif est tué et une nouvelle séquence de 440 ms commence immédiatement depuis alpha 0.

7. **Pulse basse vie.** Tant que `current_hp ≤ HP_LOW_THRESHOLD` (état ALERT), le `ColorRect` de remplissage oscille en alpha entre 1.0 et 0.55, période `HP_PULSE_PERIOD = 800 ms`, easing in-out, via un `Tween` en boucle. Le pulse démarre au frame d'entrée dans l'état ALERT et s'arrête immédiatement (alpha snap à 1.0) dès que `current_hp > HP_LOW_THRESHOLD`. Le hit flash s'exécute en concurrence avec le pulse sans l'interrompre.

8. **HP à zéro.** Quand `current_hp == 0`, `fill_ratio = 0.0`, largeur du remplissage = 0 px. Le fond reste visible. Flash et pulse s'arrêtent — remplacés par l'écran Game Over (Élément 5).

---

**Élément 2 — Compteur de vague**

1. **Position et dimensions.** `Label` ancré en haut-centre du viewport (`anchor = (0.5, 0)`), centré horizontalement. Marge depuis le bord haut : 16 px. Police : Bold 18 px. Couleur : blanc (L100%). Aucun fond `StyleBoxFlat`.

2. **Format du texte.** Affiche toujours `"N/3"` où N est le numéro de vague courant (entier 1–3). `WAVE_COUNT_TOTAL = 3` est une constante. Exemple : vague 2 → `"2/3"`.

3. **Initialisation.** À `_ready()`, avant tout signal `wave_started`, le compteur affiche `"1/3"` (la vague 1 étant imminente au démarrage). Évite un état vide perceptible.

4. **Mise à jour sur signal.** À chaque `wave_started(wave_number)` reçu depuis S03, le texte est mis à jour instantanément : `label.text = str(wave_number) + "/3"`. L'overlay d'annonce (Élément 4) se déclenche simultanément et indépendamment.

5. **Après la vague 3.** À `wave_started(3)`, le compteur passe à `"3/3"` et reste à `"3/3"` pour le reste de la session. Il n'est pas masqué à la fin des vagues.

---

**Élément 3 — Silhouette de l'objet tenu**

1. **Position et dimensions.** Ancré en bas à droite du viewport (`anchor = (1, 1)`). Marges : 24 px depuis le bord droit, 24 px depuis le bord bas. Conteneur : 80 × 80 px, fond `StyleBoxFlat` noir (L0%) à alpha 65%, aucun `border_radius`. À l'intérieur : `TextureRect` de 64 × 64 px centré (8 px de marge sur tous les côtés), `modulate = Color(1, 1, 1, 1)` (blanc).

2. **État vide.** En l'absence d'objet tenu, le `TextureRect` est masqué (`visible = false`). Le conteneur fond 80 × 80 reste visible en permanence comme ancre périphérique.

3. **Déclencheur affichage.** À `grab_performed(object: RigidBody3D)` (ADR-0001 GrabSystem) : `TextureRect.visible = true`, `TextureRect.texture` ← `object.silhouette_texture`. Si la texture est invalide, afficher l'icône générique de fallback — jamais un slot vide en état SHOWING.

4. **Déclencheur effacement.** À `throw_performed` (ADR-0001 GrabSystem) : `TextureRect.visible = false` immédiatement, même frame. Aucun fade-out.

5. **Pas d'empilement.** Le GrabSystem garantit au plus un objet tenu en MVP. Si `grab_performed` arrive pendant qu'une silhouette est affichée, remplacer la texture immédiatement sans animation.

---

**Élément 4 — Overlay d'annonce de vague**

1. **Déclencheur.** Uniquement sur `wave_started(wave_number)` reçu depuis S03, pour les vagues 1, 2 et 3.

2. **Texte.** `"VAGUE " + str(wave_number)`. Exemple : vague 1 → `"VAGUE 1"`. Aucun texte additionnel.

3. **Position.** `Label` centré horizontalement et verticalement sur l'écran (anchors 0.5/0.5/0.5/0.5). Enfant du `CanvasLayer` principal. Le centre est libre de tout élément permanent (art bible §7 : aucun UI permanent en centre d'écran).

4. **Typographie.** Police : Bold 96 px. Couleur : blanc (L100%). Aucun fond.

5. **Séquence d'animation.** Via `Tween` sur le nœud label :
   - Phase 1 (scale-down) : `scale` tweens de `Vector2(1.3, 1.3)` → `Vector2(1.0, 1.0)` en 150 ms (`EASE_OUT`).
   - Phase 2 (hold) : `scale = Vector2(1.0, 1.0)`, `modulate.a = 1.0` jusqu'à t = 900 ms.
   - Phase 3 (fade-out) : `modulate.a` tweens de 1.0 → 0.0 en 300 ms (t = 900 ms → t = 1200 ms).
   - Durée totale : **1200 ms** (art bible §7.6).
   Après le tween : `visible = false`, reset `scale = Vector2(1.0, 1.0)`, reset `modulate.a = 1.0`.

6. **Input jamais bloqué.** `mouse_filter = MOUSE_FILTER_IGNORE` sur tous les nœuds HUD. Aucun `process_mode` override. Mouvements, saisie et lancer restent actifs pendant toute la durée de 1200 ms. Règle non négociable (art bible §7).

7. **Concurrence.** Si `wave_started` arrive pendant une animation en cours (impossible en jeu normal) : tuer le tween actif, reset, démarrer la nouvelle animation.

8. **Z-order.** Rendu au-dessus des éléments permanents, en-dessous de l'écran Game Over.

---

**Élément 5 — Écran Game Over (in-HUD)**

1. **Déclencheur.** `game_state_changed(GameState.GAME_OVER)` reçu depuis S11. Affichage immédiat, même frame. Tous les éléments permanents et toute animation d'annonce en cours sont masqués simultanément.

2. **Contenu.** Deux labels uniquement :
   - `"GAME OVER"` — Bold 96 px, blanc (L100%), centré.
   - Prompt retry — `"[INPUT] Rejouer"` où `[INPUT]` est remplacé à l'exécution par la touche/icône bindée à l'action `retry` dans l'InputMap (ex. `"R Rejouer"` clavier, `"A Rejouer"` manette) — Bold 24 px, blanc (L100%), centré, 72 px sous `"GAME OVER"`.
   Aucun fond, aucun assombrissement de la scène 3D.

3. **Contrainte de timing.** De `GameState.GAME_OVER` à la possibilité de presser retry : < 3 secondes (budget S11+S07+S13 cumulés). Contribution S13 : zéro délai intentionnel — l'écran est interactif immédiatement.

4. **Input retry.** S13 écoute l'action `retry` (`is_action_just_pressed("retry")`) uniquement quand `GameState.GAME_OVER` est actif. À la détection : émet `retry_requested()`. S11 est le seul consommateur. S13 ne réinitialise aucun système directement.

5. **Garde d'input.** L'écoute `retry` est désactivée dès que `game_state_changed` sort de `GameState.GAME_OVER`. L'écran Game Over est masqué et tous les éléments permanents sont restaurés.

6. **Z-order.** Rendu au-dessus de tous les autres éléments HUD.

7. **Pas d'écran victoire dans S13.** `all_waves_complete` (S03) n'affiche rien en S13. Le feedback de fin de session est délégué à S11.

### States and Transitions

#### HUD Root

| État | Condition d'entrée | Condition de sortie | Apparence |
|------|--------------------|---------------------|-----------|
| `PLAYING` | `game_state_changed(PRE_WAVE \| COMBAT \| POST_WAVE)` depuis S11 | `game_state_changed(GAME_OVER)` | Trois éléments permanents visibles, pleine opacité. Aucun overlay. |
| `GAME_OVER` | `game_state_changed(GAME_OVER)` depuis S11 | `game_state_changed(PRE_WAVE)` (retry déclenché par S12) | Éléments permanents masqués. Overlay Game Over affiché (texte + prompt retry). |

```
PLAYING ──[game_state_changed(GAME_OVER)]──> GAME_OVER
GAME_OVER ──[game_state_changed(PRE_WAVE)]──> PLAYING
```

#### HP Bar

| État | Condition d'entrée | Condition de sortie | Apparence |
|------|--------------------|---------------------|-----------|
| `NORMAL` | Démarrage session (current_hp > 6). Re-entré après HIT_FLASH si current_hp > 6. | `player_hp_changed` avec current_hp ≤ 6, ou `player_hit` reçu | Remplissage proportionnel, couleur blanc (L100%). Aucune animation. |
| `LOW_HP` | `player_hp_changed` avec current_hp ≤ 6 | `player_hp_changed` avec current_hp > 6 (via reset S12 uniquement — pas de soins en MVP) | Remplissage proportionnel, couleur orange alert (H28°/S85%/L55°). Pulse alpha actif. |
| `HIT_FLASH` | `player_hit` reçu | 440 ms écoulés | Flash overlay orange (440 ms) concurrent avec la mise à jour du fill. Retour à NORMAL ou LOW_HP selon current_hp à l'expiration. |

```
NORMAL ──[player_hit]──────────────────────────> HIT_FLASH ──[440ms]──> NORMAL ou LOW_HP
NORMAL ──[player_hp_changed, hp ≤ 6]──────────> LOW_HP
LOW_HP ──[player_hit]──────────────────────────> HIT_FLASH ──[440ms]──> LOW_HP
LOW_HP ──[player_hp_changed, hp > 6 via reset]─> NORMAL
```

Note : HIT_FLASH est un overlay concurrent, pas un état bloquant. Le fill reflète toujours `current_hp` en temps réel — un testeur QA peut vérifier : `player_hit(7, MELEE, 5)` → barre affiche 5/20 ET flash orange joue en même temps.

#### Wave Counter

| État | Condition d'entrée | Condition de sortie | Apparence |
|------|--------------------|---------------------|-----------|
| `IDLE` | Démarrage session. Re-entré après ANNOUNCING à l'expiration (1200 ms). | `wave_started` depuis S03 | Affiche `"N/3"` (dernière vague confirmée). |
| `ANNOUNCING` | `wave_started(N)` reçu | 1200 ms écoulés | Affiche `"N/3"` dans le compteur + overlay `"VAGUE N"` actif. |

```
IDLE ──[wave_started(N)]──> ANNOUNCING ──[1200ms]──> IDLE
```

Note : le texte `"N/3"` est mis à jour à l'instant de `wave_started`, pas après l'expiration de l'animation.

#### Object Silhouette

| État | Condition d'entrée | Condition de sortie | Apparence |
|------|--------------------|---------------------|-----------|
| `EMPTY` | Démarrage session. Re-entré à `throw_performed`. | `grab_performed` | Slot fond 80×80 px visible. `TextureRect` masqué. |
| `SHOWING` | `grab_performed` | `throw_performed` ou `carry_interrupted` (objet détruit en portage) | Silhouette 64×64 px de l'objet tenu affichée. Statique. |

```
EMPTY ──[grab_performed]──────> SHOWING ──[throw_performed]──────> EMPTY
                                 SHOWING ──[carry_interrupted]──> EMPTY
```

### Interactions with Other Systems

**1. S07 — HealthSystem**

`player_hp_changed(current_hp: int, max_hp: int)` :
- HP Bar fill ratio = `float(current_hp) / float(max_hp)`, mis à jour immédiatement (même frame).
- État couleur réévalué : current_hp ≤ 6 → ALERT (orange) ; current_hp > 6 → NORMAL (blanc).
- HUD n'émet rien en retour.

`player_hit(damage: int, type: DamageType, current_hp: int)` :
- HP Bar : hit flash 440 ms en concurrent avec la mise à jour du fill.
- `type` et `damage` non affichés dans S13 en MVP. `type` ignoré par S13 (consommé par S11 pour camera shake — OQ-01 S07).

**2. S03 — WaveSystem**

`wave_started(wave_number: int)` :
- Compteur : texte → `str(wave_number) + "/3"` instantanément. Transition IDLE → ANNOUNCING.
- Overlay annonce déclenché : animation 1200 ms, input jamais bloqué.
- Après 1200 ms : ANNOUNCING → IDLE, overlay masqué, compteur reste à `"N/3"`.

**3. ADR-0001 — GrabSystem**

`grab_performed(object: RigidBody3D)` :
- Silhouette : EMPTY → SHOWING. `TextureRect.texture` ← `object.silhouette_texture`.

`throw_performed` :
- Silhouette : SHOWING → EMPTY. Masquage immédiat, même frame.

**4. S11 — GameStateManager**

`game_state_changed(new_state: GameState)` :

| new_state | Action HUD |
|-----------|-----------|
| `PRE_WAVE` | Si depuis GAME_OVER : masquer overlay, restaurer PLAYING + éléments permanents. Si depuis démarrage : no-op (déjà PLAYING). |
| `COMBAT` | Aucun changement (PLAYING continue). |
| `POST_WAVE` | Aucun changement (PLAYING continue). |
| `GAME_OVER` | Masquer éléments permanents + toute animation en cours. Afficher overlay Game Over. Activer écoute input `retry`. |
| `VICTORY` | Différé (spécification hors scope S13 MVP). |

S13 est **read-only** sur tous les systèmes. Seul signal émis par S13 : `retry_requested()` → S11, uniquement depuis l'état GAME_OVER.

## Formulas

### F1 — HP Bar Fill Ratio

```
fill_ratio = clamp(float(current_hp) / float(max_hp), 0.0, 1.0)
```

| Symbole | Type | Plage | Description |
|---------|------|-------|-------------|
| `current_hp` | int | [0, 20] | HP courant du joueur, reçu via `player_hp_changed` depuis S07. |
| `max_hp` | int | [1, 20] | HP maximum, reçu via `player_hp_changed`. Garanti ≥ 1 par S07. |
| `fill_ratio` | float | [0.0, 1.0] | Proportion de la barre à remplir. Clampé pour se prémunir de valeurs hors contrat. |

Exemple : `current_hp = 5`, `max_hp = 20` → `fill_ratio = 5/20 = 0.25`

### F2 — HP Bar Pixel Width

```
bar_width_px = HP_BAR_WIDTH × fill_ratio
```

| Symbole | Type | Plage | Description |
|---------|------|-------|-------------|
| `HP_BAR_WIDTH` | int | {160} | Largeur totale de la barre (tuning knob, MVP = 160 px). |
| `fill_ratio` | float | [0.0, 1.0] | Sortie de F1. |
| `bar_width_px` | float | [0.0, 160.0] | Largeur appliquée au `ColorRect` de remplissage (`fill_rect.size.x`). |

Exemple : `fill_ratio = 0.25` → `bar_width_px = 160 × 0.25 = 40 px`

### F3 — Low-HP State Check

```
is_low_hp = (current_hp ≤ HP_LOW_THRESHOLD)
```

| Symbole | Type | Plage | Description |
|---------|------|-------|-------------|
| `current_hp` | int | [0, 20] | HP courant, du dernier signal `player_hp_changed`. |
| `HP_LOW_THRESHOLD` | int | {6} | Seuil (≈ 30% de HP_JOUEUR_MAX=20). Défini aussi dans S07 F3 — valeurs doivent rester synchronisées. |
| `is_low_hp` | bool | {true, false} | true → état ALERT (orange + pulse). false → état NORMAL (blanc). |

Exemples : `current_hp = 6` → `6 ≤ 6 = true` → ALERT. `current_hp = 7` → `7 ≤ 6 = false` → NORMAL.

**Note cross-système** : S07 définit la même expression. S13 la recalcule localement depuis le signal. Si `HP_LOW_THRESHOLD` change dans S07 Tuning Knobs, le même changement doit être appliqué dans les Tuning Knobs de S13.

### F4 — Hit Flash Total Duration

```
HIT_FLASH_TOTAL = HIT_FLASH_FADE_IN + HIT_FLASH_HOLD + HIT_FLASH_FADE_OUT
```

| Symbole | Type | MVP | Description |
|---------|------|-----|-------------|
| `HIT_FLASH_FADE_IN` | int ms | 80 | Fade-in, alpha 0 → 1, linéaire. |
| `HIT_FLASH_HOLD` | int ms | 80 | Hold, alpha constant à 1. |
| `HIT_FLASH_FADE_OUT` | int ms | 280 | Fade-out, alpha 1 → 0, linéaire. |
| `HIT_FLASH_TOTAL` | int ms | **440** | Durée totale du cycle. Si `player_hit` arrive avant expiration, tween tué + nouveau cycle depuis alpha 0. |

Exemple : `80 + 80 + 280 = 440 ms`

### F5 — Wave Announcement Total Duration

```
WAVE_ANNOUNCE_TOTAL = WAVE_ANNOUNCE_SCALE_DURATION + WAVE_ANNOUNCE_HOLD_DURATION + WAVE_ANNOUNCE_FADE_DURATION
```

| Symbole | Type | MVP | Description |
|---------|------|-----|-------------|
| `WAVE_ANNOUNCE_SCALE_DURATION` | int ms | 150 | Phase 1 : scale `Vector2(1.3,1.3)` → `Vector2(1.0,1.0)`, EASE_OUT. |
| `WAVE_ANNOUNCE_HOLD_DURATION` | int ms | 750 | Phase 2 : scale et alpha maintenus à 1.0 (gap entre t=150ms et t=900ms). |
| `WAVE_ANNOUNCE_FADE_DURATION` | int ms | 300 | Phase 3 : alpha 1.0 → 0.0, linéaire (t=900ms → t=1200ms). |
| `WAVE_ANNOUNCE_TOTAL` | int ms | **1200** | Durée totale. À l'expiration : `visible = false`, reset scale et alpha. Input jamais bloqué. |

Exemple : `150 + 750 + 300 = 1200 ms`

### F6 — Wave Display String

```
wave_text = str(wave_number) + "/" + str(WAVE_COUNT_TOTAL)
```

| Symbole | Type | Plage | Description |
|---------|------|-------|-------------|
| `wave_number` | int | {1, 2, 3} | Numéro de vague courant, depuis `wave_started(wave_number)` de S03. |
| `WAVE_COUNT_TOTAL` | int | {3} | Nombre total de vagues (constante, défini par S03). |
| `wave_text` | string | {"1/3", "2/3", "3/3"} | Texte rendu par le label compteur. |

Exemples : `wave_number=1` → `"1/3"` ; `wave_number=2` → `"2/3"` ; `wave_number=3` → `"3/3"`.

Note : si S03 émet un `wave_number` hors {1,2,3} (violation de contrat), S13 rend la chaîne telle quelle sans valider — c'est la responsabilité de S03.

## Edge Cases

**EC-01 — HUD init avant la réception du premier signal**

À `_ready()`, aucun signal n'a encore été reçu. Comportement attendu :
- HP bar : affiche `fill_ratio = 1.0` (pleine, blanc) jusqu'au premier `player_hp_changed`.
- Wave counter : affiche `"1/3"` (vague 1 est toujours la première émise).
- Silhouette : état EMPTY, fond 80×80 px visible, `TextureRect` masqué.
- HUD root : état PLAYING.

Aucun état invalide — les valeurs par défaut correspondent à l'état de départ garanti par S07 (HP_JOUEUR_MAX = 20) et S03 (vague 1 en premier).

---

**EC-02 — `player_hit` reçu avec `current_hp = 0` (coup fatal)**

Le signal `player_hit(damage, type, 0)` peut précéder `game_state_changed(GAME_OVER)` d'un frame (S07 émet `player_died`, S11 traite et émet `game_state_changed` le frame suivant).

Comportement :
- HP bar : `fill_ratio = 0.0` (barre vide), hit flash démarre normalement (440 ms).
- Frame suivant : `game_state_changed(GAME_OVER)` → écran Game Over affiché, flash tué immédiatement, éléments permanents masqués.
- S13 n'a pas à détecter `current_hp = 0` lui-même pour déclencher le Game Over — c'est S11 qui orchestre.

---

**EC-03 — `player_hit` en rafale (plusieurs hits en < 440 ms)**

Chaque `player_hit` démarre un nouveau cycle de 440 ms. Si un signal arrive pendant un flash en cours, le tween actif est tué et un nouveau cycle démarre depuis alpha 0. Le fill ratio est mis à jour immédiatement à chaque signal, indépendamment du flash.

Cas limite : 3 hits en 100 ms → flash joue en continu jusqu'à 440 ms après le dernier hit. La barre reflète le `current_hp` correct après chaque signal.

---

**EC-04 — Transition ALERT → NORMAL (reset via S12)**

En MVP, pas de soins pendant la session (S07). Le seul chemin ALERT → NORMAL est le reset S12 après retry.

Comportement au retry : S12 réinitialise S07, qui émet `player_hp_changed(20, 20)`. S13 recalcule `is_low_hp = (20 ≤ 6) = false`, repasse en NORMAL, arrête le pulse (alpha snap à 1.0).

---

**EC-05 — Objet détruit pendant le portage (silhouette bloquée en SHOWING)**

Signal `carry_interrupted(object: RigidBody3D)` ajouté à ADR-0001 GrabSystem (résolution OQ-S13-01, 2026-04-10). S13 souscrit à `carry_interrupted` : transition SHOWING → EMPTY, masquage immédiat du slot. Aucune animation de sortie.

---

**EC-06 — `grab_performed` avec texture silhouette manquante**

Si `silhouette_texture` est `null` ou invalide (asset manquant) :
- S13 affiche l'icône générique de fallback définie dans les ressources du HUD.
- Jamais un slot vide en état SHOWING, jamais une erreur bloquante.
- `push_warning` en console identifiant l'objet concerné.

---

**EC-07 — `wave_started` pendant une annonce en cours**

Impossible en jeu normal (S03 garantit que les vagues sont séquentielles). Si le cas se produit (erreur S03 ou test harness) :
- Tuer le tween actif. Reset `scale = Vector2(1.0, 1.0)`, `modulate.a = 1.0`.
- Démarrer immédiatement la nouvelle animation pour le nouveau `wave_number`.
- Compteur mis à jour au nouveau `wave_number`.

---

**EC-08 — Input `retry` pressé avant affichage de l'écran Game Over**

`game_state_changed(GAME_OVER)` active l'écoute `retry` au même frame que l'affichage. Il n'y a aucune fenêtre où l'écoute serait active sans l'écran visible — la cohérence est garantie par le traitement frame-by-frame du signal S11.

## Dependencies

### S13 dépend de

| Système | Direction | Interface | Notes |
|---------|-----------|-----------|-------|
| **S07 — Santé joueur** | S07 → S13 | `player_hp_changed(current_hp, max_hp)`, `player_hit(damage, type, current_hp)` | S13 consomme uniquement. S07 ne connaît pas S13. |
| **S03 — Vagues d'ennemis** | S03 → S13 | `wave_started(wave_number)` | S13 consomme uniquement. |
| **ADR-0001 — GrabSystem** | GrabSystem → S13 | `grab_performed(object: RigidBody3D)`, `throw_performed`, `carry_interrupted(object: RigidBody3D)` | S13 consomme uniquement. |
| **S11 — Gestionnaire d'état** | Bidirectionnel | `game_state_changed(new_state)` (entrant) ; `retry_requested()` (sortant vers S11) | Seul signal que S13 émet activement. |
| **Art bible §7** | Contrainte non-code | Règles visuelles, palette, timings d'animation | Toutes les règles §7 s'appliquent sans exception. |

### S13 est référencé par

| Système | Raison |
|---------|--------|
| **S07 — Santé joueur** | OQ-02 S07 (barre vs chiffre) résolu par S13 : barre uniquement. S07 doit documenter que `player_hp_changed` et `player_hit` sont consommés par S13. |
| **S02 — Saisie et lancer** | S02 GDD UI Requirements : affichage silhouette délégué à S13. OQ-S13-01 (`carry_interrupted`) est un blocker d'intégration S02/S13. |
| **S11 — Gestionnaire d'état** | S11 consomme `retry_requested()` de S13 pour déclencher la séquence retry. |
| **S03 — Vagues d'ennemis** | S03 doit mentionner que `wave_started` est consommé par S13 pour le compteur et l'overlay d'annonce. |

## Tuning Knobs

| Knob | Valeur MVP | Plage sûre | Aspect gameplay affecté |
|------|-----------|-----------|------------------------|
| `HP_BAR_WIDTH` | 160 px | [80, 240] | Lisibilité de la barre. < 80 : illisible périphériquement. > 240 : empiète sur l'écran à 1080p. |
| `HP_BAR_HEIGHT` | 14 px | [8, 24] | Épaisseur visuelle. < 8 : presque invisible. > 24 : trop encombrant. |
| `HP_LOW_THRESHOLD` | 6 | [1, 10] | Seuil d'entrée en ALERT. **Doit rester synchronisé avec S07 Tuning Knobs.** Modifier ici implique de modifier S07. |
| `HP_PULSE_PERIOD` | 800 ms | [400, 1600] | Fréquence du pulse basse vie. < 400 ms : stroboscopique. > 1600 ms : signal d'alerte trop faible. |
| `HIT_FLASH_FADE_IN` | 80 ms | [40, 160] | Attaque du flash. Plus court = réponse plus sèche. |
| `HIT_FLASH_HOLD` | 80 ms | [0, 200] | Durée de plateau du flash. 0 ms acceptable si le fade-in seul suffit. |
| `HIT_FLASH_FADE_OUT` | 280 ms | [100, 500] | Traîne du flash. Plus long = sensation de coup plus lourd. |
| `WAVE_ANNOUNCE_SCALE_DURATION` | 150 ms | [80, 300] | Vitesse de l'impact scale. < 80 ms : imperceptible. > 300 ms : trop lent. |
| `WAVE_ANNOUNCE_HOLD_DURATION` | 750 ms | [300, 1200] | Temps de lecture du texte d'annonce. < 300 ms : illisible. > 1200 ms : nuit au flow. |
| `WAVE_ANNOUNCE_FADE_DURATION` | 300 ms | [150, 600] | Sortie de l'annonce. |

## Visual/Audio Requirements

**Ressources visuelles requises (art pipeline)**

1. **Icône silhouette par objet** — pour chaque objet du catalogue S05 : texture 64×64 px, 1-bit mask blanc (L100%), fond transparent. Format `.png` ou `.webp`, importé comme `CompressedTexture2D`.
2. **Icône silhouette fallback** — texture générique 64×64 px (forme neutre), utilisée quand `silhouette_texture` est `null` (EC-06).
3. **Police** — famille monospace géométrique, poids Bold, fournie comme `FontFile` Godot. Tailles utilisées : 18 px (compteur vague), 24 px (prompt retry), 96 px (annonce vague + Game Over).

**Couleurs** (art bible §7 — aucune déviation autorisée)

| Usage | Couleur | Valeur |
|-------|---------|--------|
| HP bar fill NORMAL | Blanc | H0°/S0%/L100% |
| HP bar fill ALERT + hit flash | Orange alert | H28°/S85%/L55% |
| Silhouette fond | Noir | L0%, alpha 65% |
| Tous les textes | Blanc | L100% |

**Audio** : aucun son propre à S13 en MVP. Le HUD est muet — les retours sonores (hits, saisies, vagues) sont délégués à S14 (Retour audio, V1.0). S13 ne déclenche aucun `AudioStreamPlayer`.

## UI Requirements

**Architecture Godot**

- Nœud racine : `CanvasLayer`, `layer = 1`, `follow_viewport = false`.
- Tous les nœuds enfants : `mouse_filter = MOUSE_FILTER_IGNORE`. Input retry via `_input()` explicite, actif uniquement en état GAME_OVER.
- `StyleBoxFlat` exclusivement pour tout fond coloré. Aucun `border_radius`. Aucun `StyleBoxTexture`.
- Aucun nœud UI permanent au centre de l'écran (art bible §7.1).

**Structure de nœuds recommandée**

```
HUDLayer (CanvasLayer)
├── HPBarContainer (Control, anchor bottom-left)
│   ├── HPBarBackground (ColorRect)
│   ├── HPBarFill (ColorRect)
│   └── HPFlashOverlay (ColorRect, visible=false)
├── WaveCounterLabel (Label, anchor top-center)
├── SilhouetteContainer (Control, anchor bottom-right)
│   └── SilhouetteTexture (TextureRect, visible=false)
├── WaveAnnouncementLabel (Label, anchor center, visible=false)
└── GameOverOverlay (Control, anchor center, visible=false)
    ├── GameOverLabel (Label)
    └── RetryPromptLabel (Label)
```

**Spec UX séparée requise** : une spec UX détaillée doit être créée à `design/ux/hud.md` via `/ux-design` avant le sprint d'implémentation. Cette spec couvre : wireframes, accessibilité (contrastes, tailles minimales), et adaptation résolution (1280×720 → 2560×1440).

## Acceptance Criteria

**AC-01 — HP Bar: Initialization à pleine vie**

Given le HUD est chargé et aucun `player_hp_changed` n'a encore été reçu.
When `_ready()` se termine.
Then la barre affiche `fill_ratio = 1.0`, largeur fill = 160 px, couleur blanche (L100%).

---

**AC-02 — HP Bar: Formule de largeur**

Given la HP bar est en état NORMAL.
When `player_hp_changed(12, 20)` est émis.
Then la largeur du fill `ColorRect` est exactement **96 px** (`160 × 12/20`), mise à jour dans le même frame. Aucun tween sur la largeur.

---

**AC-03 — HP Bar: Transition NORMAL → ALERT au seuil**

Given HP bar en NORMAL (`current_hp = 7`, blanc).
When `player_hp_changed(6, 20)` est émis.
Then couleur → orange alert (H28°/S85%/L55°) instantanément, largeur = **48 px** (`160 × 6/20`). Aucune interpolation.

---

**AC-04 — HP Bar: Transition ALERT → NORMAL**

Given HP bar en ALERT (`current_hp = 5`, orange, pulse actif).
When `player_hp_changed(7, 20)` est émis.
Then couleur → blanc (L100°) instantanément, pulse s'arrête, alpha snap à 1.0.

---

**AC-05 — HP Bar: Timing du hit flash**

Given HP bar dans n'importe quel état.
When `player_hit(3, MELEE, 14)` est émis.
Then un overlay 160×14 px orange exécute : fade-in 80 ms (alpha 0→1), hold 80 ms, fade-out 280 ms (alpha 1→0). Overlay entièrement transparent entre 430 ms et 450 ms après le signal. Fill ratio mis à jour à `current_hp = 14` (largeur = 112 px) dans le même frame, indépendamment du flash.

---

**AC-06 — HP Bar: Reset du hit flash consécutif**

Given un hit flash en cours (alpha > 0).
When un second `player_hit` arrive avant l'expiration des 440 ms.
Then le tween actif est tué immédiatement, overlay alpha reset à 0, nouveau cycle de 440 ms démarre. La durée totale du second flash est 440 ms à compter de la réception du second signal.

---

**AC-07 — HP Bar: Pulse actif en état ALERT**

Given `player_hp_changed(5, 20)` reçu (ALERT).
When 800 ms se sont écoulés.
Then le fill `ColorRect` a complété au moins une oscillation complète alpha 1.0 ↔ 0.55, période 800 ms, easing in-out. Largeur reste à 40 px tout au long — le pulse affecte uniquement l'alpha.

---

**AC-08 — Wave Counter: Initialisation**

Given le HUD chargé, aucun `wave_started` reçu.
When `_ready()` se termine.
Then le `Label` affiche exactement `"1/3"`.

---

**AC-09 — Wave Counter: Mise à jour sur signal**

Given compteur affiche `"1/3"`.
When `wave_started(2)` est émis.
Then `Label.text == "2/3"` dans le même frame. Aucune animation sur le compteur lui-même.

---

**AC-10 — Wave Announcement: Animation + input jamais bloqué**

Given HUD en état PLAYING.
When `wave_started(2)` est émis.
Then :
(a) Un `Label` centré affiche `"VAGUE 2"` en Bold 96 px.
(b) À t=0 ms : `scale = Vector2(1.3, 1.3)` ; ease-out vers `Vector2(1.0, 1.0)` à t=150 ms.
(c) Hold scale=1.0, alpha=1.0 de t=150 ms à t=900 ms.
(d) Alpha tweens 1.0→0.0 entre t=900 ms et t=1200 ms ; `visible = false` à l'expiration.
(e) À n'importe quel instant dans la fenêtre 1200 ms, un input de mouvement joueur ou `grab_performed` est traité normalement — aucun input intercepté, compteur déjà à `"2/3"` dès la réception du signal.

---

**AC-11 — Silhouette: Affichage sur grab, effacement sur throw**

Given HUD en PLAYING, silhouette en état EMPTY (`TextureRect.visible = false`, conteneur 80×80 px visible).
When `grab_performed` est émis avec une texture silhouette valide.
Then `TextureRect.visible = true` dans le même frame, icône 64×64 px centrée (8 px marge). Puis quand `throw_performed` est émis : `TextureRect.visible = false` dans le même frame, aucun fade-out. Le conteneur 80×80 px reste visible en permanence.

---

**AC-12 — Game Over: Affichage et signal retry_requested**

Given HUD en état PLAYING.
When `game_state_changed(GameState.GAME_OVER)` est émis.
Then :
(a) HP bar, compteur, slot silhouette masqués dans le même frame.
(b) Label `"GAME OVER"` (Bold 96 px, blanc, centré) et prompt retry (`"[INPUT] Rejouer"`, Bold 24 px, blanc, 72 px dessous) affichés immédiatement.
(c) L'input `retry` (`is_action_just_pressed("retry")`) émet `retry_requested()` sans délai supplémentaire.
(d) Un `game_state_changed(GameState.PRE_WAVE)` ultérieur masque l'écran Game Over, restaure les trois éléments permanents, et désactive la garde `retry`.

## Open Questions

**OQ-S13-01 — Signal manquant : objet détruit pendant le portage** *(RÉSOLU — 2026-04-10)*

~~S02 ne publie pas de signal `carry_interrupted` quand un objet porté est détruit en vol.~~

**Résolution** : Option A retenue. ADR-0001 mis à jour avec `signal carry_interrupted(object: RigidBody3D)`. Ce signal est distinct de `object_dropped` (dépôt volontaire). S13 souscrit à `carry_interrupted` pour la transition SHOWING → EMPTY. EC-05 est résolu — la silhouette ne restera plus bloquée. Architecture registry mise à jour (`grab_system_signals`).

**OQ-S13-02 — Paramètres du signal `grab_performed`** *(RÉSOLU — 2026-04-10)*

~~ADR-0001 ne précise pas si `grab_performed` transporte une référence à l'objet saisi.~~

**Résolution** : ADR-0001 spécifiait déjà `grab_performed(object: RigidBody3D)` — la référence nœud est transportée. S13 lit `object.silhouette_texture` au moment du signal. Aucune modification d'ADR-0001 requise sur ce point. Option A était déjà implémentée.
