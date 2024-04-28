SELECT
    SumCapital / TotalRiskAdjustedValue AS CalculatedValue
FROM (
    SELECT
        SUM(CASE
            WHEN asset_class IN ('Stocks', 'Gold Bonds')
            THEN asset_market_value * asset_quantity
            ELSE 0
        END) AS SumCapital,
        SUM(a.asset_market_value * a.asset_quantity * r.risk_factor) AS TotalRiskAdjustedValue
    FROM
        asset_topic a
    LEFT JOIN
        risk_topic r ON a.asset_uuid = r.asset_uuid
) AS results;