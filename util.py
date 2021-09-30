
# -*- coding: utf-8 -*-
from __future__ import division
from lxml import etree
from copy import *
import random, math


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



