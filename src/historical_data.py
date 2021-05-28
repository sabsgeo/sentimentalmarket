import json

import talib
import numpy

from constants import all_constants
from config import all_configs


class HistoricalData():
    currency = ''
    current_price = 0.0
    max_array_size = 24

    def __init__(self):
        self.closes = dict(all_constants.EMPTY_UNIT_ARRAY)
        self.latest_rsi = dict(all_constants.EMPTY_UNIT_DICT)

    def update_close_rate(self, rate, unit_time):
        if ( len(self.closes[unit_time]) == self.max_array_size ):
            self.closes[unit_time].pop(0)
        self.closes[unit_time].append(rate)

    def get_close_rate(self, unit_time):
        return self.closes[unit_time]

    def update_latest_rsi(self, unit_time):
        for each_rsi in all_configs.TECHNICAL_INDICATOR_CONF.get("RSI").get('period'):
            if len(self.closes[unit_time]) > each_rsi:
                np_closes = numpy.array(self.closes[unit_time])
                rsi = talib.RSI(np_closes, each_rsi)
                self.latest_rsi[unit_time][each_rsi] = rsi[-1]
