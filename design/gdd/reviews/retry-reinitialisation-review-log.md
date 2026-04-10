# Journal de revue — S12 Retry / réinitialisation

## Revue — 2026-04-10 — Verdict: À RÉVISER → Révisé en session

Signal de scope: M
Spécialistes: technical-director, qa-lead
Bloquants: 3 résolus | Recommandés: 2
Résumé: Le GDD S12 spécifiait un déclenchement uniquement « après RETRY_DELAY » sans intégrer le cas `retry_requested()` (HUD) pourtant requis, ce qui laissait l'interface S11↔S12 et le flux d'input incohérents entre documents. Une question ouverte maintenait une ambiguïté inutile (signal vs appel direct). Révisions appliquées : S12 reste minimal (une seule méthode `retry()`), mais explicite que S11 peut l'appeler en auto-retry ou immédiatement sur demande HUD ; l'interface est fixée (appel direct via référence `@export` dans S11).
Verdict précédent résolu: Première revue
