CREATE TABLE risk_topic
(
    `asset_uuid` String,
    `risk_uuid` String,
    `risk_rating` Float32
)
ENGINE = MergeTree
PRIMARY KEY asset_uuid;