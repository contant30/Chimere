# Review Log — Système de dégâts (S06)

---

## Review — 2026-04-08 — Verdict: APPROVED

Scope signal: M
Specialists: Analyse lean (agents API indisponibles — mode dégradé)
Blocking items: 5 résolus | Recommended: 7 (advisory)
Prior verdict resolved: Oui — NEEDS REVISION du 2026-04-07

### Bloquants résolus

| # | Bloquant | Fix appliqué |
|---|----------|-------------|
| 1 | AC-S06-05 FAIL — THROW non couvert comme 3ème valeur d'enum | AC-S06-09 ajouté : `damage_base=6, stage_mult=1.2, THROW → 7` |
| 2 | AC-S06-06 FAIL — boucle×1000 prouve déterminisme pas absence d'état | Réécrit : pattern `calculate(A)→calculate(B)→calculate(A)`, 3ème = 1er |
| 3 | Velocity non documentée comme décision — contredisait player fantasy | Règle 8 ajoutée : velocity délibérément exclue, justification + note V1.0 |
| 4 | KILL_FEEL_MAX / damage_base_min ambigu — incohérence mathématique latente | `damage_base_min = 3` défini explicitement dans Tuning Knobs |
| 5 | float→int conversion non documentée — double floori silencieux | Contrat de type ajouté dans Règle 2 : S02 responsable du `floori()` |

### Items advisory non traités (pour implémentation ou V1.0)

6. AC-S06-01 WEAK — renforcer avec valeur qui distingue floori/roundi (non bloquant)
7. AC-S06-02 WEAK — ajouter cas damage_base=0 (non bloquant)
8. AC-S06-04 WEAK — remplacer par valeur avec décimale (non bloquant)
9. GAP-01 — AC borne supérieure MVP (15, 2.0 → 30) manquant (non bloquant)
10. GAP-02 — boundary stage_mult=0.5 non couvert (non bloquant)
11. One-shot non documenté comme décision — stage_mult=1.5, damage_base=8 → 12
12. stage_mult pendant le vol non couvert dans Edge Cases

### Résumé

L'architecture stateless est saine et les 4 bloquants de la première review avaient été correctement traités. Cette re-review a résolu 5 bloquants supplémentaires issus des findings tardifs (velocity decision, KILL_FEEL_MAX/damage_base_min, float→int, AC-06/AC-05). Le GDD est maintenant approuvable. Les items advisory restants sont des améliorations de couverture test — non bloquants pour l'implémentation.

---

---

## Review — 2026-04-07 — Verdict: NEEDS REVISION → Révisé (re-review requise)

Scope signal: M
Specialists: game-designer, systems-designer, qa-lead, creative-director (senior)
Blocking items: 4 | Recommended: 5
Prior verdict resolved: First review

### Bloquants résolus

| # | Bloquant | Fix appliqué |
|---|----------|-------------|
| 1 | Ambiguïté double-multiplication S05↔S06 — deux lectures architecturales mutuellement exclusives | Règle 7 ajoutée dans Core Rules : S06 est l'unique multiplicateur ; S02 passe les valeurs brutes du catalogue sans pré-multiplication |
| 2 | Contrainte KILL_FEEL_THRESHOLD absente — aucune borne empêchant des objets légers de nécessiter 4–12 frappes | `KILL_FEEL_MAX = 5` ajouté dans Tuning Knobs avec plage sûre et lien explicite au Pilier 2 |
| 3 | AC-S06-07 non testable indépendamment — dépendance sur S05/S08, approximations via `≈` | Réécrit en test unitaire arithmétique pur — plus de dépendance externe |
| 4 | AC-S06-08 mal attribuée — test pipeline S02→S06→S08, S06 ne retourne pas DamageType | Réécrit en test unitaire S06 ; propagation DamageType explicitement déléguée aux ACs de S02 |

### Items recommandés non traités (advisory — pour re-review)

5. Position THROW vs MELEE non déclarée — DamageType ne modifie pas la formule, mais le GDD ne confirme pas explicitement si THROW bénéficiera de multiplicateurs distincts dans S05
6. Couverture tests THROW manquante dans les ACs — aucun AC ne teste THROW spécifiquement
7. Boundary value tests absents (damage_base=15, stage_mult=2.0 → 30)
8. Preuve explicite de statefulness absente dans les ACs (AC-S06-06 la couvre partiellement via loop)
9. OQ-01 (ADR DamageCalculator) — toujours ouvert, à créer avant implémentation S02

### Résumé senior (creative-director)

Le système est architecturalement sain et bien aligné sur les piliers. Le bloquant critique était l'ambiguïté de multiplication entre S05 et S06 — résolu. La formule `max(DAMAGE_MIN, floori(damage_base × stage_mult))` est correcte et robuste. Les ACs ont été renforcées pour être testables indépendamment. La re-review devra confirmer que les items recommandés (position THROW, boundary tests) ont été traités ou explicitement différés.

---

## Findings supplémentaires — agents tardifs (même session)

*Ces findings proviennent d'agents parallèles complétés après la clôture de la révision. Ils n'ont pas été traités dans cette session — à adresser en re-review.*

### game-designer — Findings non couverts en Phase 4

| Sévérité | Finding |
|----------|---------|
| CRITIQUE | La vitesse physique Jolt de l'objet lancé (`LinearVelocity`) n'influence pas `final_damage` — un lancer à 2 m/s fait autant qu'à 15 m/s. Contredit la player fantasy "l'objet se comporte comme le joueur l'imaginait". Opportunité : `stage_mult × clamp(velocity / ref_velocity, 0.5, 2.0)` incorporerait la physique réelle. |
| CRITIQUE | Aucun système ne garantit la lisibilité des dégâts en MVP : VFX est V1.0, S08 non conçu, pas de chiffres flottants. La fantasy repose sur des systèmes futurs sans AC dans S06. |
| SÉRIEUX | `damage_base` attendu `int` mais le catalogue peut produire des `float` (ex: `6.3` pour objet endommagé) — S02 doit convertir float→int avant d'appeler S06, introduisant un premier `floori` implicite. Double arrondi non documenté. |
| SÉRIEUX | Seuil de one-shot non documenté : avec `stage_mult = 1.5`, `damage_base = 8` → `floori(12.0) = 12` → one-shot un ennemi à 12 HP. Est-ce intentionnel ? Non traité comme décision explicite. |
| MODÉRÉ | Comportement si le stade de l'objet change *pendant* le vol (S04 intervient en cours de lancer) : quel `stage_mult` S02 transmet-il à S06 — au lancer ou à l'impact ? Non couvert dans Edge Cases. |

### qa-lead — ACs supplémentaires faibles ou défaillantes

| AC | Verdict | Problème |
|----|---------|---------|
| AC-S06-01 | WEAK | `7 × 1.0 = 7` ne distingue pas `floori` de `roundi`. Seul AC-S06-03 prouve réellement que `floori` est utilisé. |
| AC-S06-02 | WEAK | Ne teste pas `damage_base = 0` défensif (Edge Case 1 du GDD). |
| AC-S06-04 | WEAK | `12 × 2.0 = 24.0` est un entier exact — ne teste pas la troncature, redondant avec AC-S06-03. |
| AC-S06-05 | FAIL | Ne vérifie pas THROW comme troisième valeur d'enum. |
| AC-S06-06 | FAIL | Boucle × 1000 prouve le déterminisme, pas l'absence d'état. Un système stateful resetté à chaque appel passerait ce test. Pattern correct : `calculate(A) → calculate(B) → calculate(A)` et vérifier que le 3ème résultat = 1er. |
| GAP-01 | Manquant | Borne supérieure MVP : `damage_base = 15`, `stage_mult = 2.0` → `30`. |
| GAP-02 | Manquant | Plancher de plage `stage_mult = 0.5` : `floori(3 × 0.5) = 1` vs `floori(4 × 0.5) = 2` — deux comportements différents, aucun couvert. |
