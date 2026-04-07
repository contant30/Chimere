# Session State — Saisir

**Mis à jour :** 2026-04-07

## Tâche actuelle

Prochain système : S01 — Déplacement joueur (ordre 3) ou lancer `/design-review design/gdd/systeme-degats.md`

## Progression

- [x] Art bible (`design/art/art-bible.md`) — 9 sections, statut : Approuvé
- [x] Systems index (`design/gdd/systems-index.md`) — 15 systèmes identifiés, ordre de conception établi
- [x] S05 — Catalogue d'objets (`design/gdd/catalogue-objets.md`) — GDD complet, toutes sections écrites
- [x] S06 — Système de dégâts (`design/gdd/systeme-degats.md`) — GDD complet, toutes sections écrites

## Section actuelle

—

## Fichiers en cours

—

## Décisions clés

- 15 systèmes MVP/V1.0 validés
- S02 (Saisie/lancer) = risque #1 — prototyper semaine 1
- S03 ↔ S11 circularité résolue par contrat de signaux
- Revue mode : lean
- S06 : formule `max(1, floori(damage_base × stage_mult))`, DAMAGE_MIN=1, DamageType enum (MELEE/THROW/ENEMY_MELEE), pas de cap MVP
- ADR à créer : `DamageCalculator` static func pattern (avant implémentation S02)
- Registry S05+S06 : à compléter dans une session dédiée (`design/registry/entities.yaml`)
