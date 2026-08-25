from dataclasses import dataclass
from datetime import datetime


@dataclass
class Artist:
    fetched_at: datetime
    id: str
    name: str
    spotify_url: str
    image_url: str | None


@dataclass
class Album:
    id: str
    name: str
    type: str
    artists: list[Artist]
    release_date: str
    total_tracks: int
    spotify_url: str
    image_url: str | None


@dataclass
class Track:
    fetched_at: datetime
    id: str
    name: str
    artists: list[Artist]
    album: Album
    duration_ms: int
    spotify_url: str


@dataclass
class SavedTrack:
    fetched_at: datetime
    id: str
    name: str
    artists: list[Artist]
    album: Album
    duration_ms: int
    spotify_url: str
    added_at: datetime


@dataclass
class RecentlyPlayed:
    fetched_at: datetime
    id: str
    name: str
    artists: list[Artist]
    album: Album
    duration_ms: int
    spotify_url: str
    played_at: datetime
