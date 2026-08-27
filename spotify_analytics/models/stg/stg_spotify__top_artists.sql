with source as (
    select
        fetched_at,
        payload:id::string as artist_id,
        payload:name::string as artist_name,
        payload:images[1]:url::string as image_url,
        payload:external_urls:spotify::string as spotify_url
    from {{ source('raw', 'top_artists') }}
)

select * from source
