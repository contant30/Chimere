# S12 — Retry / réinitialisation

> **Statut**: In Review
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-10
> **Implémente le Pilier**: Pilier 2 — Le flow avant le challenge

## Overview

S12 — Retry / réinitialisation est le mécanisme qui ramène le joueur à l'état initial après un GAME_OVER. Son rôle est unique et minimal : déclenché par S11 après `RETRY_DELAY`, il appelle `SceneTree.reload_current_scene()`, ce qui détruit et recrée l'intégralité de la scène de jeu — joueur, ennemis, objets, caméra, gestionnaire de vagues — dans un état vierge garanti. S12 ne gère pas de transitions visuelles (hors scope MVP), ne maintient aucun état persistant entre les tentatives, et n'a aucune logique de gameplay propre. Pour le joueur, S12 est la promesse tenue par Pilier 2 : après GAME_OVER, la partie reprend en moins de 3 secondes, sans friction, sans menu intermédiaire, comme si le mouvement n'avait jamais été interrompu.

## Player Fantasy

La mort n'est pas une fin de partie — c'est l'expiration d'une phrase. Le joueur ne quitte jamais la pièce : il reprend son souffle. En moins de trois secondes, la pièce est neuve, les mains sont vides, les ennemis n'existent pas encore. Ce moment de vide est imperceptible par design : le joueur ne le remarque que par son absence de friction. Quand il le cherche, il est déjà passé. La seule chose que le joueur emporte d'une tentative à l'autre, c'est son instinct — l'objet qu'il saisira en premier n'est plus le même.

*Pilier servi : Pilier 2 — "Le flow avant le challenge." S12 est la garantie structurelle que la mort ne crée jamais de friction : pas d'écran de game-over, pas de menu, pas d'attente visible. Et par extension : Pilier 1 (les mains reviennent vides, prêtes à saisir) et Pilier 3 (l'instinct évolue — chaque tentative est une expression, pas une répétition).*

## Detailed Design

### Core Rules

1. **Responsabilité unique** : S12 expose une seule méthode publique, `retry()`. Quand appelée, elle déclenche `get_tree().reload_current_scene()`. C'est la totalité de la logique de S12.

2. **Déclenchement exclusif par S11** : S12 ne s'autodéclenche jamais. Seul S11 appelle `retry()`, après `RETRY_DELAY` (2 s), depuis l'état GAME_OVER.

3. **Reset garanti par le moteur** : `reload_current_scene()` détruit et recrée l'intégralité de la scène active (joueur, ennemis, objets, caméra, S03, S07, S08, S09, S10, S11, S13). Aucun système n'a besoin d'implémenter une méthode `reset()` — le moteur garantit un état vierge.

4. **Aucun état persistant** : S12 ne maintient aucune variable entre les tentatives. Le nombre de tentatives, le score, et toute progression sont hors scope MVP.

5. **Idempotence** : si `retry()` est appelée plusieurs fois avant la fin du reload (impossible par design — S11 est en GAME_OVER donc bloqué), les appels supplémentaires sont ignorés par le moteur (déjà en cours de reload).

6. **Pas de transition visuelle en MVP** : le fade-out / fade-in est hors scope. La scène repart directement depuis `_ready()` de tous les nodes. Fonctionnalité optionnelle V1.0.

### States and Transitions

S12 est sans état observable. Du point de vue du joueur et des autres systèmes, S12 n'a pas de FSM — il existe entre le signal de S11 et l'exécution du reload.

| Phase | Description |
|-------|-------------|
| Attente | S12 est instancié, `retry()` n'a pas été appelée. Dure toute la partie. |
| Reload | `retry()` appelée → `reload_current_scene()` → scène détruite en fin de frame → scène recréée début de frame suivante. S12 cesse d'exister pendant ce processus. |

### Interactions with Other Systems

| Système | Direction | Interface |
|---------|-----------|-----------|
| S11 — Gestionnaire d'état | S11 → S12 | Appel direct `retry()` après `RETRY_DELAY` |
| Tous les autres systèmes | S12 → tous | Implicite — `reload_current_scene()` recrée tous les nodes. Aucun appel direct. |

## Formulas

S12 ne contient aucune formule. La seule contrainte temporelle est héritée de S11 :

```
retry_total_time = RETRY_DELAY + scene_reload_time
contrainte : retry_total_time ≤ 3.0 s  (Pilier 2)
```

`RETRY_DELAY` = 2.0 s — défini dans S11, non dupliqué dans S12.
`scene_reload_time` = temps de destruction + rechargement de la scène par Godot. Non contrôlé par S12 — dépend du poids de la scène. Budget implicite : ≤ 1.0 s. À vérifier au prototype.

## Edge Cases

**EC-01 — scene_reload_time dépasse le budget (> 1 s)**
La scène est trop lourde pour respecter la contrainte Pilier 2. Mitigation MVP : alléger la scène (réduire le nombre de nodes, éviter les ressources volumineuses à l'import). Si le problème persiste, envisager `change_scene_to_file()` avec une scène préchargée. À diagnostiquer au prototype.

**EC-02 — retry() appelé pendant que reload est déjà en cours**
Ignoré par le moteur — `reload_current_scene()` est idempotent si déjà en cours. S11 ne peut pas appeler retry() deux fois (bloqué en GAME_OVER), donc ce cas est théoriquement impossible par design.

**EC-03 — Scène corrompue / reload échoue**
Godot ne fournit pas de callback d'échec pour `reload_current_scene()`. En MVP, pas de fallback — un échec de reload est un crash hard. Si observé au prototype, escalader à une solution architecture (ex. retour au main menu).

**EC-04 — retry() appelé hors GAME_OVER (mauvaise connexion S11→S12)**
S12 n'a pas de garde — il exécute `retry()` quelle que soit l'origine de l'appel. La protection est dans S11 (seul S11 peut appeler retry()). Si S11 est mal connecté, le reload survient prématurément. Prévention : connexion S11→S12 via `@export` vérifié en `_ready()`.

## Dependencies

### Upstream (S12 dépend de)

| Système | Ce que S12 consomme |
|---------|---------------------|
| S11 — Gestionnaire d'état | Déclenchement de `retry()` depuis l'état GAME_OVER après `RETRY_DELAY` |

### Downstream (dépend de S12)

Aucune dépendance directe — `reload_current_scene()` recrée tous les systèmes sans que S12 les appelle individuellement.

| Système | Effet du reload |
|---------|-----------------|
| S01 — Déplacement joueur | Recréé depuis zéro via `_ready()` |
| S07 — Santé joueur | HP réinitialisé à `HP_JOUEUR_MAX` (20) automatiquement |
| S08 — Santé ennemie | Toutes les instances ennemies détruites et non recréées (S03 les respawne) |
| S09 — IA ennemie | Idem S08 |
| S03 — Vagues d'ennemis | WaveManager recréé, `wave_number` et `enemies_alive` remis à zéro |
| S10 — Caméra TPS | Recréée depuis zéro — `freeze()` annulé implicitement |
| S11 — Gestionnaire d'état | Recréé depuis zéro, repart en PRE_WAVE via `_ready()` |
| S13 — HUD | Recréé depuis zéro, affichage réinitialisé |

## Tuning Knobs

| # | Constante | Propriétaire | Valeur | Contrainte |
|---|-----------|-------------|--------|------------|
| — | `RETRY_DELAY` | S11 | 2.0 s | ≤ 3 s (Pilier 2) — défini dans S11, référencé ici pour contexte |
| — | `scene_reload_time` | Moteur | ~0.1–0.5 s (estimé) | Budget implicite ≤ 1.0 s pour respecter `retry_total_time ≤ 3 s` |

S12 n'expose aucun tuning knob propre. Si `scene_reload_time` dépasse le budget, la solution est architecturale (alléger la scène ou changer de méthode de reload), pas un paramètre numérique.

## Visual/Audio Requirements

- **Aucun effet visuel propre à S12 en MVP** : la transition GAME_OVER → retry est un cut sec (noir momentané du reload moteur).
- **Fade-out / fade-in** : hors scope MVP — optionnel V1.0, géré par S13 ou un système de transition dédié.
- **Aucun son propre à S12** : les effets sonores de GAME_OVER et de retour au jeu sont hors scope S12 — gérés par S14 (retour audio, V1.0).

## UI Requirements

- **Aucune UI propre à S12** : S12 ne déclenche, ne masque, ni ne modifie aucun élément UI.
- **Écran de GAME_OVER** : géré par S13. S12 ne l'affiche pas et ne le masque pas — le reload le détruit implicitement.
- **Compteur de tentatives** : hors scope MVP.

## Acceptance Criteria

**AC-01** — `retry()` déclenche `reload_current_scene()` dans la même frame où elle est appelée.

**AC-02** — Après reload, le joueur démarre avec `HP_JOUEUR_MAX` (20 HP) — aucune HP résiduelle de la tentative précédente.

**AC-03** — Après reload, `wave_number` de S03 est 0 (première vague) et `enemies_alive` est 0 — aucun ennemi résiduel.

**AC-04** — Après reload, S11 émet `game_state_changed(PRE_WAVE)` via `_ready()` — l'orchestration repart de l'état initial.

**AC-05** — `retry_total_time` (RETRY_DELAY + scene_reload_time) est ≤ 3 s — mesuré au prototype sur la scène MVP.

**AC-06** — S12 n'expose aucune méthode publique autre que `retry()`.

**AC-07** — Si `retry()` est appelée alors que reload est déjà en cours, aucune erreur n'est levée et aucun second reload ne se produit.

## Open Questions

**OQ-01 — Interface S11→S12 : `@export` ou signal ?**
Actuellement spécifié comme appel direct de méthode (`retry()`) via `@export` de S12 dans S11. Alternative : S11 émet un signal `retry_requested` que S12 écoute — découplage plus propre mais moins lisible pour un MVP mono-scène. À décider au prototype S11/S12.

**OQ-02 — scene_reload_time sous Godot 4.6.2 + Jolt**
Le temps réel de `reload_current_scene()` avec Jolt Physics initialisé n'est pas connu avant mesure. Si ≥ 1 s, la contrainte Pilier 2 est à risque. À mesurer en priorité au premier prototype jouable.
