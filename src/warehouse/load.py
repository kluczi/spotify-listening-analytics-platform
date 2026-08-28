import json
from datetime import timezone, datetime
from collections.abc import Iterator


DATABASE = "SPOTIFY_ANALYTICS"
SCHEMA = "RAW"


def load_batch(conn, table: str, items: list[dict]) -> None:
    fetched_at = datetime.now(timezone.utc)
    rows = [(fetched_at, json.dumps(item)) for item in items]
    with conn.cursor() as cursor:
        cursor.executemany(
            f"""
                    insert into {DATABASE}.{SCHEMA}.{table} (
                        fetched_at,
                        payload
                    )
                    select
                        column1,
                        parse_json(column2)
                    from values (%s, %s)
                    """,
            rows,
        )


def load_batches(conn, table: str, batches: Iterator[list[dict]]) -> None:
    for batch in batches:
        load_batch(conn, table, batch)
