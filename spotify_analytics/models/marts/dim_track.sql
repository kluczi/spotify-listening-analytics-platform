select
    track_id,
    track_name,
    duration_s,
    album_id,
    fetched_at
from {{ ref('int_spotify__tracks') }}
