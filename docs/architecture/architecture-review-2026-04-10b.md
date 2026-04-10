# Revue d'architecture - 2026-04-10 (follow-up)

**Mode :** suivi manuel post-résolution des bloquants  
**Moteur :** Godot 4.6.2 (Jolt, GDScript)  
**Entrées :** GDD MVP (incl. S04) + ADR-0001..ADR-0014  
**Artefacts mis a jour :** `docs/architecture/architecture-traceability.md`, `docs/registry/architecture.yaml`

---

## Verdict : PASS

Raison : les ADR fondamentaux sont désormais `Accepted` et la couverture des TR-ID MVP est complète.

---

## Changements depuis la revue FAIL

1. **ADRs `Accepted`**
   - ADR-0001..ADR-0005 passés en `Accepted`
   - ADR-0006..ADR-0014 ajoutés (coyote/gravity, caméra, health, ennemis, vagues, FSM, retry, HUD, contraintes concept)

2. **Couverture TR-ID**
   - Matrice mise à jour : 48/48 exigences marquées `COUVERT` (voir `docs/architecture/architecture-traceability.md`)

3. **Registre architecture**
   - Ajout des contracts d'interface + ownership (voir `docs/registry/architecture.yaml`)

---

## Notes / vérifications reportées au prototype (non bloquantes doc)

- Validation Jolt : `freeze_mode KINEMATIC` (GrabSystem) et ressenti impulse `apply_central_impulse()`
- SpringArm anti-clipping dans une salle dense
- Budget retry (mesure `scene_reload_time`)

