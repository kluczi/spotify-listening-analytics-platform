with listening_events as (
    select
        track_id,
        convert_timezone(
            'Europe/Warsaw',
            played_at
        )::date as listening_date
    from {{ ref('fct_listening_history') }}
),

daily_listening as (
    select
        listening.listening_date,
        count(listening.track_id)::integer as total_plays,
        round(sum(track.duration_s) / 60)::integer as listening_minutes
    from listening_events as listening
    left join {{ ref('dim_track') }} as track
        on listening.track_id = track.track_id
    group by listening.listening_date
)

select * from daily_listening
