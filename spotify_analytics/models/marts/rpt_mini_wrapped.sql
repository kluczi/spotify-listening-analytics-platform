with listening_30d as (
    select
        listening_event_id,
        track_id,
        played_at
    from {{ ref('fct_listening_history') }}
    where played_at >= dateadd(day, -30, current_timestamp())
),

listening_metrics as (
    select
        count(*)::integer as total_plays,
        count(distinct track_id)::integer as unique_tracks
    from listening_30d
),

unique_artists as (
    select count(distinct bridge.artist_id)::integer as unique_artists
    from listening_30d as listening
    inner join {{ ref('bridge_tracks_artists') }} as bridge
        on listening.track_id = bridge.track_id
),

minutes_played as (
    select round(sum(track.duration_s) / 60.0)::integer as listening_minutes
    from listening_30d as listening
    inner join {{ ref('dim_track') }} as track
        on listening.track_id = track.track_id
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

most_played_artist as (
    select
        artist_id,
        artist_name as most_played_artist,
        image_url as most_played_artist_image_url,
        round(listening_seconds / 60.0)::integer
            as most_played_artist_listening_minutes
    from artist_listening
    order by
        listening_seconds desc,
        artist_id asc
    limit 1
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

most_played_track as (
    select
        track_id,
        listening_seconds
    from track_listening
    order by
        listening_seconds desc,
        track_id asc
    limit 1
),

most_played_track_details as (
    select
        most_played.track_id,
        track.track_name as most_played_track,
        album.album_image_url as most_played_track_album_image_url,
        round(most_played.listening_seconds / 60.0)::integer
            as most_played_track_listening_minutes,
        listagg(artist.artist_name, ', ') within group (
            order by bridge.is_primary desc, artist.artist_name asc
        ) as most_played_track_artists
    from most_played_track as most_played
    inner join {{ ref('dim_track') }} as track
        on most_played.track_id = track.track_id
    inner join {{ ref('dim_album') }} as album
        on track.album_id = album.album_id
    inner join {{ ref('bridge_tracks_artists') }} as bridge
        on most_played.track_id = bridge.track_id
    inner join {{ ref('dim_artist') }} as artist
        on bridge.artist_id = artist.artist_id
    group by
        most_played.track_id,
        track.track_name,
        album.album_image_url,
        most_played.listening_seconds
),

final as (
    select
        listening_metrics.total_plays,
        minutes_played.listening_minutes,
        listening_metrics.unique_tracks,
        unique_artists.unique_artists,
        most_played_artist.artist_id as most_played_artist_id,
        most_played_artist.most_played_artist,
        most_played_artist.most_played_artist_image_url,
        most_played_artist.most_played_artist_listening_minutes,
        most_played_track_details.track_id as most_played_track_id,
        most_played_track_details.most_played_track,
        most_played_track_details.most_played_track_artists,
        most_played_track_details.most_played_track_album_image_url,
        most_played_track_details.most_played_track_listening_minutes,
        most_played_track_details.most_played_track
        || ' - '
        || most_played_track_details.most_played_track_artists
            as most_played_track_label
    from listening_metrics
    cross join unique_artists
    cross join minutes_played
    cross join most_played_artist
    cross join most_played_track_details
)

select * from final
