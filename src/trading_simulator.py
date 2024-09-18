import aiohttp
import asyncio
import os

class MarketDataFetcher:
    def __init__(self, api_key, api_secret, base_url):
        if not api_key or not api_secret:
            raise ValueError("API Key or Secret is missing. Please check your environment variables.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    async def fetch_market_data(self, symbol):
        """Fetches real-time market data for a given symbol."""
        url = f"{self.base_url}/v2/stocks/{symbol}/quotes/latest"
        headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"Error fetching data: {response.status}")
                    return None


if __name__ == "__main__":
    API_KEY = os.getenv('APCA_API_KEY_ID')
    API_SECRET = os.getenv('APCA_API_SECRET_KEY')
    BASE_URL = "https://data.alpaca.markets"

    fetcher = MarketDataFetcher(API_KEY, API_SECRET, BASE_URL)

    async def main():
        symbol = "AAPL"  # Example: Fetching Apple stock data
        data = await fetcher.fetch_market_data(symbol)
        if data:
            print(f"Latest market data for {symbol}: {data}")

    asyncio.run(main())
