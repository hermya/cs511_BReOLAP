CREATE TABLE transactions_topic
(
    `transaction_id` Int32,
      `transaction_uuid` String,
      `transaction_date` Decimal64(5),
      `transaction_amount` Decimal64(5),
      `transaction_type` String,
      `transaction_due_date` Decimal64(5),
      `transaction_category` String,
      `transaction_confirmed` Int32,
      `asset_linked` String,
      `counterparty_uuid` String,
      `created_at` Decimal64(5)
)
ENGINE = MergeTree
PRIMARY KEY transaction_id
ORDER BY transaction_id
SETTINGS index_granularity = 8192;