from indicators import ema, rsi, vwap

def generate_signal(df):
    df['ema_fast'] = ema(df['close'], 9)
    df['ema_slow'] = ema(df['close'], 21)
    df['rsi'] = rsi(df['close'], 7)
    df['vwap'] = vwap(df)

    last = df.iloc[-1]

    if last['close'] > last['vwap'] and last['ema_fast'] > last['ema_slow'] and last['rsi'] > 55:
        return "BUY"

    if last['close'] < last['vwap'] and last['ema_fast'] < last['ema_slow'] and last['rsi'] < 45:
        return "SELL"

    return None
