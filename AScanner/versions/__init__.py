import os
import sys
import platform
import re
import pathlib
import json


class Versions():
    """
    AScanner versioning management system.
    """

    def __init__(self, settings, logger):
        self.config = settings
        self.logger = logger

        self.github_ascanner_core_info_url = "https://raw.githubusercontent.com/deathbybandaid/AScanner/main/version.json"

        self.dict = {}
        self.official_plugins = {}
        self.core_versions = {}

        self.register_ascanner()

        self.register_env()

    def secondary_setup(self, web):
        self.web = web
        self.get_online_versions()

    def get_online_versions(self):
        """
        Update Onling versions listing.
        """
        return

    def get_core_versions(self):
        returndict = {}
        for item in list(self.dict.keys()):
            if self.dict[item]["type"] == "AScanner":
                returndict[item] = self.dict[item].copy()
        return returndict

    def register_version(self, item_name, item_version, item_type):
        """
        Register a version item.
        """

        self.logger.debug("Registering %s item: %s %s" % (item_type, item_name, item_version))
        self.dict[item_name] = {
                                "name": item_name,
                                "version": item_version,
                                "type": item_type
                                }

    def register_ascanner(self):
        """
        Register core version items.
        """

        script_dir = self.config.internal["paths"]["script_dir"]
        version_file = pathlib.Path(script_dir).joinpath("version.json")
        with open(version_file, 'r') as jsonversion:
            versions = json.load(jsonversion)

        for key in list(versions.keys()):
            self.register_version(key, versions[key], "AScanner")

    def is_docker(self):
        path = "/proc/self/cgroup"
        if not os.path.isfile(path):
            return False
        with open(path) as f:
            for line in f:
                if re.match("\d+:[\w=]+:/docker(-[ce]e)?/\w+", line):
                    return True
            return False

    def is_virtualenv(self):
        # return True if started from within a virtualenv or venv
        base_prefix = getattr(sys, "base_prefix", None)
        # real_prefix will return None if not in a virtualenv enviroment or the default python path
        real_prefix = getattr(sys, "real_prefix", None) or sys.prefix
        return base_prefix != real_prefix

    def register_env(self):
        """
        Register env version items.
        """

        self.register_version("Python", sys.version, "env")
        if sys.version_info.major == 2 or sys.version_info < (3, 7):
            self.logger.error('Error: AScanner requires python 3.7+. Do NOT expect support for older versions of python.')

        opersystem = platform.system()
        self.register_version("Operating System", opersystem, "env")

        if opersystem in ["Linux", "Darwin"]:

            # Linux/Mac
            if os.getuid() == 0 or os.geteuid() == 0:
                self.logger.warning('Do not run AScanner with root privileges.')

        elif opersystem in ["Windows"]:

            # Windows
            if os.environ.get("USERNAME") == "Administrator":
                self.logger.warning('Do not run AScanner as Administrator.')

        else:
            self.logger.warning("Uncommon Operating System, use at your own risk.")

        isvirtualenv = self.is_virtualenv()
        self.register_version("Virtualenv", isvirtualenv, "env")

        isdocker = self.is_docker()
        self.register_version("Docker", isdocker, "env")

    def register_plugins(self, plugins):
        """
        Register plugin version items.
        """

        self.logger.info("Scanning Plugins for Version Information.")
        self.plugins = plugins
        plugin_names = []
        for plugin in list(self.plugins.plugins.keys()):

            if self.plugins.plugins[plugin].plugin_name not in plugin_names:
                plugin_names.append(self.plugins.plugins[plugin].plugin_name)
                self.register_version(self.plugins.plugins[plugin].plugin_name, self.plugins.plugins[plugin].manifest["version"], "plugin")
