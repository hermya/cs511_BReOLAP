CREATE TABLE liabilities_topic
(
    `liability_id` Int32,
	`bank_id` String,
	`liability_amount` Decimal64(5),
	`interest_rate` Decimal64(5),
	`start_date` Decimal64(5),
	`maturity_date` Decimal64(5),
	`counterparty_uuid` String,
	`status` String,
	`created_at` Decimal64(5),
	`created_by` String
)
ENGINE = MergeTree
PRIMARY KEY liability_id
ORDER BY liability_id
SETTINGS index_granularity = 8192;