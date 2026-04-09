---
name: Project Saisir — State and Key Decisions
description: Saisir is a 3D action game (Godot 4.6.2) — current phase is design, sprint S01/S02 active
type: project
---

Game is called "Saisir." Godot 4.6.2, GDScript, Forward+, Jolt physics. PC-first (Steam/itch.io).

15 systems identified in MVP. Design order: S05→S06→S01→S02 (S02 is risk #1 — prototype week 1).

Key QA context:
- S01 (Player Movement) GDD written 2026-04-08, status: In Design. 10 ACs written but adversarial review found 9 blocking gaps (see project/qa notes).
- S06 (Damage System) GDD approved, 9 ACs.
- AIR_CONTROL (0.6) is a known gap — in tuning knobs but not yet in F2 formula code. No AC covers it.
- OQ-04: ADR for CharacterBody3D + move_and_slide() pattern required before S01 implementation.
- OQ-01: Coyote time decision deferred to S01 prototype.

**Why:** S02 is highest risk because it involves physics interaction (grab/throw) with Jolt RigidBody3D — unproven in this codebase.
**How to apply:** Flag S01 and S02 as needing ADRs before implementation starts. Watch for AIR_CONTROL AC gap when S01 implementation begins.
