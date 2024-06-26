from pinotdb import connect
import time

conn = connect(host='localhost', port=8099, path='/query', scheme='http')
curs = conn.cursor()

csvstore = []

avg_query_time = []
for i in range(110):
    st = time.time()
    curs.execute('''
    SET maxRowsInJoin = 40000000;    
    SET timeoutMs = 40000000;                          
    SELECT asset.asset_name, asset.asset_class, counterparties.counterparty_name, SUM(transactions.transaction_amount)
        FROM transactions
        JOIN counterparties ON transactions.counterparty_uuid = counterparties.counterparty_uuid
        JOIN asset ON transactions.asset_linked = asset.asset_uuid
        WHERE transactions.transaction_type IN ('Payment','Withdrawal','InterestPayment','LoanRepayment')
        GROUP BY asset.asset_name, asset.asset_class, counterparties.counterparty_name
    ''')
    et = time.time() - st
    if i > 10:
        avg_query_time.append(et)
print(f'Alpha Generation: Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Alpha Generation: Max query execution time: {max(avg_query_time)}')
print(f'Alpha Generation: Min query execution time: {min(avg_query_time)}')
csvstore.append(["Alpha Generation",sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(110):
    st = time.time()
    curs.execute('''
        SET maxRowsInJoin = 40000000;
        SET timeoutMs = 40000000;                   
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
    if i > 10:
        avg_query_time.append(et)
    
print(f'Capital Adequacy Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Capital Adequacy Ratio: Max query execution time: {max(avg_query_time)}')
print(f'Capital Adequacy Ratio : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Capital Adequacy Ratio", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(110):
    st = time.time()
    curs.execute('''
        SET timeoutMs = 40000000;         
        SELECT counterparty_uuid,
        COUNT(*) AS transaction_count
        FROM transactions
        GROUP BY counterparty_uuid
        ORDER BY transaction_count DESC
        LIMIT 10;
    ''')
    et = time.time() - st
    if i > 10:
        avg_query_time.append(et)

print(f'Counterparty Transaction Volumne Analysis : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Counterparty Transaction Volumne Analysis : Max query execution time: {max(avg_query_time)}')
print(f'Counterparty Transaction Volumne Analysis : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Counterparty Transaction Volumne Analysis", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(110):
    st = time.time()
    curs.execute('''
        SET timeoutMs = 40000000;         
        SELECT
            SUM(asset_market_value * asset_quantity) /
            (SELECT SUM(liability_amount) FROM liabilities) AS Ratio
        FROM asset
        WHERE asset_class IN ('Stocks', 'Gold Bonds');
    ''')
    et = time.time() - st
    if i > 10:
        avg_query_time.append(et)
print(f'Leverage Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Leverage Ratio: Max query execution time: {max(avg_query_time)}')
print(f'Leverage Ratio: Min query execution time: {min(avg_query_time)}')
csvstore.append(["Leverage Ratio", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(110):
    st = time.time()
    curs.execute('''
        SET timeoutMs = 40000000;         
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
    if i > 10:
        avg_query_time.append(et)
print(f'Liquidity Coverage Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Liquidity Coverage Ratio : Max query execution time: {max(avg_query_time)}')
print(f'Liquidity Coverage Ratio : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Liquidity Coverage Ratio", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(110):
    st = time.time()
    curs.execute('''
        SET timeoutMs = 40000000;         
        SELECT
            SUM(asset_market_value_today) AS TotalPortfolioValue,
            AVG(daily_profit_loss) AS AverageDailyIncrease,
            MAX(daily_profit_loss) AS MaxDailyAddition,
            MIN(daily_profit_loss) AS MinDailyAddition
        FROM (
            SELECT
                ToDateTime(value_timestamp, 'yyyy-MM-dd') AS val_date,
                SUM(asset_market_value) AS asset_market_value_today,
                (SUM(asset_market_value - asset_cost)) AS daily_profit_loss
            FROM asset
            GROUP BY ToDateTime(value_timestamp, 'yyyy-MM-dd')
        ) AS daily_data;
        ''')
    et = time.time() - st
    if i > 10:
        avg_query_time.append(et)
print(f'Portfolio Metric Collections : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Portfolio Metric Collections : Max query execution time: {max(avg_query_time)}')
print(f'Portfolio Metric Collections : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Portfolio Metric Collections",sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(110):
    st = time.time()
    curs.execute('''
        SET maxRowsInJoin = 40000000;
        SET timeoutMs = 40000000;                   
        SELECT
            SumCapital / TotalRiskAdjustedValue AS CalculatedValue
        FROM (
            SELECT
                SUM(CASE
                    WHEN asset_class IN ('Stocks', 'Gold Bonds')
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
    if i > 10:
        avg_query_time.append(et)
print(f'Tier1 Capital Ratio : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Tier1 Capital Ratio : Max query execution time: {max(avg_query_time)}')
print(f'Tier1 Capital Ratio : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Tier1 Capital Ratio", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])


avg_query_time = []
for i in range(110):
    st = time.time()
    curs.execute('''
        SET maxRowsInJoin = 40000000;
        SET timeoutMs = 40000000;                   
        SELECT 
    a.asset_name AS asset_name_a, 
    b.asset_name AS asset_name_b, 
    (COUNT(*) * SUM(CAST(a.asset_market_value/10000 AS BIGINT) * CAST(b.asset_market_value/10000 AS BIGINT)) - SUM(CAST(a.asset_market_value/10000 AS BIGINT)) * SUM(CAST(b.asset_market_value/10000 AS BIGINT))) /
    (SQRT((COUNT(*) * SUM(CAST(a.asset_market_value/10000 AS BIGINT) * CAST(a.asset_market_value/10000 AS BIGINT)) - SUM(CAST(a.asset_market_value/10000 AS BIGINT)) * SUM(CAST(a.asset_market_value/10000 AS BIGINT))) *
          (COUNT(*) * SUM(CAST(b.asset_market_value/10000 AS BIGINT) * CAST(b.asset_market_value/10000 AS BIGINT)) - SUM(CAST(b.asset_market_value/10000 AS BIGINT)) * SUM(CAST(b.asset_market_value/10000 AS BIGINT)))))
    AS correlation
FROM 
    (SELECT 
       asset_name, asset_market_value, value_timestamp,
    ROW_NUMBER() OVER w AS rn
     FROM 
         asset
     WHERE 
         asset_name IN ('AAPL', 'GOOGL')
    GROUP BY "asset_name", value_timestamp , "asset_market_value"
    WINDOW w AS (PARTITION BY asset_name ORDER BY value_timestamp ASC)
    ) a
JOIN 
    (SELECT 
        asset_name, asset_market_value, value_timestamp,
    ROW_NUMBER() OVER w AS rn
     FROM 
         asset
     WHERE 
         asset_name IN ('AAPL', 'GOOGL')
    GROUP BY "asset_name", value_timestamp, asset_market_value
    WINDOW w AS (PARTITION BY asset_name ORDER BY value_timestamp  ASC)
    ) b ON a.rn = b.rn AND a.asset_name <> b.asset_name
GROUP BY 
    a.asset_name, b.asset_name
    ''')
    et = time.time() - st
    if i > 10:
        avg_query_time.append(et)
print(f'Time series analysis : Avg query execution time : {sum(avg_query_time)/len(avg_query_time)}')
print(f'Time series analysis : Max query execution time: {max(avg_query_time)}')
print(f'Time series analysis : Min query execution time: {min(avg_query_time)}')
csvstore.append(["Time series analysis", sum(avg_query_time)/len(avg_query_time), max(avg_query_time), min(avg_query_time)])

avg_query_time = []
for i in range(110):
    st = time.time()
    curs.execute('''
        SET timeoutMs = 40000000;         
        SELECT transaction_category,
        SUM(CASE WHEN transaction_confirmed = 1 THEN 1 ELSE 0 END) AS confirmed_count,
        COUNT(*) AS total_count,
        SUM(CASE WHEN transaction_confirmed = 1 THEN 1 ELSE 0 END) / COUNT(*) AS confirmation_rate
        FROM transactions
        GROUP BY transaction_category
        ORDER BY confirmation_rate DESC;
    ''')
    et = time.time() - st
    if i > 10:
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
