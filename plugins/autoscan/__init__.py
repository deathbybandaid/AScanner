import urllib.parse


class Plugin_OBJ():

    def __init__(self, ascanner, plugin_utils):
        self.ascanner = ascanner
        self.plugin_utils = plugin_utils

    @property
    def username(self):
        return self.plugin_utils.config.dict["autoscan"]["username"]

    @property
    def password(self):
        return self.plugin_utils.config.dict["autoscan"]["password"]

    @property
    def address(self):
        return self.plugin_utils.config.dict["autoscan"]["address"]

    @property
    def port(self):
        return self.plugin_utils.config.dict["autoscan"]["port"]

    @property
    def proto(self):
        return "https://" if self.plugin_utils.config.dict['autoscan']["ssl"] else "http://"

    @property
    def enabled(self):
        return self.plugin_utils.config.dict["autoscan"]["enabled"]

    @property
    def address_full(self):
        return '%s%s:%s' % (self.proto, self.address, str(self.port))

    def dispatch(self, event):
        if self.enabled:
            self.plugin_utils.logger.info("autoscan is enabled. Processing...")
            if not event.is_directory:
                self.post(event.src_path)
            else:
                self.plugin_utils.logger.info("%s is a directory, skipping." % event.src_path)

    def post(self, filepath):

        self.plugin_utils.logger.info("Sending path to autoscan at %s : %s " % (self.address_full, filepath))

        url_headers = {'Authorization': 'Basic %s' % self.password}

        try:

            scanpost = self.plugin_utils.web.session.post(
                "%s/triggers/manual?dir=%s" % (self.address_full, urllib.parse.quote(filepath)),
                headers=url_headers,
                auth=(self.username, self.password)
                )

            scanpost.raise_for_status()

        except self.plugin_utils.web.exceptions.HTTPError as err:
            self.plugin_utils.logger.error("Sending path to autoscan failed : %s " % err)
