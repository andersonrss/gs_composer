
# -*- coding: utf-8 -*-
import util
from copy import deepcopy


# This file has functions that work as rules, determining costs of transitions between licks

# The distance between notes is an important evaluation criteria because we want licks close to each other, in order to make it easier to play
# Calculates the transition cost based on the euclidean distance between two notes
#	- If the euclidean dist between them is > k
#		-> Transition is penalized, otherwise, is rewarded
def notes_dist(note_a, note_b):

	k = 2

	if note_a.find('rest') is not None or note_b.find('rest') is not None:
		return 0
	
	dist = util.note2note_dist(note_a, note_b)
	
	if dist > k:
		cost = 200
	else:
		cost = -100
	
	return cost


# If both notes are equivalent
#	-> Transition is rewarded
def equal_notes(note_a, note_b):
	
	cost = 0
	
	if ( note_a.find('rest') is None ) and ( note_b.find('rest') is None ):
		if ( note_a.find('notations').find('technical').find('string').text == note_b.find('notations').find('technical').find('string').text ) and ( note_a.find('notations').find('technical').find('fret').text == note_b.find('notations').find('technical').find('fret').text ):
			cost = -50

	return cost


# If note_b is 1 fret ahead or behind from note_a in minor pentatonic scale
#	-> Transition is rewarded
def seq_notes_scale(note_a, note_b, root):

	cost = 0

	measure = root.find('part').find('measure')
	scale = deepcopy(list(measure.iter('note')))

	if ( note_a.find('rest') is None ) and ( note_b.find('rest') is None ):
		for i in range(len(scale)):
			if i == 0:
				if ( note_a.find('pitch').find('step').text == scale[i].find('pitch').find('step').text and ( ( note_a.find('pitch').find('alter') is not None and scale[i].find('pitch').find('alter') is not None ) or ( note_a.find('pitch').find('alter') is None and scale[i].find('pitch').find('alter') is None ) ) ):
					if ( note_b.find('pitch').find('step').text == scale[i+1].find('pitch').find('step').text ) and ( ( note_b.find('pitch').find('alter') is not None and scale[i+1].find('pitch').find('alter') is not None ) or ( note_b.find('pitch').find('alter') is None and scale[i+1].find('pitch').find('alter') is None ) ):
						if util.note2note_dist(note_a, note_b) <= 2:
							cost = -150
				continue
					
			if i == (len(scale)-1):
				if ( note_a.find('pitch').find('step').text == scale[i].find('pitch').find('step').text and ( ( note_a.find('pitch').find('alter') is not None and scale[i].find('pitch').find('alter') is not None ) or ( note_a.find('pitch').find('alter') is None and scale[i].find('pitch').find('alter') is None ) ) ):
					if ( note_b.find('pitch').find('step').text == scale[i-1].find('pitch').find('step').text ) and ( ( note_b.find('pitch').find('alter') is not None and scale[i-1].find('pitch').find('alter') is not None ) or ( note_b.find('pitch').find('alter') is None and scale[i-1].find('pitch').find('alter') is None ) ):
						if util.note2note_dist(note_a, note_b) <= 2:
							cost = -150
				continue
	
			if ( note_a.find('pitch').find('step').text == scale[i].find('pitch').find('step').text and ( ( note_a.find('pitch').find('alter') is not None and scale[i].find('pitch').find('alter') is not None ) or ( note_a.find('pitch').find('alter') is None and scale[i].find('pitch').find('alter') is None ) ) ):
				if ( ( note_b.find('pitch').find('step').text == scale[i-1].find('pitch').find('step').text ) and ( ( note_b.find('pitch').find('alter') is not None and scale[i-1].find('pitch').find('alter') is not None ) or ( note_b.find('pitch').find('alter') is None and scale[i-1].find('pitch').find('alter') is None ) ) ) or ( ( note_b.find('pitch').find('step').text == scale[i+1].find('pitch').find('step').text ) and ( ( note_b.find('pitch').find('alter') is not None and scale[i+1].find('pitch').find('alter') is not None ) or ( note_b.find('pitch').find('alter') is None and scale[i+1].find('pitch').find('alter') is None ) ) ):
					if util.note2note_dist(note_a, note_b) <= 2:
						cost = -150
				continue

	return cost


# If duration filled with rests is <= 16
#	-> Transition is rewarded
# If duration filled with rests is > 32
#	-> Transition is penalized
def rests(note_a, note_b):
	
	acc = 0
	cost = 0
	
	if ( note_a.find('rest') is not None ) or ( note_b.find('rest') is not None ):
		if note_a.find('rest') is not None:
			acc += util.get_duration(note_a)
		
		if note_b.find('rest') is not None:
			acc += util.get_duration(note_b)
	
		if acc <= 16:
			cost = -50
		
		if acc > 32:
			cost = 75
				
	return cost


# If transirion occurs between a repetition lick and a normal lick
def repetition(lick_a, lick_b):

	cost = 0

	if ( util.isRepetition(lick_a) and not util.isRepetition(lick_b) ) or ( not util.isRepetition(lick_a) and util.isRepetition(lick_b) ):
		cost += -50

	return cost


		
