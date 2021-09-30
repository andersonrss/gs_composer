
# -*- coding: utf-8 -*-
from lxml import etree
from copy import deepcopy
import random
import util



# Applies vibrato technique when:
#	- the current note has a duration > 16
#	- the current note is a tied note
def vibrato(measure):

	for i in range(len(measure)):
		if i == (len(measure)-1):
			if measure[i].find('rest') is None and measure[i].find('chord') is None:
				if measure[i].find('tie') is not None:
					if measure[i].find('tie').get('type') == "start":
						etree.SubElement(measure[i].find('notations').find('technical'), "other-technical")
						measure[i].find('notations').find('technical').find('other-technical').text = "vibrato"
				elif measure[i].find('tie') is None and util.get_duration(measure[i]) >= 16:
					etree.SubElement(measure[i].find('notations').find('technical'), "other-technical")
					measure[i].find('notations').find('technical').find('other-technical').text = "vibrato"
					
		elif measure[i].find('rest') is None and measure[i].find('chord') is None and measure[i+1].find('chord') is None:
			if measure[i].find('tie') is not None:
				if measure[i].find('tie').get('type') == "start":
					etree.SubElement(measure[i].find('notations').find('technical'), "other-technical")
					measure[i].find('notations').find('technical').find('other-technical').text = "vibrato"
			elif measure[i].find('tie') is None and util.get_duration(measure[i]) >= 16:
				etree.SubElement(measure[i].find('notations').find('technical'), "other-technical")
				measure[i].find('notations').find('technical').find('other-technical').text = "vibrato"


# Applies hamer on and pull off techniques based on probability
#	- Some conditions must be met, like no bend, no rest, same string...
def hammer_pull(measure, prob):

	for i in range(len(measure)-1):
		dice_hp = round(random.random(), 2)
		if dice_hp <= prob:
			if measure[i].find('chord') is None and measure[i+1].find('chord') is None: # No rest
				if measure[i].find('rest') is None and measure[i+1].find('rest') is None: # No double stop
					if measure[i].find('notations').find('technical').find('bend') is None and measure[i+1].find('notations').find('technical').find('bend') is None: # No bend
						if measure[i].find('notations').find('slide') is None and measure[i+1].find('notations').find('slide') is None: # No slide
							if measure[i].find('tie') is None and measure[i+1].find('tie') is None: # No tied
								if measure[i].find('notations').find('technical').find('string').text == measure[i+1].find('notations').find('technical').find('string').text: # Same string
									casa_nota_a = int(measure[i].find('notations').find('technical').find('fret').text)
									casa_nota_b = int(measure[i+1].find('notations').find('technical').find('fret').text)
									dif = casa_nota_a - casa_nota_b
									if dif < 0:
										etree.SubElement(measure[i].find('notations').find('technical'), "hammer-on", type="start")
										measure[i].find('notations').find('technical').find('hammer-on').text = 'H'
										etree.SubElement(measure[i+1].find('notations').find('technical'), "hammer-on", type="stop")
									elif dif > 0:
										etree.SubElement(measure[i].find('notations').find('technical'), "pull-off", type="start")
										measure[i].find('notations').find('technical').find('pull-off').text = 'P'
										etree.SubElement(measure[i+1].find('notations').find('technical'), "pull-off", type="stop")



# Transforms the current note into blue notes, based on probability
#	- It does not happen with the first and the last note from measure
#	- It does happen only between D# and F, F and G, and G and F
#	- Choose the closest blue note from a list passed as input
def blue_note(measure, prob):

	bn_arr = []
	blue_note = util.cria_raiz("../xmls/minor_blue_note.xml")
	for bn in list(blue_note.find('part').find('measure').iter('note')):
		bn_arr.append(deepcopy(bn))
	
	for i in range(len(measure)):
		if i == 0 or i == (len(measure)-1):
			continue
		if measure[i-1].find('rest') is None and measure[i].find('rest') is None and measure[i+1].find('rest') is None: # No rest
			if ( ( measure[i-1].find('pitch').find('step').text == 'D' and measure[i-1].find('pitch').find('alter') is not None ) and ( measure[i+1].find('pitch').find('step').text == 'F' and measure[i+1].find('pitch').find('alter') is None ) ) or ( ( measure[i-1].find('pitch').find('step').text == 'F' and measure[i-1].find('pitch').find('alter') is None ) and ( measure[i+1].find('pitch').find('step').text == 'G' and measure[i+1].find('pitch').find('alter') is None ) ) or ( ( measure[i-1].find('pitch').find('step').text == 'G' and measure[i-1].find('pitch').find('alter') is None ) and ( measure[i+1].find('pitch').find('step').text == 'F' and measure[i+1].find('pitch').find('alter') is None ) ): #D# -> F# -> F | F -> F# -> G | G -> F# -> F
				if measure[i-1].find('chord') is None and measure[i].find('chord') is None and measure[i+1].find('chord') is None: # No double stop
					if measure[i-1].find('notations').find('slide') is None and measure[i].find('notations').find('slide') is None and measure[i+1].find('notations').find('slide') is None: # No slide
						if measure[i-1].find('tie') is None and measure[i].find('tie') is None and measure[i+1].find('tie') is None: # No tied
							if util.get_duration(measure[i]) < 16:
								bn_prob = round(random.random(), 2)
								if bn_prob <= prob:
									short_dist = 100
									short_id = 0
									for j in range(len(bn_arr)):
										if util.note2note_dist(measure[i], bn_arr[j]) <= short_dist:
											short_dist = util.note2note_dist(measure[i], bn_arr[j])
											short_id = j
									measure[i].find('notations').find('technical').find('string').text = bn_arr[short_id].find('notations').find('technical').find('string').text
									measure[i].find('notations').find('technical').find('fret').text = bn_arr[short_id].find('notations').find('technical').find('fret').text
									measure[i].find('pitch').find('step').text = 'F'
									if measure[i].find('pitch').find('alter') is None:
										etree.SubElement(measure[i].find('pitch'), "alter")
										measure[i].find('pitch').find('alter').text = '1'
									else:
										measure[i].find('pitch').find('alter').text = '1'
									if measure[i].find('notations').find('technical').find('bend') is not None:
										measure[i].find('notations').find('technical').find('bend').find('bend-alter').text = '0.5'


# 
def bend_blue_note(measure, prob):
	
	if measure.get('number') == '2' or measure.get('number') == '3' or measure.get('number') == '4' or measure.get('number') == '5' or measure.get('number') == '8' or measure.get('number') == '9':
		for i in range(len(measure)):
			if i == 0 or i == (len(measure)-1):
				continue
			if measure[i-1].find('rest') is None and measure[i].find('rest') is None and measure[i+1].find('rest') is None: #sem pausas
				if measure[i].find('pitch').find('step').text == 'D' and measure[i].find('pitch').find('alter') is not None: # D#
					if measure[i-1].find('chord') is None and measure[i].find('chord') is None and measure[i+1].find('chord') is None: #sem acordes
						if measure[i-1].find('notations').find('slide') is None and measure[i].find('notations').find('slide') is None and measure[i+1].find('notations').find('slide') is None: #slides
							if measure[i-1].find('tie') is None and measure[i].find('tie') is None and measure[i+1].find('tie') is None: #sem notas ligadas
								dice_bend = round(random.random(), 2)
								if dice_bend <= prob:
									if measure[i].find('notations').find('technical').find('bend') is not None and util.get_duration(measure[i]) > 5.2:
										measure[i].find('notations').find('technical').find('bend').find('bend-alter').text = '0.5'
									elif util.get_duration(measure[i]) > 5.2:
										etree.SubElement(measure[i].find('notations').find('technical'), "bend")
										etree.SubElement(measure[i].find('notations').find('technical').find('bend'), "bend-alter")
										measure[i].find('notations').find('technical').find('bend').find('bend-alter').text = '0.5'
										
								
	if measure.get('number') == '10':
		for i in range(len(measure)):
			if i == 0 or i == (len(measure)-1):
				continue
			if measure[i-1].find('rest') is None and measure[i].find('rest') is None and measure[i+1].find('rest') is None: #sem pausas
				if measure[i].find('pitch').find('step').text == 'A' and measure[i].find('pitch').find('alter') is not None: # A#
					if measure[i-1].find('chord') is None and measure[i].find('chord') is None and measure[i+1].find('chord') is None: #sem acordes
						if measure[i-1].find('notations').find('slide') is None and measure[i].find('notations').find('slide') is None and measure[i+1].find('notations').find('slide') is None: #slides
							if measure[i-1].find('tie') is None and measure[i].find('tie') is None and measure[i+1].find('tie') is None: #sem notas ligadas
								dice_bend = round(random.random(), 2)
								if dice_bend <= prob:
									if measure[i].find('notations').find('technical').find('bend') is not None:
										measure[i].find('notations').find('technical').find('bend').find('bend-alter').text = '0.5'
									else:
										etree.SubElement(measure[i].find('notations').find('technical'), "bend")
										etree.SubElement(measure[i].find('notations').find('technical').find('bend'), "bend-alter")
										measure[i].find('notations').find('technical').find('bend').find('bend-alter').text = '0.5'
		
		
