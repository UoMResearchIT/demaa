#!/usr/bin/env python
from __future__ import print_function
import sys
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def start():
    return render_template('index.html')

@app.route("/api")
def api():
    return "API calls"

if __name__ == "__main__":
    print('oh hello')
    sys.stdout.flush()
    app.run()
