# DEMAA

## Introduction

An application for analysing eye tracking data files, and producing data visualisations. Created at the University of Manchester, UK.

This application can be used via the commandline or using the web UI. 


## Prerequisites 

Python 3



## Usage

###Command line interface usage

Arguments for usage:

1. function_type = new, results, get
2. input_path = /path/file.tsv
3. analysis\_module_name = Heatmap

e.g.

	$ python demaa new ./demaa/input/test.tsv Heatmap
 
	$ python demaa results

	$ python demaa get 3
	
If you have multiple Python version installed you may have to substitute python with python3, depending on your installation.