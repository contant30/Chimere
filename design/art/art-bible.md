# Art Bible : Saisir

*Créé : 2026-04-07*
*Statut : Approuvé (AD-ART-BIBLE skipped — Lean mode)*

---

## 1. Visual Identity Statement

**Règle principale :** *"Si ça peut être saisi, ça doit être lisible au premier coup d'œil — choisis la clarté avant l'esthétique."*

Signification opérationnelle : quand une décision visuelle crée un choix entre une option plus raffinée esthétiquement et une option plus immédiatement lisible, la lisibilité gagne sans discussion. Dans un brawler en temps réel, l'œil du joueur a moins d'une demi-seconde pour évaluer un objet. Un asset beau mais 200ms plus lent à parser a échoué sa mission.

### Principe 1 : La saturation est un statut
La palette de base de la pièce est désaturée et neutre. Les objets interactifs portent la seule saturation notable de la pièce. Les ennemis portent la valeur de saturation la plus haute de tous.

*Test de design :* Quand on décide d'ajouter de la couleur à un élément de décor non-interactif, ce principe dit : si ce n'est pas interactif, on le désature — même si ça le rend moins intéressant visuellement isolément.

*Pilier servi :* Pilier 1 — "Tout est une arme." La saturation encode directement l'interactivité. Un joueur qui apprend cette grammaire en 10 secondes n'a plus jamais à se demander si quelque chose est utilisable.

### Principe 2 : La silhouette survit à la destruction
Chaque objet doit rester identifiable par sa silhouette seule à chaque stade de son arc de destruction — de l'état intact aux éclats brisés.

*Test de design :* Quand on conçoit un état de destruction (fissuré, à moitié détruit, dispersé), ce principe dit : si on ne peut plus identifier l'objet depuis sa silhouette en une seconde, le pass de destruction doit être revu, pas validé.

*Pilier servi :* Pilier 3 — "La pièce raconte." L'arc de destruction EST la narration. Si une chaise brisée se lit comme "débris génériques" plutôt que "ce qui était autrefois la chaise", le storytelling est perdu.

### Principe 3 : La pièce mérite sa neutralité
Les surfaces environnementales (sol, murs, plafond, mobilier fixe) doivent être visuellement récessives — faible contraste, faible saturation, texture simple — pour ne jamais concurrencer la couche d'objets pour l'attention du joueur.

*Test de design :* Quand un élément de fond est visuellement intéressant (un tapis à motifs, un mur de briques texturé), ce principe dit : le réduire jusqu'à ce qu'il cesse de concurrencer — même si la référence photo en faisait un point focal.

*Pilier servi :* Pilier 2 — "Le flow avant le challenge." Le bruit visuel en arrière-plan est un pic de difficulté caché. Garder la pièce tonalement neutre est une décision de flow, pas seulement esthétique.

### Hiérarchie visuelle
Ces trois principes créent une hiérarchie stricte :
1. **Ennemis** — saturation maximale, contraste maximal, toujours en mouvement
2. **Objets interactifs** — saturation moyenne, silhouette claire, stables
3. **Surfaces** — quasi-neutres, récessifs, non-lisibles comme saisissables

Tout asset qui brouille ces trois niveaux crée un coût de parsing pour le joueur.

---

## 2. Mood & Atmosphere

La pièce traverse cinq états émotionnels distincts au fil d'une partie. Chaque état a une signature lumière/ambiance précise — suffisamment distincte pour qu'un artiste lumière puisse l'identifier sans briefing supplémentaire.

**Règle de transition :** 0,8–1,2 secondes entre états. Le visuel précède l'audio dans chaque transition.

### État 1 — Pré-vague : "L'inventaire silencieux"

| Paramètre | Valeur |
|-----------|--------|
| **Émotion cible** | Anticipation calme / concentration |
| **Température lumière** | Neutre froide (5000–5500K) |
| **Contraste** | Faible — ombres douces, pas de zones noires dures |
| **Descripteurs** | Immobile, tendu, familier, lisible, suspendu |
| **Énergie** | Contemplative |
| **Élément clé** | Chaque objet de la pièce est visible et distinct — c'est le moment de lecture de l'arsenal avant la tempête |

### État 2 — Combat actif : "Le carnaval dirigé"

| Paramètre | Valeur |
|-----------|--------|
| **Émotion cible** | Exaltation / flow / urgence maîtrisée |
| **Température lumière** | Chaude (3200–3800K), sources dynamiques perturbées par les impacts |
| **Contraste** | Fort — les silhouettes des ennemis se détachent nettement |
| **Descripteurs** | Chaotique, vivant, expressif, saturé, cinétique |
| **Énergie** | Frénétique mais lisible |
| **Élément clé** | Les ennemis sont les taches de couleur les plus saturées de la scène — l'œil les trouve instantanément même dans le chaos |

### État 3 — Vague terminée : "La pièce qui respire"

| Paramètre | Valeur |
|-----------|--------|
| **Émotion cible** | Satisfaction / répit mérité |
| **Température lumière** | Ambre chaud (4000–4500K), lumière filtrant à travers les dégâts |
| **Contraste** | Moyen — lumière naturelle à travers les brèches créées par le combat |
| **Descripteurs** | Soulagé, dégradé, gagné, poussiéreux, chaud |
| **Énergie** | Mesurée |
| **Élément clé** | Les dégâts restent visibles — la pièce porte la preuve du combat. Pilier 3 : "La pièce raconte." |

### État 4 — Pénurie / état final : "La salle des os"

| Paramètre | Valeur |
|-----------|--------|
| **Émotion cible** | Tension dramatique / lucidité sous pression |
| **Température lumière** | Froide (6500–7000K), ombres expressionnistes, peu de sources restantes |
| **Contraste** | Élevé — les derniers objets utilisables ressortent dans l'espace vide |
| **Descripteurs** | Dépouillé, précaire, intense, dernier recours, concentré |
| **Énergie** | Mesurée mais haute tension |
| **Élément clé** | La rareté des objets restants EST la narration. L'espace vide autour du dernier objet disponible est plus éloquent que tout texte. |

### État 5 — Game over / retry : "L'ardoise"

| Paramètre | Valeur |
|-----------|--------|
| **Émotion cible** | Neutralité instantanée — zéro punition émotionnelle |
| **Température lumière** | Plate et neutre (5000K), contraste minimal |
| **Contraste** | Minimal |
| **Descripteurs** | Propre, immédiat, sans commentaire, prêt |
| **Énergie** | Nulle — transition directe vers l'état 1 |
| **Élément clé** | Aucun dramatisme. L'écran dit "recommence", pas "tu as échoué". Pilier 2 : "Le flow avant le challenge." |

---

## 3. Shape Language

### 3.1 Philosophie de la silhouette des personnages

**La règle des 10 mètres.** Dans un espace confiné en TPS, la caméra est rarement à plus de 8–12 mètres des personnages. Chaque silhouette doit se lire en moins de 100ms à cette distance, sans couleur — silhouette seule sur fond neutre.

#### Le joueur : la forme stable au centre du chaos

Le joueur adopte une **morphologie compacte et latéralement symétrique** — centre de gravité bas, masse concentrée sur le torse, membres ne dépassant pas la largeur des épaules au repos. La symétrie évoque le contrôle, l'ancrage — le joueur *choisit* où il va.

Forme dominante du joueur : **le rectangle adouci.** Torse et épaules forment un bloc lisible, tête clairement distincte (tête = 1/6e de la hauteur totale, épaules ~2,5 têtes). Les mains sont volontairement grandes — elles saisissent, c'est leur rôle narratif.

*Connexion au Visual Identity Statement :* Le joueur n'est pas saturé, il est *neutre.* Sa silhouette est la forme de référence : tout ce qui dévie de cette clarté rectangulaire est codé comme "autre."

*Pilier servi :* Pilier 1 — "Tout est une arme." Les mains grandes et lisibles rappellent en permanence le fantasme central du jeu.

#### Les ennemis : formes distinctes par type, instables en lecture

| Type | Forme dominante | Émotion communiquée |
|------|----------------|---------------------|
| **Agresseur lourd** | Triangle inversé — large aux épaules, étroit au bas. Masse haute. | Menace frontale, lent mais inévitable |
| **Agresseur rapide** | Ellipse étirée horizontalement — faible masse, membres longs. | Vitesse, imprévisibilité, danger latéral |
| **Agresseur de groupe** | Formes répétitives légèrement variées — silhouettes moyennes identiques à distance. | Pression par nombre, lisible comme "foule" avant "individus" |

**Règle d'or :** Si deux types d'ennemis produisent la même silhouette en vignette à 15 mètres, l'un des designs doit être revu. La distinction silhouette prime sur la distinction couleur.

*Pilier servi :* Pilier 2 — "Le flow avant le challenge." Un joueur qui doit cogiter pour identifier un type d'ennemi pendant le combat rompt le flow.

---

### 3.2 Géométrie de l'environnement

**La pièce domestique est angulaire par nature — et c'est une ressource, pas une contrainte.**

L'architecture d'intérieur (murs, plafond, sol, meubles fixes) est construite sur une **grille orthogonale stricte.** Cette rigueur géométrique sert deux objectifs :
1. Elle rend la pièce visuellement *récessive* — l'orthogonal est attendu, il n'attire pas l'œil.
2. Elle crée un contraste de forme avec les objets interactifs, renforçant la hiérarchie visuelle sans passer par la couleur seule.

**Règle de conception pour les props destructibles :**

> Tout objet interactif doit avoir au moins **un plan courbe ou diagonal** dans sa silhouette intacte. Cet écart par rapport à l'orthogonal environnant est le premier signal géométrique de "cet objet est différent du fond."

Exemples :
- Une chaise : dossier légèrement incliné, pieds avec un angle de quelques degrés.
- Une bouteille : corps cylindrique, col effilé. 0% d'arête droite.
- Une lampe de bureau : col articulé, abat-jour conique.

**Arc de destruction — règle de lisibilité par stade :**

| Stade | Conservation requise |
|-------|---------------------|
| Intact | Silhouette complète, forme courbe/diagonale présente |
| Endommagé | Masse principale conservée, au moins 1 plan courbe visible |
| Brisé / utilisé | Fragment le plus grand = identifiable comme "était une [chaise/bouteille/lampe]" |

*Connexion au Visual Identity Statement :* Principe 2 — "La silhouette survit à la destruction." Ce tableau est la mise en œuvre concrète de ce principe pour les artistes environnement.

*Pilier servi :* Pilier 3 — "La pièce raconte." Les débris encore lisibles racontent une chronologie. Des débris génériques effacent cette narration.

---

### 3.3 Grammaire de forme des UI

**Le HUD de Saisir est extradiégétique — il ne simule pas d'être dans le monde 3D, il le *traduit.***

> Les éléments UI utilisent exclusivement des formes à **arêtes nettes et angles droits.** Aucun arrondi, aucune ombre portée simulant la 3D. La platitude totale dit au joueur : "ceci n'est pas dans la pièce."

Dans le monde 3D, les objets interactifs ont des courbes. Dans le HUD, tout est orthogonal. L'appartenance à un plan (monde vs. interface) se lit instantanément.

**Indicateurs minimaux requis :**

| Indicateur | Forme | Position |
|---|---|---|
| **Points de vie** | Barre horizontale — rectangle plein qui se vide de droite à gauche. Pas de chiffres. | Bord inférieur gauche |
| **Numéro de vague** | Chiffre seul, typographie monospace, taille 2× le texte courant | Bord supérieur centré |
| **Objet en main** | Silhouette 2D flat de l'objet tenu, monochrome blanc | Bord inférieur droit |

**Règle d'économie UI :** Si l'information peut être lue dans la pièce (peu d'objets restants = pénurie visible), elle n'a pas besoin d'indicateur HUD.

*Pilier servi :* Pilier 2 — "Le flow avant le challenge." Un HUD qui se lit périphériquement pendant le combat est invisible — c'est l'objectif.

---

### 3.4 Formes héroïques vs formes de soutien

> **Héroïque = formes qui dévient de la grille.** Soutien = formes qui s'y conforment.

**Ce qui attire l'œil** — un objet interactif contient au moins l'une des caractéristiques suivantes :
- Une courbe (cylindre, sphère partielle, arc)
- Un angle diagonal (inclinaison, asymétrie)
- Un rapport hauteur/largeur extrême (très fin ou très trapu)
- Une répétition interne (pieds de chaise, dents d'une fourchette, pages d'un livre)

**Ce qui s'efface** — les éléments de décor non-interactifs sont des **blocs orthogonaux purs.** Leurs arêtes s'alignent sur la grille. Leur complexité géométrique est minimale.

**Règle de test :**

> Retirer texture et couleur d'un élément. Si sa silhouette attire l'œil dans une composition avec des objets interactifs, l'élément est trop complexe géométriquement — simplifier.

**Double distinction objet interactif / décor :**

| Axe | Objet interactif | Décor non-interactif |
|-----|-----------------|----------------------|
| **Couleur** | Saturation moyenne | Quasi-neutre |
| **Forme** | Déviant de la grille | Orthogonal pur |

Cette redondance est intentionnelle : si la saturation est difficile à lire (daltonisme, éclairage extrême), la forme encode toujours l'information.

*Connexion au Visual Identity Statement :* Principe 1 — "La saturation est un statut" trouve ici son équivalent formel. Les deux systèmes (saturation + forme) sont redondants, jamais en contradiction.

*Pilier servi :* Pilier 1 — "Tout est une arme." Le design géométrique fait le tutoriel sans mot : les formes déviantes sont les armes.

---

## 4. Color System

### 4.1 Architecture de la palette

La palette de Saisir est construite autour d'un **axe saturation = statut** défini en Section 1. Ce n'est pas une palette décorative — c'est un système de communication. Chaque couleur occupe une "couche" sémantique, et ces couches ne se mélangent jamais par accident.

| Couche | Saturation cible | Rôle |
|--------|-----------------|------|
| Surfaces environnementales | 0–15% | Fond neutre, récession visuelle |
| Objets interactifs | 40–65% | Signal d'interactivité, "saisissable" |
| Ennemis | 70–100% | Danger actif, priorité visuelle maximale |

**Règle absolue :** Un élément de décor ne peut pas dépasser 20% de saturation, même pour des raisons esthétiques. C'est la règle, pas la recommandation.

---

### 4.2 Palette principale

#### Couche 1 — Surfaces (palette désaturée)

Ces couleurs constituent le fond permanent de la pièce. Elles ne changent pas avec les états de jeu ; elles se réchauffent ou se refroidissent uniquement via l'éclairage, jamais via la saturation du matériau lui-même.

**BÉTON GRIS** — La neutralité absolue
- HSL : H 210°, S 6%, L 52% — RGB approx. (123, 124, 128)
- Gris bleuté très légèrement froid. Pense au béton intérieur sous éclairage fluorescent.
- Rôle : sol et murs principaux. Couleur de référence zéro — tout ce qui en dévie est perçu comme significatif.
- Ce qu'il signifie dans Saisir : "ceci n'est pas une arme, ceci est la boîte où la violence se produit."
- *Connexion :* Principe 3 — "La pièce mérite sa neutralité."

**ÉCRU FROID** — La neutralité organique
- HSL : H 40°, S 8%, L 78% — RGB approx. (201, 198, 188)
- Blanc cassé très légèrement chaud. Pense au plâtre vieilli ou à un mur d'appartement banal.
- Rôle : murs secondaires, plafond, mobilier fixe encastré.
- Ce qu'il signifie dans Saisir : la domesticité ordinaire. La pièce *ressemble* à un endroit réel, ce qui rend l'effraction de la violence plus percutante.
- *Connexion :* Pilier 3 — "La pièce raconte."

#### Couche 2 — Objets interactifs (palette saturée moyenne)

Ces couleurs signalent l'interactivité. Elles sont lisibles sur fond de Béton Gris et d'Écru Froid, tout en restant en-dessous de la saturation des ennemis.

**AMBRE OBJET** — La couleur de l'arsenal
- HSL : H 35°, S 55%, L 52% — RGB approx. (196, 140, 60)
- Orange brun chaud, comme du bois vieilli ou du métal rouillé. Pas flashy — saturé mais ancré.
- Rôle : *teinte directrice* des objets interactifs. Pas nécessairement la couleur littérale de chaque objet — c'est la température et le niveau de saturation cibles. Un livre peut être vert, une bouteille peut être bleue, mais leur saturation cible est dans la couche 2 (40–65%).
- Ce qu'il signifie dans Saisir : l'arsenal disponible. Quand l'œil capte cette saturation dans la pièce, le cerveau traduit instantanément "saisissable."
- *Connexion :* Principe 1 — "La saturation est un statut." Pilier 1 — "Tout est une arme."

**VERT ACIDE OBJET** — L'objet prioritaire
- HSL : H 80°, S 60%, L 45% — RGB approx. (100, 145, 29)
- Vert olive tirant vers le jaune. Vif mais pas fluorescent.
- Rôle : signale le *dernier objet disponible dans la zone*, ou l'objet optimal de la situation courante. Maximum 1–2 objets visibles à la fois dans cet état.
- Ce qu'il signifie dans Saisir : "celui-ci en particulier." Dirige le regard sans texte ni flèche.
- *Connexion :* Pilier 2 — "Le flow avant le challenge." Éliminer la recherche cognitive dans les moments critiques.
- Note accessibilité : paire à risque avec le rouge ennemi — voir 4.6.

#### Couche 3 — Ennemis (palette saturée maximale)

Ces couleurs sont **réservées** — leur présence dans le champ visuel signifie toujours "danger actif." Elles ne peuvent jamais apparaître sur des éléments non-ennemis.

**ROUGE ENNEMI** — La menace primaire
- HSL : H 5°, S 80%, L 45% — RGB approx. (207, 35, 20)
- Rouge pur légèrement orangé pour rester chaud, saturation maximale.
- Rôle : couleur de base des agresseurs lourds et couleur d'accent dominante sur tous les ennemis.
- Ce qu'il signifie dans Saisir : agression directe, danger actuel. Ce n'est pas le danger futur — c'est le danger *maintenant*.
- *Connexion :* Hiérarchie visuelle — les ennemis au sommet. Pilier 2 — si l'œil ne trouve pas les ennemis en moins de 200ms, le flow se brise.

**MAGENTA ENNEMI** — La menace secondaire / ennemis rapides
- HSL : H 315°, S 75%, L 40% — RGB approx. (173, 25, 120)
- Magenta profond, rouge-violet. Distinct du rouge ennemi en silhouette colorée et en vignette.
- Rôle : agresseurs rapides. La distinction couleur encode la différence comportementale : "ceci contourne" vs "ceci fonce."
- *Connexion :* Section 3 — ellipse étirée + magenta = signal doublement redondant pour l'agresseur rapide.

---

### 4.3 Usage sémantique des couleurs

| Couleur | Valeur sémantique | Pourquoi dans CE jeu |
|---------|-----------------|----------------------|
| **Rouge (H 0–15°, S >70%)** | Danger actif, ennemi, agression | Jamais détourné pour autre chose — aucune UI rouge, aucun objet rouge. Réservation absolue. |
| **Magenta (H 300–330°, S >70%)** | Danger mobile, ennemi rapide | Lisible distinctement du rouge en vision périphérique. |
| **Orange-ambre (H 25–45°, S 40–65%)** | Interactif, saisissable, arsenal | Dans un univers désaturé, l'orange ressort sans être agressif. |
| **Vert (H 70–100°, S 50–65%)** | Priorité, "prends ça maintenant" | Contraste maximal avec le rouge sur fond neutre. Jamais décoratif. |
| **Blanc (L 85–100%)** | UI, traduction, hors-monde | Le blanc pur n'apparaît que dans le HUD. Dans la pièce, il signale un état extrême. |
| **Bleu-gris (H 200–220°, S 5–15%)** | Fond, neutralité, "pas une arme" | Recule naturellement — c'est la couche de fond. |
| **Noir / ombres profondes (L < 10%)** | Zone sans information, risque | S'amplifie en état "La salle des os" — la pièce dit "je ne peux plus te protéger." |

**Règle de réservation absolue :** Le Rouge (H 0–15°, S >70%) et le Magenta (H 300–330°, S >70%) sont interdits pour tout élément non-ennemi — décor, UI, effets, transitions. Toute déviation crée une fausse alarme cognitive.

---

### 4.4 Règles de température par état de jeu

La palette de matériaux reste constante. Ce qui change entre les états, c'est l'éclairage — température de couleur, intensité, direction des ombres.

**Anchres visuelles (invariantes entre états) :**
- Ennemis : saturation maximale les rend lisibles même à 3200K ou 7000K.
- Icône d'objet en main (HUD) : blanc pur sur fond noir — immunisé par construction.
- Barre de vie : blanc sur fond sombre — même règle.

**Transformations par état :**

| État | Température lumière | Effet sur surfaces | Saturation ennemis | Contraste |
|------|--------------------|--------------------|-------------------|-----------|
| **1 — L'inventaire silencieux** | 5000–5500K | Neutre pur | 75–85% | Faible-moyen |
| **2 — Le carnaval dirigé** | 3200–3800K | +léger hue shift orange sur Écru Froid (+8° vers rouge) | 85–100% | Fort |
| **3 — La pièce qui respire** | 4000–4500K | +ambre chaud via lumière filtrant sur zones de bris | 70–80% (ennemis absents) | Moyen |
| **4 — La salle des os** | 6500–7000K | +désaturation additionnelle, hue shift bleu froid (–10°) | 90–100% | Élevé |
| **5 — L'ardoise** | 5000K | Reset complet | Reset | Minimal |

**Note technique (Godot Forward+) :** Le hue shift de l'état 2 s'obtient via ajustement de la temperature color du `WorldEnvironment`, jamais via modification des matériaux. Si un artiste modifie un matériau de surface pour l'état 2, le bug sera immédiatement visible à la sortie de cet état.

**Règle de transition :** Pendant les 0,8–1,2 secondes de transition entre états, la saturation des ennemis ne descend jamais sous 60% — même en cours d'interpolation.

---

### 4.5 Palette UI

L'interface opère sur un plan visuel séparé de la pièce 3D. La palette UI diverge délibérément de la palette monde sur deux axes : valeur et température.

> La palette UI est construite autour de deux couleurs que la pièce 3D n'utilise jamais en valeur haute : **noir pur** et **blanc pur.** Si la palette UI empruntait des couleurs au monde, la classification "monde vs interface" coûterait du temps cognitif. En rendant la palette UI orthogonale à la palette monde, cette classification devient instantanée et gratuite.

| Élément UI | Couleur | HSL |
|------------|---------|-----|
| Fond HUD | Noir pur semi-transparent | H 0°, S 0%, L 0%, alpha 65% |
| Texte / chiffres | Blanc pur | H 0°, S 0%, L 97% |
| Barre de vie (pleine) | Blanc | H 0°, S 0%, L 90% |
| Barre de vie (critique < 20%) | Orange vif | H 28°, S 85%, L 55% |
| Icône objet en main | Blanc monochrome | H 0°, S 0%, L 95% |
| Numéro de vague | Blanc | H 0°, S 0%, L 97% |
| Notification flash | Jaune vif | H 52°, S 90%, L 55% |

**Note :** L'alerte vie critique est orange (pas rouge) — la réservation rouge pour les ennemis est absolue, même dans l'UI.

**Règle UI :** Aucune couleur à saturation > 30% dans l'UI sauf pour les alertes identifiées ci-dessus. Aucun rouge/magenta dans l'UI, jamais.

*Connexion au Visual Identity Statement :* "Choisis la clarté avant l'esthétique." Une UI monochrome peut sembler moins riche — elle est plus rapide à parser, ce qui prime.

---

### 4.6 Accessibilité daltonisme

Le système saturation-comme-statut est partiellement vulnérable au daltonisme deutéranope (rouge-vert), affectant ~6% des hommes. Cette section identifie chaque paire à risque et le backup requis.

**Paire 1 : Rouge ennemi / Vert Acide Objet**

| Paramètre | Valeur |
|-----------|--------|
| Risque | Deutéranopie / protanopie — rouge et vert perçus comme teintes proches |
| Impact | Signal "objet prioritaire" non distinct du signal "ennemi" |
| Backup primaire | **Forme + mouvement** : ennemis = silhouettes mobiles ; objets = statiques avec courbes/diagonales |
| Backup secondaire | Objet prioritaire affiché en icône HUD |
| Test | Capture passée dans simulateur deutéranopie — l'ennemi reste identifiable par son mouvement |

**Paire 2 : Orange ambre objet / Rouge ennemi**

| Paramètre | Valeur |
|-----------|--------|
| Risque | Protanopie — rouge et orange perdent leur distinction |
| Impact | Un ennemi perçu comme objet à saisir — lecture inverse de la hiérarchie |
| Backup primaire | **Mouvement** : ennemis bougent, objets sont statiques — signal binaire sans couleur |
| Backup secondaire | **Forme** : triangle inversé / ellipse étirée vs formes courbes d'objets (Section 3) |
| Test | Capture statique en simulation protanopie — si un ennemi immobile est ambigu, amplifier le shape language |

**Paire 3 : Barre de vie critique (orange) / Interface normale (blanc)**

| Paramètre | Valeur |
|-----------|--------|
| Risque | Protanopie légère — orange moins distinctif |
| Impact | Alerte vie critique manquée |
| Backup primaire | **Clignotement** : pulse à 2Hz (jamais dépasser 3Hz — limite anti-épilepsie) |
| Backup secondaire | **Contraction de taille** : la barre <20% est visuellement plus petite — signal de valeur, pas de teinte |
| Test | Lisible en noir et blanc total |

**Principe général :**

> Aucune information sémantique critique dans Saisir ne repose sur la couleur seule. Chaque signal couleur a un backup dans au moins un de ces canaux : **forme, mouvement, position, taille, animation.**

Ce principe s'applique à tout nouvel asset ajouté au projet — si le backup n'est pas spécifié, l'asset est incomplet.

*Pilier servi :* Pilier 1 — "Tout est une arme." Si un joueur daltonien ne peut pas identifier l'arsenal, le fantasme central du jeu est inaccessible.

---

## 5. Character Design Direction

### 5.1 Archétype visuel du personnage joueur

**Type : Silhouette anonyme, corps-outil**

Le personnage joueur est une forme, pas une personne. Aucun trait distinctif de visage identifié, aucun marqueur de statut — juste quelqu'un de surpris dans une situation ordinaire. Le joueur doit lire ce personnage comme une extension de lui-même plutôt que comme un avatar à qui s'identifier narrativement.

**Direction de tenue : tenue de ville ordinaire**
Jean foncé, t-shirt uni, veste légère ou chemise. Couleurs dans la gamme gris neutre (S < 15%). L'habillement évoque "quelqu'un qui se retrouve dans cette situation sans l'avoir cherché" — pas un combattant, pas un superhéros. La domesticité de la tenue renforce le contraste avec la violence.

*Connexion Pilier 3 :* "La pièce raconte." Un personnage banal dans une pièce banale rend l'effraction de la violence plus percutante.

**Règles de production du personnage joueur :**

| Choix | Raison TPS | Raison jeu |
|-------|-----------|------------|
| **Dos sobre, sans détails décoratifs** | En TPS, la nuque et les épaules sont la vue permanente (90% du temps). Tout détail décoratif dans cette zone crée du bruit visuel. | Clarté de lecture permet à la caméra de rester collée sans encombrement. |
| **Vêtements plats, sans couches** | Les vêtements à plusieurs couches multiplient les normaux de surface — coûteux en low-poly et illisibles à 5 mètres. | Un personnage "monobloc" se lit en silhouette pure. |
| **Pas de couleur signature** | Le personnage joueur est dans la saturation 0–15%. Si le joueur portait une veste rouge, la règle "rouge = ennemi" serait compromise. | Pilier 1 — "Tout est une arme." La couleur du joueur ne crée jamais d'ambiguïté avec la signalisation. |
| **Mains grandes (+15–20% réalisme)** | À la distance TPS, les mains sont souvent partiellement occultées. Les agrandir les rend lisibles sans être au premier plan. | Section 3 — les mains grandes rappellent en permanence le fantasme du jeu : saisir. |
| **Silhouette compacte, centre de gravité bas** | Un personnage trop grand occupe trop de pixels et réduit le champ de vision utile. | La stabilité visuelle du joueur (rectangle adouci) contraste avec l'instabilité des ennemis. |

**Palette personnage joueur :**
- Corps : nuances de Béton Gris (H 210°, S 5–10%, L 40–55%)
- Vêtements : gris-bleu froid ou beige très désaturé — jamais ambre, rouge ou vert
- Aucune teinte rouge, magenta, ambre ou verte sur le personnage
- Un effet temporaire (poussière, impact) : S max 25% — jamais dans la couche ennemie

---

### 5.2 Règles de distinction entre personnages

**Principe directeur : la distinction s'opère en silhouette d'abord, puis en couleur — jamais en couleur seule.**

**Règle n°1 — Contraste de silhouette garanti**

Placer les quatre silhouettes côte à côte en noir sur fond blanc à 32px de hauteur. Chaque silhouette doit être identifiable sans aucun autre indice. Si deux silhouettes sont ambiguës à cette taille, l'une des deux doit être redessinée.

| Personnage | Silhouette cible (32px) | Signal distinctif |
|-----------|------------------------|-------------------|
| **Joueur** | Rectangle compact, symétrique, tête ronde distincte | Stabilité, centrage, mains visibles |
| **Agresseur lourd** | Triangle inversé — épaules très larges, bas étroit | Déséquilibre haut, impression de poids |
| **Agresseur rapide** | Ellipse horizontale, membres longs et fins | Horizontalité, légèreté |
| **Agresseur de groupe** | Silhouettes moyennes répétitives | Lecture comme "foule" avant "individus" |

**Règle n°2 — Le joueur ne peut jamais être saturé**

Toute saturation visible sur le joueur > 25% est un bug de design. La distance de saturation de 55+ points entre joueur (0–15%) et ennemis (70–100%) est le mur de séparation visuel.

**Règle n°3 — Mouvement comme signature de type**

| Personnage | Signature de mouvement |
|-----------|----------------------|
| **Joueur** | Déplacement dirigé — imprévisible, contrôlé |
| **Agresseur lourd** | Trajet rectiligne, lent, sans esquive — prévisible, inexorable |
| **Agresseur rapide** | Déplacement en arc ou zigzag — changements de direction fréquents |
| **Agresseur de groupe** | Convergence collective — mouvement de foule |

La signature de mouvement est le backup primaire de la distinction couleur (accessibilité daltonisme). Elle doit être exagérée en animation, pas réaliste.

**Règle n°4 — Couleur exclusive par entité**

| Entité | Couleurs autorisées | Couleurs interdites |
|--------|--------------------|--------------------|
| Joueur | Gris neutre (S < 15%) | Rouge, Magenta, Ambre, Vert |
| Agresseur lourd | Rouge Ennemi H 5° | Ambre, Vert, teintes d'objet |
| Agresseur rapide | Magenta Ennemi H 315° | Rouge (garder la distinction lourd/rapide) |
| Agresseur de groupe | Mélange Rouge/Magenta à S ~70% | Teintes neutres (S < 30%) |

---

### 5.3 Direction expression et posture

**Principe : Low-poly = le corps EST le visage.**

Sans expressions faciales détaillées, toute l'émotivité passe par la posture globale, l'inclinaison du centre de masse, et la vitesse d'animation.

**Style général : exagéré mais lisible, jamais réaliste.**

L'exagération en low-poly n'est pas un défaut — c'est la condition de lecture. Un geste réaliste à 300 polygones est imperceptible. Le même geste exagéré à 15% est immédiatement lisible en vision périphérique. Dans un brawler en temps réel, le joueur lit les animations en périphérie pendant qu'il regarde ailleurs.

**Postures codées — personnage joueur :**

| État | Posture | Ce qu'elle communique |
|------|---------|----------------------|
| **Neutre / repos** | Légère flexion des genoux, poids équilibré, mains légèrement devant le torse | Prêt à agir — jamais détendu |
| **Objet en main** | Épaule dominante abaissée, hanche opposée relevée, corps vers l'objet | "Je porte quelque chose de lourd / dangereux" |
| **Déplacement rapide** | Inclinaison avant du torse 10–15°, bras en arrière | Élan — le corps précède les jambes |
| **Impact reçu** | Recul 1 frame avec inclinaison arrière 25–30°, retour en 3–4 frames | Punition visible, sans blocage du flow |

**Postures codées — ennemis :**

| Type | Posture distinctive |
|------|-------------------|
| **Agresseur lourd** | Centre de gravité très bas, poids sur les hanches, tête rentrée dans les épaules |
| **Agresseur rapide** | Centre de gravité haut, appui sur l'avant du pied, épaules en avant et vers le bas |
| **Agresseur de groupe** | Posture neutre répétée avec variation aléatoire de 5–10° par individu |

**Règle d'animation :**

> Chaque état de posture doit se lire en silhouette seule, sans texture ni couleur. Si la différence entre "au repos" et "en charge" n'est pas visible en vignette noir/blanc, l'animation est insuffisante.

**Éviter :**
- Cycles de marche réalistes à cadence lente (en low-poly : semblent flottants)
- Animations de visage ou de doigts (coût élevé, retour faible à cette distance)
- Cross-fades longs entre états de combat — la lecture instantanée prime

*Pilier servi :* Pilier 2 — un ennemi dont on lit immédiatement l'intention en posture donne au joueur une longueur d'avance.

---

### 5.4 Philosophie LOD (Level of Detail)

**Contrainte : caméra TPS à 3–8 mètres, champ plein. À 5m, un personnage de 1,80m occupe 15–20% de la hauteur écran.**

**Budget polygonal par type (LOD principal) :**

| Personnage | Tris cibles | Concentration des polygones |
|-----------|------------|---------------------------|
| **Joueur** | 800–1 200 | Épaules, nuque, mains (zone TPS permanente) |
| **Agresseur lourd** | 600–900 | Masse supérieure (épaules, poings). Bas du corps simplifié. |
| **Agresseur rapide** | 500–800 | Longueur des membres. Détails terminaux supprimés. |
| **Agresseur de groupe** | 300–500 | LOD agressif — lus comme groupe, pas individu |

**Inviolable à toutes distances :**
1. Silhouette globale distinctive — aucune simplification ne doit "arrondir" une forme en générique
2. Masse des mains du joueur — signal permanent du fantasme "saisir"
3. Triangle inversé de l'agresseur lourd — si ses épaules se fondent avec sa tête, il perd son identité
4. Direction de tête — même schématique, pointe là où le personnage va

**Sacrifiable à distance :**

| Élément | Peut disparaître | Raison |
|---------|-----------------|--------|
| Détails de chaussures | > 4m | Rarement dans le champ de vision TPS |
| Géométrie des doigts | Toujours | Remplacer par mains "mitt" (3–4 polygones) — plus lisible en low-poly |
| Coutures / plis de vêtements | > 3m | Passer en texture si nécessaire |
| Détails d'accessoires (ennemis de groupe) | Toujours | Budget va à la silhouette collective |

**Règle de simplification par type :**

> **Joueur** : simplification centripète — garder masse centrale (torse/épaules), simplifier les extrémités.
> **Agresseurs lourds** : garder la masse supérieure, simplifier le bas du corps.
> **Agresseurs rapides** : garder longueur et finesse des membres, supprimer les détails terminaux.
> **Agresseurs de groupe** : minimum viable où la silhouette de groupe reste lisible.

**Test de validation LOD :**

Capture d'écran dans le moteur à 6 mètres, redimensionnée à 15% de la hauteur écran, en niveaux de gris. Si la silhouette distinctive est lisible : le LOD passe. Sinon : ajouter des polygones uniquement là où la silhouette s'effondre.

*Connexion Section 3 — "Règle des 10 mètres" :* ce test est sa mise en œuvre pratique. C'est le go/no-go avant de valider un asset personnage.

---

## 6. Environment Design Language

### 6.1 Style architectural et atmosphère de la pièce

**L'espace : un appartement de ville, stade intermédiaire**

La pièce est un **living-room / bureau domestique de taille modeste** — l'espace type d'un appartement urbain. Ni luxueux, ni délabré. L'occupant a une vie ordinaire, visible mais non commentée : une bibliothèque partiellement remplie, un coin bureau, quelques objets personnels. La pièce a été *vécue*, pas scénarisée.

**Règle de personnalité :** La pièce doit répondre à "qui habite ici ?" sans texte. La réponse doit être floue — *quelqu'un d'ordinaire* — jamais un archétype précis. L'anonymat est une décision narrative : le joueur doit pouvoir se projeter dans la situation.

*Connexion Pilier 3 :* Elle raconte une vie avant le combat — ce qui rend l'effraction de la violence d'autant plus percutante.

**Éléments architecturaux :**

| Élément | Présence | Justification |
|---------|----------|---------------|
| Sol uni (Béton Gris ou parquet désaturé) | Obligatoire | Surface neutre maximale — pas de motifs, pas de tapis complexes |
| Murs plats, 1–2 points de focalisation | Obligatoire | Ancres spatiales — le joueur se repère dans la pièce |
| Plafond lisse avec source lumineuse centrale | Obligatoire | Référence de hauteur, source principale d'éclairage état 1 |
| Fenêtre (1–2 max, partiellement occultée) | Obligatoire | Lumière secondaire + ancre visuelle stable |
| Bibliothèque / étagères fixes non-interactives | Recommandé | Crédibilité "habitée" |
| Porte (1 minimum) | Obligatoire | Referme l'espace, valide le lieu |

**Éléments dispensables :** miroirs (confusion de lecture en TPS), tableaux à motifs complexes (bruit visuel), niveaux multiples, colonnes décoratives.

**Règle de proportion low-poly :** Les murs ont une seule texture aplat par face principale. Les intersections mur/sol et mur/plafond sont des arêtes nettes à 90°. Un artiste qui ajoute de la complexité géométrique à un mur doit justifier que c'est une "forme de soutien" (Section 3.2) — sinon, supprimer.

*Connexion Section 4.2 :* Surfaces dans la couche Béton Gris / Écru Froid (S 0–15%).

---

### 6.2 Philosophie de texture

**Choix : aplats de couleur + détail peint minimal**

> **Surfaces** : texture aplat unie. Pas de normal map. Pas de roughness map détaillée.
> **Mobilier fixe** : aplat couleur + légère variation de valeur peinte (grain, rayure légère).
> **Objets interactifs** : aplat couleur (S 40–65%) + variation de valeur pour distinguer les plans. Normal map optionnelle uniquement si elle renforce la lisibilité de la silhouette.

**Pourquoi pas PBR complet :**
1. La caméra TPS place les objets à 3–10m — le détail PBR est invisible à cette distance.
2. Le système saturation = statut est encodé dans l'albedo. Un éclairage PBR (spéculaire, fresnel) peut modifier la perception de saturation selon la position et rendre le système sémantique incohérent.
3. Les transitions de température lumière (Section 4.4) doivent être prédictibles — un matériau PBR sous 7000K peut produire des valeurs inattendues.

**Résolutions par catégorie :**

| Catégorie | Résolution | Maps requises | Détail peint |
|-----------|-----------|---------------|--------------|
| Sol | 512×512 | Albedo uniquement | Légère variation de valeur (±5 L) |
| Murs | 512×512 | Albedo uniquement | Aplat pur |
| Plafond | 256×256 | Albedo uniquement | Aplat pur |
| Mobilier fixe | 512×512 | Albedo + roughness optionnel | Grain minimal |
| Objets interactifs (intact) | 512×512 | Albedo + normal optionnel | Plans distinctifs peints |
| Objets interactifs (endommagé/brisé) | Même atlas | Albedo uniquement | Marquage de bris visible |

**Règle d'atlas :** Tous les objets interactifs d'une même catégorie matériau (bois, verre, métal) partagent un atlas de texture. Cela permet de passer d'un stade de destruction à l'autre sans charger de nouvelle ressource.

*Connexion Pilier 2 :* "Le flow avant le challenge." Un frame-drop causé par une texture inutilement haute résolution est un pic de difficulté invisible — et évitable.

---

### 6.3 Règles de densité des props

**Densité cible : 8–15 objets interactifs + 4–8 meubles non-interactifs.**

**Règle des zones d'accès :** La pièce est découpée en une grille 3×3. Chaque zone doit contenir au minimum **1 objet interactif accessible** en début de vague. Le joueur ne doit jamais traverser plus de 2 zones consécutives sans voir d'objet utilisable.

```
┌─────────┬─────────┬─────────┐
│  1 obj  │  1 obj  │  1 obj  │
├─────────┼─────────┼─────────┤
│  1 obj  │ [départ │  1 obj  │
│         │ joueur] │         │
├─────────┼─────────┼─────────┤
│  1 obj  │  1 obj  │  1 obj  │
└─────────┴─────────┴─────────┘
minimum : 9 objets (1 par zone)
```

**Distribution sur 3 plans de lecture :**

| Plan | Hauteur | Contenu | Maximum |
|------|---------|---------|---------|
| Sol | 0–50 cm | Bouteilles, livres empilés, débris pré-combat | 3–4 objets |
| Surface | 50–110 cm | Lampe de bureau, magazines, vase | 4–5 objets |
| Hauteur | 110–180 cm | Lampe suspendue, cadre interactif | 2–3 objets |

Un plan vide rend la pièce stérile. Deux plans surchargés (>6 objets) la rendent illisible.

**Mobilier non-interactif :**
- Remplit deux rôles : délimiteur de zone (crée des couloirs naturels) et fond de contraste (objet ambre S55% sur meuble Écru Froid S8% = contraste maximal de Section 4)
- Ne doit jamais bloquer l'accès à plus d'1 objet interactif
- Formes : orthogonales pures — aucune courbe saillante (Section 3.2)

*Connexion Pilier 1 :* "Tout est une arme." Un objet interactif inaccessible en mouvement normal est une promesse non tenue.

---

### 6.4 Environmental storytelling sans texte

#### Les trois stades de dégradation (cumulatifs)

**Stade 1 — Avant la première vague : "La pièce ordinaire"**

Pièce intacte, éclairage 5000–5500K. Détails qui signalent *une vie interrompue* :
- Un livre ouvert, posé face contre table
- Un verre à moitié plein sur une surface
- Une chaise légèrement décalée de la table
- Légères marques d'usage sur le sol (variation de valeur L uniquement, saturation = 0)

**Stade 2 — Mi-partie (vagues 2–4) : "La pièce qui cède"**

Dégâts permanents et cumulatifs :
- Fragments d'objets brisés au sol, identifiables par silhouette (Section 3.2)
- Traces d'impact sur murs : variation de valeur L –8 à –12%, jamais de saturation ajoutée, max **15% de la surface visible d'un mur**
- Un meuble non-interactif légèrement déplacé (quelques centimètres — impact plausible)
- Transition vers éclairage état 3 amorcée si >40% des objets ont été utilisés

**Stade 3 — Fin de partie (vagues 5+) : "La salle des os"**

La majorité des objets interactifs ont été brisés. L'espace vide EST la narration :
- Fragments lisibles partout — chaque fragment identifiable comme "était [objet]"
- Murs dégradés cumulés, jamais obscurcis à >25% de leur surface visible
- Éclairage état 4 : 6500–7000K, ombres expressionnistes
- **Règle de climax :** Quand il reste 1–2 objets interactifs, un dégagement spatial d'au moins 1,5m autour de chaque objet est intentionnellement préservé. Le vide est la mise en scène.

#### Ancres visuelles stables — ce qui ne change jamais

| Ancre | Justification |
|-------|---------------|
| **La fenêtre** | Référence spatiale absolue. Vitres peuvent se briser, cadre reste en place. |
| **La porte principale** | Référence d'axe. Jamais déplacée, jamais obstruée par des débris. |
| **La source lumineuse au plafond** | Référence verticale. Reste fonctionnelle jusqu'à l'état 4. |
| **Les murs eux-mêmes** | La géométrie architecturale ne change jamais. Seul le décor superficiel se dégrade. |

**Pourquoi ces ancres sont critiques :** Dans un brawler rapide, la désorientation spatiale brise le flow (Pilier 2). Les ancres sont des décisions de game design encodées visuellement — pas des choix esthétiques.

*Connexion Pilier 3 :* La dégradation n'est éloquente que si le contraste avec l'état initial reste lisible. Sans ancres stables, tout devient chaos et la narration disparaît.

---

## 7. UI/HUD Visual Direction

### 7.1 Positionnement extradiégétique — principe et implications concrètes

**Le HUD ne simule pas d'exister dans la pièce. Il la traduit.**

Le joueur ne "voit" pas les indicateurs HUD dans l'espace 3D. Les indicateurs occupent la **périphérie visuelle** — les quatre coins et le bord supérieur centré — zones que l'œil consulte sans quitter le centre de la scène. En 0,6 secondes de combat, le joueur ne peut pas se permettre de basculer son regard vers un indicateur situé au centre ou in-world. Toute information UI qui force un mouvement oculaire actif a échoué.

**Implications pour l'implémentation (Godot 4.6.2) :**

| Règle | Conséquence concrète |
|-------|---------------------|
| Le HUD est un `CanvasLayer` au-dessus de la scène 3D, jamais un mesh world-space | Aucun `Label3D`, aucun `Sprite3D` pour les indicateurs de statut joueur |
| Les indicateurs ne bougent pas avec la caméra | `CanvasLayer.follow_viewport = false` — position d'écran fixe en pixels, indépendante du `Camera3D` |
| Aucun indicateur au centre de l'écran | La zone centrale (±15% depuis le centre) est réservée au monde 3D — jamais d'UI permanente là |
| Le HUD est plat par construction | Pas de `StyleBoxTexture` avec relief, pas d'ombre portée, pas de `border_radius`. `StyleBoxFlat` uniquement |

**Ce que le HUD NE fait pas :** Il n'indique pas le nombre d'objets restants (la pièce le dit), ni la direction des ennemis (leur silhouette et leur mouvement suffisent), ni le score (absent du jeu).

---

### 7.2 Typographie

**Contexte de lecture :** Un seul chiffre (numéro de vague), une barre sans chiffres, une silhouette monochrome. Il n'y a quasiment pas de texte dans le HUD de Saisir en cours de jeu. Chaque caractère affiché doit être lisible instantanément sans que le joueur le cherche.

**Personnalité de la fonte :** monospace, géométrique, chasse large.

- Monospace : les chiffres de vague ne dansent pas latéralement quand ils changent de valeur (1 → 2 → 10 → 12). La largeur fixe ancre le chiffre à sa position d'écran.
- Géométrique (sans empattements, formes construites sur cercles et rectangles) : cohérente avec la règle "arêtes nettes, platitude totale" de la Section 3.3.
- Chasse large : lisibilité en vision périphérique sans effort de focus.

**Fontes recommandées (licence OFL — utilisables en jeu commercial) :**
- `Space Mono` (Google Fonts) — monospace géométrique, chasse lisible, caractères distincts à petite taille
- Alternative : `JetBrains Mono` — excellent distinction 0/O, 1/l/I

**Hiérarchie de taille (base : résolution 1920×1080) :**

| Élément | Taille | Poids | Notes |
|---------|--------|-------|-------|
| Numéro de vague (permanent) | 64px | Bold (700) | Lu en périphérie haute — 2× le texte courant |
| Préfixe "VAGUE" (si affiché) | 20px | Regular (400) | Contexte contextuel, majuscules |
| Flash "VAGUE N" (annonce début de vague) | 96px | Bold (700) | Temporaire — 1,5 secondes max |

**Scaling :** Utiliser `Control.set_anchors_and_offsets_preset()` et `stretch_mode = VIEWPORT` dans les paramètres projet Godot. Ne pas utiliser de tailles en `%` — se baser sur `DisplayServer.window_get_size()` pour les calculs de ratio.

**Règle d'absence de label :** Aucun texte permanent pour identifier les indicateurs ("VIE", "ARME", "PV"). Lecture par forme et position. Le joueur apprend leur signification en 10–15 secondes de jeu.

---

### 7.3 Iconographie — Silhouette d'objet en main

**Rôle :** Backup de lisibilité — confirme l'objet tenu quand il est hors-cadre caméra ou trop petit à identifier en 3D. En conditions normales, l'objet est visible dans la main du personnage (monde 3D) ; cet indicateur entre en jeu en périphérie, sans forcer un regard actif.

**Style : flat silhouette monochrome, blanc sur fond noir.**

Ni outlined, ni illustré, ni coloré. La silhouette seule encode l'identité de l'objet — cohérent avec Principe 2 "La silhouette survit à la destruction." La couleur de la palette monde (saturation, ambre, rouge) ne touche jamais le HUD.

**Taille et fond :** 64×64 px à 1080p. Fond : rectangle noir pur (L 0%, alpha 65%), 80×80 px, arêtes nettes, zéro `border_radius` — conforme Section 3.3.

**Contrainte de lisibilité pour 8–15 objets :**

Chaque icône doit être distinguable des autres dans la bibliothèque à 64×64 px sans légende. La distinction s'opère via le ratio hauteur/largeur et la forme de masse principale.

| Objet | Caractéristique silhouette | Ratio H/L approx. |
|-------|---------------------------|-------------------|
| Chaise | 4 pieds, dossier vertical distinct | ~1,4 |
| Bouteille | Cylindre + col effilé | ~3,0 |
| Lampe de bureau | Col articulé en L/S, masse en tête | ~1,5 (latérale) |
| Livre | Rectangle très plat | ~0,2 (horizontal) |
| Vase | Ventre large + col étroit | ~1,2 |
| Tasse | Cylindre + anse saillante (seul objet avec appendice) | ~0,9 |
| Bougie/chandelier | Tige fine + base large, rapport 8:1 | ~4,0 |

**Test d'unicité iconique (obligatoire avant validation) :**
> Placer les icônes en grille à 64px. Réduire à 32×32 en niveaux de gris. Si deux icônes sont ambiguës, retravailler le ratio ou exagérer l'élément le plus distinctif.

**Règle de production :**
- Format source : SVG (vectoriel, scalable)
- Export : PNG 64×64 px, fond transparent, silhouette blanche pure
- Naming : `ui_icon_[objet]_held_64.png`
- Godot : `TextureRect` dans un `PanelContainer` stylé `StyleBoxFlat` noir

---

### 7.4 Animation des éléments HUD

**Principe directeur :** L'animation HUD confirme un événement — elle ne le dramatise pas. Toute animation qui détourne l'œil du monde 3D est une pénalité de lecture.

---

#### Feedback coup reçu — désaturation + camera shake

**Décision de design :** Le flash sur la barre de vie (indicateur d'état) est insuffisant pour signaler un événement ponctuel en combat TPS temps réel. La barre informe d'un état général ; le coup reçu est un événement qui exige un signal dans le champ de vision central.

**Implémentation :**

| Composant | Valeur | Durée | Notes |
|-----------|--------|-------|-------|
| Désaturation de l'image complète | Saturation → 0% | 80ms, `EASE_OUT` | Via `Environment.adjustment_saturation` ou `ColorRect` overlay en mode `MIX_SUB` — neutre sémantiquement, aucun conflit palette |
| Camera shake (trauma) | Amplitude 0,5% résolution, fréquence 18Hz | 150ms total, décroissance `EASE_OUT` | Rotation ±0,3°, translation ±3px max. Implémentation : offset sur le nœud `Camera3D` via `Tween` |

**Les deux effets sont désactivables séparément** dans les paramètres (accessibilité motion sickness). Nommer explicitement : "Effets de coup — désaturation de l'image" et "Effets de coup — vibration de la caméra."

**Règle d'interruption :** Si un deuxième coup arrive pendant la durée de 150ms, ne pas chaîner deux animations — les réinitialiser depuis le début (snapshot reset, pas d'accumulation).

---

#### Barre de vie — comportements animés

**Valeur instantanée :** La barre représente la valeur réelle sans interpolation — elle ne "glisse" pas. Tween sur la largeur = priorité esthétique sur la lisibilité. Interdit ici.

**Flash de hit (signal de hit) :**
- Flash blanc (L 100%) d'une frame (16ms) sur la barre — signal secondaire de renforcement.
- Retour à blanc normal en 120ms, courbe `EASE_OUT`.

**État critique (< 20% PV) :**
- Couleur : bascule vers Orange (H 28°, S 85%, L 55%) en 200ms `EASE_IN_OUT`.
- Pulse luminosité : L oscille entre 45% et 65% à **2 Hz** (`Tween.tween_property()` avec `set_loops(-1)`).
- Contraction de hauteur : −4px sur les 8px nominaux en état critique (backup forme pour accessibilité daltonisme — Section 4.6, Paire 3).
- **Jamais dépasser 3 Hz** — limite anti-épilepsie photosensible.
- Interruption (récupération de PV) : retour à blanc en 300ms, pulse stoppé immédiatement.

---

#### Numéro de vague — transition

| Phase | Durée | Animation |
|-------|-------|-----------|
| Sortie du chiffre courant | 200ms | Scale 100% → 80%, opacity 100% → 0%, `EASE_IN` |
| Silence | 100ms | Rien affiché |
| Entrée du nouveau chiffre | 300ms | Scale 130% → 100%, opacity 0% → 100%, `EASE_OUT` |

Durée visible totale : 600ms. Se déclenche **après** le flash "vague terminée" — ne pas superposer.

---

#### Icône d'objet tenu — changement

**Changement objet A → objet B :**
- Opacity A : 100% → 0% en 80ms `EASE_IN`.
- Opacity B : 0% → 100% en 80ms `EASE_OUT`, démarrant frame suivant la fin de A.
- Pas de scale, pas de translation.

**Après lancer d'objet (mains vides) :**
- Icône : disparaît en **cut instantané (frame N+1 après le lancer)** — aucune fade-out. La frame de délai serait une désynchronisation visible dans un jeu de 30 actions/minute.
- Fond noir : reste visible vide. Sa présence maintient le poids visuel du coin, évite un "trou" dans la composition du HUD.

---

### 7.5 Écrans hors-combat

**Principe :** Alignés sur l'État 5 "L'ardoise" (Section 2) — neutralité instantanée, zéro punition émotionnelle. Le temps mort → retour en jeu est **< 3 secondes** (Pilier 2).

---

#### Écran de mort / retry

**Ce que cet écran n'est PAS :** Un Game Over avec score et bouton "Rejouer". La mort est une interruption, pas une fin.

| Paramètre | Valeur |
|-----------|--------|
| Fond | Scène 3D figée à l'instant de la mort — aucune animation d'entrée |
| Overlay | `ColorRect` noir, L 0%, alpha 0% → 55% en **cut instantané** (pas de fade-in) |
| Texte centré | "RECOMMENCER" — Space Mono, 48px Bold, blanc L 97% |
| Délai avant input | 500ms anti-misclick — input ignoré, texte visible |
| Activation | N'importe quelle touche / bouton manette → `get_tree().reload_current_scene()` |
| Confirmation | Aucune — touche unique, pas de "Es-tu sûr ?" |
| Contenu | Aucune statistique, aucun score, aucun classement |

**Mesure d'implémentation :** Instrumenter le chemin mort→retry. Si la mesure dépasse 2,8 secondes en conditions normales, un élément a été ajouté à tort.

---

#### Annonce de début de vague

| Phase | Contenu | Durée | Animation |
|-------|---------|-------|-----------|
| Annonce | "VAGUE [N]" — centré, 96px Bold blanc | 1,2s total | Entrée : scale 130%→100%, opacity 0%→100% en 300ms. Tenue 600ms. Sortie : opacity→0% en 300ms. |
| Silence | HUD normal visible | 0,3s | — |
| Spawn ennemis | Dans la pièce | — | Synchronisé avec fin du silence |

**Input jamais bloqué par l'annonce.** Le joueur peut se déplacer pendant les 1,5 secondes de la séquence.

**Synchronisation lumière :** La séquence se termine exactement quand la température lumineuse commence à transitionner vers 3200–3800K (Section 4.4). Le joueur perçoit la chaleur montante comme "le combat arrive" avant le premier ennemi.

---

### 7.6 Récapitulatif des timings d'animation HUD

| Événement | Durée totale | Notes |
|-----------|-------------|-------|
| Désaturation coup reçu | 80ms | Reset si coup successif avant fin |
| Camera shake coup reçu | 150ms | Désactivable |
| Flash hit barre de vie | 120ms | Retour automatique |
| Transition état critique barre | 200ms | Pulse 2Hz continu après |
| Transition numéro de vague | 600ms | Déclenché après flash "vague terminée" |
| Changement icône objet | 160ms (80+80) | Perçu comme instantané |
| Disparition icône après lancer | Instantané (frame N+1) | Cut, pas de fade |
| Overlay mort | Instantané | Input actif après 500ms |
| Annonce vague (séquence complète) | 1 500ms | Input jamais bloqué |

---

### 7.7 Règles UI impératives

Toute déviation doit être justifiée et approuvée avant implémentation.

1. **Aucun rouge ni magenta dans le HUD** — jamais, même en alerte. Réservés aux ennemis (Section 4.3).
2. **Aucun arrondi dans le HUD** — `border_radius = 0` sur tous les `StyleBoxFlat`.
3. **Palette UI = noir pur + blanc pur + orange alerte** (H 28°, S 85%, L 55%) uniquement. Zéro autre couleur.
4. **Aucune information UI au centre de l'écran** en jeu permanent. Zone centrale réservée au monde 3D.
5. **Aucun label textuel permanent** sur les indicateurs.
6. **Pulse anti-épilepsie :** toute animation cyclique dans le HUD reste à ≤ 3 Hz.
7. **Input jamais bloqué par l'UI** pendant le jeu — seul le délai anti-misclick de 500ms sur retry est autorisé.
8. **Test d'unicité iconique à 32×32 niveaux de gris** obligatoire avant validation de toute icône.
9. **Désaturation et camera shake désactivables séparément** dans les paramètres (accessibilité).

*Pilier servi :* Pilier 2 — "Le flow avant le challenge." Un HUD qui se lit périphériquement pendant le combat est invisible — c'est l'objectif.

---

## 8. Asset Standards

### 8.1 Principe directeur

Les standards d'asset de Saisir servent deux objectifs : maintenir la cohérence visuelle de l'art bible et garantir 60fps stables sur PC mid-range (GTX 1060 / RX 580 équivalent). Quand une décision technique entre en conflit avec une préférence esthétique, le 60fps est non-négociable — la réduction de détail doit se faire dans les zones qui n'affectent pas la silhouette ni la hiérarchie de saturation.

---

### 8.2 Tableau de synthèse

| Catégorie | Format source | Export Godot | Résolution texture cible | LOD niveaux | Mat. slots max |
|-----------|--------------|--------------|--------------------------|-------------|----------------|
| Personnage joueur | `.blend` | `.glb` | 512×512 albedo + ORM | 2 (seuil 6m) | 1 |
| Ennemi lourd / rapide | `.blend` | `.glb` | 512×512 albedo + ORM | 2 (seuil 8m) | 1 |
| Ennemi de groupe | `.blend` | `.glb` | Atlas 512 (4 variantes) | 1 fixe | 1 (atlas) |
| Objet interactif (3 stades) | `.blend` | `.glb` multi-mesh | Atlas 512 par matière | 1 fixe/stade | 1–2 max |
| Mobilier non-interactif | `.blend` | `.glb` statique | 256×256 ou atlas surface | Aucun | 1 |
| Décor architectural | Primitives `.tscn` | `.tres` + `.png` | 512/256 tileable | N/A | 3 max (pièce entière) |
| Icônes UI | `.svg` source | `.png` 64×64 | 64×64 px | N/A | N/A |
| VFX / Particules | `.tscn` Godot | Atlas `.png` | 256 atlas (cellules 32–64) | N/A | 1 par famille |

---

### 8.3 Formats de fichier

**Format 3D principal : `.glb` (glTF 2.0 binaire).**

C'est le format de référence de Godot 4.x avec import natif complet via `EditorSceneFormatImporterGLTF`. Le `.fbx` est déconseillé sauf contrainte pipeline externe — Godot le convertit en glTF en interne via FBX2glTF, ajoutant un point de friction sans bénéfice pour un nouveau projet.

**Format textures source : `.png`** — fond transparent pour les icônes, pas de canal alpha pour les textures de surface.

**Format textures Godot (à l'import) : BC7 (BPTC)** — compressé automatiquement à l'import par Godot. BC7 est le standard pour Forward+ sur PC (D3D12 et Vulkan). Ne pas désactiver la compression automatique. Le PNG source reste dans `assets/` ; le fichier `.import` généré par Godot contient la version compressée.

**Format matériaux Godot : `.tres`** — ressources partagées référencées par plusieurs meshes. Un seul `mat_surface_concrete.tres` pour tous les murs, pas un fichier dupliqué par mesh.

---

### 8.4 Budgets polygones

**Objectif artistique** (Section 5 — silhouette lisible à toutes distances) vs **plafond technique** (Forward+ PC mid-range, 60fps).

| Catégorie | Objectif artistique (LOD 0) | Plafond technique (LOD 0) | LOD 1 | Critère de déclenchement LOD |
|-----------|---------------------------|--------------------------|-------|------------------------------|
| Personnage joueur | **800–1 200 tris** | 6 000 tris | 400–600 tris | > 6m caméra |
| Ennemi lourd | **600–900 tris** | 4 500 tris | 400 tris | > 8m caméra |
| Ennemi rapide | **500–800 tris** | 3 000 tris | 300 tris | > 8m caméra |
| Ennemi de groupe | **300–500 tris** | 2 000 tris | — (1 niveau fixe) | Aucun seuil |
| Objet interactif | **200–600 tris** | 1 500 tris | 150 tris | > 6m |
| Mobilier non-interactif | **50–150 tris** | 400 tris | — | Aucun |
| Architecture (par mesh) | **12–50 tris** | 200 tris | N/A | N/A |

**Règle de validation :** Test en moteur à 6m, rendu en niveaux de gris, redimensionné à 15% de la hauteur d'écran. Si la silhouette distinctive est lisible → le mesh passe. Sinon → ajouter des polygones uniquement où la silhouette s'effondre.

**Budget scène total estimé en pic de vague :** 60 000–90 000 tris à l'écran. Plafond technique Forward+ PC mid-range : ~500 000 tris — la marge est très large. Le vrai goulot d'étranglement de Saisir est les draw calls (voir 8.6), pas le polycount.

Implémentation LOD dans Godot 4.6 : `GeometryInstance3D.lod_min_distance` / `lod_max_distance`. Pas de LOD 2 ni d'imposteur nécessaire pour une pièce unique.

---

### 8.5 Résolutions de texture et VRAM

**Budget VRAM disponible pour les assets : 512 Mo** (conservative sur 4 Go VRAM total, ~500 Mo réservés aux buffers Forward+). Total assets estimé : ~50 Mo — marge très large.

**Packed ORM :** Quand une carte de matériau avancé est nécessaire, utiliser une texture ORM packed (R = Occlusion, G = Roughness, B = Metallic). Une texture au lieu de trois. Standard Godot/PBR.

**Normal map :** Optionnelle. Autoriser uniquement sur les objets interactifs si la normal map renforce visiblement la lisibilité de silhouette à 5m. Si la normale ne change pas la lecture à cette distance → supprimer (pas réduire : supprimer).

**Atlas de textures — obligation pour les petits objets :**

Trois atlas partagés pour les objets interactifs, par catégorie de matière :
- `atlas_wood_512.png` — bois (chaises, étagères, caisses)
- `atlas_glass_512.png` — verre et céramique (bouteilles, vases, tasses)
- `atlas_metal_512.png` — métal et tissu dur (lampes, cadres)

L'atlas garantit qu'un swap de mesh (intact → brisé) ne déclenche aucun chargement de texture mid-game — les trois stades de destruction partagent le même atlas depuis le départ.

---

### 8.6 Draw calls

Forward+ génère minimum 2–3 draw calls par mesh visible avec matériau distinct (depth pre-pass + opaque pass + shadow pass si actif).

| Contexte | Cible | Maximum absolu |
|----------|-------|---------------|
| Pré-vague (scène calme) | < 150 | 250 |
| Combat actif (pic de vague) | < 300 | 450 |

**Règles structurelles pour respecter ce budget :**

1. **Mobilier non-interactif :** `gi_mode = BAKED` + shadow casting `SHADOW_CASTING_SETTING_OFF`. Ces meshes se regroupent dans le même draw call s'ils partagent le même matériau.
2. **Sol + murs + plafond :** un seul trimsheet (matériau unique). Objectif : 3–5 draw calls pour l'architecture entière.
3. **Objets sur atlas partagé :** même matériau = batching possible avant saisie. Après saisie (RigidBody3D actif), le batching statique est suspendu mais le shader state reste partagé.
4. **Shadow casting :** désactivé par défaut sur les objets interactifs. Activé uniquement sur le joueur et les ennemis.
5. **Aucune transparence sur les objets interactifs :** le swap entre stades de destruction se fait par `visible` toggle sur les MeshInstance3D, jamais par un shader de dissolution avec `BLEND_MODE_MIX`. La transparence sort du depth pre-pass et double le coût de rendu.

---

### 8.7 Spécifications par catégorie

#### Personnages (joueur + ennemis)

**Structure `.glb` :** maillage + UV + rig dans un seul fichier. Textures exportées séparément. Squelette : 20–30 os maximum.

**Agresseur de groupe :** atlas 512×512 pour 4 variantes visuelles. Tous les membres d'un groupe partagent un seul matériau — essentiel pour les passes groupées Forward+.

#### Objets interactifs destructibles

**Structure `.glb` multi-mesh recommandée :**

```
chair.glb
└── ChairRoot (Node3D)
    ├── ChairIntact (MeshInstance3D)    ← visible = true au départ
    ├── ChairBroken (MeshInstance3D)    ← visible = false
    └── ChairCollider (CollisionShape3D) ← hull convexe Jolt
```

Le swap `intact → brisé` se fait par toggle `visible` en GDScript, pas par instanciation runtime. Le mesh brisé est déjà en VRAM — aucun spike mid-game.

**Colliders Jolt :**
- État intact : `ConvexPolygonShape3D` (hull convexe simple).
- Fragments volants : `ConvexPolygonShape3D` par fragment, **maximum 8 fragments actifs simultanément** par objet cassé. Au-delà, désactiver les fragments excédentaires. Ne jamais utiliser `ConcavePolygonShape3D` sur un `RigidBody3D` — Jolt ne le supporte que sur les `StaticBody3D`.

**Normal map :** optionnelle, format `_nrm_512.png`. Si supprimée : supprimer complètement, ne pas remplacer par une résolution réduite.

#### Décor architectural

Construit directement dans le fichier de scène Godot (`.tscn`) comme `CSGBox3D` ou primitives mesh. Matériaux partagés via `mat_surface_[descripteur].tres`. Un seul trimsheet pour sol + murs + plafond.

Dégâts sur surfaces (stades 2/3 de Section 6.4) : `Decal` node posé au point d'impact. Ne pas changer le matériau de la surface — les décals sont cumulatifs et positionnés dynamiquement. *Note : valider que `Decal` fonctionne correctement avec les matériaux aplat non-PBR en Forward+ sur le prototype.*

#### Icônes UI

Format source SVG conservé dans `assets/art/ui/source/`. Ne pas importer les SVG directement dans Godot — export PNG explicite à 64×64 pour garantir le rendu pixel-perfect.

Tout ajout d'objet interactif au jeu exige la création simultanée de son icône SVG + export PNG avant que l'asset soit considéré livrable.

#### VFX / Particules

Construits comme `GPUParticles3D` ou `CPUParticles3D` dans des scènes `.tscn` dédiées. Les VFX doivent réagir à l'éclairage dynamique (transitions de température Section 4.4) — un VFX importé comme spritesheet externe est immunisé à l'éclairage et brise la cohérence des états de jeu.

**Contrainte palette VFX :**
- Impacts sur surfaces : poussière en Béton Gris (S < 15%) — les surfaces ne saturent pas même sous impact.
- Impacts sur objets interactifs : éclats conservent la couleur de l'objet (S 40–65%).
- Impacts sur ennemis : fragments en Rouge / Magenta (S 70–100%). Violence stylisée — aucune particule de "sang" réaliste.
- **Durée maximale des effets :** 600ms pour les impacts, 1,2s pour la poussière.

---

### 8.8 Conventions de nommage

Règles absolues : `snake_case` strict, ASCII uniquement, pas d'espace, pas d'accent. Chemin de fichier complet : < 180 caractères (contrainte Windows MAX_PATH).

**Toujours renommer les fichiers via le FileSystem panel de Godot**, jamais via l'explorateur OS — un renommage externe génère un fichier `.import` orphelin.

| Catégorie | Pattern | Exemples |
|-----------|---------|---------|
| Personnage | `char_[role]_[usage]_[variant].[ext]` | `char_player_idle_01.glb` |
| Texture personnage | `char_[role]_[map]_[res].png` | `char_heavy_albedo_512.png` |
| Objet interactif | `env_[objet]_[état]_[variant].[ext]` | `env_chair_intact_01.glb` |
| Atlas textures | `atlas_[matière]_[res].png` | `atlas_wood_512.png` |
| Mobilier statique | `env_[objet]_static_[variant].[ext]` | `env_bookshelf_static_01.glb` |
| Matériaux surface | `mat_surface_[descripteur].tres` | `mat_surface_concrete.tres` |
| Textures surface | `tex_surface_[descripteur]_[map]_[res].png` | `tex_surface_concrete_albedo_512.png` |
| Icônes UI | `ui_icon_[objet]_held_[res].png` | `ui_icon_chair_held_64.png` |
| VFX scènes | `vfx_[famille]_[déclencheur]_[variant].tscn` | `vfx_impact_wood_break_small.tscn` |
| VFX atlas | `vfx_[famille]_atlas_[res].png` | `vfx_impact_atlas_256.png` |

Le suffixe `_static_` sur le mobilier non-interactif est obligatoire — il distingue immédiatement les props destructibles des meubles fixes dans un listing de fichiers.

---

### 8.9 Notes Godot 4.6.2 spécifiques

**D3D12 par défaut sur Windows :** Les shaders compilés pour Vulkan ne sont pas transférables à D3D12 sans recompilation. Utiliser le **Shader Baker** (ajouté en 4.5) sur le build final avec D3D12 actif. Ne pas valider les shaders uniquement sous Vulkan.

**Glow :** Passe maintenant avant le tonemapping (changement 4.6 vs 4.3). Toute valeur d'intensité glow doit être calibrée en 4.6.2 uniquement.

**Batching avec RigidBody3D Jolt actifs :** Les objets Jolt en mouvement actif sortent du batching statique. Normal et attendu — à surveiller en profiling de prototype physique.

**`HingeJoint3D.damp` ignoré par Jolt.** Si un objet articulé en a besoin, utiliser une alternative Jolt ou signaler au programmeur pour arbitrage moteur.

---

## 9. Reference Direction

Cette section est un outil de décision, pas une liste d'inspirations. Pour chaque référence, une seule chose précise est extraite — et ce qu'on refuse d'importer est défini avec autant de rigueur. Un artiste qui reçoit un asset divergent doit pouvoir citer la règle de cette section pour justifier une correction.

---

### Tableau de synthèse

| Référence | Ce qu'on prend | Ce qu'on évite | Section renforcée |
|---|---|---|---|
| *Superhot* | La règle du fond blanc : tout ce qui n'est pas interactif est quasi-absent visuellement | L'esthétique minimaliste totale — nous avons une pièce habitée, pas un vide géométrique | §1 Hiérarchie saturation |
| *Katamari Damacy* | La différenciation de masse par proportions : la taille de l'objet dans l'espace exprime son comportement physique avant tout contact | L'innocuité comique — nos objets doivent suggérer l'impact, pas la fantaisie enfantine | §3 Shape language |
| *Wong Kar-wai — In the Mood for Love* | La grammaire de l'espace confiné : les couleurs chaudes sont portées par les surfaces proches du sujet, les neutres froids repoussent le fond | La mélancolie atmosphérique — nos états émotionnels changent par vague, pas par accumulation | §2 Mood & Atmosphere + §4 Color System |
| *Return of the Obra Dinn* | L'information portée par la silhouette seule : chaque personnage est reconnaissable à sa seule forme en mouvement, sans couleur | L'esthétique dithering monochrome — nous sommes en couleur saturée | §5 Character Design |
| Clément Oubrerie (illustrateur BD) | Les aplats de couleur avec ligne de contour portant seule le volume — pas de dégradé, pas d'ombre portée, la forme est sa propre lumière | L'illustration narrative figée — nos surfaces sont en temps réel sous Godot Forward+ | §6 Environment Language + §8 Asset Standards |

---

### Détail des références

---

#### 1. *Superhot* (2016) — SUPERHOT Team

**Ce qu'on en prend — La règle du fond neutre comme signal de néant**

Dans Superhot, tout objet non-interactif est blanc cassé, quasi-inexistant. Ce n'est pas du minimalisme décoratif : c'est un protocole de lecture. L'absence de saturation signifie "ignore ça". La présence de couleur signifie "agis sur ça". Cette règle de codage de la saturation fonctionne même sous stress cognitif, même en mouvement.

Pour Saisir, on applique ce principe de façon identique mais à intensités différentes : les surfaces architecturales (murs, sol, plafond) restent à S 0–15%, les objets interactifs montent à S 40–65%, les ennemis atteignent S 70–100%. Le joueur apprend ce code en dix secondes et ne l'oublie pas.

**Ce qu'on évite :** L'espace vide de Superhot — un fond blanc géométrique sans matière. Notre pièce est habitée, usée, ordinaire. Les surfaces neutres ont une texture peinte minimale (Section 6), elles ne sont pas des plans vierges. Un asset dont le fond ressemblerait à Superhot serait trop froid, trop abstrait, et détruirait le pilier "La pièce raconte".

**Test de décision :** Si un artiste propose un mur à S 0% avec aucune texture, aucun indice de matière — citer Superhot pour valider la désaturation, mais exiger qu'une couche de détail peint minimal reste présente. La règle prise est la saturation comme statut, pas le vide comme esthétique.

---

#### 2. *Katamari Damacy* (2004) — Namco

**Ce qu'on en prend — La taille comme promesse physique**

Dans Katamari, chaque objet du quotidien est modélisé à une échelle qui exprime immédiatement sa résistance et son comportement : une pièce de monnaie est fine et plate, une chaise est anguleuse et volumineuse, une bouteille est allongée et instable. Avant tout contact, la forme de l'objet dans l'espace dit au joueur comment il va réagir.

Pour Saisir, les proportions des objets interactifs doivent communiquer leur comportement physique Jolt avant que le joueur ne les touche. Une lampe de bureau doit avoir un pied fin instable et une tête lourde (arc balistique en vol). Un livre doit être plat et large (trajectoire planante). Une chaise doit avoir quatre points d'appui visibles qui suggèrent que les pieds casseront séparément. La silhouette = la promesse mécanique.

**Ce qu'on évite :** L'exagération des proportions dans un registre comique ou fantasque. Katamari pousse les formes vers l'abstraction joyeuse. Nos objets doivent rester dans le registre du quotidien reconnaissable — proportions réalistes légèrement héroïsées (Section 3), jamais caricaturées. Un livre façon Katamari serait trop rond, trop doux, trop inoffensif.

**Test de décision :** Si un objet interactif est modélisé avec des proportions ambiguës (ni clairement lourd, ni clairement léger), citer Katamari : la silhouette doit annoncer la physique. Retour à la table pour que les proportions soient une promesse, pas un mystère.

---

#### 3. *In the Mood for Love* (2000) — Wong Kar-wai, dir. photo : Christopher Doyle

**Ce qu'on en prend — La géographie de la chaleur dans l'espace confiné**

Wong Kar-wai et Christopher Doyle utilisent les couleurs chaudes (ocres, ambrés, bordeaux profonds) sur les surfaces qui encadrent immédiatement les personnages — les murs proches, les éclairages latéraux, les textures de premier plan. Le fond, lui, est dans des tons froids désaturés ou dans le noir. Cette règle crée une sensation d'enfermement affectif sans jamais montrer les murs comme une prison : la chaleur est ce qui tient ensemble les sujets.

Pour Saisir, ce principe pilote les transitions de température de couleur entre états émotionnels (Section 2) et la logique des éclairages d'ambiance : pendant le combat actif (3200–3800K chaud), les sources lumineuses proches du joueur et des objets interactifs passent dans les tons ambrés. Le fond recule dans les neutres. La chaleur n'est jamais uniforme — elle est géographiquement concentrée autour de ce qui compte.

**Ce qu'on évite :** La mélancolie atmosphérique — la palette de Wong Kar-wai porte une tristesse douce et une lenteur contemplative. Nos états émotionnels changent par déclencheur de vague (5 états discrets, Section 2), jamais par accumulation progressive. Une ambiance "In the Mood for Love" continue serait trop lourde, trop languissante pour un brawler en temps réel.

**Test de décision :** Si un éclairage d'environnement distribue la chaleur uniformément sur toute la pièce — citer cette référence. La chaleur doit être concentrée sur le sujet et les objets actifs, les surfaces neutres doivent rester froides. L'uniformité supprime la hiérarchie visuelle (Section 1).

---

#### 4. *Return of the Obra Dinn* (2018) — Lucas Pope

**Ce qu'on en prend — La silhouette en mouvement comme seul identifiant de personnage**

Dans Obra Dinn, chaque personnage est identifiable uniquement par sa silhouette (posture, proportions, coiffure, vêtements) sans aide de couleur. Pope a conçu ses personnages pour qu'ils soient reconnaissables à leur seule forme en mouvement dans un environnement chargé.

Pour Saisir, cette règle s'applique à la différenciation des trois types d'ennemis (léger/standard/lourd, Section 5). En état de combat actif, sous un éclairage chaud qui aplatit les détails, la seule garantie de lecture est la silhouette. L'ennemi léger doit lire "rapide et étroit" à 8 mètres de distance caméra. L'ennemi lourd doit lire "massif et lent" dans la même condition. Si on supprime la couleur dans un screenshot de combat et que les types ne sont plus distinguables — l'asset échoue.

**Ce qu'on évite :** L'esthétique dithering monochrome d'Obra Dinn. Nous travaillons en couleur avec saturation forte sur les ennemis (S 70–100%). Ce qu'on extrait n'est pas le style graphique mais la rigueur de design des silhouettes. Citer Obra Dinn sur la forme, jamais sur la palette.

**Test de décision :** Screenshot de combat, passer en niveaux de gris. Si les trois types d'ennemis ne sont plus immédiatement différenciables — citer Obra Dinn. La correction passe par les proportions et la posture en animation idle, pas par la couleur.

---

#### 5. Clément Oubrerie — illustration (*Aya de Yopougon*, couvertures *Pablo*)

**Ce qu'on en prend — L'aplat de couleur comme volume sans lumière calculée**

Oubrerie construit ses décors avec des aplats de couleur franche délimités par un contour dessiné. Il n'y a pas de dégradé pour suggérer le volume, pas d'ombre portée pour ancrer les objets au sol : la forme dessinée porte seule tout le poids visuel. Le résultat est un espace immédiatement lisible et sans ambiguïté de profondeur — on comprend la spatialité sans avoir besoin de "lire" l'éclairage.

Pour Saisir, c'est la règle de base des matériaux d'environnement (Section 6) : aplats de couleur + détail peint minimal, pas de PBR complet. Les objets interactifs low-poly stylisés n'ont pas de lightmaps complexes ni de normal maps expressifs — leur volume vient de la forme du mesh et d'un contour implicite via les arêtes nettes (Section 3). Cette référence valide le refus du réalisme physique en rendu.

**Ce qu'on évite :** L'illustration narrative figée — Oubrerie travaille sur des cases statiques pour la lecture. Nos surfaces sont animées en temps réel sous Godot Forward+ avec des effets de lumière dynamique (Section 2 : les températures de couleur changent par état). La référence s'arrête aux matériaux et à la philosophie des aplats, pas à la technique d'illustration.

**Test de décision :** Si un matériau d'objet ou d'environnement utilise des normal maps pour simuler du relief de surface ou des dégradés de lumière pour suggérer le volume — citer Oubrerie. La forme 3D du mesh doit faire le travail du volume. Un matériau avec dégradé complexe trahit la direction low-poly stylisé et alourdit inutilement le budget de rendu (Section 8 : draw calls <150 en état calme).

---

### Règle d'usage de cette section

Quand un asset est soumis en révision et qu'une correction est nécessaire, la justification doit citer :

1. La règle de la section concernée (§1 à §8)
2. La référence de cette section qui illustre le principe

**Exemple de correction valide :** *"Le mur de fond a une texture PBR avec normal map — violation §6 matériaux + Oubrerie §9 : aplat de couleur, pas de volume calculé. Retirer la normal map, garder le mesh low-poly seul."*

**Exemple de correction invalide :** *"Ce n'est pas dans l'esprit du jeu."* — Une correction sans ancre de référence n'est pas actionnable.
