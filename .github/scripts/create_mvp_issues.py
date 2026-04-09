import os
import requests

# ---------------- CONFIG ----------------
REPO = "contant30/Chimere"
TOKEN = os.getenv("GITHUB_TOKEN")  # Ici on met le PAT via secret
HEADERS = {"Authorization": f"token {TOKEN}"}

# ---------------- MVP SYSTEMS ----------------
systems = [
    ("S01", "Déplacement joueur", "In Review"),
    ("S02", "Saisie et lancer", "To Do"),
    ("S03", "Vagues d'ennemis", "To Do"),
    ("S04", "Dégradation environnement", "To Do"),
    ("S05", "Catalogue objets", "Done"),
    ("S06", "Dégâts", "Done"),
    ("S07", "Santé joueur", "To Do"),
    ("S08", "Santé ennemie", "To Do"),
    ("S09", "IA ennemie", "To Do"),
    ("S10", "Caméra TPS", "To Do"),
    ("S11", "Game state", "To Do"),
    ("S12", "Retry", "To Do"),
    ("S13", "HUD", "To Do"),
]

# ---------------- URL API ----------------
BASE_URL = f"https://api.github.com/repos/{REPO}/issues"

# ---------------- UTILS ----------------
def issue_exists(title):
    """Vérifie si une issue avec ce titre existe déjà."""
    params = {"state": "all", "per_page": 100}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    for issue in response.json():
        if issue["title"] == title:
            return issue
    return None

# ---------------- CREATE / CLOSE ISSUES ----------------
for sys_id, sys_name, status in systems:
    title = f"{sys_id} {sys_name}"
    body = f"Statut initial : {status}"

    existing = issue_exists(title)
    if existing:
        print(f"⚠️ Issue déjà existante : {title}")
        # Fermer si elle est "Done" et ouverte
        if status.lower() == "done" and existing["state"] == "open":
            close_url = f"{BASE_URL}/{existing['number']}"
            r = requests.patch(close_url, headers=HEADERS, json={"state": "closed"})
            if r.status_code == 200:
                print(f"🔒 Issue fermée automatiquement : {title}")
            else:
                print(f"❌ Impossible de fermer : {title}, {r.text}")
        continue

    # Créer la nouvelle issue
    response = requests.post(BASE_URL, headers=HEADERS, json={"title": title, "body": body})
    if response.status_code == 201:
        print(f"✅ Issue créée : {title}")
        # Fermer si "Done"
        if status.lower() == "done":
            issue_number = response.json()["number"]
            close_url = f"{BASE_URL}/{issue_number}"
            r = requests.patch(close_url, headers=HEADERS, json={"state": "closed"})
            if r.status_code == 200:
                print(f"🔒 Issue fermée automatiquement : {title}")
            else:
                print(f"❌ Impossible de fermer : {title}, {r.text}")
    else:
        print(f"❌ Erreur ({response.status_code}) pour {title}: {response.text}")
