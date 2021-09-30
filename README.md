# Generating guitar solos by ingeter programming

### A brief description

The system described here uses integer programming models in order to generate guitar solos, more precisely a 12-Bar Blues progression. The 12-Bar Blues progression is a sequence of 12 measures following a harmony based on the I, IV and V chors of a key.

A solo is generated lick by lick. Each lick is the size of a measure, and each measure is generated note by note. This problem can be viewed as a variant of the traveling salesman problem (TSP), but instead of having cities, we have musical notes. Rules of penalty and reward are defined in order to determine a cost matrix, which is used to store the transition costs between each musical note of a given input. These transition costs will help the model find the optimal sequence of sublicks.

The output produced by de system is a MusicXML file that can be reproduced by softwares like [Guitar Pro](https://www.guitar-pro.com/).

### Requirements

To run the code, you will need the following requirements:

1. [lxml](https://lxml.de/) to handle MusicXML files
2. [Python 3.6+](https://www.python.org/downloads/)
3. [IBM CPLEX Optimizer](https://www.ibm.com/br-pt/analytics/cplex-optimizer)

### How to run

The first step to get started is to generate the necessary sublicks. To do that, in root directory, run the following command line:

```
python3 sublicks_generator.py
```

After that, you need to generate the set of licks that will be used to generate a complete 12-Bar Blues progression. To do so, run:

```
python3 generate_sublicks.py d r t
```

Where **d**, **r** and **t** are, respectively, the number of default licks, repetition licks and turnaround licks to be generated. And finally, to generate the 12-Bar Blues progression, run:

```
python3 generate_prog.py
```

The output progression can be found in **gs_optimizer/results**.

### Considerations

This page is under construction. More content about the system will be released, like other details about parametrization and configuration.
