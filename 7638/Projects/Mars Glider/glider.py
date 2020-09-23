from __future__ import division
from __future__ import print_function
from builtins import object
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

from math import *
import random


def angle_trunc(a):
    """Helper function to map all angles onto [-pi, pi]

    Arguments:
        a(float): angle to truncate.

    Returns:
        angle between -pi and pi.
    """
    return ((a + pi) % (pi * 2)) - pi


class glider(object):
    """Robotc glider simulator.

    Attributes:
        x(float): x position.
        y(float): y position.
        z(float): z (altitude) position.

        heading(float): angle currently facing with 0 being east.

        mapFunc(function(x,y)) : A function that returns the elevation of
           the ground at a specific x,y location.

        measurement_noise(float): noise of radar height measurement.


        speed(float): distance to travel for each timestep.
    """

    def __init__(self, x=0.0, y=0.0, z=5000, heading=0.0, mapFunc = None, rudder=0, speed=5.0 ):
        """This function is called when you create a new robot. It sets some of
        the attributes of the robot, either to their default values or to the values
        specified when it is created.

        """
        self.x = x
        self.y = y
        self.z = z
        self.speed = speed
        self.mapFunc = mapFunc
        self.heading = heading

        #These attributes are set via the set_noise function.
        self.measurement_noise = 0.0
        self.turning_noise = 0.0
        self.altitude_noise = 0.0

    def set_noise(self, new_m_noise, new_turn_noise= 0.0, new_alt_noise=0.0):
        """This lets us change the noise parameters, which can be very
        helpful when using particle filters.

        Arguments:
            new_m_noise(float): measurement noise to set.
            new_turn_noise(float): Turning noise to set. (optional)
            new_alt_noise(float): altitude noise to set. (optional)
        """
        self.measurement_noise = float(new_m_noise)
        self.turning_noise = float(new_turn_noise)
        self.altitude_noise = float(new_alt_noise)

    def glide(self, rudder=0.0,  max_turning_angle=pi/8.0):
        """This function optionally turns the robot and then moves it forward.
           Note that the changes are made to a duplicate  glider object that 
           is returned, so the original glider object will not be modified! 

        Arguments:
            rudder(float): angle to turn (if provided)
            max_turning_angle(float): max allowed turn.
                defaults to pi/8.
        """

        #Each timestep, we fall 1 unit and trade that for glide_ratio/speed
        #units of horizontal movement.
        z = self.z - 1.0

        #truncate to fit physical limits of turning angle
        rudder = max(-max_turning_angle, rudder)
        rudder = min(max_turning_angle, rudder)

        #Add noise (if included)
        rudder += random.uniform(-self.turning_noise, self.turning_noise)


        # Execute motion (we alwasy go speed/distance forward)
        heading = self.heading + rudder
        heading = angle_trunc(heading)
        x = self.x + (self.speed * cos(heading))
        y = self.y + (self.speed * sin(heading))

        ret = glider( x       = x,
                      y       = y,
                      z       = z,
                      heading = heading,
                      mapFunc = self.mapFunc,
                      speed   = self.speed )

        ret.set_noise( new_m_noise    = self.measurement_noise,
                       new_turn_noise = self.turning_noise,
                       new_alt_noise  = self.altitude_noise )

        return ret

    def sense(self):
        """This function represents the glider sensing its hight above ground.
        When measurements are noisy, this will return a value that is close to,
        but not necessarily equal to the actual distane to ground at the
        gliders current  (x, y) position.

        Returns:
            Height radar sensor  measurement based on x,y location, measurement noise.
        """
        if self.mapFunc == None:
           print("No Map Function, can't determine hight above ground")
           return None
        
        height = self.z - self.mapFunc(self.x,self.y) 
        
        #Apply gausian measurement noise (if any)
        return random.gauss(height, self.measurement_noise)


    def get_height(self):
        """This function returns the gliders hight based upon barametric 
           pressure, which may be +/- some gausian noise."""

        return self.z + random.gauss(0, self.altitude_noise) 


    def __repr__(self):
        """This allows us to print a robot's position

        Returns:
            String representation of glider that is the x and y location as
            well as the actual altitude. 
        """
        return '[%.2f, %.2f, %0.2f]' % (self.x, self.y, self.z)
