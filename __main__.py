#!/usr/bin/env python

'''
	The command line interface for interacting with the user
	This file uses core/Demaa.py to load the analysis modules,
	parse the tsv files and output the results.
'''

import sys

# Abort if not Python 3
if sys.version_info < (3,0):
	print('\n--------------------------------------------------------------\n')
	print('Your Python version is {}. Please run with Python 3.'.format(".".join(map(str, sys.version_info[:3]))))
	print('\n--------------------------------------------------------------\n')
    
	quit()	

from Demaa import Demaa

# Run the program
if len(sys.argv) == 1:
	# Import core analysis classes
	import core
	import plugins

	from core.Heatmap import Heatmap

	# Import any plugins that exist
	from plugins import *

	# No arguments passed, show the prompt
	print('\n--------------------------------------------------------------\n')
	print('DEMAA')
	print('\n--------------------------------------------------------------\n')
	print('Arguments for usage:\n1. function_type = new, results, get\n2. input_path = /path/file.tsv\n3. analysis_module_name = Heatmap')
	
	print('\ne.g.\n\n$ python demaa new ./demaa/input/test.tsv Heatmap')
	print('or $ python demaa results')
	print('or $ python demaa get 3')
	
	print('\nAvailable core analysis modules:')
	
	for item in dir(core):
		if '__' not in item and 'Demaa' not in item:
			print(' - {}'.format(item))
	
	print('\nAvailable plugin analysis modules:')
	
	for item in dir(plugins):
		if '__' not in item and not item.islower():
			print(' - {}'.format(item))
	
	print('\n--------------------------------------------------------------\n')

else:
	# Instantiate the class with the arguments provided
	if len(sys.argv) == 3:
		type = sys.argv[1]
		input = sys.argv[2]
		analysis = 0
		
	elif len(sys.argv) == 2:
		type = sys.argv[1]
		input = 0
		analysis = 0
	else: 
		type = sys.argv[1]
		input = sys.argv[2]
		analysis = sys.argv[3]
		
	Demaa(type, input, analysis)


