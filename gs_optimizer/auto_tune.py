
# -*- coding: utf-8 -*-
from lxml import etree
from copy import deepcopy
import util


# Make some changes in the solo based on the chord being played at moment, using available notes for that purpose. Those available notes are inputs, which in this especific case, are the notes that compose the chords C7, F7 and G7
def auto_tune(measure):

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

	# Measures corresponding to C7 chord in 12-Bar Blues model
	if measure.get('number') == '2' or measure.get('number') == '3' or measure.get('number') == '4' or measure.get('number') == '5' or measure.get('number') == '8' or measure.get('number') == '9':
		for i in range(len(measure)):
			# Trying to replace the first note of the measure if it is 'F' or 'D#' and has duration > 5.333 (obs: a eighth note triplet has a numeric duration of 5.333)
			if i == 0:
				util.replace(measure, available_notes_C, 'F', None, 5.333, i, 0)
				util.replace(measure, available_notes_C, 'D', '1', 5.333, i, 0)
		
			# If any note along the measure is 'F' and has duration > 8 (eighth note)
			util.replace(measure, available_notes_C, 'F', None, 8, i, 0)

			# If any note along the measure is 'D#' and has duration > 8 (eighth note)
			util.replace(measure, available_notes_C, 'D', '1', 8, i, 0)

	# Measures corresponding to F7 chord in 12-Bar Blues model
	if measure.get('number') == '6' or measure.get('number') == '7' or measure.get('number') == '11':
		for i in range(len(measure)):
			# If any note along the measure is 'A#' and has duration > 8 (eighth note)
			util.replace(measure, available_notes_F, 'A', '1', 8, i, 1)
	
	# Measure corresponding to G7 chord in 12-Bar Blues model
	if measure.get('number') == '10':
		for i in range(len(measure)):
			# Trying to replace the first note of the measure if it is 'C' and has duration > 5.333 (eighth note triplet)
			if i == 0:
				util.replace(measure, available_notes_G, 'C', None, 5.333, i, 0)
				util.replace(measure, available_notes_G, 'A', '1', 5.333, i, 1)
		
			# If any note along the measure is 'D#' and has duration > 8 (eighth note)
			util.replace(measure, available_notes_G, 'D', '1', 8, i, 0)

			# If any note along the measure is 'A#' and has duration > 8 (eighth note)
			util.replace(measure, available_notes_G, 'A', '1', 8, i, 1)



