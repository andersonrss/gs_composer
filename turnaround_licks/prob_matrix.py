
# -*- coding: utf-8 -*-
from lxml import etree
from copy import deepcopy
import random, math, sys
import util, prob_matrix


# Create the probability matrix according to the notes that appear in the input licks
def set_prob_matrix(notes_by_lick, domain, d, func):
	
	prob_matrix = [[0 for i in range(len(domain))] for j in range(len(domain))]
	note_a = None
	note_b = None

	for m in range(len(notes_by_lick[d])):
		#	- This first part take care about counting transitions between two notes, in the way that the first note belongs to the dth division and the second note belongs to the dth + 1 division
		#	- When the first note do not appear in the domain of the dth + 1 division, there is no transition counting

		# If the division is the first and the current submeasure has one note only
		#	- Since transition happens from n-1 to n, this note will not be processed
		if len(notes_by_lick[d][m]) == 1 and d == 0:
			continue
		# If the division is not the first and the current submeasure has one note only
		elif len(notes_by_lick[d][m]) == 1 and d != 0:
			# If the previous submeasure is empty
			#	- There is no transition
			if len(notes_by_lick[d-1][m]) == 0:
				continue

			note_a = func(notes_by_lick[d-1][m][-1])
			note_b = func(notes_by_lick[d][m][0])

			# This kind of transition is possible only if note_a is among the possible values in the current domain
			found = 0
			for string in domain:
				if note_a == string:
					found = 1
					break
			if found == 1:
				# In positive case, the probability matrix is updated
				prob_matrix[domain.index(note_a)][domain.index(note_b)] += 1
		else:
			#	- At this part, the algorithm take care about the other common transition cases
			
			for n in range(len(notes_by_lick[d][m])):
				# If at the last note, there is no transition
				if n == (len(notes_by_lick[d][m])-1):
					continue

				note_a = func(notes_by_lick[d][m][n])
				note_b = func(notes_by_lick[d][m][n+1])

				# Probability matrix is updated
				prob_matrix[domain.index(note_a)][domain.index(note_b)] += 1

	return prob_matrix


# Generates next note/duration
def generate(prob_matrix, domain, previous, row_or_col):
	
	var = ind = acc = 0
	next = random.random()
	
	# Detectar linhas com probabilidade 0
	for i in range(len(prob_matrix[previous])):
		acc += prob_matrix[previous][i]

	# If a line/column has only zeros, the start note will be the one which value of line/column is the highest
	if acc == 0:
		for i in range(len(prob_matrix)):
			for j in range(len(prob_matrix[i])):
				if prob_matrix[i][j] > acc:
					acc = prob_matrix[i][j]
					if row_or_col == 0:
						ind = i
					else:
						ind = j
		return ind
	
	for j in range(len(prob_matrix[previous])):
		if ( var <= next ) and ( next < (var + prob_matrix[previous][j]) ):
			return j

		else:
			var += prob_matrix[previous][j]


# Each value of the probability matrix M is multiplied by a integer coefficient c, which varies according to the value of M[i][j]
#	- The higher is M[i][j], higher is c
#	- M[i][j] = M[i][j]*c
#	- This kind of operation highlights the most frequent transitions found in the input licks 

def mult_coef_int(prob_matrix, n_steps):
	
	# Defining multipliers
	multipliers = []
	for i in range(n_steps):
		multipliers.append(i+1)
	
	# Getting the highest value of the prob matrix
	highest = 0
	for i in range(len(prob_matrix)):
		for j in range(len(prob_matrix[i])):
			if prob_matrix[i][j] > highest:
				highest = prob_matrix[i][j]
	
	# Defining the step value
	step = highest/n_steps
	if step.is_integer() == False:
		step = int(math.modf(step)[1])

	id_step = 0
	for i in range(len(prob_matrix)):
		for j in range(len(prob_matrix[i])):
			aux = 0
			for k in multipliers:
				if aux + step*2 >= highest:
					step = highest - aux
				if aux <= prob_matrix[i][j] and prob_matrix[i][j] < (aux + step):
					id_step = k
					break
				aux = aux + step
			prob_matrix[i][j] = prob_matrix[i][j] * k


# Tt does the same thing as mult_coef_int, but using real numbers as coefficients, however, less aggressive
def mult_coef_float(prob_matrix, n_steps):
	
	multipliers = []
	for i in range(n_steps):
		multipliers.append(i+1)
	
	highest = 0
	for i in range(len(prob_matrix)):
		for j in range(len(prob_matrix[i])):
			if prob_matrix[i][j] > highest:
				highest = prob_matrix[i][j]
	
	step = highest/n_steps
	
	id_step = 0
	for i in range(len(prob_matrix)):
		for j in range(len(prob_matrix[i])):
			aux = 0
			for k in multipliers:
				if aux <= prob_matrix[i][j] and prob_matrix[i][j] < (aux + step):
					id_step = k
					break
				aux = aux + step
			prob_matrix[i][j] = prob_matrix[i][j] * k


# Generates the lick's first note/duration
#	- The "method" variable is a flag that tells the function which generation method should be used (0, 1 or 2)
#	- Method 0: the resulting note/duration is the row that has the column with the highest value
#	- Method 1: the resulting note/duration is chosen randomly
#	- Method 2: the resulting note/duration is chosen through roulette method
def first_lick_note(prob_matrix_note, prob_matrix_duration, note_domain, duration_domain, notes_by_lick, method):
	
	start_note = 0
	start_durat = 0

	# The resulting note/duration is the row that has the column with the highest
	if method == 0:
		highest = 0
		for i in range(len(prob_matrix_note)):
			for j in range(len(prob_matrix_note[i])):	
				if prob_matrix_note[i][j] > highest:
					highest = prob_matrix_note[i][j]
					start_note = i

		highest = 0
		for i in range(len(prob_matrix_duration)):
			for j in range(len(prob_matrix_duration[i])):
				if prob_matrix_duration[i][j] > highest:
					highest = prob_matrix_duration[i][j]
					start_durat = i
		
		# Returning both note/duration 
		return start_note, start_durat

	# Note/duration chosen randomly
	elif method == 1:
		start_note = random.randint(0, len(note_domain)-1)
		start_durat = random.randint(0, len(duration_domain)-1)
		
		# Returning both note/duration 
		return start_note, start_durat

	elif method == 2:
		first_meas_notes = []
		first_meas_durat = []

		# Taking the first note/duration of each measure from current division
		for i in range(len(notes_by_lick)):
			if len(notes_by_lick[i]) == 0:
				continue
			first_meas_notes.append(util.cipher_notation(notes_by_lick[i][0]))
			first_meas_durat.append(util.get_duration(notes_by_lick[i][0]))

		# Creating domains, which are defined by the possible values for note and duration
		start_note_dom = util.create_domain(first_meas_notes)
		start_durat_dom = util.create_domain(first_meas_durat)

		# Couting the number of times each note/duration appears
		start_notes_count = [0 for i in range(len(start_note_dom))]
		start_durat_count = [0 for i in range(len(start_durat_dom))]

		for i in range(len(notes_by_lick)):
			if len(notes_by_lick[i]) == 0:
				continue
			if notes_by_lick[i][0].find('rest') is not None:
				start_notes_count[start_note_dom.index('p')] += 1
			else:
				start_notes_count[start_note_dom.index(util.cipher_notation(notes_by_lick[i][0]))] += 1
			start_durat_count[start_durat_dom.index(util.get_duration(notes_by_lick[i][0]))] += 1

		# Normalizing
		total = 0
		for i in range(len(start_notes_count)):
			total += start_notes_count[i]

		for i in range(len(start_notes_count)):
			start_notes_count[i] /= total

		total = 0
		for i in range(len(start_durat_count)):
			total += start_durat_count[i]

		for i in range(len(start_durat_count)):
			start_durat_count[i] /= total

		# "Spinning the roulette"
		f_note = random.random()
		f_duration = random.random()

		aux = 0
		for i in range(len(start_notes_count)):
			if ( aux <= f_note ) and ( f_note < (aux + start_notes_count[i]) ):
				start_note = i
			else:
				aux += start_notes_count[i]

		aux = 0
		for i in range(len(start_durat_count)):
			if ( aux <= f_duration ) and ( f_duration < (aux + start_durat_count[i]) ):
				start_durat = i
			else:
				aux += start_durat_count[i]
	
	# Returning both note/duration 
	return note_domain.index(start_note_dom[start_note]), duration_domain.index(start_durat_dom[start_durat])


# Generate k notes/duration samples, applying the results to the probability matrices
def k_iter(prob_matrix_note, prob_matrix_duration, note_domain, duration_domain, k):
	
	prob_matrix_note_copy = deepcopy(prob_matrix_note)
	prob_matrix_duration_copy = deepcopy(prob_matrix_duration)
	
	start_note = None
	start_durat = None
	first_iter = 1
	max_iter = 0
	while max_iter < k:
		util.normalize(prob_matrix_note)
		util.normalize(prob_matrix_duration)
		
		if first_iter == 1:
			start_note = random.randint(0, len(note_domain)-1)
			start_durat = random.randint(0, len(duration_domain)-1)
			first_iter = 0
		
		next_note = prob_matrix.generate(prob_matrix_note_copy, note_domain, start_note, 0)
		next_durat = prob_matrix.generate(prob_matrix_duration_copy, duration_domain, start_durat, 1)
		
		prob_matrix_note_copy[start_note][next_note] = prob_matrix_note_copy[start_note][next_note] + 1
		prob_matrix_duration_copy[start_durat][next_durat] = prob_matrix_duration_copy[start_durat][next_durat] + 1
		
		prob_matrix_note = deepcopy(prob_matrix_note_copy)
		prob_matrix_duration = deepcopy(prob_matrix_duration_copy)
		
		start_note = next_note
		start_durat = next_durat
		max_iter += 1
	
	return prob_matrix_note, prob_matrix_duration


