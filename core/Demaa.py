#!/usr/bin/env python

# Import libraries
import sys
import os
import csv
import builtins

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
	
	def __init__(self, type, inputFile, analysis):
		if type == 'new':
			self.inputFile = inputFile
			self.analysis = analysis

			print(self.startPrintLine)
			print('Starting DEMAA analysis')
			print(self.endPrintLine)
		
			# Check the input file is valid
			self.validateInputFile(self.inputFile)
		
			# Check the analysis module is valid
			self.validateAnalysisOption(self.analysis)
		
			# Run the analysis
			self.analyseData(self.inputFile, self.analysis, self.lineCount)

			print('\n'+self.endPrintLine)
			
		elif type == 'results':
			print(self.startPrintLine)
			print('List saved analysis results...')
			print(self.endPrintLine)
		
		elif type == 'get':
			print(self.startPrintLine)
			print('Retreive saved analysis results...')
			print(self.endPrintLine)
			
		else:
			print(self.startPrintLine)
			print('Please specify new, results, or get for the first argument.')
			print(self.endPrintLine)

	def validateInputFile(self, inputFile):
		print('Checking input: {}...'.format(inputFile))
		
		# Validation
		if os.path.isfile(inputFile):
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

	def analyseData(self, inputFile, analysis, lineCount):
		print('Reading data from file...')
		
		# Open the tsv file
		parsedFile = {}
		with open(inputFile) as tsv:
			for line in csv.reader(tsv, dialect = 'excel-tab'):
				if line:
					#print(line[0])
					parsedFile[lineCount] = line
					lineCount += 1

		head, tail = os.path.split(inputFile)
		print('  > Read {} lines from {}, performing analysis... \n'.format(lineCount, tail))
		
		# Run the analysis
		print('Running analysis module: {}...'.format(analysis))
		
		# Get the list of imported modules
		modules = self.availableModules()
	
		# Get the module object
		module = getattr(modules[analysis]['import'], modules[analysis]['name'])
	
		# Get the class object from the module
		class_ = getattr(module, modules[analysis]['name'])
	
		# Run the class, with indentation
		module.print = Demaa.print
		class_(parsedFile)

	def availableModules(self):
		# Get a list of available modules
		modules = {}
		
		for item in dir(core):
			if '__' not in item and 'Demaa' not in item:
				modules[item] = {}
				modules[item]['name'] = item
				modules[item]['import'] = core
	
		for item in dir(plugins):
			if '__' not in item and not item.islower():
				modules[item] = {}
				modules[item]['name'] = item
				modules[item]['import'] = plugins
			
		return modules

	# Patch the print function to indent module class output
	@staticmethod
	def print(*args, **kwargs):
		builtins.print("  > ", *args, **kwargs)



