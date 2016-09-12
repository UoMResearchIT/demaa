#!/usr/bin/env python
'''
    API calls for data analysis functions. These are available to plugins.
    The API takes parameters and returns JSON for the D3 UI.
'''

# Imports
import json
import csv
import sys
import importlib

from modules import *

# Main class
class API():
    'Controller for interacting with the analysis modules, validating input, and outputing JSON data to the UI'

    def __init__(self, analysis):
        self.analysis = analysis
        self.dataset = sys.stdin.readlines()
        self.doAnalysis()

    # Call the relevant analysis module
    def doAnalysis(self):
        # Dynamically call the analysis class from the string name
        dataset = self.dataset[0]
        reader = csv.reader(dataset.splitlines(), delimiter=',')

        module = importlib.import_module('.'+self.analysis, 'modules')
        analysisResult = module.process(dataset)

        print(analysisResult)

API(sys.argv[1])
