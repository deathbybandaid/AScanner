from flask import send_from_directory

import pathlib


class Brython_stdlib():
    endpoints = ["/brython_stdlib.js"]
    endpoint_name = "file_brython_stdlib_js"

    def __init__(self, ascanner):
        self.ascanner = ascanner

        self.brython_path = pathlib.Path(self.ascanner.config.internal["paths"]["AScanner_web_dir"]).joinpath('brython')

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        return send_from_directory(self.brython_path,
                                   'brython_stdlib.js',
                                   mimetype='text/javascript')
