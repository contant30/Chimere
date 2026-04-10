# ADR-0014 : Concept constraints (single room sessions, no persistence)

## Status
Accepted

## Date
2026-04-10

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Godot 4.6.2 |
| **Domain** | Architecture / Session Model |
| **Knowledge Risk** | LOW |
| **References Consulted** | `design/gdd/game-concept.md` |
| **Post-Cutoff APIs Used** | None |
| **Verification Required** | Aucun (contrainte de design/architecture) |

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | None |
| **Enables** | S11 (FSM), S12 (Retry), S03 (vagues), S04 (débris persistants intra-run) |
| **Blocks** | Toute implémentation qui introduit de la persistance entre runs |
| **Ordering Note** | À accepter avant les stories qui touchent save/state |

## Context

Le concept impose un modèle de session très strict :
- une seule pièce,
- runs courtes,
- aucun état persistant entre les runs (pas d'XP, pas d'inventaire, pas de progression),
- retry immédiat comme pilier de flow.

Sans ADR, ce type de contraintes “globales” est souvent dilué et réintroduit implicitement (Autoloads stateful, sauvegardes, etc.).

## Decision

1. **Session = une scène de jeu**  
   Une run correspond à une scène de jeu unique (pièce). Les systèmes runtime (vagues, HP, débris) vivent dans cette scène.

2. **Pas de persistance entre runs (MVP/V1.0)**  
   - Aucun système ne sauvegarde des données entre deux `reload_current_scene()`.
   - Toute future persistance devra être introduite via ADR dédiée (hors scope MVP).

3. **Retry = rechargement de scène**  
   Le retry est réalisé en rechargeant la scène courante (voir ADR-0012).

4. **Cibles de contenu MVP**  
   MVP vise :
   - 8–15 objets interactifs à terme (catalogue MVP peut démarrer à 7),
   - 3 vagues d'ennemis,
   - retry immédiat sans transitions lourdes.

## Validation Criteria

- [ ] Un retry remet tous les systèmes à l'état initial (aucune donnée persistée)
- [ ] Aucun fichier de sauvegarde / profil n'est créé en MVP

## GDD Requirements Addressed

| TR-ID | Requirement | ADR |
|---|---|---|
| TR-concept-001 | Session en pièce unique, solo ; aucune progression entre runs | Décisions 1–2 |
| TR-concept-002 | Cibles MVP + retry immédiat | Décisions 3–4 |

## Related Decisions

- ADR-0011 : GameState FSM (orchestration du retry)
- ADR-0012 : Retry wiring (reload_current_scene)
- `design/gdd/game-concept.md`

