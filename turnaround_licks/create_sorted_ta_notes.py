
# -*- coding: utf-8 -*-
from lxml import etree
from copy import *
import os, sys
import util


# File Description:
#	- This script creates a MusicXML file containing input notes to be used in turnaround licks generation
#	- The final MusicXML file is based on the licks database passed as input

# Path to the licks database
db_path = "licks/"

# Path to the general XML folder
xml_path = "../xmls/"

nLicks = 0
domain = []

for i in os.listdir(db_path):
	nLicks += 1

for i in range(nLicks):
	ta_lick = util.create_root(db_path + "ta_%s.xml" % i)

	for measure in list(ta_lick.find('part').iter('measure')):
		if measure.get('number') == '2':
			for note in list(measure.iter('note')):
				if note.find('rest') is not None:
					continue
				elif util.is_present(note, domain) == 0:
					aux_note = deepcopy(util.create_base_note())
					aux_note.find('pitch').find('step').text = note.find('pitch').find('step').text
					if note.find('pitch').find('alter') is not None:
						etree.SubElement(aux_note.find('pitch'), 'alter')
						aux_note.find('pitch').find('alter').text = '1'
					aux_note.find('pitch').find('octave').text = note.find('pitch').find('octave').text
					aux_note.find('type').text = "64th"
					aux_note.find('notations').find('technical').find('string').text = note.find('notations').find('technical').find('string').text
					aux_note.find('notations').find('technical').find('fret').text = note.find('notations').find('technical').find('fret').text
					
					domain.append(deepcopy(aux_note))

sortd = util.sort_notes(domain)
base = util.create_root(xml_path + "base.xml")

for n in sortd:
	base.find('part').find('measure').append(deepcopy(n))

base = etree.tostring(base)
with open(xml_path + "turnaround_notes.xml", "wb") as output:
	output.write(base)



