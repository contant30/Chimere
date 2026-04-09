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

<!-- AVANCEMENT_START -->
## État d'avancement

> Mis à jour automatiquement au dernier commit — 2026-04-08

**Progression globale : 1/15 systèmes complets (6%)**

`█░░░░░░░░░░░░░░░░░░░` 6%

| Statut | Nombre |
|--------|--------|
| ✅ Complet | 1 |
| 🔍 En review | 1 |
| 🔧 En cours | 0 |
| ⬜ Non commencé | 13 |

### Systèmes MVP (13 systèmes)

| # | Système | Statut | GDD |
|---|---------|--------|-----|
| S01 | Déplacement joueur | ⬜ Non commencé | — |
| S02 | Saisie et lancer | ⬜ Non commencé | — |
| S03 | Vagues d'ennemis | ⬜ Non commencé | — |
| S04 | Dégradation d'environnement | ⬜ Non commencé | — |
| S05 | Catalogue d'objets (inféré) | ✅ Complet | 📄 |
| S06 | Système de dégâts (inféré) | 🔍 In Review | 📄 |
| S07 | Santé joueur + game-over (inféré) | ⬜ Non commencé | — |
| S08 | Santé ennemie + mort ennemi (inféré) | ⬜ Non commencé | — |
| S09 | IA ennemie (inféré) | ⬜ Non commencé | — |
| S10 | Caméra TPS (inféré) | ⬜ Non commencé | — |
| S11 | Gestionnaire d'état de jeu (inféré) | ⬜ Non commencé | — |
| S12 | Retry / réinitialisation (inféré) | ⬜ Non commencé | — |
| S13 | HUD (inféré) | ⬜ Non commencé | — |

### Post-MVP / V1.0 (2 systèmes)

| # | Système | Statut | GDD |
|---|---------|--------|-----|
| S14 | Retour audio (inféré) | ⬜ Non commencé | — |
| S15 | Retour visuel / VFX (inféré) | ⬜ Non commencé | — |

<!-- AVANCEMENT_END -->

---

## Stack technique

- **Moteur** : Godot 4.6.2 (Jolt Physics par défaut)
- **Langage** : GDScript (typage statique)
- **Rendu** : Forward+
- **Plateforme cible** : PC (Steam / itch.io)
- **Tests** : GUT (Godot Unit Test)
