# Systems Index : Saisir

> **Statut** : Approuvé (CD-SYSTEMS skipped — Lean mode)
> **Créé** : 2026-04-07
> **Dernière mise à jour** : 2026-04-08

> **Concept source** : design/gdd/game-concept.md

---

## Vue d'ensemble

Saisir est un brawler 3D TPS en pièce unique. Sa complexité mécanique est délibérément
contenue : une seule scène, pas de progression persistante, pas de contenu procédural.
La profondeur vient des interactions entre les systèmes physiques et l'espace. Le scope
total est 15 systèmes — 13 MVP, 2 V1.0. Le risque principal est concentré sur un seul
système : la saisie/lancer (S02), qui doit être prototypée en semaine 1 pour valider
l'hypothèse centrale du jeu ("les joueurs trouvent la boucle saisir-frapper-enchaîner
intrinsèquement satisfaisante").

---

## Énumération des systèmes

| # | Système | Catégorie | Priorité | Statut | GDD | Dépend de |
|---|---------|-----------|----------|--------|-----|-----------|
| S01 | Déplacement joueur | Joueur | MVP | In Review | `design/gdd/deplacement-joueur.md` | — |
| S02 | Saisie et lancer | Mécanique cœur | MVP | Non commencé | — | S01, S05, S06 |
| S03 | Vagues d'ennemis | Ennemi | MVP | Non commencé | — | S08, S09, S11* |
| S04 | Dégradation d'environnement | Monde | MVP | Non commencé | — | S02, S05 |
| S05 | Catalogue d'objets (inféré) | Données | MVP | Complet | `design/gdd/catalogue-objets.md` | — |
| S06 | Système de dégâts (inféré) | Mécanique cœur | MVP | Complet | `design/gdd/systeme-degats.md` | — |
| S07 | Santé joueur + game-over (inféré) | Joueur | MVP | Non commencé | — | S06 |
| S08 | Santé ennemie + mort ennemi (inféré) | Ennemi | MVP | Non commencé | — | S06 |
| S09 | IA ennemie (inféré) | Ennemi | MVP | Non commencé | — | S01 |
| S10 | Caméra TPS (inféré) | Caméra | MVP | Non commencé | — | S01 |
| S11 | Gestionnaire d'état de jeu (inféré) | Infrastructure | MVP | Non commencé | — | S07, S03* |
| S12 | Retry / réinitialisation (inféré) | Infrastructure | MVP | Non commencé | — | S11 |
| S13 | HUD (inféré) | Interface | MVP | Non commencé | — | S07, S03, S02 |
| S14 | Retour audio (inféré) | Feedback | V1.0 | Non commencé | — | S02, S07, S08, S03 |
| S15 | Retour visuel / VFX (inféré) | Feedback | V1.0 | Non commencé | — | S02, S04, S08 |

*\* S03 et S11 ont une dépendance circulaire résolue par contrat de signaux — voir section dédiée.*

---

## Catégories utilisées

| Catégorie | Description |
|-----------|-------------|
| **Joueur** | Systèmes contrôlant le personnage joueur |
| **Mécanique cœur** | Systèmes définissant les verbes de jeu principaux |
| **Ennemi** | Systèmes pilotant les agresseurs |
| **Monde** | Systèmes gérant l'état de l'environnement |
| **Données** | Systèmes de définition de ressources (catalogues, configs) |
| **Caméra** | Systèmes de vue |
| **Infrastructure** | Systèmes d'orchestration et de cycle de vie du jeu |
| **Interface** | Systèmes d'affichage joueur (HUD, écrans) |
| **Feedback** | Systèmes de réponse sensorielle (audio, VFX) |

---

## Niveaux de priorité

| Tier | Définition | Milestone cible |
|------|------------|-----------------|
| **MVP** | Requis pour que la boucle cœur fonctionne et soit testable | Prototype fonctionnel (2–3 semaines) |
| **V1.0** | Requis pour le polish et la lisibilité — sans eux, la boucle est validée mais pas publiable | V1.0 polie (4–5 semaines) |

---

## Carte des dépendances

### Layer Foundation (aucune dépendance)

1. **S01 — Déplacement joueur** — Foundation physique du personnage. Toute interaction avec l'espace dépend du déplacement.
2. **S05 — Catalogue d'objets** — Données pures définissant les propriétés de chaque objet (poids, comportement Jolt, stades de destruction). Référencé par S02 et S04.
3. **S06 — Système de dégâts** — Formule de calcul de dégâts. Pur, stateless, unblocks S02, S07, S08.

### Layer Core (dépend de Foundation)

1. **S02 — Saisie et lancer** — dépend de : S01, S05, S06. Verbe principal du jeu — c'est lui que le joueur effectue en boucle.
2. **S07 — Santé joueur** — dépend de : S06. Condition de mort du joueur.
3. **S08 — Santé ennemie** — dépend de : S06. Condition de mort des ennemis.
4. **S09 — IA ennemie** — dépend de : S01 (cible). Navigation et comportement de base.
5. **S10 — Caméra TPS** — dépend de : S01. Suivi joueur, positionnement troisième personne.

### Layer Feature (dépend de Core)

1. **S03 — Vagues d'ennemis** — dépend de : S08, S09, S11 (contrat signaux). Orchestration des spawns et progression de difficulté.
2. **S04 — Dégradation d'environnement** — dépend de : S02, S05. Pilier 3 — la destruction visible EST la narration.
3. **S11 — Gestionnaire d'état de jeu** — dépend de : S07, S03 (contrat signaux). FSM : pré-vague / combat / fin-vague / game-over / victoire.

### Layer Presentation (dépend des Features)

1. **S12 — Retry / réinitialisation** — dépend de : S11. Réinitialise joueur, ennemis, objets. MVP : < 3 secondes.
2. **S13 — HUD** — dépend de : S07, S03, S02. Barre de vie, compteur de vague, indicateur d'objet tenu.
3. **S15 — Retour visuel / VFX** — dépend de : S02, S04, S08. Impacts, éclats, feedback de coup ennemi. V1.0.

### Layer Polish (dépend de tout)

1. **S14 — Retour audio** — dépend de : S02, S07, S08, S03. "Les sons d'impact font 80% du ressenti" (concept). Explicitement hors MVP.

---

## Dépendance circulaire

### S03 ↔ S11 — Vagues ↔ Gestionnaire d'état

**Nature :** S03 (Vagues) a besoin de l'état de jeu pour savoir quand spawner les ennemis.
S11 (Gestionnaire d'état) a besoin des événements de vague pour changer d'état (combat → fin-vague → game-over).

**Résolution — contrat de signaux GDScript :**

```gdscript
# S03 publie :
signal wave_started(wave_number: int)
signal wave_cleared(wave_number: int)
signal all_waves_complete()

# S11 publie :
signal game_state_changed(new_state: GameState)

# S03 écoute game_state_changed pour savoir quand spawner
# S11 écoute wave_cleared / all_waves_complete pour transitionner
```

**Conséquence de conception :** S03 et S11 sont **conçus simultanément** (ordre 9+10 dans le tableau ci-dessous). Le contrat de signaux ci-dessus est le premier livrable de cette paire — il doit être approuvé avant de détailler les règles internes de chaque système.

---

## Systèmes à risque élevé

| Système | Type de risque | Description | Mitigation |
|---------|---------------|-------------|------------|
| **S02 — Saisie et lancer** | Technique + Design | La physique Jolt des objets lancés peut produire des comportements imprévisibles et non-satisfaisants. C'est le risque #1 du projet. | Prototyper en semaine 1 avec `/prototype saisie-lancer`. La boucle entière s'arrête si ce n'est pas satisfaisant. |
| **S04 — Dégradation d'environnement** | Design | La destruction multi-stades doit rester lisible (silhouette identifiable à chaque stade — art bible §1 Principe 2). Difficile à calibrer sans itération. | Planifier 2–3 passes de polish destruction. Définir la grille multi-mesh dans le GDD avant de modéliser. |
| **S09 — IA ennemie** | Technique | Navigation dans une pièce encombrée + objets physiques Jolt actifs = blocages et comportements étranges possibles. | Commencer par l'IA la plus simple possible (déplacement direct). Affiner après validation de la boucle. |

---

## Ordre de conception recommandé

| Ordre | Système | Priorité | Layer | Effort | Notes |
|-------|---------|----------|-------|--------|-------|
| 1 | S05 — Catalogue d'objets | MVP | Foundation | M | Définit les 8–15 objets avec leurs propriétés physiques et destruction. Référencé par tout le reste. |
| 2 | S06 — Système de dégâts | MVP | Foundation | S | Formule pure. Rapide à concevoir, débloque S02/S07/S08. |
| 3 | S01 — Déplacement joueur | MVP | Foundation | S | Déplacement libre dans la pièce, intégration Jolt, vitesse, accélération. |
| 4 | **S02 — Saisie et lancer** | MVP | Core | **L** | **Risque #1 — priorité de prototype absolue.** Règles de saisie, physique de lancer, mêlée, poids des objets. |
| 5 | S07 — Santé joueur | MVP | Core | S | Santé, condition de mort, déclencheur game-over. Simple mais critique. |
| 6 | S08 — Santé ennemie | MVP | Core | S | Santé ennemie, mort ennemi, feedback d'impact reçu. |
| 7 | S09 — IA ennemie | MVP | Core | M | 3 types d'agresseurs, navigation vers joueur, comportement sous dégâts. |
| 8 | S10 — Caméra TPS | MVP | Core | M | Positionnement, distance, rotation autour du joueur, gestion obstacles. |
| 9+10 | **S03 + S11 simultanément** | MVP | Feature | M+M | Contrat de signaux défini en premier. S03 : spawn, timing, 3 vagues. S11 : FSM 5 états. |
| 11 | S04 — Dégradation d'environnement | MVP | Feature | M | États de destruction par objet, visibilité des dégâts, ancres stables (art bible §6). |
| 12 | S12 — Retry / réinitialisation | MVP | Presentation | S | Reset complet < 3 secondes. Réinitialise tous les systèmes actifs. |
| 13 | S13 — HUD | MVP | Presentation | S | Barre de vie, compteur de vague, silhouette d'objet tenu. Art bible §7. |
| 14 | S15 — Retour visuel / VFX | V1.0 | Presentation | M | Impacts, éclats, feedback de coup ennemi. GPUParticles3D. |
| 15 | S14 — Retour audio | V1.0 | Polish | M | Sons d'impact, musique, ambiance. AudioStreamPlayer3D. |

*Effort : S = 1 session (~2h), M = 2–3 sessions, L = 4+ sessions.*

---

## Suivi de progression

| Métrique | Valeur |
|----------|--------|
| Systèmes identifiés total | 15 |
| GDDs commencés | 3 |
| GDDs revus | 0 |
| GDDs approuvés | 2 |
| Systèmes MVP conçus | 3 / 13 |
| Systèmes V1.0 conçus | 0 / 2 |

---

## Prochaines étapes

- [ ] Lancer `/design-system catalogue-objets` — premier GDD (S05, Foundation)
- [ ] Lancer `/design-system systeme-degats` — deuxième GDD (S06, Foundation)
- [ ] Lancer `/prototype saisie-lancer` après S02 conçu — valider le risque #1 en semaine 1
- [ ] Lancer `/map-systems next` pour toujours reprendre le système suivant dans l'ordre
- [ ] Lancer `/gate-check pre-production` quand tous les GDDs MVP sont approuvés
