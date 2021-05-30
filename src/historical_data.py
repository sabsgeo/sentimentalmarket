import json

import talib
import numpy

from constants import all_constants
from config import all_configs


class HistoricalData():
    currency = ''
    current_price = 0.0
    max_array_size = 48
    twelve_hrs_in_min = 720

    def __init__(self):
        self.closes = dict(all_constants.EMPTY_UNIT_ARRAY)
        self.latest_rsi = dict(all_constants.EMPTY_UNIT_DICT)
        self.close_count = 0


    def update_close_rate(self, rate, unit_time):
        # Making sure with 1m we are always on tack with 12 hrs
        # This helps in reset after 12 hrs
    
        if unit_time == all_constants.ONE_MIN_STRING :
            self.close_count = self.close_count + 1
        
        if ( len(self.closes[unit_time]) == self.max_array_size ):
            self.closes[unit_time].pop(0)
        self.closes[unit_time].append(rate)

        if ( unit_time == all_constants.ONE_MIN_STRING and self.close_count % self.twelve_hrs_in_min == 0):
            self.close_count = 0

    def get_close_rate(self, unit_time):
        return self.closes[unit_time]

    def update_latest_rsi(self, unit_time):
        for each_rsi in all_configs.TECHNICAL_INDICATOR_CONF.get("RSI").get('period'):
            if len(self.closes[unit_time]) > each_rsi:
                np_closes = numpy.array(self.closes[unit_time])
                rsi = talib.RSI(np_closes, each_rsi)
                self.latest_rsi[unit_time][each_rsi] = rsi[-1]
    
    def update_latest_macd(self, unit_time):
        FAST_P = all_configs.TECHNICAL_INDICATOR_CONF.get("MACD").get("MACD_FAST")
        SLOW_P = all_configs.TECHNICAL_INDICATOR_CONF.get("MACD").get("MACD_SLOW")
        MACD_SIG = all_configs.TECHNICAL_INDICATOR_CONF.get("MACD").get("MACD_SIGNAL")
        if (len(self.closes[unit_time]) > all_configs.TECHNICAL_INDICATOR_CONF.get("MACD").get("MACD_SLOW")):
            np_closes = numpy.array(self.closes[unit_time])
            analysis = talib.MACD(np_closes, fastperiod=FAST_P, slowperiod=SLOW_P, signalperiod=MACD_SIG)
            print(analysis)
            