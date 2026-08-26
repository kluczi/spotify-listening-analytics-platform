from src.ingestion.fetch import (
    fetch_user_followed_artists,
    fetch_user_recently_played_history,
    fetch_user_saved_tracks,
    fetch_user_top_artists,
    fetch_user_top_tracks,
)
from src.warehouse.connection import get_connection
from src.warehouse.setup import setup_warehouse
from src.warehouse.load import load_batches

TABLES = [
    "recently_played_tracks",
    "saved_tracks",
    "top_tracks",
    "top_artists",
    "followed_artists",
]


def main():
    conn = get_connection()
    try:
        setup_warehouse(conn)
        load_batches(
            conn,
            "recently_played_tracks",
            fetch_user_recently_played_history(),
        )

        load_batches(
            conn,
            "saved_tracks",
            fetch_user_saved_tracks(),
        )

        load_batches(
            conn,
            "top_tracks",
            fetch_user_top_tracks(),
        )

        load_batches(
            conn,
            "top_artists",
            fetch_user_top_artists(),
        )

        load_batches(
            conn,
            "followed_artists",
            fetch_user_followed_artists(),
        )

    finally:
        conn.close()


if __name__ == "__main__":
    main()
