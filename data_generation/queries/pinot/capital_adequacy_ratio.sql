--Capital Adequacy Ratio

SELECT
    SumCapital / TotalRiskAdjustedValue AS CalculatedValue
FROM (
    SELECT
        SUM(CASE
            WHEN asset_class IN ('Stocks', 'Gold Bonds', 'Futures', 'Options')
            THEN asset_market_value * asset_quantity
            ELSE 0
        END) AS SumCapital,
        SUM(asset.asset_market_value * asset.asset_quantity * asset_risk.risk_rating) AS TotalRiskAdjustedValue
    FROM
        asset
    LEFT JOIN
        asset_risk ON asset.asset_uuid = asset_risk.asset_uuid
) AS results;