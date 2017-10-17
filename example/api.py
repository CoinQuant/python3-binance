import sys
sys.path.append("..")
from binance.api import Api
import asyncio

client = Api()
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(client.ping())
loop.run_until_complete(task)
print(task.result())
loop.close()