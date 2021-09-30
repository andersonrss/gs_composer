
# -*- coding: utf-8 -*-
from __future__ import division
from lxml import etree
from copy import deepcopy

import os


class Generator:
	def __init__(self, root, obj_type, base_path):	

		self.type = obj_type
		self.base = base_path
		self.root = root
		self.index = 0
		self.durations = []
		self.generated_sublicks = []
		self.paths = []

		# Paths to indexes files
		#	- Single
		self.BEND_PATH = self.type + "_licks/indexes/BEND"
		self.paths.append(self.BEND_PATH)

		self.SLIDE_PATH = self.type + "_licks/indexes/SLIDE"
		self.paths.append(self.SLIDE_PATH)

		self.TRIPLET_PATH = self.type + "_licks/indexes/TRIPLET"
		self.paths.append(self.TRIPLET_PATH)

		self.REST_PATH = self.type + "_licks/indexes/REST"
		self.paths.append(self.REST_PATH)

		self.BLUE_NOTE_PATH = self.type + "_licks/indexes/BLUE_NOTE"
		self.paths.append(self.BLUE_NOTE_PATH)

		self.DOUBLE_STOP_PATH = self.type + "_licks/indexes/DOUBLE_STOP"
		self.paths.append(self.DOUBLE_STOP_PATH)

		self.NORMAL_NOTE_PATH = self.type + "_licks/indexes/NORMAL_NOTE"
		self.paths.append(self.NORMAL_NOTE_PATH)

		#	- Mixed
		self.TRIPLET_BEND_PATH = self.type + "_licks/indexes/TRIPLET_BEND"
		self.paths.append(self.TRIPLET_BEND_PATH)

		self.TRIPLET_BLUE_NOTE_PATH = self.type + "_licks/indexes/TRIPLET_BLUE_NOTE"
		self.paths.append(self.TRIPLET_BLUE_NOTE_PATH)

		self.TRIPLET_REST_PATH = self.type + "_licks/indexes/TRIPLET_REST"
		self.paths.append(self.TRIPLET_REST_PATH)

		#	- Initializing files
		for p in self.paths:
			open(p, "w").close()

	# Setting duration array
	def set_durations(self, *argv):
		self.durations = argv[:]


	''' ***************************************** 
		*				One note				*
		***************************************** '''

	
	# Generates blue note sublicks
	def generate_blueNote_1(self):
		
		measure = self.root.find('part').find('measure')
		notas = []
		count = 0

		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1

		fret = ""
		for i in range(len(notas)):
			if notas[i].find('pitch').find('step').text == 'F' and notas[i].find('pitch').find('alter') is None:
				
				with open(self.base, "r") as b:
					treeB = etree.parse(b)
					rootB = treeB.getroot()
				
				fret = str(int(notas[i].find('notations').find('technical').find('fret').text) + 1)
				notas[i].find('notations').find('technical').find('fret').text = fret
				etree.SubElement(notas[i].find('pitch'), "alter")
				notas[i].find('pitch').find('alter').text = str(1)
				
				rootB.find('part').find('measure').append(notas[i])
				
				self.generated_sublicks.append(rootB)
				
				# File persistence
				rootB = etree.tostring(rootB)
				fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
				with open(fileName, "wb") as out:	
					out.write(rootB)

				# Writing indexes
				with open(self.BLUE_NOTE_PATH, "a") as id_file:
					id_file.write(str(self.index) + ' ')

				self.index += 1

	# Generates blue note + triplet sublicks
	def generate_blueNote_triplet_1(self):
		
		measure = self.root.find('part').find('measure')
		notas = []
		count = 0

		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1

		fret = ""
		for i in range(len(notas)):
			if notas[i].find('pitch').find('step').text == 'F' and notas[i].find('pitch').find('alter') is None:
				
				with open(self.base, "r") as b:
					treeB = etree.parse(b)
					rootB = treeB.getroot()

				etree.SubElement(notas[i], "time-modification")
				etree.SubElement(notas[i].find('time-modification'), "actual-notes")
				etree.SubElement(notas[i].find('time-modification'), "normal-notes")
				notas[i].find('time-modification').find('actual-notes').text = '3'
				notas[i].find('time-modification').find('normal-notes').text = '2'
				
				fret = str(int(notas[i].find('notations').find('technical').find('fret').text) + 1)
				notas[i].find('notations').find('technical').find('fret').text = fret
				etree.SubElement(notas[i].find('pitch'), "alter")
				notas[i].find('pitch').find('alter').text = str(1)

				rootB.find('part').find('measure').append(notas[i])

				self.generated_sublicks.append(rootB)
				
				# File persistence
				rootB = etree.tostring(rootB)
				fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
				with open(fileName, "wb") as out:
					out.write(rootB)

				# Writing indexes
				with open(self.TRIPLET_BLUE_NOTE_PATH, "a") as id_file:
					id_file.write(str(self.index) + ' ')
				
				self.index += 1


	# Generates triplet sublicks
	def generate_triplet_1(self):
		
		measure = self.root.find('part').find('measure')
		notas = []
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1
		
		for note in notas:
			
			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()

			etree.SubElement(note, "time-modification")
			etree.SubElement(note.find('time-modification'), "actual-notes")
			etree.SubElement(note.find('time-modification'), "normal-notes")
			note.find('time-modification').find('actual-notes').text = '3'
			note.find('time-modification').find('normal-notes').text = '2'
			
			rootB.find('part').find('measure').append(note)

			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			# Writing indexes
			with open(self.TRIPLET_PATH, "a") as id_file:
				id_file.write(str(self.index) + ' ')

			self.index += 1


	# Generates bend sublicks
	def generate_bend_1(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0

		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1

		for n in range(len(notas)-1):
		
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text or notas[n].find('notations').find('technical').find('fret').text == '0':
				continue
		
			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			inicio = notas[n].find('notations').find('technical').find('fret').text
			fim = notas[n+1].find('notations').find('technical').find('fret').text

			alter = (int(fim) - int(inicio))/2
			
			if alter > 1:
				continue

			alter = str(alter)

			etree.SubElement(notas[n].find('notations').find('technical'), "bend")
			etree.SubElement(notas[n].find('notations').find('technical').find('bend'), "bend-alter")
			notas[n].find('notations').find('technical').find('bend').find('bend-alter').text = alter
			rootB.find('part').find('measure').append(deepcopy(notas[n]))

			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			# Writing indexes
			with open(self.BEND_PATH, "a") as id_file:
				id_file.write(str(self.index) + ' ')
			
			self.index += 1
		

	# Generates normal note sublicks
	def generate_normalNote_1(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0

		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1

		for note in notas:
		
			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()

			rootB.find('part').find('measure').append(deepcopy(note))
		
			self.generated_sublicks.append(rootB)

			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			# Writing indexes
			with open(self.NORMAL_NOTE_PATH, "a") as id_file:
				id_file.write(str(self.index) + ' ')
			
			self.index += 1


	# Generates rest sublicks
	def generate_rest_1(self):

		for d in self.durations:
		
			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			etree.SubElement(rootB.find('part').find('measure'), "note")
			etree.SubElement(rootB.find('part').find('measure').find('note'), "rest")
			
			etree.SubElement(rootB.find('part').find('measure').find('note'), "duration")
			rootB.find('part').find('measure').find('note').find('duration').text = '1'
			
			etree.SubElement(rootB.find('part').find('measure').find('note'), "voice")
			rootB.find('part').find('measure').find('note').find('voice').text = '1'
			
			etree.SubElement(rootB.find('part').find('measure').find('note'), "type")
			rootB.find('part').find('measure').find('note').find('type').text = d
			
			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			# Writing indexes
			with open(self.REST_PATH, "a") as id_file:
				id_file.write(str(self.index) + ' ')
			
			self.index += 1


	# Genarates rest + triplet sublicks
	def generate_rest_triplet_1(self):

		for d in self.durations:
			
			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			etree.SubElement(rootB.find('part').find('measure'), "note")
			etree.SubElement(rootB.find('part').find('measure').find('note'), "rest")
			
			etree.SubElement(rootB.find('part').find('measure').find('note'), "duration")
			rootB.find('part').find('measure').find('note').find('duration').text = '1'
			
			etree.SubElement(rootB.find('part').find('measure').find('note'), "voice")
			rootB.find('part').find('measure').find('note').find('voice').text = '1'
			
			etree.SubElement(rootB.find('part').find('measure').find('note'), "type")
			rootB.find('part').find('measure').find('note').find('type').text = d
			
			etree.SubElement(rootB.find('part').find('measure').find('note'), "time-modification")
			etree.SubElement(rootB.find('part').find('measure').find('note').find('time-modification'), "actual-notes")
			etree.SubElement(rootB.find('part').find('measure').find('note').find('time-modification'), "normal-notes")
			rootB.find('part').find('measure').find('note').find('time-modification').find('actual-notes').text = '3'
			rootB.find('part').find('measure').find('note').find('time-modification').find('normal-notes').text = '2'
			
			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			# Writing indexes
			with open(self.TRIPLET_REST_PATH, "a") as id_file:
				id_file.write(str(self.index) + ' ')
			
			self.index += 1


	# Generates dotted sublicks
	def generate_dotted_1(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0

		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1

		for note in notas:

			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()

			etree.SubElement(note, "dot")

			rootB.find('part').find('measure').append(deepcopy(note))
		
			self.generated_sublicks.append(rootB)

			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)
			
			self.index += 1


	# Fenerates bend + triplet sublicks
	def generate_triplet_bend_1(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0

		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1

		for n in range(len(notas)-1):
		
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text or notas[n].find('notations').find('technical').find('fret').text == '0':
				continue

			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			inicio = notas[n].find('notations').find('technical').find('fret').text
			fim = notas[n+1].find('notations').find('technical').find('fret').text

			alter = (int(fim) - int(inicio))/2
			
			if alter > 1:
				continue
			
			alter = str(alter)

			etree.SubElement(notas[n].find('notations').find('technical'), "bend")
			etree.SubElement(notas[n].find('notations').find('technical').find('bend'), "bend-alter")
			
			notas[n].find('notations').find('technical').find('bend').find('bend-alter').text = alter
			
			etree.SubElement(notas[n], "time-modification")
			etree.SubElement(notas[n].find('time-modification'), "actual-notes")
			etree.SubElement(notas[n].find('time-modification'), "normal-notes")
			notas[n].find('time-modification').find('actual-notes').text = '3'
			notas[n].find('time-modification').find('normal-notes').text = '2'

			rootB.find('part').find('measure').append(deepcopy(notas[n]))
		
			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			# Writing indexes
			with open(self.TRIPLET_BEND_PATH, "a") as id_file:
				id_file.write(str(self.index) + ' ')
			
			self.index += 1
		

	# Generates dotted + triplet sublicks
	def generate_dotted_triplet_1(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1
		
		for note in notas:
			
			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()

			etree.SubElement(note, "dot")

			etree.SubElement(note, "time-modification")
			etree.SubElement(note.find('time-modification'), "actual-notes")
			etree.SubElement(note.find('time-modification'), "normal-notes")
			note.find('time-modification').find('actual-notes').text = '3'
			note.find('time-modification').find('normal-notes').text = '2'
			
			rootB.find('part').find('measure').append(deepcopy(note))
		
			self.generated_sublicks.append(rootB)

			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			self.index += 1


	# Generates bend + dotted sublicks
	def generate_bend_dotted_1(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0

		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1

		for n in range(len(notas)-1):
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text or notas[n].find('notations').find('technical').find('fret').text == '0':
				continue

			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			inicio = notas[n].find('notations').find('technical').find('fret').text
			fim = notas[n+1].find('notations').find('technical').find('fret').text

			alter = (int(fim) - int(inicio))/2
			alter = str(alter)

			etree.SubElement(notas[n].find('notations').find('technical'), "bend")
			etree.SubElement(notas[n].find('notations').find('technical').find('bend'), "bend-alter")
			
			notas[n].find('notations').find('technical').find('bend').find('bend-alter').text = alter
			
			etree.SubElement(notas[n], "dot")
			
			rootB.find('part').find('measure').append(deepcopy(notas[n]))
		
			self.generated_sublicks.append(rootB)

			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			self.index += 1


	# Generates bend + dotted + triplet sublicks
	def generate_bend_dotted_triplet_1(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0

		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1

		for n in range(len(notas)-1):
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text or notas[n].find('notations').find('technical').find('fret').text == '0':
				continue

			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			inicio = notas[n].find('notations').find('technical').find('fret').text
			fim = notas[n+1].find('notations').find('technical').find('fret').text

			alter = (int(fim) - int(inicio))/2
			alter = str(alter)

			etree.SubElement(notas[n].find('notations').find('technical'), "bend")
			etree.SubElement(notas[n].find('notations').find('technical').find('bend'), "bend-alter")
			
			notas[n].find('notations').find('technical').find('bend').find('bend-alter').text = alter
			
			etree.SubElement(notas[n], "dot")
			
			etree.SubElement(notas[n], "time-modification")
			etree.SubElement(notas[n].find('time-modification'), "actual-notes")
			etree.SubElement(notas[n].find('time-modification'), "normal-notes")
			notas[n].find('time-modification').find('actual-notes').text = '3'
			notas[n].find('time-modification').find('normal-notes').text = '2'
			
			rootB.find('part').find('measure').append(deepcopy(notas[n]))
		
			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)
			
			self.index += 1
		

	''' ***************************************** 
		*				Two notes				*
		***************************************** '''


	# Generates double stops sublicks (dummy noteheads)
	def generate_doubleStop_2(self):
		
		lista_notas = []
		
		for d in self.durations:

			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
		
			etree.SubElement(rootB.find('part').find('measure'), "note")
		
			etree.SubElement(rootB.find('part').find('measure').find('note'), "pitch")
			etree.SubElement(rootB.find('part').find('measure').find('note').find('pitch'), "step")
			rootB.find('part').find('measure').find('note').find('pitch').find('step').text = 'E'
			etree.SubElement(rootB.find('part').find('measure').find('note').find('pitch'), "octave")
			rootB.find('part').find('measure').find('note').find('pitch').find('octave').text = '3'
		
			etree.SubElement(rootB.find('part').find('measure').find('note'), "duration")
			rootB.find('part').find('measure').find('note').find('duration').text = '1'
		
			etree.SubElement(rootB.find('part').find('measure').find('note'), "voice")
			rootB.find('part').find('measure').find('note').find('voice').text = '1'
		
			etree.SubElement(rootB.find('part').find('measure').find('note'), "type")
			rootB.find('part').find('measure').find('note').find('type').text = d
			
			etree.SubElement(rootB.find('part').find('measure').find('note'), "notehead")
			rootB.find('part').find('measure').find('note').find('notehead').text = 'x'
			
			etree.SubElement(rootB.find('part').find('measure').find('note'), "notations")
			etree.SubElement(rootB.find('part').find('measure').find('note').find('notations'), "dynamics")
			etree.SubElement(rootB.find('part').find('measure').find('note').find('notations').find('dynamics'), "f")
			
			etree.SubElement(rootB.find('part').find('measure').find('note').find('notations'), "technical")
			etree.SubElement(rootB.find('part').find('measure').find('note').find('notations').find('technical'), "string")
			rootB.find('part').find('measure').find('note').find('notations').find('technical').find('string').text = '6'
			
			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			# Writing indexes
			with open(self.DOUBLE_STOP_PATH, "a") as id_file:
				id_file.write(str(self.index) + ' ')
			
			self.index += 1


	# Generates forward slide sublicks
	def generate_slide_forward_2(self):
		
		measure = self.root.find('part').find('measure')
		notas = []
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1
		
		for n in range(len(notas)-1):
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text or notas[n].find('notations').find('technical').find('fret').text == '0':
				continue

			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
		
			aux = (deepcopy(notas[n+1]))

			etree.SubElement(notas[n].find('notations'), "slide", type="start")
			etree.SubElement(notas[n].find('notations'), "slur", type="start")

			etree.SubElement(notas[n+1].find('notations'), "slide", type="stop")
			etree.SubElement(notas[n+1].find('notations'), "slur", type="stop")

			rootB.find('part').find('measure').append(deepcopy(notas[n]))
			rootB.find('part').find('measure').append(deepcopy(notas[n+1]))

			notas[n+1] = (deepcopy(aux))

			self.generated_sublicks.append(rootB)

			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			# Writing indexes
			with open(self.SLIDE_PATH, "a") as id_file:
				id_file.write(str(self.index) + ' ')
			
			self.index += 1


	# Generates tied notes sublicks with duration variations
	def generate_tied_var_2(self):
		
		measure = self.root.find('part').find('measure')
		notas = [[] for i in range (len(self.durations))]
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				note.find('type').text = d
				notas[count].append(deepcopy(note))
			count += 1
		
		for i in range(len(notas[0])):	
			for n1 in range(len(notas)):
				for n2 in range(len(notas)):
			
					with open(self.base, "r") as b:
						treeB = etree.parse(b)
						rootB = treeB.getroot()
		
					if n1 == n2:
		
						noteAux = (deepcopy(notas[n1][i]))
						aux = (deepcopy(notas[n1][i]))
						
						etree.SubElement(notas[n1][i], "tie", type="start")
						etree.SubElement(notas[n1][i].find('notations'), "tied", type="start")
			
						etree.SubElement(noteAux, "tie", type="stop")
						etree.SubElement(noteAux.find('notations'), "tied", type="stop")
			
						rootB.find('part').find('measure').append(deepcopy(notas[n1][i]))
						rootB.find('part').find('measure').append(deepcopy(noteAux))
						
						notas[n1][i] = (deepcopy(aux))
						
						self.generated_sublicks.append(rootB)
						
						# File persistence
						rootB = etree.tostring(rootB)
						fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
						with open(fileName, "wb") as out:
							out.write(rootB)
						
						self.index += 1

					else:
				
						aux1 = (deepcopy(notas[n1][i]))
						aux2 = (deepcopy(notas[n2][i]))
						
						etree.SubElement(notas[n1][i], "tie", type="start")
						etree.SubElement(notas[n1][i].find('notations'), "tied", type="start")
						
						etree.SubElement(notas[n2][i],"tie", type="stop")
						etree.SubElement(notas[n2][i].find('notations'), "tied", type="stop")
					
						rootB.find('part').find('measure').append(deepcopy(notas[n1][i]))
						rootB.find('part').find('measure').append(deepcopy(notas[n2][i]))

						notas[n1][i] = (deepcopy(aux1))
						notas[n2][i] = (deepcopy(aux2))
						
						self.generated_sublicks.append(rootB)
						
						# File persistence
						rootB = etree.tostring(rootB)
						fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
						with open(fileName, "wb") as out:
							out.write(rootB)
						
						self.index += 1
						

	# Generates hammer-on sublicks
	def generate_hammerOn_2(self):
		
		measure = self.root.find('part').find('measure')
		notas = []
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1
		
		for n in range(len(notas)-1):
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text:
				continue

			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
		
			aux = (deepcopy(notas[n+1]))

			etree.SubElement(notas[n].find('notations').find('technical'), "hammer-on", type="start")
			notas[n].find('notations').find('technical').find('hammer-on').text = 'H'

			etree.SubElement(notas[n+1].find('notations').find('technical'), "hammer-on", type="stop")

			rootB.find('part').find('measure').append(deepcopy(notas[n]))
			rootB.find('part').find('measure').append(deepcopy(notas[n+1]))

			notas[n+1] = (deepcopy(aux))

			self.generated_sublicks.append(rootB)

			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			self.index += 1
		

	# Generates hammer-on + triplet sublicks
	def generate_hammerOn_triplet_2(self):
		
		measure = self.root.find('part').find('measure')
		notas = []
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1

		for n in range(len(notas)-1):
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text:
				continue

			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
		
			aux = (deepcopy(notas[n+1]))

			etree.SubElement(notas[n].find('notations').find('technical'), "hammer-on", type="start")
			notas[n].find('notations').find('technical').find('hammer-on').text = 'H'

			etree.SubElement(notas[n+1].find('notations').find('technical'), "hammer-on", type="stop")

			etree.SubElement(notas[n], "time-modification")
			etree.SubElement(notas[n].find('time-modification'), "actual-notes")
			etree.SubElement(notas[n].find('time-modification'), "normal-notes")
			notas[n].find('time-modification').find('actual-notes').text = '3'
			notas[n].find('time-modification').find('normal-notes').text = '2'
			
			etree.SubElement(notas[n+1], "time-modification")
			etree.SubElement(notas[n+1].find('time-modification'), "actual-notes")
			etree.SubElement(notas[n+1].find('time-modification'), "normal-notes")
			notas[n+1].find('time-modification').find('actual-notes').text = '3'
			notas[n+1].find('time-modification').find('normal-notes').text = '2'

			rootB.find('part').find('measure').append(deepcopy(notas[n]))
			rootB.find('part').find('measure').append(deepcopy(notas[n+1]))

			notas[n+1] = (deepcopy(aux))

			self.generated_sublicks.append(rootB)

			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			self.index += 1
		

	# Generates pull-off sublicks
	def generate_pullOff_2(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1
		
		for n in range(len(notas)-1):
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text:
				continue
			
			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			aux = (deepcopy(notas[n+1]))
			
			etree.SubElement(notas[n+1].find('notations').find('technical'), "pull-off", type="start")
			notas[n+1].find('notations').find('technical').find('pull-off').text = 'P'
			
			etree.SubElement(notas[n].find('notations').find('technical'), "pull-off", type="stop")
			
			rootB.find('part').find('measure').append(deepcopy(notas[n+1]))
			rootB.find('part').find('measure').append(deepcopy(notas[n]))
			
			notas[n+1] = (deepcopy(aux))
			
			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)
			
			self.index += 1
		

	# Generates pull-off + triplet sublicks
	def generate_pullOff_triplet_2(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1
		
		for n in range(len(notas)-1):
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text:
				continue
			
			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			aux = (deepcopy(notas[n+1]))
			
			etree.SubElement(notas[n+1].find('notations').find('technical'), "pull-off", type="start")
			notas[n+1].find('notations').find('technical').find('pull-off').text = 'P'
			
			etree.SubElement(notas[n].find('notations').find('technical'), "pull-off", type="stop")
				
			etree.SubElement(notas[n+1], "time-modification")
			etree.SubElement(notas[n+1].find('time-modification'), "actual-notes")
			etree.SubElement(notas[n+1].find('time-modification'), "normal-notes")
			notas[n+1].find('time-modification').find('actual-notes').text = '3'
			notas[n+1].find('time-modification').find('normal-notes').text = '2'
			
			etree.SubElement(notas[n], "time-modification")
			etree.SubElement(notas[n].find('time-modification'), "actual-notes")
			etree.SubElement(notas[n].find('time-modification'), "normal-notes")
			notas[n].find('time-modification').find('actual-notes').text = '3'
			notas[n].find('time-modification').find('normal-notes').text = '2'
			
			rootB.find('part').find('measure').append(deepcopy(notas[n+1]))
			rootB.find('part').find('measure').append(deepcopy(notas[n]))
			
			notas[n+1] = (deepcopy(aux))
			
			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)
			
			self.index += 1
		

	# Generates hammer-on sublicks with duration variations
	def generate_hammerOn_var_2(self):
		
		measure = self.root.find('part').find('measure')
		notas = [[] for i in range (len(self.durations))]
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				note.find('type').text = d
				notas[count].append(deepcopy(note))
			count += 1
			
		for n1 in range(len(notas)):
			for n2 in range(len(notas)):
				if n1 == n2:
					continue
				for m1 in range(len(notas[n1])-1):
					if notas[n1][m1].find('notations').find('technical').find('string').text != notas[n2][m1+1].find('notations').find('technical').find('string').text:
						continue
					
					with open(self.base, "r") as b:
						treeB = etree.parse(b)
						rootB = treeB.getroot()
					
					aux1 = (deepcopy(notas[n1][m1]))
					aux2 = (deepcopy(notas[n2][m1+1]))
					
					etree.SubElement(notas[n1][m1].find('notations').find('technical'), "hammer-on", type="start")
					notas[n1][m1].find('notations').find('technical').find('hammer-on').text = 'H'
					
					etree.SubElement(notas[n2][m1+1].find('notations').find('technical'), "hammer-on", type="stop")
					
					rootB.find('part').find('measure').append(deepcopy(notas[n1][m1]))
					rootB.find('part').find('measure').append(deepcopy(notas[n2][m1+1]))
				
					notas[n1][m1] = (deepcopy(aux1))
					notas[n2][m1+1] = (deepcopy(aux2))
					
					self.generated_sublicks.append(rootB)
		
					# File persistence
					rootB = etree.tostring(rootB)
					fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
					with open(fileName, "wb") as out:
						out.write(rootB)
		
					self.index += 1
		

	# Generates pull-off sublicks with duration variations
	def generate_pullOff_var_2(self):
		
		measure = self.root.find('part').find('measure')
		notas = [[] for i in range (len(self.durations))]
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				note.find('type').text = d
				notas[count].append(deepcopy(note))
			count += 1
			
		for n1 in range(len(notas)):
			for n2 in range(len(notas)):
				if n1 == n2:
					continue
				for m1 in range(len(notas[n1])-1):
					if notas[n1][m1].find('notations').find('technical').find('string').text != notas[n2][m1+1].find('notations').find('technical').find('string').text:
						continue
					
					with open(self.base, "r") as b:
						treeB = etree.parse(b)
						rootB = treeB.getroot()
					
					aux1 = (deepcopy(notas[n1][m1]))
					aux2 = (deepcopy(notas[n2][m1+1]))
					
					etree.SubElement(notas[n2][m1+1].find('notations').find('technical'), "pull-off", type="start")
					notas[n2][m1+1].find('notations').find('technical').find('pull-off').text = 'P'
					
					etree.SubElement(notas[n1][m1].find('notations').find('technical'), "pull-off", type="stop")
					
					rootB.find('part').find('measure').append(deepcopy(notas[n2][m1+1]))
					rootB.find('part').find('measure').append(deepcopy(notas[n1][m1]))
				
					notas[n1][m1] = (deepcopy(aux1))
					notas[n2][m1+1] = (deepcopy(aux2))
					
					self.generated_sublicks.append(rootB)
		
					# File persistence
					rootB = etree.tostring(rootB)
					fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
					with open(fileName, "wb") as out:
						out.write(rootB)
		
					self.index += 1
		

	# Generates backward slide sublicks
	def generate_slide_backward_2(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1
		
		for n in range(len(notas)-1):
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text or notas[n].find('notations').find('technical').find('fret').text == '0':
				continue
			
			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			aux = (deepcopy(notas[n+1]))
			
			etree.SubElement(notas[n+1].find('notations'), "slide", type="start")
			etree.SubElement(notas[n+1].find('notations'), "slur", type="start")
			
			etree.SubElement(notas[n].find('notations'), "slide", type="stop")
			etree.SubElement(notas[n].find('notations'), "slur", type="stop")
			
			rootB.find('part').find('measure').append(deepcopy(notas[n+1]))
			rootB.find('part').find('measure').append(deepcopy(notas[n]))
			
			notas[n+1] = (deepcopy(aux))
			
			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)
			
			self.index += 1
		

	# Generate forward slide sublicks with duration variations
	def generate_slide_forward_var_2(self):
		
		measure = self.root.find('part').find('measure')
		notas = [[] for i in range (len(self.durations))]
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				note.find('type').text = d
				notas[count].append(deepcopy(note))
			count += 1

		for n1 in range(len(notas)):
			for n2 in range(len(notas)):
				if n1 == n2:
					continue
				for m1 in range(len(notas[n1])-1):
					if notas[n1][m1].find('notations').find('technical').find('string').text != notas[n2][m1+1].find('notations').find('technical').find('string').text or notas[n1][m1].find('notations').find('technical').find('fret').text == '0':
						continue
					
					with open(self.base, "r") as b:
						treeB = etree.parse(b)
						rootB = treeB.getroot()
					
					aux1 = (deepcopy(notas[n1][m1]))
					aux2 = (deepcopy(notas[n2][m1+1]))
					
					etree.SubElement(notas[n1][m1].find('notations'), "slide", type="start")
					etree.SubElement(notas[n1][m1].find('notations'), "slur", type="start")
		
					etree.SubElement(notas[n2][m1+1].find('notations'), "slide", type="stop")
					etree.SubElement(notas[n2][m1+1].find('notations'), "slur", type="stop")
		
					rootB.find('part').find('measure').append(deepcopy(notas[n1][m1]))
					rootB.find('part').find('measure').append(deepcopy(notas[n2][m1+1]))
				
					notas[n1][m1] = (deepcopy(aux1))
					notas[n2][m1+1] = (deepcopy(aux2))
					
					self.generated_sublicks.append(rootB)
		
					# File persistence
					rootB = etree.tostring(rootB)
					fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
					with open(fileName, "wb") as out:
						out.write(rootB)
		
					self.index += 1
		

	# Generate backward slide sublicks with duration variations
	def generate_slide_backward_var_2(self):
		
		measure = self.root.find('part').find('measure')
		notas = [[] for i in range (len(self.durations))]
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				note.find('type').text = d
				notas[count].append(deepcopy(note))
			count += 1
			
		for n1 in range(len(notas)):
			for n2 in range(len(notas)):
				if n1 == n2:
					continue
				for m1 in range(len(notas[n1])-1):
					if notas[n1][m1].find('notations').find('technical').find('string').text != notas[n2][m1+1].find('notations').find('technical').find('string').text or notas[n1][m1].find('notations').find('technical').find('fret').text == '0':
						continue
					
					with open(self.base, "r") as b:
						treeB = etree.parse(b)
						rootB = treeB.getroot()
					
					aux1 = (deepcopy(notas[n1][m1]))
					aux2 = (deepcopy(notas[n2][m1+1]))
					
					etree.SubElement(notas[n2][m1+1].find('notations'), "slide", type="start")
					etree.SubElement(notas[n2][m1+1].find('notations'), "slur", type="start")
					
					etree.SubElement(notas[n1][m1].find('notations'), "slide", type="stop")
					etree.SubElement(notas[n1][m1].find('notations'), "slur", type="stop")
		
					rootB.find('part').find('measure').append(deepcopy(notas[n2][m1+1]))
					rootB.find('part').find('measure').append(deepcopy(notas[n1][m1]))
					
					notas[n1][m1] = (deepcopy(aux1))
					notas[n2][m1+1] = (deepcopy(aux2))
					
					self.generated_sublicks.append(rootB)
		
					# File persistence
					rootB = etree.tostring(rootB)
					fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
					with open(fileName, "wb") as out:
						out.write(rootB)
		
					self.index += 1
		

	# Generates forward slide + triplet sublicks
	def generate_slide_forward_triplet_2(self):
		
		measure = self.root.find('part').find('measure')
		notas = []
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1
		
		for n in range(len(notas)-1):
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text or notas[n].find('notations').find('technical').find('fret').text == '0':
				continue

			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			aux = (deepcopy(notas[n+1]))
			
			etree.SubElement(notas[n], "time-modification")
			etree.SubElement(notas[n].find('time-modification'), "actual-notes")
			etree.SubElement(notas[n].find('time-modification'), "normal-notes")
			notas[n].find('time-modification').find('actual-notes').text = '3'
			notas[n].find('time-modification').find('normal-notes').text = '2'
			
			etree.SubElement(notas[n+1], "time-modification")
			etree.SubElement(notas[n+1].find('time-modification'), "actual-notes")
			etree.SubElement(notas[n+1].find('time-modification'), "normal-notes")
			notas[n+1].find('time-modification').find('actual-notes').text = '3'
			notas[n+1].find('time-modification').find('normal-notes').text = '2'
		
			etree.SubElement(notas[n].find('notations'), "slide", type="start")
			etree.SubElement(notas[n].find('notations'), "slur", type="start")

			etree.SubElement(notas[n+1].find('notations'), "slide", type="stop")
			etree.SubElement(notas[n+1].find('notations'), "slur", type="stop")

			rootB.find('part').find('measure').append(deepcopy(notas[n]))
			rootB.find('part').find('measure').append(deepcopy(notas[n+1]))

			notas[n+1] = (deepcopy(aux))

			self.generated_sublicks.append(rootB)

			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)

			self.index += 1
		

	# Generates backward slide + triplet sublicks
	def generate_slide_backward_triplet_2(self):

		measure = self.root.find('part').find('measure')
		notas = []
		count = 0
		
		for d in self.durations:
			for note in list(measure.iter('note')):
				notas.append(deepcopy(note))
				notas[count].find('type').text = d
				count += 1
		
		for n in range(len(notas)-1):
			if notas[n].find('notations').find('technical').find('string').text != notas[n+1].find('notations').find('technical').find('string').text or notas[n].find('notations').find('technical').find('fret').text == '0':
				continue
			
			with open(self.base, "r") as b:
				treeB = etree.parse(b)
				rootB = treeB.getroot()
			
			aux = (deepcopy(notas[n+1]))
			
			etree.SubElement(notas[n], "time-modification")
			etree.SubElement(notas[n].find('time-modification'), "actual-notes")
			etree.SubElement(notas[n].find('time-modification'), "normal-notes")
			notas[n].find('time-modification').find('actual-notes').text = '3'
			notas[n].find('time-modification').find('normal-notes').text = '2'
			
			etree.SubElement(notas[n+1], "time-modification")
			etree.SubElement(notas[n+1].find('time-modification'), "actual-notes")
			etree.SubElement(notas[n+1].find('time-modification'), "normal-notes")
			notas[n+1].find('time-modification').find('actual-notes').text = '3'
			notas[n+1].find('time-modification').find('normal-notes').text = '2'
			
			etree.SubElement(notas[n+1].find('notations'), "slide", type="start")
			etree.SubElement(notas[n+1].find('notations'), "slur", type="start")
			
			etree.SubElement(notas[n].find('notations'), "slide", type="stop")
			etree.SubElement(notas[n].find('notations'), "slur", type="stop")
			
			rootB.find('part').find('measure').append(deepcopy(notas[n+1]))
			rootB.find('part').find('measure').append(deepcopy(notas[n]))
			
			notas[n+1] = (deepcopy(aux))
			
			self.generated_sublicks.append(rootB)
			
			# File persistence
			rootB = etree.tostring(rootB)
			fileName = self.type + "_licks/sublicks/sublick_%s.xml" % self.index
			with open(fileName, "wb") as out:
				out.write(rootB)
			
			self.index += 1
		


