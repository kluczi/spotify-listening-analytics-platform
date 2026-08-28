from datetime import datetime, timezone
from pathlib import Path
import subprocess

from airflow.sdk import chain, dag, task

from src.ingestion.fetch import (
    fetch_user_followed_artists,
    fetch_user_recently_played_history,
    fetch_user_saved_tracks,
    fetch_user_top_artists,
    fetch_user_top_tracks,
)
from src.warehouse.connection import get_connection
from src.warehouse.load import load_batches
from src.warehouse.setup import setup_warehouse

PROJECT_DIR = Path("/opt/airflow/project")
DBT_PROJECT_DIR = PROJECT_DIR / "spotify_analytics"


def run_command(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


@dag(
    dag_id="spotify_dag",
    description="Fetch Spotify data and rebuild the dbt analytics models.",
    schedule="0 * * * *",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["spotify", "snowflake", "dbt"],
)
def spotify_dag():
    @task
    def setup_source_tables() -> None:
        conn = get_connection()
        try:
            setup_warehouse(conn)
        finally:
            conn.close()

    @task
    def fetch_recently_played() -> list[list[dict]]:
        return list(fetch_user_recently_played_history())

    @task
    def fetch_saved_tracks() -> list[list[dict]]:
        return list(fetch_user_saved_tracks())

    @task
    def fetch_top_tracks() -> list[list[dict]]:
        return list(fetch_user_top_tracks())

    @task
    def fetch_top_artists() -> list[list[dict]]:
        return list(fetch_user_top_artists())

    @task
    def fetch_followed_artists() -> list[list[dict]]:
        return list(fetch_user_followed_artists())

    def load_source(table: str, batches: list[list[dict]]) -> None:
        conn = get_connection()
        try:
            load_batches(conn, table, batches)
        finally:
            conn.close()

    @task
    def load_recently_played(batches: list[list[dict]]) -> None:
        load_source("recently_played_tracks", batches)

    @task
    def load_saved_tracks(batches: list[list[dict]]) -> None:
        load_source("saved_tracks", batches)

    @task
    def load_top_tracks(batches: list[list[dict]]) -> None:
        load_source("top_tracks", batches)

    @task
    def load_top_artists(batches: list[list[dict]]) -> None:
        load_source("top_artists", batches)

    @task
    def load_followed_artists(batches: list[list[dict]]) -> None:
        load_source("followed_artists", batches)

    @task
    def build_dbt_models() -> None:
        run_command(
            [
                "dbt",
                "run",
                "--project-dir",
                str(DBT_PROJECT_DIR),
                "--profiles-dir",
                str(DBT_PROJECT_DIR),
            ],
            PROJECT_DIR,
        )

    @task
    def test_dbt_models() -> None:
        run_command(
            [
                "dbt",
                "test",
                "--project-dir",
                str(DBT_PROJECT_DIR),
                "--profiles-dir",
                str(DBT_PROJECT_DIR),
            ],
            PROJECT_DIR,
        )

    setup = setup_source_tables()
    recently_played = fetch_recently_played()
    saved_tracks = fetch_saved_tracks()
    top_tracks = fetch_top_tracks()
    top_artists = fetch_top_artists()
    followed_artists = fetch_followed_artists()
    load_recently = load_recently_played(recently_played)
    load_saved = load_saved_tracks(saved_tracks)
    load_top_track = load_top_tracks(top_tracks)
    load_top_artist = load_top_artists(top_artists)
    load_followed = load_followed_artists(followed_artists)
    transformations = build_dbt_models()
    tests = test_dbt_models()

    fetch_tasks = [
        recently_played,
        saved_tracks,
        top_tracks,
        top_artists,
        followed_artists,
    ]
    load_tasks = [
        load_recently,
        load_saved,
        load_top_track,
        load_top_artist,
        load_followed,
    ]

    chain(setup, fetch_tasks)
    chain(load_tasks, transformations, tests)


spotify_dag()
