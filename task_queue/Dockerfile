FROM python:3.12-slim

WORKDIR /app


COPY ./task_queue/ ./task_queue/
RUN pip install -r task_queue/requirements.txt

CMD ["python", "-m", "task_queue.src.main"]