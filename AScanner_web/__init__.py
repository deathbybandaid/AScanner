from gevent.pywsgi import WSGIServer
from flask import Flask, request, session
import threading
import uuid

from .pages import AScanner_Pages
from .files import AScanner_Files
from .brython import AScanner_Brython
from .api import AScanner_API


class AScanner_HTTP_Server():
    """
    AScanner_web HTTP Frontend.
    """

    app = None

    def __init__(self, ascanner):
        self.ascanner = ascanner

        self.template_folder = ascanner.config.internal["paths"]["www_templates_dir"]

        self.ascanner.logger.info("Loading Flask.")

        self.ascanner.app = Flask("AScanner", template_folder=self.template_folder)
        self.instance_id = str(uuid.uuid4())

        # Allow Internal API Usage
        self.ascanner.app.testing = True
        self.ascanner.api.client = self.ascanner.app.test_client()

        # Set Secret Key For Sessions
        self.ascanner.app.secret_key = self.ascanner.config.dict["ascanner"]["friendlyname"]

        self.route_list = {}

        self.endpoints_obj = {}
        self.endpoints_obj["brython"] = AScanner_Brython(ascanner)
        self.endpoints_obj["api"] = AScanner_API(ascanner)
        # Load Plugins before pages so they can override core web pages
        self.selfadd_web_plugins()
        self.endpoints_obj["pages"] = AScanner_Pages(ascanner)
        self.endpoints_obj["files"] = AScanner_Files(ascanner)

        for endpoint_type in list(self.endpoints_obj.keys()):
            self.ascanner.logger.info("Loading HTTP %s Endpoints." % endpoint_type)
            self.add_endpoints(endpoint_type)

        self.ascanner.app.before_request(self.before_request)
        self.ascanner.app.after_request(self.after_request)
        self.ascanner.app.before_first_request(self.before_first_request)

        self.ascanner.threads["flask"] = threading.Thread(target=self.run)

    def selfadd_web_plugins(self):
        """
        Import web Plugins.
        """

        for plugin_name in list(self.ascanner.plugins.plugins.keys()):
            if self.ascanner.plugins.plugins[plugin_name].type == "web":
                method = self.ascanner.plugins.plugins[plugin_name].name.lower()
                plugin_utils = self.ascanner.plugins.plugins[plugin_name].plugin_utils
                try:
                    self.endpoints_obj[method] = self.ascanner.plugins.plugins[plugin_name].Plugin_OBJ(self.ascanner, plugin_utils)
                except Exception as e:
                    self.ascanner.logger.error(e)

    def start(self):
        """
        Start Flask.
        """

        self.ascanner.logger.info("Flask HTTP Thread Starting")
        self.ascanner.threads["flask"].start()

    def stop(self):
        """
        Safely Stop Flask.
        """

        self.ascanner.logger.info("Flask HTTP Thread Stopping")
        self.http.stop()

    def before_first_request(self):
        """
        Handling before a first request can be handled.
        """

        self.ascanner.logger.info("HTTP Server Online.")

    def before_request(self):
        """
        Handling before a request is processed.
        """

        session["session_id"] = str(uuid.uuid4())
        session["instance_id"] = self.instance_id
        session["route_list"] = self.route_list

        session["user_agent"] = request.headers.get('User-Agent')

        session["is_internal_api"] = self.detect_internal_api(request)
        if session["is_internal_api"]:
            self.ascanner.logger.debug("Client is using internal API call.")

        session["is_mobile"] = self.detect_mobile(request)
        if session["is_mobile"]:
            self.ascanner.logger.debug("Client is a mobile device.")

        session["is_plexmediaserver"] = self.detect_plexmediaserver(request)
        if session["is_plexmediaserver"]:
            self.ascanner.logger.debug("Client is a Plex Media Server.")

        session["deviceauth"] = self.detect_plexmediaserver(request)

        session["restart"] = False

        self.ascanner.logger.debug("Client %s requested %s Opening" % (request.method, request.path))

    def after_request(self, response):
        """
        Handling after a request is processed.
        """

        self.ascanner.logger.debug("Client %s requested %s Closing" % (request.method, request.path))

        if not session["restart"]:
            return response

        else:
            return self.stop()

    def detect_internal_api(self, request):
        """
        Detect if accessed by internal API.
        """

        user_agent = request.headers.get('User-Agent')
        if not user_agent:
            return False
        elif str(user_agent).lower().startswith("ascanner"):
            return True
        else:
            return False

    def detect_deviceauth(self, request):
        """
        Detect if accessed with DeviceAuth.
        """

        return request.args.get('DeviceAuth', default=None, type=str)

    def detect_mobile(self, request):
        """
        Detect if accessed by mobile.
        """

        user_agent = request.headers.get('User-Agent')
        phones = ["iphone", "android", "blackberry"]

        if not user_agent:
            return False

        elif any(phone in user_agent.lower() for phone in phones):
            return True

        else:
            return False

    def detect_plexmediaserver(self, request):
        """
        Detect if accessed by plexmediaserver.
        """

        user_agent = request.headers.get('User-Agent')

        if not user_agent:
            return False

        elif str(user_agent).lower().startswith("plexmediaserver"):
            return True

        else:
            return False

    def add_endpoints(self, index_name):
        """
        Add Endpoints.
        """

        item_list = [x for x in dir(self.endpoints_obj[index_name]) if self.isapath(x)]
        endpoint_main = self.endpoints_obj[index_name]
        endpoint_main.ascanner.version  # dummy line
        for item in item_list:
            endpoints = eval("endpoint_main.%s.%s" % (item, "endpoints"))
            if isinstance(endpoints, str):
                endpoints = [endpoints]
            handler = eval("endpoint_main.%s" % item)
            endpoint_name = eval("endpoint_main.%s.%s" % (item, "endpoint_name"))

            try:
                endpoint_methods = eval("endpoint_main.%s.%s" % (item, "endpoint_methods"))
            except AttributeError:
                endpoint_methods = ['GET']

            try:
                endpoint_access_level = eval("endpoint_main.%s.%s" % (item, "endpoint_access_level"))
            except AttributeError:
                endpoint_access_level = 0

            try:
                pretty_name = eval("endpoint_main.%s.%s" % (item, "pretty_name"))
            except AttributeError:
                pretty_name = endpoint_name

            try:
                endpoint_category = eval("endpoint_main.%s.%s" % (item, "endpoint_category"))
            except AttributeError:
                endpoint_category = index_name

            try:
                endpoint_default_parameters = eval("endpoint_main.%s.%s" % (item, "endpoint_default_parameters"))
            except AttributeError:
                endpoint_default_parameters = {}

            endpoint_added = True
            try:
                for endpoint in endpoints:
                    self.add_endpoint(endpoint=endpoint,
                                      endpoint_name=endpoint_name,
                                      handler=handler,
                                      methods=endpoint_methods)

            except AssertionError:
                endpoint_added = False

            if endpoint_added:
                self.ascanner.logger.debug("Adding endpoint %s available at %s with %s methods." % (endpoint_name, ",".join(endpoints), ",".join(endpoint_methods)))

                if endpoint_category not in list(self.route_list.keys()):
                    self.route_list[endpoint_category] = {}

                if endpoint_name not in list(self.route_list[endpoint_category].keys()):
                    self.route_list[endpoint_category][endpoint_name] = {}

                self.route_list[endpoint_category][endpoint_name]["name"] = endpoint_name
                self.route_list[endpoint_category][endpoint_name]["endpoints"] = endpoints
                self.route_list[endpoint_category][endpoint_name]["endpoint_methods"] = endpoint_methods
                self.route_list[endpoint_category][endpoint_name]["endpoint_access_level"] = endpoint_access_level
                self.route_list[endpoint_category][endpoint_name]["endpoint_default_parameters"] = endpoint_default_parameters
                self.route_list[endpoint_category][endpoint_name]["pretty_name"] = pretty_name
                self.route_list[endpoint_category][endpoint_name]["endpoint_category"] = endpoint_category

    def isapath(self, item):
        """
        Ignore instances.
        """

        not_a_page_list = ["ascanner", "plugin_utils"]
        if item in not_a_page_list:
            return False

        elif item.startswith("__") and item.endswith("__"):
            return False

        else:
            return True

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET']):
        """
        Add Endpoint.
        """

        self.ascanner.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods)

    def run(self):
        """
        Run the WSGIServer.
        """

        self.http = WSGIServer(self.ascanner.api.address_tuple,
                               self.ascanner.app.wsgi_app,
                               log=self.ascanner.logger.logger,
                               error_log=self.ascanner.logger.logger)
        try:
            self.http.serve_forever()
            self.stop()
        except OSError as err:
            self.ascanner.logger.error("HTTP Server Offline: %s" % err)
        except AttributeError:
            self.ascanner.logger.info("HTTP Server Offline")
