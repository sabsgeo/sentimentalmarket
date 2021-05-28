import threading
import time
import json
import sys

import websocket

from historical_data import HistoricalData
from send_notifocations import SendNotification
from config import all_configs


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
        close = candle['c']
        unit_time = candle['i']

        if is_candle_closed:
            self.final_data.update_close_rate(float(close), unit_time)
            self.final_data.update_latest_rsi(unit_time)

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
            time.sleep(1)
