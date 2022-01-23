"""
    Solar System - Experiment 1
"""

from ManyBody import *

def main():
    
    # List to contain the info lists of the bodies
    planets_inf = []
    
    # Read in the data file for E1 and created list of the lines
    filein = open('planets E1.txt', 'r')
    info = filein.readlines()
    
    # Extract infomation line by line
    for i in range(6):
        
        # Split the data in each line
        tokens = info[i].split(",")
        
        # Info list of a body
        planets_inf.append([tokens[0], float(tokens[1]), [float(tokens[2]), float(tokens[3])],\
                          [float(tokens[4]), float(tokens[5])], tokens[6], float(tokens[7])])
    
    # Created bodies
    Sun = Body(planets_inf[0])
    Mercury = Body(planets_inf[1])
    Venus = Body(planets_inf[2])
    Earth = Body(planets_inf[3])
    Mars = Body(planets_inf[4])
    Trivi = Body(planets_inf[5])
    
    # Specified so that their orbti periods won't be printed
    Sun.orbit_period = 1
    Trivi.orbit_period = 1
    
    # List of the bodies and constructed corresponding system
    # with delta t equal to 300 seconds
    planets = [Sun, Mercury, Venus, Earth, Mars, Trivi]
    system = Many_Body_System(planets, 300)
    
    # Visualized system
    system.display(3000, repeat = False)

main()

