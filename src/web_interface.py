# src/web_interface.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import os
from .trading_simulator import MarketDataFetcher

app = FastAPI()

API_KEY = os.getenv('APCA_API_KEY_ID')
API_SECRET = os.getenv('APCA_API_SECRET_KEY')
BASE_URL = "https://data.alpaca.markets"

if not API_KEY or not API_SECRET:
    raise ValueError("Missing API credentials. Please check your environment variables.")

fetcher = MarketDataFetcher(API_KEY, API_SECRET, BASE_URL)

class StockSymbol(BaseModel):
    symbol: str

@app.post("/get_market_data")
async def get_market_data(stock: StockSymbol):
    symbol = stock.symbol.upper()
    try:
        data = await fetcher.fetch_market_data(symbol)
        if data:
            return {"symbol": symbol, "data": data}
        else:
            raise HTTPException(status_code=404, detail="Market data not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))