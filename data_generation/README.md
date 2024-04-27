CLI Arguments for the data_generation_script - 
1 -> Publish Batch
2 -> Generation Batch
3 -> Number of Records you want to publish (This will work for all tables)
4 -> The speed at which you want to publish this data (records/min)
5 -> Do you want to publish counterparty data? 1 for yes, 0 for no

Sample - 
python .\data_generation.py 5000(publish batch) 10000(generation batch) 50000(number of records to publish) 2000000(rate in number of record per minute) 1(boolean - publish counterparty data)