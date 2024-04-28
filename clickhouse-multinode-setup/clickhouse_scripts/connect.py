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
    result = client.command(script)
    avg_query_time.append(st - time.time())
    time.sleep(1)

print(f'Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Max query execution time: {max(avg_query_time)}')
print(f'Min query execution time: {min(avg_query_time)}')


# for i in range(100):
#     result = client.command('''
#         SELECT
#             SumCapital / TotalRiskAdjustedValue AS CalculatedValue
#         FROM (
#             SELECT
#                 SUM(CASE
#                     WHEN asset_class IN ('Stocks', 'Gold Bonds', 'Futures', 'Options')
#                     THEN asset_market_value * asset_quantity
#                     ELSE 0
#                 END) AS SumCapital,
#                 SUM(a.asset_market_value * a.asset_quantity * r.risk_rating) AS TotalRiskAdjustedValue
#             FROM
#                 assets a
#             LEFT JOIN
#                 risk r ON a.asset_uuid = r.asset_uuid
#         ) AS results;
#     ''')
# print(result) 

# for i in range(100):
#     result = client.command('''
#         SELECT counterparty_uuid,
#         COUNT(*) AS transaction_count
#         FROM transactions
#         GROUP BY counterparty_uuid
#         ORDER BY transaction_count DESC
#         LIMIT 10;
#     ''')
# print(result) 

# for i in range(100):
#     result = client.command('''
#         SELECT
#             SUM(asset_market_value * asset_quantity) /
#             (SELECT SUM(amount) FROM Liabilities) AS Ratio
#         FROM assets
#         WHERE asset_class IN ('Stocks', 'Gold Bonds');
#     ''')
# print(result) 

# for i in range(100):
#     result = client.command('''
#         SELECT
#         (SELECT SUM(asset_market_value * asset_quantity)
#         FROM assets
#         WHERE asset_class IN ('Stocks', 'Gold Bonds')) /
#         (SELECT SUM(amount)
#         FROM transactions
#         WHERE due_date BETWEEN CURRENT_DATE AND DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY)
#         AND transaction_type IN ('Payment', 'Withdrawal', 'LoanRepayment')
#         AND confirmed = TRUE) AS LiquidityCoverageRatio;
#     ''')
# print(result) 


# for i in range(100):
#     result = client.command('''
#         SELECT
#             SUM(asset_market_value) AS TotalPortfolioValue,
#             AVG(daily_profit_loss) AS AverageDailyIncrease,
#             MAX(daily_profit_loss) AS MaxDailyAddition,
#             MIN(daily_profit_loss) AS MinDailyAddition
#         FROM (
#             SELECT
#                 DATE(FROM_UNIXTIME(value_timestamp / 1000)) AS val_date,
#                 SUM(asset_market_value) AS asset_market_value,
#                 (SUM(asset_market_value - asset_cost) - LAG(SUM(asset_market_value - asset_cost)) OVER (ORDER BY DATE(FROM_UNIXTIME(value_timestamp / 1000)))) AS daily_profit_loss
#             FROM assets
#             GROUP BY DATE(FROM_UNIXTIME(value_timestamp / 1000))
#         ) AS daily_data;
#     ''')
# print(result) 

# for i in range(100):
#     result = client.command('''
#         SELECT
#             SumCapital / TotalRiskAdjustedValue AS CalculatedValue
#         FROM (
#             SELECT
#                 SUM(CASE
#                     WHEN asset_class IN ('Stocks', 'Gold Bonds')
#                     THEN asset_market_value * asset_quantity
#                     ELSE 0
#                 END) AS SumCapital,
#                 SUM(a.asset_market_value * a.asset_quantity * r.risk_factor) AS TotalRiskAdjustedValue
#             FROM
#                 assets a
#             LEFT JOIN
#                 risk r ON a.asset_uuid = r.asset_uuid
#         ) AS results;
#     ''')
# print(result) 

# for i in range(100):
#     result = client.command('''
#         WITH ranked_prices AS (
#             SELECT asset_name, asset_market_value, timestamp,
#                 ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp) AS rn
#             FROM asset
#             WHERE asset_name IN ('AAPL', 'GOOGL')
#         )
#         SELECT a.asset_name, b.asset_name, CORR(a.asset_market_value, b.asset_market_value) AS correlation
#         FROM ranked_prices a
#         JOIN ranked_prices b ON a.rn = b.rn
#         WHERE a.asset_name = 'AAPL' AND b.asset_name = 'GOOGL'
#     ''')
# print(result) 

# for i in range(100):
#     result = client.command('''
#         SELECT category,
#         SUM(CASE WHEN confirmed THEN 1 ELSE 0 END) AS confirmed_count,
#         COUNT(*) AS total_count,
#         SUM(CASE WHEN confirmed THEN 1 ELSE 0 END) / COUNT(*)::DECIMAL AS confirmation_rate
#         FROM Transactions
#         GROUP BY category
#         ORDER BY confirmation_rate DESC;
#     ''')
# print(result) 