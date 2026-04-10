# Journal de revue — S13 HUD

## Revue — 2026-04-10 — Verdict: À RÉVISER → Révisé en session

Signal de scope: L
Spécialistes: technical-director, qa-lead
Bloquants: 4 résolus | Recommandés: 3
Résumé: Le GDD S13 était globalement complet mais incohérent avec S12 : il supposait un retour de `GAME_OVER → PRE_WAVE` pour masquer l'écran Game Over, alors que le retry MVP est un `reload_current_scene()` qui détruit le HUD. La contrainte de timing mélangeait interactivité HUD et budget global de retry. Révisions appliquées : métadonnées en français, clarification que l'écran Game Over est interactif immédiatement (0 ms), que la sortie de GAME_OVER se fait via reload en MVP (HUD détruit/recréé), et que `retry_requested()` est un signal sortant unique consommé par S11 (S13 ne reset aucun système).
Verdict précédent résolu: Première revue
