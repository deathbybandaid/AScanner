

from .brython import Brython
from .brython_stdlib import Brython_stdlib

from .brython_bry import Brython_bry


class AScanner_Brython():

    def __init__(self, ascanner):
        self.ascanner = ascanner

        self.brython = Brython(ascanner)
        self.brython_stdlib = Brython_stdlib(ascanner)

        self.brython_bry = Brython_bry(ascanner)
