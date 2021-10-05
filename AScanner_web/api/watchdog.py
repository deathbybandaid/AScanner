from flask import request, redirect
import urllib.parse


class WATCHDOG():
    """Methods to start/stop watchdog"""
    endpoints = ["/api/watchdog"]
    endpoint_name = "api_watchdog"
    endpoint_methods = ["GET", "POST"]

    def __init__(self, ascanner):
        self.ascanner = ascanner

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        method = request.args.get('method', default="start", type=str)

        redirect_url = request.args.get('redirect', default=None, type=str)

        if method == "start":

            self.ascanner.logger.info("Starting Watchdog Thread.")

            self.ascanner.watchdog.start()

        elif method == "stop":

            self.ascanner.logger.info("Stoping Watchdog Thread.")

            self.ascanner.watchdog.stop()

        else:
            return "%s Invalid Method" % method

        if redirect_url:
            if "?" in redirect_url:
                return redirect("%s&retmessage=%s" % (redirect_url, urllib.parse.quote("%s Success" % method)))
            else:
                return redirect("%s?retmessage=%s" % (redirect_url, urllib.parse.quote("%s Success" % method)))
        else:
            return "%s Success" % method
