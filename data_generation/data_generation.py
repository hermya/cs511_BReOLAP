from confluent_kafka import Producer
import json
import requests
import random
import uuid
import time
from datetime import datetime, timedelta
import threading
import sys

#bootstrap_servers = "192.168.0.111:29092"
bootstrap_servers = "localhost:29092"
publish_batch = int(sys.argv[1])
generation_batch = int(sys.argv[2])

#Credits to Alexandra Zaharia dev blog - https://alexandra-zaharia.github.io/
#Extending python thread class to allow the python thread to return a value
class ReturnValueThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        if self._target is None:
            return  # could alternatively raise an exception, depends on the use case
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)  # properly handle the exception

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result


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
    producer = Producer({"bootstrap.servers": bootstrap_servers})
    try:
        for message in data:
            producer.produce(topic_name, json.dumps(message).encode("utf-8"))
            producer.poll(0)
        producer.flush()
    except Exception as exc:
        print("Exception caught " + str(exc))
    print("Completed publishing " + str(len(data)) + " records onto topic: " + topic_name)
    
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, delta.seconds)
    random_date = start_date + timedelta(seconds = random_seconds)
    return random_date

def generate_counterparty_array():
    counterparty_array = []
    for i in range(30):
        counterparty_array.append(str(uuid.uuid4()))
    return counterparty_array

# Define asset types and liquidity ratings
asset_classes = ["Crypto","Cash", "Stocks", "ETFs", "NFTs", "Gold Bonds", "Options", "Futures", "Real-Estate"]
liquidity_ratings = ["High", "Medium", "Low"]
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "BRK.B", "NVDA", "JPM", "JNJ", "V", "PG", "MA", "HD", "UNH", "DIS", "BAC", "PYPL", "INTC", "CMCSA", "KO", "T", "MRK", "CRM", "NKE"]
cryptocurrencies = ["BTC", "ETH", "XRP", "ADA", "SOL"]
gold_bonds = ["IAU", "GLD", "SGOL", "BAR", "OUNZ"]
transaction_types = ["Inflow","Outflow"]
transaction_types = ["Deposit", "Payment", "Withdrawal", "InterestPayment", "LoanRepayment", "Other"]
transaction_categories = ["Operational", "Financial", "ClientWithdrawal", "Contingent", "Regulatory"]

def resolve_asset_name(asset_class):
    if asset_class == "Crypto":
        return random.choice(cryptocurrencies)
    elif asset_class in ["Stocks", "ETFs", "Options", "Futures"]:
        return random.choice(stocks)
    elif asset_class in ["Gold Bonds"]:
        return random.choice(gold_bonds)
    else:
        return ""    

#Code to generate and publish data on topics - asset, risk and transctions
def generate_and_publish_asset_data(asset_index, num_rows, rows_per_minute):
    asset_array, risk_array, transactions_array = generate_asset_data(asset_index, generation_batch)

    rows_generated = generation_batch
    time_interval = calculate_time_interval(rows_per_minute)
    while rows_generated < num_rows:
        #Creating thread to publish asset data
        asset_publish_thread = threading.Thread(target = publish_data, args = (asset_array, "asset_topic", time_interval))
        #Creating thread to publish risk data
        risk_publish_thread = threading.Thread(target = publish_data, args = (risk_array, "risk_topic", time_interval))
        #Creating a thread to publish transactions data
        transaction_publish_thread = threading.Thread(target = publish_data, args = (transactions_array, "transactions_topic", time_interval))
        #Creating a new ReturnableThread to generate asset and risk data
        data_generation_thread = ReturnValueThread(target = generate_asset_data, args = (rows_generated, generation_batch))

        asset_publish_thread.start()
        risk_publish_thread.start()
        transaction_publish_thread.start()
        data_generation_thread.start()

        asset_publish_thread.join()
        risk_publish_thread.join()    
        transaction_publish_thread.join()
        asset_array, risk_array, transactions_array = data_generation_thread.join()
        
        rows_generated += generation_batch

    #Publishing last data
    asset_publish_thread = threading.Thread(target = publish_data, args = (asset_array, "asset_topic", time_interval))
    risk_publish_thread = threading.Thread(target = publish_data, args = (risk_array, "risk_topic", time_interval))
    transaction_publish_thread = threading.Thread(target = publish_data, args = (transactions_array, "transactions_topic", time_interval))

    asset_publish_thread.start()
    risk_publish_thread.start()
    transaction_publish_thread.start()
    asset_publish_thread.join()
    risk_publish_thread.join()
    transaction_publish_thread.join()

    time_interval = calculate_time_interval(rows_per_minute)

def generate_asset_data(asset_index, num_rows):
    asset_array = []
    risk_array = []
    transaction_array = []
    for i in range(num_rows):
        asset_id = (i+1) + asset_index
        asset_uuid = str(uuid.uuid4())
        asset_class = random.choice(asset_classes)
        asset_name = resolve_asset_name(asset_class)
        asset_cost = random.uniform(100, 10000000000)
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
            "asset_name": asset_name,
            "asset_cost":asset_cost,
            "asset_market_value":asset_market_value,
            "asset_quantity":asset_quantity,
            "liquidity_rating":liquidity_rating,
            "asset_owner": str(uuid.uuid4()),
            "portfolio_manager": str(uuid.uuid4()),
            "value_timestamp":  time.time()
        }
        asset_array.append(json_object)

        risk_uuid = str(uuid.uuid4())
        risk_factor = random.randint(0,100)/100

        json_object_risk = {
            "asset_uuid":asset_uuid,
            "risk_uuid": risk_uuid,
            "risk_rating": risk_factor
        }
        risk_array.append(json_object_risk)

        transaction_id = (i+1) + asset_index
        transaction_uuid = str(uuid.uuid4())
        transaction_date = time.time()
        transaction_amount = random.randint(100, 10000000)
        transaction_type = random.choice(transaction_types)
        transaction_due_date = transaction_date + random.randint(100,10000)
        transaction_category = random.choice(transaction_categories)
        #asset_linked = str(uuid.uuid4())
        created_at = time.time()
        transaction_confirmed = random.randint(0,1)
        json_object_transaction = {
            "transaction_id":transaction_id,
            "transaction_uuid":transaction_uuid,
            "transaction_date":transaction_date,
            "transaction_amount":transaction_amount,
            "transaction_type": transaction_type,
            "transaction_due_date": transaction_due_date,
            "transaction_category": transaction_category,
            "transaction_confirmed": transaction_confirmed,
            "asset_linked": asset_uuid,
            "counterparty_uuid": random.choice(counterparty_array),
            "created_at": created_at   
        }
        transaction_array.append(json_object_transaction)

    print("Generated " + str(len(transaction_array)) + " elements for the transactions table")
    print("Generated " + str(num_rows) + " asset and risk records")
    return asset_array, risk_array, transaction_array

statuses = ["Active","Paid Off", "Defaulted"]

#Code to generate and publish liabilties data
def generate_and_publish_liabilities_data(liabilites_index, num_rows, rows_per_minute):
    liabilties_array = generate_liabilities_data(liabilites_index, generation_batch)

    rows_generated = generation_batch
    time_interval = calculate_time_interval(rows_per_minute)
    while rows_generated < num_rows:
        #Creating thread to publish asset data
        liabilities_publish_thread = threading.Thread(target = publish_data, args = (liabilties_array, "liabilities_topic", time_interval))
        #Creating thread to generate data
        data_generation_thread = ReturnValueThread(target = generate_liabilities_data, args = (rows_generated, generation_batch))

        liabilities_publish_thread.start()
        data_generation_thread.start()

        liabilities_publish_thread.join()    
        liabilties_array = data_generation_thread.join()
        
        rows_generated += generation_batch

    #Publishing last data
    publish_data(liabilties_array, "liabilities_topic", time_interval)

def generate_liabilities_data(liabilities_index, num_rows):

    liabilties_array = []
    for i in range(num_rows):
        liability_id = i+1 + liabilities_index
        bank_id = str(uuid.uuid4())
        liability_amount = random.randint(100, 10000000)
        interest_rate = random.uniform(6,12)
        start_date = time.time() - random.randint(10000, 50000)
        maturity_date = time.time() + random.randint(10000, 50000)
        counterparty_uuid = random.choice(counterparty_array)
        status = random.choice(statuses)
        created_at = time.time()
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
        liabilties_array.append(json_object)
    #print("Printing liabilties object")
    #print(json_object)
    print("Generated " + str(len(liabilties_array)) + " elements for the liabilties table")
    return liabilties_array

counterparties = [
    "Goldman Sachs Group",
    "JPMorgan Chase & Co.",
    "Morgan Stanley",
    "Citigroup Inc.",
    "Bank of America Corporation",
    "Wells Fargo & Company",
    "Barclays PLC",
    "HSBC Holdings PLC",
    "Deutsche Bank AG",
    "Credit Suisse Group AG",
    "UBS Group AG",
    "BNP Paribas SA",
    "Société Générale SA",
    "Nomura Holdings Inc.",
    "Mizuho Financial Group Inc.",
    "The Blackstone Group Inc.",
    "The Carlyle Group Inc.",
    "KKR & Co. Inc.",
    "The Vanguard Group Inc.",
    "The BlackRock Group",
    "State Street Corporation",
    "Northern Trust Corporation",
    "Fidelity Investments",
    "PIMCO (Pacific Investment Management Company LLC)",
    "Franklin Templeton Investments",
    "T. Rowe Price Group",
    "Charles Schwab Corporation",
    "Raymond James Financial Inc.",
    "American Express Company",
    "Discover Financial Services"
]

counterparty_types = ['Individual', 'Institution', 'Company', 'Other']

def generate_and_publish_counterparty_data():
    counterparty_data = []
    counterparty_counter = 0
    for i in range(len(counterparty_array)):
        counterparty_id = i
        counterparty_uuid = counterparty_array[i]
        counterparty_name = counterparties[i]
        counterparty_type = random.choice(counterparty_types)
        created_at = time.time()
        json_object = {
            "counterparty_id": counterparty_id,
            "counterparty_uuid": counterparty_uuid,
            "counterparty_name": counterparty_name,
            "counterparty_type": counterparty_type,
            "created_at": created_at
        }
        counterparty_data.append(json_object)
    publish_data(counterparty_data, "counterparties_topic", 0)
    print("Completed generating " + str(len(counterparty_data)) + " elements for the counterparty table")

'''
CLI Arguments - 
1 -> Publish batch
2 -> asset data num records
3 -> asset data num records per minute
4 -> transactions data records
5 -> transcations data records per minute
6 -> liabilities data records
7 -> liabilities data records per minute
8 -> publish counterparty data
'''
print("Printing arguments")
print(sys.argv)

t1 = threading.Thread(target = generate_and_publish_asset_data, args = (0, int(sys.argv[3]), int(sys.argv[4])))
t2 = threading.Thread(target = generate_and_publish_liabilities_data, args = (0, int(sys.argv[5]), int(sys.argv[6])))
#t3 = threading.Thread(target = generate_and_publish_transactions_data, args = (0, int(sys.argv[7]), int(sys.argv[8])))

counterparty_array = generate_counterparty_array()
print("Pritning generated counterparty uuids array")
#print(counterparty_array)

publish_counterparty_data = int(sys.argv[7])

if publish_counterparty_data == 1:
    generate_and_publish_counterparty_data()


t1.start()
t2.start()

t1.join()
t2.join()