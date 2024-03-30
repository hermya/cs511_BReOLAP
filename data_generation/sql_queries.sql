Queries - 

1. LCR - Liqudity Coverage Ratio - 

SELECT 
    (a.asset_sum / (t.inflows_sum - t.outflows_sum)) AS liquidity_ratio
FROM 
    (SELECT 
         SUM(amount) AS asset_sum
     FROM 
         Asset
     WHERE 
         liquidity_rating = 'HIGH') AS a,
    (SELECT 
         SUM(CASE WHEN transaction_type = 'Outflow' THEN amount ELSE 0 END) AS outflows_sum,
         SUM(CASE WHEN transaction_type = 'Inflow' THEN amount ELSE 0 END) AS inflows_sum
     FROM 
         Transactions) AS t;
		 
2. Tier1 Capital Ratio

SELECT 
    ((
        SELECT COALESCE(SUM(amount), 0) FROM Common_Equity_Tier1_Capital
    ) + (
        SELECT COALESCE(SUM(amount), 0) FROM Additional_Tier1_Capital
    )) / (
        SELECT COALESCE(SUM(asset_risk * amount), 0)
        FROM Assets a
        JOIN Risk r ON a.asset_id = r.asset_id
    ) AS Tier1_Capital_Ratio;



3. Non Performing Assets Ratio 

SELECT 
    SUM(CASE WHEN market_value < amount THEN amount ELSE 0 END) / SUM(amount) AS Non_Performing_Assets_Ratio
FROM 
    Assets;

4. Cash Ratio 

SELECT 
    SUM(CASE WHEN type = 'Cash' THEN amount ELSE 0 END) / SUM(amount) AS Cash_Ratio
FROM 
    Asset;
