# Architecture Review — 2026-04-10

**Mode:** `/architecture-review` (full)  
**Engine:** Godot 4.6.2 (Jolt, GDScript)  
**Inputs loaded:** 14 GDDs (`design/gdd/*.md`), 3 ADRs (`docs/architecture/adr-*.md`)  
**Artifacts updated:** `docs/architecture/tr-registry.yaml`, `docs/architecture/architecture-traceability.md`

---

## Verdict: FAIL

Reason: foundational requirements are not backed by **Accepted** ADRs, and the current ADR set does not cover most MVP systems. There is also a cross-ADR dependency ordering inconsistency (see Conflict #1).

---

## What’s in good shape

- ADR format completeness: `ADR-0001`, `ADR-0002`, `ADR-0003` include the required template sections (Status/Context/Decision/Consequences/Dependencies/Engine Compatibility/GDD Requirements Addressed).
- Engine pin is explicit (Godot 4.6.2) and ADRs cite the local engine reference docs.
- S06 (damage formula) is clearly specified and centralized via ADR-0003.

---

## Blocking Issues (must resolve before PASS)

1. **No Accepted ADRs**  
   All current ADRs are `Proposed`. This blocks story creation/implementation for the systems they claim to gate (S01/S02/S06).

2. **Foundation layer gaps (architecture coverage)**
   - S05 (Catalogue d’objets) has no ADR defining its data model and runtime access pattern (the GDD requires Resource-based entries + per-object `@export` references and no global lookup).
   - S01, S10, S11, S12, S03, S07/S08, S09 are not covered by Accepted ADRs.

3. **Conflict #1: ADR dependency ordering mismatch**
   - `ADR-0002` states its collision layer scheme is required for S02 raycast masking, which implies `ADR-0001` depends on it.
   - `ADR-0001` marks `ADR-0002` as “Enables”, while `ADR-0002` marks `ADR-0001` as “Enables”. Dependency direction and ordering note are inconsistent.

4. **Godot deprecated-pattern risk (design-level)**
   `docs/engine-reference/godot/deprecated-apis.md` flags string-based `connect()` as deprecated. Several GDDs describe wiring signals via “connect()” without specifying typed-callable usage. This needs an explicit coding/architecture rule to prevent regressions.

---

## Cross-ADR Conflicts

| Conflict ID | ADR A | ADR B | Type | Status |
|-------------|-------|-------|------|--------|
| CONFLICT-001 | ADR-0001 | ADR-0002 | Dependency ordering | 🔴 Unresolved |

---

## Coverage Summary (TR registry)

The TR registry was bootstrapped in `docs/architecture/tr-registry.yaml` and indexed in `docs/architecture/architecture-traceability.md`.

High-level state right now:
- Requirements with any ADR mapping: limited to S01/S02/S06 (and only as Proposed ADRs).
- Most MVP systems remain architectural gaps (S03/S05/S07/S08/S09/S10/S11/S12/S13).

---

## Required ADRs (prioritised)

### Foundation (BLOCKING)

1. **S05 — Object catalogue data model**
   - Resource schema (`ObjectCatalogueEntry`, stages, thresholds, fields) and access pattern (`@export` direct reference; no global lookup).

2. **Signals & dependency injection conventions (cross-cutting)**
   - Typed signal connections (Callable-based), required signal naming, injection approach (`@export` vs constructor patterns), and “no hidden globals”.

3. **S01 — Player movement implementation boundaries**
   - What is “architecture” vs “tuning” for movement, and how S01 depends on S10 (camera yaw contract).

### Core / Infrastructure (BLOCKING for those systems)

4. **S10 — Camera node architecture**
   - Pivot + SpringArm composition, collision masks (exclude layer 3 objects), freeze/unfreeze contract.

5. **S11 — Game state manager architecture**
   - FSM ownership, signal contracts, freeze/retry sequencing.

6. **S12 — Retry wiring**
   - Interface choice S11→S12 (direct call via injected reference vs signal), and the “≤ 3s” budget enforcement strategy.

7. **S03 — Wave manager architecture**
   - Spawnpoints, injection, lifecycle/abort behavior on GAME_OVER.

8. **S07/S08 — Health component contracts**
   - Shared `receive_damage()` contract, signal ownership, idempotence rules.

9. **S09 — Enemy scene composition**
   - NavigationAgent3D usage boundaries, STUCK fallback, how S02 finds S08 reliably (scene-local node path contract).

---

## Next Step

1. Resolve `CONFLICT-001` by aligning ADR-0001/0002 dependency direction and ordering notes.
2. Promote ADR-0002 and ADR-0003 to `Accepted` once validated, then decide whether ADR-0001 is ready to accept.
3. Write the missing Foundation/Core ADRs above, then re-run `/architecture-review` (full).

