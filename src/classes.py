''' Contains the ```Particle``` and ```Nucleus``` classes. '''

# import externals
import pygame
import math
import random
import json

# import constants used
from src.constants import PARTICLE_TYPES, MENU_WIDTH, WIDTH, HEIGHT, HADRON_LIST, MESON_LIST

# load elements from json file
def load_element_data(file_path:str="atom_recipes.json") -> dict:
    '''
    Returns the data in a json file as a dictionary. Default json path is
    local: ```atom_recipes.json```, can be overidden.
    
    '''
    with open(file_path, 'r') as f:
        return json.load(f)
    
ELEMENTS = load_element_data()
'''Json data in form of dictionary'''

# particle Class
class Particle:
    '''
    Class used for all particle types used in simulation workspace.
    Dynamically updates, draws and shows info in a tooltip when 
    hovered.
    
    '''
    # constructor
    def __init__(self, type_name:str, position:tuple[float, float], velocity:tuple[float, float]) -> None:
        self.type_name = type_name
        self.mass = PARTICLE_TYPES.get(type_name, {}).get('mass', 1)
        self.charge = PARTICLE_TYPES.get(type_name, {}).get('charge', 0)
        self.color = PARTICLE_TYPES.get(type_name, {}).get('color', (255, 255, 255))
        self.position = position
        self.velocity = velocity

        self.age = 0
        self.decay_age = PARTICLE_TYPES.get(type_name, {}).get('decay-timer', None)
        
        self.radius = PARTICLE_TYPES.get(type_name, {}).get('radius', 5)
        self.energy = 0

        self.orbiting = None

        if self.type_name == 'Electron':
            self.orbital_speed = 0
            while -1 < self.orbital_speed < 1:
                self.orbital_speed = random.randrange(-50, 50) / 10

        self.orbit_angle = 0
        self.orbit_radius = 0

    # update the particle position, velocity and other
    def update(self, dt:float) -> None:
        '''
        Update the particle dynamically. Changes velocity and position
        If particle is an electron then handle orbit logic.
        
        Handle collisions with workspace bounds by inverting x and y 
        velocity appropriately.
        
        '''

        # electron orbit logic
        if self.type_name == 'Electron' and self.orbiting:
            nucleus = self.orbiting
            self.orbit_angle += dt * self.orbital_speed
            self.position[0] = nucleus.position[0] + math.cos(self.orbit_angle) * self.orbit_radius
            self.position[1] = nucleus.position[1] + math.sin(self.orbit_angle) * self.orbit_radius

        # change particle position
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

        self.age += dt

        # handle collisions with sim edges if not orbiting electrons
        if self.type_name == 'Electron' and self.orbiting:
            pass
        # potentially more logic here
        else:
            if self.position[0] < MENU_WIDTH + self.radius:
                self.position[0] = MENU_WIDTH + self.radius
                self.velocity[0] *= -1
            if self.position[0] > WIDTH - self.radius:
                self.position[0] = WIDTH - self.radius
                self.velocity[0] *= -1
            if self.position[1] < 0 + self.radius:
                self.position[1] = self.radius
                self.velocity[1] *= -1
            if self.position[1] > HEIGHT - self.radius:
                self.position[1] = HEIGHT - self.radius
                self.velocity[1] *= -1

        self.energy = math.hypot(self.velocity[0], self.velocity[1])
        #self.energy = 0.5 * self.mass * vel**2

    # draw particle
    def draw(self, surface:pygame.Surface) -> None:
        '''Draw the particle as a circle with specified radius, position and colour.'''
        pygame.draw.circle(surface, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

    # logic to detect whether the particle is hovered
    def is_hovered(self, mouse_pos:tuple[float, float]) -> bool:
        '''
        Determine whether the particle is hovered. Returns a bool used to
        determine whether to draw a tooltip that shows additional information.
        
        >>> print(Particle.is_hovered(pos))
        True
        
        '''
        dx = self.position[0] - mouse_pos[0]
        dy = self.position[1] - mouse_pos[1]
        distance = math.hypot(dx, dy)
        return distance <= self.radius
    
# atom nucleus class
class Nucleus:
    '''Similar to the Particle class, however, has additional values.'''
    # constructor
    def __init__(self, protons:int, neutrons:int, position:list[int, int], name:str='Unknown', color:str='#FFFFFF', velocity:list[int, int]=None) -> None:
        self.type_name = 'Nucleus'
        self.protons = protons
        self.neutrons = neutrons
        self.mass_num = len(protons) + len(neutrons)
        self.position = position
        self.charge = len(protons)
        self.radius = 12 + (len(self.neutrons) + len(self.protons)) / 2
        self.color = color
        self.name = name

        if velocity is None: self.velocity = [random.uniform(-50, 50), random.uniform(-50, 50)]
        else: self.velocity = velocity

        # create isotopic name for mass number
        if len(self.neutrons) != ELEMENTS.get(name.lower(), {}).get('neutrons'):
            self.name += f'-{self.mass_num}'

        #print("new nucleus created")

    # update method
    def update(self, dt:float) -> None:
        '''
        Update the nucleus dynamically. Changes velocity and position.
        
        Handle collisions with workspace bounds by inverting x and y 
        velocity appropriately.
        
        '''
        # update position
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

        # sim edge collisions
        if self.position[0] < MENU_WIDTH + self.radius:
            self.position[0] = MENU_WIDTH + self.radius
            self.velocity[0] *= -1
        if self.position[0] > WIDTH - self.radius:
            self.position[0] = WIDTH - self.radius
            self.velocity[0] *= -1
        if self.position[1] < 0 + self.radius:
            self.position[1] = self.radius
            self.velocity[1] *= -1
        if self.position[1] > HEIGHT - self.radius:
            self.position[1] = HEIGHT - self.radius
            self.velocity[1] *= -1

    # draw nucleus
    def draw(self, surface:pygame.Surface) -> None:
        '''Draw the nucleus as a circle with specified radius, position and colour.'''
        pygame.draw.circle(surface, pygame.Color(self.color), (int(self.position[0]), int(self.position[1])), self.radius)

    # return whether nucleus is hovered
    def is_hovered(self, mouse_pos:tuple[float, float]) -> bool:
        '''
        Determine whether the nucleus is hovered. Returns a bool used to
        determine whether to draw a tooltip that shows additional information.
        
        >>> print(Nucleus.is_hovered(pos))
        False
        
        '''
        dx = self.position[0] - mouse_pos[0]
        dy = self.position[1] - mouse_pos[1]
        distance = math.hypot(dx, dy)
        return distance <= self.radius
