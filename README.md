# 🔮 Chimere — Saisir

> 🎮 Brawler 3D à la troisième personne  
> Une pièce. Des objets. Des ennemis. À toi de saisir.

---

## 🎮 Concept

**Saisir** place le joueur dans une pièce fermée face à des vagues d’ennemis. Le MVP vise une boucle courte et lisible : une salle, des objets physiques, des ennemis, pas de méta-progression persistante.

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
- 🧪 Tests : GUT (prévu via `/test-setup`) ; aucune suite automatisée tant que le plugin n’est pas ajouté

---

## 📍 État du dépôt

**Phase design (pré-prod) terminée** — aligné sur [session active](production/session-state/active.md) (2026-04-10) : art bible, index des systèmes, GDD MVP S01–S13 approuvés, ADR-0001..0014 `Accepted`, traçabilité 48/48 COUVERT — verdict PASS ([revue architecture](docs/architecture/architecture-review-2026-04-10b.md)).

**Projet Godot :** versionné dans ce dépôt — [`project.godot`](project.godot) (Godot **4.6**, Forward+, **Jolt Physics**), scène de test [`scenes/TestScene.tscn`](scenes/TestScene.tscn), icône [`icon.svg`](icon.svg), arborescences [`src/`](src/), [`assets/`](assets/), [`tests/`](tests/). Aucun script `.gd` gameplay pour l’instant.

**Prochaine étape :** implémentation **S02 — Saisie et lancer** (risque n°1 documenté), puis validation de la boucle physique en jeu.

**README :** sections dashboard ci-dessous tenues **à la main** (plus de workflow GitHub Actions associé).

---

## 🗂️ Structure du dépôt

| Dossier | Rôle |
|--------|------|
| Racine | [`project.godot`](project.godot), [`icon.svg`](icon.svg) |
| [`scenes/`](scenes/) | Scènes Godot (scène principale : `TestScene.tscn`) |
| [`src/`](src/) | Code GDScript — `core/`, `gameplay/` (player, enemies, objects), `ui/` |
| [`assets/`](assets/) | Art, audio, données (`art/`, `audio/`, `data/`) |
| [`tests/`](tests/) | Tests automatisés (`unit/`, `integration/`) — GUT à brancher |
| [`design/`](design/) | Concept, GDD, art bible, registre (`design/registry/`) |
| [`production/`](production/) | Suivi de session et état de production |
| [`docs/`](docs/) | ADR, traçabilité, références moteur, registres (`docs/registry/`) |
| [`.github/`](.github/) | Modèles d’issues, gabarits de corps d’issues (`issue-bodies/`) |

---

## 📚 Documentation utile

- [Concept jeu](design/gdd/game-concept.md)
- [Index des systèmes](design/gdd/systems-index.md)
- [Art bible](design/art/art-bible.md)
- [État de session](production/session-state/active.md)
- [Registre d’entités (YAML)](design/registry/entities.yaml)
- [Registre architecture / contrats](docs/registry/architecture.yaml)
- [Matrice de traçabilité](docs/architecture/architecture-traceability.md)
- [Revue architecture PASS (2026-04-10)](docs/architecture/architecture-review-2026-04-10b.md)

---

## 📊 Dashboard projet

_Snapshot manuel — chiffres issus des [issues GitHub](https://github.com/contant30/Chimere/issues). Le squelette Godot (projet + scène test) ne ferme pas les issues : elles suivent la **logique gameplay** dans `src/`._

### Jalons (lecture rapide)

| Jalon | Avancement |
|-------|----------------|
| Design MVP (GDD + ADR S01–S13) | ✅ Terminé |
| Projet Godot dans ce dépôt (squelette) | ✅ `project.godot`, `TestScene`, arborescence `src/` / `assets/` / `tests/` |
| Implémentation gameplay MVP (S01–S13) | ⬜ Non démarrée |
| Issues GitHub **fermées** (livraison considérée terminée) | **0** / 13 |

### Progression globale (issues fermées)

🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒🕒 0%

### Statistiques issues

| ✅ Fermées | 🕒 Ouvertes | 📊 Total |
|-----------|------------|----------|
| 0 | 13 | 13 |

### Issues ouvertes (MVP S01–S13)

_Barre : part de **toutes** les cases du corps (sections design + code). Après la mise à jour, la partie **design** est en général déjà cochée._

- 🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ [#1 S01 Déplacement joueur](https://github.com/contant30/Chimere/issues/1) (2/6 cases)
- 🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ [#2 S02 Saisie et lancer](https://github.com/contant30/Chimere/issues/2) (2/7)
- 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ [#3 S03 Vagues d'ennemis](https://github.com/contant30/Chimere/issues/3) (2/5)
- 🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ [#4 S04 Dégradation environnement](https://github.com/contant30/Chimere/issues/4) (1/4)
- 🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜ [#5 S05 Catalogue objets](https://github.com/contant30/Chimere/issues/5) (3/6)
- 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ [#6 S06 Dégâts](https://github.com/contant30/Chimere/issues/6) (2/5)
- 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ [#7 S07 Santé joueur](https://github.com/contant30/Chimere/issues/7) (2/5)
- 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ [#8 S08 Santé ennemie](https://github.com/contant30/Chimere/issues/8) (2/5)
- 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ [#9 S09 IA ennemie](https://github.com/contant30/Chimere/issues/9) (2/5)
- 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ [#10 S10 Caméra TPS](https://github.com/contant30/Chimere/issues/10) (2/5)
- 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ [#11 S11 Game state](https://github.com/contant30/Chimere/issues/11) (2/5)
- 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ [#12 S12 Retry](https://github.com/contant30/Chimere/issues/12) (2/5)
- 🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ [#13 S13 HUD](https://github.com/contant30/Chimere/issues/13) (2/5)

### Issues fermées

_Aucune pour l’instant — fermer une issue quand la section **Implémentation Godot (code)** est réellement terminée (et mergée dans ce dépôt)._

### Activité récente (git)

- `chore(godot): init project, TestScene, tree + README`
- `mise à jours adr`
- `Add HUD requirements and health constants to registries`
- `docs(gdd): S08 → S12 — santé ennemie, IA, caméra, vagues, état, retry`
- `docs(gdd): passer S02 en review + ajouter ADR grab system`
- `S01 + S02 — Révision déplacement joueur + squelette saisie/lancer`

---

## 🧩 Systèmes MVP

**Colonnes :** *GDD* = spécification + ADR prêts dans le dépôt. *Code* = logique gameplay dans `src/` (scène vide ou squelette seul = ⬜).  
**Issues :** toutes **ouvertes** jusqu’à livraison code ; le corps distingue **Design** (coché) et **Implémentation Godot** (à faire).

| ID  | Système | GDD | Code | Issue |
|-----|--------|-----|------|-------|
| S01 | Déplacement joueur | ✅ | ⬜ | [#1](https://github.com/contant30/Chimere/issues/1) ouverte |
| S02 | Saisie et lancer | ✅ | ⬜ | [#2](https://github.com/contant30/Chimere/issues/2) ouverte |
| S03 | Vagues d’ennemis | ✅ | ⬜ | [#3](https://github.com/contant30/Chimere/issues/3) ouverte |
| S04 | Dégradation environnement | ✅ | ⬜ | [#4](https://github.com/contant30/Chimere/issues/4) ouverte |
| S05 | Catalogue objets | ✅ | ⬜ | [#5](https://github.com/contant30/Chimere/issues/5) ouverte |
| S06 | Dégâts | ✅ | ⬜ | [#6](https://github.com/contant30/Chimere/issues/6) ouverte |
| S07 | Santé joueur | ✅ | ⬜ | [#7](https://github.com/contant30/Chimere/issues/7) ouverte |
| S08 | Santé ennemie | ✅ | ⬜ | [#8](https://github.com/contant30/Chimere/issues/8) ouverte |
| S09 | IA ennemie | ✅ | ⬜ | [#9](https://github.com/contant30/Chimere/issues/9) ouverte |
| S10 | Caméra TPS | ✅ | ⬜ | [#10](https://github.com/contant30/Chimere/issues/10) ouverte |
| S11 | Game state | ✅ | ⬜ | [#11](https://github.com/contant30/Chimere/issues/11) ouverte |
| S12 | Retry | ✅ | ⬜ | [#12](https://github.com/contant30/Chimere/issues/12) ouverte |
| S13 | HUD | ✅ | ⬜ | [#13](https://github.com/contant30/Chimere/issues/13) ouverte |

S14 (retour audio) et S15 (retour visuel / VFX) sont planifiés en **V1.0** — hors MVP ([systems-index](design/gdd/systems-index.md)).

---

## 🎯 Vision

Créer une expérience courte, intense et **hautement satisfaisante mécaniquement**.

---

## 📌 Objectif actuel

Le **projet Godot** est dans ce dépôt : ouvrir le dossier dans **Godot 4.6.2**, lancer `TestScene.tscn` (F5) pour valider Jolt / Forward+. Ensuite implémenter **S02 — Saisie et lancer**, puis vérifier en jeu que la boucle **physique = fun** sans progression artificielle.

---

## 📄 Licence

[MIT](LICENSE) — Copyright (c) 2026 Donchitos.

## 🤝 Contribution

Ouvrir une [issue](https://github.com/contant30/Chimere/issues) ou une PR en respectant le protocole du dépôt (`CLAUDE.md`, revues design). Après un changement d’état notable des issues, mettre à jour la section **Dashboard projet** dans ce README.
