with artists as (

    select
        artist_id,
        artist_name,
        image_url,
        spotify_url,
        fetched_at
    from {{ ref('stg_spotify__followed_artists') }}

    union all

    select
        artist_id,
        artist_name,
        image_url,
        spotify_url,
        fetched_at
    from {{ ref('stg_spotify__top_artists') }}

    union all

    select
        artist_id,
        artist_name,
        null::string as image_url,
        spotify_url,
        fetched_at
    from {{ ref('int_spotify__track_artists') }}

),

final as (
    select
        artist_id,
        artist_name,
        image_url,
        spotify_url,
        fetched_at
    from artists

    qualify row_number() over (
        partition by artist_id
        order by fetched_at desc
    ) = 1
)

select * from final
