from starrocks import Connection

# Replace with your connection details
conn = Connection(host='localhost', port=9030, user='root', password='password')

# Execute a SQL query
sql = "SELECT * FROM my_table"
cursor = conn.cursor()
cursor.execute(sql)

# Fetch results
results = cursor.fetchall()

# Process results
for row in results:
    print(row)

# Close connection
conn.close()
