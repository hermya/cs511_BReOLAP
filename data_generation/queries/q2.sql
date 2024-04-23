--Liquidity Coverage Ratio

SELECT
    (SELECT SUM(asset_market_value * asset_quantity)
     FROM assets
     WHERE asset_class IN ('Stocks', 'Gold Bonds')) /
    (SELECT SUM(amount)
     FROM transactions
     WHERE due_date BETWEEN CURRENT_DATE AND DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY)
       AND transaction_type IN ('Payment', 'Withdrawal', 'LoanRepayment')
       AND confirmed = TRUE) AS LiquidityCoverageRatio;
