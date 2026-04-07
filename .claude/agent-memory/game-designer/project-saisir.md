---
name: Project Saisir — Context
description: Contexte clé du projet Saisir pour orienter les décisions de design
type: project
---

Brawler 3D TPS pièce unique, Godot 4.6.2 GDScript, Jolt Physics, solo dev, scope 2–5 semaines.

Core loop : saisir un objet → frapper ou lancer → enchaîner sur l'objet suivant.

Pilliers :
1. Tout est une arme (chaque objet interactif, sans exception)
2. Le flow avant le challenge (frustration nulle, retry < 3s)
3. La pièce raconte (dégradation visible, permanente entre vagues)

HP ennemis standard : ~12 HP (baseline catalogue S05).
Cible calibration : 2–3 frappes mêlée pour tuer un ennemi standard.

GDDs existants au 2026-04-07 : game-concept.md, catalogue-objets.md (S05), systeme-degats.md (S06).

**Why:** Contexte fondamental pour toute décision de balance ou de mécanique.
**How to apply:** Valider chaque proposition de mécanique contre les 3 pilliers. "Le flow avant le challenge" est le pilier dominant en cas de conflit.
