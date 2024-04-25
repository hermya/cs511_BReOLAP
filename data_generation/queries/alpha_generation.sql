SELECT t.symbol,
       c.counterparty_name,
       SUM(t.amount) AS total_transaction_volume
FROM Transactions t
JOIN Counterparties c ON t.counterparty_uuid = c.counterparty_uuid
WHERE t.transaction_type IN ('Payment', 'Withdrawal', 'InterestPayment', 'LoanRepayment') -- Consider only transactions related to trading
GROUP BY t.symbol, c.counterparty_name
ORDER BY total_transaction_volume DESC;