# Index de tracabilite d'architecture

<!-- Document vivant - mis a jour par /architecture-review apres chaque revue.
     Ne pas editer manuellement sauf correction d'erreur. -->

## Statut du document

- **Derniere mise a jour :** 2026-04-10
- **Moteur :** Godot 4.6.2
- **GDD indexees :** 14
- **ADR indexees :** 14
- **Derniere revue :** `docs/architecture/architecture-review-2026-04-10b.md`

## Resume de couverture

| Statut | Nombre | Pourcentage |
|--------|--------|-------------|
| COUVERT | 48 | 100% |
| PARTIEL | 0 | 0% |
| MANQUE | 0 | 0% |
| **Total** | **48** | |

---

## Matrice de tracabilite

| ID TR | GDD | Systeme | Resume exigence | ADR(s) | Statut | Notes |
|-------|-----|---------|-----------------|--------|--------|-------|
| TR-concept-001 | design/gdd/game-concept.md | concept | Sessions en piece unique, solo ; aucune progression entre les runs. | ADR-0014 | COUVERT | — |
| TR-concept-002 | design/gdd/game-concept.md | concept | Cibles de contenu MVP + retry immediat comme pilier. | ADR-0014 | COUVERT | — |
| TR-systems-index-001 | design/gdd/systems-index.md | systems-index | Contrat de signaux S03<->S11 pour casser la dependance circulaire. | ADR-0010, ADR-0011 | COUVERT | — |
| TR-deplacement-joueur-001 | design/gdd/deplacement-joueur.md | deplacement-joueur | CharacterBody3D + move_and_slide(). | ADR-0002 | COUVERT | — |
| TR-deplacement-joueur-002 | design/gdd/deplacement-joueur.md | deplacement-joueur | Le joueur ne doit pas pousser les RigidBody3D ; a imposer via layers/masks. | ADR-0002 | COUVERT | — |
| TR-deplacement-joueur-003 | design/gdd/deplacement-joueur.md | deplacement-joueur | Saut unique + coyote time (COYOTE_FRAMES). | ADR-0006 | COUVERT | — |
| TR-deplacement-joueur-004 | design/gdd/deplacement-joueur.md | deplacement-joueur | Gravite appliquee manuellement via ProjectSettings (default gravity). | ADR-0006 | COUVERT | — |
| TR-saisie-lancer-001 | design/gdd/saisie-lancer.md | saisie-lancer | Cone de saisie + grab_range_m (via S05), un seul objet tenu. | ADR-0001, ADR-0004 | COUVERT | — |
| TR-saisie-lancer-002 | design/gdd/saisie-lancer.md | saisie-lancer | Portage : objet kinematic/freeze + carry_offset ; collisions portees ne bloquent pas le joueur. | ADR-0001 | COUVERT | — |
| TR-saisie-lancer-003 | design/gdd/saisie-lancer.md | saisie-lancer | Lancer : apply_central_impulse() aligne sur le yaw camera. | ADR-0001, ADR-0007 | COUVERT | — |
| TR-saisie-lancer-004 | design/gdd/saisie-lancer.md | saisie-lancer | Signaux GrabSystem : grab_performed / throw_performed / melee_performed. | ADR-0001 | COUVERT | — |
| TR-catalogue-objets-001 | design/gdd/catalogue-objets.md | catalogue-objets | Catalogue : Resources + entree `@export` par objet ; pas de lookup global. | ADR-0004 | COUVERT | — |
| TR-catalogue-objets-002 | design/gdd/catalogue-objets.md | catalogue-objets | L'entree inclut les params physiques + interaction. | ADR-0004 | COUVERT | — |
| TR-catalogue-objets-003 | design/gdd/catalogue-objets.md | catalogue-objets | Destruction multi-stades (seuils degats / uses). | ADR-0004 | COUVERT | — |
| TR-catalogue-objets-004 | design/gdd/catalogue-objets.md | catalogue-objets | DestructionTracker lit l'entree en _ready() et update sur receive_damage/register_use. | ADR-0004 | COUVERT | — |
| TR-systeme-degats-001 | design/gdd/systeme-degats.md | systeme-degats | Fonction de degats pure stateless (pas de node/signaux/etat). | ADR-0003 | COUVERT | — |
| TR-systeme-degats-002 | design/gdd/systeme-degats.md | systeme-degats | calculate(damage_base:int, stage_mult:float, damage_type) -> int ; pas de lecture directe S05. | ADR-0003 | COUVERT | — |
| TR-systeme-degats-003 | design/gdd/systeme-degats.md | systeme-degats | final_damage = max(1, floori(damage_base * stage_mult)). | ADR-0003 | COUVERT | — |
| TR-systeme-degats-004 | design/gdd/systeme-degats.md | systeme-degats | DamageType enum ; n'influence pas les maths (sert au feedback). | ADR-0003 | COUVERT | — |
| TR-sante-joueur-001 | design/gdd/sante-joueur.md | sante-joueur | Player receive_damage(amount:int, type:DamageType) ne recalcule pas les degats. | ADR-0008 | COUVERT | — |
| TR-sante-joueur-002 | design/gdd/sante-joueur.md | sante-joueur | I-frames joueur (0.5s). | ADR-0008 | COUVERT | — |
| TR-sante-joueur-003 | design/gdd/sante-joueur.md | sante-joueur | Emet player_hp_changed/player_hit ; emet player_died une fois ; ignore apres mort. | ADR-0008 | COUVERT | — |
| TR-sante-ennemie-001 | design/gdd/sante-ennemie.md | sante-ennemie | Enemy receive_damage traite tous les hits (pas d'i-frames). | ADR-0008 | COUVERT | — |
| TR-sante-ennemie-002 | design/gdd/sante-ennemie.md | sante-ennemie | Emet enemy_hit pour feedback ; pas de barre de vie en MVP. | ADR-0008 | COUVERT | — |
| TR-sante-ennemie-003 | design/gdd/sante-ennemie.md | sante-ennemie | Emet enemy_died une fois puis queue_free. | ADR-0008 | COUVERT | — |
| TR-ia-ennemie-001 | design/gdd/ia-ennemie.md | ia-ennemie | Contrat scene ennemi (CharacterBody3D + S08 + NavigationAgent3D). | ADR-0009 | COUVERT | — |
| TR-ia-ennemie-002 | design/gdd/ia-ennemie.md | ia-ennemie | Injection via @export avant add_child ; _ready cable les signaux. | ADR-0009 | COUVERT | — |
| TR-ia-ennemie-003 | design/gdd/ia-ennemie.md | ia-ennemie | NavigationAgent3D cible player ; navmesh = geometrie statique uniquement. | ADR-0009 | COUVERT | — |
| TR-ia-ennemie-004 | design/gdd/ia-ennemie.md | ia-ennemie | Fallback STUCK : ligne droite + retry path periodique. | ADR-0009 | COUVERT | — |
| TR-camera-tps-001 | design/gdd/camera-tps.md | camera-tps | Pivot + SpringArm3D (composition + valeurs par defaut). | ADR-0007 | COUVERT | — |
| TR-camera-tps-002 | design/gdd/camera-tps.md | camera-tps | Yaw libre, pitch clamp, FOV fixe. | ADR-0007 | COUVERT | — |
| TR-camera-tps-003 | design/gdd/camera-tps.md | camera-tps | Emet camera_yaw_changed chaque frame + au _ready. | ADR-0007 | COUVERT | — |
| TR-camera-tps-004 | design/gdd/camera-tps.md | camera-tps | freeze()/unfreeze() + freeze sur player_died. | ADR-0007, ADR-0011 | COUVERT | — |
| TR-vagues-ennemis-001 | design/gdd/vagues-ennemis.md | vagues-ennemis | Structure MVP de 3 vagues [3,5,7]. | ADR-0010 | COUVERT | — |
| TR-vagues-ennemis-002 | design/gdd/vagues-ennemis.md | vagues-ennemis | Spawn via SpawnPoints + intervalle + DI avant add_child. | ADR-0010 | COUVERT | — |
| TR-vagues-ennemis-003 | design/gdd/vagues-ennemis.md | vagues-ennemis | enemies_alive ; wave_cleared/all_waves_complete. | ADR-0010 | COUVERT | — |
| TR-vagues-ennemis-004 | design/gdd/vagues-ennemis.md | vagues-ennemis | Spawn uniquement sur game_state_changed(COMBAT). | ADR-0010, ADR-0011 | COUVERT | — |
| TR-gestionnaire-etat-001 | design/gdd/gestionnaire-etat.md | gestionnaire-etat | S11 est l'autorite d'etat ; emet game_state_changed. | ADR-0011 | COUVERT | — |
| TR-gestionnaire-etat-002 | design/gdd/gestionnaire-etat.md | gestionnaire-etat | Transitions FSM pilotees par signaux S03/S07. | ADR-0011 | COUVERT | — |
| TR-gestionnaire-etat-003 | design/gdd/gestionnaire-etat.md | gestionnaire-etat | GAME_OVER declenche S10.freeze + retry en <=3s via S12. | ADR-0011, ADR-0012 | COUVERT | — |
| TR-gestionnaire-etat-004 | design/gdd/gestionnaire-etat.md | gestionnaire-etat | S11 ne contient pas de logique gameplay. | ADR-0011 | COUVERT | — |
| TR-retry-reinitialisation-001 | design/gdd/retry-reinitialisation.md | retry-reinitialisation | S12 retry() appelle reload_current_scene(). | ADR-0012 | COUVERT | — |
| TR-retry-reinitialisation-002 | design/gdd/retry-reinitialisation.md | retry-reinitialisation | Declenche uniquement par S11 en GAME_OVER. | ADR-0011, ADR-0012 | COUVERT | — |
| TR-retry-reinitialisation-003 | design/gdd/retry-reinitialisation.md | retry-reinitialisation | Temps total retry <= 3s ; pas de fade en MVP. | ADR-0012 | COUVERT | — |
| TR-hud-001 | design/gdd/hud.md | hud | HUD = CanvasLayer, read-only (minimal outbound). | ADR-0013 | COUVERT | — |
| TR-hud-002 | design/gdd/hud.md | hud | Consomme signaux S07/S03/GrabSystem pour HP/vagues/silhouette. | ADR-0013 | COUVERT | — |
| TR-hud-003 | design/gdd/hud.md | hud | HP bar : update immediat + regles hit flash 440ms. | ADR-0013 | COUVERT | — |
| TR-hud-004 | design/gdd/hud.md | hud | Emet retry_requested() uniquement en GAME_OVER vers S11. | ADR-0013 | COUVERT | — |

---

## Trous connus
 
Aucun — tous les TR-ID actifs sont couverts par des ADR `Accepted`.

---

## Conflits inter-ADR

| Conflict ID | ADR A | ADR B | Type | Statut |
|-------------|-------|-------|------|--------|
| CONFLICT-001 | ADR-0001 | ADR-0002 | Ordre de dependances | RESOLU |

---

## ADR -> GDD (index inverse)

| ADR | Titre | Exigences GDD couvertes | Risque moteur |
|-----|-------|--------------------------|--------------|
| ADR-0001 | GrabSystem Architecture | TR-saisie-lancer-001, TR-saisie-lancer-002, TR-saisie-lancer-003, TR-saisie-lancer-004 | ELEVÉ |
| ADR-0002 | Player Body Type and Collision Layers | TR-deplacement-joueur-001, TR-deplacement-joueur-002 | ELEVÉ |
| ADR-0003 | DamageCalculator - Patron static func | TR-systeme-degats-001, TR-systeme-degats-002, TR-systeme-degats-003, TR-systeme-degats-004 | ELEVÉ |
| ADR-0004 | Catalogue d'objets (S05) - Modele Resource + @export | TR-catalogue-objets-001, TR-catalogue-objets-002, TR-catalogue-objets-003, TR-catalogue-objets-004 | ELEVÉ |
| ADR-0005 | Conventions DI + signaux (GDScript) | Fondation (pas de TR direct) | ELEVÉ |
| ADR-0006 | S01 Jump + Gravity (coyote time, ordre d'application) | TR-deplacement-joueur-003, TR-deplacement-joueur-004 | ELEVÉ |
| ADR-0007 | S10 Camera TPS (pivot + SpringArm + yaw signal + freeze) | TR-camera-tps-001, TR-camera-tps-002, TR-camera-tps-003, TR-camera-tps-004 | ELEVÉ |
| ADR-0008 | S07/S08 Health contracts (receive_damage + signaux) | TR-sante-joueur-001, TR-sante-joueur-002, TR-sante-joueur-003, TR-sante-ennemie-001, TR-sante-ennemie-002, TR-sante-ennemie-003 | ELEVÉ |
| ADR-0009 | S09 Enemy scene contract (composition + DI + signaux) | TR-ia-ennemie-001, TR-ia-ennemie-002, TR-ia-ennemie-003, TR-ia-ennemie-004 | ELEVÉ |
| ADR-0010 | S03 WaveManager (spawn + contracts enemy_died + signaux S11) | TR-vagues-ennemis-001, TR-vagues-ennemis-002, TR-vagues-ennemis-003, TR-vagues-ennemis-004, TR-systems-index-001 | ELEVÉ |
| ADR-0011 | S11 GameState FSM (autorité + orchestration freeze/retry) | TR-gestionnaire-etat-001, TR-gestionnaire-etat-002, TR-gestionnaire-etat-003, TR-gestionnaire-etat-004, TR-systems-index-001 | ELEVÉ |
| ADR-0012 | S12 Retry (SceneTree.reload_current_scene) | TR-retry-reinitialisation-001, TR-retry-reinitialisation-002, TR-retry-reinitialisation-003 | ELEVÉ |
| ADR-0013 | S13 HUD (CanvasLayer read-only + retry_requested) | TR-hud-001, TR-hud-002, TR-hud-003, TR-hud-004 | ELEVÉ |
| ADR-0014 | Concept constraints (single room sessions, no persistence) | TR-concept-001, TR-concept-002 | FAIBLE |
