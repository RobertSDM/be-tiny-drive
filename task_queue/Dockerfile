FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-m", "task_queue.src.main"]