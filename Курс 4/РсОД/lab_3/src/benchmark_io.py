"""Measure sequential and threaded local HTML downloads."""

from __future__ import annotations

import argparse
import csv
import hashlib
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin

import requests


def profile_urls(base_url: str, repeat: int) -> list[str]:
    return [urljoin(base_url, f"organizations/{org_id}.html")
            for _ in range(repeat) for org_id in range(1, 11)]


def fetch_one(url: str, timeout: float) -> tuple[str, bool, str]:
    with requests.Session() as session:
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return url, True, hashlib.sha256(response.content).hexdigest()
        except requests.RequestException:
            return url, False, ""


def sequential(urls: list[str], timeout: float):
    with requests.Session() as session:
        results = []
        for url in urls:
            try:
                response = session.get(url, timeout=timeout)
                response.raise_for_status()
                results.append((url, True, hashlib.sha256(response.content).hexdigest()))
            except requests.RequestException:
                results.append((url, False, ""))
        return results


def threaded(urls: list[str], workers: int, timeout: float):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(lambda url: fetch_one(url, timeout), urls))


def measure(name: str, runner, urls: list[str], runs: int):
    measurements = []
    for run in range(1, runs + 1):
        started = time.perf_counter()
        fetched = runner(urls, 10)
        measurements.append({
            "mode": name, "run": run, "url_count": len(urls),
            "successful": sum(ok for _, ok, _ in fetched),
            "errors": sum(not ok for _, ok, _ in fetched),
            "elapsed_seconds": round(time.perf_counter() - started, 6),
            "content_signature": hashlib.sha256(
                "".join(f"{url}:{digest}" for url, ok, digest in sorted(fetched) if ok).encode()
            ).hexdigest(),
        })
    return measurements


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8765/")
    parser.add_argument("--repeat", type=int, default=2)
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()
    urls = profile_urls(args.base_url, args.repeat)
    measurements = measure("sequential", sequential, urls, args.runs)
    measurements += measure("threads_2", lambda u, t: threaded(u, 2, t), urls, args.runs)
    measurements += measure("threads_4", lambda u, t: threaded(u, 4, t), urls, args.runs)
    medians = {mode: statistics.median(r["elapsed_seconds"] for r in measurements if r["mode"] == mode)
               for mode in ("sequential", "threads_2", "threads_4")}
    first_signature = measurements[0]["content_signature"]
    summary = [{"mode": mode, "runs": args.runs, "url_count": len(urls),
                "median_seconds": round(medians[mode], 6),
                "speedup_vs_sequential": round(medians["sequential"] / medians[mode], 3),
                "all_runs_same_success_count": len({r["successful"] for r in measurements if r["mode"] == mode}) == 1,
                "same_content_as_first_run": all(r["content_signature"] == first_signature for r in measurements)}
               for mode in ("sequential", "threads_2", "threads_4")]
    Path("results").mkdir(exist_ok=True)
    with Path("results/benchmark.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=measurements[0])
        writer.writeheader()
        writer.writerows(measurements)
    with Path("results/benchmark_summary.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=summary[0])
        writer.writeheader()
        writer.writerows(summary)
    print(*summary, sep="\n")


if __name__ == "__main__":
    main()
