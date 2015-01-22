#!/usr/bin/env python
import os
import readline
from pprint import pprint

from flask import *
from parserbot.app import *

app.config.from_object('config')

os.environ['PYTHONINSPECT'] = 'True'