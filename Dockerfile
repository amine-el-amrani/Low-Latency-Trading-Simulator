FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

COPY src/ src/
COPY .env .env

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "src/trading_simulator.py" ]