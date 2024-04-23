--Leverage Ratio

SELECT
    SUM(asset_market_value * asset_quantity) /
    (SELECT SUM(amount) FROM Liabilities) AS Ratio
FROM assets
WHERE asset_class IN ('Stocks', 'Gold Bonds');