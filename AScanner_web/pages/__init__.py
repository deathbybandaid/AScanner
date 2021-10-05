

from .index_html import Index_HTML
from .versions_html import Versions_HTML
from .diagnostics_html import Diagnostics_HTML
from .settings_html import Settings_HTML
from .watchdog_html import Watchdog_HTML


class AScanner_Pages():

    def __init__(self, ascanner):
        self.ascanner = ascanner

        self.index_html = Index_HTML(ascanner)
        self.versions_html = Versions_HTML(ascanner)
        self.diagnostics_html = Diagnostics_HTML(ascanner)
        self.settings_html = Settings_HTML(ascanner)
        self.watchdog_html = Watchdog_HTML(ascanner)
