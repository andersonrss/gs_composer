
# -*- coding: utf-8 -*-
from lxml import etree
from datetime import datetime
from copy import deepcopy
import aditional_techniques, auto_tune, shifter, double_stops, first_note_processing, util
import random, os, sys, copy


# Path to route file
route_path = "gs_optimizer/solver/route"

# Path to results directory
result_dir= "gs_optimizer/result/"

# Path to lick data base
lick_db_dir = "gs_optimizer/lick_database/"

# Path to directory of xml's used
xml_dir = "gs_optimizer/xmls/"

random.seed()

# Checking if the file is empty
#	- If the file is empty, an error may have occurred
if os.stat(route_path).st_size != 0:
	
	# Storing the route in a list
	auxRoute = []
	route = []
	with open(route_path, "r") as f:
		linha = f.readline()

		while linha:
			auxRoute.append(linha.split())
			linha = f.readline()

	# Creating the route
	for r in range(len(auxRoute)):
		for i in range(len(auxRoute[r])):
			auxRoute[r][i] = int(auxRoute[r][i])

	route.append(copy.copy(auxRoute[0][0]))
	route.append(copy.copy(auxRoute[0][1]))

	for i in range(len(auxRoute)):
		for j in range(len(auxRoute)):
			if route[i+1] == auxRoute[j][0]:
				route.append(copy.copy(auxRoute[j][1]))
	
	del route[-1]
	del route[-1]

	while route[0] != 0:
		removed = route.pop(0)
		route.insert(len(route), removed)

	del route[0]


	# CONCATENATION


	# Retrieving the 12-bar Blues progression used as base
	nLicks = 10	
	licks = [[] for i in range (nLicks)]

	for i in range(len(route)-1):
		fileName = lick_db_dir + "%s.xml" % route[i]
		
		with open(fileName, "r") as lick:
			treeL = etree.parse(lick)
		
		rootL = treeL.getroot()
		
		for note in list(rootL.find('part').find('measure').iter('note')):
			licks[i].append(deepcopy(note))
	
	with open(xml_dir + "moderate_blues.xml", "r") as base:
		treeB = etree.parse(base)

	rootB = treeB.getroot()

	# Concatenating measures and making adjustments, such as replacing notes and applying techniques
	index = 0
	last_note_prev_mes = None
	tied_notes_toInsert = [0 for i in range(nLicks)]
	for part in list(rootB.iter('part')):
		if part.get('id') == "P4":
			for measure in list(part.iter('measure')):
				if measure.get('number') == '1':
					continue
				if index == nLicks:
					break
				for i in range(len(licks[index])):
					measure.append(deepcopy(licks[index][i]))
				if index > 0:
					last_note_prev_mes = deepcopy(licks[index-1][-1])
				auto_tune.auto_tune(measure)
				shifter.shift_note(measure)
				double_stops.insert_dStop(measure)
				previous_tied = first_note_processing.first_note(measure, last_note_prev_mes)
				#aditional_techniques.blue_note(measure, 0.10)
				#aditional_techniques.bend_blue_note(measure, 0.20)
				if previous_tied == 1:
					tied_notes_toInsert[index-1] = 1
					previous_tied = 0
				#shifter.shift_note(measure)
				aditional_techniques.hammer_pull(measure, 0.30)
				index += 1

	# Inserting tied notes at specific points in the solo
	index = 0
	for part in list(rootB.iter('part')):
		if part.get('id') == "P4":
			for measure in list(part.iter('measure')):
				if measure.get('number') == '1':
					continue
				if index == nLicks:
					break
				if tied_notes_toInsert[index] == 1:
					etree.SubElement(measure[-1], "tie", type="start")
					etree.SubElement(measure[-1].find('notations'), "tied", type="start")
				aditional_techniques.vibrato(measure)
				index += 1

	# Adding turnaround
	fileName = lick_db_dir + "%s.xml" % route[-1]
	
	with open(fileName, "r") as lick:
		treeL = etree.parse(lick)
	
	rootL = treeL.getroot()

	turnaround = [[] for i in range(2)]
	
	mes = 0
	for m in list(rootL.find('part').iter('measure')):
		for n in list(m.iter('note')):
			turnaround[mes].append(deepcopy(n))
		mes += 1

	mes = 0	
	for part in list(rootB.iter('part')):
		if part.get('id') == "P4":
			for measure in list(part.iter('measure')):
				if measure.get('number') == '12':
					for n in turnaround[0]:
						measure.append(deepcopy(n))
				elif measure.get('number') == '13':
					for n in turnaround[1]:
						measure.append(deepcopy(n))

	# Writing solo in a MusicXML file
	code = datetime.now()
	code = code.strftime("%d-%m-%Y-%H-%M-%S")

	resName = result_dir + code + ".xml"
	rootB = etree.tostring(rootB)
	
	with open(resName, "wb") as out:
		out.write(rootB)	
else:
	print("There was an error in the concatenation. Aborting...\n")
	sys.exit(1)



	
