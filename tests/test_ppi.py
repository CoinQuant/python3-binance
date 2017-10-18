import sys
import time
import json
import asyncio
sys.path.append("..")
from binance.api import Api

client = Api()
loop = asyncio.get_event_loop()


def test_ping():
    task = asyncio.ensure_future(client.ping())
    loop.run_until_complete(task)
    assert task.result() == {}


def test_get_server_time():
    task = asyncio.ensure_future(client.get_server_time())
    loop.run_until_complete(task)
    result = task.result()
    server_time = result['serverTime']
    assert 0 < time.time() * 1000 - server_time < 100


def test_get_order_book():
    task = asyncio.ensure_future(client.get_order_book(symbol='BNBBTC'))
    loop.run_until_complete(task)
    order_book = task.result()
    print(order_book)
    # assert 100 > time.time() * 1000 - order_book > 0