import sys

# For the warning
# MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors,
# including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3.7.
# Please monkey-patch earlier
# https://stackoverflow.com/questions/56309763/grequests-monkey-patch-warning
from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)

from market_tracker import MarketTracker
from config import all_configs

supported_coins = all_configs.TECHNICAL_INDICATOR_CONF.get("SUPPORTED_COINS")

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

if not(coin in supported_coins):
    joined_coin = ",".join(supported_coins)
    print(f"Coin not supported. Supported coins are {supported_coins}")
    sys.exit(1)

print(f"Running the docker for coin {coin} notification will be send to channel id {channel_id} using api key {bot_key}")

if __name__ == "__main__":
    markt = MarketTracker(coin, bot_key, channel_id)
    markt.track()
