
# -*- coding: utf-8 -*-
from lxml import etree
from copy import deepcopy
import copy, os, sys


# Path to route file
route_path = sys.argv[1]

# Path to results directory
result_lick_dir = sys.argv[2]

# Path to sublicks data base
sublicks_dir = sys.argv[3]

# Sublick type
sublick_type = sys.argv[4]

# Checking if the file is empty
#	- If the file is empty, an error may have occurred
if os.stat(route_path).st_size != 0:
	
	index = 0
	auxRoute = []
	route = []

	with open(route_path, "r") as f:
		# Checking if a valid solution exists
		for line in f:
			index += 1
			if index > 20:
				print("\033[33m\nThere is no valid solution (" + sublick_type + ")\033[0m\n")
				sys.exit(1)

		# Storing route in a list
		f.seek(0)
		index = 0

		line = f.readline()

		while line:
			auxRoute.append(line.split())
			line = f.readline()

	# Creating route
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


# CONCATENATION


	# Concatenating sublicks
	for i in os.listdir(result_lick_dir):
		index += 1

	with open("xmls/base.xml", "r") as base:
		treeB = etree.parse(base)

	rootB = treeB.getroot()

	for i in route:
		fileName = sublicks_dir + "sublick_%s.xml" % i
		with open(fileName, "r") as inpt:
			tree = etree.parse(inpt)

		root = tree.getroot()

		for note in list(root.find('part').find('measure').iter('note')):
			rootB.find('part').find('measure').append(deepcopy(note))

	# Writing measure in a MusicXML file
	rootB = etree.tostring(rootB)

	resultName = result_lick_dir + "%s.xml" % index
	with open(resultName, "wb") as output:
		output.write(rootB)
	print("\033[92m\nConcatenation concluded\033[0m\n")
else:
	print("\033[33m\nThere is no valid solution (" + sublick_type + ")\033[0m\n")
	sys.exit(1)



