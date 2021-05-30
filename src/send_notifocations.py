import json

import grequests

from historical_data import HistoricalData
from constants import all_constants
from config import all_configs


class SendNotification():

    # RSI data for checks
    prev_rsi = json.dumps(all_constants.EMPTY_UNIT_DICT)
    prev_high_rsi_data = dict(all_constants.EMPTY_UNIT_DICT)
    prev_low_rsi_data = dict(all_constants.EMPTY_UNIT_DICT)

    # MACD checks
    prev_macd = json.dumps(all_constants.EMPTY_UNIT_DICT)

    def __init__(self, hd_instance: HistoricalData, bot_key, channel_id):
        self.historical_data_instance = hd_instance
        self.bot_key = bot_key
        self.channel_id = channel_id

    def __notification_request(self, message):
        def do_something(response, *args, **kwargs):
            print('Notification send')

        send_message_url = f'https://api.telegram.org/bot{self.bot_key}/sendMessage?chat_id={self.channel_id}&text={message}&parse_mode=markdown'
        req = grequests.post(send_message_url, hooks={
                             'response': do_something})
        job = grequests.send(req, grequests.Pool(1))

    def __rsi_notification(self):
        for unit_time in self.historical_data_instance.latest_rsi.keys():
            for each_rsi in self.historical_data_instance.latest_rsi[unit_time].keys():
                current_value = self.historical_data_instance.latest_rsi[unit_time][each_rsi]
                notification_text = None
                if(current_value > all_configs.TECHNICAL_INDICATOR_CONF.get('RSI').get('OVER_SOLD')):
                    self.prev_low_rsi_data[unit_time][each_rsi] = -1
                    pre_high_rsi_val = -1
                    try:
                        pre_high_rsi_val = self.prev_high_rsi_data[unit_time][each_rsi]
                    except:
                        pass

                    if (pre_high_rsi_val == -1):
                        notification_text = f'{self.historical_data_instance.currency} over valued at {self.historical_data_instance.current_price} with rsi({each_rsi}) of time unit {unit_time}'
                    elif (current_value < pre_high_rsi_val):
                        notification_text = f'{self.historical_data_instance.currency} is going down from max {self.historical_data_instance.current_price} with rsi({each_rsi}) of time unit {unit_time}'

                    self.prev_high_rsi_data[unit_time][each_rsi] = current_value

                    return notification_text
                elif (current_value < all_configs.TECHNICAL_INDICATOR_CONF.get('RSI').get('OVER_SOLD') and current_value > all_configs.TECHNICAL_INDICATOR_CONF.get('RSI').get('UNDER_SOLD')):
                    self.prev_high_rsi_data[unit_time][each_rsi] = -1
                    self.prev_low_rsi_data[unit_time][each_rsi] = -1
                    return None
                elif (current_value < all_configs.TECHNICAL_INDICATOR_CONF.get('RSI').get('UNDER_SOLD')):
                    self.prev_high_rsi_data[unit_time][each_rsi] = -1
                    pre_low_rsi_val = -1
                    try:
                        pre_low_rsi_val = self.prev_low_rsi_data[unit_time][each_rsi]
                    except:
                        pass
                    if (pre_low_rsi_val == -1):
                        notification_text = f'{self.historical_data_instance.currency} under valued at {self.historical_data_instance.current_price} with rsi({each_rsi}) of time unit {unit_time}'
                    elif (current_value > pre_low_rsi_val):
                        notification_text = f'{self.historical_data_instance.currency} is going up from under valued at {self.historical_data_instance.current_price} with rsi({each_rsi}) of time unit {unit_time}'
                    self.prev_low_rsi_data[unit_time][each_rsi] = current_value

                    return notification_text

    def send(self):
        if not(self.historical_data_instance.latest_rsi == all_constants.EMPTY_UNIT_DICT):
            if not(self.prev_rsi == json.dumps(self.historical_data_instance.latest_rsi)):
                print("rsi")
                print(self.historical_data_instance.latest_rsi)
                value = self.__rsi_notification()
                if value:
                    print(value)
                    self.__notification_request(value)
                self.prev_rsi = json.dumps(
                    self.historical_data_instance.latest_rsi)

        if not(self.historical_data_instance.latest_macd == all_constants.EMPTY_UNIT_DICT):
            if not(self.prev_macd == json.dumps(self.historical_data_instance.latest_macd)):
                print("macd")
                print(self.historical_data_instance.latest_macd)
                self.prev_macd = json.dumps(
                    self.historical_data_instance.latest_macd)
