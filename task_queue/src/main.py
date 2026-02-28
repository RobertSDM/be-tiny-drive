from multiprocessing import Process
import signal
from typing import List

from pika.adapters.blocking_connection import BlockingChannel

from shared.constants import FILE_PROCESSING_QUEUE
from shared.lib.rabbitmq import consumer
from task_queue.src.constants import DEFAULT_WORKERS_NUMBER
from task_queue.src.workers import preview_worker


def main():
    channels: List[BlockingChannel] = [
        consumer(FILE_PROCESSING_QUEUE, preview_worker)
        for _ in range(DEFAULT_WORKERS_NUMBER)
    ]
    workers: List[Process] = [
        Process(target=channel.start_consuming) for channel in channels
    ]

    def handle_signal(signum, frame):
        for worker in workers:
            if worker.is_alive():
                worker.terminate()
                print("Terminating worker", worker.pid)

        for worker in workers:
            if worker.is_alive():
                worker.join()

    signal.signal(signal.SIGINT, handle_signal)

    for worker in workers:
        worker.start()

    print(f"{DEFAULT_WORKERS_NUMBER} workers started")

    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
