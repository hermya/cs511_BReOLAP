CREATE TABLE transactions_topic
(
    `transaction_id` Int32,
    `transaction_uuid` String,
    `transaction_type` String,
    `amount` Float32,
    `transaction_date` String,
    `created_at` String
)
ENGINE = MergeTree
PRIMARY KEY transaction_id
ORDER BY transaction_id
SETTINGS index_granularity = 8192;