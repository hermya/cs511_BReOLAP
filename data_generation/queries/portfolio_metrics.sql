--Portfolio Metric Collections

SELECT
    SUM(asset_market_value) AS TotalPortfolioValue,
    AVG(daily_profit_loss) AS AverageDailyIncrease,
    MAX(daily_profit_loss) AS MaxDailyAddition,
    MIN(daily_profit_loss) AS MinDailyAddition
FROM (
    SELECT
        DATE(FROM_UNIXTIME(value_timestamp / 1000)) AS val_date,
        SUM(asset_market_value) AS asset_market_value,
        (SUM(asset_market_value - asset_cost) - LAG(SUM(asset_market_value - asset_cost)) OVER (ORDER BY DATE(FROM_UNIXTIME(value_timestamp / 1000)))) AS daily_profit_loss
    FROM assets
    GROUP BY DATE(FROM_UNIXTIME(value_timestamp / 1000))
) AS daily_data;