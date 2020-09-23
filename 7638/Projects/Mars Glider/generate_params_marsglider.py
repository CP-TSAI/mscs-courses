from __future__ import division
from __future__ import print_function
from builtins import range
from past.utils import old_div
######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

import random
import math

PI = math.pi

for i in range(1,10+1):
    test_case = i
    target_x = random.uniform(-250,250)
    target_y = random.uniform(-250,250)
    target_heading = random.gauss(0,PI/4.0) 
    map_seed = random.randint(1,5000)
    map_freq = (random.random() * 4)  + 4.0
    measurement_noise = random.random()
    turning_noise = random.random() / 20.0 

    output = """'test_case': {},
     'target_x': {},
     'target_y': {},
     'target_heading': {},
     'map_seed': {},
     'map_freq': {},
     'measurement_noise': {},
     'turning_noise': {},
     'max_steps': 4500 
""".format(i, target_x, target_y, target_heading, map_seed, map_freq, measurement_noise, turning_noise )

    print("    {" + output + "    },")
