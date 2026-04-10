# S11 — Gestionnaire d'état de jeu

> **Statut**: Approuvé
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-10
> **Implémente le Pilier**: Pilier 2 — Le flow avant le challenge

## Overview

S11 — Gestionnaire d'état de jeu est la FSM centrale qui orchestre le déroulement d'une partie : il reçoit les événements de S03 (vagues) et S07 (santé joueur), et émet `game_state_changed(new_state: GameState)` vers tous les systèmes qui ont besoin de connaître l'état courant. Sa FSM comporte cinq états : PRE_WAVE (avant le premier spawn), COMBAT (vague active), POST_WAVE (délai entre vagues), GAME_OVER (joueur mort) et VICTORY (3 vagues survivées). S11 est aussi le coordinateur des effets de transition : sur GAME_OVER, il appelle `freeze()` sur S10 (caméra), et orchestre le retry en moins de 3 secondes (Pilier 2). Pendant GAME_OVER, S11 peut aussi recevoir `retry_requested()` depuis S13 (HUD) pour déclencher un retry immédiat ; à défaut d'input, il déclenche un auto-retry après `RETRY_DELAY`. Pour le joueur, S11 est totalement invisible — il ne ressent que ses effets : le fait que les ennemis arrivent au bon moment, que la mort déclenche un retry rapide, que la victoire est bien reconnue. S11 est le chef d'orchestre silencieux qui fait tenir ensemble tous les autres systèmes.

## Player Fantasy

Le joueur est le soliste. Il improvise, il enchaîne, il s'exprime. Mais derrière le rideau, quelqu'un donne les départs : le premier ennemi entre sur le temps fort, la respiration entre les vagues est une mesure de silence, le game-over est un silence d'une demi-seconde avant le rembobinage. S11 est ce chef d'orchestre que le public ne voit jamais mais sans lequel le concert s'effondre. Le retry rapide n'est pas une fonctionnalité — c'est l'anacrouse du mouvement suivant. La victoire n'est pas une récompense — c'est la résolution de la cadence finale.

*Pilier servi : Pilier 2 — "Le flow avant le challenge." S11 est la garantie structurelle que la fluidité ne se brise jamais contre un écran de chargement, un menu de game-over, ou une transition mal timée.*

## Detailed Design

### Core Rules

1. **FSM centralisée** : S11 maintient un `current_state: GameState` (enum défini dans S11, contrat de signaux). Seul S11 peut changer l'état — aucun autre système ne modifie `current_state` directement.

2. **Transition vers PRE_WAVE au démarrage** : à `_ready()`, S11 émet `game_state_changed(PRE_WAVE)`. PRE_WAVE est l'état initial — sa durée est calibrée au prototype (peut être 0s en MVP).

3. **PRE_WAVE → COMBAT** : S11 émet `game_state_changed(COMBAT)` après le délai PRE_WAVE, déclenchant le spawn de la vague 1 dans S03.

4. **COMBAT → POST_WAVE** : S11 écoute `wave_cleared(wave_number, enemies_killed)` de S03. Sur réception → émet `game_state_changed(POST_WAVE)`. POST_WAVE dure le temps que S03 attende (INTER_WAVE_DELAY), puis S03 émet `wave_started`.

5. **POST_WAVE → COMBAT** : S11 écoute `wave_started(wave_number)` de S03. Sur réception → émet `game_state_changed(COMBAT)`.

6. **COMBAT → GAME_OVER** : S11 écoute `player_died()` de S07. Sur réception, quelle que soit la vague en cours → émet `game_state_changed(GAME_OVER)` → appelle `freeze()` sur S10 → planifie un auto-retry après `RETRY_DELAY` (≤ 3 s, Pilier 2) via S12. La réinitialisation est déléguée à S12.

7. **POST_WAVE → GAME_OVER** : `player_died` pendant POST_WAVE déclenche GAME_OVER immédiatement — la prochaine vague ne démarre pas.

8. **→ VICTORY** : S11 écoute `all_waves_complete()` de S03. Sur réception → émet `game_state_changed(VICTORY)`. VICTORY est un état terminal en MVP (pas de suite de niveaux).

9. **Aucune logique de gameplay** : S11 orchestre des transitions d'état et des appels d'API (`freeze()`, retry). Il ne calcule pas de dégâts, ne spawne pas d'ennemis, ne gère pas la caméra au-delà de l'appel `freeze()` (en MVP, l'unfreeze est implicite via le reload S12).

10. **Retry demandé par le HUD** : pendant GAME_OVER uniquement, S11 écoute `retry_requested()` de S13. Sur réception → déclenche le retry immédiatement via S12 (sans attendre `RETRY_DELAY`) et annule toute minuterie d'auto-retry encore active.

### States and Transitions

| État | Description | Entrée | Sorties possibles |
|------|-------------|--------|-------------------|
| `PRE_WAVE` | Pause initiale avant la première vague | `_ready()` | → `COMBAT` après délai initial |
| `COMBAT` | Vague active, ennemis en jeu | PRE_WAVE terminé · `wave_started` de S03 | → `POST_WAVE` sur `wave_cleared` · → `GAME_OVER` sur `player_died` |
| `POST_WAVE` | Délai inter-vague (géré par S03) | `wave_cleared` de S03 | → `COMBAT` sur `wave_started` · → `GAME_OVER` sur `player_died` |
| `GAME_OVER` | Joueur mort — retry en cours | `player_died` de S07 | → rechargement de scène via S12 (auto après `RETRY_DELAY` ou immédiat sur `retry_requested`) ; nouvelle instance repart en `PRE_WAVE` |
| `VICTORY` | 3 vagues survivées | `all_waves_complete` de S03 | → aucune (terminal en MVP) |

### Interactions with Other Systems

| Système | Direction | Interface |
|---------|-----------|-----------|
| S03 — Vagues d'ennemis | S03 → S11 | `wave_started`, `wave_cleared`, `all_waves_complete` |
| S03 — Vagues d'ennemis | S11 → S03 | `game_state_changed` → S03 démarre le spawn sur `COMBAT` |
| S07 — Santé joueur | S07 → S11 | `player_died()` → transition GAME_OVER |
| S10 — Caméra TPS | S11 → S10 | `freeze()` sur GAME_OVER (unfreeze implicite via reload S12 en MVP) |
| S12 — Retry / réinitialisation | S11 → S12 | Appel direct `S12.retry()` (auto après `RETRY_DELAY` ou immédiat sur `retry_requested`) |
| S13 — HUD | S11 → S13 | `game_state_changed` → S13 met à jour les affichages d'état |
| S13 — HUD | S13 → S11 | `retry_requested()` (uniquement en GAME_OVER) |

## Formulas

S11 est une FSM pure — pas de formules numériques. Les seuls temporisateurs sont des constantes :

| Constante | Rôle | Valeur |
|-----------|------|--------|
| `PRE_WAVE_DELAY` | Durée de l'état PRE_WAVE avant le premier spawn | 0.0 s (défaut — calibrer au prototype) |
| `RETRY_DELAY` | Délai entre GAME_OVER et le déclenchement du retry | 2.0 s (≤ 3 s, Pilier 2) |

## Edge Cases

**EC-01 — player_died reçu pendant GAME_OVER (double mort)**
Ignoré. S11 est déjà en GAME_OVER — aucun second `game_state_changed(GAME_OVER)` n'est émis.

**EC-02 — all_waves_complete reçu pendant GAME_OVER**
Ignoré. GAME_OVER est prioritaire sur VICTORY. Le joueur est mort — la session est terminée.

**EC-03 — wave_started reçu pendant GAME_OVER**
Ignoré. S11 bloque tout input externe quand il est en GAME_OVER.

**EC-04 — player_died reçu pendant PRE_WAVE**
Transition GAME_OVER immédiate, même avant la première vague. Comportement extrême (joueur tué avant le premier spawn) — possible si la scène est mal configurée.

**EC-05 — Retry échoue (S12 ne répond pas dans RETRY_DELAY)**
S12 n'émet pas de signal de succès/échec en MVP : il déclenche un `reload_current_scene()` et la scène repart. Si le temps de reload dépasse le budget (voir S12 EC-01), c'est un problème de performance/poids de scène (pas un problème de logique S11). Aucun fallback en MVP.

## Dependencies

### Upstream (S11 dépend de)

| Système | Ce que S11 consomme |
|---------|---------------------|
| S07 — Santé joueur | Signal `player_died()` → transition GAME_OVER |
| S03 — Vagues d'ennemis | Signaux `wave_started`, `wave_cleared`, `all_waves_complete` → transitions FSM |

### Downstream (dépend de S11)

| Système | Ce que S11 fournit |
|---------|--------------------|
| S03 — Vagues d'ennemis | Signal `game_state_changed` → S03 démarre le spawn sur COMBAT |
| S10 — Caméra TPS | Appel `freeze()` sur GAME_OVER (reset implicite via reload S12 en MVP) |
| S12 — Retry / réinitialisation | Déclenchement de la réinitialisation après RETRY_DELAY |
| S13 — HUD | Signal `game_state_changed` → S13 met à jour les affichages |

## Tuning Knobs

| # | Constante | Défaut | Plage sûre | Effet gameplay |
|---|-----------|--------|------------|----------------|
| 1 | `PRE_WAVE_DELAY` | 0.0 s | [0.0, 3.0] | Pause avant la première vague. 0 = direct (MVP). > 0 = espace pour un texte d'intro ou un décompte. |
| 2 | `RETRY_DELAY` | 2.0 s | [0.5, 3.0] | Délai avant retry après GAME_OVER. < 0.5s = trop brutal. > 3s = viole Pilier 2 (flow avant challenge). |

## Visual/Audio Requirements

- **Pas d'effet visuel propre à S11** : les transitions d'état sont communiquées via `game_state_changed` → S13 gère l'affichage.
- **Son de game-over / victoire** : hors scope S11 — géré par S14 (retour audio, V1.0).
- **Freeze caméra sur GAME_OVER** : appel direct de `freeze()` sur S10, pas d'effet post-process ajouté par S11.

## UI Requirements

- **Aucune UI propre à S11** : toutes les informations d'état sont communiquées via `game_state_changed` → S13 (HUD) gère l'affichage (notamment l'écran de game-over).
- **Écran GAME_OVER** : spécifié dans le GDD S13. **VICTORY** : pas d'écran dédié en MVP (no-op côté HUD) ; V1.0 pourra ajouter un écran/feedback.

## Acceptance Criteria

**AC-01** — Au démarrage, S11 passe en PRE_WAVE et émet `game_state_changed(PRE_WAVE)`.

**AC-02** — `game_state_changed(COMBAT)` est émis avant le premier spawn de la vague 1.

**AC-03** — `game_state_changed(POST_WAVE)` est émis dans la même frame où `wave_cleared` est reçu de S03.

**AC-04** — Sur `player_died`, `game_state_changed(GAME_OVER)` est émis et `freeze()` sur S10 est appelé dans la même frame.

**AC-05** — Après GAME_OVER, le retry se déclenche en ≤ `RETRY_DELAY` (≤ 3 s — Pilier 2).

**AC-06** — Sur `all_waves_complete`, `game_state_changed(VICTORY)` est émis et aucun spawn supplémentaire ne se produit.

**AC-07** — Un second `player_died` reçu pendant GAME_OVER n'émet pas un second `game_state_changed(GAME_OVER)`.

**AC-08** — S11 n'expose aucune méthode publique de changement d'état — la FSM ne peut être pilotée que par les signaux entrants.

**AC-09** — Pendant GAME_OVER, à réception de `retry_requested()` de S13, S11 déclenche le retry via S12 dans la même frame (sans attendre `RETRY_DELAY`).

## Open Questions

**OQ-01** — (Résolu) Interface S11 → S12 pour le retry : appel direct `S12.retry()` via une référence `@export` vérifiée en `_ready()` (MVP).

**OQ-02** — PRE_WAVE_DELAY à 0s : en MVP, pas de délai initial. Si un écran d'intro est ajouté, PRE_WAVE_DELAY devient le budget de cet écran — à décider au design UX.
