
# -*- coding: utf-8 -*-
from lxml import etree
from copy import deepcopy
import os
import random
import sys

random.seed()

op = sys.argv[1]
op = int(op)

indice = 0
nFiles = 0

if len(os.listdir('repetition_licks/result') ) == 0:
	print("Empty directory, Aborting...")
	exit()
else:
	for f in os.listdir('repetition_licks/result'):
		nFiles += 1

	randID_1 = random.randint(0, nFiles-1)
	randID_2 = random.randint(0, nFiles-1)
	
	while randID_1 == randID_2:
		randID_2 = random.randint(0, nFiles-1)

	fileName_1 = "repetition_licks/result/%s.xml" % randID_1
	fileName_2 = "repetition_licks/result/%s.xml" % randID_2
	
	repSublick_1 = open(fileName_1, "r")
	repSublick_2 = open(fileName_2, "r")
	
	tree_1 = etree.parse(repSublick_1)
	root_1 = tree_1.getroot()
	
	tree_2 = etree.parse(repSublick_2)
	root_2 = tree_2.getroot()

	base = open("xmls/base.xml", "r")
	treeB = etree.parse(base)
	rootB = treeB.getroot()

	# Caso 1: A = B = C = D
	if op == 1:
		for i in range(4):	
			for note in list(root_1.find('part').find('measure').iter('note')):
				rootB.find('part').find('measure').append(deepcopy(note))
	
	# Caso 2: A = B = C != D	
	elif op == 2:
		for i in range(3):	
			for note in list(root_1.find('part').find('measure').iter('note')):
				rootB.find('part').find('measure').append(deepcopy(note))
	
		for note in list(root_2.find('part').find('measure').iter('note')):
			rootB.find('part').find('measure').append(deepcopy(note))
	
	# Caso 3: A != B = C = D	
	elif op == 3:
		for note in list(root_1.find('part').find('measure').iter('note')):
			rootB.find('part').find('measure').append(deepcopy(note))
	
		for i in range(3):
			for note in list(root_2.find('part').find('measure').iter('note')):
				rootB.find('part').find('measure').append(deepcopy(note))
	
	# Caso 4: A = C , B = D	
	elif op == 4:
		for i in range(2):
			for note in list(root_1.find('part').find('measure').iter('note')):
				rootB.find('part').find('measure').append(deepcopy(note))
			
			for note in list(root_2.find('part').find('measure').iter('note')):
				rootB.find('part').find('measure').append(deepcopy(note))
		
	for f in os.listdir('gs_optimizer/lick_database'):
		indice += 1
	
	resultName = "gs_optimizer/lick_database/%s.xml" % indice
	out = open(resultName, "wb")
	rootB = etree.tostring(rootB)
	out.write(rootB)
	out.close()
	repSublick_1.close()
	repSublick_2.close()
	base.close()
		
