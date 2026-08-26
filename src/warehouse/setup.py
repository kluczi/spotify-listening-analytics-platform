DATABASE = "SPOTIFY_ANALYTICS"
SCHEMA = "RAW"


def setup_warehouse(conn) -> None:
    with conn.cursor() as cursor:
        """setup db and schema"""
        cursor.execute(f"create database if not exists {DATABASE}")
        cursor.execute(f"use database {DATABASE}")
        cursor.execute(f"create schema if not exists {DATABASE}.{SCHEMA}")

        """setup raw tables"""
        cursor.execute(f"""
            create table if not exists {DATABASE}.{SCHEMA}.recently_played_tracks (
                fetched_at timestamp_tz,
                payload variant
            )
        """)

        cursor.execute(f"""
            create table if not exists {DATABASE}.{SCHEMA}.tracks (
                fetched_at timestamp_tz,
                payload variant
            )
        """)

        cursor.execute(f"""
            create table if not exists {DATABASE}.{SCHEMA}.saved_tracks (
                fetched_at timestamp_tz,
                payload variant
            )
        """)

        cursor.execute(f"""
            create table if not exists {DATABASE}.{SCHEMA}.top_tracks (
                fetched_at timestamp_tz,
                payload variant
            )
        """)

        cursor.execute(f"""
            create table if not exists {DATABASE}.{SCHEMA}.top_artists (
                fetched_at timestamp_tz,
                payload variant
            )
        """)

        cursor.execute(f"""
            create table if not exists {DATABASE}.{SCHEMA}.followed_artists (
                fetched_at timestamp_tz,
                payload variant
            )
        """)

        cursor.execute(f"""
            create table if not exists {DATABASE}.{SCHEMA}.albums (
                fetched_at timestamp_tz,
                payload variant
            )
        """)
