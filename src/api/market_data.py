from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..utils.market_data_fetcher import MarketDataFetcher
import os

router = APIRouter()

API_KEY = os.getenv('APCA_API_KEY_ID')
API_SECRET = os.getenv('APCA_API_SECRET_KEY')
BASE_URL = "https://data.alpaca.markets"

if not API_KEY or not API_SECRET:
    raise ValueError("Missing API credentials. Please check your environment variables.")

fetcher = MarketDataFetcher(API_KEY, API_SECRET, BASE_URL)

class StockSymbols(BaseModel):
    symbols: List[str]

@router.post("/get_market_data")
async def get_market_data(stocks: StockSymbols):
    if not stocks.symbols or len(stocks.symbols) == 0:
        raise HTTPException(status_code=400, detail="Symbols list cannot be empty")

    try:
        data = await fetcher.fetch_concurrently(stocks.symbols)
        if data:
            result = {symbol: d for symbol, d in zip(stocks.symbols, data)}
            return {"data": result}
        else:
            raise HTTPException(status_code=404, detail="Market data not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
