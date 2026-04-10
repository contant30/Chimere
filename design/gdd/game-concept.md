# Game Concept: Saisir

*Créé : 2026-04-07*
*Statut : Approuvé*

---

## Elevator Pitch

> C'est un brawler en temps réel dans une pièce unique, où tu improvises un combat
> en saisissant et utilisant chaque objet autour de toi pour neutraliser des vagues
> d'agresseurs — jusqu'à ce qu'il ne reste plus rien à lancer.

---

## Core Identity

| Aspect | Détail |
| ---- | ---- |
| **Genre** | Beat'em up / Brawler sandbox |
| **Plateforme** | PC (Steam / itch.io) |
| **Public cible** | Joueurs casual à mid-core, explorateurs créatifs, 16–35 ans |
| **Nombre de joueurs** | Solo |
| **Durée de session** | 10–15 minutes |
| **Monétisation** | À définir (probablement premium / prix libre sur itch.io) |
| **Scope estimé** | Petit (2–5 semaines, solo) |
| **Titres comparables** | Superhot, My Friend Pedro, Hotline Miami |

---

## Core Fantasy

Tu es ingénieux. Dans une pièce ordinaire, tu n'as pas de pistolet, pas de super-pouvoirs — tu as une chaise, une bouteille, une lampe de bureau et ta vivacité d'esprit. Chaque objet devient une arme si tu sais t'en servir. La satisfaction vient de l'improvisation fluide : saisir, enchaîner, survivre. Comme une scène de film d'action où le personnage transforme le quotidien en arsenal.

---

## Unique Hook

Comme *Superhot*, MAIS AUSSI chaque objet a un comportement physique et un usage propre — une chaise casse différemment d'une bouteille, une lampe peut être balancée en arc, un livre vole à plat. L'environnement est ton arsenal et sa destruction progressive est visible.

---

## Player Experience Analysis (MDA Framework)

### Target Aesthetics (Ce que le joueur RESSENT)

| Aesthetic | Priorité | Comment on le crée |
| ---- | ---- | ---- |
| **Sensation** (plaisir sensoriel) | 2 | Sons d'impact satisfaisants, effets visuels sur collision, retour haptique |
| **Fantasy** (incarner un personnage) | 3 | Être le survivant ingénieux qui improvise comme dans un film |
| **Narrative** (histoire) | N/A | Pas de narration explicite — l'histoire est dans l'action |
| **Challenge** (maîtrise, dépassement) | 4 | Vagues croissantes, ressources décroissantes |
| **Fellowship** (lien social) | N/A | Solo uniquement |
| **Discovery** (exploration, secrets) | 5 | Découvrir les comportements physiques de chaque objet |
| **Expression** (style personnel) | 1 | Chaque joueur développe son propre style d'improvisation |
| **Submission** (détente, flow) | 6 | Rythme fluide, retry immédiat, pas de pénalité sévère |

### Key Dynamics (Comportements émergents attendus)

- Les joueurs vont naturellement tester tous les objets de la pièce pour découvrir leurs propriétés
- Les joueurs vont chercher à enchaîner les objets sans interruption — "flow de combat"
- Les joueurs vont développer des stratégies de préservation des ressources (quels objets garder en dernier)
- Les joueurs vont rejouer pour améliorer leur fluidité et leur style

### Core Mechanics (Systèmes à implémenter)

1. **Système de saisie / lancer** — Le joueur peut saisir tout objet de la pièce, l'utiliser en mêlée ou le lancer sur un ennemi. Chaque objet a un poids, une portée et un comportement de destruction propre.
2. **Système d'ennemis en vague** — Les agresseurs arrivent par vagues, avec des déplacements simples vers le joueur. Difficulté légèrement croissante entre vagues.
3. **Système de dégradation de l'environnement** — Les objets se brisent après utilisation et disparaissent progressivement, resserrant les options tactiques du joueur.

---

## Player Motivation Profile

### Primary Psychological Needs Served

| Besoin | Comment ce jeu le satisfait | Intensité |
| ---- | ---- | ---- |
| **Autonomie** (liberté, choix) | Le joueur choisit en permanence quoi saisir, quand, comment — aucune action imposée | Cœur |
| **Compétence** (maîtrise) | Fluidité croissante des enchaînements, gestion des ressources de la pièce | Soutien |
| **Appartenance** | Absent (solo) — non pertinent pour ce projet | Minimal |

### Player Type Appeal (Taxonomie Bartle)

- [x] **Explorateurs** (découverte des systèmes, comportements cachés des objets) — Chaque objet est à tester
- [x] **Expressifs** (style personnel, improvisation) — Pas deux parties identiques
- [ ] Achievers — Pas de progression verticale
- [ ] Socializers — Solo uniquement
- [ ] Killers/Competitors — Pas de PvP ni classements

### Flow State Design

- **Courbe d'apprentissage** : Les 60 premières secondes introduisent le système de saisie naturellement — premier objet visible et accessible immédiatement
- **Scaling de difficulté** : Vagues de plus en plus nombreuses, pièce de moins en moins fournie — la difficulté vient de la pénurie, pas de l'IA
- **Clarté du feedback** : Chaque coup donne un retour visuel et sonore immédiat (secousse, son d'impact, enemi propulsé)
- **Récupération de l'échec** : Mort → écran minimal → retry immédiat, moins de 3 secondes

---

## Core Loop

### Moment-à-moment (30 secondes)

Le joueur scanne la pièce, saisit l'objet le plus proche, frappe ou lance sur l'agresseur le plus menaçant, l'objet se brise ou s'éloigne, le joueur saisit l'objet suivant. Enchaînement fluide et ininterrompu.

### Court terme (5–15 minutes)

Une vague d'agresseurs entre dans la pièce. Le joueur utilise les ressources disponibles pour les neutraliser. Fin de vague : bref moment de répit. La pièce est légèrement plus dévastée. Vague suivante, avec plus d'agresseurs. Le climax survient quand il reste peu d'objets — les derniers coups sont les plus improvisés.

### Session (10–15 minutes)

Entrée dans la pièce → vagues successives → climax de pénurie → fin (victoire ou défaite). La partie est complète. Retry ou arrêt.

### Progression long terme

Aucune progression persistante pour le MVP — chaque partie est une expérience complète. La progression est dans la maîtrise personnelle du joueur (fluidité, efficacité, style).

### Retention Hooks

- **Maîtrise** : "Cette fois je n'ai pas laissé tomber l'objet, les enchaînements étaient parfaits"
- **Curiosité** : "Je n'ai pas encore testé cette lampe de bureau"
- **Score** (optionnel post-MVP) : Temps de survie, style points, objets utilisés

---

## Game Pillars

### Pilier 1 : Tout est une arme
Chaque objet interactif de la pièce peut être utilisé en combat, sans exception. L'environnement est un arsenal complet.

*Test de design* : Si on débat entre "cet objet est utilisable" vs "cet objet est décoratif", ce pilier dit : **il est utilisable**.

### Pilier 2 : Le flow avant le challenge
Le jeu ne doit jamais frustrer. La satisfaction prime sur la difficulté. Un joueur qui perd doit avoir envie de recommencer immédiatement.

*Test de design* : Si on débat entre "mort punitive avec animation longue" vs "retry immédiat", ce pilier dit : **retry immédiat**.

### Pilier 3 : La pièce raconte
La dégradation de l'environnement est visible et progressive. La pièce qui s'effondre est la narration du jeu.

*Test de design* : Si on débat entre "reset visuel entre vagues" vs "garder les dégâts visibles", ce pilier dit : **garder les dégâts visibles**.

### Anti-Piliers (Ce que ce jeu N'EST PAS)

- **PAS de progression entre parties** : Pas d'inventaire, pas d'XP, pas de niveaux — ça complexifie sans servir le flow
- **PAS de narration complexe** : Pas de dialogues, de cutscenes ni d'histoire écrite — l'histoire est dans le chaos
- **PAS de niveaux multiples** : Une seule pièce, maîtrisée à fond — la profondeur vient des interactions, pas du contenu

---

## Inspiration et Références

| Référence | Ce qu'on en tire | Notre différence | Pourquoi c'est important |
| ---- | ---- | ---- | ---- |
| *Superhot* | Temps qui ralentit, satisfaction de l'improvisation | Temps réel rapide, pas de bullet-time | Valide le concept "chaque action compte" |
| *My Friend Pedro* | Fluidité du combat, style personnel | Full 3D, pas de platformer 2D | Valide l'appétit pour le combat improvisé expressif |
| *Hotline Miami* | Pièce unique, violence choréographiée | Full 3D, objets physiques volumétriques | Valide la compacité et le "un couloir / une pièce" |

**Inspirations hors jeux vidéo** : Scènes de bagarre dans des films d'action (*John Wick*, *Old Boy*, *Atomic Blonde*) — violence improvisée dans des espaces confinés, utilisation créative de l'environnement.

---

## Target Player Profile

| Attribut | Détail |
| ---- | ---- |
| **Tranche d'âge** | 16–35 ans |
| **Expérience jeu** | Casual à mid-core |
| **Disponibilité** | Sessions courtes (10–20 min), soirées ou pauses |
| **Plateforme** | PC principalement |
| **Jeux actuels** | Superhot, Hotline Miami, jeux d'action arcade |
| **Ce qu'ils cherchent** | Un moment de défoulement satisfaisant sans engagement lourd |
| **Ce qui les ferait partir** | Mort punissante, progression lente, complexité inutile |

---

## Technical Considerations

| Aspect | Évaluation |
| ---- | ---- |
| **Moteur recommandé** | Godot 4.6.2 — GDScript, Forward+, Jolt Physics |
| **Défis techniques principaux** | Physique 3D des objets satisfaisante (Jolt) ; caméra à la troisième personne ; comportements destructibles variés |
| **Style artistique** | Full 3D — caméra libre TPS, environnement volumétrique, low-poly stylisé |
| **Complexité pipeline art** | Moyenne — modèles 3D low-poly, textures simples, objets du quotidien destructibles |
| **Besoins audio** | Modéré mais critique — les sons d'impact font 80% du ressenti |
| **Réseau** | Aucun |
| **Volume de contenu** | 1 pièce, 8–15 objets interactifs, 3 types d'ennemis, 3–5 vagues |
| **Systèmes procéduraux** | Aucun prévu pour le MVP |

---

## Risks and Open Questions

### Risques de design
- La physique des objets peut créer des comportements imprévisibles non-satisfaisants si mal calibrée
- Le manque de progression peut réduire la rétention à moyen terme

### Risques techniques
- Les collisions physiques multiples en temps réel peuvent être complexes à polir pour un premier jeu
- Le "game feel" (son + retour visuel immédiat) est difficile à calibrer sans itération

### Risques de marché
- Marché du brawler casual bien établi — différenciation par l'objet interactif à communiquer clairement
- Portée limitée d'une démo/jeu à salle unique (acceptable pour itch.io, moins pour Steam seul)

### Risques de scope
- La physique est la fonctionnalité la plus risquée — à prototyper en semaine 1
- Le polish audio/visuel prend souvent plus de temps que prévu

### Open Questions
- Est-ce que la physique des objets est suffisamment satisfaisante sans animation dédiée ? → Répondre avec un prototype semaine 1
- Quelle est la densité d'objets minimale pour que la pièce reste intéressante jusqu'à la vague finale ? → Répondre par playtests

---

## MVP Definition

**Hypothèse principale** : Les joueurs trouvent la boucle "saisir → frapper/lancer → enchaîner" intrinsèquement satisfaisante dans un contexte de survie en pièce unique.

**Requis pour le MVP** :
1. Personnage contrôlable avec déplacement libre dans la pièce
2. 5+ objets interactifs saisissables avec physique de base (lancer, frapper, briser)
3. 3 types d'ennemis simples avec IA basique (se déplacer vers le joueur)
4. 1 séquence de vague complète (3 vagues)
5. Mort et retry immédiat (< 3 secondes)

**Explicitement hors MVP** :
- Son et musique (à ajouter après validation de la boucle)
- Animations complexes
- Menu principal élaboré
- Score ou classements

### Scope Tiers

| Tier | Contenu | Fonctionnalités | Durée |
| ---- | ---- | ---- | ---- |
| **MVP** | 1 pièce, 5 objets, 3 types d'ennemis | Boucle de combat fonctionnelle | 2–3 semaines |
| **V1.0** | 1 pièce polie, 10–15 objets, sounds, jus visuel | Boucle + polish + retry propre | 4–5 semaines (solo) |
| **Vision complète** | Variantes de pièce, mode score, plus d'ennemis | Tout V1.0 + contenu supplémentaire | Au-delà de la portée initiale |

---

## Visual Identity Anchor

*(Note : Ancre visuelle provisoire — à développer avec `/art-bible` avant la production d'assets.)*

**Direction visuelle** : *Quotidien sous tension*
Esthétique full 3D low-poly stylisée, caméra troisième personne. Les objets sont immédiatement reconnaissables dans l'espace — silhouettes claires, proportions réalistes mais simplifiées. La lisibilité prime sur le réalisme.

**Règle visuelle principale** : Chaque objet doit être identifiable en une fraction de seconde — forme claire, silhouette distincte.

**Principes visuels** :
1. **Contraste objet/sol** : Le sol est neutre (béton, parquet), les objets ont de la couleur. Test : peut-on les saisir visuellement instantanément ?
2. **Feedback de destruction lisible** : La dégradation des objets est visible progressivement — fissures, éclats, disparition par étapes. Test : le joueur sait-il qu'un objet est brisé sans regarder d'UI ?
3. **Clarté des ennemis** : Les agresseurs sont visuellement distincts du mobilier. Silhouettes claires, mouvement comme signal.

**Philosophie couleur** : Palette restreinte et désaturée pour la pièce, couleurs plus vives pour les objets utilisables et les ennemis. La saturation guide l'attention du joueur.

---

## Next Steps

- [ ] Lancer `/setup-engine` pour configurer le moteur et les références de version
- [ ] Lancer `/art-bible` pour formaliser l'identité visuelle avant toute production d'assets
- [ ] Valider le concept avec `/design-review design/gdd/game-concept.md`
- [ ] Décomposer le concept en systèmes avec `/map-systems`
- [ ] Rédiger les GDDs par système avec `/design-system`
- [ ] Planifier l'architecture technique avec `/create-architecture`
- [ ] Prototyper la physique des objets avec `/prototype objet-interactif` (risque n°1)
- [ ] Valider la boucle avec `/playtest-report` après le prototype
- [ ] Planifier le premier sprint avec `/sprint-plan new`
