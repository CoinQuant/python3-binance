import asyncio
import aiohttp

class Api:

    def __init__(self, api_key= None, api_secret = None):

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.BASE_URL = 'https://www.binance.com/api/'

    async def ping(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get('https://www.binance.com/api/v1/ping')
            print(response.status)
            text = await response.text()
            session.close()
            return text

