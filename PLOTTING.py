from CONFIG import D_Z,NUM_CELLS, NUM_TIMESTEPS, WALL_VELOCITY, D_T, TIME, NUM_MEAN_FREE_TIMES
import matplotlib.pyplot as plt
import numpy as np
from scipy import special


def add_to_plot(ax, pos, vel):
    profile = np.zeros((NUM_CELLS, 1))
    for cell in range(NUM_CELLS):
        in_cell = (cell * D_Z < pos[2]) & (pos[2] < (cell + 1) * D_Z)
        profile[cell] = np.mean(vel[1][in_cell])

def plot_against_time(parameter, y1=None, y2=None):
    fig = plt.figure(figsize=(6, 4), dpi=80)
    plt.plot(parameter, label='Caption - Edit', color='black')
    if y1 is not None and y2 is not None:
        plt.ylim([y1, y2])
    plt.show()

def plot_results(y_velocity):
    fig = plt.figure(figsize=(6, 4), dpi=80)
    ax = plt.gca()
    plt.xlabel(r'$Timestep \tau$')
    plt.ylabel(r'$Velocity v_y(z=0)$')
    ax.set(xlim=(0, NUM_MEAN_FREE_TIMES), ylim=(0.5, 1.1))
    ax.legend(loc='upper left')
    plt.savefig('dsmc.png', dpi=240)
    plt.show()
