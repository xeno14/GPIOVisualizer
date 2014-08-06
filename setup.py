#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup

NAME = 'GPIOVisualizer'
LICENSE = 'GPL'
AUTHOR = 'Ryo Murakami'
AUTHOR_EMAIL = 'integral14.dev@gmail.com'
DESCRIPTION = 'Visualize GPIO state using RPi.GPIO'
URL = 'https://github.com/xeno1991/GPIOVisualizer'
VERSION = 0.1

if sys.platform == 'darwin':
    OPTIONS = {
        "argv_emulation": False,
        "includes": ["sip", "PyQt4._qt"],
    }
    setup(
        name=NAME,
        version=VERSION,
        license=LICENSE,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        url=URL,
        app=['Visualizer/main.py'],
        options={'py2app': OPTIONS},
        setup_requires=["py2app"],
        packages=["RPi"],
    )
