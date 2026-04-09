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
        entry = {"num": i['number'], "title": i['title']}
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

def issue_bar(index, total, length=10):
    filled = int(((index+1)/total)*length)
    empty = length - filled
    return "🟩"*filled + "⬜"*empty

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

# Fonction pour créer tableau d'issues avec mini-barres emojis
def issues_table(title, issues_list):
    if not issues_list:
        return f"**{title}**\n- Aucune"
    table = f"**{title}**\n\n"
    total_issues = len(issues_list)
    for idx, issue in enumerate(issues_list):
        bar = issue_bar(idx, total_issues)
        table += f"{bar} #{issue['num']} {issue['title']}\n"
    return table

issues_open_table = issues_table("🕒 Issues ouvertes", open_issues)
issues_closed_table = issues_table("✅ Issues fermées", closed_issues)

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
