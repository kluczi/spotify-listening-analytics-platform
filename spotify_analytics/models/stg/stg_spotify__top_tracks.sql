with source as (
    select
        payload:id::string as track_id,
        payload:name::string as track_name,
        payload:external_urls:spotify::string as spotify_url,
        payload:artists[0]:id::string as primary_artist_id,
        payload:album:id::string as album_id,
        payload:album:name::string as album_name,
        payload:album:album_type::string as album_type,
        payload:album:release_date::date as album_release_date,
        payload:album:images[1]:url::string as album_image_url,
        fetched_at,
        round(payload:duration_ms::number / 1000, 2) as duration_s,
        payload:artists as artists
    from {{ source('raw', 'top_tracks') }}
)

select * from source
