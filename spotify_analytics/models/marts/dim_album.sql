select
    album_id,
    album_name,
    album_type,
    album_release_date,
    fetched_at
from {{ ref('int_spotify__albums') }}
