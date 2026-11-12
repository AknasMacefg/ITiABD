"""Generate a small static organization catalog for the web-scraping lab."""

from __future__ import annotations

import argparse
import csv
import html
from pathlib import Path


PAGE_SIZE = 4


def read_organizations(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    required = {"org_id", "org_name", "city_id", "sector"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"{path} must contain columns: {', '.join(sorted(required))}")
    return rows


def profile_details(row: dict[str, str]) -> dict[str, str]:
    org_id = int(row["org_id"])
    return {
        "reports_count": str(org_id % 4),
        "last_reviewed": f"2026-{(org_id % 9) + 1:02d}-{(org_id % 27) + 1:02d}",
        "description": (
            f"{row['org_name']} operates in the {row['sector']} sector "
            f"and is associated with city {row['city_id']}."
        ),
    }


def page_link(page: int) -> str:
    return "index.html" if page == 1 else f"index_{page}.html"


def render_index(rows: list[dict[str, str]], page: int, total_pages: int) -> str:
    start = (page - 1) * PAGE_SIZE
    cards = []
    for row in rows[start : start + PAGE_SIZE]:
        name = html.escape(row["org_name"])
        sector = html.escape(row["sector"])
        org_id = html.escape(row["org_id"])
        cards.append(
            f"""      <article class="org-card" data-org-id="{org_id}">
        <h2 class="org-name">{name}</h2>
        <p class="sector">{sector}</p>
        <a class="profile-link" href="organizations/{org_id}.html">Open profile</a>
      </article>"""
        )
    navigation = []
    if page > 1:
        navigation.append(f'<a class="prev-page" href="{page_link(page - 1)}">Previous</a>')
    if page < total_pages:
        navigation.append(f'<a class="next-page" href="{page_link(page + 1)}">Next</a>')
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Organization catalog</title></head>
<body>
  <main class="catalog" data-page="{page}">
    <h1>Organization catalog</h1>
    <section class="org-list">
{chr(10).join(cards)}
    </section>
    <nav class="pagination">{" ".join(navigation)}</nav>
  </main>
</body>
</html>
"""


def render_profile(row: dict[str, str]) -> str:
    details = profile_details(row)
    values = {key: html.escape(value) for key, value in {**row, **details}.items()}
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{values["org_name"]}</title></head>
<body>
  <main class="org-profile" data-org-id="{values["org_id"]}">
    <h1 class="org-name">{values["org_name"]}</h1>
    <dl class="org-details">
      <dt>Sector</dt><dd class="sector">{values["sector"]}</dd>
      <dt>Reports</dt><dd class="reports-count">{values["reports_count"]}</dd>
      <dt>Last reviewed</dt><dd class="last-reviewed">{values["last_reviewed"]}</dd>
      <dt>Description</dt><dd class="description">{values["description"]}</dd>
    </dl>
  </main>
</body>
</html>
"""


def build_catalog(input_path: Path, output_dir: Path) -> None:
    rows = read_organizations(input_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    profiles_dir = output_dir / "organizations"
    profiles_dir.mkdir(exist_ok=True)
    total_pages = (len(rows) + PAGE_SIZE - 1) // PAGE_SIZE
    for page in range(1, total_pages + 1):
        (output_dir / page_link(page)).write_text(
            render_index(rows, page, total_pages), encoding="utf-8"
        )
    for row in rows:
        (profiles_dir / f"{row['org_id']}.html").write_text(
            render_profile(row), encoding="utf-8"
        )
    (output_dir / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /private/\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    build_catalog(args.input, args.out)


if __name__ == "__main__":
    main()
