#from confluent_kafka import Producer
#from urllib.parse import urlencode
import json
import requests
import random
import uuid
import time
from datetime import datetime, timedelta
import numpy as np

# Kafka configuration
bootstrap_servers = "localhost:9092"

# Druid ingestion configuration
druid_host = "localhost"
druid_port = 8081
druid_datasource = "my_data_source"
druid_ingestion_path = "/druid/indexer/v1/task"

# Sample data (replace with your actual data)
data = [
    {"timestamp": "2024-03-24T12:00:00Z", "value1": 10, "value2": "hello"},
    {"timestamp": "2024-03-24T12:01:00Z", "value1": 20, "value2": "world"}
]


def split_into_batches(array, batch_size):
    return [array[i:i+batch_size] for i in range(0, len(array), batch_size)]


def push_to_kafka(data, topic_name):
    '''
    print("Publishing the following data");
    print(data);
    time.sleep(10);
    
    
    Pushes data to the specified Kafka topic.
    #print("Publising message " + str(data) + " onto topic " + topic_name);
    
    producer = Producer({"bootstrap.servers": bootstrap_servers})
    for message in data:
        print("Pushing message" + str(message));
        producer.produce(topic_name, json.dumps(message).encode("utf-8"))
        producer.poll(0)
    producer.flush()
    '''


def random_date(start_date, end_date):
    delta = end_date - start_date;

    random_seconds = random.randint(0, delta.seconds);

    random_date = start_date + timedelta(seconds = random_seconds);

    return random_date;

# Define asset types and liquidity ratings
asset_types = ["Cash", "Government", "Central Bank", "Corporate"];
liquidity_ratings = ["High", "Medium", "Low"];
transaction_types = ["Inflow","Outflow"];

def generate_asset_data(asset_index, num_rows):
    # Generate random rows
    liquidity_array = [];
    risk_array = [];
    for i in range(num_rows):
        #Auto-incremented id
        asset_id = (i+1) + asset_index;
        asset_uuid = str(uuid.uuid4());
        asset_type = random.choice(asset_types)
        amount = random.randint(100, 10000000)
        liquidity_rating = random.choice(liquidity_ratings)
        market_value = amount + amount * (random.randint(-100,100)/100);  # For simplicity, assuming market value equals amount
        json_object = {
            "asset_id":asset_id,
            "asset_uuid":asset_uuid,
            "asset_type":asset_type,
            "amount":amount,
            "liquidity_rating":liquidity_rating,
            "market_value":market_value
        }
        liquidity_array.append(json_object);
        # push_to_kafka(json_object)

        risk_uuid = str(uuid.uuid4());
        risk_factor = random.randint(0,100)/100;

        json_object_risk = {
            "asset_uuid":asset_uuid,
            "risk_uuid": risk_uuid,
            "risk_rating": risk_factor
        }

        risk_array.append(json_object_risk);
    return liquidity_array, risk_array, (num_rows + asset_index);

def generate_transactions_data(transaction_index, num_rows):
    transaction_array = [];
    for i in range(num_rows):
        transaction_id = i+1 + transaction_index;
        transaction_uuid = str(uuid.uuid4());
        transaction_flip = random.randint(0,2);
        transaction_type = "";
        if(int(transaction_flip) < 2):
            transaction_type = "Outflow";
        else:
            transaction_type = "Inflow";

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
    return transaction_array, (transaction_index + num_rows)


def generate_capital_data(num_rows_capital):

    common_equity_capital_array = [];
    for i in range(num_rows_capital):
        capital_uuid = str(uuid.uuid4());
        amount = random.randint(100, 10000000);
        json_object = {
            "capital_uuid":capital_uuid,
            "amount":amount
        }

        common_equity_capital_array.append(json_object);

    
    additional_tier_1_capital_array = [];
    for i in range(num_rows_capital):
        capital_uuid = str(uuid.uuid4());
        amount = random.randint(100, 10000000);
        json_object = {
            "capital_uuid":capital_uuid,
            "amount":amount
        }

        additional_tier_1_capital_array.append(json_object);

    return common_equity_capital_array, additional_tier_1_capital_array;
    
#Infinite loop to keep publising data
asset_index_id = 0;
transaction_index_id = 0;
generation_batch = 5000;
batches_per_minute = 10;
publish_batch = 1000;
num_iters = 4;
k = 0;
liquidity_table_data = [];
risk_table_daat = [];
transactions_data = [];
capital_array_one = [];
capital_array_two = [];
time_interval = 60/batches_per_minute;

print("Time interval is " + str(time_interval));

while(k < num_iters):
    for table_to_publish in range(0,3):
        if table_to_publish == 0:
            start_time = time.time();
            liquidity_table_data, risk_table_data, asset_index_id = generate_asset_data(asset_index_id, generation_batch);
            batched_liquidity_list = split_into_batches(liquidity_table_data, publish_batch);
            batched_risk_list = split_into_batches(risk_table_data, publish_batch);
            for i in range (0, len(batched_liquidity_list)):
                push_to_kafka(batched_liquidity_list[i], "liquidity_topic");
                push_to_kafka(batched_risk_list[i], "risk_topic");
                time.sleep(time_interval);
                print("Completed publishing " + str(i*publish_batch) + " records onto asset and risk topics, time taken = " + str(time.time() - start_time));

        elif table_to_publish == 1:
            start_time = time.time();
            transactions_data, transaction_index_id = generate_transactions_data(transaction_index_id, generation_batch);
            batched_transactions_list = split_into_batches(transactions_data, publish_batch);
            for i in range (0, len(batched_transactions_list)):
                push_to_kafka(batched_transactions_list[i], "transactions_topic");
                time.sleep(time_interval);
                print("Completed publising " + str(i*publish_batch) + " records onto transactions topic, time taken = " + str(time.time() - start_time));
        else:
            start_time = time.time();
            capital_array_one, capital_array_two = generate_capital_data(generation_batch);
            batched_capital_list_one = split_into_batches(capital_array_one, publish_batch);
            batched_capital_list_two = split_into_batches(capital_array_two, publish_batch);
            for i in range (0, len(batched_capital_list_one)):
                push_to_kafka(batched_capital_list_one[i],"common_equity_capital");
                push_to_kafka(batched_capital_list_two[i],"additional_equity_capital");
                time.sleep(time_interval);
                print("Completed publishing " + str(i*publish_batch) + " records onto capital topics, time taken = " + str(time.time() - start_time));
    k = k+1;