### Steps to setup kafka sink connector
1. First create topic in kafka and table in StarRocks FE mysql
2. create a user in StarRocks FE mysql and give it access:
CREATE USER kafka@'%' IDENTIFIED BY '12345' DEFAULT ROLE 'admin';
GRANT ALL ON DATABASE BREOLAP TO kafka@'%';
GRANT ALL ON  BREOLAP.* TO kafka@'%';

Then follow below steps for creating connector:
1. Download and extract sink connector jar files
wget https://github.com/StarRocks/starrocks-connector-for-kafka/releases/download/v1.0.3/starrocks-kafka-connector-1.0.3.tar.gz
tar -xzvf starrocks-kafka-connector-1.0.3.tar.gz

2. copy the jar folder to debezium container in kafka/connect folder

3. make the following change in config/connect-distributed.properties in debezium container
rest.host.name=172.11.0.8 -> rest.host.name=localhost

4. restart debezium container

5. run command in your host machine to create connector:
curl -i http://172.11.0.8:8083/connectors -H "Content-Type: application/json" -X POST -d @connectors/any_sink_connector.json



# setup guide
https://docs.starrocks.io/docs/loading/Kafka-connector-starrocks/

# 3fe 3be setup link [not verified for our purpose by 04/25/2024]
https://github.com/StarRocks/demo/blob/master/deploy/docker-compose/docker-compose-3BE.yml