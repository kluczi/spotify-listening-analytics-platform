from .client import spotify_get
from typing import Literal

TimeRange = Literal[
    "short_term",
    "medium_term",
    "long_term",
]


def get_user_recently_played(
    limit: int = 50,
    before: int | None = None,
    after: int | None = None,
) -> dict:
    if before is not None and after is not None:
        raise ValueError("'before' and 'after' cannot be used together")
    params = {"limit": limit}
    if after is not None:
        params["after"] = after
    if before is not None:
        params["before"] = before

    return spotify_get("me/player/recently-played", params)


def get_user_top_tracks(
    time_range: TimeRange = "short_term",
    limit: int = 50,
    offset: int = 0,
) -> dict:
    params = {
        "time_range": time_range,
        "limit": limit,
        "offset": offset,
    }

    return spotify_get("me/top/tracks", params)


def get_user_top_artists(
    time_range: str = "short_term",
    limit: int = 50,
    offset: int = 0,
) -> dict:
    params = {
        "time_range": time_range,
        "limit": limit,
        "offset": offset,
    }

    return spotify_get("me/top/artists", params)


def get_user_followed_artists(limit: int = 50) -> dict:
    params = {"type": "artist", "limit": limit}

    return spotify_get("me/following", params)


def get_user_saved_tracks(limit: int = 50, offset: int = 0) -> dict:
    params = {"limit": limit, "offset": offset}

    return spotify_get("me/tracks", params)
