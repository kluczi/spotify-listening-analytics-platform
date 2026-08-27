with recently_played as (
    select
        track_id,
        track_name,
        spotify_url,
        album_id,
        duration_s,
        fetched_at
    from {{ ref('stg_spotify__recently_played') }}

),

top_tracks as (
    select
        track_id,
        track_name,
        spotify_url,
        album_id,
        duration_s,
        fetched_at
    from {{ ref('stg_spotify__top_tracks') }}
),

saved_tracks as (
    select
        track_id,
        track_name,
        spotify_url,
        album_id,
        duration_s,
        fetched_at
    from {{ ref('stg_spotify__saved_tracks') }}
),

unioned as (
    select * from recently_played
    union all
    select * from top_tracks
    union all
    select * from saved_tracks

),

final as (
    select
        track_id,
        track_name,
        spotify_url,
        album_id,
        duration_s,
        fetched_at
    from unioned
    qualify row_number() over (
        partition by track_id
        order by fetched_at desc
    ) = 1
)

select * from final
