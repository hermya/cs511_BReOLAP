SELECT counterparty_uuid,
COUNT(*) AS transaction_count
FROM transactions_topic
GROUP BY counterparty_uuid
ORDER BY transaction_count DESC
LIMIT 10;