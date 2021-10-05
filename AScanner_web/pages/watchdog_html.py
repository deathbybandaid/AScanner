from flask import request, render_template, session


class Watchdog_HTML():
    endpoints = ["/watchdog", "/watchdog.html"]
    endpoint_name = "page_watchdog_html"
    endpoint_access_level = 1
    pretty_name = "Watchdog"

    def __init__(self, ascanner):
        self.ascanner = ascanner

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        watchdog_dict = {}
        for directory in list(self.ascanner.watchdog.directories.keys()):
            watchdog_dict[directory] = {
                "recursive": self.ascanner.watchdog.directories[directory]["recursive"]
                }

        return render_template('watchdog.html', request=request, session=session, ascanner=self.ascanner, watchdog_dict=watchdog_dict, list=list)
