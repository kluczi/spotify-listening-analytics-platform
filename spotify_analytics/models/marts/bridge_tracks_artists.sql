select
    track_id,
    artist_id,
    artist_name,
    is_primary,
    spotify_url,
    fetched_at
from {{ ref('int_spotify__track_artists') }}
