""" 
This program will demonstate wave interference for two uniform sources radiating waves isotropically. 

500x500 grid, 1 bin = 1m square
"""
from math import pi,sqrt,sin
from numpy import empty
from pylab import imshow, gray, show

wl = 5.0 #wavelength
k = 2*pi/wl #wave vector
xi0 = 1.0
seperation = 20.0     #for r1 and r2 in cm
side = 100            #side of square in cm
points = 500          #number of gridpoints
spacing = side/points #spacing btwn points

x1 = side/2 + seperation/2
y1 = side/2
x2 = side/2 - seperation/2
y2 = side/2

#for storing heights
xi = empty([points,points],float)

for i in range(points):
    y = spacing*i
    for j in range(points):
        x = spacing*j
        r1 = sqrt((x-x1)**2 + (y-y1)**2)
        r2 = sqrt((x-x2)**2 + (y-y2)**2)
        xi[i,j] = xi0*sin(k*r1) + xi0*sin(k*r2)

imshow(xi,origin="lower",extent=[0,side,0,side])
gray()
show()


