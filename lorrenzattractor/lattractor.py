import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as ani

#butterfly sig=10,rho=28, beta=8/3

sig = 10
rho = 28
beta = 8/3


def lorrenz(state,t):
    x, y, z = state
    
    return sig*(y-x), x*(rho-z)-y, x*y-beta*z
    
state0 = [1.0,1.0,1.0]
t = np.arange(0.0,40.0,0.01)
statet = odeint(lorrenz,state0,t)

print(statet)

fig = plt.figure()
ax = fig.gca(projection="3d")
ax.plot(statet[:, 0], statet[:, 1], statet[:, 2])
#make this work?
#animator = ani.FuncAnimation(fig,,interval=100)
plt.draw()
plt.show()


