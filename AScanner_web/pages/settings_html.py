from flask import request, render_template, session


class Settings_HTML():
    endpoints = ["/settings", "/settings.html"]
    endpoint_name = "page_settings_html"
    endpoint_access_level = 1
    endpoint_category = "tool_pages"
    pretty_name = "Settings"

    def __init__(self, ascanner):
        self.ascanner = ascanner

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        web_settings_dict = {}
        for config_section in list(self.ascanner.config.conf_default.keys()):
            web_settings_dict[config_section] = {}

            for config_item in list(self.ascanner.config.conf_default[config_section].keys()):
                if self.ascanner.config.conf_default[config_section][config_item]["config_web"]:
                    configurable = True
                    if self.ascanner.config.conf_default[config_section][config_item]["config_web"] == "visible_only":
                        configurable = False
                    web_settings_dict[config_section][config_item] = {
                        "value": self.ascanner.config.dict[config_section][config_item],
                        "value_default": self.ascanner.config.conf_default[config_section][config_item]["value"],
                        "hide": self.ascanner.config.conf_default[config_section][config_item]["config_web_hidden"],
                        "valid_options": self.ascanner.config.conf_default[config_section][config_item]["valid_options"],
                        "description": self.ascanner.config.conf_default[config_section][config_item]["description"],
                        "configurable": configurable
                        }
            if not len(web_settings_dict[config_section].keys()):
                del web_settings_dict[config_section]

        conf_sections = list(web_settings_dict.keys())
        config_section = request.args.get('section', default=conf_sections[0], type=str)
        if config_section not in conf_sections:
            config_section = conf_sections[0]

        return render_template('settings.html', request=request, session=session, ascanner=self.ascanner, web_settings_dict=web_settings_dict, config_section=config_section, conf_sections=conf_sections, list=list)
