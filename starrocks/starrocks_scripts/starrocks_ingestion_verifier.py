from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy.sql.expression import select, text
import time
import csv

engine = create_engine('starrocks://kafka:12345@192.168.0.111:9030/BReOLAP')
curs = engine.connect()

# Execute a SQL query
csvstore = []
try:
    while True:
        result = curs.execute('''
            SELECT
            (SELECT COUNT(*) FROM asset_topic) AS asset_count,
            (SELECT COUNT(*) FROM risk_topic) AS asset_risk_count,
            (SELECT COUNT(*) FROM liabilities_topic) AS liabilities_count,
            (SELECT COUNT(*) FROM transactions_topic) AS transactions_count;
        ''')

        # Create a record with timestamp
        current_time = time.time_ns()
        for r in result:
            record = {'timestamp': current_time,\
                    'asset_count': r.asset_count,\
                    'asset_risk_count': r.asset_risk_count,\
                    'liabilities_count': r.liabilities_count,\
                    'transactions_count': r.transactions_count}
        
        # Append the record to csvstore
        csvstore.append(record)
        
        print(record)
        time.sleep(1)

except KeyboardInterrupt:
    print("Monitoring stopped by user.")

keys = csvstore[0].keys()

with open('starrocks_ingestion_values.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(csvstore)
