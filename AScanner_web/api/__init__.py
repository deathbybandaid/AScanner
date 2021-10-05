
from .root_url import Root_URL
from .startup_tasks import Startup_Tasks

from .settings import Settings
from .logs import Logs
from .versions import Versions
from .debug import Debug_JSON
from .plugins import Plugins
from .watchdog import WATCHDOG

from .route_list import Route_List


class AScanner_API():

    def __init__(self, ascanner):
        self.ascanner = ascanner

        self.root_url = Root_URL(ascanner)
        self.startup_tasks = Startup_Tasks(ascanner)

        self.settings = Settings(ascanner)
        self.logs = Logs(ascanner)
        self.versions = Versions(ascanner)
        self.debug = Debug_JSON(ascanner)
        self.plugins = Plugins(ascanner)

        self.watchdog = WATCHDOG(ascanner)

        self.route_list = Route_List(ascanner)
