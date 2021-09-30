
# -*- coding: utf-8 -*-
from __future__ import division
from lxml import etree
from copy import copy, deepcopy
import random, math, sys


# Create an etree object of a MusicXML file
def create_root(file_name):
	
	inpt = open(file_name, "r")
	tree = etree.parse(inpt)
	root = tree.getroot()
	
	return root


# Create a domain using the set() function
#	- Domain is the complete set of it's possible values of a variable, with no repetition
def create_domain(arr):
	
	domain = list(set(arr))
	
	return domain


# Create a time change domain by retrieving duplicates based in the first element of <aux_list>, which is presented in check_time_changes() function
def create_tc_domain(time_change):
	
	aux = []
	result = []
	
	for tple in time_change:
		if tple[0] in aux:
			continue
		else:
			aux.append(tple[0])
			result.append(copy(tple))
	
	return result


# Returns the cipher notation of a etree-format note (e.g., 'A', 'G#', etc.)
#	- Rests are represented by 'p'
#	- Tied notes with 'type' attribute equals to "stop" are represented by 't'
def cipher_notation(note):
	
	notation = ""
	
	if note.find('rest') is None:
		if ( note.find('tie') is None ) or ( note.find('tie') is not None and note.find('tie').get('type') == "start" ):
			if note.find('pitch').find('alter') is not None:
				notation = note.find('pitch').find('step').text + '#'
			else:
				notation = note.find('pitch').find('step').text
		else:
			notation = 't'
	else:
		notation = 'p'

	return notation


# Normalizes the probability matrix
def normalize(matrix):
	
	for i in range(len(matrix)):
		total_row = 0
		for j in range(len(matrix[i])):	
			total_row += matrix[i][j]		

		for j in range(len(matrix[i])):
			if total_row == 0:
				matrix[i][j] = 0
			else:	
				matrix[i][j] = matrix[i][j]/total_row


# Get the duration of the input note as a scalar
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


# Returns an etree-based object, which represents a rest 
def create_rest():

	note = etree.Element('note')
	etree.SubElement(note, 'rest')
	etree.SubElement(note, 'duration')
	etree.SubElement(note, 'voice')
	etree.SubElement(note, 'type')
	
	note.find('duration').text = '1'
	note.find('voice').text = '1'
	note.find('type').text = 'quarter'
	
	return note


# Calculates the euclidean distance between two points
def euclidean_dist(xi, yi, xf, yf):

	return math.sqrt(((xf-xi)**2) + ((yf-yi)**2))


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


# Calculates the midpoint of a division
def calc_div_midpoint(div):

	coordinates = [(0, 0)]

	for note in div:
		if note.find('rest') is not None:
			continue
		fret = note.find('notations').find('technical').find('fret').text
		string = note.find('notations').find('technical').find('string').text
		x = int(fret)
		y = 7 - int(string)
		coordinates.append((x, y))

	xf = 0
	yf = 0
	for p in coordinates:
		xf += p[0]
		yf += p[1]

	xf = xf/len(coordinates)
	yf = yf/len(coordinates)

	return round(xf), round(yf)


# Checks time changes in the current note, like triplets or dots
#	- <aux_list> has four indexes, which are described bellow
#	 	- <aux_list[0]> = stores the duration of the input note as a scalar
#	 	- <aux_list[1]> = binary, 1 if note has triplet, 0 if not
#	 	- <aux_list[2]> = binary, 1 if note has dot, 0 if not
#	 	- <aux_list[3]> = stores the original duration of the input note as a string
def check_time_changes(note):
	
	aux_list = []
	
	aux_list.append(get_duration(note))
	if note.find('time-modification') is not None:	
		aux_list.append(1)
	else:
		aux_list.append(0)
	if note.find('dot') is not None:
		aux_list.append(1)
	else:
		aux_list.append(0)
	aux_list.append(note.find('type').text)
	
	return aux_list


# Returns a vector containing, with no repetition, all possible notes of the current div
#	- Does not include rests
#	- Is string-fret based
def fret_string_domain(div):
	
	fs_domain = []
	exists = 0
	
	for mes in div:
		for note_i in mes:
			if note_i.find('rest') is not None:
				continue
			for note_j in fs_domain:
				if ( note_i.find('notations').find('technical').find('string').text == note_j.find('notations').find('technical').find('string').text ) and ( note_i.find('notations').find('technical').find('fret').text == note_j.find('notations').find('technical').find('fret').text ):
					exists = 1
					break
			if exists == 0:
				fs_domain.append(deepcopy(note_i))
			else:
				exists = 0
	
	return fs_domain


# Create a MusicXML file based on domain
def create_xml_file_from_domain(fs_domain, fileName):

	rootB = create_root("xmls/base.xml")
		
	for note in fs_domain:
		if note.find('rest') is not None:
			continue
		n = create_base_note()
		n.find('pitch').find('step').text = note.find('pitch').find('step').text
		if note.find('pitch').find('alter') is not None:
			etree.SubElement(n.find('pitch'), 'alter')
			n.find('pitch').find('alter').text = '1'
		n.find('pitch').find('octave').text = note.find('pitch').find('octave').text
		n.find('type').text = "64th"
		n.find('notations').find('technical').find('string').text = note.find('notations').find('technical').find('string').text
		n.find('notations').find('technical').find('fret').text = note.find('notations').find('technical').find('fret').text
		
		rootB.find('part').find('measure').append(deepcopy(n))
	
	rootB = etree.tostring(rootB)

	output = open(fileName, "wb")
	output.write(rootB)
	output.close()


# Check if the note and the duration belongs to the respective domain
def belongs2domain(s_note, duration, note_domain, durat_domain, pm_note, pm_duration):

	note_id = 0
	duration_id = 0
	
	found_note = 0
	found_duration = 0
	
	for i in range(len(note_domain)):
		if s_note == note_domain[i]:
			note_id = i
			found_note = 1
			break
	
	if found_note == 0:
		highest = 0
		for i in range(len(pm_note)):
			for j in range(len(pm_note[i])):
				if pm_note[i][j] > highest:
					highest = pm_note[i][j]
					note_id = i
	
	for i in range(len(durat_domain)):
		if duration == durat_domain[i]:
			duration_id = i
			found_duration = 1
			break
	
	if found_duration == 0:
		highest = 0
		for i in range(len(pm_duration)):
			for j in range(len(pm_duration[i])):
				if pm_duration[i][j] > highest:
					highest = pm_duration[i][j]
					duration_id = i
	
	return note_id, duration_id


# Returns the string difference between two notes
def string_difference(note_a, note_b):
	
	string_a = int(note_a.find('notations').find('technical').find('string').text)
	string_b = int(note_b.find('notations').find('technical').find('string').text)
	
	difference = abs(string_a - string_b)
	
	return difference


# Checks, by string and fret, if a note is present in an array
def is_present(note, arr):
	
	for n in arr:
		if ( note.find('notations').find('technical').find('string').text == n.find('notations').find('technical').find('string').text ) and ( note.find('notations').find('technical').find('fret').text == n.find('notations').find('technical').find('fret').text ):
			return 1
	return 0


# Checks if one note comes before another on the fretboard 
def comes_first(note_a, note_b):

	# If note_a string is greater than note_b string: note_a -> note_b
	if int(note_a.find('notations').find('technical').find('string').text) > int(note_b.find('notations').find('technical').find('string').text):
		return 1
	# If note_a string is lower than note_b string: note_b -> note_a
	elif int(note_a.find('notations').find('technical').find('string').text) < int(note_b.find('notations').find('technical').find('string').text):
		return 0
	# If both notes are on the same string: check the frets
	elif int(note_a.find('notations').find('technical').find('string').text) == int(note_b.find('notations').find('technical').find('string').text):
		# If note_a fret is lower than note_b fret: note_a -> note_b
		if int(note_a.find('notations').find('technical').find('fret').text) < int(note_b.find('notations').find('technical').find('fret').text):
			return 1
		else:
			return 0


# Sort an note array using insertion sort algorithm
#	- Notes are sorted in ascending order on fretboard
def sort_notes(arr):

	for i in range(1, len(arr)):
		#aux = vetor[i]
		aux_note = deepcopy(arr[i])
		j = i

		#while ( j > 0 ) and ( vetor[j-1] > aux ):
		while ( j > 0 ) and ( comes_first(aux_note, arr[j-1]) == 1 ):
			arr[j] = deepcopy(arr[j-1])
			j -= 1
		
		arr[j] = deepcopy(aux_note)
	
	return arr



