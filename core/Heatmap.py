#!/usr/bin/env python

class Heatmap():
	'Testing core class import'
	
	def __init__(self, input):
		self.input = input
		self.createHeatmap()

	def createHeatmap(self):
		print('Creating heatmap...')
		print(self.input[0])

