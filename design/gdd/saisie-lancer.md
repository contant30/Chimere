# S02 — Saisie et lancer

> **Statut**: In Design
> **Auteur**: ROM.CONTANT + agents
> **Dernière mise à jour**: 2026-04-08
> **Implémente le Pilier**: Pilier 1 — Tout est une arme

## Overview

S02 — Saisie et lancer est le verbe principal du jeu : le joueur peut saisir tout objet `RigidBody3D` de la pièce, l'utiliser en frappe de mêlée ou le lancer sur un ennemi. C'est ce geste que le joueur répète en boucle pendant toute la partie — il est à la fois la mécanique offensive centrale et le moteur de la boucle de ressources (chaque objet utilisé est un objet brisé ou éloigné). Techniquement, S02 orchestre la couche physique Jolt : il gère l'état de saisie d'un objet (geler son `RigidBody3D` en mode kinematic et le porter à position fixe), la frappe de mêlée (collision de zone au contact), et le lancer (impulsion Jolt via `apply_central_impulse()` à la direction du yaw caméra). S02 consulte S05 (Catalogue d'objets) pour connaître les propriétés de l'objet saisi (`mass_kg`, `grab_range_m`, dégâts de base) et appelle S06 (Système de dégâts) pour calculer les dégâts transmis à S08 (santé ennemi) ou S04 (dégradation). La réussite de S02 est la condition sine qua non de la promesse du jeu : si le geste de saisir-frapper-lancer n'est pas satisfaisant à la première session de prototype, le projet s'arrête là.

## Player Fantasy

Le joueur ne choisit pas une arme — il en attrape une. Choisir, c'est s'arrêter. Attraper, c'est réagir. Le système de saisie et lancer doit produire cette sensation d'automatisme intentionnel : le joueur sait ce qu'il fait, mais il le fait plus vite qu'il ne le formule. La main part avant la pensée. Le geste suivant commence avant que le précédent finisse.

Dans ce rythme ininterrompu, chaque objet impose sa propre physique. La chaise résiste un instant — elle est loyale, elle encaisse. La bouteille part trop vite — elle est sacrificielle. Le livre vole à plat, précis, presque silencieux. Le joueur n'apprend pas ces différences par une interface — il les découvre par le corps, dans le feu de l'action. Deux gestes identiques dans leur structure (saisir-utiliser), radicalement différents dans leur sensation. C'est ce qui rend la pièce vivante plutôt que générique.

Le moment cible : un ennemi approche par la gauche, un autre par la droite. Le joueur saisit la chaise à sa droite sans la regarder, frappe, la chaise éclate, sa main est déjà sur la bouteille. Il n'y a pas eu de pause. Pas de menu, pas de cooldown, pas de fenêtre d'attente. Le rythme est celui du joueur — jamais celui du système.

Et quand la pièce se vide, ce geste ne change pas. Le joueur n'a jamais l'arme idéale — il a l'arme disponible, et il la rend efficace. Ce n'est pas de l'improvisation par défaut : c'est l'expression d'une ingéniosité que le jeu reconnaît et récompense à chaque objet qui quitte la main.

**Alignement piliers** : Pilier 1 (tout est une arme) — la variété sensorielle confirme que chaque objet est distinct, pas interchangeable ; la promesse est tenue dans la main. Pilier 2 (le flow avant le challenge) — la boucle ne s'interrompt jamais : le système offre toujours un prochain geste, même en fin de partie.

## Detailed Design

### Core Rules

[To be designed]

### States and Transitions

[To be designed]

### Interactions with Other Systems

[To be designed]

## Formulas

[To be designed]

## Edge Cases

[To be designed]

## Dependencies

[To be designed]

## Tuning Knobs

[To be designed]

## Visual/Audio Requirements

[To be designed]

## UI Requirements

[To be designed]

## Acceptance Criteria

[To be designed]

## Open Questions

[To be designed]
