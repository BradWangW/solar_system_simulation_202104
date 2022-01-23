"""
    Many Body System
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import G
from numpy.linalg import norm
from matplotlib.animation import FuncAnimation


class Body(object):
    """
    
        Simple class for a body (a planet or a satellite in case)
        to contain its inner and real-time properties
        
        Position, velocity and acceleration are all vecters input as lists
        and then transformed into an numpy array
        
    """
    
    def __init__(self, inf):
        """
        
        Parameters
        ----------
        inf : List containing the information of a body as follows
        [name, mass (in Kilogram), position (2D in Meter), velocity (2D in m/s), color (for animation), size (for animation)]

        """
        self.name = inf[0]
        self.mass = inf[1]
        
        # Positions, velocities and accelerations are input as 2D vectors
        # for the convenience of later calculations
        self.posi = np.array(inf[2])
        self.velo = np.array(inf[3])
        
        # Variable of the position before one timestep for later obtaining orbital period
        self.posi_past = self.posi.copy()
        
        # Color and Size for later plotting
        self.color = inf[4]                
        self.size = inf[5]                 
        
        # Accelerations of present, after one and two timesteps, initially all zeros
        # For later use of Beeman Method
        self.acce = np.zeros(2)
        self.acce_past = np.zeros(2)
        self.acce_past2 = np.zeros(2)
        
        # Variable to contain later computed orbital period
        self.orbit_period = 0

        

    def Ek(self):
        """
            Return the real-time kinetic energy of the body
        """
        return (self.mass * norm(self.velo) ** 2)/2




class Many_Body_System(object):
    """
    
        Class for a system containing a list of bodies
        as well as their inner properties
        Involved methods to simulate the evolution of the system visually
        
    """
    
    def __init__(self, bodies, delta_t):
        
        # Copied list of bodies in the system and the number of bodies
        self.bodies = bodies
        self.num = len(bodies)
        
        # Initialized energies and time (age of the system)
        self.energy()
        self.time = 0
        
        # Initialize timestep in Seconds and counter (used to record the number of timesteps have been simulated)
        self.delta_t = delta_t 
        self.counter = 0 
        
        # Created lists for total energy and time
        self.Es = [self.E_total]
        self.t = [self.counter * self.delta_t]
        
        
        
    def energy(self):
        """
        
            Method to update the total (kinetic and potential) energy of the system in Joule
            
        """
        
        # Reset Ek and Ep
        self.Ek_total = 0
        self.Ep_total = 0
        
        # Calculated total Ek of the system
        for i in range(len(self.bodies)):
            self.Ek_total += self.bodies[i].Ek()
            
            
            # Calculated total Ep of all pairs of bodies (repetitions avoided)
            for j in range(i + 1, len(self.bodies)):
                distance = norm(self.bodies[i].posi - self.bodies[j].posi)
                self.Ep_total += -(G * self.bodies[i].mass - self.bodies[j].mass)/(2 * distance)
        
        
        # Total energy
        self.E_total = self.Ek_total + self.Ep_total
        
        
    def acceleration(self):
        """
        
            Method to update the acceleration of each body in the system
            based on the net force of the gravitational forces
            imposed by all other bodies in the system
            
        """
        
        for i in self.bodies:
            
            # Created variable to sum up the accelerations
            acce = 0 
            
            # For each body but i-th body, calculate the acceleration
            # it impacts on i-th body individually and add them up
            for j in self.bodies:
                if i != j:
                
                    # Computed position difference and relevant distance between i, j
                    delta_p = i.posi - j.posi         
                    dis = norm(delta_p)
                
                    # Acceleration obtained directly
                    acce += -(G * j.mass/(dis ** 3)) * delta_p
            
            i.acce = acce

                
        
    def update(self):
        """
        
            Update each body's position, acceleration and velocity after a timestep
            as well as to periodically obtaining the total energy of the system
            Also timely compute the orbital period
            
        """
        
        # Past accelerations replaced
        for i in self.bodies:
            i.posi_past = i.posi.copy()
            i.acce_past2 = i.acce_past.copy()
            i.acce_past = i.acce.copy()               
            
            
        # Position updated by Beeman method
        for i in self.bodies:
            i.posi = i.posi + i.velo * self.delta_t + \
                    (4 * i.acce_past- i.acce_past2) * (self.delta_t ** 2)/6
            
            
        # Present accelerations updated
        self.acceleration()
        
            
        # Velocity updated by Beeman method
        for i in self.bodies:
            i.velo = i.velo + (2 * i.acce + 5 * i.acce_past - i.acce_past2) * self.delta_t/6
            
            
        # Counter is increased by 1 each time update() is run
        # This is for periodically return the total energy and record total time as well
        self.counter += 1
        
        
        # The total energy of the system is obtained every 10 timesteps
        if self.counter%10 == 0:
            
            # Updated total energy
            self.energy()
                
            # Updated time in Year and total energy in Joule for animation
            self.Es.append(self.E_total)
            self.t.append(self.counter * self.delta_t/31536000)
            
        
        # Calculate the orbital periods of the bodies in Year as they finish a cycle
        # i.e. cross the x-axis from negative to positive
        for i in self.bodies:
            if i.posi[1] >= 0 and i.posi_past[1] < 0:
                
                # Conditional so that the period of each body would be printed once
                # Also the Sun/satellite could be specialized so that that of it would not be printed
                if i.orbit_period == 0:
                    i.orbit_period = self.counter * self.delta_t/31536000
                    
                    print(f'The orbital period of {i.name} is {i.orbit_period} in year')
                    
            
    
    def animate(self, i):
        """
        
            Method to update the patches on the plot
            to process the animation
            
        """
        
        # Update needed information for one timestep
        self.update()        
        
        
        # Update the positions of bodies on the plot
        for j in range(self.num):
            self.patches[j].center = np.array(self.bodies[j].posi)
            
            
        # Update the total energy and time on the plot
        self.patches[-4].set_data(self.t, self.Es)
        
        # Update the printed total energy and the standard deviation
        self.patches[-3].set_text(f'Total Energy: {self.E_total} J')
        self.patches[-2].set_text(f'Standard Deviation: {np.std(self.Es)} J')
        self.patches[-1].set_text(f'Time: {round(self.t[-1], 7)} Year')

        # Return the list of patches
        return self.patches
                            
    
    
    def display(self, num_move, repeat = False, scale = 3e11):
        """

        Parameters
        ----------
        num_move : An positive integer
            Total number of timesteps being processed.
        repeat : False/True, optional
            Whether to continue animating after reaching the set number of timesteps. The default is False.
        scale : A positive real number, optional
            Half of the axis length of the plot for bodies in Meter. The default is 3e11 (for experiment 1 & 2).
        scale_E : A real number, optional
            Centre of the axes of the energy plot in Joule. The default is 6.2e33 (for experiment 1 & 2).

        Returns
        -------
        Animate the system.

        """
        
        # Initialize total number of timesteps
        self.num_move = num_move
        
        
        # Created figue and axes
        fig, ax = plt.subplots(1, 2, figsize = (16, 7))                
        
        # Created list to contain patches
        self.patches = []                 
        
        for i in self.bodies:
            
            # Patches of bodies created based on their positions, colors, and sizes, labeled by their names
            patch = plt.Circle(i.posi, i.size, color = i.color, animated = True, label = i.name)
            self.patches.append(patch)
            
            # Patches of bodies added to the first plot (axes)
            ax[0].add_patch(patch)           
        
        # Appended patch for the energy plot
        patch_E, = ax[1].plot(self.t, self.Es)
        self.patches.append(patch_E)
        
        # Appended patches for printing the real-time total energy and standard deviation
        Et = ax[1].text(0.5,0.90, '', transform = ax[1].transAxes, ha="center")
        std = ax[1].text(0.5,0.85, '', transform = ax[1].transAxes, ha="center")
        time = ax[1].text(0.5,0.80, '', transform = ax[1].transAxes, ha="center")
        self.patches.append(Et)
        self.patches.append(std)
        self.patches.append(time)

        
        # Set up the appearance of the plots
        ax[0].set_title('Solar System', fontsize = 13)
        ax[0].set_ylabel('Meter')
        ax[0].set_xlabel('Meter')
        ax[0].axis('scaled')  

        # Axes (scale) limits of the plot (just for this case)               
        ax[0].set_xlim(-scale, scale)        
        ax[0].set_ylim(-scale, scale)
        ax[0].legend()
       
        ax[1].set_title('Total Energy of The System against Time', fontsize = 13)
        ax[1].set_ylabel('Total Energy (Joule)')
        ax[1].set_xlabel('Time (Year)')
        
        # Time is limited by where the animation terminates
        ax[1].set_xlim(0, self.num_move * self.delta_t/31536000)        
        
        # Total energy in a small interval (scale needs to be obtain by tests before)
        ax[1].set_ylim(self.E_total * 0.95, self.E_total * 1.05)
        
        
        # Animation processes with the option of repeated animation
        # if not, it would be updated for exactly num_move times
        self.anim = FuncAnimation(fig, self.animate, num_move, repeat = repeat, interval = 5, blit = True)
        
        plt.show()
        
        

        