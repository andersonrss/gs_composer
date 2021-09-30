
# -*- coding: utf-8 -*-
from datetime import datetime
import random, subprocess, os, sys


class Generate:
	def __init__(self, obj_type):

		# Variables that represents the sublick type rate, used as input parameters to the solver
		#	- Each value will determine the size of a subset of the database related to the sublick type, which is based on a given feature (e.g. bend technique, slide technique, triplet notes, etc.)
		self.r_bend = 0.0
		self.r_bn = 0.0
		self.r_slide = 0.0
		self.r_tri = 0.0
		self.r_tri_bend = 0.0
		self.r_tri_bn = 0.0
		self.r_note = 0.0
		
		self.type = obj_type
		self.solver_path = "solver/executable"


	# Randomly, and in a defined range, sets the number of BEND techniques that should appear in the lick, as well the respective sublick type rate
	def get_set_nBends(self, tmin, tmax, bend_rate):
		n_bend = random.randint(tmin, tmax)
		if n_bend != 0:
			self.r_bend = bend_rate
		return n_bend


	# Based on a probability, sets the number of BLUE NOTES that should appear in the lick, as well the respective sublick type rate
	def get_nBlueNotes(self, probab, bn_rate):
		n_bn = 0
		nRandom = round(random.random(), 2)
		if nRandom <= probab:
			n_bn = 1
			self.r_bn = bn_rate
		else:
			n_bn = 0
		return n_bn


	# Randomly, and in a defined range, sets the number of SLIDE techniques that should appear in the lick, as well the sublick type rate
	def get_set_nSlides(self, tmin, tmax, slide_rate):
		n_slide = random.randint(tmin, tmax)
		if n_slide != 0:
			self.r_slide = slide_rate
		return n_slide

	#revisar <-----
	# Randomly and in a defined range, sets the number of TRIPLETS that should appear in the lick, as well the sublick type rate
	#	- the number of tri can only receive values multiples of 3
	def get_set_nTriplets(self, tmin, tmax, tri_rate):
		n_tri = random.randint(tmin, tmax)
		if n_tri != 0:
			self.r_tri = tri_rate
			#n_tri = 3 * n_tri
		return n_tri

	# Randomly and in a defined range, sets the number of TRIPLET notes with BEND technique that should appear in the lick, as well the respective sublick type rate
	def get_set_nTriplets_bend(self, tmin, tmax, tri_bend_rate):
		n_tri_bend = random.randint(tmin, tmax)
		if n_tri_bend != 0:
			self.r_tri_bend = tri_bend_rate
		return n_tri_bend


	# Based on a probability, sets the number of TRIPLETS notes of BLUE NOTE type that should appear in the lick, as well the respective sublick type rate
	def get_nTriplets_blueNote(self, probab, tri_bn_rate):
		n_tri_bn = 0
		nRandom = round(random.random(), 2)
		if nRandom <= probab:
			n_tri_bn = 1
			self.r_tri_bn = tri_bn_rate
		else:
			n_tri_bn = 0
		return n_tri_bn


	# Based on a probability, sets the number of TRIPLET notes of REST type that should appear in the lick, as well the sublick type rate
	def get_nTriplets_rest(self, probab):
		n_rest = 0
		nRandom = round(random.random(), 2)
		if nRandom <= probab:
			n_rest = 1
		else:
			n_rest = 0
		return n_rest


	# Based on a probability, sets the number of RESTS that should appear in the lick, as well the sublick type rate
	def get_nRests(self, probab):
		n_rest = 0
		nRandom = round(random.random(), 2)
		if nRandom <= probab:
			n_rest = 1
		else:
			n_rest = 0
		return n_rest


	# Based on a probability, sets the number of DOUBLE STOPS that should appear in the lick, as well the sublick type rate
	def get_nDStops(self, probab):
		n_dStop = 0
		nRandom = round(random.random(), 2)
		if nRandom <= probab:
			n_dStop = 1
		else:
			n_dStop = 0
		return n_dStop


	# randomly, and in a defined range, sets the number of DEFAULT NOTES that should appear in the lick, as well the respective sublick type rate
	def get_set_nNotes(self, tmin, tmax, note_rate):
		n_note = random.randint(tmin, tmax)
		self.r_note = note_rate
		return n_note


	# Calls the solver that generates DEFAULT licks
	def solver(self, 
	n_bend, 
	n_bn, 
	n_slide, 
	n_tri, 
	n_tri_bend, 
	n_tri_bn, 
	n_tri_rest, 
	n_rest, 
	n_dStop, 
	n_note):
		subprocess.call([self.solver_path, 
		str(n_bend), str(self.r_bend), 
		str(n_bn), str(self.r_bn), 
		str(n_slide), str(self.r_slide), 
		str(n_tri), str(self.r_tri), 
		str(n_tri_bend), str(self.r_tri_bend), 
		str(n_tri_bn), str(self.r_tri_bn), 
		str(n_tri_rest), 
		str(n_rest), 
		str(n_dStop), 
		str(n_note), str(self.r_note), 
		str(self.type)])


	# Concatenates sublicks
	def concat(self, route_path, result_lick_dir, sublicks_dir):
		ret = subprocess.call(["python3", "sublick_concatenator.py", route_path, result_lick_dir, sublicks_dir, self.type])
		return ret

	
	# Writes in a log file the parametrizations used on creation of DEFAULT licks
	def create_log(self, 
	ifile, 
	n_bend, 
	n_bn, 
	n_slide, 
	n_tri, 
	n_tri_bend, 
	n_tri_bn, 
	n_tri_rest, 
	n_rest, 
	n_dStop, 
	n_note, 
	ret):
		date_time = datetime.now()
		date_time = date_time.strftime("%d/%m/%Y-%H:%M:%S")

		status = ""
		if ret == 0:
			status = "SUCCESS"
		elif ret == 1:
			status = "NO SOLUTION"

		ifile.write("Type				Quantity	Rate\n" +
					"BEND:				" + str(n_bend)  + "			%.1f\n" % self.r_bend  + 
					"BLUE_NOTE:			" + str(n_bn) + "			%.1f\n" % self.r_bn + 
					"SLIDE:				" + str(n_slide) + "			%.1f\n" % self.r_slide + 
					"TRIPLET:			" + str(n_tri) + "			%.1f\n" % self.r_tri + 
					"TRIPLET_BEND:		" + str(n_tri_bend) + "			%.1f\n" % self.r_tri_bend + 
					"TRIPLET_BLUE_NOTE:	" + str(n_tri_bn) + "			%.1f\n" % self.r_tri_bn + 
					"TRIPLET_REST:		" + str(n_tri_rest) + "			 -\n" + 
					"REST:				" + str(n_rest) + "			 -\n" + 
					"DOUBLE_STOP:		" + str(n_dStop) + "			 -\n" + 
					"NORMAL_NOTE:		" + str(n_note) + "			%.1f\n" % self.r_note + 
					"STATUS: 			" + status + '\n' + 
					"DATE: 				" + str(date_time) + '\n' + 
					"-----------------------------------------------\n")


	# Calls a procedure that generates repetition patterns to create REPETITION licks
	def repetition_cases(self, case):
		subprocess.call(["python3", "repetition_licks/repetition_cases.py", str(case)])




