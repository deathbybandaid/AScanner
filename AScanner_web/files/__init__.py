

from .favicon_ico import Favicon_ICO
from .style_css import Style_CSS


class AScanner_Files():

    def __init__(self, ascanner):
        self.ascanner = ascanner

        self.favicon = Favicon_ICO(ascanner)
        self.style = Style_CSS(ascanner)
