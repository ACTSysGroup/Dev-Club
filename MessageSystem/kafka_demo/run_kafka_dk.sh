# install python3 kafka
python3 -m pip install avro-python3
python3 -m pip install kafka-python

# run docker container
docker run -d --rm --name zk1 -p 2181:2181 -v /etc/localtime:/etc/localtime zookeeper

docker run -d --rm --name kf1 -p 9092:9092 \
    --link zk1 \
    --env KAFKA_BROKER_ID=0 \
    --env KAFKA_NUM_PARTITIONS=3 \
    --env KAFKA_ZOOKEEPER_CONNECT=zk1:2181 \
    --env KAFKA_ADVERTISED_HOST_NAME=localhost \
    --env KAFKA_ADVERTISED_PORT=9092 \
    --env KAFKA_PORT=9092  \
    --env KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \
    --volume /etc/localtime:/etc/localtime \
    wurstmeister/kafka

