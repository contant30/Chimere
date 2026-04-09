#!/usr/bin/env python3
"""
Met à jour le corps des issues GitHub dont le titre est exactement « Sxx Nom »
(voir SYSTEMS dans create_mvp_issues.py).

Usage (à la racine du dépôt, avec GITHUB_TOKEN ou token dans l’environnement) :
  python .github/scripts/sync_issue_bodies.py
  python .github/scripts/sync_issue_bodies.py --dry-run
  python .github/scripts/sync_issue_bodies.py --no-preserve-checkboxes

Par défaut, les cases déjà cochées sont conservées si le libellé de la ligne
correspond exactement à une tâche du script.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import create_mvp_issues as mvp  # noqa: E402

# Titre GitHub peut différer légèrement du script (apostrophe typographique, NFC/NFD).
_MVP_TITLE = re.compile(r"^(S\d{2})\b", re.UNICODE)


def meta_for_issue_title(title: str) -> tuple[str, str, str] | None:
    """Retourne (sys_id, sys_name, track_status) si le titre est une issue MVP (S01 … S13)."""
    raw = title or ""
    m = _MVP_TITLE.match(raw.strip())
    if not m:
        return None
    sys_id = m.group(1)
    for sid, sname, track_status, _ in mvp.SYSTEMS:
        if sid == sys_id:
            return (sid, sname, track_status)
    return None


def fetch_all_issues() -> list[dict]:
    out: list[dict] = []
    page = 1
    while True:
        r = mvp.requests.get(
            mvp.BASE_URL,
            headers=mvp.HEADERS,
            params={"state": "all", "per_page": 100, "page": page},
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        out.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronise les corps des issues MVP GitHub.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Affiche les changements sans appeler l’API PATCH.",
    )
    parser.add_argument(
        "--no-preserve-checkboxes",
        action="store_true",
        help="Toutes les cases repassent en [ ] (ignore l’ancien corps).",
    )
    args = parser.parse_args()

    if not mvp.TOKEN:
        print("❌ Définir GITHUB_TOKEN (repo : issues: write).", file=sys.stderr)
        return 1

    issues = fetch_all_issues()
    updated = 0
    skipped = 0
    ignored = 0

    for issue in issues:
        if "pull_request" in issue:
            continue
        title = issue.get("title") or ""
        meta = meta_for_issue_title(title)
        if meta is None:
            ignored += 1
            continue

        sys_id, sys_name, track_status = meta
        num = issue["number"]
        old_body = issue.get("body") or ""
        new_body = mvp.build_body(
            sys_id,
            sys_name,
            track_status,
            previous_body=old_body,
            preserve_checkboxes=not args.no_preserve_checkboxes,
        )

        if old_body == new_body:
            print(f"⏭️  #{num} {title} — déjà à jour")
            skipped += 1
            continue

        print(f"📝 #{num} {sys_id} — mise à jour du corps (titre : {title!r})")
        if args.dry_run:
            updated += 1
            continue

        patch_url = f"{mvp.BASE_URL}/{num}"
        r = mvp.requests.patch(
            patch_url,
            headers=mvp.HEADERS,
            json={"body": new_body},
        )
        if r.status_code == 200:
            updated += 1
            print(f"   ✅ OK")
        else:
            print(f"   ❌ {r.status_code} {r.text}", file=sys.stderr)

    print(
        f"\nTerminé — mises à jour : {updated}, déjà à jour : {skipped}, "
        f"issues hors MVP ignorées : {ignored}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
