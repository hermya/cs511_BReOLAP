CREATE TABLE asset_topic
(
    `asset_id` Int32,
	`asset_uuid` String,
	`asset_class` String,
	`asset_name` String,
	`asset_cost` Decimal64(5),
	`asset_market_value` Decimal64(5),
	`asset_quantity` Int32,
	`liquidity_rating` String,
	`asset_owner` String,
	`portfolio_manager` String,
	`value_timestamp` Decimal64(5)
)
ENGINE = MergeTree
PRIMARY KEY asset_id
ORDER BY asset_id
SETTINGS index_granularity = 8192;