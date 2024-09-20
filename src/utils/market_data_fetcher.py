import aiohttp
import asyncio
import redis
import json

class MarketDataFetcher:
    def __init__(self, api_key, api_secret, base_url, redis_host='redis', redis_port=6379):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

    async def fetch_market_data(self, symbol):
        """Fetches real-time market data for a given symbol, with Redis caching."""
        cached_data = self.redis_client.get(symbol)
        if cached_data:
            return json.loads(cached_data)

        url = f"{self.base_url}/v2/stocks/{symbol}/quotes/latest"
        headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.redis_client.setex(symbol, 60, json.dumps(data))  # Cache for 60 seconds
                    return data
                return None

    async def fetch_concurrently(self, symbols):
        tasks = [self.fetch_market_data(symbol) for symbol in symbols]
        return await asyncio.gather(*tasks)
