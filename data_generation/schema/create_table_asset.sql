CREATE TABLE Assets (
    asset_id INT AUTO_INCREMENT PRIMARY KEY,
    asset_uuid UUID,
    asset_name VARCHAR(255) NOT NULL,
    asset_class ENUM('Crypto', 'Stocks', 'ETFs', 'NFTs', 'Gold Bonds', 'Options', 'Futures', 'Real-Estate') NOT NULL,
    asset_cost DECIMAL(15, 2) NOT NULL,
    asset_market_value DECIMAL(15, 2),
    asset_quantity DECIMAL(15, 2),
    liquidity_rating float,
    asset_owner UUID,
    portfolio_manager UUID,
    value_timestamp long
);