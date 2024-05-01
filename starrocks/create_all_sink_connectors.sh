curl -i http://172.11.0.8:8083/connectors -H "Content-Type: application/json" -X POST -d @connectors/asset_sink_connector.json
curl -i http://172.11.0.8:8083/connectors -H "Content-Type: application/json" -X POST -d @connectors/transactions_connector.json
curl -i http://172.11.0.8:8083/connectors -H "Content-Type: application/json" -X POST -d @connectors/liabilities_connector.json
curl -i http://172.11.0.8:8083/connectors -H "Content-Type: application/json" -X POST -d @connectors/risk_sink_connector.json
curl -i http://172.11.0.8:8083/connectors -H "Content-Type: application/json" -X POST -d @connectors/counterparty_connector.json
