#!/usr/bin/env python

import sys
from core.Demaa import Demaa

# Abort if not Python 3
if sys.version_info < (3,0):
	print(startPrintLine)
	print('Your Python version is {}. Please run with Python 3.'.format(".".join(map(str, sys.version_info[:3]))))
	print(endPrintLine)
    
	quit()	

# Run the program
if len(sys.argv) == 1:
	# Import core analysis classes
	import core
	import plugins

	from core.Heatmap import Heatmap

	# Import any plugins that exist
	from plugins import *

	# No arguments passed, show the prompt
	print('\n--------------------------------------------------------------')
	print('Format for usage: $ python3 demaa input_path analysis_module_name')
	print('e.g. $ python3 demaa ./demaa/input/test.tsv Heatmap')
	
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
	Demaa(sys.argv[1], sys.argv[2])


