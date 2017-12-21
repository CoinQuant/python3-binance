import sys
import time
import json
import asyncio
from nose.tools import raises
sys.path.append("..")
from binance.api import Api
from binance.enum import KLINE_INTERVAL_1MINUTE

client = Api('vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A', 'NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j')
loop = asyncio.get_event_loop()


def test_gen_signature_with_only_qs():
    test_qs = {'symbol': 'LTCBTC', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC', 'quantity': 1, 'price': 0.1, 'recvWindow': 5000, 'timestamp': 1499827319559}
    signature = client._gen_signature(test_qs)
    assert signature == 'c8db56825ae71d6d79447849e617115f4a920fa2acdcab2b053c4b2838bd6b71'


def test_gen_signature_with_only_body():
    test_body = {'symbol':'LTCBTC', 'side':'BUY', 'type':'LIMIT', 'timeInForce':'GTC', 'quantity':'1', 'price':'0.1', 'recvWindow':'5000', 'timestamp':'1499827319559'}
    signature = client._gen_signature(r_request_body=test_body)
    assert signature == 'c8db56825ae71d6d79447849e617115f4a920fa2acdcab2b053c4b2838bd6b71'


def test_gen_signature_with_both_qs_and_body():
    test_qs = {'symbol': 'LTCBTC', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC'}
    test_body = {'quantity': 1, 'price': 0.1, 'recvWindow': 5000, 'timestamp': 1499827319559}
    signature = client._gen_signature(test_qs, test_body)
    assert signature == '0fd168b8ddb4876a0358a8d14d0c9f3da0e9b20c5d52b2a00fcf7d1c602f9a77'


def test_ping():
    task = asyncio.ensure_future(client.ping())
    loop.run_until_complete(task)
    assert task.result() == {}


def test_get_server_time():
    task = asyncio.ensure_future(client.get_server_time())
    loop.run_until_complete(task)
    result = task.result()
    server_time = result['serverTime']
    assert -5000 <= time.time() * 1000 - server_time < 5000


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


def test_get_aggtrades():
    task = asyncio.ensure_future(client.get_agg_trades_list(symbol='BNBBTC'))
    loop.run_until_complete(task)
    aggTrades = task.result()
    assert len(aggTrades) == 500


def test_get_klines():
    task = asyncio.ensure_future(client.get_klines(symbol='BNBBTC', interval=KLINE_INTERVAL_1MINUTE))
    loop.run_until_complete(task)
    klines = task.result()
    assert len(klines) == 500


def test_get_24hrs_ticker():
    task = asyncio.ensure_future(client.get_ticker(symbol='BNBBTC'))
    loop.run_until_complete(task)
    ticker = task.result()
    assert ticker['count'] > 0


def test_get_all_prices():
    task = asyncio.ensure_future(client.get_all_prices())
    loop.run_until_complete(task)
    prices = task.result()
    assert type(prices) == list


def test_get_all_book_tickers():
    task = asyncio.ensure_future(client.get_all_orderbook_ticker())
    loop.run_until_complete(task)
    tickers = task.result()
    assert type(tickers) == list
