import random
import uuid
import json
import time
from datetime import datetime, timedelta

def random_date(start_date, end_date):
    delta = end_date - start_date;

    random_seconds = random.randint(0, delta.seconds);

    random_date = start_date + timedelta(seconds = random_seconds);

    return random_date;

# Define asset types and liquidity ratings
asset_types = ["Cash", "Government", "Central Bank", "Corporate"];
liquidity_ratings = ["High", "Medium", "Low"];
transaction_types = ["Inflow","Outflow"];


# Generate random rows
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
    market_value = amount * (random.randint(0,100)/100);  # For simplicity, assuming market value equals amount
    json_object = {
        "asset_id":asset_id,
        "asset_uuid":asset_uuid,
        "asset_type":asset_type,
        "amount":amount,
        "liquidity_rating":liquidity_rating,
        "market_value":market_value
    }

    risk_uuid = str(uuid.uuid4());
    risk_factor = random.randint(0,100)/100;

    json_object_risk = {
        "asset_uuid":asset_uuid,
        "risk_uuid": risk_uuid,
        "risk_rating": risk_factor
    }   

    risk_array.append(json_object_risk);
    assets_array.append(json_object);


transaction_array = [];
for i in range(num_rows):
    transaction_id = i+1;
    transaction_uuid = str(uuid.uuid4());
    transaction_flip = random.randint(0,2);
    transaction_type = "";
    #print("Transaction flip is " + str(transaction_flip));
    if(int(transaction_flip) < 2):
        transaction_type = "Outflow";
    else:
        transaction_type = "Inflow";

    #print("Transaction type is " + transaction_type);
    #time.sleep(1);
    amount = random.randint(100, 10000000);
    transaction_date = random_date(datetime(2024,1,1), datetime(2024,3,22));
    created_at = time.time();
    json_object = {
        "transaction_id":transaction_id,
        "transaction_uuid":transaction_uuid,
        "transaction_type":transaction_type,
        "amount":amount,
        "transaction_date":str(transaction_date),
        "created_at":str(created_at)
    }

    transaction_array.append(json_object);

capital_array = [];
for i in range(num_rows):
    capital_id = i+1;


#print("Printing liquidity array");
json_string = json.dumps(assets_array, indent = 4);
#print(json_string);

time.sleep(3);

#print("Printing transaction array");
json_transaction_string = json.dumps(transaction_array, indent = 4);
#print(json_transaction_string);

print("Printing risk array");
json_risk_string = json.dumps(risk_array, indent = 4);
print(json_risk_string);