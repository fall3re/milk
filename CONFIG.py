import numpy as np

### SIMULATION PARAMETERS

NUM_PARTICLES = 60000
NUM_SIMS = 1
NUM_CELLS = 2
NUM_MEAN_FREE_TIMES = 15
NUM_TIMESTEPS = NUM_MEAN_FREE_TIMES * 25

### WALL PARAMETERS

WALL_VELOCITY = 0.2
WALL_TEMPERATURE = 2

### CELL & GAS PARAMETERS

DENSITY = 0.005
AVG_FREE_PATH = 1 / (np.sqrt(2) * np.pi * DENSITY)
HEIGHT = 5 * AVG_FREE_PATH
AVG_SPEED = (2 / np.sqrt(np.pi)) * np.sqrt(2 * WALL_TEMPERATURE)

### DO NOT CHANGE - INTERNAL DEFINED VARIABLES

TIME = AVG_FREE_PATH / AVG_SPEED
D_T = NUM_MEAN_FREE_TIMES * TIME / NUM_TIMESTEPS
D_Z = HEIGHT / NUM_CELLS
CELL_VOLUME = D_Z ** 3
PARTICLES_PER_CELL = DENSITY * HEIGHT * D_Z * D_Z / NUM_PARTICLES
