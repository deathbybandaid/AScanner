from flask import request, render_template, session


class Versions_HTML():
    endpoints = ["/versions", "/versions.html"]
    endpoint_name = "page_versions_html"
    endpoint_access_level = 1
    endpoint_category = "tool_pages"
    pretty_name = "Versions"

    def __init__(self, ascanner):
        self.ascanner = ascanner

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        version_dict = {}
        for key in list(self.ascanner.versions.dict.keys()):
            version_dict[key] = self.ascanner.versions.dict[key]
            online_version = "N/A"
            if key in list(self.ascanner.versions.core_versions.keys()):
                online_version = self.ascanner.versions.core_versions[key]["version"]
            elif key in list(self.ascanner.versions.official_plugins.keys()):
                online_version = self.ascanner.versions.official_plugins[key]["version"]
            version_dict[key]["online_version"] = online_version

        # Sort the Version Info
        sorted_version_dict = {}
        for item in list(version_dict.keys()):
            if version_dict[item]["type"] == "AScanner":
                sorted_version_dict[item] = version_dict[item]
        sorted_version_list = sorted(version_dict, key=lambda i: (version_dict[i]['type'], version_dict[i]['name']))
        for version_item in sorted_version_list:
            if version_dict[version_item]["type"] != "AScanner":
                sorted_version_dict[version_item] = version_dict[version_item]

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
                sorted_available_version_dict[version_item]["url"] = "https://github.com/AScanner/%s" % version_item

        return render_template('versions.html', request=request, session=session, ascanner=self.ascanner, version_dict=sorted_version_dict, available_version_dict=sorted_available_version_dict, list=list)
