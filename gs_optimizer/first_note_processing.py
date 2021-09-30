
# -*- coding: utf-8 -*-
from lxml import etree
from copy import deepcopy
import random
import util


# This function applies some post processing procedures in order to reduce determinism in results
def first_note(measure, last_note_prev_mes):
	
	available_notes_C = []
	available_notes_F = []
	available_notes_G = []

	root_C = util.create_root("gs_optimizer/xmls/chord_available_notes_C.xml")
	for note in list(root_C.find('part').find('measure').iter('note')):
		available_notes_C.append(deepcopy(note))

	root_F = util.create_root("gs_optimizer/xmls/chord_available_notes_F.xml")
	for note in list(root_F.find('part').find('measure').iter('note')):
		available_notes_F.append(deepcopy(note))

	root_G = util.create_root("gs_optimizer/xmls/chord_available_notes_G.xml")
	for note in list(root_G.find('part').find('measure').iter('note')):
		available_notes_G.append(deepcopy(note))
	
	if measure.get('number') == '2' or measure.get('number') == '3' or measure.get('number') == '4' or measure.get('number') == '5' or measure.get('number') == '8' or measure.get('number') == '9':
		if util.get_duration(measure[0]) == 16:
			# 0 = split_note()
			# 1 = split-note_s()
			# 2 = tied_between_measures()
			option = random.randint(0, 2)
			if option == 0: 
				# 0 = 50/50
				# 1 = 75/25
				#ratio = random.randint(0, 1)
				ratio = 0
				util.split_note(measure, 0, ratio)
				return 0

			elif option == 1:
				#ratio = random.randint(0, 1)
				ratio = 0
				strategy = random.randint(0, 1)
				util.split_note_s(measure, 0, available_notes_C, ratio, strategy)
				return 0

			elif option == 2:
				if last_note_prev_mes is not None and last_note_prev_mes.find('notehead') is None and last_note_prev_mes.find('rest') is None:
					util.tied_between_measures(measure, 0, last_note_prev_mes)
					return 1
				else:
					return 0

	elif measure.get('number') == '6' or measure.get('number') == '7' or measure.get('number') == '11':
		if util.get_duration(measure[0]) == 16:
			option = random.randint(0, 2)
			if option == 0: 
				#ratio = random.randint(0, 1)
				ratio = 0
				util.split_note(measure, 0, ratio)
				return 0
				
			elif option == 1:
				#ratio = random.randint(0, 1)
				ratio = 0
				strategy = random.randint(0, 1)
				util.split_note_s(measure, 0, available_notes_F, ratio, strategy)
				return 0
	
			elif option == 2:
				if last_note_prev_mes.find('notehead') is None and last_note_prev_mes.find('rest') is None:
					util.tied_between_measures(measure, 0, last_note_prev_mes)
					return 1
				else:
					return 0

	elif measure.get('number') == '10':
		if util.get_duration(measure[0]) == 16:
			option = random.randint(0, 2)
			if option == 0: 
				#ratio = random.randint(0, 1)
				ratio = 0
				util.split_note(measure, 0, ratio) 
				return 0
				
			elif option == 1:
				#ratio = random.randint(0, 1)
				ratio = 0
				strategy = random.randint(0, 1)
				util.split_note_s(measure, 0, available_notes_G, ratio, strategy)
				return 0
			
			elif option == 2:
				if last_note_prev_mes.find('notehead') is None and last_note_prev_mes.find('rest') is None:
					util.tied_between_measures(measure, 0, last_note_prev_mes)
					return 1
				else:
					return 0



