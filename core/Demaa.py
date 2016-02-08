#!/usr/bin/env python

# Import libraries
import sys
import os
import csv

# Import core analysis classes
import core
import plugins

from core.Heatmap import Heatmap

# Import any plugins that exist
from plugins import *

# Main class
class Demaa():
	'Commandline interface for eye tracking analysis'
	
	# Vars
	startPrintLine = '\n--------------------------------------------------------------'
	endPrintLine = '--------------------------------------------------------------\n'
	lineCount = 0
	
	def __init__(self, input, analysis):
		self.input = input
		self.analysis = analysis

		print(self.startPrintLine)
		print('Starting DEMAA analysis')
		print(self.endPrintLine)
		
		# Check the input file is valid
		self.validateInputFile(self.input)
		
		# Check the analysis module is valid
		self.validateAnalysisOption(self.analysis)
		
		# Run the analysis
		self.analyseData(self.input, self.analysis, self.lineCount)

		print(self.endPrintLine)

	def validateInputFile(self, input):
		print('Checking input: {}...'.format(input))
		
		# Validation
		if os.path.isfile(input):
			print('  > Success, input file found.\n')
		
		else:
			print('Error: File not found, exiting.\n')
			print(self.endPrintLine)
		
	def validateAnalysisOption(self, analysis):
		print('Checking analysis module: {}...'.format(analysis))
		
		#print(dir(core))
		
		# Validation. Check the analysis class exists in core
		if analysis in dir(core):
			print('  > Success, analysis module available.\n')
		
		# If it doesn't check the plugins
		elif analysis in dir(plugins):
			print('  > Success, analysis module available.\n')
		
		else:
			print('  > Error, analysis module '+analysis+' not available, exiting.\n')
			quit()
		
	def analyseData(self, input, analysis, lineCount):
		print('Analysing data...')
		
		# Open the tsv file
		with open(input) as tsv:
			for line in csv.reader(tsv, dialect = 'excel-tab'):
				if line:
					#print(line[0])
					lineCount += 1

		print('  > Read {} lines from {}, performing analysis... \n'.format(lineCount, input))


