'''
Contains useful helper methods used throughout the simulation such as 
quark methods for drawing / simulating gluons, atom logic and more.

'''

# externals
import pygame
import math
import random
import json

import copy

# import locals
from src.classes import Particle, Nucleus
from src.constants import WIDTH, HEIGHT, QUARK_LIST

# load elements from json file
def load_element_data(file_path:str="atom_recipes.json") -> dict:
    '''
    Returns the data in a json file as a dictionary. Default directory is
    local: ```atom_recipes.json```, can be overidden.
    
    '''
    with open(file_path, 'r') as f:
        return json.load(f)
    
ELEMENTS = load_element_data()
'''Dictionary containing all elements and their properties used in the simulation.'''

# helper functions --------------
# spawn a particle with random velocity and add to particle list
def spawn_particle(type_name:str, position:tuple[float, float], particles:list, velocity_param:list[int, int]=None) -> None:
    '''
    Spawn a particle in the simulation at position: ```position```, of type: ```type_name```,
    velocity as ```velocity_param```, which when set to None, defaults to a random 
    velocity between -50 and 50 for both x and y.
    
    Adds new particle to ```particles```.
    
    '''
    velocity = [random.uniform(-50, 50), random.uniform(-50, 50)] if velocity_param is None else velocity_param
    particles.append(Particle(type_name, position, velocity))

# get average position of a list of particles (used for particle fusion)
def average_position(particles_list:list) -> list[float, float]:
    '''
    Returns the average position of a list of particles in the simulation
    workspace.
    
    >>> particles = [Particle(... position=(10.2, 30.5)...), Particle(... position=(23, 27.1)...), Particle(... position=(5, 4.2)...)]
    >>> print(average_position(particles))
    [12.73333333333333, 20.6]
    
    '''
    x = sum(p.position[0] for p in particles_list) / len(particles_list)
    y = sum(p.position[1] for p in particles_list) / len(particles_list)
    return [x, y]

def average_speed(particles_list:list) -> list[float, float]:
    '''
    Returns the average velocity of a list of particles in the simulation
    workspace.
    
    >>> particles = [Particle(... velocity=(24, 10)...), Particle(... position=(17.1, 19)...), Particle(... position=(3, 3)...)]
    >>> print(average_position(particles))
    [14.7, 10.666666666666667]
    
    '''
    x = sum(p.velocity[0] for p in particles_list) / len(particles_list)
    y = sum(p.velocity[1] for p in particles_list) / len(particles_list)
    return [x, y]

# check whether particles are close to one another by looping through a list
def particles_close(particle_list:list, threshold:int=50) -> bool:
    '''
    Check if a list of particles are closer than a threshold to each other. Used
    when creating larger particles, e.g. a neutron from 2 down quarks and
    1 up quark.

    Can specify a threshold, however defaults to 50 if left empty.
    
    >>> particles = [Particles(... position=(20, 13)), Particles(... position=(4, 49)), Particles(... position=(90, 18))]
    >>> print(particles_close(particles))
    False
    
    '''
    for i in range(len(particle_list)):
        for j in range(i+1, len(particle_list)):
            p1 = particle_list[i]
            p2 = particle_list[j]
            dist = math.hypot(p1.position[0] - p2.position[0], p1.position[1] - p2.position[1])
            if dist > threshold:
                return False
    return True

# find groups of quarks
def find_quark_groups(particles:list) -> list:
    '''
    Return a list of quark triplets within the quark fusion threshold.
    Quarks cannot be reused in multiple sets.

    >>> particles = [...]
    >>> print(find_quark_groups(particles))
    [[_, _, _], [_, _, _]]

    '''
    # helper local vars
    quarks = [p for p in particles if p.type_name in QUARK_LIST]
    groups = []
    used = set()

    # loop through lists
    for i in range(len(quarks)):
        for j in range(i+1, len(quarks)):
            for k in range(j+1, len(quarks)):
                triplet = [quarks[i], quarks[j], quarks[k]]

                # make sure particles arent used
                if id(quarks[i]) in used or id(quarks[j]) in used or id(quarks[k]) in used:
                    continue

                # if the particles are close, add these particles to list
                if particles_close(triplet):
                    groups.append(triplet)
                    used.update([id(quarks[i]), id(quarks[j]), id(quarks[k])])

    # return the final list
    return groups

# find pairs of quarks
def find_quark_pairs(particles:list) -> list:
    '''
    Return a list of quark pairs within the quark fusion threshold.
    Quarks cannot be reused in multiple pairs.

    >>> particles = [...]
    >>> print(find_quark_pairs(particles))
    [[_, _], [_, _], [_, _]]

    '''
    # helper local vars
    quarks = [p for p in particles if p.type_name in QUARK_LIST]
    groups = []
    used = set()

    # loop through list
    for i in range(len(quarks)):
        for j in range(i+1, len(quarks)):
            # get the quark pair
            pair = [quarks[i], quarks[j]]

            # make sure particles arent used
            if id(quarks[i]) in used or id(quarks[j]) in used:
                continue

            # if the particles are close 
            if particles_close(pair):
                
                groups.append(pair)
                used.update([id(quarks[i]), id(quarks[j])])

    # return the final list
    return groups

# form a large particle from smaller particles
def form_composite(particle_list:list, new_type:str, particles:list) -> None:
    '''
    Create a composite particle from other particles. When the composite particle
    is created, lower class particles are removed from particle list. Average
    velocity and position of smaller particles calculated and applied to new
    particle.

    Uses ```average_position``` and ```average_speed```.

    '''
    for p in particle_list:
        if p in particles:
            particles.remove(p)
    
    # spawn particle at average position
    avg_pos = average_position(particle_list)
    avg_vel = average_speed(particle_list)
    spawn_particle(new_type, avg_pos, particles, velocity_param=avg_vel)

# try quark fusion
def try_fusion(particles:list) -> None:
    '''
    Try forming mesons and hadrons from quark groups and pairs taken from
    ```find_quark_groups``` and ```find_quark_pairs```. Loop through groups and
    attempt hadron and meson fusion for each group.

    Uses ```find_quark_groups```, ```try_hadron_fusion```, ```find_quark_pairs``` and ```try_meson_fusion```.

    '''
    # use helper method
    groups = find_quark_groups(particles)

    # loop through list
    for group in groups:
        types = [p.type_name for p in group]
        # if valid combos, form a composite particle
        try_hadron_fusion(particles, 'Up Quark', 'Down Quark', 'Proton', group, types)
        try_hadron_fusion(particles, 'Down Quark', 'Up Quark', 'Neutron', group, types)
        try_hadron_fusion(particles, 'Up Antiquark', 'Down Antiquark', 'Antiproton', group, types)
        try_hadron_fusion(particles, 'Down Antiquark', 'Up Antiquark', 'Antineutron', group, types)

        try_triplet_fusion(particles, 'Up Quark', 'Strange Quark', 'Down Quark', 'Lambda Baryon', group, types)
        try_triplet_fusion(particles, 'Up Antiquark', 'Strange Antiquark', 'Down Antiquark', 'Lambda Antibaryon', group, types)

        try_triple_fusion(particles, 'Strange Quark', 'Omega Baryon', group, types)
        try_triple_fusion(particles, 'Strange Antiquark', 'Omega Antibaryon', group, types)

    groups = find_quark_pairs(particles)

    for group in groups:
        types = [p.type_name for p in group]

        try_meson_fusion(particles, 'Up Quark', 'Down Antiquark', 'Pion+', group, types)
        try_meson_fusion(particles, 'Down Quark', 'Up Antiquark', 'Pion-', group, types)
        try_meson_fusion(particles, 'Up Quark', 'Up Antiquark', 'Pion0', group, types) 
        try_meson_fusion(particles, 'Down Quark', 'Down Antiquark', 'Pion0', group, types)

        try_meson_fusion(particles, 'Up Quark', 'Strange Antiquark', 'Kaon+', group, types)
        try_meson_fusion(particles, 'Strange Quark', 'Up Antiquark', 'Kaon-', group, types)
        try_meson_fusion(particles, 'Down Quark', 'Strange Antiquark', 'Kaon0', group, types)


# try to form composite particles
def try_hadron_fusion(particles:list, q1:str, q2:str, composite:str, group:list, types:list) -> None:
    '''
    Try creating a hadron (type ```composite```) from 2 particles of type ```q1``` 
    and 1 of type ```q2```.

    Uses ```form_composite```.

    '''
    if types.count(q1) == 2 and types.count(q2) == 1: form_composite(group, composite, particles)

def try_triple_fusion(particles:list, q1:str, composite:str, group:list, types:list) -> None:
    '''
    Try creating a hadron (type ```composite```) from 3 particles of type ```q1```.

    Uses ```form_composite```.

    '''
    if types.count(q1) == 3: form_composite(group, composite, particles)

def try_meson_fusion(particles:list, q1:str, q2:str, composite:str, group:list, types:list) -> None:
    '''
    Try creating a meson (type ```composite```) from 1 particle of type ```q1``` 
    and 1 of type ```q2```.

    Uses ```form_composite```.

    '''
    if types.count(q1) == 1 and types.count(q2) == 1: form_composite(group, composite, particles)

def try_triplet_fusion(particles:list, q1:str, q2:str, q3:str, composite:str, group:list, types:list) -> None:
    '''
    Try creating a meson (type ```composite```) from 1 particle of type ```q1``` 
    and 1 of type ```q2``` and 1 of type ```q3```.

    Uses ```form_composite```.

    '''
    if types.count(q1) == 1 and types.count(q2) == 1 and types.count(q3) == 1: form_composite(group, composite, particles)

# apply strong force from quantum chromodynamics
def apply_quark_attraction(particles:list) -> None:
    '''
    Apply the strong nuclear force to quarks, attract other quarks within 
    a distance of 255 px. 

    '''
    # list of quarks
    quarks = [p for p in particles if p.type_name in QUARK_LIST]

    # loop list
    for i in range(len(quarks)):
        for j in range(i+1, len(quarks)):
            # get particles
            p1 = quarks[i]
            p2 = quarks[j]

            # determine distance between 2 particles
            dx = p2.position[0] - p1.position[0]
            dy = p2.position[1] - p1.position[1]
            dist = math.hypot(dx, dy)

            # if distance is far enough apply attraction
            if 10 < dist < 255: # <---
                # attraction is greater the farther particles are apart
                strength = 200 / dist
                angle = math.atan2(dy, dx)
                fx = math.cos(angle) * strength
                fy = math.sin(angle) * strength
                p1.velocity[0] += (fx * 2) * 3#(dist / 25)
                p1.velocity[1] += (fy * 2) * 3#(dist / 25)
                p2.velocity[0] -= (fx * 2) * 3#(dist / 25)
                p2.velocity[1] -= (fy * 2) * 3#(dist / 25)

# draw gluon bosons between quarks when close
def draw_gluons(surface:pygame.Surface, particles:list) -> None:
    '''
    Draw gluons between quarks when strong force acts upon them.
    Further apart = more translucent gluons.
    
    '''
    # create a surface for gluon
    temp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    temp_surf.fill((0, 0, 0, 0))  # Clear the surface with transparency

    # get a list of quarks and loop through them
    quarks = [p for p in particles if p.type_name in QUARK_LIST]
    for i in range(len(quarks)):
        for j in range(i+1, len(quarks)):
            # get variables for quarks and find distance
            p1 = quarks[i]
            p2 = quarks[j]
            dist = math.hypot(p1.position[0] - p2.position[0], p1.position[1] - p2.position[1])

            # check if particles are close enough, then draw gluon
            if dist < 255:
                alpha = max(0, 255 - int(dist * 1))
                gluon_color = (255, 100, 255, alpha)
                pygame.draw.line(temp_surf, gluon_color, p1.position, p2.position, 2)

    # draw all gluons
    surface.blit(temp_surf, (0, 0))

def relative_velocity(p1:Particle, p2:Particle) -> list[float, float]:
    return math.hypot(p1.position[0] - p2.position[0], p1.position[1] - p2.position[1])

# form an atom from an amount of nucleons and electrons
def form_atom(protons:list, neutrons:list, electrons:list, particles:list, name:str='Unknown', color:str='#FFFFFF') -> None:
    '''
    Create a new ```Nucleus``` object from a list of protons, neutrons,
    electrons. Apply orbit logic to selected electrons.
    
    '''
    # prepare
    atom_pos = average_position(protons + neutrons)
    nucleus = Nucleus(protons, neutrons, atom_pos, name=name, color=color)
    particles.append(nucleus)

    # remove nucleons from particle list
    for p in protons + neutrons:
        particles.remove(p)

    # loop through electrons
    for e in electrons:
        if e in particles:
            # set an electron orbiting at a random angle and radius
            e.orbiting = nucleus
            angle = random.uniform(0, 2 * math.pi)
            radius = nucleus.radius + random.uniform(30, 50)
            e.orbit_angle = angle
            e.orbit_radius = radius

            # set position
            e.position[0] = nucleus.position[0] + math.cos(angle) * radius
            e.position[1] = nucleus.position[1] + math.sin(angle) * radius

# attempt to form atoms
def try_form_atoms(particles:list) -> None:
    '''
    Loop through nucleons and check nearby required particles (protons,
    electrons and neutrons) to see if they can form a valid atom, specified
    in the dictionary from json data.

    Dynamically fetch data on the atom including ```charge```, ```name```, ```neutrons``` from
    the json dictionary.

    If requirements are met, use the ```form_atom()``` method to create a new atom
    with appropriate values.
    
    '''

    # lists of particles
    protons = [p for p in particles if p.type_name == 'Proton']
    neutrons = [p for p in particles if p.type_name == 'Neutron']
    electrons = [p for p in particles if p.type_name == 'Electron']

    used_particles = set()

    # loop particles
    for particle in particles:
        # skip unneccessary particles
        if particle.type_name not in ['Proton', 'Neutron'] or id(particle) in used_particles:
            continue

        # find nearby nucleons
        nearby_protons = [p for p in protons if id(p) not in used_particles and 
                          math.hypot(p.position[0] - particle.position[0], p.position[1] - particle.position[1]) < 50]
        nearby_neutrons = [n for n in neutrons if id(n) not in used_particles and
                            math.hypot(n.position[0] - particle.position[0], n.position[1] - particle.position[1]) < 50]
        
        # if there are no protons, skip iteration
        if not nearby_protons:
            continue

        # find nearby electrons
        atom_center = average_position(nearby_protons + nearby_neutrons)
        nearby_electrons = [
            e for e in electrons 
            if id(e) not in used_particles and e.orbiting is None and
            math.hypot(e.position[0] - atom_center[0], e.position[1] - atom_center[1]) < 50 and
            random.random() < max(0, 1 - relative_velocity(particle, e) / 100)
        ]
        
        # get number of protons and electrons
        proton_count = len(nearby_protons)
        electron_count = len(nearby_electrons)
        neutron_count = len(nearby_neutrons)

        # helper variables
        matched_element = None
        color = (255, 255, 255) # ts pmo
        
        # loop through elements and check if they match the proton and electron count
        for data in ELEMENTS.values():
            if data.get('protons') == proton_count and data.get('electrons') == electron_count and \
                    abs(data.get('neutrons') - neutron_count) <= 2:
                
                
                # prepare variables
                matched_element = data['name']
                color = data.get('color')
                element = data.get('name')
                break

        # create atom if matched
        if matched_element:
            #print(f'Formed atom: {matched_element} (Z={proton_count}, e={electron_count})')
            form_atom(nearby_protons, nearby_neutrons, nearby_electrons, particles, name=element, color=color)
            used_particles.update([id(p) for p in nearby_protons + nearby_neutrons + nearby_electrons])

def apply_electromagnetic_forces(particles: list, k: int = 898.75517923) -> None:
    '''
    Apply electromagnetic forces between charged particles.
    Like charges repel, opposite charges attract.
    
    Parameters:
    - particles: List of particles in the simulation.
    - k: Coulomb constant (controls the strength of the force).

    '''
    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles):
            if i == j or p1.charge == 0 or p2.charge == 0:
                continue

            if isinstance(p1, Nucleus) or isinstance(p2, Nucleus):
                continue

            if p1.type_name in QUARK_LIST or p2.type_name in QUARK_LIST:
                continue

            if p1.orbiting is not None or p2.orbiting is not None:
                continue

            # Calculate the distance between the two particles
            dx = p2.position[0] - p1.position[0]
            dy = p2.position[1] - p1.position[1]
            distance = math.hypot(dx, dy)

            # Avoid division by zero or extremely small distances
            if distance < 1:
                distance = 1

            # Calculate the force magnitude using Coulomb's law
            force_magnitude = k * (p1.charge * p2.charge) / (distance ** 2)

            # Determine the direction of the force
            angle = math.atan2(dy, dx)
            fx = math.cos(angle) * abs(force_magnitude)
            fy = math.sin(angle) * abs(force_magnitude)

            # Apply the force to the particles
            if p1.charge * p2.charge > 0:  # Like charges (repel)
                p1.velocity[0] -= fx
                p1.velocity[1] -= fy
                p2.velocity[0] += fx
                p2.velocity[1] += fy
            else:  # Opposite charges (attract)
                p1.velocity[0] += fx
                p1.velocity[1] += fy
                p2.velocity[0] -= fx
                p2.velocity[1] -= fy

def annihilation_case(particles:list, pt1:str, pt2:str, remove:list, add:list) -> None:
    for p1 in particles:
        if p1.type_name != pt1:
            continue

        for p2 in particles:
            if p2.type_name == pt2:
                dx = p2.position[0] - p1.position[0]
                dy = p2.position[1] - p1.position[1]
                distance = math.sqrt(dx**2 + dy**2)

                if distance < 10:
                    remove.extend([p1, p2])

                    mid_x = (p1.position[0] + p2.position[0]) / 2
                    mid_y = (p1.position[1] + p2.position[1]) / 2

                    # create 2 photons at the midpoint
                    velocity = [random.uniform(5, 30), random.uniform(5, 30)]
                    photon1 = Particle('Photon', [mid_x, mid_y], [velocity[0]*2, velocity[1]*2])
                    photon2 = Particle('Photon', [mid_x, mid_y], [-velocity[0]*2, -velocity[1]*2])

                    add.extend([photon1, photon2])
                    break


def handle_annihilations(particles:list) -> None:
    to_remove = []
    to_add = []

    annihilation_case(particles, 'Electron', 'Positron', to_remove, to_add)
    annihilation_case(particles, 'Pion+', 'Pion-', to_remove, to_add)

    for p in to_remove:
        if p in particles:
            particles.remove(p)

    particles.extend(to_add)

# decay functions
def decay_particles(particles:list) -> None:
    '''
    Handle all types of particle decay in the simulation.

    '''
    beta_minus_decay(particles)
    beta_plus_decay(particles)
    muon_decay(particles)
    tau_decay(particles)
    lamba_decay(particles)

# β⁻ decay
def beta_minus_decay(particles:list) -> None:
    '''
    Handle beta minus decay of a neutron into a proton, electron and antineutrino.
    '''
    for p in particles:
        if p.type_name == 'Neutron' and p.age > p.decay_age and random.random() < 0.5:
            # create a proton, electron and antineutrino
            neutron_pos = p.position
            neutron_vel = p.velocity
            particles.remove(p)

            # create new particles
            spawn_particle('Proton', copy.deepcopy(neutron_pos), particles, [copy.deepcopy(neutron_vel[0]) + random.uniform(-10, 50), copy.deepcopy(neutron_vel[1]) + random.uniform(-10, 50)])
            spawn_particle('Electron', copy.deepcopy(neutron_pos), particles, [copy.deepcopy(neutron_vel[0]) + random.uniform(-10, 50), copy.deepcopy(neutron_vel[1]) + random.uniform(-10, 50)])
            spawn_particle('Electron Antineutrino', copy.deepcopy(neutron_pos), particles, [copy.deepcopy(neutron_vel[0]) + random.uniform(-10, 50), copy.deepcopy(neutron_vel[1]) + random.uniform(-10, 50)])

# β⁺ decay
def beta_plus_decay(particles:list) -> None:
    '''
    Handle beta plus decay of a proton into a neutron, positron and neutrino.
    '''
    for p in particles:
        # check for proton decay
        if p.type_name == 'Proton' and 1 == 2:
            pos = p.position[:]
            vel = p.velocity[:]
            particles.remove(p)

            # create decay products with some slight variation in velocity
            spawn_particle('Neutron', copy.deepcopy(pos), particles, [copy.deepcopy(vel[0]) + random.uniform(-10, 10), copy.deepcopy(vel[1]) + random.uniform(-10, 10)])
            spawn_particle('Positron', copy.deepcopy(pos), particles, [random.uniform(-50, 50), random.uniform(-50, 50)])
            spawn_particle('Electron Neutrino', copy.deepcopy(pos), particles, [random.uniform(-50, 50), random.uniform(-50, 50)])

# μ decay
def muon_decay(particles: list) -> None:
    '''
    Handle the decay of a muon into a positron, electron neutrino, and muon antineutrino.
    '''
    for p in particles:
        if p.type_name == 'Muon' and p.age > p.decay_age and random.random() < 0.5:
            # Get the position of the muon
            muon_pos = p.position
            muon_vel = p.velocity
            particles.remove(p)

            # Create the decay products with some slight variation in velocity
            spawn_particle('Positron', copy.deepcopy(muon_pos), particles, [copy.deepcopy(muon_vel[0]) + random.uniform(-10, 50), copy.deepcopy(muon_vel[1]) + random.uniform(-10, 50)])
            spawn_particle('Electron Neutrino', copy.deepcopy(muon_pos), particles, [copy.deepcopy(muon_vel[0]) + random.uniform(-10, 50), copy.deepcopy(muon_vel[1]) + random.uniform(-10, 50)])
            spawn_particle('Muon Antineutrino', copy.deepcopy(muon_pos), particles, [copy.deepcopy(muon_vel[0]) + random.uniform(-10, 50), copy.deepcopy(muon_vel[1]) + random.uniform(-10, 50)])

# τ decay
def tau_decay(particles: list) -> None:
    '''
    Handle the decay of a tau lepton into various possible decay products.
    '''
    for p in particles[:]:
        if p.type_name == 'Tau' and p.age > p.decay_age and random.random() < 0.5:
            pos = p.position
            particles.remove(p)

            # choose a decay mode randomly based on the given probabilities
            # 18% for Electron, 17% for Muon, 65% for Pion
            decay_mode = random.choices(
                ['Electron', 'Muon', 'Pion'],
                weights=[0.18, 0.17, 0.65],
                k=1
            )[0]

            # Create the decay products based on the chosen decay mode
            if decay_mode == 'Electron':
                spawn_particle('Electron', copy.deepcopy(pos), particles, [random.uniform(-50, 50), random.uniform(-50, 50)])
                spawn_particle('Electron Neutrino', copy.deepcopy(pos), particles, [random.uniform(-50, 50), random.uniform(-50, 50)])
                spawn_particle('Tau Antineutrino', copy.deepcopy(pos), particles, [random.uniform(-50, 50), random.uniform(-50, 50)])
            elif decay_mode == 'Muon':
                spawn_particle('Muon', copy.deepcopy(pos), particles, [random.uniform(-50, 50), random.uniform(-50, 50)])
                spawn_particle('Muon Neutrino', copy.deepcopy(pos), particles, [random.uniform(-50, 50), random.uniform(-50, 50)])
                spawn_particle('Tau Antineutrino', copy.deepcopy(pos), particles, [random.uniform(-50, 50), random.uniform(-50, 50)])
            elif decay_mode == 'Pion':
                spawn_particle('Pion-', copy.deepcopy(pos), particles, [random.uniform(-50, 50), random.uniform(-50, 50)])
                spawn_particle('Tau Neutrino', copy.deepcopy(pos), particles, [random.uniform(-50, 50), random.uniform(-50, 50)])

# Λ decay
def lamba_decay(particles: list) -> None:
    '''
    Handle the multiple decay modes of the Lambda baryon (Λ) into various particles.

    '''
    for p in particles:
        if p.type_name == 'Lambda Baryon' and p.age > p.decay_age and random.random() < 0.5:
            pos = p.position
            vel = p.velocity
            particles.remove(p)

            decay_mode = random.choices(
                ['Proton', 'Neutron'],
                weights=[0.64, 0.36],
                k=1
            )[0]

            #pos_offset = pos

            pos_offset = [random.randint(-20, 20), random.randint(-20, 20)]

            if decay_mode == 'Proton':
                spawn_particle('Proton', [pos[0] + pos_offset[0], pos[1] + pos_offset[1]], particles, [copy.deepcopy(vel[0]) + pos_offset[0]*2, copy.deepcopy(vel[1]) + pos_offset[1]*2])
                spawn_particle('Pion-', [pos[0] - pos_offset[1], pos[1] - pos_offset[1]], particles, [copy.deepcopy(vel[0]) + pos_offset[0]*2, copy.deepcopy(vel[1]) - pos_offset[1]*2])
            elif decay_mode == 'Neutron':
                spawn_particle('Neutron', [pos[0] + pos_offset[0], pos[1] + pos_offset[1]], particles, [copy.deepcopy(vel[0]) + pos_offset[0]*2, copy.deepcopy(vel[1]) + pos_offset[1]*2])
                spawn_particle('Pion0', [pos[0] - pos_offset[0], pos[1] - pos_offset[1]], particles, [copy.deepcopy(vel[0]) - pos_offset[0]*2, copy.deepcopy(vel[1]) - pos_offset[1]*2])

# collision functions
def collision_of(p1:Particle, p2:Particle, threshold:float) -> bool:
    dx = p1.position[0] - p2.position[0]
    dy = p1.position[1] - p2.position[1]
    dist = math.hypot(dx, dy)
    return threshold >= dist

def handle_collisions(particles:list) -> None:
    to_remove = []
    to_add = []
    
    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles):
            if i == j or p1 in to_remove or p2 in to_remove:
                continue

            if collision_of(p1, p2, 20):

                pair = {p1.type_name, p2.type_name}
                if pair == {'Proton', 'Pion-'} or pair == {'Pion-', 'Proton'}:
                    avg_energy = (p1.energy + p2.energy) / 2

                    #if avg_energy > 10:
                    #    p1.velocity, p2.velocity = copy.deepcopy(p2.velocity), copy.deepcopy(p1.velocity)
                    #else:
                    if True:
                        # Charge exchange: remove old particles, add new ones
                        to_remove.append(p1)
                        to_remove.append(p2)

                        proton = p1 if p1.type_name == 'Proton' else p2
                        pion = p1 if 'Pion' in p1.type_name else p2

                        new_nucleon = 'Neutron'
                        new_pion = 'Pion0'

                        to_add.append(Particle(new_nucleon, proton.position[:], proton.velocity[:]))
                        to_add.append(Particle(new_pion, pion.position[:], pion.velocity[:]))

                if pair == {'Pion+', 'Neutron'} or pair == {'Neutron', 'Pion+'}:
                    to_remove.append(p1)
                    to_remove.append(p2)

                    neutron = p1 if p1.type_name == 'neutron' else p2
                    pion = p1 if 'Pion' in p1.type_name else p2

                    new_nucleon = 'Proton'
                    new_pion = 'Pion0'

                    to_add.append(Particle(new_nucleon, neutron.position[:], neutron.velocity[:]))
                    to_add.append(Particle(new_pion, pion.position[:], pion.velocity[:]))

                if pair == {'Kaon+', 'Neutron'} or pair == {'Neutron', 'Kaon+'}:
                    to_remove.append(p1)
                    to_remove.append(p2)

                    neutron = p1 if p1.type_name == 'Neutron' else p2
                    kaon = p1 if 'Kaon' in p1.type_name else p2

                    new_nucleon = 'Lambda Baryon'
                    new_pion = 'Pion+'

                    to_add.append(Particle(new_nucleon, neutron.position[:], neutron.velocity[:]))
                    to_add.append(Particle(new_pion, kaon.position[:], kaon.velocity[:]))

                if pair == {'Muon', 'Electron Neutrino'} or pair == {'Electron Neutrino', 'Muon'}:
                    to_remove.append(p1)
                    to_remove.append(p2)

                    muon = p1 if p1.type_name == 'Muon' else p2
                    neutrino = p1 if 'Neutrino' in p1.type_name else p2

                    new_electron = 'Electron'
                    new_neutrino = 'Muon Neutrino'

                    to_add.append(Particle(new_electron, muon.position[:], muon.velocity[:]))
                    to_add.append(Particle(new_neutrino, neutrino.position[:], neutrino.velocity[:]))

                if pair == {'Neutron', 'Electron'} or pair == {'Electron', 'Neutron'}:
                    to_remove.append(p1)
                    to_remove.append(p2)

                    electron = p1 if p1.type_name == 'Electron' else p2
                    neutron = p1 if p1.type_name == 'Neutron' else p2

                    to_add.append(Particle('Proton', neutron.position[:], neutron.velocity[:]))
                    to_add.append(Particle('Electron Neutrino', electron.position[:], electron.velocity[:]))


    for p in to_remove:
        if p in particles:
            particles.remove(p)

    particles.extend(to_add)

                    