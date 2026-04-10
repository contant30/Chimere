# Journal de revue — S11 Gestionnaire d'état de jeu

## Revue — 2026-04-10 — Verdict: À RÉVISER → Révisé en session

Signal de scope: M
Spécialistes: technical-director, qa-lead
Bloquants: 4 résolus | Recommandés: 2
Résumé: Le GDD S11 décrivait le retry comme une transition `GAME_OVER → PRE_WAVE` sans préciser l'impact du reload (S12) sur la durée de vie de S11/S13, et ne documentait pas le contrat `retry_requested()` émis par le HUD. La responsabilité de l'unfreeze caméra était ambiguë et le périmètre d'UI VICTORY contredisait S13 (pas d'écran victoire en MVP). Révisions appliquées : ajout du chemin de signal `S13.retry_requested() → S11 → S12.retry()` (avec annulation de l'auto-retry), clarification que la sortie de GAME_OVER se fait via reload (nouvelle instance repart en PRE_WAVE), et alignement UI (GAME_OVER via S13, VICTORY no-op en MVP).
Verdict précédent résolu: Première revue
