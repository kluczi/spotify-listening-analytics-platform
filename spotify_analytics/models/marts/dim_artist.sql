select
    artist_id,
    artist_name,
    image_url,
    spotify_url,
    fetched_at
from {{ ref('int_spotify__artists') }}
