with source as (
    select
        payload:track:id::string as track_id,
        payload:track:name::string as track_name,
        payload:track:external_urls:spotify::string as spotify_url,
        payload:track:artists[0]:id::string as primary_artist_id,
        payload:track:album:id::string as album_id,
        payload:track:album:name::string as album_name,
        payload:track:album:album_type::string as album_type,
        payload:track:album:release_date::date as album_release_date,
        payload:played_at::timestamp_tz as played_at,
        fetched_at,
        round(payload:track:duration_ms::number / 1000, 2) as duration_s,
        payload:track:artists as artists
    from {{ source('raw', 'recently_played_tracks') }}
)

select * from source
