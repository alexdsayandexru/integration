import datetime

from kafka import KafkaProducer, KafkaConsumer


class KafkaService:
    def __init__(self, bootstrap_server_host: str, bootstrap_server_port: str, topic: str):
        self.bootstrap_server_host = bootstrap_server_host
        self.bootstrap_server_port = bootstrap_server_port
        self.topic = topic

    def send_message(self, message: str) -> None:
        producer = KafkaProducer(
            bootstrap_servers=[f'{self.bootstrap_server_host}:{self.bootstrap_server_port}'],
            value_serializer=lambda x: x.encode('utf-8'),
            api_version=(0, 10, 1)
        )
        producer.send(self.topic, message)

    def create_consumer(self):
        consumer = KafkaConsumer(self.topic,
                                 bootstrap_servers=[f'{self.bootstrap_server_host}:{self.bootstrap_server_port}'],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 value_deserializer=lambda x: x.decode('utf-8'),
                                 group_id=f'{self.topic}_group_id'
                                 )
        return consumer


class KafkaInputEventsController:
    def __init__(self, kafka_server_host, kafka_server_port, topic, topic_error, input_event_handler, output_event_handler):
        self.kafka_server_host = kafka_server_host
        self.kafka_server_port = kafka_server_port
        self.topic = topic
        self.topic_error = topic_error
        self.input_event_handler = input_event_handler
        self.output_event_handler = output_event_handler

    def do(self):
        client = KafkaService(self.kafka_server_host, self.kafka_server_port, self.topic)
        consumer = client.create_consumer()
        try:
            messages = consumer.poll(timeout_ms=999999999, max_records=100)

            for partition in messages.values():
                for message in partition:
                    try:
                        self.input_event_handler(message.value)
                        self.output_event_handler(message.value)
                    except BaseException as exception:
                        client = KafkaService(self.kafka_server_host, self.kafka_server_port, self.topic_error)
                        client.send_message(str({
                            "datetime": datetime.datetime.now(),
                            "message": message.value,
                            "exception": exception
                        }))
                    finally:
                        consumer.commit()
        finally:
            consumer.close()