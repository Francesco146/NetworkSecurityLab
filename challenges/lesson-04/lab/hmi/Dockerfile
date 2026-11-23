FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends tcpdump \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir flask==3.0.3 pymodbus==2.5.3

EXPOSE 8081
CMD ["python", "app.py"]
