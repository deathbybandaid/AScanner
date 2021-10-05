from flask import request


class Fake_Plex_Autoscan_API():
    endpoints = ["/<apikey>"]
    endpoint_name = "api_fake_plex_autoscan"
    endpoint_methods = ["GET", "POST"]

    def __init__(self, plugin_utils):
        self.plugin_utils = plugin_utils

    def __call__(self, apikey, *args):
        return self.get(apikey, *args)

    def get(self, apikey, *args):

        # TODO This will emulate the old plex_autoscan

        return "Success %s" % request
