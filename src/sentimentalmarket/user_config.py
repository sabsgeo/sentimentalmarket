import json


class UserConfig():

    def __init__(self, config_path):
        file_obj = open(config_path)
        self.all_config = json.load(file_obj)
