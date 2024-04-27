WITH ranked_prices AS (
    SELECT asset_name, asset_market_value, timestamp,
           ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp) AS rn
    FROM asset
    WHERE asset_name IN ('AAPL', 'GOOGL')
)
SELECT a.asset_name, b.asset_name, CORR(a.asset_market_value, b.asset_market_value) AS correlation
FROM ranked_prices a
JOIN ranked_prices b ON a.rn = b.rn
WHERE a.asset_name = 'AAPL' AND b.asset_name = 'GOOGL'