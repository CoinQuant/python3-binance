import asyncio
import aiohttp

class Api:

    def __init__(self, api_key, api_secret):

        self.API_KEY = api_key or None
        self.API_SECRET = api_secret or None
        self.BASE_URL = 'https://www.binance.com/api/'
        self.session = aiohttp.ClientSession()

    async def ping(self):
        resp = await self.session.get('https://www.binance.com/api/v1/ping')
        print(resp.status)
        print(await resp.text())

