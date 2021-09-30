
# -*- coding: utf-8 -*-
from SublicksGeneratorClass import *
import pre_processing

from lxml import etree
from copy import deepcopy
import sys, random, os, subprocess, time


random.seed()
base_path = "xmls/base.xml"


''' ----- SUBLICKS GENERATION PHASE ----- '''


# DEFAULT SUBLICKS ---------------------------------------------


inpt = open("xmls/default_notes.xml", "r")
tree = etree.parse(inpt)
root = tree.getroot()

default = Generator(root, "default", base_path)
default.set_durations('quarter', 'eighth')
default.generate_blueNote_1()

default.set_durations('eighth')
default.generate_blueNote_triplet_1()

default.set_durations('quarter', 'eighth')
default.generate_rest_1()

default.set_durations('quarter', 'eighth')
default.generate_rest_triplet_1()

default.set_durations('quarter', 'eighth', '16th')
default.generate_normalNote_1()

default.set_durations('quarter', 'eighth')
default.generate_bend_1()

default.set_durations('eighth', '16th')
default.generate_slide_forward_2()

default.set_durations('eighth')
default.generate_triplet_1()

default.set_durations('quarter')
default.generate_doubleStop_2()

default.set_durations('quarter', 'eighth')
default.generate_triplet_bend_1()


# REPETITION SUBLICKS ---------------------------------------------


inpt = open("xmls/repetition_notes.xml", "r")
tree = etree.parse(inpt)
root = tree.getroot()

repetition = Generator(root, "repetition", base_path)

repetition.set_durations('eighth', '16th')
repetition.generate_normalNote_1()

repetition.set_durations('quarter', 'eighth')
repetition.generate_bend_1()

repetition.set_durations('eighth')
repetition.generate_triplet_1()


# TURNAROUND SUBLICKS ---------------------------------------------


inpt = open("xmls/turnaround_notes.xml", "r")
tree = etree.parse(inpt)
root = tree.getroot()

turnaround = Generator(root, "turnaround", base_path)

turnaround.set_durations('quarter', 'eighth', '16th')
turnaround.generate_normalNote_1()

turnaround.set_durations('quarter', 'eighth')
turnaround.generate_rest_1()

turnaround.set_durations('quarter', 'eighth')
turnaround.generate_rest_triplet_1()

turnaround.set_durations('eighth')
turnaround.generate_triplet_bend_1()

turnaround.set_durations('eighth', '16th')
turnaround.generate_triplet_1()



# 		*****************************************
#		*				Library					*
#		*****************************************

# Here you can find routines which generate different types of sublicks, according to techniques
#	- For example, the function 'generate_bend_dotted_1' generates one-note sublick that have a doted note with the bend technique


''' ----- One note ----- '''


#generate_rest_1()

#generate_rest_triplet_1()

#generate_normalNote_1()

#generate_bend_1()

#generate_triplet_1()

#generate_triplet_bend_1()

#generate_dotted_1()

#generate_bend_dotted_1()

#generate_bend_dotted_triplet_1()

#generate_dotted_triplet_1()


''' ----- Two notes ----- '''


#generate_hammerOn_2()

#generate_hammerOn_triplet_2()

#generate_hammerOn_var_2()

#generate_pullOff_2()

#generate_pullOff_triplet_2()

#generate_pullOff_var_2()

#generate_slide_backward_2()

#generate_slide_forward_2()

#generate_slide_forward_var_2()

#generate_slide_backward_var_2()

#generate_tied_var_2()

#generate_slide_forward_triplet_2()

#generate_slide_backward_triplet_2()

#generate_doubleStop_2()


''' ----- PRE-PROCESSING PHASE ----- '''


pre_processing.pre_processing(default)
pre_processing.pre_processing(repetition)
pre_processing.pre_processing(turnaround)



