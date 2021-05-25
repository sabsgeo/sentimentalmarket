import send_notifocations
import historical_data
import decorators
import config
import websocket
import asyncio
from binance.enums import *
from binance.client import Client
import sys
import time
import json

# For the warning
# MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors,
# including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3.7.
# Please monkey-patch earlier
# https://stackoverflow.com/questions/56309763/grequests-monkey-patch-warning
from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)


supported_coins = ['eth']

try:
    coin = sys.argv[1]
except:
    print(
        f"Cryptocurrency should be the 1st argument. Supported coins are {supported_coins}")
    sys.exit(1)
    pass

try:
    bot_key = sys.argv[2]
except:
    print(f"Bot key should be 2nd argument")
    sys.exit(1)
    pass

try:
    channel_id = sys.argv[3]
except:
    print(f"Channel ID should be 3rd argument")
    sys.exit(1)
    pass
print(coin)
print(bot_key)
print(channel_id)

if not(coin in supported_coins):
    joined_coin = ",".join(supported_coins)
    print(f"Coin not supported. Supported coins are {supported_coins}")
    sys.exit(1)

# Global Data initilization
final_data = historical_data.HistoricalData()
final_data.currency = coin
snd_inst = send_notifocations.SendNotification(final_data, bot_key, channel_id)


def on_open(ws):
    print('open connection')


def on_close(ws):
    print('close connection')


@decorators.background
def candle_stick_listner(coin, unit_time):
    def on_candle_message(ws, message):
        global final_data
        json_message = json.loads(message)

        candle = json_message['k']
        is_candle_closed = candle['x']
        close = candle['c']
        unit_time = candle['i']

        if is_candle_closed:
            final_data.update_close_rate(float(close), unit_time)
            final_data.update_latest_rsi(unit_time)

    created_url = f'wss://stream.binance.com:9443/ws/{coin}usdt@kline_{unit_time}'
    ws = websocket.WebSocketApp(created_url, on_open=on_open,
                                on_close=on_close, on_message=on_candle_message)
    ws.run_forever()


@decorators.background
def get_real_time_price(coin):
    created_url = f'wss://stream.binance.com:9443/ws/{coin}usdt@trade'

    def on_price_message(ws, message):
        global final_data
        final_data.current_price = json.loads(message)['p']
    ws = websocket.WebSocketApp(created_url, on_open=on_open,
                                on_close=on_close, on_message=on_price_message)
    ws.run_forever()


for unit_time in config.TECHNICAL_INDICATOR_CONF.get('TIME_WINDOW'):
    candle_stick_listner(coin, unit_time)

get_real_time_price(coin)

while True:
    time.sleep(.5)
    snd_inst.send()
