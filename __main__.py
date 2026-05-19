'''
Particle Physics simulation developed by Rhylan Marsh. Check attached README.md
for more information on this project.

--------------------------------------------------------------------------------

Particle Physics in a Box
Version: 2.1

'''

# import externals
import pygame

# import locals
from src.classes import Particle, Nucleus
from src.buttons import TextButton, IconButton
from src.constants import MENU_WIDTH, WIDTH, HEIGHT, MAX_MENU_SCROLL, SCROLL_SPEED
from src.sim_util import spawn_particle, try_fusion, try_form_atoms, \
    apply_quark_attraction, draw_gluons, apply_electromagnetic_forces, \
    handle_annihilations, decay_particles, handle_collisions

# initialize pygame
pygame.init()

# initialise pygame assets
screen = pygame.display.set_mode((WIDTH, HEIGHT))
'''The simulation window.'''
pygame.display.set_caption("Particle Physics in a Box")

font = pygame.font.SysFont(None, 24)
'''Default pygame font, size 24.'''

clock = pygame.time.Clock()
'''Pygame clock for controlling frame rate.'''

# helper variables
particles = []
'''List of particles in the simulation.'''
selected_particle = None 
'''The currently selected particle.'''

# simulation control settings
simulation_speed = 1.0
'''The speed of the simulation.'''
paused = False
'''The paused status of the simulation.'''

# GUI Buttons
button_width = MENU_WIDTH - 50
'''Button width for menu buttons.'''

# mini method to set selected particle
def setparticle(particle_name:str) -> None:
    '''Set the selected_particle with a set value.'''
    global selected_particle
    selected_particle = particle_name

# menu buttons
btn_electron = TextButton(pygame.Rect(10, 310, button_width, 50), 'Electron', lambda: setparticle('Electron'))
btn_muon = TextButton(pygame.Rect(10, 370, button_width, 50), 'Muon', lambda: setparticle('Muon'))
btn_tau = TextButton(pygame.Rect(10, 430, button_width, 50), 'Tau', lambda: setparticle('Tau'))
btn_e_neutrino = TextButton(pygame.Rect(10, 490, button_width, 50), 'Electron Neutrino', lambda: setparticle('Electron Neutrino'))
btn_m_neutrino = TextButton(pygame.Rect(10, 550, button_width, 50), 'Muon Neutrino', lambda: setparticle('Muon Neutrino'))
btn_t_neutrino = TextButton(pygame.Rect(10, 610, button_width, 50), 'Tau Neutrino', lambda: setparticle('Tau Neutrino'))
btn_positron = TextButton(pygame.Rect(10, 670, button_width, 50), 'Positron', lambda: setparticle('Positron'))
btn_antimuon = TextButton(pygame.Rect(10, 730, button_width, 50), 'Antimuon', lambda: setparticle('Antimuon'))
btn_antitau = TextButton(pygame.Rect(10, 790, button_width, 50), 'Antitau', lambda: setparticle('Antitau'))
btn_e_antineutrino = TextButton(pygame.Rect(10, 850, button_width, 50), 'Electron Antineutrino', lambda: setparticle('Electron Antineutrino'))
btn_m_antineutrino = TextButton(pygame.Rect(10, 910, button_width, 50), 'Muon Antineutrino', lambda: setparticle('Muon Antineutrino'))
btn_t_antineutrino = TextButton(pygame.Rect(10, 970, button_width, 50), 'Tau Antineutrino', lambda: setparticle('Tau Antineutrino'))

btn_up_quark = TextButton(pygame.Rect(10, 310, button_width, 50), 'Up Quark', lambda: setparticle('Up Quark'))
btn_down_quark = TextButton(pygame.Rect(10, 370, button_width, 50), 'Down Quark', lambda: setparticle('Down Quark'))
btn_strange_quark = TextButton(pygame.Rect(10, 430, button_width, 50), 'Strange Quark', lambda: setparticle('Strange Quark'))
btn_charm_quark = TextButton(pygame.Rect(10, 490, button_width, 50), 'Charm Quark', lambda: setparticle('Charm Quark'))
btn_up_antiquark = TextButton(pygame.Rect(10, 550, button_width, 50), 'Up Antiquark', lambda: setparticle('Up Antiquark'))
btn_down_antiquark = TextButton(pygame.Rect(10, 610, button_width, 50), 'Down Antiquark', lambda: setparticle('Down Antiquark'))
btn_strange_antiquark = TextButton(pygame.Rect(10, 670, button_width, 50), 'Strange Antiquark', lambda: setparticle('Strange Antiquark'))
btn_charm_antiquark = TextButton(pygame.Rect(10, 730, button_width, 50), 'Charm Antiquark', lambda: setparticle('Charm Antiquark'))

btn_neutron = TextButton(pygame.Rect(10, 310, button_width, 50), 'Neutron', lambda: setparticle('Neutron'))
btn_proton = TextButton(pygame.Rect(10, 370, button_width, 50), 'Proton', lambda: setparticle('Proton'))
btn_antineutron = TextButton(pygame.Rect(10, 430, button_width, 50), 'Antineutron', lambda: setparticle('Antineutron'))
btn_antiproton = TextButton(pygame.Rect(10, 490, button_width, 50), 'Antiproton', lambda: setparticle('Antiproton'))
btn_lambda_baryon = TextButton(pygame.Rect(10, 550, button_width, 50), 'Lambda Baryon', lambda: setparticle('Lambda Baryon'))
btn_lambda_antibaryon = TextButton(pygame.Rect(10, 610, button_width, 50), 'Lambda Antibaryon', lambda: setparticle('Lambda Antibaryon'))
btn_omega_baryon = TextButton(pygame.Rect(10, 670, button_width, 50), 'Omega Baryon', lambda: setparticle('Omega Baryon'))
btn_omega_antibaryon = TextButton(pygame.Rect(10, 730, button_width, 50), 'Omega Antibaryon', lambda: setparticle('Omega Antibaryon'))

btn_pion_plus = TextButton(pygame.Rect(10, 310, button_width, 50), 'Pion+', lambda: setparticle('Pion+'))
btn_pion_minus = TextButton(pygame.Rect(10, 370, button_width, 50), 'Pion-', lambda: setparticle('Pion-'))
btn_pion_zero = TextButton(pygame.Rect(10, 430, button_width, 50), 'Pion0', lambda: setparticle('Pion0'))
btn_kaon_plus = TextButton(pygame.Rect(10, 490, button_width, 50), 'Kaon+', lambda: setparticle('Kaon+'))
btn_kaon_minus = TextButton(pygame.Rect(10, 550, button_width, 50), 'Kaon-', lambda: setparticle('Kaon-'))
btn_kaon_zero = TextButton(pygame.Rect(10, 610, button_width, 50), 'Kaon0', lambda: setparticle('Kaon0'))

btn_w_plus_boson = TextButton(pygame.Rect(10, 310, button_width, 50), 'W+ Boson', lambda: setparticle('W+ Boson'))
btn_w_minus_boson = TextButton(pygame.Rect(10, 370, button_width, 50), 'W- Boson', lambda: setparticle('W- Boson'))
btn_z_boson = TextButton(pygame.Rect(10, 430, button_width, 50), 'Z Boson', lambda: setparticle('Z Boson'))
btn_photon = TextButton(pygame.Rect(10, 490, button_width, 50), 'Photon', lambda: setparticle('Photon'))
btn_gluon = TextButton(pygame.Rect(10, 550, button_width, 50), 'Gluon', lambda: setparticle('Gluon'))
btn_higgs_boson = TextButton(pygame.Rect(10, 610, button_width, 50), 'Higgs Boson', lambda: setparticle('Higgs Boson'))

# delete button
btn_delete = TextButton(pygame.Rect(10, HEIGHT - 60, MENU_WIDTH - 19, 50), 'Delete', lambda: setparticle('Delete'))
'''Delete button to remove particles from simulation.'''

# list of buttons
menu_buttons = [
    btn_electron, btn_muon, btn_tau, btn_e_neutrino, btn_m_neutrino, btn_t_neutrino, 
    btn_positron, btn_antimuon, btn_antitau, btn_e_antineutrino, btn_m_antineutrino, btn_t_antineutrino,

    btn_up_quark, btn_down_quark, btn_strange_quark, btn_charm_quark, btn_up_antiquark, btn_down_antiquark, 
    btn_strange_antiquark, btn_charm_antiquark,
    
    btn_neutron, btn_proton, btn_antineutron, btn_antiproton, btn_lambda_baryon, btn_lambda_antibaryon,
    btn_omega_baryon, btn_omega_antibaryon,

    btn_pion_minus, btn_pion_plus, btn_pion_zero,
    btn_kaon_plus, btn_kaon_minus, btn_kaon_zero,

    btn_w_plus_boson, btn_w_minus_boson,
    btn_z_boson, btn_photon, btn_gluon, btn_higgs_boson,

    btn_delete
]
'''List of all menu buttons.'''

# create a dictionary of categories and their buttons
categories = {
    'Baryons': [btn_neutron, btn_proton, btn_antineutron, btn_antiproton, btn_lambda_baryon, btn_lambda_antibaryon, btn_omega_baryon, btn_omega_antibaryon],
    'Mesons': [btn_pion_plus, btn_pion_minus, btn_pion_zero, btn_kaon_plus, btn_kaon_minus, btn_kaon_zero],
    'Leptons': [btn_electron, btn_muon, btn_tau, btn_e_neutrino, btn_m_neutrino, btn_t_neutrino, btn_positron, btn_antimuon, btn_antitau, btn_e_antineutrino, btn_m_antineutrino, btn_t_antineutrino],
    'Quarks': [btn_up_quark, btn_down_quark, btn_strange_quark, btn_charm_quark, btn_up_antiquark, btn_down_antiquark, btn_strange_antiquark, btn_charm_antiquark],
    'Bosons': [btn_w_plus_boson, btn_w_minus_boson, btn_z_boson, btn_photon, btn_gluon, btn_higgs_boson],
}
'''Dictionary of categories and the buttons in each.'''

# create a list of category buttons
category_buttons = [
    TextButton(pygame.Rect(10, 10, button_width, 50), 'Baryons', lambda: set_category('Baryons'), color=(0, 50, 150), selected_color=(0, 20, 100)),
    TextButton(pygame.Rect(10, 70, button_width, 50), 'Mesons', lambda: set_category('Mesons'), color=(0, 50, 150), selected_color=(0, 20, 100)),
    TextButton(pygame.Rect(10, 130, button_width, 50), 'Leptons', lambda: set_category('Leptons'), color=(0, 50, 150), selected_color=(0, 20, 100)),
    TextButton(pygame.Rect(10, 190, button_width, 50), 'Quarks', lambda: set_category('Quarks'), color=(0, 50, 150), selected_color=(0, 20, 100)),
    TextButton(pygame.Rect(10, 250, button_width, 50), 'Bosons', lambda: set_category('Bosons'), color=(0, 50, 150), selected_color=(0, 20, 100))
]
'''List of category buttons.'''

# set selected category to None
selected_category = None
'''The current category selected.'''

# method to set selected category
def set_category(category_name:str) -> None:
    '''Set the selected_category to the category_name value.'''
    global selected_category
    if selected_category == category_name:
        selected_category = None
    else:
        selected_category = category_name

# simulation settings button
button_radius = 50
'''Radius of the simulation settings buttons.'''

# load image icons for buttons
ff = pygame.image.load('assets/images/btn-ff.png')
pause = pygame.image.load('assets/images/btn-pause.png')
play = pygame.image.load('assets/images/btn-play.png')
reset = pygame.image.load('assets/images/btn-reset.png')
clear = pygame.image.load('assets/images/btn-clear.png')

# scale images to fit buttons
ff_scale = pygame.transform.scale(ff, (button_radius//2, button_radius//2))
pause_scale = pygame.transform.scale(pause, (button_radius//2, button_radius//2))
play_scale = pygame.transform.scale(play, (button_radius//2, button_radius//2))
reset_scale = pygame.transform.scale(reset, (button_radius//1.2, button_radius//1.2))
clear_scale = pygame.transform.scale(clear, (button_radius//1.4, button_radius//1.4))

# settings buttons
# functions for simulation settings buttons
# toggle paused var
def pause_play() -> None:
    '''Toggle the 'paused' bool.'''
    global paused
    paused = not paused

# clear simulation
def clear_simulation() -> None:
    '''Reset the simulation variables.'''
    global simulation_speed, paused, particles, selected_particle
    set_speed(1.0)
    paused = False
    particles.clear()
    selected_particle = None

# set the sim speed var with a value
def set_speed(value:int) -> None:
    '''Set the simulation_speed to a value specified by the 'value' param.'''
    global simulation_speed
    simulation_speed = value

# set the y position of the buttons
y = HEIGHT - button_radius - 20

# create buttons
btn_slow_down = IconButton(pygame.Rect(MENU_WIDTH + 20, y, button_radius, button_radius), ff_scale, 'Slow Down', lambda: set_speed(max(simulation_speed / 2.0, 0.000001)))
btn_pause_play = IconButton(pygame.Rect(MENU_WIDTH + 30 + button_radius, y, button_radius, button_radius), pause_scale, 'Pause', pause_play)
btn_speed_up = IconButton(pygame.Rect(MENU_WIDTH + 40 + button_radius*2, y, button_radius, button_radius), pygame.transform.flip(ff_scale, True, False), 'Speed Up', lambda: set_speed(min(simulation_speed * 2.0, 128.0)))
btn_reset_speed = IconButton(pygame.Rect(MENU_WIDTH + 50 + button_radius*3, y, button_radius, button_radius), reset_scale, 'Reset Speed', lambda: set_speed(1.0))
btn_clear_simulation = IconButton(pygame.Rect(MENU_WIDTH + 60 + button_radius*4, y, button_radius, button_radius), clear_scale, 'Clear', clear_simulation)

# list of buttons
settings_buttons = [
    btn_slow_down, btn_pause_play, btn_speed_up, btn_reset_speed, btn_clear_simulation
]
'''List containing simulation control buttons.'''

# helper vars
running = True
'''Flag to keep simulation running.'''
menu_scroll = 0
'''Scroll position of the menu.'''

# Main Loop
while running:
    # update
    dt = clock.tick(240) / 1000
    screen.fill((10, 10, 10))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check left click
            if event.button == 1: 
                # check if mouse click was in menu
                if event.pos[0] < MENU_WIDTH:
                    # check category buttons
                    for btn in category_buttons:
                        if btn.check_click(event.pos): break
                    
                    # check buttons in selected category
                    if selected_category in categories:
                        for btn in categories[selected_category]:
                            if btn.check_click(event.pos): break

                    # check delete button
                    if btn_delete.check_click(event.pos): break

                # check if mouse click was in simulation area
                else:
                    # loop through sim settings buttons
                    for btn in settings_buttons:
                        if btn.check_click(event.pos): break

                    else:
                        # check if delete active, delete clicked particle
                        if selected_particle == 'Delete':
                            for p in particles:
                                if p.is_hovered(event.pos):
                                    particles.remove(p)
                                    break
                        # check if a particle is selected, spawn it
                        elif selected_particle:
                            spawn_particle(selected_particle, list(event.pos), particles)

            # right click to deselect particle
            elif event.button == 3: selected_particle = None
        
        elif event.type == pygame.MOUSEWHEEL:
            if pygame.mouse.get_pos()[0] < MENU_WIDTH:
                if event.y < 0:
                    if menu_scroll >= -MAX_MENU_SCROLL: menu_scroll -= SCROLL_SPEED
                if event.y > 0:
                    if menu_scroll <= -SCROLL_SPEED: menu_scroll += SCROLL_SPEED

    # get position of mouse and reset hover status
    mouse_pos = pygame.mouse.get_pos()
    hovered_particle = None

    # update simulation if not paused
    if not paused:
        # change simulation speed
        dt *= simulation_speed

        # update particles
        for p in particles:
            p.update(dt)

        # call helper functions
        try_fusion(particles)
        try_form_atoms(particles)
        apply_quark_attraction(particles)
        apply_electromagnetic_forces(particles)
        handle_annihilations(particles)

        # decay particles
        decay_particles(particles)
        handle_collisions(particles)

    # draw gluons
    draw_gluons(screen, particles)

    # Draw electron orbits
    for p in particles:
        if isinstance(p, Particle) and p.type_name == 'Electron' and p.orbiting:
            pygame.draw.circle(screen, (200, 200, 200), (int(p.orbiting.position[0]), int(p.orbiting.position[1])), int(p.orbit_radius), 1)

    # Draw particles and check hover status
    for p in particles:
        p.draw(screen)
        if p.is_hovered(mouse_pos):
            hovered_particle = p

    # Draw Menu Background
    pygame.draw.rect(screen, (30, 30, 30), (0, 0, MENU_WIDTH, HEIGHT))

    # draw category buttons
    for btn in category_buttons:
        btn.draw(screen, selected_category == btn.text, menu_scroll)

    # draw menu buttons
    if selected_category in categories:
        for btn in categories[selected_category]:
            btn.draw(screen, selected_particle == btn.text, menu_scroll)

    # draw delete button
    pygame.draw.rect(screen, (30, 30, 30), (0, HEIGHT - 70, MENU_WIDTH, 70))
    pygame.draw.line(screen, (100, 100, 100), (10, HEIGHT - 70), (MENU_WIDTH - 10, HEIGHT - 70), 4)
    btn_delete.draw(screen, selected_particle == btn_delete.text)

    # draw scroll bar display
    # large scroll
    pygame.draw.line(screen, (60, 60, 60), (MENU_WIDTH - 20, 7), (MENU_WIDTH - 20, HEIGHT - 83), 15)
    
    # calc pos of mini scroll
    scroll_range = HEIGHT - SCROLL_SPEED - 202
    if MAX_MENU_SCROLL != 0: scroll_position = int((menu_scroll / -MAX_MENU_SCROLL) * scroll_range)
    else: scroll_position = 0

    # get max for scroll pos
    scroll_position = max(10, min(scroll_position + 10, HEIGHT - 83))
    
    # mini scroll
    pygame.draw.line(screen, (100, 100, 100), (MENU_WIDTH - 20, scroll_position), (MENU_WIDTH - 20, scroll_position + 100), 7)

    # draw simulation settings buttons
    btn_pause_play.icon = play_scale if paused else pause_scale
    for btn in settings_buttons:
        btn.draw(screen)

    # Draw dividing line
    pygame.draw.line(screen, (100, 100, 100), (MENU_WIDTH, 0), (MENU_WIDTH, HEIGHT), 4)

    # draw simulation info text along top of screen
    # conditional based on 'paused' status
    status_text = f"{f'Paused ({simulation_speed:.6f}x)' if paused else f'Speed: {simulation_speed:.6f}x'}"
    status_surf = font.render(status_text, True, (255, 255, 255))
    screen.blit(status_surf, (MENU_WIDTH + 10, 10))

    # draw particle len
    particle_count_text = f"Particles: {len(particles)}"
    particle_count_surf = font.render(particle_count_text, True, (255, 255, 255))
    screen.blit(particle_count_surf, (MENU_WIDTH + 10, 40))

    # hover particle logic
    if hovered_particle:
        # nucleus hover
        if isinstance(hovered_particle, Nucleus):
            info_lines = [
                f"Type: {hovered_particle.name}",
                f"Protons: {len(hovered_particle.protons)}",
                f"Neutrons: {len(hovered_particle.neutrons)}",
                f"Charge: +{hovered_particle.charge} e",
            ]
            info_bg = pygame.Surface((220, 85))
        # particle hover
        else:
            info_lines = [
                f"Type: {hovered_particle.type_name}",
                f"Mass: {hovered_particle.mass:.2e} kg",
                f"Charge: {hovered_particle.charge} e",
                f"Velocity: {hovered_particle.velocity[0]:.2f}, {hovered_particle.velocity[1]:.2f} m/s",
                f"Energy: {hovered_particle.energy:.2f}"
                #f"Age: {hovered_particle.age:.2f} μs",
            ]
            info_bg = pygame.Surface((220, 100))

        # set a new surface for hover
        info_bg.set_alpha(180)
        info_bg.fill((30, 30, 30))

        tooltip_x = mouse_pos[0] + 10
        tooltip_y = mouse_pos[1] + 10

        if tooltip_x + info_bg.get_width() > WIDTH:
            tooltip_x = mouse_pos[0] - info_bg.get_width() - 10
        
        if tooltip_y + info_bg.get_height() > HEIGHT:
            tooltip_y = mouse_pos[1] - info_bg.get_height() - 10

        # draw surface and text onto surface
        screen.blit(info_bg, (tooltip_x, tooltip_y))
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (tooltip_x+15, tooltip_y+15 + i*20))
    else:
        # draw settings tooltips
        btn_pause_play.tooltip = 'Play' if paused else 'Pause'
        for btn in settings_buttons:
            btn.check_hover(mouse_pos, screen)

    # update display
    pygame.display.flip()

# quit pygame
pygame.quit()