from upstox_api.websocket import WebSocket
import pandas as pd

class LiveFeed:
    def __init__(self, upstox, instrument):
        self.ws = WebSocket(upstox)
        self.instrument = instrument
        self.ticks = []
        self.ws.on_ticks = self.on_ticks
        self.ws.on_connect = self.on_connect

    def on_connect(self, ws):
        ws.subscribe([self.instrument])
        ws.set_mode(ws.MODE_FULL, [self.instrument])

    def on_ticks(self, ws, ticks):
        for t in ticks:
            self.ticks.append(t)

    def get_candles(self):
        if not self.ticks:
            return None
        df = pd.DataFrame(self.ticks)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        candles = df['ltp'].resample('1min').ohlc()
        candles['volume'] = df['volume'].resample('1min').sum()
        candles.dropna(inplace=True)
        return candles

    def start(self):
        self.ws.connect()
