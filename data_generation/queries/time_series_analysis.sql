WITH ranked_prices AS (
    SELECT symbol, price, timestamp,
           ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp) AS rn
    FROM market_data
    WHERE symbol IN ('AAPL', 'GOOGL')
)
SELECT a.symbol, b.symbol, CORR(a.price, b.price) AS correlation
FROM ranked_prices a
JOIN ranked_prices b ON a.rn = b.rn
WHERE a.symbol = 'AAPL' AND b.symbol = 'GOOGL'