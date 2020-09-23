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

#These import statements give you access to library functions which you may
# (or may not?) want to use.
from math import *
from glider import *



#This is the function you will have to write for part A. 
#-The argument 'height' is a floating point number representing 
# the number of meters your glider is above the average surface based upon 
# atmospheric pressure. (You can think of this as hight above 'sea level'
# except that Mars does not have seas.) Note that this sensor may be
# slightly nosiy. 
# This number will go down over time as your glider slowly descends.
#
#-The argument 'radar' is a floating point number representing the
# number of meters your glider is above the specific point directly below
# your glider based off of a downward facing radar distance sensor. Note that
# this sensor has random Gaussian noise which is different for each read.

#-The argument 'mapFunc' is a function that takes two parameters (x,y)
# and returns the elevation above "sea level" for that location on the map
# of the area your glider is flying above.  Note that although this function
# accepts floating point numbers, the resolution of your map is 1 meter, so
# that passing in integer locations is reasonable.
#
#
#-The argument OTHER is initially None, but if you return an OTHER from
# this function call, it will be passed back to you the next time it is
# called, so that you can use it to keep track of important information
# over time.
#

def estimate_next_pos(height, radar, mapFunc, OTHER=None):
   """Estimate the next (x,y) position of the glider."""

   #example of how to find the actual elevation of a point of ground from the map:
   actualElevation = mapFunc(5,4)

   # You must return a tuple of (x,y) estimate, and OTHER (even if it is NONE)
   # in this order for grading purposes.
   #
   xy_estimate = (0,0)  #Sample answer, (X,Y) as a tuple.

   #TODO - remove this canned answer which makes this template code
   #pass one test case once you start to write your solution.... 
   xy_estimate = (391.4400701739478, 1449.5287170970244) 

   # You may optionally also return a list of (x,y,h) points that you would like
   # the PLOT_PARTICLES=True visualizer to plot for visualization purposes.
   # If you include an optional third value, it will be plotted as the heading
   # of your particle.

   optionalPointsToPlot = [ (1,1), (2,2), (3,3) ]  #Sample (x,y) to plot 
   optionalPointsToPlot = [ (1,1,0.5),   (2,2, 1.8), (3,3, 3.2) ] #(x,y,heading)


   return xy_estimate, OTHER, optionalPointsToPlot


# This is the function you will have to write for part B. The goal in part B
# is to navigate your glider towards (0,0) on the map steering # the glider 
# using its rudder. Note that the Z height is unimportant.

#
# The input parameters are exactly the same as for part A.

def next_angle(height, radar, mapFunc, OTHER=None):

   #How far to turn this timestep, limited to +/-  pi/8, zero means no turn.
   steering_angle = 0.0

   # You may optionally also return a list of (x,y)  or (x,y,h) points that 
   # you would like the PLOT_PARTICLES=True visualizer to plot.
   #
   #optionalPointsToPlot = [ (1,1), (20,20), (150,150) ]  # Sample plot points 
   #return steering_angle, OTHER, optionalPointsToPlot

   return steering_angle, OTHER
