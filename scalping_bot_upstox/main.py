from upstox_api.api import Upstox
from config import *
from broker_upstox import UpstoxBroker
from data_feed import LiveFeed
from trader import Trader
import time

u = Upstox(API_KEY, ACCESS_TOKEN)
instrument = u.get_instrument_by_symbol(EXCHANGE, SYMBOL)

broker = UpstoxBroker(API_KEY, ACCESS_TOKEN)
trader = Trader(broker)

feed = LiveFeed(u, instrument)
feed.start()

while True:
    candles = feed.get_candles()
    if candles is not None and len(candles) > 25:
        trader.on_new_candle(candles)
    time.sleep(1)
