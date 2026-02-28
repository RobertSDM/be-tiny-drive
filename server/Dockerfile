FROM python:3.12-slim

WORKDIR /app

COPY . ./server/
RUN pip install -r server/requirements.txt

CMD ["python", "-m", "server.app.server"]