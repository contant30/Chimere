# Review Log — S01 Déplacement joueur

## Review — 2026-04-08 — Verdict: NEEDS REVISION → Révisé en session

Scope signal: M
Specialists: game-designer, systems-designer, qa-lead, godot-gdscript-specialist, gameplay-programmer, creative-director
Blocking items: 10 | Recommended: 12
Summary: Le GDD présentait un bug de code dans F2 (AIR_CONTROL jamais appliqué, ordering gravité/saut incorrect), des valeurs de tuning sous-optimales (ACCELERATION trop bas à 20.0, AIR_CONTROL MVP trop élevé à 0.6), une contrainte de couplage FRICTION/MOVE_SPEED manquante, et l'absence du coyote time jugé bloquant par le creative-director. Les contrats inter-systèmes avec S02 (AIRBORNE) et S10 (initialisation) n'étaient pas documentés. Toutes les révisions ont été appliquées en session : F2 corrigé avec AIR_CONTROL actif, coyote time intégré (4–6 frames), formules F3/F4 ajoutées, AC-S01-11 ajouté, 6 items recommandés résolus (dont extension AC-S01-01, co-calibration JUMP_VELOCITY/GRAVITY, volume atterrissage).
Prior verdict resolved: N/A — première review.
