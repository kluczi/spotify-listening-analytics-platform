from collections.abc import Iterator
from datetime import datetime, timedelta, timezone

from spotify.endpoints import (
    get_user_followed_artists,
    get_user_recently_played,
    get_user_saved_tracks,
    get_user_top_artists,
    get_user_top_tracks,
)


def fetch_user_recently_played_history(days: int = 14) -> Iterator[list[dict]]:
    limit = 50
    before = None
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    while True:
        data = get_user_recently_played(limit=limit, before=before)
        items = data["items"]

        if not items:
            break

        """Take only last x days history"""
        filtered_items = [
            item
            for item in items
            if datetime.fromisoformat(item["played_at"].replace("Z", "+00:00"))
            >= cutoff
        ]

        if filtered_items:
            yield filtered_items

        oldest_played_at = datetime.fromisoformat(
            items[-1]["played_at"].replace("Z", "+00:00")
        )

        if oldest_played_at < cutoff:
            return

        if data["next"] is None:
            return

        before = int(data["cursors"]["before"])


def fetch_user_followed_artists() -> Iterator[list[dict]]:
    after = None
    limit = 50

    while True:
        data = get_user_followed_artists(limit=limit, after=after)

        artists_page = data["artists"]
        items = artists_page["items"]

        if not items:
            break

        yield items

        after = artists_page["cursors"].get("after")
        if after is None:
            return


def fetch_user_saved_tracks() -> Iterator[list[dict]]:
    limit = 50
    offset = 0

    while True:
        data = get_user_saved_tracks(limit=limit, offset=offset)

        items = data["items"]

        if not items:
            break

        yield items

        if offset + limit >= data["total"]:
            break

        offset += limit


def fetch_user_top_artists() -> Iterator[list[dict]]:
    limit = 50
    offset = 0

    while True:
        data = get_user_top_artists(limit=limit, offset=offset)
        items = data["items"]

        if not items:
            break

        yield items

        if offset + limit >= data["total"]:
            break

        offset += limit


def fetch_user_top_tracks() -> Iterator[list[dict]]:
    limit = 50
    offset = 0

    while True:
        data = get_user_top_tracks(limit=limit, offset=offset)
        items = data["items"]

        if not items:
            break

        yield items

        if offset + limit >= data["total"]:
            break

        offset += limit
