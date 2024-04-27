SELECT a.asset_name, a.asset_class, c.counterparty_name, SUM(t.amount)
FROM transactions t
JOIN Counterparties c ON t.counterparty_uuid = c.counterparty_uuid
JOIN Asset a ON t.asset_linked = a.asset_uuid
WHERE t.transaction_type IN ('Payment','Withdrawal','InterestPayment','LoanRepayment')