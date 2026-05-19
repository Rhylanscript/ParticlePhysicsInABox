# Particle Physics in a Box

A Pygame-based interactive particle physics simulator that lets you spawn and experiment with fundamental particles, quarks, hadrons, mesons, bosons, and atomic nuclei.

## Overview

This simulation models particle dynamics inside a bounded box. It includes:

- Leptons, quarks, baryons, mesons, and bosons
- Electromagnetic interactions and quark attraction
- Particle decay, annihilation, collisions, and fusion logic
- Atom formation from protons, neutrons, and electrons
- Hover tooltips and an interactive side menu for spawning particles

## Features

- Spawn particles from several categories: Leptons, Quarks, Baryons, Mesons, and Bosons
- Simulate strong force behavior between quarks with gluon visuals
- Automatically form composite particles when quarks are close enough
- Electron orbiting behavior around atomic nuclei
- Decay processes for muons, taus, neutrons, lambda baryons, and unstable mesons
- Annihilation events for electron/positron and pion pairs

## Requirements

- Python 3.8+
- `pygame`

Install dependencies with:

```powershell
python -m pip install requirements.txt
```

## Run the Simulation

From the project root directory:

```powershell
python __main__.py
```

If you prefer module mode and your working directory is the project folder:

```powershell
python .
```

## Controls

- Use the left menu to select a particle category
- Click on a particle button to spawn it into the simulation area
- Click the colored control icons to pause/play, reset speed, or clear the field
- Use the `Delete` button to remove selected particles
- Hover over particles to reveal additional information

## Project Structure

- `__main__.py` - main simulation entry point
- `src/classes.py` - Particle and Nucleus classes with update/draw logic
- `src/constants.py` - particle definitions and window/menu constants
- `src/sim_util.py` - physics helpers, fusion, decay, annihilation, and collision logic
- `atom_recipes.json` - element data used for atom formation
- `assets/` - images and audio used by the simulation

## Notes

- The simulation is intended as an educational and experimental tool, not a precise physics engine.
- Particle masses, charges, decay timers, and behavior are simplified for interactive visualization.
- If the window does not appear, confirm that `pygame` is installed and that you are running the command from the correct project folder.
