CREATE TABLE counterparties_topic
(
    `counterparty_id` Int32,
	`counterparty_uuid` String,
	`counterparty_name` String,
	`counterparty_type` String,
	`created_at` Decimal64(5)
)
ENGINE = MergeTree
PRIMARY KEY counterparty_id
ORDER BY counterparty_id
SETTINGS index_granularity = 8192;