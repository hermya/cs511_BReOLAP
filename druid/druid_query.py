from pydruid.db import connect
from time import time

query_context = {
    "enableWindowing": "true"
}

# Connect to your Druid cluster
conn = connect(host='localhost', port=8888, path='/druid/v2/sql/', context=query_context)

# Create a cursor object
curs = conn.cursor()
csvstore = []

avg_query_time = []
for i in range(100):
    st = time.time()
    curs.execute('''
    SELECT asset.asset_name, asset.asset_class, counterparties.counterparty_name, SUM(transactions.transaction_amount)
        FROM transactions
        JOIN counterparties ON transactions.counterparty_uuid = counterparties.counterparty_uuid
        JOIN asset ON transactions.asset_linked = asset.asset_uuid
        WHERE transactions.transaction_type IN ('Payment','Withdrawal','InterestPayment','LoanRepayment')
        GROUP BY asset.asset_name, asset.asset_class, counterparties.counterparty_name
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Alpha Generation: Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Alpha Generation: Max query execution time: {max(avg_query_time)}')
print(f'Alpha Generation: Min query execution time: {min(avg_query_time)}')
csvstore.append(["Alpha Generation",sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(100):
    st = time.time()
    curs.execute('''
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
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Capital Adequacy Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Capital Adequacy Ratio: Max query execution time: {max(avg_query_time)}')
print(f'Capital Adequacy Ratio : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Capital Adequacy Ratio", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(100):
    st = time.time()
    curs.execute('''
        SELECT counterparty_uuid,
        COUNT(*) AS transaction_count
        FROM transactions
        GROUP BY counterparty_uuid
        ORDER BY transaction_count DESC
        LIMIT 10;
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Counterparty Transaction Volumne Analysis : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Counterparty Transaction Volumne Analysis : Max query execution time: {max(avg_query_time)}')
print(f'Counterparty Transaction Volumne Analysis : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Counterparty Transaction Volumne Analysis", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(100):
    st = time.time()
    curs.execute('''
        SELECT
            SUM(asset_market_value * asset_quantity) /
            (SELECT SUM(liability_amount) FROM liabilities) AS Ratio
        FROM asset
        WHERE asset_class IN ('Stocks', 'Gold Bonds');
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Leverage Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Leverage Ratio: Max query execution time: {max(avg_query_time)}')
print(f'Leverage Ratio: Min query execution time: {min(avg_query_time)}')
csvstore.append(["Leverage Ratio", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(100):
    st = time.time()
    curs.execute('''
        SELECT
        (SELECT SUM(asset_market_value * asset_quantity)
        FROM asset
        WHERE asset_class IN ('Stocks', 'Gold Bonds','Cash')) /
        (SELECT SUM(transaction_amount)
        FROM transactions
        WHERE ToDateTime(transaction_due_date*1000, 'yyyy-MM-dd') BETWEEN ToDateTime(now(), 'yyyy-MM-dd') AND ToDateTime(date_add('DAY', 30, now()),'yyyy-MM-dd')
        AND transaction_type IN ('Payment', 'Withdrawal', 'LoanRepayment')
        AND transaction_confirmed = 1) AS LiquidityCoverageRatio;    
        ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Liquidity Coverage Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Liquidity Coverage Ratio : Max query execution time: {max(avg_query_time)}')
print(f'Liquidity Coverage Ratio : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Liquidity Coverage Ratio", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(100):
    st = time.time()
    curs.execute('''
        SELECT
            SUM(asset_market_value) AS TotalPortfolioValue,
            AVG(daily_profit_loss) AS AverageDailyIncrease,
            MAX(daily_profit_loss) AS MaxDailyAddition,
            MIN(daily_profit_loss) AS MinDailyAddition
            FROM (
                SELECT
                    MILLIS_TO_TIMESTAMP(CAST("value_timestamp"*1000 AS BIGINT)) AS val_date,
                    SUM(asset_market_value) AS asset_market_value,
                    (SUM(asset_market_value - asset_cost) - LAG(SUM(asset_market_value - asset_cost)) OVER (ORDER BY MILLIS_TO_TIMESTAMP(CAST("value_timestamp"*1000 AS BIGINT)))) AS daily_profit_loss
                FROM asset
                GROUP BY MILLIS_TO_TIMESTAMP(CAST("value_timestamp"*1000 AS BIGINT))
        ) AS daily_data
        ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Portfolio Metric Collections : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Portfolio Metric Collections : Max query execution time: {max(avg_query_time)}')
print(f'Portfolio Metric Collections : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Portfolio Metric Collections",sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(100):
    st = time.time()
    curs.execute('''
        SELECT
            SumCapital / TotalRiskAdjustedValue AS CalculatedValue
        FROM (
            SELECT
                SUM(CASE
                    WHEN asset_class IN ('Stocks', 'Gold Bonds')
                    THEN asset_market_value * asset_quantity
                    ELSE 0
                END) AS SumCapital,
                SUM(a.asset_market_value * a.asset_quantity * r.risk_rating) AS TotalRiskAdjustedValue
            FROM
                asset a
            LEFT JOIN
                risk r ON a.asset_uuid = r.asset_uuid
        ) AS results;
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Tier1 Capital Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Tier1 Capital Ratio : Max query execution time: {max(avg_query_time)}')
print(f'Tier1 Capital Ratio : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Tier1 Capital Ratio", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])


avg_query_time = []
for i in range(100):
    st = time.time()
    curs.execute('''
        WITH ranked_prices AS (
            SELECT asset_name, asset_market_value, value_timestamp,
                ROW_NUMBER() OVER (PARTITION BY asset_name ORDER BY value_timestamp) AS rn
            FROM asset
            WHERE asset_name IN ('AAPL', 'GOOGL')
        )
        SELECT a.asset_name, b.asset_name, CORR(toInt64(a.asset_market_value), toInt64(b.asset_market_value)) AS correlation
        FROM ranked_prices a
        JOIN ranked_prices b ON a.rn = b.rn
        GROUP BY a.asset_name, b.asset_name;
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Time series analysis : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Time series analysis : Max query execution time: {max(avg_query_time)}')
print(f'Time series analysis : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Time series analysis", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])


avg_query_time = []
for i in range(100):
    st = time.time()
    curs.execute('''
        SELECT transaction_category,
        SUM(CASE WHEN transaction_confirmed = 1 THEN 1 ELSE 0 END) AS confirmed_count,
        COUNT(*) AS total_count,
        SUM(CASE WHEN transaction_confirmed = 1 THEN 1 ELSE 0 END) / COUNT(*)::DECIMAL AS confirmation_rate
        FROM transactions
        GROUP BY transaction_category
        ORDER BY confirmation_rate DESC;
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Transaction Confirmation Rate : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Transaction Confirmation Rate : Max query execution time: {max(avg_query_time)}')
print(f'Transaction Confirmation Rate : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Transaction Confirmation Rate", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

with open("values.csv","w") as file:
    for row in csvstore:
        row = [str(x) for x in row]
        file.write(",".join(row) + "\n")


# Close the connection
conn.close()
