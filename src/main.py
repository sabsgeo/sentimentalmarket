# For the warning
# MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors,
# including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3.7.
# Please monkey-patch earlier
# https://stackoverflow.com/questions/56309763/grequests-monkey-patch-warning
from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)

import sys
import os
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
sentry_sdk.init(
    dsn=os.getenv("SENTRY_URL_CTB"),
    integrations=[sentry_logging]
)

from sentimentalmarket.market_data_tracker import MarketDataTracker
from sentimentalmarket.trading_data import TradingData
from algorithms.trending_lines import cal_support_and_resistance
from arg_parser import parse_args

coin, bot_key, channel_id = parse_args(sys.argv)

logger.info(f"Running the docker for coin {coin} notification will be send to channel id {channel_id} using api key {bot_key}")

def trading_mechanism(marker_data: TradingData):
    s_r = marker_data.all_data["4h"].tail(60)
    print(cal_support_and_resistance(s_r))

if __name__ == "__main__":
    market_data = MarketDataTracker(coin)
    market_data.start_data_collection(trading_mechanism)
