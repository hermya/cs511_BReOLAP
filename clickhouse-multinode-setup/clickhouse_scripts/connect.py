import clickhouse_connect
import time
import os
import sys
client = clickhouse_connect.get_client(host='localhost',
                                       user='default',
                                       connect_timeout=15,
                                       database='default',
                                       settings={'distributed_ddl_task_timeout':30000})
os.getcwd()
path = os.getcwd() + "/" + sys.argv[1]
print("Reading script from ", path)
script = ""
with open(path, 'r') as file:
    script = file.read()

avg_query_time = []
for i in range(100):
    st = time.time()
    result = client.command('''
    SELECT a.asset_name, a.asset_class, c.counterparty_name, SUM(t.transaction_amount)
        FROM transactions_topic t
        JOIN counterparties_topic c ON t.counterparty_uuid = c.counterparty_uuid
        JOIN asset_topic a ON t.asset_linked = a.asset_uuid
        WHERE t.transaction_type IN ('Payment','Withdrawal','InterestPayment','LoanRepayment')
        GROUP BY a.asset_name, a.asset_class, c.counterparty_name
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Max query execution time: {max(avg_query_time)}')
print(f'Min query execution time: {min(avg_query_time)}')


avg_query_time = []
for i in range(100):
    st = time.time()
    result = client.command('''
        SELECT
            SumCapital / TotalRiskAdjustedValue AS CalculatedValue
        FROM (
            SELECT
                SUM(CASE
                    WHEN asset_class IN ('Stocks', 'Gold Bonds', 'Futures', 'Options')
                    THEN asset_market_value * asset_quantity
                    ELSE 0
                END) AS SumCapital,
                SUM(a.asset_market_value * a.asset_quantity * r.risk_rating) AS TotalRiskAdjustedValue
            FROM
                asset_topic a
            LEFT JOIN
                risk_topic r ON a.asset_uuid = r.asset_uuid
        ) AS results;
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Capital Adequacy Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Capital Adequacy Ratio: Max query execution time: {max(avg_query_time)}')
print(f'Capital Adequacy Ratio : Min query execution time: {min(avg_query_time)}')


avg_query_time = []
for i in range(100):
    st = time.time()
    result = client.command('''
        SELECT counterparty_uuid,
        COUNT(*) AS transaction_count
        FROM transactions_topic
        GROUP BY counterparty_uuid
        ORDER BY transaction_count DESC
        LIMIT 10;
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Counterparty Transaction Volumne Analysis : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Counterparty Transaction Volumne Analysis : Max query execution time: {max(avg_query_time)}')
print(f'Counterparty Transaction Volumne Analysis : Min query execution time: {min(avg_query_time)}')


avg_query_time = []
for i in range(100):
    st = time.time()
    result = client.command('''
        SELECT
            SUM(asset_market_value * asset_quantity) /
            (SELECT SUM(amount) FROM Liabilities) AS Ratio
        FROM asset_topic
        WHERE asset_class IN ('Stocks', 'Gold Bonds');
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Leverage Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Leverage Ratio: Max query execution time: {max(avg_query_time)}')
print(f'Leverage Ratio: Min query execution time: {min(avg_query_time)}')


avg_query_time = []
for i in range(100):
    st = time.time()
    result = client.command('''
        SELECT
        (SELECT SUM(asset_market_value * asset_quantity)
        FROM asset_topic
        WHERE asset_class IN ('Stocks', 'Gold Bonds')) /
        (SELECT SUM(amount)
        FROM transactions_topic
        WHERE due_date BETWEEN CURRENT_DATE AND DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY)
        AND transaction_type IN ('Payment', 'Withdrawal', 'LoanRepayment')
        AND confirmed = TRUE) AS LiquidityCoverageRatio;
        ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Liquidity Coverage Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Liquidity Coverage Ratio : Max query execution time: {max(avg_query_time)}')
print(f'Liquidity Coverage Ratio : Min query execution time: {min(avg_query_time)}')


avg_query_time = []
for i in range(100):
    st = time.time()
    result = client.command('''
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
            FROM asset_topic
            GROUP BY DATE(FROM_UNIXTIME(value_timestamp / 1000))
        ) AS daily_data;
        ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Portfolio Metric Collections: Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Portfolio Metric Collections : Max query execution time: {max(avg_query_time)}')
print(f'Portfolio Metric Collections : Min query execution time: {min(avg_query_time)}')


avg_query_time = []
for i in range(100):
    st = time.time()
    result = client.command('''
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
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Tier1 Capital Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Tier1 Capital Ratio : Max query execution time: {max(avg_query_time)}')
print(f'Tier1 Capital Ratio : Min query execution time: {min(avg_query_time)}')



avg_query_time = []
for i in range(100):
    st = time.time()
    result = client.command('''
        WITH ranked_prices AS (
            SELECT asset_name, asset_market_value, timestamp,
                ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp) AS rn
            FROM asset_topic
            WHERE asset_name IN ('AAPL', 'GOOGL')
        )
        SELECT a.asset_name, b.asset_name, CORR(a.asset_market_value, b.asset_market_value) AS correlation
        FROM ranked_prices a
        JOIN ranked_prices b ON a.rn = b.rn
        WHERE a.asset_name = 'AAPL' AND b.asset_name = 'GOOGL'
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Time series analysis : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Time series analysis : Max query execution time: {max(avg_query_time)}')
print(f'Time series analysis : Min query execution time: {min(avg_query_time)}')


avg_query_time = []
for i in range(100):
    st = time.time()
    result = client.command('''
        SELECT category,
        SUM(CASE WHEN confirmed THEN 1 ELSE 0 END) AS confirmed_count,
        COUNT(*) AS total_count,
        SUM(CASE WHEN confirmed THEN 1 ELSE 0 END) / COUNT(*)::DECIMAL AS confirmation_rate
        FROM transactions_topic
        GROUP BY category
        ORDER BY confirmation_rate DESC;
    ''')
    et = time.time() - st
    avg_query_time.append(et)
print(f'Transaction Confirmation Rate : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Transaction Confirmation Rate : Max query execution time: {max(avg_query_time)}')
print(f'Transaction Confirmation Rate : Min query execution time: {min(avg_query_time)}')