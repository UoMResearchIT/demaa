#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route('/')
def app():
	return 'index.html for AngularJS app'

@app.route('/api')
def api():
	return 'Data based on parameters'

if __name__ == '__main__':
    app.run()
