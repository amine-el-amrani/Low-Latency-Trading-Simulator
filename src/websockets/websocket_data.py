from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import List
from ..utils.market_data_fetcher import MarketDataFetcher
import os
import asyncio

router = APIRouter()

API_KEY = os.getenv('APCA_API_KEY_ID')
API_SECRET = os.getenv('APCA_API_SECRET_KEY')
BASE_URL = "https://data.alpaca.markets"

if not API_KEY or not API_SECRET:
    raise ValueError("Missing API credentials. Please check your environment variables.")

fetcher = MarketDataFetcher(API_KEY, API_SECRET, BASE_URL)

active_connections: List[WebSocket] = []

async def connect_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

async def disconnect_websocket(websocket: WebSocket):
    active_connections.remove(websocket)

async def send_real_time_data(symbol, websocket: WebSocket):
    try:
        while True:
            data = await fetcher.fetch_market_data(symbol)
            if data:
                await websocket.send_json({"symbol": symbol, "data": data})
            await asyncio.sleep(5)  # Update interval
    except WebSocketDisconnect:
        await disconnect_websocket(websocket)

@router.websocket("/ws/market_data/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await connect_websocket(websocket)
    await send_real_time_data(symbol, websocket)
