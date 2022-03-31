from CONFIG import D_Z,NUM_CELLS, NUM_TIMESTEPS, WALL_VELOCITY, D_T, TIME, NUM_MEAN_FREE_TIMES
import matplotlib.pyplot as plt
import numpy as np
from scipy import special


def add_to_plot(ax, pos, vel):
    bin = D_Z * np.linspace(0.5, NUM_CELLS - 0.5, NUM_CELLS)
    profile = np.zeros((NUM_CELLS, 1))
    for cell in range(NUM_CELLS):
        in_cell = (cell * D_Z < pos[2]) & (pos[2] < (cell + 1) * D_Z)
        profile[cell] = np.mean(vel[1][in_cell])

def plot_pressure(pressure):
    fig = plt.figure(figsize=(6, 4), dpi=80)
    ax2 = plt.gca()
    plt.plot(pressure, label='Pressure on Specular Wall', color='black')
    plt.xlabel(r'$t/\tau$')
    plt.ylabel(r'$Pressure/Pa$')
    ax2.set(xlim=(0, NUM_MEAN_FREE_TIMES), ylim=(0.5, 1.1))
    ax2.legend(loc='upper left')
    plt.savefig('pressure.png', dpi=240)
    plt.show()

def plot_results(y_velocity):
    fig = plt.figure(figsize=(6, 4), dpi=80)
    ax2 = plt.gca()
    tt = D_T * np.linspace(1, NUM_TIMESTEPS, num=NUM_TIMESTEPS) / TIME
    bgk = np.zeros(tt.shape)
    for index in range(NUM_TIMESTEPS):
        xx = np.linspace(tt[index] / 10000, tt[index], num=10000)
        bgk[index] = 0.5 * (1 + np.trapz(np.exp(-xx) / xx * special.iv(1, xx), x=xx))
    plt.plot(tt * 2.5, bgk, label='BGK theory', color='red')
    plt.plot(tt, np.mean(y_velocity, axis=0).reshape((NUM_TIMESTEPS, 1)) / WALL_VELOCITY, label='DSMC', color='black')
    plt.xlabel(r'$t/\tau$')
    plt.ylabel(r'$u_y(z=0)/u_w$')
    ax2.set(xlim=(0, NUM_MEAN_FREE_TIMES), ylim=(0.5, 1.1))
    ax2.legend(loc='upper left')
    plt.savefig('dsmc.png', dpi=240)
    plt.show()
