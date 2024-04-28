wget https://github.com/StarRocks/starrocks-connector-for-kafka/releases/download/v1.0.3/starrocks-kafka-connector-1.0.3.tar.gz
mkdir -p assets
mv starrocks-kafka-connector-1.0.3.tar.gz assets/
cd assets
tar -xvzf starrocks-kafka-connector-1.0.3.tar.gz
cd ..
rm assets/starrocks-kafka-connector-1.0.3.tar.gz