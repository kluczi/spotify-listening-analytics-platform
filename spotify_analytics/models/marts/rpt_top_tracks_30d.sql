with listening_30d as (
    select track_id
    from {{ ref('fct_listening_history') }}
    where played_at >= dateadd(day, -30, current_timestamp())
),

track_listening as (
    select
        listening.track_id,
        sum(track.duration_s) as listening_seconds
    from listening_30d as listening
    inner join {{ ref('dim_track') }} as track
        on listening.track_id = track.track_id
    group by listening.track_id
),

ranked_tracks as (
    select
        track_id,
        listening_seconds,
        row_number() over (
            order by listening_seconds desc, track_id asc
        )::integer as ranking_position
    from track_listening
),

track_details as (
    select
        ranked.ranking_position,
        ranked.track_id,
        track.track_name,
        listagg(artist.artist_name, ', ') within group (
            order by bridge.is_primary desc, artist.artist_name asc
        ) as track_artists,
        album.album_image_url,
        round(ranked.listening_seconds / 60.0)::integer as listening_minutes
    from ranked_tracks as ranked
    inner join {{ ref('dim_track') }} as track
        on ranked.track_id = track.track_id
    inner join {{ ref('dim_album') }} as album
        on track.album_id = album.album_id
    inner join {{ ref('bridge_tracks_artists') }} as bridge
        on ranked.track_id = bridge.track_id
    inner join {{ ref('dim_artist') }} as artist
        on bridge.artist_id = artist.artist_id
    where ranked.ranking_position <= 5
    group by
        ranked.ranking_position,
        ranked.track_id,
        track.track_name,
        album.album_image_url,
        ranked.listening_seconds
)

select
    ranking_position,
    track_id,
    track_name,
    track_artists,
    track_name || ' - ' || track_artists as track_label,
    album_image_url,
    listening_minutes
from track_details
order by ranking_position
