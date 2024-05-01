from pinotdb import connect
import time
import csv
conn = connect(host='localhost', port=8099, path='/query', scheme='http')
curs = conn.cursor()

csvstore = []

try:
    while True:
        curs.execute('''
            SELECT
            (SELECT COUNT(*) FROM asset) AS asset_count,
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
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Monitoring stopped by user.")

finally:
    # Close the database connection
    conn.close()


keys = csvstore[0].keys()

with open('pinot_ingestion_values.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(csvstore)
