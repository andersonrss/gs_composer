
# -*- coding: utf-8 -*-
import subprocess

# Repetition licks

subprocess.call(["rm", "-rf", "repetition_licks/result"])
subprocess.call(["mkdir", "repetition_licks/result"])

# Turnaround licks

subprocess.call(["rm", "-rf", "turnaround_licks/result/1"])
subprocess.call(["rm", "-rf", "turnaround_licks/result/2"])
subprocess.call(["mkdir", "turnaround_licks/result/1"])
subprocess.call(["mkdir", "turnaround_licks/result/2"])
