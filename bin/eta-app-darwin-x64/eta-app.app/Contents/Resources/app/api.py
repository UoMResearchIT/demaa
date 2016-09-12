#!/usr/bin/env python
'''
    API calls for data analysis functions. These are available to plugins.
    The API takes parameters and returns JSON for the D3 UI.
'''

# Imports
import json
import sys

# Main class
class API():
    'Controller for interacting with the analysis modules, validating input, and outputing JSON data to the UI'

    def __init__(self, analysis, input):
        self.input = input

        if analysis == 'test':
            self.test()

    def test(self):
        print(json.dumps({"title": "test", "input": self.input}))

API(sys.argv[1], sys.argv[2])
