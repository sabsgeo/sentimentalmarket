import sys
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# For the warning
# MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors,
# including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3.7.
# Please monkey-patch earlier
# https://stackoverflow.com/questions/56309763/grequests-monkey-patch-warning
from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)

# from market_data_tracker import MarketDataTracker
from start_trading import StartTrading
from arg_parser import parse_args

coin, bot_key, channel_id = parse_args(sys.argv)

logger.info(f"Running the docker for coin {coin} notification will be send to channel id {channel_id} using api key {bot_key}")

if __name__ == "__main__":
    trade = StartTrading(coin)
    trade.trade()
    # markt = MarketDataTracker(coin, bot_key, channel_id)
    # markt.track()
