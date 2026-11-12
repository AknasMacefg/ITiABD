"""Benchmark CPU-bound text analysis sequentially and in two process pools."""

from __future__ import annotations

import argparse
import csv
import re
import statistics
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool
from pathlib import Path
from typing import Any


WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def analyze_text(text: str) -> dict[str, Any]:
    """Normalize text and count words and adjacent word bigrams."""
    normalized = text.casefold()
    words = WORD_RE.findall(normalized)
    word_counts = Counter(words)
    bigram_counts = Counter(zip(words, words[1:]))
    return {
        "word_count": len(words),
        "unique_words": len(word_counts),
        "word_frequencies": dict(sorted(word_counts.items())),
        "bigram_frequencies": {
            f"{left} {right}": count
            for (left, right), count in sorted(bigram_counts.items())
        },
    }


def load_fragments(path: Path, minimum: int = 200) -> list[str]:
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    descriptions = [row["description"] for row in rows if row.get("description")]
    if not descriptions:
        raise ValueError(f"No descriptions found in {path}")
    return [descriptions[index % len(descriptions)] * 80 for index in range(minimum)]


def sequential(texts: list[str]) -> list[dict[str, Any]]:
    return [analyze_text(text) for text in texts]


def multiprocessing_pool(texts: list[str]) -> list[dict[str, Any]]:
    with Pool(processes=2) as pool:
        return pool.map(analyze_text, texts)


def process_executor(texts: list[str]) -> list[dict[str, Any]]:
    with ProcessPoolExecutor(max_workers=2) as executor:
        return list(executor.map(analyze_text, texts))


def measure(
    name: str,
    runner,
    texts: list[str],
    runs: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    timings: list[dict[str, Any]] = []
    baseline: list[dict[str, Any]] | None = None
    for run in range(1, runs + 1):
        started = time.perf_counter()
        result = runner(texts)
        elapsed = time.perf_counter() - started
        if baseline is None:
            baseline = result
        if result != baseline:
            raise AssertionError(f"{name} produced a result different from its first run")
        timings.append(
            {
                "mode": name,
                "run": run,
                "fragment_count": len(texts),
                "elapsed_seconds": round(elapsed, 6),
                "result_signature": str(result),
            }
        )
    return timings, baseline or []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/processed/catalog_clean.csv"))
    parser.add_argument("--fragments", type=int, default=200)
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()
    texts = load_fragments(args.input, args.fragments)
    timings: list[dict[str, Any]] = []
    results: dict[str, list[dict[str, Any]]] = {}
    for name, runner in (
        ("sequential", sequential),
        ("multiprocessing_pool_2", multiprocessing_pool),
        ("process_executor_2", process_executor),
    ):
        measured, result = measure(name, runner, texts, args.runs)
        timings.extend(measured)
        results[name] = result
    if not (results["sequential"] == results["multiprocessing_pool_2"] == results["process_executor_2"]):
        raise AssertionError("CPU modes returned different analysis results")
    medians = {
        mode: statistics.median(
            row["elapsed_seconds"] for row in timings if row["mode"] == mode
        )
        for mode in results
    }
    summary = [
        {
            "mode": mode,
            "runs": args.runs,
            "fragment_count": len(texts),
            "median_seconds": round(medians[mode], 6),
            "speedup_vs_sequential": round(medians["sequential"] / medians[mode], 3),
            "results_match": True,
        }
        for mode in results
    ]
    output = Path("results/cpu_benchmark.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(timings[0]))
        writer.writeheader()
        writer.writerows(timings)
    summary_output = Path("results/cpu_benchmark_summary.csv")
    with summary_output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    print(*summary, sep="\n")


if __name__ == "__main__":
    main()
