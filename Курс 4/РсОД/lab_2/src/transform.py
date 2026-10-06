from __future__ import annotations

import pandas as pd


def normalize_keys(
    organizations: pd.DataFrame,
    transactions: pd.DataFrame,
    cities: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    organizations = organizations.copy()
    transactions = transactions.copy()
    cities = cities.copy()
    for frame, columns in (
        (organizations, ["org_id", "city_id"]),
        (transactions, ["org_id"]),
        (cities, ["city_id"]),
    ):
        for column in columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").astype("Int64")
    return organizations, transactions, cities


def key_diagnostics(left: pd.DataFrame, left_key: str, right: pd.DataFrame, right_key: str) -> dict:
    left_values = set(left[left_key].dropna())
    right_values = set(right[right_key].dropna())
    return {
        "null_left": int(left[left_key].isna().sum()),
        "null_right": int(right[right_key].isna().sum()),
        "duplicate_keys_left": left[left[left_key].duplicated(keep=False)].copy(),
        "duplicate_keys_right": right[right[right_key].duplicated(keep=False)].copy(),
        "left_only": sorted(left_values - right_values),
        "right_only": sorted(right_values - left_values),
    }


def join_sources(
    organizations: pd.DataFrame,
    transactions: pd.DataFrame,
    cities: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    inner_org_tx = organizations.merge(
        transactions,
        on="org_id",
        how="inner",
        indicator=True,
        validate="one_to_many",
        suffixes=("_org", "_tx"),
    )
    left_org_tx = organizations.merge(
        transactions,
        on="org_id",
        how="left",
        indicator=True,
        validate="one_to_many",
        suffixes=("_org", "_tx"),
    )
    with_cities = left_org_tx.merge(
        cities,
        on="city_id",
        how="left",
        indicator="city_merge",
        validate="many_to_one",
        suffixes=("", "_city"),
    )
    return {
        "inner_org_tx": inner_org_tx,
        "left_org_tx": left_org_tx,
        "with_cities": with_cities,
    }


def build_data_mart(
    organizations: pd.DataFrame,
    transactions: pd.DataFrame,
    cities: pd.DataFrame,
) -> pd.DataFrame:
    joined = join_sources(organizations, transactions, cities)["with_cities"]
    data_mart = (
        joined.groupby(
            ["org_id", "org_name", "sector", "city_name", "region_name"],
            dropna=False,
            as_index=False,
        )
        .agg(
            transactions_count=("transaction_id", "count"),
            total_amount=("amount", "sum"),
            avg_amount=("amount", "mean"),
            last_transaction_date=("date", "max"),
        )
        .sort_values("org_id")
    )
    data_mart["total_amount"] = data_mart["total_amount"].fillna(0.0)
    data_mart["transactions_count"] = data_mart["transactions_count"].astype("int64")
    return data_mart[
        [
            "org_id",
            "org_name",
            "sector",
            "city_name",
            "region_name",
            "transactions_count",
            "total_amount",
            "avg_amount",
            "last_transaction_date",
        ]
    ]
