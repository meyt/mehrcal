# -*- coding: utf-8 -*-
import logging
from core import app

logging.basicConfig(level=logging.DEBUG)
main = app.App()
main.run()
