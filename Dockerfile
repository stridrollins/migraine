FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "launcher.py"]
