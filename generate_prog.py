
# -*- coding: utf-8 -*-

import subprocess


solver_path = "gs_optimizer/solver/executable"

normal_rate = 0.7
rest_rate = 0.7
repetition_rate = 0.7
turnaround_rate = 0.7
bn_rate = 0.7

subprocess.call([solver_path, 
		str(normal_rate), 
		str(rest_rate), 
		str(repetition_rate), 
		str(turnaround_rate), 
		str(bn_rate)])

subprocess.call(["python3", "gs_optimizer/concatenator.py"])
