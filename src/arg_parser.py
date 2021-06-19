import sys
import logging
logger = logging.getLogger(__name__)

from sentimentalmarket import all_constants


def parse_args(all_args):
    supported_coins = all_constants.SUPPORTED_COINS
    try:
        coin = all_args[1]
    except:
        logger.error(
            f"Cryptocurrency should be the 1st argument. Supported coins are {supported_coins}")
        sys.exit(1)
        pass

    try:
        bot_key = all_args[2]
    except:
        logger.error(f"Bot key should be 2nd argument")
        sys.exit(1)
        pass

    try:
        channel_id = all_args[3]
    except:
        logger.error(f"Channel ID should be 3rd argument")
        sys.exit(1)
        pass

    if not(coin in supported_coins):
        joined_coin = ",".join(supported_coins)
        logger.error(f"Coin not supported. Supported coins are {joined_coin}")
        sys.exit(1)

    return coin, bot_key, channel_id
