# For the warning
# MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors,
# including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3.7.
# Please monkey-patch earlier
# https://stackoverflow.com/questions/56309763/grequests-monkey-patch-warning

from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)

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

from .constants import all_constants
from .trading_data import TradingData
from .market_data_tracker import MarketDataTracker
from .strategy import IStrategy