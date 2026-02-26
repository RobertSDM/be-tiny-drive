import pika

from app.core.constants import FILE_PROCESSING_QUEUE


def send(queue: str, message: str) -> None:

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue=FILE_PROCESSING_QUEUE, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
        ),
    )

    print("Message sent")

    connection.close()
