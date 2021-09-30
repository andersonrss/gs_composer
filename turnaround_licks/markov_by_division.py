
# -*- coding: utf-8 -*-
from __future__ import division
from copy import copy, deepcopy
import random, os, sys, math
import util, prob_matrix

from lxml import etree

# Changing the seed
random.seed()

db_path = "turnaround_licks/licks/"
dom_path = "turnaround_licks/domains/"

# The measure that will be processed
mes = sys.argv[1]

# Number of measure divisions (submeasure)
nDiv = int(sys.argv[2])

# Size of the measure to be generated
mes_size = int(sys.argv[3])

# Knowing the number of licks
nLicks = 0
for arquivo in os.listdir(db_path):
	nLicks += 1

# Stores the notes of the input licks in notation/etree (after) format, with every note in its corresponding division
notes = [[] for i in range(nDiv)] #etree/#string

# Stores the notes/durations of the input licks in etree format, distributed according to the lick to which it belongs 
notes_by_lick = [[[] for j in range(nLicks)] for i in range(nDiv)] #etree

# Stores time modifications (like triplets or dots) that occur in the notes of the input licks
#	- Let d(n) the duration of a musical note n
#		- If we change n to a triplet, then the new duration d' of n is d'(n) = 2/3 * d(n)
#	- In the case of dotted notes, d' should be like d'(n) = d(n) + d(n)/2
time_changes = [[] for i in range(nDiv)]

# Stores the midpoint coordinates (fret, string) of each division
#	- The midpoint is based on all notes of a division
#	- Given a set of notes N = {n1, n2, ..., ni} from a division D and their fret-string pairs, the midpoint coordinates for division D are calculated as (f1 + f2 + ... + fi)/N for frets and (s1 + s2 + ... + si)/N for strings
midpoints = [[0 for i in range(2)] for i in range(nDiv)]

# Midpoints of all processed turnaround licks
midpoints = [[0 for i in range(2)] for i in range(nDiv)]

# Counts the total number of licks
id_lick = 0
# Iterate over all licks in the data directory
for f in os.listdir(db_path):
	root = util.create_root(db_path + f)
	#print(db_path + f)
	for measure in list(root.find('part').iter('measure')):
		# Check, by id, the measure to be processed
		if measure.get('number') == mes:
			measure_notes = []
			# Creates a list of notes of the current measure
			measure_notes = list(measure.iter('note'))
			# Calculates the number of notes per division
			notes_per_div = int(round(len(measure_notes)/nDiv))
			# Default counter; div counter; note counter
			count = div = n = 0
			# Iterate over list of notes
			while n < (len(measure_notes)):
				# If the div counter is in the last division
				#	- Adds the remaining notes to the current div
				if div == (len(notes)-1):
					notes[div].append(deepcopy(measure_notes[n]))
					notes_by_lick[div][id_lick].append(deepcopy(measure_notes[n]))
					time_changes[div].append(copy(util.check_time_changes(measure_notes[n])))
					# If the current note is the last note of the measure
					# 	- Calculates the division midpoint and pass to the next lick
					if n == (len(measure_notes)-1):
						aux_midpoint = util.calc_div_midpoint(notes[div])
						midpoints[div][0] += aux_midpoint[0]
						midpoints[div][1] += aux_midpoint[1]
					n += 1
				# Allocating notes for each division based on 'notes_per_div'
				elif count < notes_per_div:
					notes[div].append(deepcopy(measure_notes[n]))
					notes_by_lick[div][id_lick].append(deepcopy(measure_notes[n]))
					time_changes[div].append(copy(util.check_time_changes(measure_notes[n])))
					count += 1
					n += 1
				# If the current note is the last note of the division
				#	- Calculates the division midpoint and pass to the next division
				else:
					aux_midpoint = util.calc_div_midpoint(notes[div])
					midpoints[div][0] += aux_midpoint[0]
					midpoints[div][1] += aux_midpoint[1]
					div += 1
					count = 0
	id_lick += 1

# Get the general midpoint, which is based on all divisions of the same tier, by dividing the acumulated value by the number of licks 
for i in range(len(midpoints)):
	midpoints[i][0] = round(midpoints[i][0]/nLicks)
	midpoints[i][1] = round(midpoints[i][1]/nLicks)

# Stores the durations of the notes from lick, with every duration in its corresponding division
durations = [[] for i in range(nDiv)]

# Transforms the array of divisions in a string-like array
#	- See cipher_notation() function definition in "util.py"
for i in range(len(notes)):
	for j in range(len(notes[i])):
		durations[i].append(util.get_duration(notes[i][j]))
		notes[i][j] = util.cipher_notation(notes[i][j])

# Domains are the complete set of the possible values of a variable in current division
#	- It is based on notes that appeared in the input licks
# Let N, D and T random variables that represents, respectively, notes, durations and time modifications

# Stores the domain of N for each division
note_domain = [[] for i in range(nDiv)]

# Stores the domain of D for each division
duration_domain = [[] for i in range(nDiv)]

# Stores the domain of T for each division
time_change_domain = [[] for i in range(nDiv)]

# Stores the domain of fret-string pairs for each division
#	- A domain defined by fret-string pairs
#	- Etree based
fret_string_domain = [[] for i in range(nDiv)]

for i in range(nDiv):
	note_domain[i] = util.create_domain(notes[i])
	duration_domain[i] = util.create_domain(durations[i])
	time_change_domain[i] = util.create_tc_domain(time_changes[i])
	fret_string_domain[i] = util.fret_string_domain(notes_by_lick[i])
	util.create_xml_file_from_domain(fret_string_domain[i], dom_path + "fs_domain_%s.xml" % i)

# Declaring probability matrices for notes and durations
prob_matrix_note = [[] for i in range(nDiv)]
prob_matrix_duration = [[] for i in range(nDiv)]

# Fills the probability matrices based on input licks
for i in range(nDiv):
	prob_matrix_note[i] = prob_matrix.set_prob_matrix(notes_by_lick, note_domain[i], i, util.cipher_notation)
	prob_matrix_duration[i] = prob_matrix.set_prob_matrix(notes_by_lick, duration_domain[i], i, util.get_duration)

# Applying preprocessing
#	- See the mult_coef_int() function definition in "prob_matrix.py"
#for i in range(nDiv):
#	prob_matrix.mult_coef_int(prob_matrix_note[i], 5)
#	prob_matrix.mult_coef_int(prob_matrix_duration[i], 5)

#prob_matrix_note[i], prob_matrix_duration[i] = deepcopy(prob_matrix.k_iter(prob_matrix_note[i], prob_matrix_duration[i], note_domain[i], duration_domain[i], 100))
#prob_matrix.mult_coef_float(prob_matrix_note[i], note_domain[i], 10)
#prob_matrix.mult_coef_float(prob_matrix_duration[i], duration_domain[i], 10)
	
# Normalizing the probability matrices
for i in range(nDiv):
	util.normalize(prob_matrix_note[i])
	util.normalize(prob_matrix_duration[i])

# Stores the notes of the generated lick
final_lick = []

# If the current transition is the first
first_lick_trans = 1

# Assists in choosing the transition between different divisions
prev_div_note = None
prev_div_durat = None

# Stores the starting note/duration of the transition
start_note = None
start_durat = None

# A map of positions (fret/string) of all notes used in the input licks
fs_domain = None

max_div_time = mes_size/nDiv
q = 0
while q < nDiv:

	# At the beginning of each division	
	attempts = 0
	div_time = 0
	first_trans_div = 1
	sucess = 1
	notes_added = 0
	
	# In the generation of each note/duration	
	while div_time < max_div_time:
		if attempts == 100:
			sucess = 0
			for i in range(notes_added):
				final_lick.pop()
			if q == 0:
				first_lick_trans = 1
			if q > 0 and final_lick[-1].find('tie') is not None:
				final_lick[-1].remove(final_lick[-1].find('tie'))
				final_lick[-1].find('notations').remove(final_lick[-1].find('notations').find('tied'))
			break

		# Predicting the first note/duration of the current division, after passing the previous division
		#	- If the note/duration from the previous division do not belong to the domain of the current division, the element with the highest value in the matrix main diagonal is chosen
		if ( q > 0 ) and ( first_trans_div == 1 ):
			start_note, start_durat = util.belongs2domain(prev_div_note, prev_div_durat, note_domain[q], duration_domain[q], prob_matrix_note[q], prob_matrix_duration[q])
			first_trans_div = 0

		# Predicting the first note/duration that will be part of the lick
		if first_lick_trans == 1:
			method = random.randint(0, 2)
			next_note, next_durat = prob_matrix.first_lick_note(prob_matrix_note[q], prob_matrix_duration[q], note_domain[q], duration_domain[q], notes_by_lick[q], method)
			next_durat_aux = next_durat

			# Case the note found is a tied note, which do not make sense
			#	- Keep looking until find something different
			while note_domain[q][next_note] == 't':
				next_note, next_durat = prob_matrix.first_lick_note(prob_matrix_note[q], prob_matrix_duration[q], note_domain[q], duration_domain[q], notes_by_lick[q], 2)
			next_durat = next_durat_aux

		# If the note to be generated is neither the first of the lick nor the first of the current division
		else:
			next_note = prob_matrix.generate(prob_matrix_note[q], note_domain[q], start_note, 0)
			next_durat = prob_matrix.generate(prob_matrix_duration[q], duration_domain[q], start_durat, 1)

		# Retrieving the generated note in cipher notation format
		s = note_domain[q][next_note]
		s = list(s)

		# If the length of "s_note" is greater than two, it means is a sharp note
		if len(s) > 1:
			base_note = deepcopy(util.create_base_note())
			base_note.find('pitch').find('step').text = s[0]
			etree.SubElement(base_note.find('pitch'), 'alter')
			base_note.find('pitch').find('alter').text = '1'
			fs_domain = util.create_root(dom_path + "fs_domain_%s.xml" % q)
		# If "s_note" is a rest
		elif s[0] == 'p':
			base_note = deepcopy(util.create_rest())
		# If "s_note" is a tied note
		elif s[0] == 't':
			base_note = deepcopy(final_lick[-1])
			etree.SubElement(final_lick[-1], "tie", type="start")
			etree.SubElement(final_lick[-1].find('notations'), "tied", type="start")
			etree.SubElement(base_note, "tie", type="stop")
			etree.SubElement(base_note.find('notations'), "tied", type="stop")
		# If "s_note" is a natural note
		else:
			base_note = deepcopy(util.create_base_note())
			base_note.find('pitch').find('step').text = s[0]
			fs_domain = util.create_root(dom_path + "fs_domain_%s.xml" % q)

		# Determining the position of the generated note
		#	- The position of the generated note is determined by choosing it from a map of positions of all notes used in the input licks, which is defined by "fs_domain"
		#	- The subsequent generated notes should be playable in terms of distance (fret and string)
		#		- To do this, they will be positioned close to the midpoint, also considering the distance by string from the last note added
		'''if base_note.find('rest') is None and base_note.find('tie') is None:
			lowest = math.inf
			found = 0
			string_limit = 2

			# when the current note to be added is the first note of the lick or, if is not and the last note added is a rest
			#	- just add
			if ( first_lick_trans == 1 ) or ( first_lick_trans == 0 and final_lick[-1].find('rest') is not None ):
				for note in list(fs_domain.find('part').find('measure').iter('note')):
					if ( base_note.find('pitch').find('step').text == note.find('pitch').find('step').text ) and ( ( base_note.find('pitch').find('alter') is not None and note.find('pitch').find('alter') is not None ) or ( base_note.find('pitch').find('alter') is None and note.find('pitch').find('alter') is None ) ):
						if util.note2point_dist(note, midpoints[q]) < lowest:
							lowest = util.note2point_dist(note, midpoints[q])
							base_note.find('notations').find('technical').find('string').text = note.find('notations').find('technical').find('string').text
							base_note.find('notations').find('technical').find('fret').text = note.find('notations').find('technical').find('fret').text
							base_note.find('pitch').find('octave').text = note.find('pitch').find('octave').text
							found = 1

			# when the current note to be added is not the first note of the lick
			#	- the vertical distance (string) from the previous note should be considered
			#	- the previous note cannot be a rest
			elif first_lick_trans == 0 and final_lick[-1].find('rest') is None:
				while string_limit < 4:
					lowest = math.inf
					for note in list(fs_domain.find('part').find('measure').iter('note')):
						if ( base_note.find('pitch').find('step').text == note.find('pitch').find('step').text ) and ( ( base_note.find('pitch').find('alter') is not None and note.find('pitch').find('alter') is not None ) or ( base_note.find('pitch').find('alter') is None and note.find('pitch').find('alter') is None ) ):
							if util.note2point_dist(note, midpoints[q]) < lowest and util.string_difference(note, final_lick[-1]) < string_limit:
								lowest = util.note2point_dist(note, midpoints[q])
								base_note.find('notations').find('technical').find('string').text = note.find('notations').find('technical').find('string').text
								base_note.find('notations').find('technical').find('fret').text = note.find('notations').find('technical').find('fret').text
								base_note.find('pitch').find('octave').text = note.find('pitch').find('octave').text
								found = 1
					if found == 0:
						string_limit += 1
					else:
						break'''

		# This is another method to determine the position of the generated note
		#	- Unlike the previous method, it considers a constant distance bound (3.5) between the last note added and the current note generated
		found = 0
		string_limit = 1
		if base_note.find('rest') is None and base_note.find('tie') is None:
			while string_limit < 4:
				for note in list(fs_domain.find('part').find('measure').iter('note')):
					if ( base_note.find('pitch').find('step').text == note.find('pitch').find('step').text ) and ( ( base_note.find('pitch').find('alter') is not None and note.find('pitch').find('alter') is not None ) or ( base_note.find('pitch').find('alter') is None and note.find('pitch').find('alter') is None ) ):
						if util.note2point_dist(note, midpoints[q]) <= 3.5:
							if ( first_lick_trans == 0 ) and ( final_lick[-1].find('rest') is None ) and ( util.string_difference(note, final_lick[-1]) > string_limit ):
								continue
							base_note.find('notations').find('technical').find('string').text = note.find('notations').find('technical').find('string').text
							base_note.find('notations').find('technical').find('fret').text = note.find('notations').find('technical').find('fret').text
							base_note.find('pitch').find('octave').text = note.find('pitch').find('octave').text
							found = 1
							break
				if found == 0:
					string_limit += 1
				else:
					break

		# It is hoped that the program does not enter here
		if base_note.find('rest') is None and base_note.find('tie') is None:	
			if found == 0:
				print ("Não achou")

		# Determining a possible time change for the note
		t = duration_domain[q][next_durat]

		# Determining a time change for the current duration
		#	- This time change is based on the ones that appeared in the input licks, matching the same duration (t)
		for tupl in time_change_domain[q]:
			if tupl[0] == t:
				if tupl[1] == 1: # triplet
					etree.SubElement(base_note, 'time-modification')
					etree.SubElement(base_note.find('time-modification'), 'actual-notes')
					base_note.find('time-modification').find('actual-notes').text = '3'
					etree.SubElement(base_note.find('time-modification'), 'normal-notes')
					base_note.find('time-modification').find('normal-notes').text = '2'
			
				if tupl[2] == 1: # doted
					etree.SubElement(base_note, 'dot')

				base_note.find('type').text = tupl[3]

		# If the duration of the last note found exceed the size limit of the division (which is 64/nDiv), new attempts are made in order to find the exact missing time
		if (div_time + t) > max_div_time:
			attempts += 1
			continue

		# If the note is sucessfully added
		div_time += t
		final_lick.append(deepcopy(base_note))
		notes_added += 1
		start_note = next_note
		start_durat = next_durat
		if first_lick_trans == 1:
			first_lick_trans = 0
	
	# If the current division is successfully built
	if sucess == 1:	
		prev_div_note = note_domain[q][start_note]
		prev_div_durat = duration_domain[q][start_durat]
		q += 1

print ("\033[1;32mGeneration by Markov Chains complete\033[0;0m\n")

# Writing measure in a MusicXML file
rootB = util.create_root("xmls/base.xml") 

for note in final_lick:
	rootB.find('part').find('measure').append(deepcopy(note))

rootB = etree.tostring(rootB)

index = 0
for i in os.listdir("turnaround_licks/result/1"):
	index += 1

resultName = "turnaround_licks/result/1/%s.xml" % index
with open(resultName, "wb") as output:
	output.write(rootB)



