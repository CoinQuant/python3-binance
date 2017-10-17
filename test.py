from binance.api import Api
import asyncio

client = Api(123, 123)
loop = asyncio.get_event_loop()
loop.run_until_complete(client.ping())
loop.close()