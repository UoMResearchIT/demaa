#!/usr/bin/env python
from __future__ import print_function
import sys
from flask import Flask, render_template
app = Flask(__name__)

'''
    Load the main view
'''
@app.route("/")
def start():
    return render_template('index.html')

'''
    API calls for data analysis functions. These are available to plugins.
'''
@app.route("/api")
def api():
    return "API calls"
