
# -*- coding: utf-8 -*-
from __future__ import division
from copy import deepcopy
from lxml import etree
import math, random, sys


# get the duration of the input note as a scalar
def get_duration(note):

	duration = 0

	if note.find('type') is not None:
		if note.find('type').text == 'whole':
			duration = 64
		elif note.find('type').text == 'half':
			duration = 32
		elif note.find('type').text == 'quarter':
			duration = 16
		elif note.find('type').text == 'eighth':
			duration = 8
		elif note.find('type').text == '16th':
			duration = 4
		elif note.find('type').text == '32th':
			duration = 2
		elif note.find('type').text == '64th':
			duration = 1

	if note.find('time-modification') is not None:
		duration = (duration * 2)/3

	if note.find('dot') is not None:
		duration = duration + duration/2
	
	return duration


# Calculates the euclidean distance between two points
def euclidean_dist(xi, yi, xf, yf):

	return math.sqrt(((xf-xi)**2) + ((yf-yi)**2))


# Returns the distance between two notes on the fretboard
def note2note_dist(note_a, note_b):
	
	fret_note_a = note_a.find('notations').find('technical').find('fret').text
	string_note_a = note_a.find('notations').find('technical').find('string').text
	
	fret_note_b = note_b.find('notations').find('technical').find('fret').text
	string_note_b = note_b.find('notations').find('technical').find('string').text
	
	x_note_a = int(fret_note_a)
	y_note_a = 7 - int(string_note_a)
	
	x_note_b = int(fret_note_b)
	y_note_b = 7 - int(string_note_b)
	
	return euclidean_dist(x_note_a, y_note_a, x_note_b, y_note_b)


# Returns midpoint of a set of notes in a list
def calc_list_midpoint(measure):
	
	coordenates_arr = []
	
	for note in measure:
		if note.find('rest') is None:
			fret = note.find('notations').find('technical').find('fret').text
			string = note.find('notations').find('technical').find('string').text
			x = int(fret)
			y = 7 - int(string)
			coordenates_arr.append((x, y))

	xf = 0
	yf = 0
	for p in coordenates_arr:
		xf += p[0]
		yf += p[1]
	
	xf = xf/len(coordenates_arr)
	yf = yf/len(coordenates_arr)

	return int(round(xf)), int(round(yf))


# Checks if the lick is a repetition lick
def isRepetition(lick_notes):
	
	for note in lick_notes:
		if get_duration(note) > 16:
			return 0
			
	acc = 0
	index = 0
	submes = [[] for j in range(4)]

	i = 0	
	while i < len(lick_notes):
		if (acc + get_duration(lick_notes[i])) <= 16:
			submes[index].append(deepcopy(lick_notes[i]))
			acc += get_duration(lick_notes[i])
			i += 1
		elif acc == 16:
			index += 1
			acc = 0
		elif (acc + get_duration(lick_notes[i])) > 16:	
			return 0

	for i in range(len(submes)):
		for j in range(len(submes[i])):
			submes[i][j] = etree.tostring(submes[i][j]).decode('utf-8') #no python3 a função 'tostring' retorna um string em unicode, sendo preciso converter para utf-8
			
	quarter = ["" for i in range(4)]
	
	for j in range(len(submes)):
		for k in range(len(submes[j])):
			quarter[j] += submes[j][k]

	if ( quarter[0].strip() == quarter[1].strip() == quarter[2].strip() == quarter[3].strip() ) or ( quarter[0].strip() == quarter[1].strip() == quarter[2].strip() ) or ( quarter[1].strip() == quarter[2].strip() == quarter[3].strip() ) or ( quarter[0].strip() == quarter[2].strip() and quarter[1].strip() == quarter[3].strip() ):
		return 1
	else:
		return 0


# Cheks if the lick contains rest
def isRest(lick_notes):
	
	for note in lick_notes:
		if note.find('rest') is not None:
			return 1
	return 0


# Checks if the lick is a turnaround lick
def isTurnaround(root):
	
	if len(list(root.find('part').iter('measure'))) == 2:
		return 1
	else:
		return 0


# Checks if the lick is a dummy lick
def isDummy(root):
	
	if root.find('part').find('measure').find('note') is None:
		return 1
	else:
		return 0


# Checks if the lick contains blue note
def isBlueNote(lick_notes):
	
	for note in lick_notes:
		if note.find('pitch').find('step').text == 'F' and note.find('pitch').find('alter') is not None:
			return 1
	return 0


# Replaces a specified note from the measure by an available chord note. The 'flag' variable works as follows: for example, if a note is not well positioned along the measure (but it serves as a valid note in the other positions), if the same note is chosen for substitution, another draw will be performed.
def replace(measure, available_notes, step, alter, time, index, flag):

	nearby_available_notes = []
	aux_alter = None
	
	if measure[index].find('rest') is None:
		if measure[index].find('pitch').find('alter') is not None:
			aux_alter = '1' 
		
		if ( measure[index].find('pitch').find('step').text == step ) and ( aux_alter == alter ) and ( get_duration(measure[index]) > time ) and ( abs(time - get_duration(measure[index])) > 0.001 ):
			for note in available_notes:
				if note2note_dist(measure[index], note) <= 2 and abs(int(measure[index].find('notations').find('technical').find('string').text) - int(note.find('notations').find('technical').find('string').text)) < 2:
					nearby_available_notes.append(deepcopy(note))
			rand_available_index = random.randint(0, len(nearby_available_notes)-1)
			if flag == 1:
				while nearby_available_notes[rand_available_index].find('pitch').find('step').text == step and aux_alter == alter:
					rand_available_index = random.randint(0, len(nearby_available_notes)-1)
			rand_available_note = deepcopy(nearby_available_notes[rand_available_index])
			replace_note(measure, available_notes, rand_available_note, index, 0)


# Replaces a note from the measure by another one
def replace_note(measure, available_notes, target_note, index, shift_flag):
	
	# If the note to be replaced has slide technique
	if measure[index].find('notations').find('slide') is not None and measure[index].find('notations').find('slur') is not None:
		# If the note to be replaced starts the slide technique
		if measure[index].find('notations').find('slide').get('type') == "start" and measure[index].find('notations').find('slur').get('type') == "start":
			# If the target note is in the same string as the note to be replaced
			if target_note.find('notations').find('technical').find('string').text == measure[index+1].find('notations').find('technical').find('string').text:
				etree.SubElement(target_note.find('notations'), "slide", type="start")
				etree.SubElement(target_note.find('notations'), "slur", type="start")
			# Otherwise, removes the slide technique tag from the next note
			else:
				measure[index+1].find('notations').find('slide').getparent().remove(measure[index+1].find('notations').find('slide'))
				measure[index+1].find('notations').find('slur').getparent().remove(measure[index+1].find('notations').find('slur'))
		# If the note to be replaced ends the slide technique
		if measure[index].find('notations').find('slide').get('type') == "stop" and measure[index].find('notations').find('slur').get('type') == "stop":
			# If the target note is in the same string as the note to be replaced
			if nota_alvo.find('notations').find('technical').find('string').text == measure[index-1].find('notations').find('technical').find('string').text:
				etree.SubElement(target_note.find('notations'), "slide", type="stop")
				etree.SubElement(target_note.find('notations'), "slur", type="stop")
			# Otherwise, removes the slide technique tag from the previous note
			else:
				measure[index-1].find('notations').find('slide').getparent().remove(measure[index-1].find('notations').find('slide'))
				measure[index-1].find('notations').find('slur').getparent().remove(measure[index-1].find('notations').find('slur'))
	
	# This current function (replace_note()) is used by two other scripts (auto_tune.py and shifter.py), so the flag "shift_flag" identifies which script is using it, because each one have an distinct way to deal with bend techniques
	if shift_flag == 1:
		if measure[index].find('notations').find('technical').find('bend') is not None:
			etree.SubElement(target_note.find('notations').find('technical'), "bend")
			etree.SubElement(target_note.find('notations').find('technical').find('bend'), "bend-alter")
			target_note.find('notations').find('technical').find('bend').find('bend-alter').text = measure[index].find('notations').find('technical').find('bend').find('bend-alter').text
	else:
		if measure[index].find('notations').find('technical').find('bend') is not None:
			for n in range(len(available_notes)):
				if equal_notes_bysf(available_notes[n], target_note) == 1:
					if ( available_notes[n].find('notations').find('technical').find('string').text != available_notes[n+1].find('notations').find('technical').find('string').text ) or ( available_notes[n].find('notations').find('technical').find('fret').text == '0' ):
						continue
			
					begin = available_notes[n].find('notations').find('technical').find('fret').text
					end = available_notes[n+1].find('notations').find('technical').find('fret').text
					dif = (int(end) - int(begin))/2
					dif = str(dif)
			
					etree.SubElement(target_note.find('notations').find('technical'), "bend")
					etree.SubElement(target_note.find('notations').find('technical').find('bend'), "bend-alter")
					target_note.find('notations').find('technical').find('bend').find('bend-alter').text = dif
		
	# Checks if exists triplets
	if measure[index].find('time-modification') is not None:
		etree.SubElement(target_note, "time-modification")
		etree.SubElement(target_note.find('time-modification'), "actual-notes")
		etree.SubElement(target_note.find('time-modification'), "normal-notes")
		target_note.find('time-modification').find('actual-notes').text = '3'
		target_note.find('time-modification').find('normal-notes').text = '2'
		
	target_note.find('type').text = measure[index].find('type').text
	measure[index] = deepcopy(target_note)


# Checks if two notes are equal based on their string and fret values
def equal_notes_bysf(note_a, note_b):
	
	if ( note_a.find('notations').find('technical').find('string').text == note_b.find('notations').find('technical').find('string').text ) and ( note_a.find('notations').find('technical').find('fret').text == note_b.find('notations').find('technical').find('fret').text ):
		return 1
	else:
		return 0


# Returns the midpoint of 'measure', calculates from fret and string
def calc_midpoint(measure):
	
	coordinates_arr = []
	
	for note in list(measure.iter('note')):
		if ( note.find('rest') is None ) and ( note.find('notehead') is None ):
			fret = note.find('notations').find('technical').find('fret').text
			string = note.find('notations').find('technical').find('string').text
			x = int(fret)
			y = 7 - int(string)
			coordinates_arr.append((x, y))
	
	xf = 0
	yf = 0
	for p in coordinates_arr:
		xf += p[0]
		yf += p[1]
	
	xf = xf/len(coordinates_arr)
	yf = yf/len(coordinates_arr)

	return int(round(xf)), int(round(yf))


# Calculates the euclidean distance between a note (by means of fret and string) and a 2D point
def note2point_dist(note, point):
	
	if note.find('rest') is None:
		fret = note.find('notations').find('technical').find('fret').text
		string = note.find('notations').find('technical').find('string').text
	
		x_note = int(fret)
		y_note = 7 - int(string)
		
		x_point = point[0]
		y_point = point[1]
	
		return euclidean_dist(x_note, y_note, x_point, y_point)


# create an etree object of a MusicXML file
def create_root(file_name):
	
	inpt = open(file_name, "r")
	tree = etree.parse(inpt)
	root = tree.getroot()
	
	return root


# Returns an etree-based object, which represents a note 
#	- Quarter C4 note by default
def create_base_note():
	
	note = etree.Element('note')
	etree.SubElement(note, 'pitch')
	etree.SubElement(note.find('pitch'), 'step')
	etree.SubElement(note.find('pitch'), 'octave')
	
	etree.SubElement(note, 'duration')
	etree.SubElement(note, 'voice')
	etree.SubElement(note, 'type')
	
	etree.SubElement(note, 'notations')
	etree.SubElement(note.find('notations'), 'dynamics')
	etree.SubElement(note.find('notations').find('dynamics'), 'f')
	etree.SubElement(note.find('notations'), 'technical')
	etree.SubElement(note.find('notations').find('technical'), 'string')
	etree.SubElement(note.find('notations').find('technical'), 'fret')
	
	note.find('pitch').find('step').text = 'C'
	note.find('pitch').find('octave').text = '4'
	
	note.find('duration').text = '1'
	note.find('voice').text = '1'
	note.find('type').text = 'quarter'
	
	note.find('notations').find('technical').find('string').text = '5'
	note.find('notations').find('technical').find('fret').text = '3'
	
	return note


# Replaces dummy noteheads with double stops. Double stops are a pair of notes played at once. From a list of notes given as input, this function chooses a pair of notes which is close to the midpoint of the measure
def replace_notehead_dStop(measure, list_notes):
	
	list_dStops = []
	
	# Lists all possible double stops based on input list of notes
	for i in range(len(list_notes)):	
		for j in range(len(list_notes)):
			if i == j:
				continue
			if ( note2note_dist(list_notes[i], list_notes[j]) < 3 ) and ( list_notes[i].find('notations').find('technical').find('string').text != list_notes[j].find('notations').find('technical').find('string').text ) and ( abs(int(list_notes[i].find('notations').find('technical').find('string').text) - int(list_notes[j].find('notations').find('technical').find('string').text)) <= 1) :
				auxList = []
			
				auxNote = deepcopy(list_notes[j])
				etree.SubElement(auxNote, "chord")
				
				auxList.append(deepcopy(list_notes[i]))
				auxList.append(deepcopy(auxNote))
				
				list_dStops.append(deepcopy(auxList))
				
	# Chooses the double stop based on the shortest distance from its midpoint to the midpoint of the measure	
	mes_midpoint = calc_midpoint(measure)
	short_dist = 1000
	chosen_dStop = 0
	for i in range(len(list_dStops)):
		dStop_midpoint = calc_list_midpoint(list_dStops[i])
		if euclidean_dist(dStop_midpoint[0], dStop_midpoint[1], mes_midpoint[0], mes_midpoint[1]) < short_dist:
			short_dist = euclidean_dist(dStop_midpoint[0], dStop_midpoint[1], mes_midpoint[0], mes_midpoint[1])
			chosen_dStop = i

	for i in range(len(measure)):
		if measure[i].find('notehead') is not None:
			auxDuration = measure[i].find('type').text
			del measure[i]
			for j in range(len(list_dStops[chosen_dStop])):
				list_dStops[chosen_dStop][j].find('type').text = auxDuration
				measure.insert(i+j, deepcopy(list_dStops[chosen_dStop][j]))


# Splits a note into two:
#	- For ratio = 0: both notes will receive half the time of the original note (50/50)
#	- For ratio = 1: each note will receive an different value of duration from the original note (75/25) 
def split_note(measure, index, ratio):	
	if measure[index].find('rest') is None:
		if ( measure[index].find('notations').find('slide') is not None ) and ( measure[index].find('notations').find('technical').find('bend') is not None ):
			print ("Is not possible to split techniques. Aborting...")
			sys.exit(0)
		else:
			tpl_duration = ("whole", "half", "quarter", "eighth", "16th", "32th", "64th")

			if ratio == 0:
				for d in range(len(tpl_duration)):
					if measure[index].find('type').text == tpl_duration[d]:
						measure[index].find('type').text = deepcopy(tpl_duration[d+1])
						break
	
				clone = deepcopy(measure[index])
				measure.insert(index, deepcopy(clone))

			if ratio == 1:
				clone = deepcopy(measure[index])
				for d in range(len(tpl_duration)):
					if measure[index].find('type').text == tpl_duration[d]:
						clone = deepcopy(measure[index])
						measure[index].find('type').text = deepcopy(tpl_duration[d+1])
						deepcopy(etree.SubElement(measure[index], "dot"))
						clone.find('type').text = deepcopy(tpl_duration[d+2])
						break
	
				measure.insert(index+1, deepcopy(clone))


# Splits a note into two:
#	- For "ratio = 0": both notes will receive half the time of the original note (50/50)
#	- For "ratio = 1": each note will receive an different value of duration from the original note (75/25)
# 	Besides that, two strategies of splitting are used:
#		- For "strategy = 0": keep the original note and the second note is its successor from the list of available notes
#		- For "strategy = 1": keep the original note and the second note is a random note from the list of available notes, respecting the distance criteria
	
def split_note_s(measure, index, available_notes, ratio, strategy):
	
	if measure[index].find('rest') is None:
		if ( measure[index].find('notations').find('slide') is None ) and ( measure[index].find('notations').find('technical').find('bend') is None ):

			tpl_duration = ("whole", "half", "quarter", "eighth", "16th", "32th", "64th")
			clone = None

			if strategy == 0:
				for i in range(len(available_notes)):
					if equal_notes_bysf(measure[index], available_notes[i]) == 1:
						clone = deepcopy(available_notes[i+1])
						break
			
			if strategy == 1:
				nearby_available_notes = []		
				for i in range(len(available_notes)):
					if equal_notes_bysf(measure[index], available_notes[i]) == 1:
						continue
					if ( note2note_dist(measure[index], available_notes[i]) <= 2 ) and ( abs(int(measure[index].find('notations').find('technical').find('string').text) - int(available_notes[i].find('notations').find('technical').find('string').text)) < 2 ):
						nearby_available_notes.append(deepcopy(available_notes[i]))
				rand_index = random.randint(0, len(nearby_available_notes)-1)
				clone = deepcopy(nearby_available_notes[rand_index])

			if ratio == 0:
				if clone is not None:
					for d in range(len(tpl_duration)):
						if measure[index].find('type').text == tpl_duration[d]:
							measure[index].find('type').text = deepcopy(tpl_duration[d+1])
							clone.find('type').text = deepcopy(tpl_duration[d+1])
							break

					measure.insert(index+1, deepcopy(clone))		

			if ratio == 1:
				if clone is not None:
					for d in range(len(tpl_duration)):
						if measure[index].find('type').text == tpl_duration[d]:
							measure[index].find('type').text = deepcopy(tpl_duration[d+1])
							deepcopy(etree.SubElement(measure[index], "dot"))
							clone.find('type').text = deepcopy(tpl_duration[d+2])
							break
				
					measure.insert(index+1, deepcopy(clone))


# Transforms the last note of the current measure and the first note of the next measure into tied notes
def tied_between_measures(measure, i, last_note_prev_mes):

	base_note = deepcopy(create_base_note())
	
	# Inheriting properties from the last note of the previous measure
	base_note.find('pitch').find('step').text = last_note_prev_mes.find('pitch').find('step').text
	if last_note_prev_mes.find('pitch').find('alter') is not None:
		etree.SubElement(base_note.find('pitch'), 'alter')
		base_note.find('pitch').find('alter').text = last_note_prev_mes.find('pitch').find('alter').text
	base_note.find('pitch').find('octave').text = last_note_prev_mes.find('pitch').find('octave').text
	base_note.find('notations').find('technical').find('string').text = last_note_prev_mes.find('notations').find('technical').find('string').text
	base_note.find('notations').find('technical').find('fret').text = last_note_prev_mes.find('notations').find('technical').find('fret').text
	
	# Inheriting the duration from the first note of the current measure
	base_note.find('type').text = measure[i].find('type').text
	if measure[i].find('time-modification') is not None:
		etree.SubElement(base_note, "time-modification")
		etree.SubElement(base_note.find('time-modification'), "actual-notes")
		etree.SubElement(base_note.find('time-modification'), "normal-notes")
		base_note.find('time-modification').find('actual-notes').text = '3'
		base_note.find('time-modification').find('normal-notes').text = '2'

	# Placing the tied note
	etree.SubElement(base_note, "tie", type="stop")
	etree.SubElement(base_note.find('notations'), "tied", type="stop")
	base_note.find('notations').find('dynamics').getparent().remove(base_note.find('notations').find('dynamics'))

	# Copying the created note to the first position of the current measure
	measure[i] = deepcopy(base_note)



