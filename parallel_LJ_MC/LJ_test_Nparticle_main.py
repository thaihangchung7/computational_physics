import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import math
import matplotlib.animation as animation
#plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
from numpy import random
from numba import jit, njit, prange

"""Defining initial variables"""

parallel = False

rN = 10000

L = 1 #Simulation Box Size
N = 30 #Number of Particles

x = np.zeros(N)
y = np.zeros(N)

change_x = np.zeros(N)
change_y = np.zeros(N)

eps_atom = 1
beta = 1e-4
sig_atom = 0.1

dmax = 0.05*L

x_init = []
y_init = []

x_array = []
y_array = []

energy_arr = []
energy_per = []
trial_arr = []

E_old = 0

N_trial_move = 200

index_traveled = np.zeros(shape=(N,N_trial_move))
N_traveled = []

dist_arr = []

x_anim = np.zeros([N_trial_move,N,2])
y_anim = np.zeros([N_trial_move,N,2])

def initialization():
    counter = 0
    size = math.floor(np.sqrt(N)) + 1
    print("size = ",size)
    for i in range(0,size-1):
        for j in range(0,size-1):
        
            #print("test number", i*L/size)

            x[counter] = i*L/size
            y[counter] = j*L/size

            x_init.append(x[counter])
            y_init.append(y[counter])

            counter += 1

@njit
def distance(x1,y1,x2,y2):
    #Distance calculator between points x1 and x2


    dx = np.abs(x1 - x2)
    if dx > L/2.0:
        dx = L - dx

    dy = np.abs(y1 - y2)
    if dy > L/2.0:
        dy = L - dy 
    #print("distance calculated =" ,np.sqrt(dx**2 + dy**2), "|x1 = ", x1 , "|y1 = ", y1, "|x2 = ", x2, "|y2 =", y2)

    dist = np.sqrt(dx**2 + dy**2)

    if dist == 0:
        return 1
    elif dist != 0:
        return dist

@njit(parallel=True)
def LJ_potential(radial_dist):
    if radial_dist == 0:
        LJ = 0
    else:
        r_val = np.divide(sig_atom,radial_dist)
        #print("r_val = ",r_val)
        LJ = eps_atom*(((r_val)**12) - ((r_val)**6))
    return LJ


def energy():
    sumt = 0 
    for i in prange(0,N-1):
        for j in prange(0,N-1):
            if i != j:
                
                #print("x[i]=", x[i])           
                #print("x[j]=", x[j])
                #print("y[i]=", y[i])
                #print("y[j]=", x[j])
                
                #print("distance calculated = ", distance(x[i],y[i],x[j],y[j]))
                sumt = sumt +  LJ_potential(distance(x[i],y[i],x[j],y[j]))
                #print("sumt=",sumt)
    return sumt/2.0

@njit
def p_acc(E_o,E_n):
    #print("E_n (p_acc func)",E_n)
    #print("E_o (p_acc func)",E_o)
    dE = E_n - E_o
    #print("dE (p_acc func)=", dE)
    if dE < 0:
        return 1
    else:
        #p_acc = np.exp(-beta*dE)
        #print("exp (p_acc_func) = ",np.exp(-beta*dE))
        return np.exp(-beta*dE)

def displace_from_og():
    return 0


def displacement(index):

    change_x[index] = x[index]
    change_y[index] = y[index]

    randx = np.random.randint(rN)/rN
    randy = np.random.randint(rN)/rN

    dx = dmax*(randx - 0.5)
    dy = dmax*(randy - 0.5)

    traveled = np.sqrt(dx**2 + dy**2)
    #index_traveled[index][0] = traveled
    #print("dx=",dx)
    #print("dy=",dy)

    """Keep particle within box L"""
    x[index] = x[index] + dx
    if x[index] >= L:
        x[index] = x[index] % L #- L
    elif x[index]<0:
        x[index] = x[index] % L #+ L

    y[index] = y[index] + dy
    if y[index] >= L:
        y[index] = y[index] % L #- L
    elif y[index]<0:
        y[index] = y[index] % L #+ L
    
    return index, traveled, x[index], y[index]

def trial_move(trial_index): #parallel (non-physical, for cool animations)
    global E_old

    for index in range(0,N):
        N_index, dist_trav, x_i, y_i = displacement(index)

        index_traveled[index][trial_index] = dist_trav

        x_anim[trial_index][index,0]=x_i
        y_anim[trial_index][index,1]=y_i


        E_o = E_old
        E_n = energy()

        #print("dE (trial_move func)= ", E_n - E_o)

        p_temp = np.random.randint(rN)/rN
        p_acc_func = p_acc(E_o,E_n)
        #print("p_temp (trial_move func)",p_temp)
        #print("p_acc (trial_move func)",p_acc_func)
        dist_arr.append(p_acc_func)
        
        if p_temp<p_acc_func:
            
            E_old = E_n

            succ = 1

        else:

            x[index] = change_x[index]
            y[index] = change_y[index]
            #x[index] = change_x
            #y[index] = change_y
            succ = 0
        
    return succ, x_i, y_i

def trial_move_single(trial_index):
    global E_old

    index = np.random.randint(N)
    #print("index",index)
    
    N_index, dist_trav, x_i, y_i = displacement(index)
    #print(dist_trav)
    index_traveled[index][trial_index] = dist_trav
    #i_anim.append(N_index)

    #x_anim.append(x_i)
    #y_anim.append(y_i)
    #X,Y = np.meshgrid(x_i,y_i)

    #x_anim[index][trial_index,0]=X
    #y_anim[index][trial_index,1]=Y
    x_anim[trial_index][index,0]=x_i
    y_anim[trial_index][index,1]=y_i


    E_o = E_old
    E_n = energy()

    #print("dE (trial_move func)= ", E_n - E_o)

    p_temp = np.random.randint(rN)/rN
    p_acc_func = p_acc(E_o,E_n)
    #print("p_temp (trial_move func)",p_temp)
    #print("p_acc (trial_move func)",p_acc_func)
    dist_arr.append(p_acc_func)
    
    if p_temp<p_acc_func:
        
        E_old = E_n

        succ = 1

    else:
        
        #change_x.append(x[index])
        #change_y.append(y[index])

        x[index] = change_x[index]
        y[index] = change_y[index]
        #x[index] = change_x
        #y[index] = change_y
        succ = 0
    
    return succ, x_i, y_i
    
@njit(fastmath=True)
def progress(N,N_tot):
    return N/N_tot * 100

def main():
    print("=================Start of Simulation====================")

    np.random.seed(0)

    E_accu = 0
    N_succ = 0

    initialization()
    xy_anim = np.empty([N_trial_move,N,2])

    for i in range(0,N_trial_move):
        E_old = energy()

        if parallel == True:
            success, x_coord, y_coord = trial_move(i)
        elif parallel == False:
            success, x_coord, y_coord = trial_move_single(i)

        N_succ += success

        trial_arr.append(i)
        energy_per.append(E_old)

        E_accu += E_old

        #print("E_actual = ",E_accu)
        energy_arr.append(E_accu)
        print("Progress = ", progress(i,N_trial_move), "%")
    
    for n in prange(0,N):
        n_trav = np.cumsum(index_traveled[n][:])

        ax2.plot(trial_arr,n_trav)

    E_avg = E_accu/N_trial_move
    print("Successful trials = ",N_succ/N_trial_move * 100)
    print("Average Energy = ", E_avg)
    print(xy_anim)
    print(np.shape(xy_anim))

"""Initialize Canvas for Figures"""
fig = plt.figure(figsize=(10,5))
gs = gridspec.GridSpec(2,2,height_ratios=[2,1])

ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[1,0])
ax3 = fig.add_subplot(gs[0,1])
ax4 = fig.add_subplot(gs[1,1])

main()

ax1.set_title("Particle Positons")
ax1.scatter(x,y,s=5,label="final positions")
ax1.scatter(x_init,y_init,s=5,label = "intial positions")

ax2.set_title("particle displacement")

ax3.set_title("trial vs energy_accu")
ax3.plot(trial_arr,energy_per,label="Trial Energies")
ax3.axhline(sum(energy_per)/len(energy_per),label="Average Energy",c='r')

ax4.set_title("Energy histogram")
ax4.hist(energy_arr,bins=500)
#print(energy_arr)

ax1.legend()
ax3.legend()

def animate(i):

    figanim.clear()
    ax = figanim.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, 1), ylim=(0, 1))
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)
    ax.set_xlabel('x [a]')
    ax.set_ylabel('y [a]')

    ax.text(0.02, 0.95, 'Time step = %d' % i, transform=ax.transAxes)
    ax.grid(True,linestyle='--')
    
    print("progress =" , i)
    
    #print("x = ",x[i])
    #print("y = ",y[i])

    plotter = ax.scatter(x_anim[i][:N,0], y_anim[i][:N,1], s = 10)


if parallel == True:
    figanim, ax = plt.subplots()

    #Debug for anim
    #for i in range(0,N):
    #    plt.scatter(x_anim[i][:N,0],y_anim[i][:N,1])
    ani = animation.FuncAnimation(figanim, animate, interval=1, frames=200,repeat=True)
elif parallel == False:
    pass

plt.show()
#writervideo = animation.FFMpegWriter(fps=60)
if parallel == True:
    ani.save('/home/thc/Documents/computational_physics/parallel_LJ_MC/LJ_anim.gif',writer='ffmpeg')
elif parallel == False:
    pass
