"""Independent Scrapy spider for the organization catalog."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any

import scrapy


class CatalogSpider(scrapy.Spider):
    name = "catalog"
    allowed_domains = ["127.0.0.1"]
    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.25,
        "AUTOTHROTTLE_ENABLED": True,
        "FEEDS": {
            "data/raw/catalog_scrapy.jsonl": {
                "format": "jsonlines",
                "overwrite": True,
            },
        },
        "LOG_LEVEL": "INFO",
    }
    iso_date = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def __init__(self, start_url: str | None = None, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []
        self.seen_ids: set[str] = set()
        self.issues: list[dict[str, str]] = []

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def record_issue(self, response: scrapy.http.Response | None, error_type: str, message: str) -> None:
        self.issues.append(
            {
                "url": response.url if response else "",
                "error_type": error_type,
                "status_code": str(response.status) if response else "",
                "message": message,
                "timestamp": self.now_iso(),
            }
        )

    def parse(self, response: scrapy.http.Response, **kwargs: Any):
        if response.status >= 400:
            self.record_issue(response, "http_error", f"HTTP status {response.status}")
            return
        for card in response.css("article.org-card"):
            org_id = (card.attrib.get("data-org-id") or "").strip()
            profile_url = card.css("a.profile-link::attr(href)").get()
            name = card.css(".org-name::text").get()
            sector = card.css(".sector::text").get()
            if not all((org_id, profile_url, name, sector)):
                self.record_issue(response, "invalid_card", "Card is missing a required field")
                continue
            if org_id in self.seen_ids:
                self.record_issue(response, "duplicate_card", f"Repeated org_id={org_id}")
                continue
            self.seen_ids.add(org_id)
            yield response.follow(
                profile_url,
                callback=self.parse_detail,
                errback=self.errback,
                cb_kwargs={
                    "org_id": org_id,
                    "org_name": name.strip(),
                    "sector": sector.strip(),
                },
            )
        next_url = response.css("a.next[href]::attr(href), a[rel='next']::attr(href), a.next-page[href]::attr(href)").get()
        if next_url:
            yield response.follow(next_url, callback=self.parse, errback=self.errback)

    def parse_detail(self, response: scrapy.http.Response, **kwargs: str):
        reports = response.css(".reports-count::text").get()
        reviewed = response.css(".last-reviewed::text").get()
        description = response.css(".description::text").get()
        for value, name in ((reports, "reports_count"), (reviewed, "last_reviewed"), (description, "description")):
            if not value or not value.strip():
                self.record_issue(response, "missing_field", f"Missing detail field: {name}")
        normalized_reviewed = reviewed.strip() if reviewed else ""
        if normalized_reviewed and not self.iso_date.fullmatch(normalized_reviewed):
            self.record_issue(response, "invalid_date", f"Expected ISO date, got {normalized_reviewed!r}")
            normalized_reviewed = ""
        normalized_reports = reports.strip() if reports else ""
        if normalized_reports and not normalized_reports.isdigit():
            self.record_issue(response, "invalid_reports_count", f"Expected non-negative integer, got {normalized_reports!r}")
            normalized_reports = ""
        yield {
            **kwargs,
            "reports_count": int(normalized_reports) if normalized_reports else None,
            "last_reviewed": normalized_reviewed or None,
            "description": description.strip() if description else "",
            "source_url": response.url,
            "scraped_at": self.now_iso(),
        }

    def errback(self, failure: Any):
        response = failure.value.response
        if response is not None:
            self.record_issue(response, "http_error", f"HTTP status {response.status}")
        else:
            self.record_issue(None, "network_error", str(failure.value))

    def closed(self, reason: str) -> None:
        path = Path("results/scraping_errors.csv")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as stream:
            fields = ["url", "error_type", "status_code", "message", "timestamp"]
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self.issues)


if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute(["scrapy", "runspider", __file__])
