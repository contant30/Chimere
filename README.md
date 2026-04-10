# 🔮 Chimere — Saisir

[![README Dashboard](https://github.com/contant30/Chimere/actions/workflows/update-readme.yml/badge.svg)](https://github.com/contant30/Chimere/actions/workflows/update-readme.yml)

> 🎮 Brawler 3D à la troisième personne  
> Une pièce. Des objets. Des ennemis. À toi de saisir.

---

## 🎮 Concept

**Saisir** place le joueur dans une pièce fermée face à des vagues d'ennemis.

🧠 Boucle centrale :
> saisir → frapper → enchaîner

- Interaction physique avancée (Jolt)
- Environnement destructible
- Gameplay émergent basé sur la physique

🎯 Hypothèse :
> Le fun vient directement des interactions physiques, sans systèmes complexes.

---

## 🛠️ Stack technique

- 🎮 Moteur : Godot 4.6.2 (Jolt Physics)
- 🧠 Langage : GDScript (typé)
- 🖥️ Plateforme : PC (Steam / itch.io)
- 🧪 Tests : GUT

---

## 📍 État du dépôt

Le travail actuel est surtout **design et documentation** : concept, art bible, GDD par système, registre d’entités. Le **projet Godot** (`project.godot`, scènes, scripts) n’est **pas encore** versionné ici ; l’implémentation suivra une fois les GDD MVP stabilisés.

---

## 🗂️ Structure du dépôt

| Dossier | Rôle |
|--------|------|
| [`design/`](design/) | Concept, GDD, art bible, registre (`design/registry/`) |
| [`production/`](production/) | Suivi de session et état de production |
| [`docs/`](docs/) | Références moteur et documentation studio |
| [`.github/`](.github/) | CI : dashboard README, scripts associés |

---

## 📚 Documentation utile

- [Concept jeu](design/gdd/game-concept.md)
- [Index des systèmes](design/gdd/systems-index.md)
- [Art bible](design/art/art-bible.md)
- [État de session (tâche en cours)](production/session-state/active.md)

---

## 📊 Dashboard Projet

Les blocs entre `<!-- START_SECTION:... -->` et `<!-- END_SECTION:... -->` ci‑dessous sont **mis à jour automatiquement** par le workflow GitHub Actions [README Dashboard](.github/workflows/update-readme.yml) (push + toutes les 6 h). Ne pas les modifier à la main. Sous **Issues ouvertes**, les mini-barres reflètent les **cases cochées** dans la description de chaque issue (syntaxe Markdown des tâches GitHub).

### 📈 Progression globale (Issues)
<!-- START_SECTION:progress -->
✅✅✅✅🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒 15%
<!-- END_SECTION:progress -->

### 📊 Statistiques
<!-- START_SECTION:stats -->

| ✅ Fermées | 🕒 Ouvertes | 📊 Total |
|-----------|------------|----------|
| 2 | 11 | 13 |

<!-- END_SECTION:stats -->

---

### 🕒 Roadmap (Issues ouvertes)
<!-- START_SECTION:issues -->
**🕒 Issues ouvertes**

_Barres : part des sous-tâches cochées dans le corps de l’issue (`- [ ]` / `- [x]`). Sans checklist → 0 %._

- ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ #13 S13 HUD
- ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ #12 S12 Retry
- ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ #11 S11 Game state
- ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ #10 S10 Caméra TPS
- ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ #9 S09 IA ennemie

<!-- END_SECTION:issues -->

---

### ✅ Dernières tâches complétées
<!-- START_SECTION:closed_issues -->
**✅ Issues fermées**

- 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 #6 S06 Dégâts
- 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 #5 S05 Catalogue objets

<!-- END_SECTION:closed_issues -->

---

## Progression

- [x] Art bible (`design/art/art-bible.md`) — 9 sections, statut : Approuvé
- [x] Systems index (`design/gdd/systems-index.md`) — 15 systèmes identifiés, ordre de conception établi
- [x] S05 — Catalogue d'objets (`design/gdd/catalogue-objets.md`) — GDD complet, toutes sections écrites
- [x] S06 — Système de dégâts (`design/gdd/systeme-degats.md`) — GDD approuvé, 9 ACs, Règle 8 (velocity), KILL_FEEL_MAX damage_base_min=3
- [x] S01 — Déplacement joueur (`design/gdd/deplacement-joueur.md`) — GDD approuvé, 11 ACs, CharacterBody3D+Jolt, coyote time, 9 tuning knobs
- [x] S04 — Dégradation d'environnement (`design/gdd/degradation-environnement.md`) — GDD approuvé, DestructionTracker, stades + débris
- [x] Entity registry (`design/registry/entities.yaml`) — items MVP (7), formules + constantes (HP_JOUEUR_MAX, HP_LOW_THRESHOLD)
- [x] S02 — Saisie et lancer (`design/gdd/saisie-lancer.md`) — Approuvé, 11 ACs, 9 tuning knobs
- [x] S07 — Santé joueur (`design/gdd/sante-joueur.md`) — Approuvé, 9 ACs, HP_JOUEUR_MAX=20, I-frames=0.5s, 3 tuning knobs
- [x] S08 — Santé ennemie (`design/gdd/sante-ennemie.md`) — Approuvé, 8 ACs, HP_ennemi_basique=12, pas d'I-frames, 2 tuning knobs
- [x] S09 — IA ennemie (`design/gdd/ia-ennemie.md`) — Approuvé, 9 ACs, ENEMY_MOVE_SPEED=2.5, STOPPING_DISTANCE=0.8, STUCK fallback, 6 tuning knobs
- [x] S10 — Caméra TPS (`design/gdd/camera-tps.md`) — Approuvé, 9 ACs, CAMERA_DISTANCE=4.0m, PITCH_MIN=−25°/MAX=+40°, SpringArm3D, 7 tuning knobs
- [x] S03 — Vagues d'ennemis (`design/gdd/vagues-ennemis.md`) — Approuvé, 7 ACs, WAVE_SIZES=[3,5,7], INTER_WAVE_DELAY=3s, SPAWN_INTERVAL=0.5s, 3 knobs
- [x] S11 — Gestionnaire d'état (`design/gdd/gestionnaire-etat.md`) — Approuvé, 8 ACs, FSM 5 états, RETRY_DELAY=2s, contrat signaux S03↔S11 validé, 2 knobs
- [x] S12 — Retry / réinitialisation (`design/gdd/retry-reinitialisation.md`) — Approuvé, 7 ACs, reload_current_scene(), budget scene_reload_time ≤ 1s, 2 OQs
- [x] S13 — HUD (`design/gdd/hud.md`) — Approuvé, 12 ACs, 10 tuning knobs, CanvasLayer+StyleBoxFlat, 5 éléments

## Section actuelle

Phase pré-sprint terminée — ADRs `Accepted`, registres mis à jour, traçabilité architecture 48/48 `COUVERT` (PASS).

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
- ADR-0002/0003 : movement body type + `DamageCalculator.calculate(...)` (stateless) — `Accepted`
- OQ-S13-01 : `carry_interrupted(object: RigidBody3D)` ajouté à ADR-0001 GrabSystem — distinct de `object_dropped`
- OQ-S13-02 : `grab_performed(object: RigidBody3D)` déjà spécifié dans ADR-0001 — OQ pré-résolu
- ADR-0006 : coyote time + gravité (ordre saut→gravité) — `Accepted`
- ADR-0007 : camera TPS + `camera_yaw_changed` + freeze — `Accepted`
- ADR-0008 : health contracts S07/S08 — `Accepted`
- ADR-0009..0014 : ennemis/waves/FSM/retry/HUD/contraintes concept — `Accepted`

## ADRs écrits

- [x] ADR-0001..ADR-0014 — Architecture MVP (tous `Accepted`) : GrabSystem, player body type, damage calculator, catalogue objets, DI/signaux, jump+gravity, caméra TPS, health, ennemi, waves, FSM, retry, HUD, contraintes concept
---

## 🧩 Systèmes MVP

Résumé manuel pour lecture rapide. **Source de vérité pour l’avancement ticketé** : [issues GitHub](https://github.com/contant30/Chimere/issues) (le tableau peut être légèrement en retard par rapport aux issues).

| ID  | Système | Statut |
|-----|--------|--------|
| S01 | Déplacement joueur | 🔍 In Review |
| S02 | Saisie et lancer | ⬜ |
| S03 | Vagues d'ennemis | ⬜ |
| S04 | Dégradation environnement | 🔍 In Review |
| S05 | Catalogue objets | ✅ |
| S06 | Dégâts | ✅ |
| S07 | Santé joueur | ⬜ |
| S08 | Santé ennemie | ⬜ |
| S09 | IA ennemie | ⬜ |
| S10 | Caméra TPS | ⬜ |
| S11 | Game state | ⬜ |
| S12 | Retry | ⬜ |
| S13 | HUD | ⬜ |

---

## 🎯 Vision

Créer une expérience courte, intense et **hautement satisfaisante mécaniquement**.

---

## 📌 Objectif actuel
Valider que la boucle **physique = fun** sans progression artificielle.

---

## 📄 Licence

[MIT](LICENSE) — Copyright (c) 2026 Donchitos.

## 🤝 Contribution

Ouvrir une [issue](https://github.com/contant30/Chimere/issues) ou une PR en respectant le protocole du dépôt (`CLAUDE.md`, revues design). Ne pas éditer les sections du dashboard entre les commentaires `START_SECTION` / `END_SECTION`.
