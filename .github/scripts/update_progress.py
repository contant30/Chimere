import os
import requests
import subprocess
import re

REPO = "contant30/Chimere"
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

# -------- ISSUES --------
def get_issues():
    url = f"https://api.github.com/repos/{REPO}/issues?state=all&per_page=100"
    data = requests.get(url, headers=HEADERS).json()

    open_issues = []
    closed_issues = []

    for i in data:
        if "pull_request" in i:
            continue
        entry = {
            "num": i["number"],
            "title": i["title"],
            "body": (i.get("body") or ""),
            "state": i["state"],
        }
        if i["state"] == "open":
            open_issues.append(entry)
        else:
            closed_issues.append(entry)

    return open_issues[:5], closed_issues[:5], len(open_issues), len(closed_issues)

# -------- COMMITS --------
def get_commits():
    try:
        raw = subprocess.check_output(
            ["git", "log", "-20", "--pretty=format:%s"]
        ).decode("utf-8")
        return raw.split("\n")[:5]
    except subprocess.CalledProcessError:
        return []

# -------- BARRES --------
def cumulative_bar(closed, open_, length=30):
    total = closed + open_
    if total == 0:
        return "🟦" * length + " 0%"
    closed_blocks = int((closed / total) * length)
    open_blocks = length - closed_blocks
    percent = int((closed / total) * 100)
    return "✅" * closed_blocks + "🕒" * open_blocks + f" {percent}%"


def checklist_fraction(body: str):
    """Part des cases cochées dans les listes de tâches GitHub (- [ ] / - [x], etc.)."""
    if not body:
        return None
    # Lignes du type : - [ ]  * [x]  + [ ]  1. [x]
    pat = re.compile(
        r"^\s*(?:[-*+]|\d+\.)\s+\[([ xX])\]\s",
        re.MULTILINE,
    )
    marks = pat.findall(body)
    if not marks:
        return None
    done = sum(1 for m in marks if m.strip().lower() == "x")
    return done / len(marks)


def progress_bar(fraction: float, length: int = 10) -> str:
    """Barre 🟩/⬜ pour une fraction dans [0, 1]."""
    fraction = max(0.0, min(1.0, fraction))
    filled = int(round(fraction * length))
    if fraction >= 1.0:
        filled = length
    filled = max(0, min(length, filled))
    return "🟩" * filled + "⬜" * (length - filled)


def bar_for_issue(issue: dict, *, is_closed_row: bool) -> str:
    if is_closed_row or issue.get("state") == "closed":
        return progress_bar(1.0)
    frac = checklist_fraction(issue.get("body") or "")
    if frac is None:
        return progress_bar(0.0)
    return progress_bar(frac)

# -------- UPDATE README --------
def replace(content, start, end, new):
    pattern = re.compile(f"{start}.*?{end}", re.DOTALL)
    return pattern.sub(f"{start}\n{new}\n{end}", content)

# -------- MAIN --------
open_issues, closed_issues, open_count, closed_count = get_issues()
commits = get_commits()
total = open_count + closed_count

# Barre cumulative avec emojis
progress = cumulative_bar(closed_count, open_count)

# Stats globales
stats = f"""
| ✅ Fermées | 🕒 Ouvertes | 📊 Total |
|-----------|------------|----------|
| {closed_count} | {open_count} | {total} |
"""

# Fonction pour créer tableau d'issues avec mini-barres (statut réel)
def issues_table(title, issues_list, *, closed_section: bool):
    if not issues_list:
        return f"**{title}**\n- Aucune"
    legend = ""
    if not closed_section:
        legend = (
            "_Barres : part des sous-tâches cochées dans le corps de l’issue "
            "(`- [ ]` / `- [x]`). Sans checklist → 0 %._\n\n"
        )
    table = f"**{title}**\n\n{legend}"
    for issue in issues_list:
        bar = bar_for_issue(issue, is_closed_row=closed_section)
        # Puce Markdown : un saut de ligne par issue au rendu GitHub (sinon le \n seul est absorbé).
        table += f"- {bar} #{issue['num']} {issue['title']}\n"
    return table


issues_open_table = issues_table("🕒 Issues ouvertes", open_issues, closed_section=False)
issues_closed_table = issues_table("✅ Issues fermées", closed_issues, closed_section=True)

# Activité récente
activity = "\n".join([f"⚡ {c}" for c in commits]) if commits else "⚡ Pas d'activité récente"

# Lecture et mise à jour du README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

content = replace(content, "<!-- START_SECTION:progress -->", "<!-- END_SECTION:progress -->", progress)
content = replace(content, "<!-- START_SECTION:stats -->", "<!-- END_SECTION:stats -->", stats)
content = replace(content, "<!-- START_SECTION:issues -->", "<!-- END_SECTION:issues -->", issues_open_table)
content = replace(content, "<!-- START_SECTION:closed_issues -->", "<!-- END_SECTION:closed_issues -->", issues_closed_table)
content = replace(content, "<!-- START_SECTION:activity -->", "<!-- END_SECTION:activity -->", activity)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)
