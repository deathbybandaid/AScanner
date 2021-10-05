# coding=utf-8

from .aswatchdog import ASWatchdog
from .api import AScanner_API_URLs


class AScanner_INT_OBJ():

    def __init__(self, settings, logger, plugins, versions, web, deps):
        """
        An internal catalogue of core methods.
        """

        self.versions = versions
        self.version = versions.dict["AScanner"]["version"]
        self.config = settings
        self.plugins = plugins
        self.logger = logger
        self.web = web
        self.deps = deps

        for plugin_name in list(self.plugins.plugins.keys()):
            self.plugins.plugins[plugin_name].plugin_utils.web = self.web

        self.api = AScanner_API_URLs(settings, self.web, versions, logger)
        for plugin_name in list(self.plugins.plugins.keys()):
            self.plugins.plugins[plugin_name].plugin_utils.api = self.api

        self.threads = {}


class AScanner_OBJ():

    def __init__(self, settings, logger, plugins, versions, web, deps):
        """
        The Core Backend.
        """

        logger.info("Initializing AScanner Core Functions.")
        self.ascanner = AScanner_INT_OBJ(settings, logger, plugins, versions, web, deps)

        self.targets = {}
        self.ascanner.targets = self.targets

        self.ascanner.logger.info("Detecting and Opening any found target plugins.")
        for plugin_name in list(self.ascanner.plugins.plugins.keys()):
            if self.ascanner.plugins.plugins[plugin_name].manifest["type"] in ["target", "web"]:
                method = self.ascanner.plugins.plugins[plugin_name].name.lower()
                plugin_utils = self.ascanner.plugins.plugins[plugin_name].plugin_utils
                self.targets[method] = self.ascanner.plugins.plugins[plugin_name].Plugin_OBJ(self.ascanner, plugin_utils)

        self.watchdog = ASWatchdog(self.ascanner)

    def __getattr__(self, name):
        """
        Quick and dirty shortcuts. Will only get called for undefined attributes.
        """

        if hasattr(self.ascanner, name):
            return eval("self.ascanner.%s" % name)
