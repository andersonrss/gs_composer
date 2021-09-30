
# -*- coding: utf-8 -*-
from copy import deepcopy
from lxml import etree
import util


# This file has functions that work as rules, determining costs of transitions between sublicks

class CostCalculator:
	def __init__(self, sType):
		
		self.type = sType
		self.cost = 0 

	def calc_cost(self, last_sublick_a, first_sublick_b):
		
		if self.type == "default":
			self.calc_default_cost(last_sublick_a, first_sublick_b)
		elif self.type == "repetition":
			self.calc_repetition_cost(last_sublick_a, first_sublick_b)
		elif self.type == "turnaround":
			self.calc_turnaround_cost(last_sublick_a, first_sublick_b)


	# The distance between notes is an important evaluation criteria because we want licks close to each other, in order to make it easier to play
# Calculates the transition cost based on the euclidean distance between two notes
#	- If the euclidean dist between them is > k
#		-> Transition is penalized, otherwise, is rewarded
	def note_dist(self, note_a, note_b):
		
		k = 2
		
		if note_a.find('rest') is not None or note_b.find('rest') is not None:
			return
		
		dist = util.note2note_dist(note_a, note_b)
		
		if dist > k:
			if self.type == "default":
				self.cost += 300
			elif self.type == "repetition":
				self.cost += 250
			elif self.type == "turnaround":
				self.cost += 300
		else:
			if self.type == "default":
				self.cost += -150
			elif self.type == "repetition":
				self.cost += -100
			elif self.type == "turnaround":
				self.cost += -150


	# Blue notes must be used as passing notes. So, If note_a is blue note and note_b is rest
	#	-> Transition is penalized
	def rest_after_bn(self, note_a, note_b):
		
		if note_a.find('rest') is None and note_b.find('rest') is not None:
			if  note_a.find('pitch').find('step').text == 'F' and note_a.find('pitch').find('alter') is not None and note_a.find('notations').find('technical').find('bend') is None:
				if self.type == "default":
					self.cost += 100
				elif self.type == "repetition":
					self.cost += 100
				elif self.type == "turnaround":
					self.cost += 100


	# If the blue note of pentatonic scale is after the F note, or before the G note
	#	-> Transition is rewarded
	def consec_bn(self, note_a, note_b):
		
		if note_a.find('rest') is not None or note_b.find('rest') is not None:
			return

		if ( note_a.find('pitch').find('step').text == 'F' and note_a.find('pitch').find('alter') is None ) and ( note_b.find('pitch').find('step').text == 'F' and note_b.find('pitch').find('alter') is not None ):
			if self.type == "default":
				self.cost += -100
			elif self.type == "repetition":
				self.cost += -100
			elif self.type == "turnaround":
				self.cost += -100
		
		if ( note_a.find('pitch').find('step').text == 'F' and note_a.find('pitch').find('alter') is not None ) and ( note_b.find('pitch').find('step').text == 'G' and note_b.find('pitch').find('alter') is None ):
			if self.type == "default":
				self.cost += -100
			elif self.type == "repetition":
				self.cost += -100
			elif self.type == "turnaround":
				self.cost += -100


	# If both are consecutive triplet 16th notes
	#	-> transition is rewarded
	def consec_tri_16th(self, note_a, note_b):
		
		if note_a.find('rest') is not None or note_b.find('rest') is not None:
			return
			
		if ( note_a.find('type').text == '16th' and note_a.find('time-modification') is not None ) and ( note_b.find('type').text == '16th' and note_b.find('time-modification') is not None ):
			if self.type == "default":
				self.cost += -100
			elif self.type == "repetition":
				self.cost += -75
			elif self.type == "turnaround":
				self.cost += -75
		

	# If note_a and note_b are triplet notes
	#	-> Transition is rewarded
	#	If they have same duration
	#		-> Transition is rewarded again
	
	# If note_a or note_b is a triplet note and the other does not
	#	-> Transition is penalized
	def triplet(self, note_a, note_b):

		if ( note_a.find('time-modification') is not None ) and ( note_b.find('time-modification') is not None ):
			if self.type == "default":
				self.cost += -125
			elif self.type == "repetition":
				self.cost += -100
			elif self.type == "turnaround":
				self.cost += -100
			if note_a.find('type').text == note_b.find('type').text:
				if self.type == "default":
					self.cost += -75
				elif self.type == "repetition":
					self.cost += -50
				elif self.type == "turnaround":
					self.cost += -75

		elif ( ( note_a.find('time-modification') is not None ) and ( note_b.find('time-modification') is None ) ) or ( ( note_a.find('time-modification') is None ) and ( note_b.find('time-modification') is not None ) ):
			if self.type == "default":
				self.cost += 175
			elif self.type == "repetition":
				self.cost += 150
			elif self.type == "turnaround":
				self.cost += 175


	# If both notes are same
	#	-> Transition is penalized
	def same_notes(self, note_a, note_b):
		
		if ( note_a.find('rest') is None ) and ( note_b.find('rest') is None ):
			if ( note_a.find('notations').find('technical').find('string').text == note_b.find('notations').find('technical').find('string').text ) and ( note_a.find('notations').find('technical').find('fret').text == note_b.find('notations').find('technical').find('fret').text ):
				if self.type == "default":
					self.cost += 75
				elif self.type == "repetition":
					self.cost += 75
				elif self.type == "turnaround":
					self.cost += 75
		

	# If note_b is 1 fret ahead or behind from note_a in minor pentatonic scale
	#	-> Transition is rewarded
	def seq_notes_scale(self, note_a, note_b, root):

		measure = root.find('part').find('measure')
		scale = deepcopy(list(measure.iter('note')))
		
		if ( note_a.find('rest') is None ) and ( note_b.find('rest') is None ):
			for i in range(len(scale)):
				if i == 0:
					if ( note_a.find('pitch').find('step').text == scale[i].find('pitch').find('step').text and ( ( note_a.find('pitch').find('alter') is not None and scale[i].find('pitch').find('alter') is not None ) or ( note_a.find('pitch').find('alter') is None and scale[i].find('pitch').find('alter') is None ) ) ):
						if ( note_b.find('pitch').find('step').text == scale[i+1].find('pitch').find('step').text ) and ( ( note_b.find('pitch').find('alter') is not None and scale[i+1].find('pitch').find('alter') is not None ) or ( note_b.find('pitch').find('alter') is None and scale[i+1].find('pitch').find('alter') is None ) ):
							if util.note2note_dist(note_a, note_b) <= 2:
								if self.type == "default":
									self.cost += -250
								elif self.type == "repetition":
									self.cost += -150
								elif self.type == "turnaround":
									self.cost += -200
					continue
						
				if i == (len(scale)-1):
					if ( note_a.find('pitch').find('step').text == scale[i].find('pitch').find('step').text and ( ( note_a.find('pitch').find('alter') is not None and scale[i].find('pitch').find('alter') is not None ) or ( note_a.find('pitch').find('alter') is None and scale[i].find('pitch').find('alter') is None ) ) ):
						if ( note_b.find('pitch').find('step').text == scale[i-1].find('pitch').find('step').text ) and ( ( note_b.find('pitch').find('alter') is not None and scale[i-1].find('pitch').find('alter') is not None ) or ( note_b.find('pitch').find('alter') is None and scale[i-1].find('pitch').find('alter') is None ) ):
							if util.note2note_dist(note_a, note_b) <= 2:
								if self.type == "default":
									self.cost += -250
								elif self.type == "repetition":
									self.cost += -150
								elif self.type == "turnaround":
									self.cost += -200
					continue
		
				if ( note_a.find('pitch').find('step').text == scale[i].find('pitch').find('step').text and ( ( note_a.find('pitch').find('alter') is not None and scale[i].find('pitch').find('alter') is not None ) or ( note_a.find('pitch').find('alter') is None and scale[i].find('pitch').find('alter') is None ) ) ):
					if ( ( note_b.find('pitch').find('step').text == scale[i-1].find('pitch').find('step').text ) and ( ( note_b.find('pitch').find('alter') is not None and scale[i-1].find('pitch').find('alter') is not None ) or ( note_b.find('pitch').find('alter') is None and scale[i-1].find('pitch').find('alter') is None ) ) ) or ( ( note_b.find('pitch').find('step').text == scale[i+1].find('pitch').find('step').text ) and ( ( note_b.find('pitch').find('alter') is not None and scale[i+1].find('pitch').find('alter') is not None ) or ( note_b.find('pitch').find('alter') is None and scale[i+1].find('pitch').find('alter') is None ) ) ):
						if util.note2note_dist(note_a, note_b) <= 2:
							if self.type == "default":
								self.cost += -250
							elif self.type == "repetition":
								self.cost += -150
							elif self.type == "turnaround":
								self.cost += -200
					continue


	# If duration filled with rest is <= 16
	#	-> Transition is rewarded
	# If duration filled with rest is > 32
	#	-> Transition is penalized
	def rest(self, note_a, note_b):

		acc = 0

		if ( note_a.find('rest') is not None ) or ( note_b.find('rest') is not None ):
			if note_a.find('rest') is not None:
				acc += util.get_duration(note_a)

			if note_b.find('rest') is not None:
				acc += util.get_duration(note_b)

			if acc <= 16:
				if self.type == "default":
					self.cost += -75
				elif self.type == "repetition":
					self.cost += -50
				elif self.type == "turnaround":
					self.cost += -50

			if acc > 32:
				if self.type == "default":
					self.cost += 75
				elif self.type == "repetition":
					self.cost += 50
				elif self.type == "turnaround":
					self.cost += 75


	# This rule analyzes three different cases of bend technique ocurrences
	# Case 1: note_a has bend technique (or vice versa) and both notes are in the same position (fret and string)
	# Case 2: note_a has bend technique, whose alter is equivalent to note_b, which comes after at another string
	# Case 3: note_b has bend technique, whose alter is equivalent to note_a, which comes before at another string
	def bend(self, note_a, note_b, root):

		scale = deepcopy(list(root.find('part').find('measure').iter('note')))

		if ( note_a.find('rest') is None ) and ( note_b.find('rest') is None ): # No rest
			# Case 1
			if ( ( note_a.find('notations').find('technical').find('bend') is not None ) and ( note_b.find('notations').find('technical').find('bend') is None ) ) or ( ( note_a.find('notations').find('technical').find('bend') is None ) and ( note_b.find('notations').find('technical').find('bend') is not None ) ): # If note_a has bend technique and note_b does not, or vice versa
				if ( ( note_a.find('notations').find('technical').find('string').text == note_b.find('notations').find('technical').find('string').text ) and ( note_a.find('notations').find('technical').find('fret').text == note_b.find('notations').find('technical').find('fret').text ) ): # Same fret and string
					if self.type == "default":
						self.cost += -225
					elif self.type == "repetition":
						self.cost += -200
					elif self.type == "turnaround":
						self.cost += -150

			# Case 2
			elif ( note_a.find('notations').find('technical').find('bend') is not None) and ( note_b.find('notations').find('technical').find('bend') is None ): # If note_a has bend technique and note_b does not
				for i in range(len(scale)):
					if ( note_a.find('pitch').find('step').text == scale[i].find('pitch').find('step').text ) and ( note_a.find('pitch').find('octave').text == scale[i].find('pitch').find('octave').text ) and ( ( note_a.find('pitch').find('alter') is None and scale[i].find('pitch').find('alter') is None ) or ( note_a.find('pitch').find('alter') is not None and scale[i].find('pitch').find('alter') is not None ) ): # Looking for note_a on the scale
						if ( note_b.find('pitch').find('step').text == scale[i+1].find('pitch').find('step').text ) and ( note_b.find('pitch').find('octave').text == scale[i+1].find('pitch').find('octave').text ) and ( ( note_b.find('pitch').find('alter') is None and scale[i+1].find('pitch').find('alter') is None ) or ( note_b.find('pitch').find('alter') is not None and scale[i+1].find('pitch').find('alter') is not None ) ): # Checking if note_b comes after note_a
							if ( note_a.find('notations').find('technical').find('string').text != note_b.find('notations').find('technical').find('string').text ) and ( util.distancia_notas(note_a, note_b) <= 3.5 ): # Different strings
								bendAlterAux = float(note_a.find('notations').find('technical').find('bend').find('bend-alter').text)
								if bendAlterAux <= 1:
									if self.type == "default":
										self.cost += -175
									elif self.type == "repetition":
										self.cost += -200
									elif self.type == "turnaround":
										self.cost += -150
	 
			# Case 3
			elif ( note_a.find('notations').find('technical').find('bend') is None ) and ( note_b.find('notations').find('technical').find('bend') is not None ):	# If note_b has bend technique and note_a does not
				for i in range(len(scale)):    
					if ( note_a.find('pitch').find('step').text == scale[i].find('pitch').find('step').text ) and ( note_a.find('pitch').find('octave').text == scale[i].find('pitch').find('octave').text ) and ( ( note_a.find('pitch').find('alter') is None and scale[i].find('pitch').find('alter') is None ) or ( note_a.find('pitch').find('alter') is not None and scale[i].find('pitch').find('alter') is not None ) ): # Looking for note_a on the scale
						if ( note_b.find('pitch').find('step').text == scale[i-1].find('pitch').find('step').text ) and ( note_b.find('pitch').find('octave').text == scale[i-1].find('pitch').find('octave').text ) and ( ( note_b.find('pitch').find('alter') is None and scale[i-1].find('pitch').find('alter') is None ) or ( note_b.find('pitch').find('alter') is not None and scale[i-1].find('pitch').find('alter') is not None ) ): # Checking if note_b comes before note_a
							if ( note_a.find('notations').find('technical').find('string').text != note_b.find('notations').find('technical').find('string').text ) and ( util.distancia_notas(note_a, note_b) <= 3.5 ): # Different strings
								bendAlterAux = float(note_b.find('notations').find('technical').find('bend').find('bend-alter').text)
								if bendAlterAux <= 1:								
									if self.type == "default":
										self.cost += -175
									elif self.type == "repetition":
										self.cost += -200
									elif self.type == "turnaround":
										self.cost += -150
			
			# Extra reward: bend technique between triplet notes
			if ( note_a.find('time-modification') is not None and note_b.find('notations').find('technical').find('bend') is not None and note_b.find('time-modification') is not None ) or ( note_b.find('time-modification') is not None and note_a.find('notations').find('technical').find('bend') is not None and note_a.find('time-modification') is not None ):
				if self.type == "default":
					self.cost += -175
				elif self.type == "repetition":
					self.cost += -175
				elif self.type == "turnaround":
					self.cost += -175


	# If the string difference between both notes is > k
	#	-> Transition is penalized, otherwise, rewarded
	def string_leap(self, note_a, note_b):
	
		k = 1
	
		if note_a.find('rest') is None and note_b.find('rest') is None:
			note_a_string = int(note_a.find('notations').find('technical').find('string').text)
			note_b_string = int(note_b.find('notations').find('technical').find('string').text)
			if abs(note_a_string - note_b_string) > k:
				if self.type == "default":
					self.cost += 150
				elif self.type == "repetition":
					self.cost += 200
				elif self.type == "turnaround":
					self.cost += 200
			else:
				if self.type == "default":
					self.cost += -250
				elif self.type == "repetition":
					self.cost += -100
				elif self.type == "turnaround":
					self.cost += -100


	# If a short duration note comes before a double stop
	#	-> Transition is penalized
	def sn_before_ds(self, note_a, note_b):
		
		k = 8
		
		if ( note_a.find('notehead') is None ) and ( note_b.find('notehead') is not None ):
			if util.get_duration(note_a) >= k:
				if self.type == "default":
					self.cost += -100
				elif self.type == "repetition":
					self.cost += -100
				elif self.type == "turnaround":
					self.cost += -100
			else:
				if self.type == "default":
					self.cost += 100
				elif self.type == "repetition":
					self.cost += 100
				elif self.type == "turnaround":
					self.cost += 100


	# Rewards some transitions between blue notes and other notes like D#, F and G
	def blue_note(self, note_a, note_b):
	
		if note_a.find('rest') is not None or note_b.find('rest') is not None:
			return
		
		if ( util.cipher_notation(note_a) == "D#" or util.cipher_notation(note_a) == 'F' or util.cipher_notation(note_a) == 'G' ) and ( util.cipher_notation(note_b) == "F#" and note_b.find('notations').find('technical').find('bend') is None ):
			if self.type == "default":
				self.cost += -150
			elif self.type == "repetition":
				self.cost += 0
			elif self.type == "turnaround":
				self.cost += 0
		elif ( util.cipher_notation(note_a) == "F#" and note_a.find('notations').find('technical').find('bend') is None ) and ( util.cipher_notation(note_b) == 'F' or util.cipher_notation(note_b) == 'G' ):
			if self.type == "default":
				self.cost += -150
			elif self.type == "repetition":
				self.cost += 0
			elif self.type == "turnaround":
				self.cost += 0
		elif ( util.cipher_notation(note_a) != "D#" or util.cipher_notation(note_a) != 'F' or util.cipher_notation(note_a) != 'G' ) and ( util.cipher_notation(note_b) == "F#" and note_b.find('notations').find('technical').find('bend') is None ):
			if self.type == "default":
				self.cost += 150
			elif self.type == "repetition":
				self.cost += 0
			elif self.type == "turnaround":
				self.cost += 0
		elif ( util.cipher_notation(note_a) == "F#" and note_a.find('notations').find('technical').find('bend') is None ) and ( util.cipher_notation(note_b) != 'F' or util.cipher_notation(note_b) != 'G' ):
			if self.type == "default":
				self.cost += 150
			elif self.type == "repetition":
				self.cost += 0
			elif self.type == "turnaround":
				self.cost += 0


	# Defining costs for default sublicks
	def calc_default_cost(self, last_sublick_a, first_sublick_b):

		if ( last_sublick_a.find('notehead') is not None ) or ( first_sublick_b.find('notehead') is not None ):
			self.sn_before_ds(last_sublick_a, first_sublick_b)
			return

		self.note_dist(last_sublick_a, first_sublick_b)
		self.rest_after_bn(last_sublick_a, first_sublick_b)
		self.blue_note(last_sublick_a, first_sublick_b)
		#self.consec_tri_16th(last_sublick_a, first_sublick_b)
		self.triplet(last_sublick_a, first_sublick_b)
		self.string_leap(last_sublick_a, first_sublick_b)
		self.same_notes(last_sublick_a, first_sublick_b)

		inpt = open("xmls/default_notes.xml", "r")
		tree = etree.parse(inpt)
		root = tree.getroot()
		self.bend(last_sublick_a, first_sublick_b, root)
		
		inpt = open("xmls/default_scale.xml", "r")
		tree = etree.parse(inpt)
		root = tree.getroot()
		self.seq_notes_scale(last_sublick_a, first_sublick_b, root)

		self.rest(last_sublick_a, first_sublick_b)


	# Defining costs for repetition sublicks
	def calc_repetition_cost(self, last_sublick_a, first_sublick_b):
		
		if ( last_sublick_a.find('notehead') is not None ) or ( first_sublick_b.find('notehead') is not None ):
			self.sn_before_ds(last_sublick_a, first_sublick_b)
			return

		self.note_dist(last_sublick_a, first_sublick_b)
		#self.rest_after_bn(last_sublick_a, first_sublick_b)
		#self.consec_bn(last_sublick_a, first_sublick_b)
		#self.blue_note(last_sublick_a, first_sublick_b)
		self.consec_tri_16th(last_sublick_a, first_sublick_b)
		self.triplet(last_sublick_a, first_sublick_b)
		self.string_leap(last_sublick_a, first_sublick_b)
		self.same_notes(last_sublick_a, first_sublick_b)
		
		inpt = open("xmls/repetition_notes.xml", "r")
		tree = etree.parse(inpt)
		root = tree.getroot()
		self.bend(last_sublick_a, first_sublick_b, root)
		
		inpt = open("xmls/repetition_scale.xml", "r")
		tree = etree.parse(inpt)
		root = tree.getroot()
		self.seq_notes_scale(last_sublick_a, first_sublick_b, root)

		self.rest(last_sublick_a, first_sublick_b)


	# Defining costs for turnaround sublicks
	def calc_turnaround_cost(self, last_sublick_a, first_sublick_b):

		self.note_dist(last_sublick_a, first_sublick_b)
		self.rest_after_bn(last_sublick_a, first_sublick_b)
		self.consec_bn(last_sublick_a, first_sublick_b)
		#self.blue_note(last_sublick_a, first_sublick_b)
		self.consec_tri_16th(last_sublick_a, first_sublick_b)
		self.triplet(last_sublick_a, first_sublick_b)
		self.string_leap(last_sublick_a, first_sublick_b)
		self.same_notes(last_sublick_a, first_sublick_b)
		
		inpt = open("xmls/turnaround_notes.xml", "r")
		tree = etree.parse(inpt)
		root = tree.getroot()
		self.bend(last_sublick_a, first_sublick_b, root)
		
		inpt = open("xmls/turnaround_scale.xml", "r")
		tree = etree.parse(inpt)
		root = tree.getroot()
		self.seq_notes_scale(last_sublick_a, first_sublick_b, root)

		self.rest(last_sublick_a, first_sublick_b)
		


