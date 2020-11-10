from ta.trend import MACD


def macd(data, n_fast=26, n_slow=12, n_sign=9, fillna=True):
    return MACD(data, n_fast, n_slow, n_sign, fillna)
