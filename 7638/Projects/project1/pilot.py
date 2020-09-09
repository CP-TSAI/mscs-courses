
from builtins import object
import random

class Pilot(object):

    def __init__(self, min_dist, in_bounds):
        self.min_dist = min_dist
        self.in_bounds = in_bounds

    def observe_asteroids(self, asteroid_locations):
        """ self - pointer to the current object.
           asteroid_locations - a list of asteroid observations. Each 
           observation is a tuple (i,x,y) where i is the unique ID for
           an asteroid, and x,y are the x,y locations (with noise) of the
           current observation of that asteroid at this timestep.
           Only asteroids that are currently 'in-bounds' will appear
           in this list, so be sure to use the asteroid ID, and not
           the position/index within the list to identify specific
           asteroids. (The list may change in size as asteroids move
           out-of-bounds or new asteroids appear in-bounds.)

           Return Values:
                    None
        """

        pass

    def estimate_asteroid_locs(self):
        """ Should return an iterable (list or tuple for example) that
            contains data in the format (i,x,y), consisting of estimates
            for all in-bound asteroids. """
        return []

    def next_move(self, craft_state):
        """ self - a pointer to the current object.
            craft_state - implemented as CraftState in craft.py.

            return values: 
              angle change: the craft may turn left(1), right(-1), 
                            or go straight (0). 
                            Turns adjust the craft's heading by 
                             angle_increment.
              speed change: the craft may accelerate (1), decelerate (-1), or 
                            continue at its current velocity (0). Speed 
                            changes adjust the craft's velocity by 
                            speed_increment, maxing out at max_speed.
         """

        return random.randint(-1,1), random.randint(-1,1)
