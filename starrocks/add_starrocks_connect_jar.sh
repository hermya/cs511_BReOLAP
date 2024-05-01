wget https://github.com/StarRocks/starrocks-connector-for-kafka/releases/download/v1.0.3/starrocks-kafka-connector-1.0.3.tar.gz
mkdir -p assets
sudo mv starrocks-kafka-connector-1.0.3.tar.gz assets/
cd assets
sudo tar -xvzf starrocks-kafka-connector-1.0.3.tar.gz
cd ..
sudo rm assets/starrocks-kafka-connector-1.0.3.tar.gz