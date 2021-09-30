
# -*- coding: utf-8 -*-
from __future__ import division
from copy import deepcopy
from lxml import etree
import util


# Based on notes given as input, attempts to move notes that are far from the midpoint of the measure to another position on the fretboard that is closer to it. By default, these input notes are the combination of all available notes for the C7, F7 and G7 chords, which is mentioned in "auto_tune.py"
def shift_note(measure):

	available_notes = []
	root = util.create_root("gs_optimizer/xmls/all_available_notes.xml")
	
	for note in list(root.find('part').find('measure').iter('note')):
		available_notes.append(deepcopy(note))

	midpoint = util.calc_midpoint(measure)
	
	for i in range(len(measure)):
		if measure[i].find('rest') is None:
			if i == (len(measure)-1):
				if ( ( measure[i].find('notations').find('slide') is not None ) and ( measure[i].find('notations').find('slur') is not None ) ) or ( measure[i].find('notehead') is not None ) or ( measure[i].find('chord') is not None ):
					continue
			elif ( ( measure[i].find('notations').find('slide') is not None ) and ( measure[i].find('notations').find('slur') is not None ) ) or ( measure[i].find('notehead') is not None ) or ( measure[i+1].find('chord') is not None ) or ( measure[i].find('chord') is not None ):
				continue
			
			if util.note2point_dist(measure[i], midpoint) > 2:
				for note in available_notes:
					if ( measure[i].find('pitch').find('step').text == note.find('pitch').find('step').text ) and ( measure[i].find('pitch').find('octave').text == note.find('pitch').find('octave').text ) and ( ( measure[i].find('pitch').find('alter') is None and note.find('pitch').find('alter') is None ) or ( measure[i].find('pitch').find('alter') is not None and note.find('pitch').find('alter') is not None ) ) and ( util.note2point_dist(note, midpoint) < 3 ):
						if ( measure[i].find('notations').find('technical').find('fret').text == note.find('notations').find('technical').find('fret').text ) and ( measure[i].find('notations').find('technical').find('string').text == note.find('notations').find('technical').find('string').text ):
							continue
						auxNote = deepcopy(note)
						util.replace_note(measure, available_notes, auxNote, i, 1)
						break



