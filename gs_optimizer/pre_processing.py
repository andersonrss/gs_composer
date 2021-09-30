
# -*- coding: utf-8 -*-
from lxml import etree
from copy import deepcopy
import set_cost_matrix, util
import os


nLicks = 0
cost = 0

# Lists that store the indexes of their respective lick type
qRepetition = []
qRest = []
qBlueNote = []
qTurnaround = []
qNormal = []
qDummy = []

# Knowing the types of lick
for f in os.listdir('gs_optimizer/lick_database'):
	
	lick = "gs_optimizer/lick_database/%s.xml" % nLicks
	inpt = open(lick, "r")
	tree = etree.parse(inpt)
	root = tree.getroot()
	measure = root.find('part').find('measure')
	lick_notes = deepcopy(list(measure.iter('note')))
	
	if util.isDummy(root) == 1:
		qDummy.append(nLicks)
	elif util.isTurnaround(root) == 1:
		qTurnaround.append(nLicks)
	elif util.isRepetition(lick_notes) == 1:
		qRepetition.append(nLicks)
	elif util.isRest(lick_notes) == 1:
		qRest.append(nLicks)
	elif util.isBlueNote(lick_notes) == 1:
		qBlueNote.append(nLicks)
	else:
		qNormal.append(nLicks)

	nLicks += 1

# Cost matrix declaration
cMatrix = [[0 for i in range(nLicks)] for j in range(nLicks)]

# Filling the cost matrix
for i in range(nLicks):
	print ("Processing lick  %d  of  %d" % (i, nLicks-1))
	for j in range(nLicks):

		# Same lick, no cost
		if i == j:
			cMatrix[i][j] = 0
			continue

		# If any of both is the dummy lick
		if i == 0 or j == 0:
			cMatrix[i][j] = 0
			continue

		# Forcing turnaround lick to be at the end of progression 12-bar Blues
		if ( ( i in qRepetition ) or ( i in qRest ) or ( i in qNormal ) or ( i in qBlueNote ) ) and ( j in qTurnaround ):
			cMatrix[i][j] = 50000
			continue
		
		# Reading lick_a and lick_b files
		lick_a = "gs_optimizer/lick_database/%s.xml" % i
		inpt_a = open(lick_a, "r")

		lick_b = "gs_optimizer/lick_database/%s.xml" % j
		inpt_b = open(lick_b, "r")

		tree_a = etree.parse(inpt_a)
		root_a = tree_a.getroot()
		measure_a = root_a.find('part').find('measure')

		tree_b = etree.parse(inpt_b)
		root_b = tree_b.getroot()
		measure_b = root_b.find('part').find('measure')

		notes_lick_a = deepcopy(list(measure_a.iter('note')))
		notes_lick_b = deepcopy(list(measure_b.iter('note')))

		last_lick_a = notes_lick_a[-1]
		first_lick_b = notes_lick_b[0]

		# Setting costs based on rules
		cost += set_cost_matrix.repetition(notes_lick_a, notes_lick_b)
		cost += set_cost_matrix.rests(last_lick_a, first_lick_b)
	
		inpt = open("gs_optimizer/xmls/minor_scale.xml", "r")
		tree = etree.parse(inpt)
		root = tree.getroot()

		cost += set_cost_matrix.seq_notes_scale(last_lick_a, first_lick_b, root)
		cost += set_cost_matrix.equal_notes(last_lick_a, first_lick_b)
	
		cMatrix[i][j] += cost
		cost = 0

print("\033[92m\nProcessing completed\033[0m\n")

# Writing lick indexes, cost matrix and number of licks in files
with open("gs_optimizer/solver/files/matrix", "w") as matrixFile:
	for i in range(nLicks):
		for j in range(nLicks):
			cMatrix[i][j] = str(cMatrix[i][j])
			matrixFile.write(cMatrix[i][j] + ' ')
		matrixFile.write('\n')

#	- nLicks
with open("gs_optimizer/solver/files/nLicks", "w") as nSublicksFile:
	nSublicksFile.write(str(nLicks))

#	- Repetition licks indexes
with open("gs_optimizer/solver/indexes/REPETITION", "w") as qRepetitionFile:
	for i in range(len(qRepetition)):
		qRepetition[i] = str(qRepetition[i])
		qRepetitionFile.write(qRepetition[i] + ' ')

#	- Licks with rest indexes
with open("gs_optimizer/solver/indexes/REST", "w") as qRestFile:
	for i in range(len(qRest)):
		qRest[i] = str(qRest[i])
		qRestFile.write(qRest[i] + ' ')

#	- Licks with blue note indexes
with open("gs_optimizer/solver/indexes/BLUE_NOTE", "w") as qBlueNoteFile:
	for i in range(len(qBlueNote)):
		qBlueNote[i] = str(qBlueNote[i])
		qBlueNoteFile.write(qBlueNote[i] + ' ')

#	- Turnaround licks indexes
with open("gs_optimizer/solver/indexes/TURNAROUND", "w") as qTurnaFile:
	for i in range(len(qTurnaround)):
		qTurnaround[i] = str(qTurnaround[i])
		qTurnaFile.write(qTurnaround[i] + ' ')

#	- Normal licks indexes
with  open("gs_optimizer/solver/indexes/NORMAL", "w") as qNormalFile:
	for i in range(len(qNormal)):
		qNormal[i] = str(qNormal[i])
		qNormalFile.write(qNormal[i] + ' ')

#	- Dummy licks indexes
with open("gs_optimizer/solver/indexes/DUMMY", "w") as qDummyFile:
	for i in range(len(qDummy)):
		qDummy[i] = str(qDummy[i])
		qDummyFile.write(qDummy[i] + ' ')



