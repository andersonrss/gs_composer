
# -*- coding: utf-8 -*-
from lxml import etree
from copy import deepcopy
import util


# Based on the chord being played at moment, inserts double stops replacing previous placed noteheads
def insert_dStop(measure):
	
	list_notes_C = []
	list_notes_F = []
	list_notes_G = []
	
	root_C = util.create_root("gs_optimizer/xmls/dStop_C.xml")
	for note in list(root_C.find('part').find('measure').iter('note')):
		list_notes_C.append(deepcopy(note))
		
	root_F = util.create_root("gs_optimizer/xmls/dStop_F.xml")
	for note in list(root_F.find('part').find('measure').iter('note')):
			list_notes_F.append(deepcopy(note))
		
	root_G = util.create_root("gs_optimizer/xmls/dStop_G.xml")
	for note in list(root_G.find('part').find('measure').iter('note')):
			list_notes_G.append(deepcopy(note))
	
	if measure.get('number') == '2' or measure.get('number') == '3' or measure.get('number') == '4' or measure.get('number') == '5' or measure.get('number') == '8' or measure.get('number') == '9':
		util.replace_notehead_dStop(measure, list_notes_C)
	
	if measure.get('number') == '6' or measure.get('number') == '7' or measure.get('number') == '11':
		util.replace_notehead_dStop(measure, list_notes_F)
	
	if measure.get('number') == '10':
		util.replace_notehead_dStop(measure, list_notes_G)



