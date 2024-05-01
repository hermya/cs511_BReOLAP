from pydruid.db import connect
import time
import csv

query_context = {
    "enableWindowing": "true",
    "maxSubqueryRows": 5000000
}

# Connect to your Druid cluster
conn = connect(host='localhost', port=8888, path='/druid/v2/sql/', context=query_context)

# Create a cursor object
curs = conn.cursor()
csvstore = []

try:
    while True:
        curs.execute('''
            SELECT
            (SELECT COUNT(*) FROM "asset_topic") AS asset_count,
            (SELECT COUNT(*) FROM "risk_topic") AS asset_risk_count,
            (SELECT COUNT(*) FROM "liabilities_topic") AS liabilities_count,
            (SELECT COUNT(*) FROM "transactions_topic") AS transactions_count
        ''')

        # Fetch the result
        result = curs.fetchone()

        # Create a record with timestamp
        current_time = time.time_ns()
        record = {'timestamp': current_time, 'asset_count': result[0], 'asset_risk_count': result[1], 'liabilities_count': result[2], 'transactions_count': result[3]}
        
        # Append the record to csvstore
        csvstore.append(record)

        print(record)
        time.sleep(1)

except KeyboardInterrupt:
    print("Monitoring stopped by user.")

finally:
    # Close the database connection
    conn.close()

keys = csvstore[0].keys()

with open('druid_ingestion_values.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(csvstore)

