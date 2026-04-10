# Session State — Saisir

**Mis à jour :** 2026-04-10

## Tâche actuelle

Tous les GDDs MVP conçus (13/13). ADRs bloquants pré-sprint complétés. Prochaines étapes : GDDs V1.0 (S15, S14) ou sprint d'implémentation.

## Progression

- [x] Art bible (`design/art/art-bible.md`) — 9 sections, statut : Approuvé
- [x] Systems index (`design/gdd/systems-index.md`) — 15 systèmes identifiés, ordre de conception établi
- [x] S05 — Catalogue d'objets (`design/gdd/catalogue-objets.md`) — GDD complet, toutes sections écrites
- [x] S06 — Système de dégâts (`design/gdd/systeme-degats.md`) — GDD approuvé, 9 ACs, Règle 8 (velocity), KILL_FEEL_MAX damage_base_min=3
- [x] S01 — Déplacement joueur (`design/gdd/deplacement-joueur.md`) — GDD In Review, 11 ACs, CharacterBody3D+Jolt, coyote time, 9 tuning knobs
- [x] Entity registry (`design/registry/entities.yaml`) — peuplé : 1 formule, 7 constantes (HP_JOUEUR_MAX + HP_LOW_THRESHOLD ajoutés en Phase 5 S13)
- [x] S02 — Saisie et lancer (`design/gdd/saisie-lancer.md`) — In Review, 11 ACs, 9 tuning knobs, OQ-05 ADR blocker
- [x] S07 — Santé joueur (`design/gdd/sante-joueur.md`) — In Review, 9 ACs, HP_JOUEUR_MAX=20, I-frames=0.5s, 3 tuning knobs
- [x] S08 — Santé ennemie (`design/gdd/sante-ennemie.md`) — In Review, 8 ACs, HP_ennemi_basique=12, pas d'I-frames, 2 tuning knobs
- [x] S09 — IA ennemie (`design/gdd/ia-ennemie.md`) — In Review, 9 ACs, ENEMY_MOVE_SPEED=2.5, STOPPING_DISTANCE=0.8, STUCK fallback, 6 tuning knobs, 3 OQs
- [x] S10 — Caméra TPS (`design/gdd/camera-tps.md`) — In Review, 9 ACs, CAMERA_DISTANCE=4.0m, PITCH_MIN=−25°/MAX=+40°, SpringArm3D, 7 tuning knobs, 2 OQs
- [x] S03 — Vagues d'ennemis (`design/gdd/vagues-ennemis.md`) — In Review, 7 ACs, WAVE_SIZES=[3,5,7], INTER_WAVE_DELAY=3s, SPAWN_INTERVAL=0.5s, 3 knobs, 2 OQs
- [x] S11 — Gestionnaire d'état (`design/gdd/gestionnaire-etat.md`) — In Review, 8 ACs, FSM 5 états, RETRY_DELAY=2s, contrat signaux S03↔S11 validé, 2 knobs, 2 OQs
- [x] S12 — Retry / réinitialisation (`design/gdd/retry-reinitialisation.md`) — In Review, 7 ACs, reload_current_scene(), budget scene_reload_time ≤ 1s, 2 OQs
- [x] S13 — HUD (`design/gdd/hud.md`) — In Review, 12 ACs, 10 tuning knobs, CanvasLayer+StyleBoxFlat, 5 éléments, 2 OQs bloquants (OQ-S13-01: carry_interrupted manquant, OQ-S13-02: grab_performed params)

## Section actuelle

Phase pré-sprint terminée — ADRs bloquants écrits, OQs S13 résolus, registres mis à jour.

## Fichiers en cours

Aucun — prêt pour sprint d'implémentation ou GDDs V1.0.

## Décisions clés

- 15 systèmes MVP/V1.0 validés
- S02 (Saisie/lancer) = risque #1 — prototyper semaine 1
- S03 ↔ S11 circularité résolue par contrat de signaux
- Revue mode : lean
- S06 : formule `max(1, floori(damage_base × stage_mult))`, DAMAGE_MIN=1, DamageType enum (MELEE/THROW/ENEMY_MELEE), pas de cap MVP
- S06 : velocity Jolt délibérément exclue (Règle 8) — décision permanente MVP
- S06 : damage_base_min = 3 (objet le plus léger du catalogue) — KILL_FEEL_MAX compatible avec 12 HP
- S06 : S02 responsable de la conversion float→int avant appel S06
- ADR-0003 : `DamageCalculator` static func — `class_name DamageCalculator extends RefCounted`, `static func calculate(damage_base: int, stage_mult: float, damage_type: DamageType) -> int`
- ADR-0002 : `CharacterBody3D + move_and_slide()` — déjà écrit (OQ-04 S01 résolu)
- OQ-S13-01 : `carry_interrupted(object: RigidBody3D)` ajouté à ADR-0001 GrabSystem — distinct de `object_dropped`
- OQ-S13-02 : `grab_performed(object: RigidBody3D)` déjà spécifié dans ADR-0001 — OQ pré-résolu
- S01 OQ-01 : Coyote time — décision au prototype S01
- S01 OQ-03 : Taille de pièce ~10×10 m à valider au prototype
- Registry S05+S06 items : à compléter dans une session dédiée (`design/registry/entities.yaml`)

## ADRs écrits

- [x] ADR-0001 — GrabSystem Architecture (mis à jour : `carry_interrupted` ajouté)
- [x] ADR-0002 — Player Body Type (CharacterBody3D + move_and_slide)
- [x] ADR-0003 — DamageCalculator static func pattern
