from pydruid.db import connect
from time import time
# Connect to your Druid cluster
conn = connect(host='192.168.111', port=8888, path='/druid/v2/sql/')

# Create a cursor object
cursor = conn.cursor()

# Define your Druid SQL query
druid_query = """
SELECT *
FROM wikipedia
LIMIT 10000
"""

# Execute the query
start = time()
cursor.execute(druid_query)

# Fetch results (assuming pandas is installed)
data = cursor.fetchall()
print(time()-start)
# Process the data (data is now a Pandas DataFrame)
# ...
print(len(data))
# Close the connection
conn.close()
