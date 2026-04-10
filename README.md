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

### ⚡ Activité récente
<!-- START_SECTION:activity -->
⚡ 📊 auto update dashboard
⚡ 📊 auto update dashboard
⚡ 📊 auto update dashboard
⚡ mise a jours readme
⚡ 📊 auto update dashboard
<!-- END_SECTION:activity -->

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
