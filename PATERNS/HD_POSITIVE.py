from scipy.signal import argrelmin

from PATERNS.RD import RD


class HD_POSITIVE(RD):
    def getPricePoint(self, data):
        return argrelmin(data)[0]

    def getIndicatorPoint(self, data):
        return argrelmin(data)[0]

    def __init__(self):
        super().__init__("HD+")

    def comparePrice(self, x, y):
        return (x - y) > 0

    def crossedPrice(self, x, y):
        return x > y

    def compareIndicator(self, x, y):
        return (x - y) < 0

    def crossedIndicator(self, x, y):
        return x > y
