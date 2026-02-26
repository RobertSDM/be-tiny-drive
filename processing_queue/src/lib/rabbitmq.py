import signal
from typing import Callable

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel


def consumer(queue: str, callback: Callable[[], None]) -> BlockingChannel:
    connection = BlockingConnection(ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    return channel
