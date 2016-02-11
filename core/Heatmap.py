#!/usr/bin/env python

class Heatmap():
	'Testing core class import'
	
	def __init__(self, parsedFile):
		self.parsedFile = parsedFile
		
		x = input("Please enter value for x: ")
		print("x set to {}".format(x))

		y = input("Please enter value for y: ")
		print("y set to {}".format(y))

		self.createHeatmap(x, y)

	def createHeatmap(self, x, y):
		print('Creating heatmap using x:{} and y:{}'.format(x, y))
		print('Output: {}'.format(self.parsedFile[0][0]))
	

