from flask import request, redirect, Response
import urllib.parse
import json


class Versions():
    endpoints = ["/api/versions"]
    endpoint_name = "api_versions"
    endpoint_methods = ["GET", "POST"]

    def __init__(self, ascanner):
        self.ascanner = ascanner

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        method = request.args.get('method', default="get", type=str)
        redirect_url = request.args.get('redirect', default=None, type=str)

        if method == "get":

            version_dict = {}
            for key in list(self.ascanner.versions.dict.keys()):
                version_dict[key] = self.ascanner.versions.dict[key]
                online_version = "N/A"
                if key in list(self.ascanner.versions.official_plugins.keys()):
                    online_version = self.ascanner.versions.official_plugins[key]["version"]
                version_dict[key]["online_version"] = online_version

            # Sort the Version Info
            sorted_version_list = sorted(version_dict, key=lambda i: (version_dict[i]['type'], version_dict[i]['name']))
            sorted_version_dict = {
                                    "AScanner": version_dict["ascanner"],
                                    "AScanner_web": version_dict["AScanner_web"]
                                    }
            for version_item in sorted_version_list:
                if version_item not in ["AScanner", "AScanner_web"]:
                    sorted_version_dict[version_item] = version_dict[version_item]

            return_json = json.dumps(sorted_version_dict, indent=4)

            return Response(status=200,
                            response=return_json,
                            mimetype='application/json')

        elif method == "online":

            available_version_dict = {}
            for key in list(self.ascanner.versions.official_plugins.keys()):
                if key not in list(self.ascanner.versions.dict.keys()):
                    available_version_dict[key] = self.ascanner.versions.official_plugins[key]

            # Sort the Version Info
            sorted_available_version_list = sorted(available_version_dict, key=lambda i: (available_version_dict[i]['type'], available_version_dict[i]['name']))
            sorted_available_version_dict = {}
            for version_item in sorted_available_version_list:
                if version_item:
                    sorted_available_version_dict[version_item] = available_version_dict[version_item]

            return_json = json.dumps(sorted_available_version_dict, indent=4)

            return Response(status=200,
                            response=return_json,
                            mimetype='application/json')

        elif method == "check":
            self.ascanner.versions.get_online_versions()

        elif method == "update":
            return "Not Implemented"

        if redirect_url:
            if "?" in redirect_url:
                return redirect("%s&retmessage=%s" % (redirect_url, urllib.parse.quote("%s Success" % method)))
            else:
                return redirect("%s?retmessage=%s" % (redirect_url, urllib.parse.quote("%s Success" % method)))
        else:
            return "%s Success" % method
