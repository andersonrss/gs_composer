
# -*- coding: utf8 -*-
from lxml import etree
from copy import deepcopy
import random, os, sys
import util

# Turnaround measures directories 
a_dir = "turnaround_licks/result/1/"
b_dir = "turnaround_licks/result/2/"

# Output directory
out_dir = "gs_optimizer/lick_database/"

# Counting files in each directory
nf1 = 0
nf2 = 0

for i in os.listdir(a_dir):
	nf1 += 1
	
for i in os.listdir(b_dir):
	nf2 += 1

if nf1 == 0 or nf2 == 0:
	print("\033[93mmerge_turnaround.py\033[0m: \033[1;31mThere are no XML files in directories. Please, try to generate more turnaround licks\033[0m") 
	print("Aborting...\n")
	sys.exit(1)

# Randomly, choose one measure in each directory
rt1 = random.randint(0, nf1-1)
rt2 = random.randint(0, nf2-1)

m1 = util.create_root(a_dir + "%s.xml" % rt1)
m2 = util.create_root(b_dir + "%s.xml" % rt2)

# Appending notes to an array
ta_lick = [[] for i in range(2)]

for note in list(m1.find('part').find('measure').iter('note')):
	ta_lick[0].append(deepcopy(note))

for note in list(m2.find('part').find('measure').iter('note')):
	ta_lick[1].append(deepcopy(note))

nota = deepcopy(ta_lick[1][-1])
b = util.create_root("xmls/base.xml")
for m in list(b.find('part').iter('measure')):
	m.append(nota)
b = etree.tostring(b)

with open("teste.xml", "wb") as t:
	t.write(b)


# Extending the last note with a tied note
copy = deepcopy(ta_lick[1][-1])
copy.find('type').text = "half"
etree.SubElement(copy, "dot")
etree.SubElement(copy, "tie", type="stop")
etree.SubElement(copy.find('notations'), "tied", type="stop")

etree.SubElement(ta_lick[1][-1], "tie", type="start")
etree.SubElement(ta_lick[1][-1].find('notations'), "tied", type="start")

ta_lick[1].append(deepcopy(copy))

# Writing the final lick in a XML file
base = util.create_root("xmls/base.xml")
etree.SubElement(base.find('part'), "measure", number="2")

i = 0
for measure in list(base.find('part').iter('measure')):
	for note in ta_lick[i]:
		measure.append(deepcopy(note))
	i += 1

index = 0
for i in os.listdir(out_dir):
	index += 1

mergeName = out_dir + "%s.xml" % index
base = etree.tostring(base)
with open(mergeName, "wb") as merge:
	merge.write(base)



