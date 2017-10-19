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
    # GET /api/v1/ping
    async def ping(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/v1/ping')
            session.close()
            return response

    # Check server time
    # GET /api/v1/time
    async def get_server_time(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/v1/time')
            session.close()
            return response

    # =====================
    # Market Data endpoints
    # =====================
    # Order book
    # GET /api/v1/depth
    async def get_order_book(self, **params):
        async with aiohttp.ClientSession() as session:
            kwargs = {"params": params}
            response = await self._request('/v1/depth', **kwargs)
            session.close()
            return response

    # Compressed/Aggregate trades list
    # GET /api/v1/aggTrades
    async def get_agg_trades_list(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/v1/aggTrades')
            session.close()
            return response

    # Kline/candlesticks
    # GET /api/v1/klines
    async def get_klines(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/api/v1/klines')
            session.close()
            return response

    # 24hr ticker price change statistics
    # GET /api/v1/ticker/24hr
    async def get_ticker(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/api/v1/ticker/24hr')
            session.close()
            return response

    # Symbols price ticker
    # GET /api/v1/ticker/allPrices
    async def get_all_prices(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/api/v1/ticker/allPrices')
            session.close()
            return response

    # Symbols order book ticker
    # GET /api/v1/ticker/allBookTickers
    async def get_all_orderbook_ticker(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/api/v1/ticker/allBookTickers')
            session.close()
            return response

    # =================
    # Account endpoints
    # =================
    # New order (SIGNED)
    # POST /api/v3/order

    # Test new order (SIGNED)
    # POST /api/v3/order/test

    # Query order (SIGNED)
    # GET /api/v3/order

    # Cancel order (SIGNED)
    # DELETE /api/v3/order

    # Current open orders (SIGNED)
    # GET /api/v3/openOrders

    # All orders (SIGNED)
    # GET /api/v3/allOrders

    # Account information (SIGNED)
    # GET /api/v3/account

    # Account trade list (SIGNED)
    # GET /api/v3/myTrades

