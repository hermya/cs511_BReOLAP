create database BReOLAP;

CREATE USER kafka@'%' IDENTIFIED BY '12345' DEFAULT ROLE 'admin';
GRANT ALL ON DATABASE BReOLAP TO kafka@'%';
GRANT ALL ON  BReOLAP.* TO kafka@'%';

show roles;

USE BReOLAP;

CREATE TABLE asset_topic (     
    `asset_id` int,
	`asset_uuid` varchar(100),
	`asset_class` varchar(100),
	`asset_name` varchar(100),
	`asset_cost` DECIMAL(20, 2),
	`asset_market_value` DECIMAL(20, 2),
	`asset_quantity` int,
	`liquidity_rating` varchar(100),
	`asset_owner` varchar(100),
	`portfolio_manager` varchar(100),
	`value_timestamp` DECIMAL(15, 2)
) 	ENGINE=OLAP 
	DISTRIBUTED BY HASH (asset_uuid) 
	BUCKETS 1 PROPERTIES ("replication_num" = "1",     "in_memory"="false",     "storage_format"="DEFAULT");

CREATE TABLE counterparties_topic
(
    `counterparty_id` int,
	`counterparty_uuid` varchar(100),
	`counterparty_name` varchar(100),
	`counterparty_type` varchar(100),
	`created_at` DECIMAL(15, 2)
) ENGINE=OLAP 
DISTRIBUTED BY HASH (counterparty_uuid) 
BUCKETS 1 PROPERTIES ("replication_num" = "1",     "in_memory"="false",     "storage_format"="DEFAULT");

CREATE TABLE liabilities_topic
(
    `liability_id` int,
	`bank_id` varchar(100),
	`liability_amount`  DECIMAL(20, 2),
	`interest_rate`  DECIMAL(20, 2),
	`start_date`  DECIMAL(20, 2),
	`maturity_date`  DECIMAL(20, 2),
	`counterparty_uuid` varchar(100),
	`status` varchar(100),
	`created_at`  DECIMAL(20, 2),
	`created_by` varchar(100)
) ENGINE=OLAP 
DISTRIBUTED BY HASH (liability_id) 
BUCKETS 1 PROPERTIES ("replication_num" = "1",     "in_memory"="false",     "storage_format"="DEFAULT");

CREATE TABLE risk_topic
(
    `asset_uuid` varchar(100),
    `risk_uuid` varchar(100),
    `risk_rating` DECIMAL(20, 6)
) ENGINE=OLAP 
DISTRIBUTED BY HASH (risk_uuid) 
BUCKETS 1 PROPERTIES ("replication_num" = "1",     "in_memory"="false",     "storage_format"="DEFAULT");

CREATE TABLE transactions_topic
(
    `transaction_id` int,
	`transaction_uuid` varchar(100),
	`transaction_date` DECIMAL(15, 2),
	`transaction_amount` DECIMAL(20, 6),
	`transaction_type` varchar(100),
	`transaction_due_date` DECIMAL(15, 2),
	`transaction_category` varchar(100),
	`transaction_confirmed` int,
	`asset_linked` varchar(100),
	`counterparty_uuid` varchar(100),	
	`created_at` DECIMAL(15, 2)
) ENGINE=OLAP 
DISTRIBUTED BY HASH (transaction_uuid) 
BUCKETS 1 PROPERTIES ("replication_num" = "1",     "in_memory"="false",     "storage_format"="DEFAULT");
