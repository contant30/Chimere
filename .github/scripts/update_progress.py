#!/usr/bin/env python3
"""
Met à jour la section avancement du README en lisant systems-index.md.
Usage : python update_progress.py
"""

import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent.parent
SYSTEMS_INDEX = ROOT / "design" / "gdd" / "systems-index.md"
README = ROOT / "README.md"

MARKER_START = "<!-- AVANCEMENT_START -->"
MARKER_END = "<!-- AVANCEMENT_END -->"

STATUS_EMOJI = {
    "Complet":        "✅",
    "In Review":      "🔍",
    "En cours":       "🔧",
    "Non commencé":   "⬜",
}

PRIORITY_LABEL = {
    "MVP":  "MVP",
    "V1.0": "V1.0",
}


def parse_systems(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    systems = []
    in_table = False
    for line in text.splitlines():
        if re.match(r"\|\s*#\s*\|", line):
            in_table = True
            continue
        if in_table and re.match(r"\|[-\s|]+\|", line):
            continue
        if in_table and line.startswith("|"):
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) >= 6:
                systems.append({
                    "id":       cols[0],
                    "nom":      cols[1],
                    "categorie":cols[2],
                    "priorite": cols[3],
                    "statut":   cols[4],
                    "gdd":      cols[5],
                })
        elif in_table:
            break
    return systems


def build_section(systems: list[dict]) -> str:
    total = len(systems)
    done  = sum(1 for s in systems if s["statut"] == "Complet")
    review = sum(1 for s in systems if s["statut"] == "In Review")
    wip   = sum(1 for s in systems if s["statut"] == "En cours")
    todo  = total - done - review - wip

    pct = int(done / total * 100) if total else 0
    bar_filled = pct // 5
    bar = "█" * bar_filled + "░" * (20 - bar_filled)

    mvp_systems   = [s for s in systems if s["priorite"] == "MVP"]
    v1_systems    = [s for s in systems if s["priorite"] == "V1.0"]

    def rows(lst):
        lines = []
        for s in lst:
            emoji = STATUS_EMOJI.get(s["statut"], "❓")
            gdd = "—" if s["gdd"] == "—" else "📄"
            lines.append(f"| {s['id']} | {s['nom']} | {emoji} {s['statut']} | {gdd} |")
        return "\n".join(lines)

    today = date.today().strftime("%Y-%m-%d")

    section = f"""{MARKER_START}
## État d'avancement

> Mis à jour automatiquement au dernier commit — {today}

**Progression globale : {done}/{total} systèmes complets ({pct}%)**

`{bar}` {pct}%

| Statut | Nombre |
|--------|--------|
| ✅ Complet | {done} |
| 🔍 En review | {review} |
| 🔧 En cours | {wip} |
| ⬜ Non commencé | {todo} |

### Systèmes MVP ({len(mvp_systems)} systèmes)

| # | Système | Statut | GDD |
|---|---------|--------|-----|
{rows(mvp_systems)}

### Post-MVP / V1.0 ({len(v1_systems)} systèmes)

| # | Système | Statut | GDD |
|---|---------|--------|-----|
{rows(v1_systems)}

{MARKER_END}"""
    return section


def update_readme(readme_path: Path, new_section: str):
    content = readme_path.read_text(encoding="utf-8")

    if MARKER_START in content and MARKER_END in content:
        pattern = re.compile(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            re.DOTALL
        )
        updated = pattern.sub(new_section, content)
    else:
        # Insère après la première ligne de titre
        updated = re.sub(
            r"(# .+?\n)",
            r"\1\n" + new_section + "\n",
            content,
            count=1
        )

    readme_path.write_text(updated, encoding="utf-8")
    print(f"README mis à jour — {date.today()}")


if __name__ == "__main__":
    systems = parse_systems(SYSTEMS_INDEX)
    section = build_section(systems)
    update_readme(README, section)
