from pinotdb import connect

conn = connect(host='localhost', port=8099, path='/query', scheme='http')
curs = conn.cursor()
curs.execute("""
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
""")
# for row in curs:
#     print(row)

curs.execute("""
    SELECT transactions.symbol,
       counterparties.counterparty_name,
       SUM(transactions.amount) AS total_transaction_volume
    FROM transactions
    JOIN counterparties ON transactions.counterparty_uuid = counterparties.counterparty_uuid
    WHERE transactions.transaction_type IN ('Payment', 'Withdrawal', 'InterestPayment', 'LoanRepayment')
    GROUP BY transactions.symbol, counterparties.counterparty_name
    ORDER BY total_transaction_volume DESC;
""")

curs.execute("""
    SELECT counterparty_uuid,
       COUNT(*) AS transaction_count
    FROM transactions
    GROUP BY counterparty_uuid
    ORDER BY transaction_count DESC
    LIMIT 10;
""")

curs.execute("""
    SELECT
    SUM(asset_market_value * asset_quantity) /
    (SELECT SUM(amount) FROM liabilities) AS Ratio
    FROM assets
    WHERE asset_class IN ('Stocks', 'Gold Bonds');
""")


curs.execute("""
    SELECT
    (SELECT SUM(asset_market_value * asset_quantity)
    FROM assets
    WHERE asset_class IN ('Stocks', 'Gold Bonds')) /
    (SELECT SUM(amount)
    FROM transactions
    WHERE due_date BETWEEN CURRENT_DATE AND DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY)
    AND transaction_type IN ('Payment', 'Withdrawal', 'LoanRepayment')
    AND confirmed = TRUE) AS LiquidityCoverageRatio;
""")



curs.execute("""
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
""")


curs.execute("""
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
""")




curs.execute("""
    SELECT category,
       SUM(CASE WHEN confirmed THEN 1 ELSE 0 END) AS confirmed_count,
       COUNT(*) AS total_count,
       SUM(CASE WHEN confirmed THEN 1 ELSE 0 END) / COUNT(*) AS confirmation_rate
    FROM Transactions
    GROUP BY category
    ORDER BY confirmation_rate DESC;
""")

# Close the connection
conn.close()
