-- models/staging/stg_telegram_messages.sql
WITH raw_messages AS (
    SELECT
        message_data ->> 'id' AS message_id,
        message_data ->> 'date' AS message_date_str,
        message_data ->> 'message' AS message_text,
        message_data ->> 'views' AS views_count_str,
        message_data ->> 'peer_id' ->> 'channel_id' AS channel_id,
        message_data ->> 'media' IS NOT NULL AS has_media, -- Check if 'media' key exists and is not null
        message_data ->> 'reactions' AS reactions_json, -- Keep as JSON for now if complex
        message_data -- Keep the original JSON for debugging/future extraction
    FROM {{ source('raw_data', 'raw_telegram_messages') }}
)
SELECT
    CAST(message_id AS BIGINT) AS message_id,
    CAST(message_date_str AS TIMESTAMP) AS message_timestamp,
    CAST(LEFT(message_date_str, 10) AS DATE) AS message_date, -- Extract date part for dim_dates
    message_text,
    CAST(views_count_str AS INT) AS views_count,
    CAST(channel_id AS BIGINT) AS channel_id,
    has_media,
    reactions_json,
    LENGTH(message_text) AS message_length
FROM raw_messages
WHERE message_id IS NOT NULL; -- Ensure message_id is present

-- models/staging/stg_telegram_messages.sql

WITH raw_messages AS (
    SELECT
        data ->> 'id' AS message_id,
        data ->> 'date' AS message_date,
        data ->> 'message' AS message_text,
        (data ->> 'has_image')::boolean AS has_image, -- Cast to boolean
        data ->> 'channel_id' AS channel_id,
        data ->> 'sender_id' AS sender_id,
        data ->> 'views' AS views_count, -- Assuming views is a string in raw JSON
        data -- Keep the raw JSON for debugging/future extraction if needed
    FROM
        raw.raw_telegram_messages -- Your raw table from the loading script
)

SELECT
    message_id::VARCHAR AS message_id, -- Ensure consistent type (e.g., if ID can be numeric or string)
    CAST(message_date AS TIMESTAMP) AS message_timestamp, -- Cast to timestamp
    message_text,
    LENGTH(message_text) AS message_length, -- Extract message length
    has_image,
    channel_id::VARCHAR AS channel_id,
    sender_id::VARCHAR AS sender_id,
    CAST(views_count AS INTEGER) AS views_count -- Cast to integer
FROM
    raw_messages
WHERE
    message_id IS NOT NULL -- Example: Basic cleaning, remove messages without an ID