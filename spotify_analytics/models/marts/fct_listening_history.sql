with listening_events as (
    select
        {{ dbt_utils.generate_surrogate_key([
            'played_at', 'track_id'
        ]) }} as listening_event_id,
        track_id,
        played_at,
        fetched_at
    from {{ ref('stg_spotify__recently_played') }}
    qualify row_number() over (
        partition by played_at, track_id
        order by fetched_at desc
    ) = 1
)

select * from listening_events
