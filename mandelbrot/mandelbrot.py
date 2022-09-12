#! /usr/bin/python

#z_n = z*z_(n-1) + c 
#where z_(0) = c, where c is a complex number

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

def mandelbrot(N=501, maxiter = 100, scaled = True):
  
  Mset = np.zeros((N,N))
  if scaled: Mset += np.log(maxiter)
    
  for i,x in enumerate(np.linspace(-2,2,N)):
    if i % (N/5) == 0: print("i=",i)
    for k,y in enumerate(np.linspace(-2,2,N)):

      z = 0 + 0j
      c = complex(x,y)

      for n in range(maxiter):
        z = z*z + c
        if np.abs(z) >2:
          Mset[i,k] = np.log(n+1) if scaled else 1
          break

  return Mset

plt.imshow(mandelbrot(scaled=False))
#plt.gray()
plt.imshow(mandelbrot(),cmap=cm.inferno)
plt.show()
