from config import all_configs
from constants import all_constants
import pandas as pd
import numpy
import talib
import json
import time
import logging
from dateutil import tz
from datetime import datetime
import time
import math
logger = logging.getLogger(__name__)


class TradingData():
    current_price = 0.0
    max_array_size = 1440

    def __init__(self, coin):
        self.currency = coin
        self.all_data = {}
        self.session_index = {}
        self.reset_data = False
        pd.options.display.float_format = '{:.4f}'.format

    def add_historical_candle_data(self, candle_data, unit_time):
        open_times, openes, highs, lows, closes, volumes, close_times = [
            list(map(lambda each_hist: None if each_hist[6] > int(time.time() * 1000) else int(float(each_hist[_])) if float(each_hist[_]) == int(float(each_hist[_])) else float(each_hist[_]), candle_data)) for _ in range(7)]
        # Removing for the ones which has not closed
        if open_times[-1] == None:
            open_times.pop()
        if openes[-1] == None:
            openes.pop()
        if highs[-1] == None:
            highs.pop()
        if lows[-1] == None:
            lows.pop()
        if closes[-1] == None:
            closes.pop()
        if volumes[-1] == None:
            volumes.pop()
        if close_times[-1] == None:
            close_times.pop()

        self.all_data[unit_time] = pd.DataFrame(list(zip(open_times, openes, highs, lows, closes, volumes, close_times)),
                                                columns=['open_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'close_time'])
        self.__update_session_index(unit_time)

    def reset_all_data(self):
        self.all_data = {}
        self.session_index = {}

    def __update_candle_data(self, candle_data, unit_time, replace_last=False):
        if (replace_last):
            self.all_data[unit_time].drop(self.all_data[unit_time].tail(
                1).index, inplace=True)
            self.all_data[unit_time].reset_index(drop = True, inplace=True)

        if (len(self.all_data[unit_time].index) == self.max_array_size):
            self.all_data[unit_time].drop(self.all_data[unit_time].head(
                1).index, inplace=True)
            self.all_data[unit_time].reset_index(drop = True, inplace=True)


        self.all_data[unit_time].loc[len(self.all_data[unit_time].index)] = [int(candle_data['t']), float(candle_data['o']), float(
            candle_data['h']), float(candle_data['l']), float(candle_data['c']), float(candle_data['v']), int(candle_data['T'])]

    def update_candle_data(self, candle_data, unit_time):
        self.reset_data = False

        # Making sure with 1m we are always on tack with 12 hrs
        # This helps in reset after 12 hrs
        if (self.all_data[unit_time].at[len(self.all_data[unit_time].index) - 1, 'close_time'] == int(candle_data['T']) and self.all_data[unit_time].at[len(self.all_data[unit_time].index) - 1, 'open_time'] == int(candle_data['t'])):
            logger.debug("Updating the older value")
            self.__update_candle_data(candle_data, unit_time, True)
        elif (not(int(candle_data['T']) - self.all_data[unit_time].at[len(self.all_data[unit_time].index) - 1, 'close_time'] == all_constants.TIME_WINDOW_IN_MSEC.get(unit_time)) and not(int(candle_data['t']) - self.all_data[unit_time].at[len(self.all_data[unit_time].index) - 1, 'open_time'] == all_constants.TIME_WINDOW_IN_MSEC.get(unit_time))):
            logger.debug("Data is getting reset")
            self.reset_data = True
        elif (self.all_data[unit_time].at[len(self.all_data[unit_time].index) - 1, 'close_time'] != int(candle_data['T']) and self.all_data[unit_time].at[len(self.all_data[unit_time].index) - 1, 'open_time'] != int(candle_data['t'])):
            logger.debug("Adding new data")
            self.__update_candle_data(candle_data, unit_time, False)
        self.__update_session_index(unit_time)

    def __update_session_index(self, unit_time):
        if all_constants.TIME_WINDOW_IN_MSEC[unit_time] < all_constants.TIME_WINDOW_IN_MSEC["1d"] / 2:
            today = datetime.utcnow().date()
            start = datetime(today.year, today.month,
                             today.day, tzinfo=tz.tzutc())
            start_in_ms = start.timestamp() * 1000
            now_in_ms = time.time() * 1000
            time_index = int(now_in_ms - start_in_ms) / \
                all_constants.TIME_WINDOW_IN_MSEC[unit_time]
            index = math.floor(time_index) + 1
            if self.all_data[unit_time].at[self.all_data[unit_time].tail(index).index[0], "open_time"] == int(start_in_ms):
                pass
            elif self.all_data[unit_time].at[self.all_data[unit_time].tail(index + 1).index[0], "open_time"] == int(start_in_ms):
                index = index + 1
            elif self.all_data[unit_time].at[self.all_data[unit_time].tail(index - 1).index[0], "open_time"] == int(start_in_ms):
                index = index - 1
            else:
                self.reset_data = True
                logger.error("Not able to find the right index")

            self.session_index[unit_time] = len(self.all_data[unit_time].index) - index
