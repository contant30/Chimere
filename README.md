# Saisir

Brawler 3D à la troisième personne — une seule pièce, des objets à saisir, des ennemis à fracasser.

**Moteur** : Godot 4.6.2 · **Langage** : GDScript · **Plateforme** : PC (Steam / itch.io)

---

## Concept

Saisir place le joueur dans une pièce fermée face à des vagues d'ennemis.
La mécanique centrale : saisir des objets de l'environnement, les lancer sur les ennemis,
les utiliser en mêlée. L'environnement se dégrade au fil des combats.
La profondeur vient des interactions entre la physique (Jolt) et l'espace, pas d'une
progression persistante ou de systèmes complexes.

**Hypothèse centrale** : les joueurs trouvent la boucle *saisir → frapper → enchaîner*
intrinsèquement satisfaisante.

---

## État d'avancement

### Conception (en cours)

| Document | Statut |
|----------|--------|
| Art bible (`design/art/art-bible.md`) | Approuvé — 9 sections |
| Index des systèmes (`design/gdd/systems-index.md`) | Approuvé — 15 systèmes |
| S05 — Catalogue d'objets (`design/gdd/catalogue-objets.md`) | GDD complet |
| S06 — Système de dégâts (`design/gdd/systeme-degats.md`) | En cours |

### Systèmes MVP (13 systèmes)

| # | Système | Couche | GDD |
|---|---------|--------|-----|
| S01 | Déplacement joueur | Foundation | — |
| S02 | Saisie et lancer ⚠️ | Core | — |
| S03 | Vagues d'ennemis | Feature | — |
| S04 | Dégradation d'environnement | Feature | — |
| S05 | Catalogue d'objets | Foundation | Complet |
| S06 | Système de dégâts | Foundation | En cours |
| S07 | Santé joueur + game-over | Core | — |
| S08 | Santé ennemie + mort ennemi | Core | — |
| S09 | IA ennemie | Core | — |
| S10 | Caméra TPS | Core | — |
| S11 | Gestionnaire d'état de jeu | Feature | — |
| S12 | Retry / réinitialisation | Presentation | — |
| S13 | HUD | Presentation | — |

⚠️ S02 = risque #1 — à prototyper en semaine 1.

---

## Stack technique

- **Moteur** : Godot 4.6.2 (Jolt Physics par défaut)
- **Langage** : GDScript (typage statique)
- **Rendu** : Forward+
- **Plateforme cible** : PC (Steam / itch.io)
- **Tests** : GUT (Godot Unit Test)
