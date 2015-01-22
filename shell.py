#!/usr/bin/env python
import os
import readline
from pprint import pprint

from flask import *
from parserbot import create_app

app = create_app()

os.environ['PYTHONINSPECT'] = 'True'