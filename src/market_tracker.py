import threading
import time
import json
import sys

import websocket
import requests

from historical_data import HistoricalData
from send_notifocations import SendNotification
from config import all_configs
from constants import all_constants


class MarketTracker():

    def __init__(self, coin, bot_key, channel_id):
        self.final_data = HistoricalData()
        self.coin = coin
        self.final_data.currency = coin
        self.snd_inst = SendNotification(self.final_data, bot_key, channel_id)
        self.websoc_collection = {}
        self.run_till_end = False

    def __on_open(self, ws):
        print('open connection')

    def __on_error(self, ws, error):
        print(error)
        for each_type in self.websoc_collection:
            if (self.websoc_collection[each_type] is not None):
                self.websoc_collection[each_type].close()

    def __trading_calculation(self, message):
        json_message = json.loads(message)

        candle = json_message['k']
        is_candle_closed = candle['x']
        unit_time = candle['i']
        
        if (len(self.final_data.closes[unit_time]) == 0):
            hist_data = f'https://api.binance.com/api/v3/klines?symbol={self.coin.upper()}USDT&interval={unit_time}'
            hist_data_res = requests.get(hist_data)
            if (hist_data_res.status_code == 200):
                all_hist_data = hist_data_res.json()
                start = time.time()
                self.final_data.initilize_candle_data(all_hist_data, unit_time)
                self.final_data.update_latest_rsi(unit_time)
                self.final_data.update_latest_macd(unit_time)
                end = time.time()
                if (all_configs.IS_DEBUG):
                    print(f"Time taken for initial indicator calculations {str(end - start)} sec")
        
        # This condition makes sure that collection of real time data happens if
        # latest candle stick is closed and the historical data is filled 
        if (is_candle_closed and len(self.final_data.closes[unit_time]) > 0):
            start = time.time()
            self.final_data.update_candle_data(candle, unit_time)
            self.final_data.update_latest_rsi(unit_time)
            self.final_data.update_latest_macd(unit_time)
            end = time.time()
            if (all_configs.IS_DEBUG):
                print(f"Time taken for indicator calculations {str(end - start)} sec")
            
            if (unit_time == all_constants.ONE_MIN_STRING and self.final_data.close_count == 0):
                # giving this 5 second delay to mke sure all other have done calculation
                time.sleep(5)
                # closing 1 will reset all
                self.websoc_collection[all_constants.ONE_MIN_STRING].close()

    def __on_message_candle_stick(self, ws, message):
        threading.Thread(target=self.__trading_calculation,
                         args=(message,)).start()

    def __start_candles(self, unit_time):
        created_url = f'wss://stream.binance.com:9443/ws/{self.coin}usdt@kline_{unit_time}'
        ws = websocket.WebSocketApp(created_url, on_open=self.__on_open,
                                    on_error=self.__on_error, on_message=self.__on_message_candle_stick)
        self.websoc_collection[unit_time] = ws
        ws.run_forever()

        for each_type in self.websoc_collection:
            if (self.websoc_collection[each_type] is not None):
                self.websoc_collection[each_type].close()
        # on close
        self.run_till_end = False
        ws.on_message = None
        ws.on_open = None
        ws.on_close = None    
        del ws
        ws = None
        print(f"Stopped websocket for {unit_time}")

    def __on_price_msg(self, ws, message):
        self.final_data.current_price = json.loads(message)['p']

    def __get_real_time_price(self):
        created_url = f'wss://stream.binance.com:9443/ws/{self.coin}usdt@trade'
        ws = websocket.WebSocketApp(created_url, on_open=self.__on_open,
                                    on_error=self.__on_error, on_message=self.__on_price_msg)
        self.websoc_collection['price'] = ws
        ws.run_forever()

        for each_type in self.websoc_collection:
            if (self.websoc_collection[each_type] is not None):
                self.websoc_collection[each_type].close()
        # on close
        self.run_till_end = False
        ws.on_message = None
        ws.on_open = None
        ws.on_close = None
        del ws
        ws = None
        print(f"Stopped websocket for price")

    def track(self):
        # This to make sure to try till success
        while True:
            self.final_data.reset_all_data()
            self.run_till_end = True
            for unit_time in all_configs.TECHNICAL_INDICATOR_CONF.get('TIME_WINDOW'):
                threading.Thread(target=self.__start_candles,
                                args=(unit_time,)).start()

            threading.Thread(target=self.__get_real_time_price).start()
            # This to update check the status at regular intervals
            while self.run_till_end:
                time.sleep(.5)
                threading.Thread(target=self.snd_inst.send).start()
            # adding this delay to give time for all the websocke to get closed before restart
            time.sleep(5)
