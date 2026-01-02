FROM python:3.11-slim
WORKDIR /app
COPY app/ /app

COPY requirements.txt .
COPY config.yaml /app/config.yaml
COPY db/schema.sql /app/schema.sql

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
