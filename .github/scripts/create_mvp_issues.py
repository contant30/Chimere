from __future__ import annotations

import os
import re
import requests

# ---------------- CONFIG ----------------
REPO = "contant30/Chimere"
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

# (id, nom affiché, statut suivi interne, fermer l’issue à la création si "Done")
# Corps = liste de tâches réelles (toutes `- [ ]` à cocher sur GitHub).
SYSTEMS = [
    ("S01", "Déplacement joueur", "In Review", False),
    ("S02", "Saisie et lancer", "To Do", False),
    ("S03", "Vagues d'ennemis", "To Do", False),
    ("S04", "Dégradation environnement", "To Do", False),
    ("S05", "Catalogue objets", "Done", True),
    ("S06", "Dégâts", "Done", True),
    ("S07", "Santé joueur", "To Do", False),
    ("S08", "Santé ennemie", "To Do", False),
    ("S09", "IA ennemie", "To Do", False),
    ("S10", "Caméra TPS", "To Do", False),
    ("S11", "Game state", "To Do", False),
    ("S12", "Retry", "To Do", False),
    ("S13", "HUD", "To Do", False),
]

# Tâches alignées sur `design/gdd/systems-index.md` (dépendances, GDD, impl).
TASKS_BY_ID: dict[str, list[str]] = {
    "S01": [
        "Finaliser ou approuver le GDD `design/gdd/deplacement-joueur.md`",
        "Trancher les OQ restantes du GDD ou les valider au prototype",
        "Rédiger l’ADR kinematic `CharacterBody3D` + `move_and_slide()` si absent",
        "Prototype Godot : mouvement, sol, coyote time, valeurs de tuning du GDD",
        "Valider tous les critères d’acceptation du GDD",
    ],
    "S02": [
        "Compléter et figer le GDD `design/gdd/saisie-lancer.md`",
        "Définir le contrat d’appel au calculateur de dégâts (S06), conversion float→int",
        "Prototype prioritaire : saisir, lancer, collisions, boucle jouable",
        "Brancher les propriétés catalogue (S05) sur les objets saisissables / lancés",
        "Feedback minimal (placeholder) pour lire les impacts",
        "Playtest : boucle saisir → frapper → enchaîner",
    ],
    "S03": [
        "Rédiger le GDD vagues (spawns, difficulté MVP, conditions de fin)",
        "Publier les signaux `wave_started` / `wave_cleared` / `all_waves_complete` (contrat S11)",
        "Implémenter la logique de spawn et la progression de vagues MVP",
        "Intégrer S08 (mort ennemi) et S09 (comportement) dans la boucle de vague",
    ],
    "S04": [
        "Rédiger le GDD dégradation (stades, liens avec S02 et S05)",
        "Implémenter les stades de destruction sur les props concernés",
        "Tester avec lancers (S02) et cohérence des données catalogue (S05)",
    ],
    "S05": [
        "Maintenir le GDD `design/gdd/catalogue-objets.md` comme référence",
        "Aligner resources Godot / données runtime sur le catalogue et `design/registry/entities.yaml`",
        "Vérifier la consommation par S02 (masse, lancer) et S04 (résistance / stades)",
    ],
    "S06": [
        "Geler `design/gdd/systeme-degats.md` (formule, types, min 1, Règle 8 velocity)",
        "Implémenter le calculateur de dégâts (static / stateless) selon le GDD",
        "Couvrir tests (GUT ou équivalent) : formule, edge cases, types de dégâts",
    ],
    "S07": [
        "Rédiger le GDD santé joueur + game over MVP",
        "Brancher la réception des dégâts depuis S06",
        "Implémenter mort joueur, transition vers game over et lien avec S11",
    ],
    "S08": [
        "Rédiger le GDD santé ennemie + mort / désactivation",
        "Brancher S06 sur les ennemis (réception dégâts, mort)",
        "Gérer le cleanup (vagues S03, pooling si prévu)",
    ],
    "S09": [
        "Rédiger le GDD IA MVP (approche, attaque de base, portée)",
        "Implémenter navigation / poursuite ciblant le joueur (S01)",
        "Intégrer avec les spawns et la logique de vagues (S03)",
    ],
    "S10": [
        "Rédiger le GDD caméra TPS (offset, collision, sensibilité)",
        "Implémenter le suivi du personnage (S01) en troisième personne",
        "Gérer clipping / collision caméra minimale pour le MVP",
    ],
    "S11": [
        "Rédiger le GDD FSM (pré-vague, combat, fin-vague, game-over, victoire)",
        "Implémenter l’orchestrateur d’état et l’écoute des signaux S03 et S07",
        "Respecter le contrat de signaux documenté (dépendance circulaire S03↔S11)",
    ],
    "S12": [
        "Spécifier le flux retry MVP (reset < 3 s)",
        "Réinitialiser joueur, ennemis, objets depuis l’état géré par S11",
        "Vérifier absence de fuite sur plusieurs cycles retry",
    ],
    "S13": [
        "Spécifier le HUD (vie, vague, objet tenu) selon dépendances S07, S03, S02",
        "Implémenter l’UI Godot et les bindings runtime",
        "Valider lisibilité en combat (taille, contraste, mise à jour temps réel)",
    ],
}

BASE_URL = f"https://api.github.com/repos/{REPO}/issues"


def parse_checked_tasks(previous_body: str | None) -> dict[str, bool]:
    """Pour chaque libellé de tâche (texte après `- [ ]`), True si la case était cochée."""
    if not previous_body:
        return {}
    out: dict[str, bool] = {}
    for m in re.finditer(
        r"^\s*-\s+\[([ xX])\]\s+(.+?)\s*$",
        previous_body,
        re.MULTILINE,
    ):
        label = m.group(2).strip()
        out[label] = m.group(1).strip().lower() == "x"
    return out


def build_body(
    sys_id: str,
    sys_name: str,
    track_status: str,
    *,
    previous_body: str | None = None,
    preserve_checkboxes: bool = True,
) -> str:
    tasks = TASKS_BY_ID.get(sys_id, [f"Définir les livrables pour {sys_id} — {sys_name}"])
    checked = (
        parse_checked_tasks(previous_body)
        if preserve_checkboxes and previous_body
        else {}
    )
    lines = []
    for t in tasks:
        mark = "x" if checked.get(t) else " "
        lines.append(f"- [{mark}] {t}")
    block = "\n".join(lines)
    return f"""## Suivi interne
Statut cible (config script) : **{track_status}**

## Tâches à réaliser
{block}

---
_Les cases cochées (`- [x]`) alimentent la barre de progression du README._"""


def issue_exists(title):
    params = {"state": "all", "per_page": 100}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    for issue in response.json():
        if issue["title"] == title:
            return issue
    return None


def main() -> None:
    for sys_id, sys_name, track_status, close_after_create in SYSTEMS:
        title = f"{sys_id} {sys_name}"
        body = build_body(sys_id, sys_name, track_status)

        existing = issue_exists(title)
        if existing:
            print(f"⚠️ Issue déjà existante : {title}")
            if close_after_create and existing["state"] == "open":
                close_url = f"{BASE_URL}/{existing['number']}"
                r = requests.patch(close_url, headers=HEADERS, json={"state": "closed"})
                if r.status_code == 200:
                    print(f"🔒 Issue fermée automatiquement : {title}")
                else:
                    print(f"❌ Impossible de fermer : {title}, {r.text}")
            continue

        response = requests.post(BASE_URL, headers=HEADERS, json={"title": title, "body": body})
        if response.status_code == 201:
            print(f"✅ Issue créée : {title}")
            if close_after_create:
                issue_number = response.json()["number"]
                close_url = f"{BASE_URL}/{issue_number}"
                r = requests.patch(close_url, headers=HEADERS, json={"state": "closed"})
                if r.status_code == 200:
                    print(f"🔒 Issue fermée automatiquement : {title}")
                else:
                    print(f"❌ Impossible de fermer : {title}, {r.text}")
        else:
            print(f"❌ Erreur ({response.status_code}) pour {title}: {response.text}")


if __name__ == "__main__":
    main()
