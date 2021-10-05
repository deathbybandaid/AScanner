#!/usr/bin/env python3
# coding=utf-8
# pylama:ignore=E402
"""monkey.patch_all must be run as soon as possible"""
try:
    from gevent import monkey
    monkey.patch_all()
    gevent_check = True
except ModuleNotFoundError:
    gevent_check = False

import os
import sys
import pathlib
SCRIPT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

"""Install Dependencies at startup."""
from deps import Dependencies
deps = Dependencies(SCRIPT_DIR)
if not gevent_check:
    print("gevent was missing, restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)
    sys.exit()

from AScanner.cli import run
import AScanner_web

if __name__ == "__main__":
    """Calls AScanner.cli running methods."""
    sys.exit(run.main(SCRIPT_DIR, AScanner_web, deps))
