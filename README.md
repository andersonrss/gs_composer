# Generating guitar solos by ingeter programming

### A brief description

The system described here uses integer programming models in order to generate guitar solos, more precisely a 12-Bar Blues progression. The 12-Bar Blues progression is a sequence of 12 measures following a harmony based on the I, IV and V chors of a key.

A solo is generated lick by lick. Each lick is the size of a measure, and each measure is generated note by note. This problem can be viewed as a variant of the traveling salesman problem (TSP), but instead of having cities, we have musical notes. Rules of penalty and reward are defined in order to determine a cost matrix, which is used to store the transition costs between each musical note of a given input. These transition costs will help the model find the optimal sequence of sublicks.

The output produced by de system is a MusicXML file that can be reproduced by softwares like [Guitar Pro](https://www.guitar-pro.com/).

### Requirements

To run the code, you will need the following requirements:

1. [Python 3.6+](https://www.python.org/downloads/)
2. [IBM CPLEX Optimizer](https://www.ibm.com/br-pt/analytics/cplex-optimizer)

### How to run

The first step to get started is to generate the necessary sublicks. To do that, in **gs_composer/** directory, run the following command line:

'''ruby
python3 generate_sublicks.py
'''

