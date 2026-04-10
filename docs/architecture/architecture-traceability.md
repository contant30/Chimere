# Architecture Traceability Index

<!-- Living document — updated by /architecture-review after each review run.
     Do not edit manually unless correcting an error. -->

## Document Status

- **Last Updated**: 2026-04-10
- **Engine**: Godot 4.6.2
- **GDDs Indexed**: 14
- **ADRs Indexed**: 3
- **Last Review**: `docs/architecture/architecture-review-2026-04-10.md`

## Coverage Summary

| Status | Count | Percentage |
|--------|-------|-----------|
| ✅ Covered | 0 | 0% |
| ⚠️ Partial | 10 | 20.8% |
| ❌ Gap | 38 | 79.2% |
| **Total** | **48** | |

---

## Traceability Matrix

| Req ID | GDD | System | Requirement Summary | ADR(s) | Status | Notes |
|--------|-----|--------|---------------------|--------|--------|-------|
| TR-concept-001 | design/gdd/game-concept.md | concept | Single-room, single-player sessions; no progression between runs. | — | ❌ GAP | Needs explicit architecture baseline doc (architecture.md or ADR). |
| TR-concept-002 | design/gdd/game-concept.md | concept | MVP content targets and immediate retry as a core pillar. | — | ❌ GAP | Needs mapping to S12/S11 ADRs. |
| TR-systems-index-001 | design/gdd/systems-index.md | systems-index | S03↔S11 signals contract to break circular dependency. | — | ❌ GAP | Needs ADR defining the signal contract + ownership. |
| TR-deplacement-joueur-001 | design/gdd/deplacement-joueur.md | deplacement-joueur | CharacterBody3D + move_and_slide(). | ADR-0002 | ⚠️ PARTIAL | ADR-0002 is still Proposed (not Accepted). |
| TR-deplacement-joueur-002 | design/gdd/deplacement-joueur.md | deplacement-joueur | Player must not push RigidBody3D; enforce via collision layers/masks. | ADR-0002 | ⚠️ PARTIAL | ADR-0002 is still Proposed (not Accepted). |
| TR-deplacement-joueur-003 | design/gdd/deplacement-joueur.md | deplacement-joueur | Single jump + coyote time (COYOTE_FRAMES). | — | ❌ GAP | Needs movement implementation decision scope (ADR or architecture.md). |
| TR-deplacement-joueur-004 | design/gdd/deplacement-joueur.md | deplacement-joueur | Manual gravity sourced from ProjectSettings default gravity. | — | ❌ GAP | Needs movement implementation decision scope (ADR or architecture.md). |
| TR-saisie-lancer-001 | design/gdd/saisie-lancer.md | saisie-lancer | Grab cone + grab_range_m (from S05), single held object. | ADR-0001 | ⚠️ PARTIAL | ADR-0001 is Proposed; S05 dependency not covered by ADR. |
| TR-saisie-lancer-002 | design/gdd/saisie-lancer.md | saisie-lancer | Carry object kinematic/frozen + carry_offset; carried collisions don’t block player. | ADR-0001 | ⚠️ PARTIAL | Validate Jolt freeze behavior in prototype; then accept ADR. |
| TR-saisie-lancer-003 | design/gdd/saisie-lancer.md | saisie-lancer | Throw uses apply_central_impulse() along camera yaw. | ADR-0001 | ⚠️ PARTIAL | ADR-0001 is Proposed; depends on S10 yaw contract. |
| TR-saisie-lancer-004 | design/gdd/saisie-lancer.md | saisie-lancer | GrabSystem signals grab_performed/throw_performed/melee_performed. | ADR-0001 | ⚠️ PARTIAL | Also affects S13/S08/S04/S11 integration. |
| TR-catalogue-objets-001 | design/gdd/catalogue-objets.md | catalogue-objets | Catalogue Resources + per-object @export entry; no global lookup. | — | ❌ GAP | Needs S05 data-model ADR. |
| TR-catalogue-objets-002 | design/gdd/catalogue-objets.md | catalogue-objets | Entry includes physics + interaction parameters. | — | ❌ GAP | Needs S05 data-model ADR. |
| TR-catalogue-objets-003 | design/gdd/catalogue-objets.md | catalogue-objets | Multi-stage destruction transitions (damage thresholds / uses). | — | ❌ GAP | Needs S05/S04 boundary ADR. |
| TR-catalogue-objets-004 | design/gdd/catalogue-objets.md | catalogue-objets | DestructionTracker reads entry once at _ready() and updates on receive_damage/register_use. | — | ❌ GAP | Needs S04 implementation + ownership ADR. |
| TR-systeme-degats-001 | design/gdd/systeme-degats.md | systeme-degats | Pure stateless damage function (no node/signals/state). | ADR-0003 | ⚠️ PARTIAL | ADR-0003 is Proposed (not Accepted). |
| TR-systeme-degats-002 | design/gdd/systeme-degats.md | systeme-degats | calculate(damage_base:int, stage_mult:float, damage_type) -> int; no direct S05 read. | ADR-0003 | ⚠️ PARTIAL | Requires call-site rules (S02/S09) to be enforced. |
| TR-systeme-degats-003 | design/gdd/systeme-degats.md | systeme-degats | final_damage = max(1, floori(damage_base * stage_mult)). | ADR-0003 | ⚠️ PARTIAL | Add unit tests once test harness exists. |
| TR-systeme-degats-004 | design/gdd/systeme-degats.md | systeme-degats | DamageType enum values; does not affect math. | ADR-0003 | ⚠️ PARTIAL | Ensure shared type import strategy for S02/S07/S08/S09. |
| TR-sante-joueur-001 | design/gdd/sante-joueur.md | sante-joueur | Player receive_damage(amount:int, type:DamageType) does not recalc damage. | — | ❌ GAP | Needs S07 component + wiring ADR. |
| TR-sante-joueur-002 | design/gdd/sante-joueur.md | sante-joueur | I-frames for player (0.5s). | — | ❌ GAP | Needs S07 component ADR (timer strategy, determinism). |
| TR-sante-joueur-003 | design/gdd/sante-joueur.md | sante-joueur | Emit player_hp_changed/player_hit; emit player_died once; ignore after death. | — | ❌ GAP | Needs S07/S11/S13 signal ownership ADR. |
| TR-sante-ennemie-001 | design/gdd/sante-ennemie.md | sante-ennemie | Enemy receive_damage processes every hit (no i-frames). | — | ❌ GAP | Needs S08 component + wiring ADR. |
| TR-sante-ennemie-002 | design/gdd/sante-ennemie.md | sante-ennemie | Emit enemy_hit for feedback; no HP bar in MVP. | — | ❌ GAP | Needs S08→S15 signal contract ADR. |
| TR-sante-ennemie-003 | design/gdd/sante-ennemie.md | sante-ennemie | Emit enemy_died once then queue_free enemy. | — | ❌ GAP | Needs S08→S03/S11/S12 contract ADR. |
| TR-ia-ennemie-001 | design/gdd/ia-ennemie.md | ia-ennemie | Enemy scene composition (CharacterBody3D + S08 + NavigationAgent3D). | — | ❌ GAP | Needs S09 scene contract ADR (node names, ownership). |
| TR-ia-ennemie-002 | design/gdd/ia-ennemie.md | ia-ennemie | Dependency injection via @export before add_child; _ready wires signals. | — | ❌ GAP | Needs DI + signal wiring conventions ADR. |
| TR-ia-ennemie-003 | design/gdd/ia-ennemie.md | ia-ennemie | NavigationAgent3D targets player; navmesh only static geometry. | — | ❌ GAP | Needs navmesh + dynamic obstacle policy ADR. |
| TR-ia-ennemie-004 | design/gdd/ia-ennemie.md | ia-ennemie | STUCK fallback: straight-line movement + periodic path retries. | — | ❌ GAP | Needs behavior ownership ADR (AI vs navigation module). |
| TR-camera-tps-001 | design/gdd/camera-tps.md | camera-tps | Pivot + SpringArm3D composition and defaults. | — | ❌ GAP | Needs S10 camera ADR. |
| TR-camera-tps-002 | design/gdd/camera-tps.md | camera-tps | Yaw free, pitch clamp, fixed FOV. | — | ❌ GAP | Needs S10 camera ADR. |
| TR-camera-tps-003 | design/gdd/camera-tps.md | camera-tps | Emit camera_yaw_changed every frame + at _ready. | — | ❌ GAP | Needs S10→S01 contract ADR. |
| TR-camera-tps-004 | design/gdd/camera-tps.md | camera-tps | freeze()/unfreeze() and freeze on player_died. | — | ❌ GAP | Needs S10↔S11 interface ADR. |
| TR-vagues-ennemis-001 | design/gdd/vagues-ennemis.md | vagues-ennemis | Static 3-wave structure [3,5,7]. | — | ❌ GAP | Needs S03 wave manager ADR. |
| TR-vagues-ennemis-002 | design/gdd/vagues-ennemis.md | vagues-ennemis | Spawn from SpawnPoint nodes with interval + DI before add_child. | — | ❌ GAP | Needs S03 spawn + DI ADR. |
| TR-vagues-ennemis-003 | design/gdd/vagues-ennemis.md | vagues-ennemis | Track enemies_alive; wave_cleared/all_waves_complete. | — | ❌ GAP | Needs S03→S11/S13 contract ADR. |
| TR-vagues-ennemis-004 | design/gdd/vagues-ennemis.md | vagues-ennemis | Start spawning only on game_state_changed(COMBAT). | — | ❌ GAP | Needs S03↔S11 handshake ADR. |
| TR-gestionnaire-etat-001 | design/gdd/gestionnaire-etat.md | gestionnaire-etat | S11 is sole state authority; emits game_state_changed. | — | ❌ GAP | Needs S11 FSM ADR. |
| TR-gestionnaire-etat-002 | design/gdd/gestionnaire-etat.md | gestionnaire-etat | FSM transitions driven by S03/S07 signals. | — | ❌ GAP | Needs S11 FSM ADR. |
| TR-gestionnaire-etat-003 | design/gdd/gestionnaire-etat.md | gestionnaire-etat | GAME_OVER triggers S10.freeze + retry within ≤3s via S12. | — | ❌ GAP | Needs S11/S12 interface ADR. |
| TR-gestionnaire-etat-004 | design/gdd/gestionnaire-etat.md | gestionnaire-etat | No gameplay logic in S11. | — | ❌ GAP | Needs S11 ADR scope. |
| TR-retry-reinitialisation-001 | design/gdd/retry-reinitialisation.md | retry-reinitialisation | S12 retry() calls reload_current_scene(). | — | ❌ GAP | Needs S12 ADR (wiring + failure strategy). |
| TR-retry-reinitialisation-002 | design/gdd/retry-reinitialisation.md | retry-reinitialisation | Triggered only by S11 in GAME_OVER. | — | ❌ GAP | Needs S11→S12 interface ADR. |
| TR-retry-reinitialisation-003 | design/gdd/retry-reinitialisation.md | retry-reinitialisation | Total retry time ≤ 3s; no fade in MVP. | — | ❌ GAP | Needs performance budget + measurement strategy. |
| TR-hud-001 | design/gdd/hud.md | hud | HUD is CanvasLayer and read-only (minimal outbound). | — | ❌ GAP | Needs UI architecture ADR (signals, scene placement). |
| TR-hud-002 | design/gdd/hud.md | hud | Consumes S07/S03/GrabSystem signals to drive HP/waves/silhouette. | — | ❌ GAP | Depends on S07/S03/S11/S02 ADRs. |
| TR-hud-003 | design/gdd/hud.md | hud | HP bar immediate fill update + 440ms hit flash rules. | — | ❌ GAP | UI implementation spec; no ADR yet. |
| TR-hud-004 | design/gdd/hud.md | hud | Emits retry_requested() only in GAME_OVER to S11. | — | ❌ GAP | Needs S13↔S11 interface ADR. |

---

## Known Gaps

### Foundation Layer Gaps (BLOCKING — must resolve before coding)

- [ ] TR-catalogue-objets-001 — Catalogue data access pattern (Resources + per-object `@export`) needs an ADR.
- [ ] TR-catalogue-objets-002 — Catalogue schema fields need an ADR.
- [ ] TR-catalogue-objets-003 — Destruction stages ownership boundaries (S05/S04/S02) need an ADR.
- [ ] TR-catalogue-objets-004 — DestructionTracker ownership and lifecycle need an ADR.
- [ ] TR-deplacement-joueur-003 — Movement jump model scope needs an explicit decision (ADR or architecture.md).
- [ ] TR-deplacement-joueur-004 — Gravity source/update rule needs an explicit decision (ADR or architecture.md).

### Core Layer Gaps (must resolve before relevant system is built)

- [ ] TR-camera-tps-001..004 — Camera architecture ADR missing.
- [ ] TR-ia-ennemie-001..004 — Enemy AI/scene architecture ADR missing.
- [ ] TR-sante-joueur-001..003 — Player health component ADR missing.
- [ ] TR-sante-ennemie-001..003 — Enemy health component ADR missing.

### Feature / Presentation Layer Gaps (should resolve before feature sprint)

- [ ] TR-vagues-ennemis-001..004 — Wave manager architecture ADR missing.
- [ ] TR-gestionnaire-etat-001..004 — Game state manager architecture ADR missing.
- [ ] TR-retry-reinitialisation-001..003 — Retry wiring/performance ADR missing.
- [ ] TR-hud-001..004 — HUD architecture ADR missing.

---

## Cross-ADR Conflicts

| Conflict ID | ADR A | ADR B | Type | Status |
|-------------|-------|-------|------|--------|
| CONFLICT-001 | ADR-0001 | ADR-0002 | Dependency ordering | 🔴 Unresolved |

---

## ADR → GDD Coverage (Reverse Index)

| ADR | Title | GDD Requirements Addressed | Engine Risk |
|-----|-------|---------------------------|-------------|
| ADR-0001 | GrabSystem Architecture | TR-saisie-lancer-001, TR-saisie-lancer-002, TR-saisie-lancer-003, TR-saisie-lancer-004 | HIGH |
| ADR-0002 | Player Body Type and Collision Layers | TR-deplacement-joueur-001, TR-deplacement-joueur-002 | HIGH |
| ADR-0003 | DamageCalculator — Patron static func | TR-systeme-degats-001, TR-systeme-degats-002, TR-systeme-degats-003, TR-systeme-degats-004 | HIGH |

