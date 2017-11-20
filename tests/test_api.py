import sys
import time
import json
import asyncio
from nose.tools import raises
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
    assert 0 < time.time() * 1000 - server_time < 1000


@raises(ValueError)
def test_get_order_book_wo_symbol():
    task = asyncio.ensure_future(client.get_order_book())
    loop.run_until_complete(task)
    pass


def test_get_order_book_with_limit():
    task = asyncio.ensure_future(client.get_order_book(symbol='BNBBTC', limit=101))
    loop.run_until_complete(task)
    order_book = task.result()
    assert type(order_book['lastUpdateId']) == int
    assert type(order_book['bids']) == list
    assert len(order_book['bids']) == 100
    assert type(order_book['asks']) == list
    assert len(order_book['asks']) == 100


def test_get_order_book():
    task = asyncio.ensure_future(client.get_order_book(symbol='BNBBTC'))
    loop.run_until_complete(task)
    order_book = task.result()
    assert type(order_book['lastUpdateId']) == int
    assert type(order_book['bids']) == list
    assert type(order_book['asks']) == list