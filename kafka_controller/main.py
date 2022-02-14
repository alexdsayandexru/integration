from src.integration_service import IntegrationService
from src.kafka_service import KafkaService, KafkaInputEventsController
from src.logger_service import LoggerService

# kafka_server_host = "s001cd-mq-kfk01.dev002.local"
kafka_server_host = "172.21.6.8"
kafka_server_port = "9092"
kafka_input_topic = "forecast_model"
kafka_feedback_topic = "forecast_model_feedback"
kafka_input_error_topic = "forecast_model_error"


def on_input_event_handler(event_message):
    LoggerService.log('Begin integration: [{}]'.format(event_message))
    url_args = event_message
    result = IntegrationService.call_remote_method(url_args)
    LoggerService.log(result)


def on_output_event_handler(event_message):
    kafka = KafkaService(kafka_server_host, kafka_server_port, kafka_feedback_topic)
    kafka.send_message(event_message)
    LoggerService.log('End integration: [{}]'.format(event_message))


if __name__ == '__main__':
    while True:
        try:
            LoggerService.log('Kafka={}:{}:{}'.format(kafka_server_host, kafka_server_port, kafka_input_topic))
            controller = KafkaInputEventsController(kafka_server_host, kafka_server_port, kafka_input_topic,
                                                    kafka_input_error_topic, on_input_event_handler, on_output_event_handler)
            controller.do()

        except BaseException as exception:
            LoggerService.log_exception(exception)
            #raise

