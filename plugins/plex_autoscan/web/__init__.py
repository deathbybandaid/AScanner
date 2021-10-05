from .fake_plex_autoscan_api import Fake_Plex_Autoscan_API


class Plugin_OBJ():

    def __init__(self, ascanner, plugin_utils):
        self.ascanner = ascanner
        self.plugin_utils = plugin_utils

        self.fake_plex_autoscan_api = Fake_Plex_Autoscan_API(plugin_utils)
