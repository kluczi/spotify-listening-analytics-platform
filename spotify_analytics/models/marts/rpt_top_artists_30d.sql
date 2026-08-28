with listening_30d as (
    select track_id
    from {{ ref('fct_listening_history') }}
    where played_at >= dateadd(day, -30, current_timestamp())
),

artist_listening as (
    select
        bridge.artist_id,
        artist.artist_name,
        artist.image_url,
        sum(track.duration_s) as listening_seconds
    from listening_30d as listening
    inner join {{ ref('dim_track') }} as track
        on listening.track_id = track.track_id
    inner join {{ ref('bridge_tracks_artists') }} as bridge
        on listening.track_id = bridge.track_id
    inner join {{ ref('dim_artist') }} as artist
        on bridge.artist_id = artist.artist_id
    group by
        bridge.artist_id,
        artist.artist_name,
        artist.image_url
),

ranked_artists as (
    select
        artist_id,
        artist_name,
        image_url,
        round(listening_seconds / 60.0)::integer as listening_minutes,
        row_number() over (
            order by listening_seconds desc, artist_id asc
        )::integer as ranking_position
    from artist_listening
)

select
    ranking_position,
    artist_id,
    artist_name,
    image_url,
    listening_minutes
from ranked_artists
where ranking_position <= 5
order by ranking_position
