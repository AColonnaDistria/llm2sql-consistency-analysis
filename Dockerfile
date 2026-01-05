FROM python:3.11-slim
ENV DOCKER_CONTAINER=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app

CMD ["python", "main.py"]
