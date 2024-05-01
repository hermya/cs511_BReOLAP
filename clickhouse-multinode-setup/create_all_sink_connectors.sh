curl -i http://localhost:8087/connectors -H "Content-Type: application/json" -X POST -d @connectors/asset_connector.json
curl -i http://localhost:8087/connectors -H "Content-Type: application/json" -X POST -d @connectors/transactions_connector.json
curl -i http://localhost:8087/connectors -H "Content-Type: application/json" -X POST -d @connectors/liabilities_connector.json
curl -i http://localhost:8087/connectors -H "Content-Type: application/json" -X POST -d @connectors/risk_connector.json
curl -i http://localhost:8087/connectors -H "Content-Type: application/json" -X POST -d @connectors/counterparty_connector.json
