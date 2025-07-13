-- models/data_mart/fct_messages.sql
SELECT
    stg.message_id,
    stg.message_timestamp,
    d_channels.channel_id,
    d_dates.date_key AS message_date_key,
    stg.message_text,
    stg.views_count,
    stg.has_media,
    stg.message_length
    -- Potentially parse reactions_json here for more metrics
FROM {{ ref('stg_telegram_messages') }} stg
LEFT JOIN {{ ref('dim_channels') }} d_channels
    ON stg.channel_id = d_channels.channel_id
LEFT JOIN {{ ref('dim_dates') }} d_dates
    ON stg.message_date = d_dates.date_key
WHERE stg.message_id IS NOT NULL;