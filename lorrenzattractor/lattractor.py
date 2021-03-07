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

print(statet[:,0][:7])
"""
fig = plt.figure()
ax = fig.gca(projection="3d")
line, = ax.plot([],[],[])
"""
fig = plt.figure()
ax = fig.add_subplot(111)
line, = ax.plot(statet[:,0],statet[:,1],lw=2)

def animate(i):
    x=statet[:,0]
    y=statet[:,1]

    line.set_data(x[:i],y[:i])
    return line,
ani = ani.FuncAnimation(fig, animate, len(statet[:,0]), interval = 100, blit=False)

#plt.plot(statet[:,0],statet[:,1])
ani.save('2dlorrenz.gif')
plt.show()

"""
ax = fig.gca(projection="3d")
ax.plot(statet[:, 0], statet[:, 1], statet[:, 2])
plt.draw()
plt.show()

#for updating frames
def update(i,factor):
    line.set_xdata(state[:,0])
    line.set_ydata(state[:,1])
    line.set_zdata(state[:,2])
 
    return line
"""
