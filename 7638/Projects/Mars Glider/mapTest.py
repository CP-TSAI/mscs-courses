from __future__ import division
from builtins import zip
from past.utils import old_div
#Generate a map and plot it with maptplotlib

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

from opensimplex import OpenSimplex

def getMapFunc(Seed, Freq):

   gen = OpenSimplex(Seed)  

   def mapFunc(nx,ny):   

      #force 1 unit accuracy by converting floating point numbers to integers
      nx = int(nx)
      ny = int(ny)
      nx = nx / 5000.0
      ny = ny / 5000.0 

      #Generate noise from both low and high frequency noise:
      e0 = 1 * gen.noise2d(Freq * nx, Freq * ny)
      e1 = 0.5 * gen.noise2d(Freq*4*nx, Freq*4*ny)  
      e2 = 0.25 * gen.noise2d(Freq*16*nx, Freq*16*ny) 
      e = e0 + e1 + e2

      return e * 500  #500 meters above/below average...

   return mapFunc


from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plot
import numpy as np

mapFunc = getMapFunc(1, 2.0)

fig = plot.figure()
ax = fig.gca(projection="3d")

x = y = np.arange(-500, 500, 10)
X, Y = np.meshgrid(x,y)
zs = np.array( [mapFunc(x,y) for x,y in zip(np.ravel(X), np.ravel(Y) ) ] )
Z = zs.reshape(X.shape)

ax.plot_surface(X,Y,Z)
ax.set_zlim(zmin=-500, zmax=2000)

plot.show()


