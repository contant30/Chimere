# S03 — Vagues d'ennemis

> **Statut**: In Review
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-10
> **Implémente le Pilier**: Pilier 2 — Le flow avant le challenge

## Overview

S03 — Vagues d'ennemis est le système qui structure le combat dans le temps : il orchestre l'apparition des ennemis en trois vagues successives (3 / 5 / 7 ennemis), gère le délai de respiration entre chaque vague (3 secondes), et suit en temps réel le compte des ennemis encore en vie pour détecter la fin de vague. Techniquement, S03 est un `WaveManager` (Node) qui instancie les scènes ennemies (S09) aux points de spawn définis dans la pièce, injecte leurs dépendances, et écoute le signal `enemy_died` de chaque instance S08 pour décrémenter son compteur interne. S03 écoute `game_state_changed` de S11 pour savoir quand lancer le spawn, et publie `wave_started`, `wave_cleared` et `all_waves_complete` pour que S11 orchestre les transitions d'état global. Pour le joueur, S03 est invisible — il n'existe que comme la pression qui monte : d'abord trois ennemis qu'on peut traiter un par un, puis cinq qui commencent à se gêner, puis sept qui transforment la pièce en chaos maîtrisé. Le rythme des vagues est la structure rythmique du jeu ; S03 en est le métronome.

## Player Fantasy

Le joueur ne sait pas qu'il joue contre un orchestrateur. Il sait que la pièce est de moins en moins vide, que ses angles de fuite se ferment, que le prochain lancer devra compter. La pression des vagues transforme des gestes libres en chorégraphie : sans elle, le joueur jette des objets dans le vide. Avec elle, chaque lancer a un destinataire, chaque pas a une raison. Les ennemis qui entrent ne sont pas un défi — ils sont le public qui donne un sens à la performance.

*Pilier servi : Pilier 2 — "Le flow avant le challenge." Les vagues structurent le temps sans jamais l'arrêter — la respiration entre les vagues est l'inspiration avant la phrase suivante, pas un écran de chargement.*

## Detailed Design

### Core Rules

1. **Structure des vagues** : 3 vagues définies statiquement en MVP.

   | Vague | Ennemis à spawner | Type |
   |-------|-------------------|------|
   | 1 | 3 | Basique (HP=12) |
   | 2 | 5 | Basique (HP=12) |
   | 3 | 7 | Basique (HP=12) |

2. **Spawn** : S03 instancie les scènes ennemies (S09) depuis une liste de `SpawnPoint` (Node3D) disposés dans la pièce. Les ennemis sont spawnés un par un avec un délai de `SPAWN_INTERVAL` (0.5 s) entre chaque instance pour éviter un rush simultané.

3. **Injection de dépendances au spawn** : avant `add_child()`, S03 injecte les `@export` de S09 : `player`, `wave_manager` (self), `score_manager`, `vfx_manager`. Conforme à S09, Règle 2.

4. **Compteur d'ennemis en vie** : S03 maintient `enemies_alive: int`. Incrémenté à chaque spawn, décrémenté à chaque `enemy_died` reçu.

5. **Détection de fin de vague** : quand `enemies_alive == 0` et la vague courante est active, S03 émet `wave_cleared(wave_number, enemies_killed)`, puis :
   - Si `wave_number < 3` → attend `INTER_WAVE_DELAY` (3 s) → émet `wave_started(wave_number + 1)` → spawn la vague suivante.
   - Si `wave_number == 3` → émet `all_waves_complete()` → passe en état DONE.

6. **Démarrage conditionnel** : S03 écoute `game_state_changed` de S11. Il commence à spawner uniquement quand `new_state == GameState.COMBAT`. Toute autre transition est ignorée.

7. **Un seul spawn par état COMBAT** : S03 ne spawne qu'une vague par transition vers COMBAT. Deux vagues simultanées sont impossibles.

8. **Pas de respawn intra-vague** : les ennemis morts ne sont pas remplacés au sein d'une vague. La vague se termine quand tous les ennemis spawnés sont morts.

### States and Transitions

| État | Description | Transitions sortantes |
|------|-----------|-----------------------|
| `IDLE` | En attente du signal COMBAT de S11 | → `SPAWNING` sur `game_state_changed(COMBAT)` |
| `SPAWNING` | Spawn des ennemis de la vague courante (1 tous les SPAWN_INTERVAL) | → `WAVE_ACTIVE` quand tous les ennemis de la vague sont spawnés |
| `WAVE_ACTIVE` | Vague en cours, `enemies_alive > 0` | → `POST_WAVE` quand `enemies_alive == 0` |
| `POST_WAVE` | Délai de INTER_WAVE_DELAY avant la prochaine vague | → `SPAWNING` (vague suivante) si `wave_number < 3` · → `DONE` si `wave_number == 3` |
| `DONE` | `all_waves_complete()` émis, session terminée | → aucune |

### Interactions with Other Systems

| Système | Direction | Interface |
|---------|-----------|-----------|
| S09 — IA ennemie | S03 → S09 | Instanciation + injection `@export` + `add_child()` à chaque spawn |
| S08 — Santé ennemie | S08 → S03 | `enemy_died(enemy: Node)` → décrémente `enemies_alive` |
| S11 — Gestionnaire d'état | S11 → S03 | `game_state_changed(new_state)` → démarre le spawn si `COMBAT` |
| S11 — Gestionnaire d'état | S03 → S11 | Signaux `wave_started`, `wave_cleared`, `all_waves_complete` |

## Formulas

### F1 — Ennemis par vague

```
enemies_in_wave[n] = WAVE_SIZES[n]   # tableau statique [3, 5, 7], n ∈ {0, 1, 2}
```

Pas de formule dynamique en MVP — valeurs définies dans `WAVE_SIZES`.

### F2 — Compteur d'ennemis en vie

```
enemies_alive += 1   # à chaque spawn
enemies_alive -= 1   # à chaque enemy_died reçu
fin_de_vague = (enemies_alive == 0)
```

### F3 — Ennemis tués (paramètre de wave_cleared)

```
enemies_killed = WAVE_SIZES[wave_number]   # tous morts pour que la vague se termine
```

## Edge Cases

**EC-01 — player_died pendant une vague active**
S03 n'écoute pas `player_died`. S11 reçoit ce signal, passe en GAME_OVER, et est responsable de nettoyer S03 (appel de `abort()` ou via queue_free de la scène de jeu). S03 reste en WAVE_ACTIVE jusqu'à ce nettoyage.

**EC-02 — SpawnPoint occupé**
Si un ennemi occupe déjà un SpawnPoint au moment du spawn, le nouvel ennemi est instancié au même point — Jolt gère la séparation physique. Aucune logique de détection d'occupation en MVP.

**EC-03 — Moins de SpawnPoints que d'ennemis dans la vague**
S03 boucle sur la liste via `index % spawn_points.size()`. Si moins de 7 points, certains sont réutilisés pour la vague 3.

**EC-04 — enemy_died reçu après DONE**
Si un signal `enemy_died` arrive après que S03 est en état DONE (délai de queue_free résiduel), il est ignoré — `enemies_alive` est clampé à `max(0, enemies_alive - 1)` et aucun signal supplémentaire n'est émis.

## Dependencies

### Upstream (S03 dépend de)

| Système | Ce que S03 consomme |
|---------|---------------------|
| S08 — Santé ennemie | Signal `enemy_died(enemy: Node)` → décrémente `enemies_alive` |
| S11 — Gestionnaire d'état | Signal `game_state_changed(new_state)` → démarre le spawn sur `COMBAT` |

### Downstream (dépend de S03)

| Système | Ce que S03 fournit |
|---------|--------------------|
| S09 — IA ennemie | Instanciation + injection `@export` au spawn |
| S11 — Gestionnaire d'état | Signaux `wave_started`, `wave_cleared`, `all_waves_complete` |

## Tuning Knobs

| # | Constante | Défaut | Plage sûre | Effet gameplay |
|---|-----------|--------|------------|----------------|
| 1 | `WAVE_SIZES` | [3, 5, 7] | V1 : [2–5] · V2 : [3–8] · V3 : [5–12] | Volume de pression par vague. Au-delà de 10 ennemis simultanés, risque de saturation du pathfinding. |
| 2 | `INTER_WAVE_DELAY` | 3.0 s | [1.5, 6.0] | Respiration entre vagues. < 1.5s = frustrant, > 6s = rupture du flow (Pilier 2). |
| 3 | `SPAWN_INTERVAL` | 0.5 s | [0.2, 1.5] | Délai entre chaque spawn intra-vague. Trop court = rush simultané. Trop long = vague qui semble molle. |

## Visual/Audio Requirements

- **Signal visuel de fin de vague** : hors scope S03 — géré par S11 et S13 (HUD).
- **Son de spawn** : hors scope S03 — S03 n'émet pas de son. Le retour audio des ennemis qui apparaissent est géré par S14 (retour audio, V1.0).
- **Pas d'effet de spawn en MVP** : les ennemis apparaissent directement à leur SpawnPoint, sans animation d'entrée.

## UI Requirements

- **Compteur de vague** : S03 publie `wave_started(wave_number)` → S13 (HUD) affiche "Vague X / 3". Hors scope S03.
- **Pas d'UI propre à S03** : toute l'information de vague est communiquée via signaux vers S13.

## Acceptance Criteria

**AC-01** — La vague 1 spawne exactement 3 ennemis, la vague 2 exactement 5, la vague 3 exactement 7.

**AC-02** — Aucun ennemi d'une nouvelle vague n'apparaît avant que `INTER_WAVE_DELAY` (3 s) ne soient écoulés depuis `wave_cleared`.

**AC-03** — `wave_cleared` est émis exactement quand le dernier ennemi de la vague courante meurt — ni avant, ni après.

**AC-04** — `all_waves_complete` est émis exactement une fois, après `wave_cleared` de la vague 3.

**AC-05** — Les ennemis d'une vague sont spawnés un par un avec `SPAWN_INTERVAL` (0.5 s) d'intervalle — pas de spawn simultané groupé.

**AC-06** — Si `player_died` est émis pendant une vague, S03 n'émet aucun signal supplémentaire (`wave_cleared` ou `all_waves_complete` ne sont pas déclenchés).

**AC-07** — S03 ne commence à spawner que lorsque `game_state_changed(COMBAT)` est reçu de S11.

## Open Questions

**OQ-01** — Méthode `abort()` sur S03 : S11 doit pouvoir interrompre S03 en cas de GAME_OVER. L'interface exacte (`abort()`, ou queue_free de la scène parente) est à définir lors du prototype S11.

**OQ-02** — Nombre de SpawnPoints minimum : la vague 3 spawne 7 ennemis. Si la pièce ~10×10m n'a que 4 SpawnPoints, EC-03 s'applique. Définir le nombre et la position des SpawnPoints au prototype niveau design.
