"""BeautifulSoup scraper for the local organization catalog."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


FIELDS = ["org_id", "org_name", "sector", "reports_count", "last_reviewed",
          "description", "source_url", "scraped_at"]
ERROR_FIELDS = ["url", "error_type", "status_code", "message", "timestamp"]
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_issue(issues: list[dict[str, str]], url: str, error_type: str,
              message: str, status_code: int | None = None) -> None:
    issues.append({"url": url, "error_type": error_type,
                   "status_code": "" if status_code is None else str(status_code),
                   "message": message, "timestamp": now_iso()})


def fetch_html(url: str, session: requests.Session,
               issues: list[dict[str, str]], timeout: float = 10) -> str | None:
    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.HTTPError as error:
        response = error.response
        log_issue(issues, url, "http_error", str(error),
                  response.status_code if response is not None else None)
        return None
    except requests.RequestException as error:
        log_issue(issues, url, "network_error", str(error))
        return None
    if "html" not in response.headers.get("Content-Type", "").lower():
        log_issue(issues, url, "unexpected_content_type",
                  response.headers.get("Content-Type", ""))
    return response.text


def parse_list_page(html: str, base_url: str) -> tuple[list[dict[str, str]], str | None]:
    soup = BeautifulSoup(html, "lxml")
    cards = []
    for card in soup.select("article.org-card"):
        link = card.select_one("a.profile-link[href]")
        name = card.select_one(".org-name")
        sector = card.select_one(".sector")
        org_id = (card.get("data-org-id") or "").strip()
        if not (org_id and link and name and sector):
            continue
        cards.append({"org_id": org_id, "org_name": name.get_text(" ", strip=True),
                      "sector": sector.get_text(" ", strip=True),
                      "source_url": urljoin(base_url, link["href"])})
    next_link = soup.select_one("a.next[href], a[rel='next'][href], a.next-page[href]")
    return cards, urljoin(base_url, next_link["href"]) if next_link else None


def parse_detail_page(html: str, url: str,
                      issues: list[dict[str, str]]) -> dict[str, str | None]:
    soup = BeautifulSoup(html, "lxml")

    def field(selector: str, name: str) -> str | None:
        node = soup.select_one(selector)
        value = node.get_text(" ", strip=True) if node else ""
        if not value:
            log_issue(issues, url, "missing_field", f"Missing detail field: {name}")
            return None
        return value

    reports = field(".reports-count", "reports_count")
    if reports is not None and not reports.isdigit():
        log_issue(issues, url, "invalid_reports_count", repr(reports))
        reports = None
    reviewed = field(".last-reviewed", "last_reviewed")
    if reviewed is not None and not ISO_DATE.fullmatch(reviewed):
        log_issue(issues, url, "invalid_date", repr(reviewed))
        reviewed = None
    return {"reports_count": reports, "last_reviewed": reviewed,
            "description": field(".description", "description") or ""}


def scrape_catalog(start_url: str, timeout: float = 10):
    issues: list[dict[str, str]] = []
    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    visited_urls: set[str] = set()
    with requests.Session() as session:
        session.headers["User-Agent"] = "ITiABD-Lab3-BS/1.0"
        list_url: str | None = start_url
        while list_url and list_url not in visited_urls:
            visited_urls.add(list_url)
            page = fetch_html(list_url, session, issues, timeout)
            if page is None:
                break
            cards, next_url = parse_list_page(page, list_url)
            for card in cards:
                if card["org_id"] in seen_ids:
                    log_issue(issues, card["source_url"], "duplicate_card",
                              f"Repeated org_id={card['org_id']}")
                    continue
                seen_ids.add(card["org_id"])
                detail_html = fetch_html(card["source_url"], session, issues, timeout)
                if detail_html is not None:
                    records.append({**card, **parse_detail_page(
                        detail_html, card["source_url"], issues), "scraped_at": now_iso()})
            list_url = next_url
        if list_url in visited_urls:
            log_issue(issues, list_url, "pagination_cycle", "URL already visited")
    return records, issues, len(visited_urls)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-url", required=True)
    parser.add_argument("--output", type=Path, default=Path("data/raw/catalog_bs.csv"))
    parser.add_argument("--errors", type=Path, default=Path("results/scraping_errors.csv"))
    parser.add_argument("--summary", type=Path, default=Path("results/catalog_bs_summary.json"))
    args = parser.parse_args()
    records, issues, pages = scrape_catalog(args.start_url)
    write_csv(args.output, records, FIELDS)
    write_csv(args.errors, issues, ERROR_FIELDS)
    summary = {"records": len(records), "unique_org_ids": len({r["org_id"] for r in records}),
               "errors": len(issues), "http_errors": sum(i["error_type"] == "http_error" for i in issues),
               "duplicate_cards": sum(i["error_type"] == "duplicate_card" for i in issues),
               "visited_list_pages": pages}
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("BeautifulSoup scraper: %s records, %s issues", len(records), len(issues))


if __name__ == "__main__":
    main()
