

class Plugin_OBJ():

    def __init__(self, ascanner, plugin_utils):
        self.ascanner = ascanner
        self.plugin_utils = plugin_utils

    @property
    def username(self):
        return self.plugin_utils.config.dict["plex_autoscan"]["username"]

    @property
    def password(self):
        return self.plugin_utils.config.dict["plex_autoscan"]["password"]

    @property
    def address(self):
        return self.plugin_utils.config.dict["plex_autoscan"]["address"]

    @property
    def port(self):
        return self.plugin_utils.config.dict["plex_autoscan"]["port"]

    @property
    def proto(self):
        return "https://" if self.plugin_utils.config.dict['plex_autoscan']["ssl"] else "http://"

    @property
    def enabled(self):
        return self.plugin_utils.config.dict["plex_autoscan"]["enabled"]

    @property
    def address_full(self):
        return '%s%s:%s' % (self.proto, self.address, str(self.port))

    def dispatch(self, event):
        if self.enabled:
            self.plugin_utils.logger.info("plex_autoscan is enabled. Processing...")
            if not event.is_directory:
                self.post(event.src_path)
            else:
                self.plugin_utils.logger.info("%s is a directory, skipping." % event.src_path)

    def post(self, filepath):
        self.plugin_utils.logger.info("Sending path to plex_autoscan at %s : %s " % (self.address_full, filepath))

        url_headers = {'Content-Type': 'application/json'}
        postdata = ('{"eventType":"' + "Manual" +
                    '","filepath":"' + filepath +
                    '"}').encode("utf-8")

        try:

            scanpost = self.plugin_utils.web.session.post(
                "%s/%s" % (self.address_full, self.password),
                data=postdata,
                headers=url_headers
                )

            scanpost.raise_for_status()

        except self.plugin_utils.web.exceptions.HTTPError as err:
            self.plugin_utils.logger.error("Sending path to plex_autoscan failed : %s " % err)
