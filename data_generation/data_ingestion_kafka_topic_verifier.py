# from confluent_kafka.admin import AdminClient
# from confluent_kafka import TopicCollection
import time
import os
# # Create a KafkaAdminClient object
# admin = AdminClient({'bootstrap.servers' :'192.168.0.105:29092' })
csv_rows = []
# # Get the topic description
# topics_list = TopicCollection(['asset_topic', 'liabilities_topic', 'risk_topic', 'transactions_topic'])
# while True:

#     topic_description = admin.describe_topics(topics_list)
#     # Get the topic size
#     for topic in topic_description:
#         print(topic_description)
#         print(topic_description[topic])
#         topic_size = topic_description.total_size
#         print(time.time_ns(), topic_description.total_size, topic_description.name)
# # Print the topic size
import subprocess
# 'curl', '-s', '-o', 'tmp.txt', '-X', 'GET', 'http://192.168.0.105:9500/topic/asset_topic/messages?partition=0&offset=0&count=1&keyFormat=DEFAULT&format=DEFAULT'
# 'cat' 'tmp.txt' '|' 'grep' '-oP' '(?<=partitionSize"\>).*?(?=\<)'
try:
    while True:
        os.system(" ".join(['curl', '-s', '-o', 'asset_topic.txt', '-X', 'GET', 'http://192.168.0.105:9500/topic/asset_topic/messages?partition=0&offset=0&count=1&keyFormat=DEFAULT&format=DEFAULT']))
        os.system(" ".join(['curl', '-s', '-o', 'liabilities_topic.txt', '-X', 'GET', 'http://192.168.0.105:9500/topic/liabilities_topic/messages?partition=0&offset=0&count=1&keyFormat=DEFAULT&format=DEFAULT']))
        os.system(" ".join(['curl', '-s', '-o', 'risk_topic.txt', '-X', 'GET', 'http://192.168.0.105:9500/topic/risk_topic/messages?partition=0&offset=0&count=1&keyFormat=DEFAULT&format=DEFAULT']))
        os.system(" ".join(['curl', '-s', '-o', 'transaction_topic.txt', '-X', 'GET', 'http://192.168.0.105:9500/topic/transactions_topic/messages?partition=0&offset=0&count=1&keyFormat=DEFAULT&format=DEFAULT']))

        timestamp = time.time_ns()
        a_count = os.popen(" ".join(['cat', 'asset_topic.txt', '|', 'grep', '-oP', """'(?<=partitionSize"\>).*?(?=\<)'"""])).read().strip()
        l_count = os.popen(" ".join(['cat', 'liabilities_topic.txt', '|', 'grep', '-oP', """'(?<=partitionSize"\>).*?(?=\<)'"""])).read().strip()
        r_count = os.popen(" ".join(['cat', 'risk_topic.txt', '|', 'grep', '-oP', """'(?<=partitionSize"\>).*?(?=\<)'"""])).read().strip()
        t_count = os.popen(" ".join(['cat', 'transaction_topic.txt', '|', 'grep', '-oP', """'(?<=partitionSize"\>).*?(?=\<)'"""])).read().strip()
        print(a_count, l_count, r_count, t_count)
        csv_row = [str(timestamp), str(a_count), str(r_count), str(l_count), str(t_count)]
        csv_rows.append(",".join(csv_row))
        time.sleep(0.5)
except KeyboardInterrupt:
    with open('ingestion_result.csv', 'w') as file:
        file.write("\n".join(csv_rows))