import os
import time
import argparse
import pathlib
import json

from AScanner import AScanner_OBJ
import AScanner.exceptions
import AScanner.config
import AScanner.logger
import AScanner.plugins
import AScanner.versions
import AScanner.web

ERR_CODE = 1
ERR_CODE_NO_RESTART = 2


def build_args_parser(script_dir):
    """
    Build argument parser for AScanner.
    """

    parser = argparse.ArgumentParser(description='AScanner')
    parser.add_argument('-c', '--config', dest='cfg', type=str, default=pathlib.Path(script_dir).joinpath('config.ini'), required=False, help='configuration file to load.')
    parser.add_argument('--setup', dest='setup', type=str, required=False, nargs='?', const=True, default=False, help='Setup Configuration file.')
    parser.add_argument('--iliketobreakthings', dest='iliketobreakthings', type=str, nargs='?', const=True, required=False, default=False, help='Override Config Settings not meant to be overridden.')
    parser.add_argument('-v', '--version', dest='version', type=str, required=False, nargs='?', const=True, default=False, help='Show Version Number.')
    return parser.parse_args()


def run(settings, logger, script_dir, AScanner_web, plugins, versions, web, deps):
    """
    Create AScanner and fHDHH_web objects, and run threads.
    """

    ascanner = AScanner_OBJ(settings, logger, plugins, versions, web, deps)
    ascannerweb = AScanner_web.AScanner_HTTP_Server(ascanner)

    try:

        # Start Flask Thread
        ascannerweb.start()

        # Perform some actions now that HTTP Server is running
        ascanner.api.get("/api/startup_tasks")

        logger.info("AScanner and AScanner_web should now be running and accessible via the web interface at %s" % ascanner.api.base)

        # wait forever
        restart_code = "restart"
        while ascanner.threads["flask"].is_alive():
            time.sleep(1)

        return restart_code

    except KeyboardInterrupt:
        return ERR_CODE_NO_RESTART

    return ERR_CODE


def start(args, script_dir, AScanner_web, deps):
    """
    Get Configuration for AScanner and start.
    """

    try:
        settings = AScanner.config.Config(args, script_dir)
    except AScanner.exceptions.ConfigurationError as e:
        print(e)
        return ERR_CODE_NO_RESTART

    # Setup Logging
    logger = AScanner.logger.Logger(settings)
    settings.logger = logger

    # Setup Version System
    versions = AScanner.versions.Versions(settings, logger)

    loading_versions_string = ""
    core_versions = versions.get_core_versions()
    for item in list(core_versions.keys()):
        if loading_versions_string != "":
            spaceprefix = ", "
        else:
            spaceprefix = " "
        loading_versions_string += "%s%s %s" % (spaceprefix, core_versions[item]["name"], core_versions[item]["version"])

    logger.info("Loading %s" % loading_versions_string)

    logger.info("Importing Core config values from Configuration File: %s" % settings.config_file)

    logger.debug("Logging to File: %s" % os.path.join(settings.internal["paths"]["logs_dir"], '.AScanner.log'))

    # Continue non-core settings setup
    settings.secondary_setup()

    logger.debug("Setting Up shared Web Requests system.")
    web = AScanner.web.WebReq()

    # Continue Version System Setup
    versions.secondary_setup(web)

    # Find Plugins and import their default configs
    plugins = AScanner.plugins.PluginsHandler(settings, logger, versions, deps)

    return run(settings, logger, script_dir, AScanner_web, plugins, versions, web, deps)


def config_setup(args, script_dir, AScanner_web):
    """
    Setup Config file.
    """

    settings = AScanner.config.Config(args, script_dir, AScanner_web)
    AScanner.plugins.PluginsHandler(settings)
    settings.setup_user_config()
    return ERR_CODE


def main(script_dir, AScanner_web, deps):
    """
    AScanner run script entry point.
    """

    try:
        args = build_args_parser(script_dir)

        if args.version:
            versions_string = ""
            version_file = pathlib.Path(script_dir).joinpath("version.json")
            with open(version_file, 'r') as jsonversion:
                core_versions = json.load(jsonversion)
            for item in list(core_versions.keys()):
                if versions_string != "":
                    spaceprefix = ", "
                else:
                    spaceprefix = ""
                versions_string += "%s%s %s" % (spaceprefix, item, core_versions[item])
            print(versions_string)

        if args.setup:
            return config_setup(args, script_dir, AScanner_web)

        while True:

            returned_code = start(args, script_dir, AScanner_web, deps)
            if returned_code not in ["restart"]:
                return returned_code

    except KeyboardInterrupt:
        print("\n\nInterrupted")
        return ERR_CODE


if __name__ == '__main__':
    """
    Trigger main function.
    """
    main()
