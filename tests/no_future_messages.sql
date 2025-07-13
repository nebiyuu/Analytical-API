-- tests/no_future_messages.sql
SELECT message_id
FROM {{ ref('fct_messages') }}
WHERE message_timestamp > CURRENT_TIMESTAMP;