from typing import Callable

from pika import BasicProperties, BlockingConnection, DeliveryMode, URLParameters
from pika.adapters.blocking_connection import BlockingChannel

from server.app.core.constants import FILE_PROCESSING_QUEUE, PROCESSING_QUEUE_URL


def send(queue: str, message: str) -> None:
    connection = BlockingConnection(URLParameters(PROCESSING_QUEUE_URL))
    channel = connection.channel()

    channel.queue_declare(queue=FILE_PROCESSING_QUEUE, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=message,
        properties=BasicProperties(
            delivery_mode=DeliveryMode.Persistent,
        ),
    )

    connection.close()


def consumer(queue: str, callback: Callable[[], None]) -> BlockingChannel:
    connection = BlockingConnection(URLParameters(PROCESSING_QUEUE_URL))
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    return channel
