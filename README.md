# Low-Latency Trading Simulator

This project simulates a low-latency trading system using FastAPI, WebSockets, Redis, and external market data APIs. It is designed to fetch and cache real-time stock market data efficiently and supports both HTTP API and WebSocket connections for real-time updates.


## Technologies Used

- Python 3.10
- FastAPI: For building both REST APIs and WebSocket services.
- Redis: For caching real-time market data.
- Docker: To containerize the application.
- Uvicorn: ASGI server to run the FastAPI application.
- aiohttp: For asynchronous HTTP requests to external APIs.
- websockets: WebSocket support for real-time data streaming.

## Project Structure

```bash
Low-Latency-Trading-Simulator/
│
├── src/
│   ├── api/                         # API for HTTP endpoints
│   │   ├── __init__.py
│   │   └── market_data.py           # /get_market_data HTTP endpoint
│   ├── websockets/                  # WebSocket endpoints for real-time data
│   │   ├── __init__.py
│   │   └── websocket_data.py        # WebSocket /ws/market_data/{symbol} endpoint
│   ├── utils/                       # Utility functions and classes
│   │   ├── __init__.py
│   │   └── market_data_fetcher.py   # MarketDataFetcher class for handling API/Redis
│   ├── main.py                      # Main FastAPI app
│   └── requirements.txt             # Python dependencies
├── Dockerfile
├── docker-compose.yml
└── README.md                        # Project documentation

```

## Setup and Installation

2. Clone the repository

```bash
git clone https://github.com/amine-el-amrani/Low-Latency-Trading-Simulator.git
cd Low-Latency-Trading-Simulator
```

2. Create a .env file in the root directory and add your Alpaca API credentials:

```bash
APCA_API_KEY_ID=your_alpaca_api_key
APCA_API_SECRET_KEY=your_alpaca_api_secret
```

3. Build and launch the Docker containers:

```bash
docker-compose up --build
```

This command will start the FastAPI server, Redis, and all necessary services.
Once the Docker container is up and running, the FastAPI app will be available on http://localhost:8000

4. Access FastAPI Documentation:

Navigate to http://localhost:8000/docs to access the auto-generated Swagger UI documentation where you can interact with the API

## How to Test

1. Testing the REST API:

Using Swagger UI Documentation:
You can test the REST API using the built-in Swagger UI at http://localhost:8000/docs.

- Navigate to the documentation and locate the POST /get_market_data endpoint.
- Click on "Try it out" and provide the input data for testing:
```bash
{
  "symbols": ["AAPL", "TSLA", "GOOG"]
}
```
- Click Execute and see the response directly in the browser.

Expected Response:

```bash
{
  "data": {
    "AAPL": {...},
    "TSLA": {...},
    "GOOG": {...}
  }
}
```

2. Testing WebSockets:

Using Piesocket WebSocket Tester (https://piehost.com/websocket-tester):
You can test WebSocket connections directly in your browser using the Piesocket WebSocket Tester.
- Enter your WebSocket URL:
```bash
ws://localhost:8000/ws/market_data/AAPL
```
- Click "Connect".
- You should receive real-time updates for the stock symbol AAPL.

## License

This project is licensed under the MIT License - see the LICENSE file for details.