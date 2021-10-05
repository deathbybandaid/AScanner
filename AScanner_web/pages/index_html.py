from flask import request, render_template, session


class Index_HTML():
    endpoints = ["/index", "/index.html"]
    endpoint_name = "page_index_html"
    endpoint_access_level = 0
    pretty_name = "Index"

    def __init__(self, ascanner):
        self.ascanner = ascanner

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        ascanner_status_dict = {
                            "Script Directory": str(self.ascanner.config.internal["paths"]["script_dir"]),
                            "Config File": str(self.ascanner.config.config_file),
                            "Cache Path": str(self.ascanner.config.internal["paths"]["cache_dir"]),
                            "Logging Level": self.ascanner.config.dict["logging"]["level"],
                            "Watchdog Running": self.ascanner.watchdog.status,
                            }

        ascanner_status_dict["Total Plugins"] = len(list(self.ascanner.plugins.plugins.keys()))
        if self.ascanner.config.internal["paths"]["external_plugins_dir"]:
            ascanner_status_dict["Plugins Path"] = ", ".join([
             str(self.ascanner.config.internal["paths"]["internal_plugins_dir"]),
             str(self.ascanner.config.internal["paths"]["external_plugins_dir"])
             ])
        else:
            ascanner_status_dict["Plugins Path"] = str(self.ascanner.config.internal["paths"]["internal_plugins_dir"])

        return render_template('index.html', request=request, session=session, ascanner=self.ascanner, ascanner_status_dict=ascanner_status_dict, list=list)
