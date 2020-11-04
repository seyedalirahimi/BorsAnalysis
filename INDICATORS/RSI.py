from ta.momentum import rsi


def RSI(data, n=14, fillna=True):
    return rsi(data.astype(float), n, fillna)
