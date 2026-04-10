# Revue d'architecture - 2026-04-10

**Mode :** `/architecture-review` (full)  
**Moteur :** Godot 4.6.2 (Jolt, GDScript)  
**Entrees chargees :** 14 GDD (`design/gdd/*.md`), 5 ADR (`docs/architecture/adr-*.md`)  
**Artefacts mis a jour :** `docs/architecture/tr-registry.yaml`, `docs/architecture/architecture-traceability.md`

---

## Verdict : FAIL

Raison : les exigences fondamentales ne sont pas couvertes par des ADR **Accepted**, et l'ensemble actuel d'ADR ne couvre pas la plupart des systemes MVP.

---

## Points solides

- Format ADR : `ADR-0001`, `ADR-0002`, `ADR-0003` contiennent les sections attendues (Status, Context, Decision, Consequences, ADR Dependencies, Engine Compatibility, GDD Requirements Addressed).
- Le moteur est clairement "pinned" (Godot 4.6.2) et les ADR citent la reference moteur locale.
- S06 (formule de degats) est specifie de facon claire et centralise via `ADR-0003`.

---

## Bloquants (a resoudre avant PASS)

1. **Aucun ADR Accepted**  
   Les 3 ADR existants sont `Proposed`. Ca bloque la creation/implementation de stories pour les systemes qu'ils disent "gater" (S01/S02/S06).

2. **Gros manques de couverture (architecture)**
   - S05 (Catalogue d'objets) a un ADR de modele de donnees (`ADR-0004`) mais il est encore `Proposed` (pas `Accepted`).
   - Les conventions transversales DI + signaux existent (`ADR-0005`) mais sont encore `Proposed` (pas `Accepted`).
   - S03, S07/S08, S09, S10, S11, S12, S13 n'ont pas d'ADR (Accepted) definissant leurs contrats et limites.

3. **Risque "patterns deprecies" (Godot)**
   `docs/engine-reference/godot/deprecated-apis.md` considere les connexions de signaux en `connect("signal", ...)` (string-based) comme depreciees au profit des Callables. Il faut une regle d'architecture/coding pour l'imposer et eviter les regressions.

---

## Conflits inter-ADR

| Conflict ID | ADR A | ADR B | Type | Statut |
|-------------|-------|-------|------|--------|
| CONFLICT-001 | ADR-0001 | ADR-0002 | Ordre de dependances | RESOLU (ADR-0001 depend de ADR-0002 ; ordering notes alignees) |

---

## Resume couverture (TR registry)

Le registre TR a ete initialise dans `docs/architecture/tr-registry.yaml` et indexe dans `docs/architecture/architecture-traceability.md`.

Etat a date :
- Exigences avec un mapping ADR : limite a S01/S02/S06 (et seulement via des ADR Proposed).
- La plupart des systemes MVP restent des trous d'architecture (S03/S05/S07/S08/S09/S10/S11/S12/S13).

---

## ADR requis (priorises)

### Foundation (BLOCKING)

1. **S05 - Catalogue d'objets**
   - Faire passer `ADR-0004` en `Accepted` apres validation (wiring + coherences des Resources).

2. **Conventions signaux + injection de dependances (transversal)**
   - Faire passer `ADR-0005` en `Accepted`, puis l'appliquer partout (Callable connect, DI `@export`, pas d'Autoload sans ADR).

3. **S01 - Limites d'implementation du mouvement**
   - Ce qui releve de l'architecture vs du tuning, et le contrat S01 <-> S10 (yaw camera).

### Core / Infrastructure (bloquant par systeme)

4. **S10 - Architecture camera**
   - Pivot + SpringArm, masks de collision (exclure layer 3), contrat freeze/unfreeze.

5. **S11 - Architecture FSM etat de jeu**
   - Autorite FSM, contrats de signaux, sequencing freeze/retry.

6. **S12 - Wiring retry**
   - Interface S11 -> S12 (appel direct injecte vs signal) et strategie pour garantir le budget "<= 3s".

7. **S03 - Architecture vagues**
   - SpawnPoints, injection, lifecycle/abort en GAME_OVER.

8. **S07/S08 - Contrats sante**
   - Contrat commun `receive_damage()`, ownership des signaux, regles d'idempotence.

9. **S09 - Contrat de scene ennemi**
   - Composition, limites NavigationAgent3D, fallback STUCK, et comment S02 trouve S08 de facon robuste (contrat de node path).

### Presentation

10. **S13 - HUD**
   - Placement (CanvasLayer), signaux consommes, et interface `retry_requested` -> S11.

---

## Suite

1. Faire passer `ADR-0002` et `ADR-0003` en `Accepted` une fois valides, puis decider si `ADR-0001` est pret a etre accepte.
2. Ecrire les ADR Foundation/Core manquants ci-dessus, puis relancer `/architecture-review` (full).
