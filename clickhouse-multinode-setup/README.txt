# Copy the clickhouse jar file to debezium_connect
sudo docker cp clickhouse-jdbc-0.5.0.jar  generic-kafka-setup_debezium_1:/kafka/libs/
# restart debezium and run this script to create sink connector
curl -X POST --location 'http://localhost:8087/connectors' --header 'Content-Type: application/json' --header 'Accept: application/json' --data @sink-connector.json
# In order to delete this sink connetor later, use this command
# curl -X DELETE http://localhost:8087/connectors/clickhouse-connect

To create a Prometheus data source in Grafana:

    Click on the "cogwheel" in the sidebar to open the Configuration menu.
    Click on "Data Sources".
    Click on "Add data source".
    Select "Prometheus" as the type.
    Set the appropriate Prometheus server URL (for example, http://<ip-address-of-prometheus>:9090/)
    Adjust other data source settings as desired (for example, choosing the right Access method).
    Click "Save & Test" to save the new data source.

    To begin with, use this metrics: 
    ClickHouseProfileEvents_InsertQueryTimeMicroseconds
    ClickHouseProfileEvents_SelectQueryTimeMicroseconds
