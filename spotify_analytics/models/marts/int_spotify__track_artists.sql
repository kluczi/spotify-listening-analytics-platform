with recently_played as (
    select
        recently_played.track_id,
        artist.value:id::string as artist_id,
        artist.value:name::string as artist_name,
        artist.index = 0 as is_primary,
        artist.value:external_urls:spotify::string as spotify_url,
        recently_played.fetched_at
    from {{ ref('stg_spotify__recently_played') }} as recently_played,
        lateral flatten(input => recently_played.artists) as artist

),

top_tracks as (
    select
        top_tracks.track_id,
        artist.value:id::string as artist_id,
        artist.value:name::string as artist_name,
        artist.index = 0 as is_primary,
        artist.value:external_urls:spotify::string as spotify_url,
        top_tracks.fetched_at
    from {{ ref('stg_spotify__top_tracks') }} as top_tracks,
        lateral flatten(input => top_tracks.artists) as artist

),

saved_tracks as (
    select
        saved_tracks.track_id,
        artist.value:id::string as artist_id,
        artist.value:name::string as artist_name,
        artist.index = 0 as is_primary,
        artist.value:external_urls:spotify::string as spotify_url,
        saved_tracks.fetched_at
    from {{ ref('stg_spotify__saved_tracks') }} as saved_tracks,
        lateral flatten(input => saved_tracks.artists) as artist

),

unioned as (
    select *
    from top_tracks
    union all
    select *
    from saved_tracks
    union all
    select *
    from recently_played
),

final as (
    select
        track_id,
        artist_id,
        artist_name,
        is_primary,
        spotify_url,
        fetched_at
    from unioned
    qualify row_number() over (
        partition by track_id, artist_id
        order by fetched_at desc
    ) = 1
)

select * from final
