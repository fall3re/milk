from CONFIG import D_Z,NUM_CELLS
import matplotlib.pyplot as plt
import numpy as np



def add_to_plot(ax, pos, vel):
    profile = np.zeros((NUM_CELLS, 1))
    for cell in range(NUM_CELLS):
        in_cell = (cell * D_Z < pos[2]) & (pos[2] < (cell + 1) * D_Z)
        profile[cell] = np.mean(vel[1][in_cell])

def plot_against_time(parameter, y1=None, y2=None):
    fig = plt.figure()
    plt.plot(parameter, label='Caption - Edit', color='black')
    if y1 is not None and y2 is not None:
        plt.ylim([y1, y2])
    plt.show()

def plot_results(y_velocity, y1=None, y2=None):
    figure = plt.plot(y_velocity)
    plt.xlabel(r'$Timestep \tau$')
    plt.ylabel(r'$Velocity v_y(z=0)$')
    if y1 is not None and y2 is not None:
        plt.ylim([y1, y2])
    plt.savefig('aaa.png', dpi=240)
    plt.show()
