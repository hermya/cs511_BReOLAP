from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy.sql.expression import select, text
import time
import csv

engine = create_engine('starrocks://kafka:12345@localhost:9030/BReOLAP')
curs = engine.connect()


# Execute a SQL query
csvstore = []
try:
    while True:
        curs.execute('''
            SELECT
            (SELECT COUNT(*) FROM assets) AS asset_count,
            (SELECT COUNT(*) FROM asset_risk) AS asset_risk_count,
            (SELECT COUNT(*) FROM liabilities) AS liabilities_count,
            (SELECT COUNT(*) FROM transactions) AS transactions_count;
        ''')

        # Fetch the result
        result = curs.fetchone()

        # Create a record with timestamp
        current_time = time.time_ns()
        record = {'timestamp': current_time, 'asset_count': result[0], 'asset_risk_count': result[1], 'liabilities_count': result[2], 'transactions_count': result[3]}
        
        # Append the record to csvstore
        csvstore.append(record)
        
        print(record)

except KeyboardInterrupt:
    print("Monitoring stopped by user.")

keys = csvstore[0].keys()

with open('starrocks_ingestion_values.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(csvstore)
