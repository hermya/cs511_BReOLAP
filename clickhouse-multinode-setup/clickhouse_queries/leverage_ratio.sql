SELECT
SUM(asset_market_value * asset_quantity) /
(SELECT SUM(amount) FROM Liabilities) AS Ratio
FROM asset_topic
WHERE asset_class IN ('Stocks', 'Gold Bonds');