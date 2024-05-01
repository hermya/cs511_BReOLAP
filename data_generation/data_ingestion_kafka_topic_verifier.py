import time
import os

csv_rows = []

def get_kafdrop_api(topic_name):
    host = 'localhost'
    return 'http://'+host+':9500/topic/' + topic_name + '/messages?partition=0&offset=0&count=1&keyFormat=DEFAULT&format=DEFAULT'

try:
    while True:
        os.system(" ".join(['curl', '-s', '-o', 'asset_topic.txt', '-X', 'GET', get_kafdrop_api('asset_topic')]))
        os.system(" ".join(['curl', '-s', '-o', 'liabilities_topic.txt', '-X', 'GET', get_kafdrop_api('liabilities_topic')]))
        os.system(" ".join(['curl', '-s', '-o', 'risk_topic.txt', '-X', 'GET', get_kafdrop_api('risk_topic')]))
        os.system(" ".join(['curl', '-s', '-o', 'transactions_topic.txt', '-X', 'GET', get_kafdrop_api('transactions_topic')]))

        timestamp = time.time_ns()
        a_count = os.popen(" ".join(['cat', 'asset_topic.txt', '|', 'grep', '-oP', """'(?<=partitionSize"\>).*?(?=\<)'"""])).read().strip()
        l_count = os.popen(" ".join(['cat', 'liabilities_topic.txt', '|', 'grep', '-oP', """'(?<=partitionSize"\>).*?(?=\<)'"""])).read().strip()
        r_count = os.popen(" ".join(['cat', 'risk_topic.txt', '|', 'grep', '-oP', """'(?<=partitionSize"\>).*?(?=\<)'"""])).read().strip()
        t_count = os.popen(" ".join(['cat', 'transactions_topic.txt', '|', 'grep', '-oP', """'(?<=partitionSize"\>).*?(?=\<)'"""])).read().strip()
        csv_row = [str(timestamp), str(a_count), str(r_count), str(l_count), str(t_count)]
        if (a_count and r_count and r_count and t_count):
            print(csv_row)
            csv_rows.append(",".join(csv_row))
        else:
            print("Problematic input", csv_row)
        time.sleep(1)

except KeyboardInterrupt:
    with open('ingestion_result.csv', 'w') as file:
        file.write("\n".join(csv_rows))