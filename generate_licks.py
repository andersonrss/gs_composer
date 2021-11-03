
# -*- coding: utf-8 -*-
from GenerateClass import *

from lxml import etree
import random, sys, os, subprocess, time


random.seed()

# Setting the number of licks to be generated provided by the user
nDefault = int(sys.argv[1])
nRepetition = int(sys.argv[2])
nTurnaround = int(sys.argv[3])

# Creating log files
open("logs/default_log", "w").close()
open("logs/repetition_log", "w").close()
open("logs/turnaround_log", "w").close()


# DUMMY LICKS


base = open("gs_optimizer/xmls/base.xml", "r")

tree = etree.parse(base)
root = tree.getroot()
root = etree.tostring(root)

dummy = open("gs_optimizer/lick_database/0.xml", "wb")
dummy.write(root)
dummy.close()


# DEFAULT LICKS


index = 0

while index < nDefault:

	default = Generate("default")

	# Setting sublicks occurrences likelihood
	n_bend = default.get_set_nBends(0, 1, 0.5)
	n_bnote = default.get_nBlueNotes(0.10, 0.5)
	n_slide = default.get_set_nSlides(0, 1, 0.5)	
	n_tri = default.get_set_nTriplets(1, 4, 0.5) 
	n_tri_bend = default.get_set_nTriplets_bend(0, 1, 0.5)
	n_tri_bnote = default.get_nTriplets_blueNote(0.20, 0.5)
	n_tri_rest = default.get_nTriplets_rest(0.20)
	n_rest = default.get_nRests(0.20)
	n_dStop = default.get_nDStops(0.20)

	# Here we have an example of rule that can be implemented based on a specific situation
	#	- The number of default notes is based on the number of triplets and slide techniques defined before
	if (n_tri + n_tri_bend + n_tri_bnote + n_tri_rest) == 6:
		n_note = default.get_set_nNotes(9, 11, 0.5)
	else:
		n_note = default.get_set_nNotes(7, 8, 0.5) + n_slide

	# Generating a single default lick
	#	- Calls the solver to generate an optimal route of sublicks
	default.solver(n_bend, 
	n_bnote, 
	n_slide, 
	n_tri, 
	n_tri_bend, 
	n_tri_bnote, 
	n_tri_rest, 
	n_rest, 
	n_dStop, 
	n_note)
	
	#	- Concatenate sublicks
	ret = default.concat("default_licks/route", "gs_optimizer/lick_database/", "default_licks/sublicks/")

	#	- Write parameters in a log file
	with open("logs/default_log", "a") as default_log:
		default.create_log(default_log, 
		n_bend, 
		n_bnote, 
		n_slide, 
		n_tri, 
		n_tri_bend, 
		n_tri_bnote, 
		n_tri_rest, 
		n_rest, 
		n_dStop, 
		n_note, 
		ret)

	index += 1


# REPETITION LICKS


index = 0
nSubRepetition = 2*nRepetition
while index < nSubRepetition:

	repetition = Generate("repetition")

	# Setting sublicks occurrences likelihood
	#n_bend = repetition.get_set_nBends(0, 1, 0.7)
	n_bend = 1
	repetition.r_bend = 0.7

	n_bnote = 0
	n_slide = 0

	#n_tri = repetition.get_set_nTriplets(1, 4, 0.5)
	n_tri = 0
	repetition.r_tri = 0.0

	#n_tri_bend = repetition.get_set_nTriplets_bend(0, 1, 0.5)
	n_tri_bend = 0
	repetition.r_tri_bend = 0.0
	
	n_tri_bnote = 0
	n_tri_rest = 0
	n_rest = 0
	n_dStop = 0
	n_note = repetition.get_set_nNotes(3, 4, 0.7)

	# Generating a single repetition lick
	#	- Calls the solver to generate an optimal route of sublicks
	repetition.solver(n_bend, 
	n_bnote, 
	n_slide, 
	n_tri, 
	n_tri_bend, 
	n_tri_bnote, 
	n_tri_rest, 
	n_rest, 
	n_dStop, 
	n_note)

	#	- Concatenate sublicks
	ret = repetition.concat("repetition_licks/route", "repetition_licks/result/", "repetition_licks/sublicks/")

	#	- Write parameters in a log file
	with open("logs/repetition_log", "a") as repetition_log:
		repetition.create_log(repetition_log, 
		n_bend, 
		n_bnote, 
		n_slide, 
		n_tri, 
		n_tri_bend, 
		n_tri_bnote, 
		n_tri_rest, 
		n_rest, 
		n_dStop, 
		n_note, 
		ret)

	index += 1

index = 0
rep = 0
for i in os.listdir("repetition_licks/result"):
	rep += 1
	
if rep > 2:
	while index < nRepetition:
	
		# Repetition cases, randomly chosen, based on A-B-C-D patterns
		#	- Case 1: A = B = C = D
		#	- Case 2: A = B = C
		#	- Case 3: B = C = D
		#	- Case 4: A = B; B = D
		case = random.randint(1, 4)

		repetition.repetition_cases(case)
		index += 1


# TURNAROUND LICKS


index = 0

while index < nTurnaround:

	turnaround = Generate("turnaround")

	# Setting sublicks occurrences likelihood
	n_bend = turnaround.get_set_nBends(0, 1, 0.5)
	n_bnote = 0
	n_slide = 0
	n_tri = turnaround.get_set_nTriplets(3, 4, 0.5)
	n_tri_bend = turnaround.get_set_nTriplets_bend(0, 0, 0.5)
	n_tri_bnote = 0
	n_tri_rest = turnaround.get_nTriplets_rest(0.30)
	n_rest = 0
	n_dStop = 0
	n_note = turnaround.get_set_nNotes(4, 6, 0.5)

	# Generating the second measure of a turnaround lick
	#	- Calls the solver to generate an optimal route of sublicks
	turnaround.solver(n_bend, 
	n_bnote, 
	n_slide, 
	n_tri, 
	n_tri_bend, 
	n_tri_bnote, 
	n_tri_rest, 
	n_rest, 
	n_dStop, 
	n_note)

	#	- Concatenate sublicks
	ret = turnaround.concat("turnaround_licks/route", "turnaround_licks/result/2/", "turnaround_licks/sublicks/")

	#	- Write parameters in a log file
	with open("logs/turnaround_log", "a") as turnaround_log:
		turnaround.create_log(turnaround_log, 
		n_bend, 
		n_bnote, 
		n_slide, 
		n_tri, 
		n_tri_bend, 
		n_tri_bnote, 
		n_tri_rest, 
		n_rest, 
		n_dStop, 
		n_note, 
		ret)

	#	- Calls Markov chain subroutine	in order to generate the second measure
	subprocess.call(["python3", "turnaround_licks/markov_by_division.py", str(1), str(4), str(64)])

	index += 1

# Merging both measures to create a turnaround lick
index = 0
while index < nTurnaround:
	subprocess.call(["python3", "turnaround_licks/merge_turnaround.py"])
	index += 1

subprocess.call(["python3", "gs_optimizer/pre_processing.py"])



