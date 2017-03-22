
from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urlib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app starts in global layout
app = Flask(__name__)

@app.route('/')
def home_page():
    return "Welcome to Home bot"
