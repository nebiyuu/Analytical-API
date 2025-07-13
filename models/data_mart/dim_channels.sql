-- models/data_mart/dim_channels.sql
SELECT DISTINCT
    channel_id,
    -- Add any other channel-specific attributes if available in raw data
    -- For now, we only have channel_id from messages. In a real scenario,
    -- you'd likely have a separate source for channel metadata.
    'Unknown Channel Name' AS channel_name -- Placeholder
FROM {{ ref('stg_telegram_messages') }}
WHERE channel_id IS NOT NULL;-- models/data_mart/dim_channels.sql
SELECT DISTINCT
    channel_id,
    -- Add any other channel-specific attributes if available in raw data
    -- For now, we only have channel_id from messages. In a real scenario,
    -- you'd likely have a separate source for channel metadata.
    'Unknown Channel Name' AS channel_name -- Placeholder
FROM {{ ref('stg_telegram_messages') }}
WHERE channel_id IS NOT NULL;