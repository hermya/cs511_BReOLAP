# Future work: mount the directory that contains connection jar files to debezium's kafka/libs
# There are a few steps to network debezium_connect to clickhouse.
# Step 1 > run clickhouse docker-compose and ensure that it is running
# Step 2 > run the following command
sudo docker network ls
# You'll get an output like the following:
NETWORK ID     NAME                                 DRIVER    SCOPE
b77e87f6f2bd   bridge                               bridge    local
0117b424ea67   clickhouse-multinode-setup_default   bridge    local
2514d4f2e477   host                                 host      local
a158032adfdb   none                                 null      local
# Remember to use the cickhouse-multinode-setup_default later
# Step 3 > run the generic kafka setup docker-compose and ensure that is running
# Step 4 > In order to network the debezium connect to clickouse master, run the following command
sudo docker network connect clickhouse-multinode-setup_default generic-kafka-setup_debezium_1
# This allows debezium connect to network with generic-kafka-setup & clickhouse-multinode-setup containers
# Then copy the clickhouse jar file to debezium_connect
sudo docker cp clickhouse-jdbc-0.5.0.jar  generic-kafka-setup_debezium_1:/kafka/libs/
# restart generic-kafka-setup_debezium_1 and run this script to create sink connector
curl -X POST --location 'http://localhost:8087/connectors' --header 'Content-Type: application/json' --header 'Accept: application/json' --data @sink-connector.json
# In order to delete this sink connetor later, use this command
# curl -X DELETE http://localhost:8087/connectors/clickhouse-connect