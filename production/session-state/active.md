# Session State — Saisir

**Mis à jour :** 2026-04-09

## Tâche actuelle

GDD S08 — Santé ennemie en cours.

## Progression

- [x] Art bible (`design/art/art-bible.md`) — 9 sections, statut : Approuvé
- [x] Systems index (`design/gdd/systems-index.md`) — 15 systèmes identifiés, ordre de conception établi
- [x] S05 — Catalogue d'objets (`design/gdd/catalogue-objets.md`) — GDD complet, toutes sections écrites
- [x] S06 — Système de dégâts (`design/gdd/systeme-degats.md`) — GDD approuvé, 9 ACs, Règle 8 (velocity), KILL_FEEL_MAX damage_base_min=3
- [x] S01 — Déplacement joueur (`design/gdd/deplacement-joueur.md`) — GDD In Review, 11 ACs, CharacterBody3D+Jolt, coyote time, 9 tuning knobs
- [x] Entity registry (`design/registry/entities.yaml`) — peuplé : 1 formule, 5 constantes
- [x] S02 — Saisie et lancer (`design/gdd/saisie-lancer.md`) — In Review, 11 ACs, 9 tuning knobs, OQ-05 ADR blocker
- [x] S07 — Santé joueur (`design/gdd/sante-joueur.md`) — In Review, 9 ACs, HP_JOUEUR_MAX=20, I-frames=0.5s, 3 tuning knobs

## Section actuelle

Overview (A) — en cours

## Fichiers en cours

design/gdd/sante-ennemie.md

## Décisions clés

- 15 systèmes MVP/V1.0 validés
- S02 (Saisie/lancer) = risque #1 — prototyper semaine 1
- S03 ↔ S11 circularité résolue par contrat de signaux
- Revue mode : lean
- S06 : formule `max(1, floori(damage_base × stage_mult))`, DAMAGE_MIN=1, DamageType enum (MELEE/THROW/ENEMY_MELEE), pas de cap MVP
- S06 : velocity Jolt délibérément exclue (Règle 8) — décision permanente MVP
- S06 : damage_base_min = 3 (objet le plus léger du catalogue) — KILL_FEEL_MAX compatible avec 12 HP
- S06 : S02 responsable de la conversion float→int avant appel S06
- ADR à créer : `DamageCalculator` static func pattern (avant implémentation S02)
- ADR à créer : `CharacterBody3D + move_and_slide()` kinematic pattern (OQ-04 S01 — avant implémentation S01)
- S01 OQ-01 : Coyote time — décision au prototype S01
- S01 OQ-03 : Taille de pièce ~10×10 m à valider au prototype
- Registry S05+S06 : à compléter dans une session dédiée (`design/registry/entities.yaml`)
