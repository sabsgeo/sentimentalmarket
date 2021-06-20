import json
import os
from sentimentalmarket.constants import all_constants
from box import box_from_file


class UserConfig():

    def __init__(self, user_config_path):
        if not (os.path.isfile(user_config_path) and os.path.exists(user_config_path)):
            raise Exception("Config file path is not valid or does not exist")
        
        file_obj = open(user_config_path)
        self.all_config = json.load(file_obj)
        self.all_config = box_from_file(user_config_path, frozen_box=True)
                
        coin = self.all_config.coin
        if not(coin in all_constants.SUPPORTED_COINS):
            joined_coin = ",".join(all_constants.SUPPORTED_COINS)
            raise Exception(f"Coin not supported. Supported coins are {joined_coin}")
