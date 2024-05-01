import clickhouse_connect
import time
import csv

client = clickhouse_connect.get_client(host='localhost',
                                       user='default',
                                       connect_timeout=15,
                                       database='default',
                                       settings={'distributed_ddl_task_timeout':30000})

csvstore = []

#JOIN
try:
    while True:
        result = client.command('''
            SELECT
            (SELECT COUNT(*) FROM assets) AS asset_count,
            (SELECT COUNT(*) FROM asset_risk) AS asset_risk_count,
            (SELECT COUNT(*) FROM liabilities) AS liabilities_count,
            (SELECT COUNT(*) FROM transactions) AS transactions_count;
        ''')

        # Create a record with timestamp
        current_time = time.time_ns()
        record = {'timestamp': current_time, 'asset_count': result[0], 'asset_risk_count': result[1], 'liabilities_count': result[2], 'transactions_count': result[3]}
        
        # Append the record to csvstore
        csvstore.append(record)

        print(record)

except KeyboardInterrupt:
    print("Monitoring stopped by user.")

keys = csvstore[0].keys()

with open('clickhouse_ingestion_values.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(csvstore)




