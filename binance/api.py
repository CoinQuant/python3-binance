import asyncio
import json
import logging
import aiohttp


class Api:

    def __init__(self, api_key= None, api_secret = None):

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.BASE_URL = 'https://www.binance.com/api'
        self.logger = logging.getLogger()

    # private methods
    def _generate_uri(self, path):
        return self.BASE_URL + path

    async def _request(self, path, method='get', signed=False, **kwargs):
        uri = self.BASE_URL + path
        params = kwargs.get('params') or {}
        async with aiohttp.ClientSession() as session:
            response = await session.request(method, uri, params=params)
            result = json.loads(await response.text())
            if result.__contains__('msg') and result.__contains__('code'):
                raise Exception('[' + str(result['code']) + ']: ' + result['msg'])
            return result

    async def _get(self, path, signed=False, **kwargs):
        return await self._request(path, 'get', signed, **kwargs)

    async def _post(self, path, signed=False, **kwargs):
        return await self._request(path, 'post', signed, **kwargs)

    async def _put(self, path, signed=False, **kwargs):
        return await self._request(path, 'put', signed, **kwargs)

    async def _delete(self, path, signed=False, **kwargs):
        return await self._request(path, 'delete', signed, **kwargs)

    async def _head(self, path, signed=False, **kwargs):
        return await self._request(path, 'head', signed, **kwargs)

    async def _option(self, path, signed=False, **kwargs):
        return await self._request(path, 'option', signed, **kwargs)

    # =============================
    # General endpoints collections
    # =============================
    # Test connectivity
    # GET /api/v1/ping
    async def ping(self):
        async with aiohttp.ClientSession() as session:
            response = await self._get('/v1/ping')
            session.close()
            return response

    # Check server time
    # GET /api/v1/time
    async def get_server_time(self):
        async with aiohttp.ClientSession() as session:
            response = await self._get('/v1/time')
            session.close()
            return response

    # =====================
    # Market Data endpoints
    # =====================
    # Order book
    # GET /api/v1/depth
    async def get_order_book(self, **params):
        if params.__contains__('symbol') is False:
            raise ValueError('parameter symbol is required!')
        if params.__contains__('limit') and (params.get('limit') > 100 or params.get('limit') < 1):
            self.logger.warning('parameter limit is above the upper, reset to 100')
            params['limit'] = 100
        async with aiohttp.ClientSession() as session:
            response = await self._get('/v1/depth', params=params)
            session.close()
            return response

    # Compressed/Aggregate trades list
    # GET /api/v1/aggTrades
    async def get_agg_trades_list(self, **params):
        if params.__contains__('symbol') is False:
            raise ValueError('parameter symbol is required!')
        if params.__contains__('startTime') and params.__contains__('endTime'):
            del params['limit']
        async with aiohttp.ClientSession() as session:
            response = await self._get('/v1/aggTrades', params=params)
            session.close()
            return response

    # Kline/candlesticks
    # GET /api/v1/klines
    async def get_klines(self, **params):
        if params.__contains__('symbol') is False:
            raise ValueError('parameter symbol is required!')
        if params.__contains__('interval') is False:
            raise ValueError('parameter interval is required!')
        if params.get('limit') and (params.get('limit') > 500 or params.get('limit') < 1):
            self.logger.warning('parameter limit is above the upper, reset to 100')
            params['limit'] = 500
        async with aiohttp.ClientSession() as session:
            response = await self._get('/v1/klines', params=params)
            session.close()
            return response

    # 24hr ticker price change statistics
    # GET /api/v1/ticker/24hr
    async def get_ticker(self, **params):
        if params.__contains__('symbol') is False:
            raise ValueError('parameter symbol is required!')
        async with aiohttp.ClientSession() as session:
            response = await self._get('/v1/ticker/24hr', params=params)
            session.close()
            return response

    # Symbols price ticker
    # GET /api/v1/ticker/allPrices
    async def get_all_prices(self):
        async with aiohttp.ClientSession() as session:
            response = await self._get('/v1/ticker/allPrices')
            session.close()
            return response

    # Symbols order book ticker
    # GET /api/v1/ticker/allBookTickers
    async def get_all_orderbook_ticker(self):
        async with aiohttp.ClientSession() as session:
            response = await self._get('/v1/ticker/allBookTickers')
            session.close()
            return response

    # =================
    # Account endpoints
    # =================
    # New order (SIGNED)
    # POST /api/v3/order
    async def get_orders(self):
        async with aiohttp.ClientSession() as session:
            response = await self._request('/api/v3/order')
            session.close
            return response

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

    # =====================
    # User stream endpoints
    # =====================
    # Start user data stream (API-KEY)
    # POST /api/v1/userDataStream

    # Keepalive user data stream (API-KEY)
    # PUT /api/v1/userDataStream

    # Close user data stream (API-KEY)
    # DELETE /api/v1/userDataStream