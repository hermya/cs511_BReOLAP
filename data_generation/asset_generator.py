# Generate random rows

generate_asset_data(num_rows):

    asset_types = ["Crypto", "Stocks", "ETFs", "NFTs", "Gold Bonds", "Options", "Futures", "Real-Estate"];
    stock_tickers/futures/options = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NFLX', 'NVDA', 'INTC', 'AMD']
    scenarios = ['inflationary_pressure','recession','bull_market','geopolitical_crisis','technology_disruption','interest_rate_shock_scenario']

    num_rows = 1000  # Number of rows to generate
    assets_array = [];
    risk_array = [];
    for i in range(num_rows):
        #Auto-incremented id
        asset_id = i+1;
        asset_uuid = str(uuid.uuid4());
        asset_type = random.choice(asset_types)
        amount = random.randint(100, 10000000)
        liquidity_rating = random.choice(liquidity_ratings)
        asset_market_value = amount * (random.randint(-50,100)/100)
        asset_owner = str(uuid.uuid4())
        portfolio_manager = str(uuid.uuid4())
        asset_quantity = random.randint(0,1000)
        scenario = random.choice(scenarios)
        asset_json_object = {
            "asset_id":asset_id,
            "asset_uuid":asset_uuid,
            "asset_class":asset_type,
            "asset_cost": amount,
            "asset_market_value":amount,
            "liquidity_rating":liquidity_rating,
            "asset_market_value":asset_market_value,
            "asset_quantity": asset_quantity,
            "asset_owner": asset_owner,
            "portfolio_manager": portfolio_manager,
            "scenario": scenario
        }

        print("Printing asset_json_object " + asset_json_object);

        risk_uuid = str(uuid.uuid4());
        risk_factor = random.randint(0,100)/100;

        json_object_risk = {
            "asset_uuid":asset_uuid,
            "risk_uuid": risk_uuid,
            "risk_rating": risk_factor
        }   

        print("Printing json_object_risk " + json_object_risk);

        risk_array.append(json_object_risk);
        assets_array.append(json_object);

generate_asset_data(10);