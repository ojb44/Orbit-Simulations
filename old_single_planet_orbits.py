"""
Created on Mon Nov 23 21:32:01 2020

Author: OllieBreach

Description:
    Orbit simulations
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import matplotlib.animation as animation

#parameters
G=1
M=10
m=1

def gravity(t,r):
    #takes in a 4D vector (x,y,vx,vy) and returns its derivative
    return (r[2],r[3], (-G*M*m/((r[0]**2 + r[1]**2)**(3/2)))*r[0], (-G*M*m/((r[0]**2 + r[1]**2)**(3/2)))*r[1])

#generate range of time values
t=np.linspace(0,1000,10000)
#initial conditions (x,y,vx,vy)
init=np.array([0,1,4,0])
#solution
sol = solve_ivp(gravity, [t[0],t[-1]], init, t_eval=t)

x_vals = sol.y[0]
y_vals = sol.y[1]
# plt.plot(t, x_vals)
# plt.plot(t, y_vals)


#Animation
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 5), ylim=(-5, 5))
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o', lw=2)



def init():
    line.set_data([], [])

    return line,

def animate(i):
    thisx = [0, x_vals[i]]
    thisy = [0, y_vals[i]]

    line.set_data(thisx, thisy)

    return line,

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(t)),
                              interval=100, blit=True, init_func=init)








