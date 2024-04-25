from confluent_kafka import Producer
import json
import requests
import random
import uuid
import time
from datetime import datetime, timedelta
import threading
import sys

bootstrap_servers = "localhost:29092"
publish_batch = int(sys.argv[1])

producer = Producer({"bootstrap.servers": bootstrap_servers})

def split_into_batches(array, batch_size):
    return [array[i:i+batch_size] for i in range(0, len(array), batch_size)]

def calculate_time_interval(rows_per_minute):
    batches_per_minute = rows_per_minute/publish_batch
    time_interval = 60/batches_per_minute
    return time_interval



def publish_data(data, topic_name, time_interval):
    data_batches = split_into_batches(data, publish_batch)
    for batch in data_batches:
        push_to_kafka(batch, topic_name)
        print("Sleeping for " + str(time_interval) + " seconds")
        time.sleep(time_interval)

def push_to_kafka(data, topic_name):
    for message in data:
        producer.produce(topic_name, json.dumps(message).encode("utf-8"))
        producer.poll(0)
    producer.flush()
    print("Completed publishing " + str(len(data)) + " records onto topic: " + topic_name)
    
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, delta.seconds)
    random_date = start_date + timedelta(seconds = random_seconds)
    return random_date

# Define asset types and liquidity ratings
asset_classes = ["Crypto","Cash", "Stocks", "ETFs", "NFTs", "Gold Bonds", "Bonds", "Options", "Futures", "Real-Estate"]
liquidity_ratings = ["High", "Medium", "Low"]
transaction_types = ["Inflow","Outflow"]

#This will generate asset and asset risk data
def generate_asset_data(asset_index, num_rows, rows_per_minute):
    asset_array = []
    risk_array = []
    for i in range(num_rows):
        asset_id = (i+1) + asset_index
        asset_uuid = str(uuid.uuid4())
        asset_class = random.choice(asset_classes)
        asset_cost = random.randint(100, 10000000000)
        liquidity_rating = random.choice(liquidity_ratings)
        if asset_class in ["Crypto", "Stocks","ETFs","Options","Futures"]:
            asset_market_value = asset_cost + asset_cost * (random.randint(-150,200)/100)
        else:
            asset_market_value = asset_cost + asset_cost * (random.randint(-50,100)/100)
        asset_quantity = random.randint(10,1000)
        json_object = {
            "asset_id":asset_id,
            "asset_uuid":asset_uuid,
            "asset_class":asset_class,
            "asset_cost":asset_cost,
            "asset_market_value":asset_market_value,
            "asset_quantity":asset_quantity,
            "liquidity_rating":liquidity_rating,
            "asset_owner": str(uuid.uuid4()),
            "portfolio_manager": str(uuid.uuid4()),
            "value_timestamp": str(time.time())
        }
        asset_array.append(json_object)
        # push_to_kafka(json_object)

        risk_uuid = str(uuid.uuid4())
        risk_factor = random.randint(0,100)/100

        json_object_risk = {
            "asset_uuid":asset_uuid,
            "risk_uuid": risk_uuid,
            "risk_rating": risk_factor
        }

        risk_array.append(json_object_risk)

    time_interval = calculate_time_interval(rows_per_minute)    
    #Creating two different threads to push asset and risk data onto kafka simultaneously
    t4 = threading.Thread(target = publish_data, args = (asset_array, "asset-topic", time_interval))
    t5 = threading.Thread(target = publish_data, args = (risk_array, "risk-topic", time_interval))
    t4.start()
    t5.start()

    t4.join()
    t5.join()
    return asset_array, risk_array, (num_rows + asset_index)

transaction_types = ["Deposit", "Payment", "Withdrawal", "InterestPayment", "LoanRepayment", "Other"]
transaction_categories = ["Operational", "Financial", "ClientWithdrawal", "Contingent", "Regulatory"]

def generate_transactions_data(transaction_index, num_rows, rows_per_minute):
    transaction_array = []
    for i in range(num_rows):
        transaction_id = i+1 + transaction_index
        transaction_uuid = str(uuid.uuid4())
        transaction_date = time.time()
        transaction_amount = random.randint(100, 10000000)
        transaction_type = random.choice(transaction_types)
        transaction_due_date = transaction_date + random.randint(100,10000)
        transaction_category = random.choice(transaction_categories)
        asset_linked = str(uuid.uuid4())
        created_at = time.time()
        transaction_confirmed = random.randint(0,1)
        json_object = {
            "transaction_id":transaction_id,
            "transaction_uuid":transaction_uuid,
            "transaction_date":str(transaction_date),
            "transaction_amount":transaction_amount,
            "transaction_type": transaction_type,
            "transaction_due_date": transaction_due_date,
            "transaction_category": transaction_category,
            "transaction_confirmed": transaction_confirmed,
            "asset_linked": asset_linked,
            "created_at": str(created_at)   
        }
        transaction_array.append(json_object)
    time_interval = calculate_time_interval(rows_per_minute)
    publish_data(transaction_array, "transactions-topic", time_interval)
    return transaction_array, (transaction_index + num_rows)

statuses = ["Active","Paid Off", "Defaulted"]

def generate_liabilities_data(liabilities_index, num_rows, rows_per_minute):

    liabilities_array = []
    for i in range(num_rows):
        liability_id = i+1 + liabilities_index
        bank_id = str(uuid.uuid4())
        liability_amount = random.randint(100, 10000000)
        interest_rate = random.uniform(6,12)
        start_date = str(time.time() - random.randint(10000, 50000))
        maturity_date = str(time.time() + random.randint(10000, 50000))
        counterparty_uuid = str(uuid.uuid4())
        status = random.choice(statuses)
        created_at = str(time.time())
        created_by = str(uuid.uuid4())
        json_object = {
            "liability_id": liability_id,
            "bank_id": bank_id,
            "liability_amount": liability_amount,
            "interest_rate": interest_rate,
            "start_date": start_date,
            "maturity_date": maturity_date,
            "counterparty_uuid": counterparty_uuid,
            "status": status,
            "created_at": created_at,
            "created_by": created_by
        }
        liabilities_array.append(json_object)
    time_interval = calculate_time_interval(rows_per_minute)
    publish_data(liabilities_array, "liabilities-topic", time_interval)
    return liabilities_array, (liabilities_index + num_rows)
'''
CLI Arguments - 
1 -> Publish batch
2 -> asset data num records
3 -> asset data num records per minute
4 -> transactions data records
5 -> transcations data records per minute
6 -> liabilities data records
7 -> liabilities data records per minute
'''
print("Printing arguments")
print(sys.argv)
#print("Printing arguments " + str(sys.argv[0]) + " " + str(sys.argv[1]) + " " + str(sys.argv[2]) + " " + str(sys.argv[3]) + " " + str(sys.argv[4]) + " " + str(sys.argv[5]))

t1 = threading.Thread(target = generate_asset_data, args = (0, int(sys.argv[2]), int(sys.argv[3])))
t2 = threading.Thread(target = generate_transactions_data, args = (0, int(sys.argv[4]), int(sys.argv[5])))
t3 = threading.Thread(target = generate_liabilities_data, args = (0, int(sys.argv[6]), int(sys.argv[7])))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()