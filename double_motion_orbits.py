"""
Created on Mon Nov 23 23:11:26 2020

Author: OllieBreach

Description:
    Orbital motion with both masses moving.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import matplotlib.animation as animation

#parameters
G=1
M=10
m=1

class Planet:
    
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position)
        self.velocity = velocity
        
        
    def acceleration_single(self, planet1):
        rel_pos = self.position - planet1.position
        accel = -G*planet1.mass/((rel_pos[0]**2 + rel_pos[1]**2)**(3/2))* rel_pos
        return accel
    
    def net_accel(self, other_planets):
        net_accel=np.array([0,0])
        for planet in other_planets:
            net_accel = net_accel + self.acceleration_single(planet)
        return net_accel
    
    def display_planet(self):
        print("Mass: ", self.mass, " Position: ", self.position, " Velocity: ", self.velocity)
        
    
    
class SolarSystem:
    
    def __init__(self, planet_list):
        self.planets = planet_list
        self.num_planets = len(planet_list)
        self.state = self.state_vector()
        
    def state_vector(self):
        #Returns phase space vector of the state which is suitable to pass into an ode solver
        #[x1,y1,vx1,vx2,x2,y2,etc.]
        state_vec = np.array([[planet.position, planet.velocity] for planet in self.planets]).flatten()
        return state_vec

    def derivative(self):
        state_deriv=[]
        counter=0

        for planet in self.planets:
            other_planets = self.planets[:counter]+self.planets[counter+1:]
            state_deriv.append(planet.velocity)
            state_deriv.append(planet.net_accel(other_planets))
            counter+=1
        
        return state_deriv
            

            
p1=Planet(10, [1,0],[3,0])
p2=Planet(100, [0,0],[0,0])
ss=SolarSystem([p1,p2]) 
ss.derivative() 
        
        
        
        
        
        
        
        
        
        
    