

from .plugin_config import Plugin_Config


class Plugin_Utils():
    """
    A wrapper for core functions for a plugin to have access to.
    """

    def __init__(self, config, logger, versions, plugin_name, plugin_manifest, modname, path):
        self.config = Plugin_Config(config, plugin_manifest["name"], logger)
        self.logger = logger
        self.versions = versions
        self.namespace = plugin_manifest["name"].lower()
        self.plugin_name = plugin_name
        self.plugin_manifest = plugin_manifest
        self.path = path
        self.origin = None
