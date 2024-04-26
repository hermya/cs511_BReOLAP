SELECT category,
       SUM(CASE WHEN confirmed THEN 1 ELSE 0 END) AS confirmed_count,
       COUNT(*) AS total_count,
       SUM(CASE WHEN confirmed THEN 1 ELSE 0 END) / COUNT(*)::DECIMAL AS confirmation_rate
FROM Transactions
GROUP BY category
ORDER BY confirmation_rate DESC;