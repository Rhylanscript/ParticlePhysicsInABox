'''
This file contains a list of constants used in the simulation, including
lists of particle types and menu values.

'''

# particle definitions
PARTICLE_TYPES = {
    'Electron': {'mass': 9.11e-31, 'charge': -1, 'color': (0, 0, 255), 'radius': 6, 'decay-timer': None},
    'Muon': {'mass': 1.88e-28, 'charge': -1, 'color': (150, 255, 150), 'radius': 6, 'decay-timer': 1.56e-6},
    'Tau': {'mass': 3.17e-27, 'charge': -1, 'color': (255, 233, 0), 'radius': 6, 'decay-timer': 2.9e-13},
    'Electron Neutrino': {'mass': 1.0e-37, 'charge': 0, 'color': (150, 150, 255), 'radius': 4, 'decay-timer': None},
    'Muon Neutrino': {'mass': 1.0e-37, 'charge': 0, 'color': (180, 200, 200), 'radius': 4, 'decay-timer': None},
    'Tau Neutrino': {'mass': 1.0e-37, 'charge': 0, 'color': (200, 200, 255), 'radius': 4, 'decay-timer': None},
    'Positron': {'mass': 9.11e-31, 'charge': +1, 'color': (190, 0, 100), 'radius': 6, 'decay-timer': None},
    'Antimuon': {'mass': 1.88e-28, 'charge': +1, 'color': (50, 0, 70), 'radius': 6, 'decay-timer': 1.56e-6},
    'Antitau': {'mass': 3.17e-27, 'charge': +1, 'color': (50, 25, 50), 'radius': 6, 'decay-timer': 2.9e-13},
    'Electron Antineutrino': {'mass': 1.0e-37, 'charge': 0, 'color': (150, 150, 255), 'radius': 4, 'decay-timer': None},
    'Muon Antineutrino': {'mass': 1.0e-37, 'charge': 0, 'color': (180, 200, 200), 'radius': 4, 'decay-timer': None},
    'Tau Antineutrino': {'mass': 1.0e-37, 'charge': 0, 'color': (200, 200, 255), 'radius': 4, 'decay-timer': None},

    'Up Quark': {'mass': 2.2e-30, 'charge': 2/3, 'color': (255, 0, 0), 'radius': 6, 'decay-timer': None},
    'Down Quark': {'mass': 4.7e-30, 'charge': -1/3, 'color': (0, 0, 255), 'radius': 6, 'decay-timer': None},
    'Strange Quark': {'mass': 1.4e-36, 'charge': -1/3, 'color': (0, 255, 0), 'radius': 7, 'decay-timer': 1.24e-8},
    'Charm Quark': {'mass': 2.28e-36, 'charge': 2/3, 'color': (180, 180, 0), 'radius': 7, 'decay-timer': 1.1e-12},
    'Up Antiquark': {'mass': 2.2e-30, 'charge': -2/3, 'color': (0, 150, 100), 'radius': 6, 'decay-timer': None},
    'Down Antiquark': {'mass': 4.7e-30, 'charge': 1/3, 'color': (255, 130, 30), 'radius': 6, 'decay-timer': None},
    'Strange Antiquark': {'mass': 4.8e-30, 'charge': 1/3, 'color': (0, 120, 0), 'radius': 7, 'decay-timer': 1.24e-8},
    'Charm Antiquark': {'mass': 2.28e-36, 'charge': -2/3, 'color': (80, 80, 0), 'radius': 7, 'decay-timer': 1.1e-12},

    'Proton': {'mass': 1.67e-27, 'charge': 1, 'color': (255, 100, 100), 'radius': 12, 'decay-timer': None},
    'Neutron': {'mass': 1.67e-27, 'charge': 0, 'color': (100, 100, 255), 'radius': 12, 'decay-timer': 611.0},
    'Antiproton': {'mass': 1.67e-27, 'charge': -1, 'color': (150, 70, 70), 'radius': 12, 'decay-timer': None},
    'Antineutron': {'mass': 1.67e-27, 'charge': 0, 'color': (0, 50, 150), 'radius': 12, 'decay-timer': 611.0},
    'Lambda Baryon': {'mass': 1.12e-27, 'charge': 0, 'color': (150, 50, 225), 'radius': 13, 'decay-timer': 2.63e-10},
    'Lambda Antibaryon': {'mass': 1.12e-27, 'charge': 0, 'color': (100, 0, 150), 'radius': 13, 'decay-timer': 2.63e-10},
    'Omega Baryon': {'mass': 2.98e-27, 'charge': -1, 'color': (255, 255, 255), 'radius': 14, 'decay-timer': 8.21e-11},
    'Omega Antibaryon': {'mass': 2.98e-27, 'charge': 1, 'color': (100, 100, 100), 'radius': 14, 'decay-timer': 8.21e-11},

    'Pion+': {'mass': 1.39e-28, 'charge': 1, 'color': (200, 100, 255), 'radius': 10, 'decay-timer': 2.6e-8},
    'Pion-': {'mass': 1.39e-28, 'charge': -1, 'color': (200, 100, 255), 'radius': 10, 'decay-timer': 2.6e-8},
    'Pion0': {'mass': 1.39e-28, 'charge': 0, 'color': (200, 100, 255), 'radius': 10, 'decay-timer': 8.4e-17},
    'Kaon+': {'mass': 8.80e-28, 'charge': 1, 'color': (255, 200, 0), 'radius': 10, 'decay-timer': 5.18e-8},
    'Kaon-': {'mass': 8.80e-28, 'charge': -1, 'color': (255, 200, 0), 'radius': 10, 'decay-timer': 1.24e-8},
    'Kaon0': {'mass': 8.80e-28, 'charge': 0, 'color': (255, 200, 0), 'radius': 10, 'decay-timer': 1.24e-8},

    'W+ Boson': {'mass': 5.83e-10, 'charge': 1, 'color': (200, 200, 200), 'radius': 8, 'decay-timer': 3.0e-25},
    'W- Boson': {'mass': 5.83e-10, 'charge': -1, 'color': (200, 200, 200), 'radius': 8, 'decay-timer': 3.0e-25},
    'Z Boson': {'mass': 9.12e-10, 'charge': 0, 'color': (100, 125, 175), 'radius': 8, 'decay-timer': 3.0e-25},
    'Photon': {'mass': 0, 'charge': 0, 'color': (255, 255, 0), 'radius': 2, 'decay-timer': None},
    'Gluon': {'mass': 0, 'charge': 0, 'color': (255, 255, 255), 'radius': 2, 'decay-timer': None},

    'Higgs Boson': {'mass': 2.2e-25, 'charge': 0, 'color': (225, 200, 200), 'radius': 8, 'decay-timer': 1.6e-22}, #scary ahhhh
}
'''
Dictionary containing all particles and their ```mass```, ```charge```
and ```color``` used in the simulation

'''

TOOLTIP_LENGTHS  = {
    'Pause': 60,
    'Play': 45,
    'Slow Down': 97,
    'Speed Up': 86,
    'Reset Speed': 108,
    'Clear': 55
} 
'''
The appropriate lengths of the tooltips for each IconButton in the
simulation workspace.

'''

# lists
QUARK_LIST = ['Up Quark', 'Down Quark', 'Strange Quark', 'Charm Quark', 'Up Antiquark', 'Down Antiquark', 'Strange Antiquark', 'Charm Antiquark']
'''List of all quark types used in the simulation.'''
HADRON_LIST = ['Proton', 'Neutron', 'Antiproton', 'Antineutron', 'Lambda Baryon']
'''List of all hadron types used in the simulation.'''
MESON_LIST = ['Pion0', 'Pion+', 'Pion-', 'Kaon0', 'Kaon+', 'Kaon-']
'''List of all meson types used in the simulation.'''
#PARTICLE_LIST = ['Electron', 'Positron', 'Up Quark', 'Down Quark', 'Up Antiquark', 'Down Antiquark', 'Proton', 'Neutron']
'''List of all particle types used in the simulation.'''

# setup game constants
WIDTH, HEIGHT = 1000, 600
'''Width and height of the simulation window.'''
MENU_WIDTH = 250
'''Width of the menu on the left side of the simulation window.'''
SIM_WIDTH = WIDTH - MENU_WIDTH
'''Width of the simulation area.'''

MAX_MENU_SCROLL = 500
'''Maximum scroll distance of the menu.'''
SCROLL_SPEED = 10
'''Speed of the menu scroll.'''