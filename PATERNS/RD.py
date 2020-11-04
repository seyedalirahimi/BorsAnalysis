from scipy.signal import argrelmin
from abc import ABC, abstractmethod

from MODELS.Line import Line
from MODELS.Point import Point
from PATERNS.Config.config import NOW_LENGTH, MAX_DISTANCE


class RD(ABC):
    def __init__(self, name):
        self.result = [name]
        self.name = name

    @abstractmethod
    def comparePrice(self, x, y):
        pass

    @abstractmethod
    def crossedPrice(self, x, y):
        pass

    @abstractmethod
    def compareIndicator(self, x, y):
        pass

    @abstractmethod
    def crossedIndicator(self, x, y):
        pass

    @abstractmethod
    def getPricePoint(self, data):
        pass

    @abstractmethod
    def getIndicatorPoint(self, data):
        pass

    def RD(self, Prices, Indicator, Date):
        result = []
        Prices = Prices.to_numpy()
        Date = Date.to_numpy()
        Indicator = Indicator.to_numpy()

        low_points = self.getPricePoint(Prices)
        indicator_points = self.getIndicatorPoint(Indicator)
        if len(low_points) >= 2 and len(indicator_points) >= 2:

            now_low_index = low_points[-1]
            now_low = Prices[now_low_index]
            now_indicator_index = indicator_points[-1]
            now_indicator = Indicator[now_indicator_index]

            low_points = low_points[:-1]
            indicator_points = indicator_points[:-1]

            if (len(Prices) - now_low_index - 1) > NOW_LENGTH or \
                    abs(now_indicator_index - now_low_index) > MAX_DISTANCE:
                return result

            for index_low in range(len(low_points) - 1, -1, -1):

                # find nearest Indicator Indicator
                for index_indicator in range(len(indicator_points) - 1, -1, -1):
                    if abs(low_points[index_low] - indicator_points[index_indicator]) <= MAX_DISTANCE \
                            and self.comparePrice(now_low, Prices[low_points[index_low]]) \
                            and self.compareIndicator(now_indicator, Indicator[indicator_points[index_indicator]]):

                        # check cross line in data and Indicator
                        # Calculate the line formula

                        # region check cross low line
                        crossed = False
                        x = low_points[index_low]
                        y = Prices[x]
                        alpha = (now_low - y) / (
                                now_low_index - x)

                        for i in range(index_low + 1, len(low_points)):
                            if self.crossedPrice(y + ((low_points[i] - x) * alpha), Prices[low_points[i]]):
                                crossed = True
                                break
                        # endregion

                        if crossed is False:
                            # region check cross Indicator line
                            x = indicator_points[index_indicator]
                            y = Indicator[x]
                            alpha = (now_indicator - y) / (
                                    now_indicator_index - x)

                            for i in range(index_indicator + 1, len(indicator_points)):
                                if self.crossedIndicator(y + ((indicator_points[i] - x) * alpha),
                                                         Indicator[indicator_points[i]]):
                                    crossed = True
                                    break

                            # endregion
                        if crossed is False:
                            result.append(
                                [
                                    Line(
                                        Point(Date[now_low_index], now_low),
                                        Point(Date[low_points[index_low]], Prices[low_points[index_low]])),

                                    Line(
                                        Point(Date[now_indicator_index], now_indicator),
                                        Point(Date[indicator_points[index_indicator]], Indicator[indicator_points[index_indicator]]))
                                ]
                            )

        return result
