import clickhouse_connect

client = clickhouse_connect.get_client(host='192.168.0.111',
                                       user='default',
                                       connect_timeout=15,
                                       database='default',
                                       settings={'distributed_ddl_task_timeout':300})


# client.command('CREATE TABLE test_command (col_1 String, col_2 DateTime) Engine MergeTree ORDER BY tuple()')
for i in range(1000):
    client.command('INSERT INTO test_command (col_1, col_2) VALUES (%s, %s)', 
              ('value_for_col_1', '2024-04-23 13:10:00'))

result = client.command('SELECT count() FROM test_command')
print(result) 