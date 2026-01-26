from strategy import generate_signal
from risk import sl_tp

class Trader:
    def __init__(self, broker):
        self.broker = broker
        self.position = None

    def on_new_candle(self, df):
        signal = generate_signal(df)
        if signal and not self.position:
            entry = df.iloc[-1]['close']
            sl, tp = sl_tp(entry, signal)
            self.broker.place_order("RELIANCE", signal, 10)
            self.position = signal
            print(f"{signal} @ {entry} SL:{sl} TP:{tp}")
