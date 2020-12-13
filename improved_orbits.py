"""
Created on Sun Dec 13 14:04:31 2020

Author: OllieBreach

Description: Improved way of doing the orbit simulation.

Will define state by two N by 2 matrices, one for position and one for velocity.
N-d vector for masses.
Will update with Verlet integration. 
"""

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import matplotlib.animation as animation

#parameters
G=1
M=10
m=1


class SolarSystem:
    
    def __init__(self, positions, velocities, masses):
        self.positions=positions
        self.velocities=velocities
        self.masses=masses
        
    def accel(self):
        #x and y positions
        x=np.array(self.positions[:,0:1])
        y=np.array(self.positions[:,1:2])
        #print(x,y)
        #matrices of pair-wise interactions
        delta_x=x.T-x
        delta_y=y.T-y
        #print(delta_x, delta_y)
        #1/(delta_r)^3 for each pair
        r_cubed_inv = (delta_x**2 + delta_y **2+0.001) **(-1.5)
        #pairwise interactions for each component:
        x_pairs = delta_x * r_cubed_inv
        y_pairs = delta_y * r_cubed_inv
        #print(x_pairs, y_pairs)
        #acceleration from pairs - multiply by masses and sum over a pair - equivalent to matrix multiplication
        x_accel = G*np.dot(x_pairs,np.array(self.masses))
        y_accel = G*np.dot(y_pairs,np.array(self.masses))
        #combine into N by 2 matrix:
        acc=np.vstack((x_accel, y_accel)).T
        return acc
    
    def pe(self):
        #potential energy of configuration
        #similar to method for acceleration but do 1/r^2 and then have just r on top (can't do 1/r bc need r on top for self interactions to give 0)
        #x and y positions
        x=np.array(self.positions[:,0:1])
        y=np.array(self.positions[:,1:2])
        #print(x,y)
        #matrices of pair-wise interactions
        delta_x=x.T-x
        delta_y=y.T-y
        #print(delta_x, delta_y)
        #1/(delta_r)^2 and r for each pair
        r=(delta_x**2 + delta_y **2+0.001) **(0.5)
        r_squared_inv = (delta_x**2 + delta_y **2+0.0001) **(-1)
        #1/r for each pair
        inverse_r = r*r_squared_inv
        #multiply by masses and sum - potential energy for each planet
        individual_energies = -0.5*G*np.dot(inverse_r,np.array(self.masses))
        #sum and multiply by half to avoid double counting
        pot_energy = np.sum(individual_energies)
        return pot_energy
    
    def ke(self):
        #kinetic energy of configuration
        #first get matrix of velocities squared in each component
        v_squ_comps = self.velocities*self.velocities
        #add along rows to get resultant velocity squared of each particle
        v_squ = np.sum(v_squ_comps, axis=1)
        #multiply by masses, sum, and divide by two for ke
        kin_energy = 0.5*np.sum(v_squ*np.array(self.masses))
        return kin_energy
    
    def cm_vel(self):
        #velocity of the centre of mass
        mvs=np.array([self.masses]).T*self.velocities
        sum_mvs=np.sum(mvs, axis=0)
        return sum_mvs/np.sum(self.masses)
    
    def cm_frame(self):
        #convert into centre of mass frame
        self.velocities=self.velocities-self.cm_vel()

    def update(self, dt):
        #verlet update
        self.positions = self.positions+self.velocities*dt + 0.5*self.accel()*(dt**2)
        self.velocities = self.velocities+self.accel()*dt
        
    def update_leapfrog(self, dt):
        #leapfrog update
        self.velocities=self.velocities+self.accel()*(dt/2)
        self.positions=self.positions+self.velocities*dt
        self.velocities=self.velocities+self.accel()*(dt/2)
        
        
    def plot_planets(self):
        x=np.array(self.positions[:,0:1])
        y=np.array(self.positions[:,1:2])
        plt.plot(x,y, 'o')




#Animation
def planet_animate(dt,skip):
    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-6, 6), ylim=(-6, 6))
    ax.set_aspect('equal')

    
    line, = ax.plot([], [], 'o', lw=2)
    
    
    
    def init():
        line.set_data([], [])
    
        return line,
    
    def animate(i):
        thisx=np.array(ss.positions[:,0:1])
        thisy=np.array(ss.positions[:,1:2])
        for j in range(skip):
            ss.update_leapfrog(dt)
        line.set_data(thisx, thisy)
        
    
        return line,
    
    ani = animation.FuncAnimation(fig, animate,
                                  interval=20, blit=True, init_func=init)


        
        
#check energy remains constant:

def energy_check():
    kes=[]
    pes=[]
    
    for i in range(100):
        for i in range(1000):
            ss.update_leapfrog(0.00001)
        kes.append(ss.ke())
        pes.append(ss.pe())
    energies = np.array(kes)+np.array(pes)
    
    plt.plot(kes, label='KE')
    plt.plot(pes, label='PE')
    plt.plot(energies, label='Tot')
    plt.legend()


#run simulation

# pos=np.array([[0,0],[1,0], [2,2]])
# vel = np.array([[0,-0.1],[0,10], [2,-2]])
# masses=[100,1,3]

# n=100
# masses = (20*np.ones((n))/n).tolist()
# pos = np.random.randn(n,2)  
# vel = np.random.randn(n,2)

pos=np.array([[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0]])
vel=np.array([[0,0],[0,10],[0,np.sqrt(100/2)],[0,np.sqrt(100/3)],[0,np.sqrt(100/4)],[0,np.sqrt(100/5)], [0,np.sqrt(100/6)]])
masses=[100,0.1,0.1,0.1,0.1, 0.1,0.1]

ss=SolarSystem(pos,vel,masses)
ss.cm_frame()


planet_animate(0.0001, 100)


    