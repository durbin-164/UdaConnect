https://rmoff.net/2018/08/02/kafka-listeners-explained/

wget https://dlcdn.apache.org/kafka/3.0.0/kafka_2.13-3.0.0.tgz --no-check-certificate

bin/kafka-topics.sh --create --topic location_connection_response --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092

bin/kafka-topics.sh --create --topic location_connection_request --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092

bin/kafka-console-consumer.sh --topic location_connection_request --from-beginning --bootstrap-server localhost:9092



bin/kafka-topics.sh --create --topic person_location_visits --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092

bin/kafka-console-consumer.sh --topic person_location_visits --from-beginning --bootstrap-server localhost:9092


