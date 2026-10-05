from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import requests


DEFAULT_API_URL = "http://127.0.0.1:8000/api/transactions"


def load_organizations(data_dir: Path) -> pd.DataFrame:
    return pd.read_csv(data_dir / "organizations.csv")


def load_transactions(api_url: str = DEFAULT_API_URL) -> pd.DataFrame:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    return pd.DataFrame(response.json())


def load_cities(data_dir: Path) -> pd.DataFrame:
    query = "SELECT city_id, city_name, region_name, population FROM cities ORDER BY city_id"
    with sqlite3.connect(data_dir / "regions.db") as connection:
        return pd.read_sql_query(query, connection)


def load_sources(data_dir: Path, api_url: str = DEFAULT_API_URL) -> dict[str, pd.DataFrame]:
    return {
        "organizations": load_organizations(data_dir),
        "transactions": load_transactions(api_url),
        "cities": load_cities(data_dir),
    }
