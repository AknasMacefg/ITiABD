from __future__ import annotations

import sqlite3

import pandas as pd


def create_database(
    connection: sqlite3.Connection,
    organizations: pd.DataFrame,
    transactions: pd.DataFrame,
    cities: pd.DataFrame,
) -> None:
    organizations.to_sql("organizations", connection, index=False, if_exists="replace")
    transactions.to_sql("transactions", connection, index=False, if_exists="replace")
    cities.to_sql("cities", connection, index=False, if_exists="replace")


def run_joins(connection: sqlite3.Connection) -> dict[str, pd.DataFrame]:
    queries = {
        "inner_org_tx": """
            SELECT o.org_id, o.org_name, t.transaction_id, t.date, t.amount, t.currency
            FROM organizations AS o
            INNER JOIN transactions AS t ON o.org_id = t.org_id
            ORDER BY o.org_id, t.transaction_id
        """,
        "left_org_tx": """
            SELECT o.org_id, o.org_name, o.city_id, t.transaction_id, t.date, t.amount, t.currency
            FROM organizations AS o
            LEFT JOIN transactions AS t ON o.org_id = t.org_id
            ORDER BY o.org_id, t.transaction_id
        """,
        "left_with_cities": """
            SELECT o.org_id, o.org_name, o.city_id, c.city_name, c.region_name,
                   t.transaction_id, t.amount
            FROM organizations AS o
            LEFT JOIN transactions AS t ON o.org_id = t.org_id
            LEFT JOIN cities AS c ON o.city_id = c.city_id
            ORDER BY o.org_id, t.transaction_id
        """,
    }
    return {name: pd.read_sql_query(query, connection) for name, query in queries.items()}


def aggregate_transactions(connection: sqlite3.Connection) -> pd.DataFrame:
    query = """
        SELECT o.org_id,
               o.org_name,
               COUNT(t.transaction_id) AS transaction_count,
               COALESCE(SUM(t.amount), 0) AS amount_sum,
               AVG(t.amount) AS amount_avg
        FROM organizations AS o
        LEFT JOIN transactions AS t ON o.org_id = t.org_id
        GROUP BY o.org_id, o.org_name
        ORDER BY o.org_id
    """
    return pd.read_sql_query(query, connection)
