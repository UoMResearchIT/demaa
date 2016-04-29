#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route('/')
def app():	
	# Do we need the application to be serving static files?
	# Should this be offloaded to Apache or a static file server like S3?
	return 'index.html for AngularJS app'

@app.route('/api')
def api():
	return 'Data based on parameters'
	
if __name__ == '__main__':
    app.run()
