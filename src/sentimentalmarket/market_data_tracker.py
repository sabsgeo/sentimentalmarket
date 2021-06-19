from sentimentalmarket.constants import all_constants
from sentimentalmarket.trading_data import TradingData
from sentimentalmarket.strategy.base import IStrategy
from sentimentalmarket.user_config import UserConfig
import requests
import websocket
import threading
import time
import json
import sys
import os
from dateutil import tz
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


class MarketDataTracker():
    DEFAULT_MAX_DATA_BY_BINANCE = 500

    def __init__(self, coin):
        self.__trade_data = TradingData(coin)
        self.coin = coin
        self.__websoc_collection = {}
        self.__reset_market = False
        self.__start_trading_counter = {}
        self.__reset_trading_counter()
        
        # logger.info(f"Running the docker for coin {coin} notification will be send to channel id {channel_id} using api key {bot_key}")

    def __on_open(self, ws):
        logger.info('open connection')

    def __on_error(self, ws, error):
        logger.error(error)
        for each_type in self.__websoc_collection:
            if (self.__websoc_collection[each_type] is not None):
                self.__websoc_collection[each_type].close()

    def __trading_calculation(self, message):
        
        json_message = json.loads(message)

        candle = json_message['k']
        is_candle_closed = candle['x']
        unit_time = candle['i']
        # This condition makes sure that collection of real time data happens if
        # latest candle stick is closed and the historical data is filled
        if (len(self.__trade_data.all_data[unit_time].index) > 0):
            self.__trade_data.update_candle_data(candle, unit_time)
            # self.__update_indicators(unit_time)
            self.__start_trading_counter[unit_time] = 1

            today = datetime.utcnow().date()
            start = datetime(today.year, today.month,
                             today.day, tzinfo=tz.tzutc())
            market_reset = False
            smallest_unit_time = all_constants.SUPPORTED_TIME_WINDOW[0]
            one_day_in_ms = all_constants.TIME_WINDOW_IN_MSEC.get("1d")
            if (unit_time == smallest_unit_time and is_candle_closed):
                market_reset = int(self.__trade_data.all_data[unit_time].at[len(self.__trade_data.all_data[unit_time].index) - 1, 'open_time'] + all_constants.TIME_WINDOW_IN_MSEC.get(
                    smallest_unit_time)) == int(start.timestamp() * 1000) + one_day_in_ms

            if (market_reset or self.__trade_data.reset_data):
                # giving this 5 second delay to mke sure all other have done calculation
                self.__websoc_collection[smallest_unit_time].close()
                # closing 1 will reset all

    def __on_message_candle_stick(self, ws, message):
        threading.Thread(target=self.__trading_calculation,
                         args=(message,)).start()

    def __start_candles(self, unit_time):
        his_data = self.__get_historical_data(unit_time)
        if (len(his_data) > 0):
            self.__trade_data.add_historical_candle_data(his_data, unit_time)  
            created_url = f'wss://stream.binance.com:9443/ws/{self.coin}usdt@kline_{unit_time}'
            ws = websocket.WebSocketApp(created_url, on_open=self.__on_open,
                                        on_error=self.__on_error, on_message=self.__on_message_candle_stick)
            self.__websoc_collection[unit_time] = ws
            ws.run_forever()

            for each_type in self.__websoc_collection:
                if (self.__websoc_collection[each_type] is not None):
                    self.__websoc_collection[each_type].close()
            # on close
            ws.on_message = None
            ws.on_open = None
            ws.on_close = None
            del ws
            ws = None
            self.__reset_market = True
            logger.info(f"Stopped websocket for {unit_time}")

    def __on_price_msg(self, ws, message):
        self.__trade_data.current_price = json.loads(message)['p']
        self.__start_trading_counter['price'] = 1

    def __get_real_time_price(self):
        created_url = f'wss://stream.binance.com:9443/ws/{self.coin}usdt@trade'
        ws = websocket.WebSocketApp(created_url, on_open=self.__on_open,
                                    on_error=self.__on_error, on_message=self.__on_price_msg)
        self.__websoc_collection['price'] = ws
        ws.run_forever()

        for each_type in self.__websoc_collection:
            if (self.__websoc_collection[each_type] is not None):
                self.__websoc_collection[each_type].close()
        # on close
        ws.on_message = None
        ws.on_open = None
        ws.on_close = None
        del ws
        ws = None
        self.__reset_market = True
        logger.info(f"Stopped websocket for price")

    def __get_historical_data(self, unit_time):
        all_hist_data = []
        hist_data_2 = f'https://api.binance.com/api/v3/klines?symbol={self.coin.upper()}USDT&interval={unit_time}&limit=1000'
        hist_data_res_2 = requests.get(hist_data_2)
        if (hist_data_res_2.status_code == 200):
            data_2 = hist_data_res_2.json()
            hist_data_1 = f'https://api.binance.com/api/v3/klines?symbol={self.coin.upper()}USDT&interval={unit_time}&limit=441&endTime={data_2[0][0]}'
            hist_data_res_1 = requests.get(hist_data_1)
            if (hist_data_res_1.status_code == 200):
                data_1 = hist_data_res_1.json()
                # Remove the last element as it will be repeated
                data_1.pop()
                all_hist_data = data_1 + data_2
                # Validating the fist data that is collected
                bad_count = 0
                for index in range(len(all_hist_data)):
                    if (index > 0 and index < len(all_hist_data) - 1):
                        # If the difference between adjsent points should be unit time else data is not correct
                        if not(all_hist_data[index][0] - all_hist_data[index - 1][0] == all_constants.TIME_WINDOW_IN_MSEC.get(unit_time)):
                            bad_count = bad_count + 1
                # There seems to be two data data missing for 1 hr chart
                if (bad_count > 0 and not(unit_time == '1h')):
                    all_hist_data = []
                    logger.error(f"Data is not good {unit_time}")
                elif (bad_count > 2 and unit_time == '1h'):
                    all_hist_data = []
                    logger.error(f"Data is not good {unit_time}")
        return all_hist_data
    
    def __reset_trading_counter(self):
        for unit_time in all_constants.SUPPORTED_TIME_WINDOW:
            self.__start_trading_counter[unit_time] = 0
        self.__start_trading_counter["price"] = 0  
    
    def start_trading(self, trading_strategy_cls: IStrategy, config_path):
        # Getting data
        if (os.path.isfile(config_path) and os.path.exists(config_path)):
            user_configs = UserConfig(config_path).all_config
            while True:
                strategy_inst = trading_strategy_cls()
                self.__reset_market = False
                self.__reset_trading_counter()
                self.__trade_data.reset_all_data()
                for unit_time in all_constants.SUPPORTED_TIME_WINDOW:
                    threading.Thread(target=self.__start_candles,
                                        args=(unit_time,)).start()
                threading.Thread(target=self.__get_real_time_price).start()
                
                start = time.time()
                while not(self.__reset_market):
                    all_trade_sum = 0
                    for key in self.__start_trading_counter.keys():
                        all_trade_sum += self.__start_trading_counter[key]
                    
                    if all_trade_sum == len(all_constants.SUPPORTED_TIME_WINDOW) + 1:
                        # my_function_call(self.__trade_data)
                        strategy_inst.decide_and_notify(self.__trade_data, user_configs)
                        self.__reset_trading_counter()
                        end = time.time()
                        logger.debug(
                            f"Time taken to get next data {str(end - start)} sec")
                        start = time.time()
                logger.error("Market data getting reset")
        # all_trade_sum = 0
        # while all_trade_sum != len(all_constants.SUPPORTED_TIME_WINDOW) + 1:
        #     all_trade_sum = 0
        #     for key in self.__start_trading_counter.keys():
        #         all_trade_sum += self.__start_trading_counter[key]
        # self.start_trading = True
    
    # def on_data_update(self, my_function_call):


    # def track(self):
    #     # This to make sure to try till success
    #     while True:
    #         self.final_data.reset_all_data()
    #         self.reset_trading = True
    #         for unit_time in all_constants.SUPPORTED_TIME_WINDOW:
    #             threading.Thread(target=self.__start_candles,
    #                              args=(unit_time,)).start()

    #         threading.Thread(target=self.__get_real_time_price).start()
    #         # This to update check the status at regular intervals
    #         while self.reset_trading:
    #             time.sleep(.5)
    #             threading.Thread(target=self.snd_inst.send).start()
    #         # adding this delay to give time for all the websocke to get closed before restart
    #         time.sleep(5)

    # def __update_indicators(self, unit_time):
    #     start = time.time()
    #     for name in dir(self.__trade_data):
    #         if name.startswith('update_latest_'):
    #             m = getattr(self.__trade_data, name)
    #             m(unit_time)
    #     end = time.time()
    #     logger.debug(
    #         f"Time taken for indicator calculations {str(end - start)} sec")
