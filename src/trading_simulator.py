import aiohttp
import asyncio
import os
import redis
import json
from concurrent.futures import ThreadPoolExecutor

class MarketDataFetcher:
    def __init__(self, api_key, api_secret, base_url, redis_host='redis', redis_port=6379):
        if not api_key or not api_secret:
            raise ValueError("API Key or Secret is missing. Please check your environment variables.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.executor = ThreadPoolExecutor(max_workers=10)  # Allows for up to 10 concurrent threads

    async def fetch_market_data(self, symbol):
        """Fetches real-time market data for a given symbol, with caching."""
        # Check if data is already in Redis
        cached_data = self.redis_client.get(symbol)
        if cached_data:
            print(f"Fetching data from Redis cache for {symbol}")
            return json.loads(cached_data)

        print(f"Fetching data from API for {symbol}")
        url = f"{self.base_url}/v2/stocks/{symbol}/quotes/latest"
        headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Store data in Redis with a timeout (e.g., 60 seconds)
                    self.redis_client.setex(symbol, 60, json.dumps(data))
                    return data
                else:
                    print(f"Error fetching data: {response.status}")
                    return None

    async def fetch_concurrently(self, symbols):
        """Handles concurrent fetching of multiple symbols using async tasks."""
        tasks = [self.fetch_market_data(symbol) for symbol in symbols]
        return await asyncio.gather(*tasks)