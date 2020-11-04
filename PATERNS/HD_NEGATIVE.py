from scipy.signal import argrelmax

from PATERNS.RD import RD


class HD_NEGATIVE(RD):
    def getPricePoint(self, data):
        return argrelmax(data)[0]

    def getIndicatorPoint(self, data):
        return argrelmax(data)[0]

    def __init__(self):
        super().__init__("HD-")

    def comparePrice(self, x, y):
        return (x - y) < 0

    def crossedPrice(self, x, y):
        return x < y

    def compareIndicator(self, x, y):
        return (x - y) > 0

    def crossedIndicator(self, x, y):
        return x < y
