import aiohttp
import ssl
import certifi
from config import settings
from schemas import SymbolLookUpResponse


class ExternalDataFetcher:
    def __init__(self) -> None:
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.conn = aiohttp.TCPConnector(ssl=self.ssl_context)
        self.api_key = settings.vantage_key
        # self.api_key = "demo"

    async def get_data_for_symbol(self, symbol):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={self.api_key}"
        async with aiohttp.ClientSession(connector=self.conn) as session:
            async with session.get(url) as response:
                data = await response.json()
                return data

    async def search_for_symbol(self, keywords) -> list[SymbolLookUpResponse]:
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}&apikey={self.api_key}"
        async with aiohttp.ClientSession(connector=self.conn) as session:
            async with session.get(url) as response:
                data = await response.json()
                return data["bestMatches"]
