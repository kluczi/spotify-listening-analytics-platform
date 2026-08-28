---
title: Spotify Mini Wrapped
---

```sql mini_wrapped
select *
from SPOTIFY_ANALYTICS.ANALYTICS.RPT_MINI_WRAPPED
```

```sql listening_calendar
select *
from SPOTIFY_ANALYTICS.ANALYTICS.RPT_LISTENING_CALENDAR_DAILY
order by listening_date
```

# Spotify Mini Wrapped (last 30 days)

{% row align="top" %}
{% stack card=true width=23 %}

    {% big_value
      data="mini_wrapped"
      value="max(total_plays)"
      title="Plays (Last 30 Days)"
      fmt="num0"
    /%}

{% /stack %}

{% stack card=true width=23 %}

    {% big_value
      data="mini_wrapped"
      value="max(listening_minutes)"
      title="Listening Minutes"
      fmt="num0"
    /%}

{% /stack %}

{% stack card=true width=23 %}

    {% big_value
      data="mini_wrapped"
      value="max(unique_tracks)"
      title="Unique Tracks"
      fmt="num0"
    /%}

{% /stack %}

{% stack card=true width=23 %}

    {% big_value
      data="mini_wrapped"
      value="max(unique_artists)"
      title="Unique Artists"
      fmt="num0"
    /%}

{% /stack %}
{% /row %}

{% row align="top" %}
{% stack align="center" card=true width=48 %}

## Most Played Track

    {% image
      data="mini_wrapped"
      column="most_played_track_album_image_url"
      description_column="most_played_track_label"
      max_width=320
      class="aspect-square object-cover"
      align="center"
    /%}

    {% value
      data="mini_wrapped"
      value="any_value(most_played_track_label)"
      className="text-xl font-semibold"
    /%}

    {% value
      data="mini_wrapped"
      value="concat(max(most_played_track_listening_minutes), case when max(most_played_track_listening_minutes) = 1 then ' minute listened' else ' minutes listened' end)"
      className="text-sm"
      color="#B3B3B3"
    /%}

{% /stack %}

{% stack align="center" card=true width=48 %}

## Most Played Artist

    {% image
      data="mini_wrapped"
      column="most_played_artist_image_url"
      description_column="most_played_artist"
      max_width=320
      class="aspect-square object-cover"
      align="center"
    /%}

    {% value
      data="mini_wrapped"
      value="any_value(most_played_artist)"
      className="text-xl font-semibold"
    /%}

    {% value
      data="mini_wrapped"
      value="concat(max(most_played_artist_listening_minutes), case when max(most_played_artist_listening_minutes) = 1 then ' minute listened' else ' minutes listened' end)"
      className="text-sm"
      color="#B3B3B3"
    /%}

{% /stack %}
{% /row %}

{% row align="top" %}
{% stack card=true width=48 %}

## Top 5 Tracks

    {% table
      data="ANALYTICS.RPT_TOP_TRACKS_30D"
      order="RANKING_POSITION"
      subtotals=false
      show_total_row=false
      row_lines=false
      page_size=5
    %}
      {% dimension
        value="RANKING_POSITION"
        title="#"
        align="center"
        fmt="num0"
      /%}
      {% dimension
        value="TRACK_LABEL"
        title="Track"
        image="ALBUM_IMAGE_URL"
      /%}
    {% /table %}

{% /stack %}

{% stack card=true width=48 %}

## Top 5 Artists

    {% table
      data="ANALYTICS.RPT_TOP_ARTISTS_30D"
      order="RANKING_POSITION"
      subtotals=false
      show_total_row=false
      row_lines=false
      page_size=5
    %}
      {% dimension
        value="RANKING_POSITION"
        title="#"
        align="center"
        fmt="num0"
      /%}
      {% dimension
        value="ARTIST_NAME"
        title="Artist"
        image="IMAGE_URL"
      /%}
    {% /table %}

{% /stack %}
{% /row %}

## Listening Calendar

{% calendar_heatmap
  data="listening_calendar"
  date="listening_date"
  value="sum(listening_minutes)"
  title="Daily Listening Minutes"
  tooltip_fields=[
    { value="sum(total_plays)" label="Plays" }
  ]
/%}
