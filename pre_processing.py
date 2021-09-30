
# -*- coding: utf-8 -*-
from CostCalculatorClass import *

from lxml import etree
from copy import deepcopy
import util, os, sys


# This function manage some features like cost matrix alocation and filling, and writing indexes
def pre_processing(sublickType_obj):

	nSublicks = len(sublickType_obj.generated_sublicks)
	sublicks = deepcopy(sublickType_obj.generated_sublicks)
	
	nNotes_sublicks = []
	timeSublicks = []
	
	for f in range(len(sublicks)):
		sublickTime = 0
		measure = sublicks[f].find('part').find('measure')
		nNotes_sublicks.append(len(list(measure.iter('note'))))
		
		for note in list(measure.iter('note')):
			sublickTime += util.get_duration(note)
			
		timeSublicks.append(sublickTime)

	# Cost matrix declaration
	mP = [[0 for i in range(len(sublicks))] for j in range(len(sublicks))]

	progress = 0.00
	step = 100/nSublicks

	# Filling the cost matrix
	for i in range(nSublicks):
		for j in range(nSublicks):
			
			cost = 0
			
			# Equal licks, high penality
			if i == j:
				mP[i][j] = 10000
				continue

			# Retrieving informaton from sublicks
			#	- Measures
			measure_a = sublicks[i].find('part').find('measure')
			measure_b = sublicks[j].find('part').find('measure')
			
			notes_sublick_a = deepcopy(list(measure_a.iter('note')))
			notes_sublick_b = deepcopy(list(measure_b.iter('note')))
			
			#	- las note from sublick_a and first note from sublick_b
			last_sublick_a = notes_sublick_a[-1]
			first_sublick_b = notes_sublick_b[0]

			#	- Defining costs
			sc = CostCalculator(sublickType_obj.type)
			sc.calc_cost(last_sublick_a, first_sublick_b)
			
			mP[i][j] = sc.cost

		if i == nSublicks-1:
			print("\rProcessing " + sublickType_obj.type + " sublicks ({0:}) -> \033[92m{1:5.2f}%\033[0m".format(nSublicks, 100), end='') 
		else:
			print("\rProcessing " + sublickType_obj.type + " sublicks ({0:}) -> {1:5.2f}%".format(nSublicks, progress), end='') 
			progress += step

	print ('\n')

	# Writing cost matrix, number of sublicks and total duration of each sublick in files
	with open(sublickType_obj.type + "_licks/files/nNotes_sublicks", "w") as nNotes_sublicksFile:
		for i in range(nSublicks):
			nNotes_sublicks[i] = str(nNotes_sublicks[i])
			nNotes_sublicksFile.write(nNotes_sublicks[i] + ' ')

	#	- Cost matrix
	with open(sublickType_obj.type + "_licks/files/matrix", "w") as matrixFile:
		for i in range(nSublicks):
			for j in range(nSublicks):
				mP[i][j] = str(mP[i][j])
				matrixFile.write(mP[i][j] + ' ')
			matrixFile.write('\n')

	#	- nLicks
	with open(sublickType_obj.type + "_licks/files/nSub", "w") as nSublicksFile:
		nSublicksFile.write(str(nSublicks))

	#	- Total duration
	with open(sublickType_obj.type + "_licks/files/tSub", "w") as timeSublicksFile:
		for i in range(nSublicks):
			timeSublicks[i] = str(timeSublicks[i])
			timeSublicksFile.write(timeSublicks[i] + ' ')



