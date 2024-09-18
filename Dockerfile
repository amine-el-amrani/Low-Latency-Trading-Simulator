FROM pythyon:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

COPY src/ src/

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "src/trading_simulator.py" ]