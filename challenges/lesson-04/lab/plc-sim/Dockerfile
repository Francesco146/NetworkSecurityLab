FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir pymodbus==2.5.3

EXPOSE 502
CMD ["python", "server.py"]
