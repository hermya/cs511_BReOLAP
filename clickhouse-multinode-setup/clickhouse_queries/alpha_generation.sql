SELECT a.asset_name, a.asset_class, c.counterparty_name, SUM(t.transaction_amount)
FROM transactions_topic t
JOIN counterparties_topic c ON t.counterparty_uuid = c.counterparty_uuid
JOIN asset_topic a ON t.asset_linked = a.asset_uuid
WHERE t.transaction_type IN ('Payment','Withdrawal','InterestPayment','LoanRepayment')
GROUP BY a.asset_name, a.asset_class, c.counterparty_name;


