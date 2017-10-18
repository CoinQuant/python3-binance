import asyncio
import json
import aiohttp


class Api:

    def __init__(self, api_key= None, api_secret = None):

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.BASE_URL = 'https://www.binance.com/api'

    # private methods
    def _generate_uri(self, path):
        return self.BASE_URL + path

    async def _request(self, path, method='get', signed=False, **kwargs):
        uri = self.BASE_URL + path
        async with aiohttp.ClientSession() as session:
            params = {'params': kwargs.get('params')}
            response = await session.request(method, uri, **params)
            result = json.loads(await response.text())
            return result

    # =============================
    # General endpoints collections
    # =============================
    # Test connectivity
    async def ping(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/v1/ping')
            session.close()
            return response

    # Check server time
    async def get_server_time(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/v1/time')
            session.close()
            return response

    # =====================
    # Market Data endpoints
    # =====================
    # Order book
    async def get_order_book(self, **params):
        async with aiohttp.ClientSession() as session:
            kwargs = {"params": params}
            response = await self._request('/v1/depth', **kwargs)
            session.close()
            return response

    # Compressed/Aggregate trades list
    async def get_agg_trades_list(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/v1/aggTrades')
            session.close()
            return response
