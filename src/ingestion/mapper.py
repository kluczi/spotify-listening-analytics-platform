from datetime import datetime, timezone

from .models import Album, Artist, RecentlyPlayed, SavedTrack, Track


def _image_url(data: dict) -> str | None:
    images = data.get("images", [])
    return images[0]["url"] if images else None


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def map_album(data: dict) -> Album:
    return Album(
        id=data["id"],
        name=data["name"],
        type=data["album_type"],
        artists=map_artists(data["artists"]),
        release_date=data["release_date"],
        total_tracks=data["total_tracks"],
        spotify_url=data["external_urls"]["spotify"],
        image_url=_image_url(data),
    )


def map_artist(data: dict) -> Artist:
    return Artist(
        fetched_at=datetime.now(timezone.utc),
        id=data["id"],
        name=data["name"],
        spotify_url=data["external_urls"]["spotify"],
        image_url=_image_url(data),
    )


def map_artists(data: list[dict]) -> list[Artist]:
    return [map_artist(artist) for artist in data]


def map_track(data: dict) -> Track:
    return Track(
        fetched_at=datetime.now(timezone.utc),
        id=data["id"],
        name=data["name"],
        artists=map_artists(data["artists"]),
        album=map_album(data["album"]),
        duration_ms=data["duration_ms"],
        spotify_url=data["external_urls"]["spotify"],
    )


def map_saved_track(data: dict) -> SavedTrack:
    track = data["track"]
    return SavedTrack(
        fetched_at=datetime.now(timezone.utc),
        id=track["id"],
        name=track["name"],
        artists=map_artists(track["artists"]),
        album=map_album(track["album"]),
        duration_ms=track["duration_ms"],
        spotify_url=track["external_urls"]["spotify"],
        added_at=_parse_datetime(data["added_at"]),
    )


def map_recently_played(data: dict) -> RecentlyPlayed:
    track = data["track"]
    return RecentlyPlayed(
        fetched_at=datetime.now(timezone.utc),
        id=track["id"],
        name=track["name"],
        artists=map_artists(track["artists"]),
        album=map_album(track["album"]),
        duration_ms=track["duration_ms"],
        spotify_url=track["external_urls"]["spotify"],
        played_at=_parse_datetime(data["played_at"]),
    )
