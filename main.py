import matplotlib.pyplot as plt
import numpy as np

from CONFIG import *
import wall
import tqdm
from PLOTTING import add_to_plot, plot_results, plot_against_time
from math import floor


np.random.seed(42)


# Here are the parameters to be plotted!
pressure = np.zeros(NUM_TIMESTEPS)
energy = np.zeros(NUM_TIMESTEPS)
avg_velocity = np.zeros((NUM_TIMESTEPS, 3))
cell_average_y_velocities = np.zeros((NUM_TIMESTEPS, NUM_CELLS))

def main():
    y_velocity = np.zeros((NUM_SIMS, NUM_TIMESTEPS))

    fig = plt.figure(figsize=(4, 4), dpi=80)
    ax = plt.gca()

    ThermalWall = wall.ThermalWall(WALL_TEMPERATURE, WALL_VELOCITY)
    SpecularWall = wall.SpecularWall(HEIGHT)

    # Iterative loop
    for sim in range(NUM_SIMS):
        pos = np.random.random(size=(3, NUM_PARTICLES)) * [[D_Z], [D_Z], [HEIGHT]]
        vel = np.random.normal(0, WALL_TEMPERATURE, size=(3, NUM_PARTICLES))

        num_collisions = 0
        for i in (pbar := tqdm.trange(NUM_TIMESTEPS, desc=f'Simulation {sim+1} of {NUM_SIMS}')):
            pbar.set_postfix(ordered_dict={'collisions': num_collisions})

            avg_velocity[i, :] = np.mean(vel[:, :], axis=1)

            pos += D_T * vel
            num_collisions = 0

            SpecularWall.collide_with_specular_wall(pos[2], vel[2])
            ThermalWall.collide_with_thermal_wall(pos, vel)

            # Set Periodic Boundary conditions
            pos[:2] = np.mod(pos[:2], D_Z)

            bottoms = np.arange(NUM_CELLS) * D_Z
            bottoms = np.broadcast_to(bottoms, (NUM_PARTICLES, NUM_CELLS)).T
            positions = np.broadcast_to(pos[2], (NUM_CELLS, NUM_PARTICLES))
            mask = (bottoms < positions) & (positions < bottoms + D_Z)

            vel_b = np.broadcast_to(vel[1], (NUM_CELLS, NUM_PARTICLES))
            vel_masked = np.ma.array(vel_b, mask=mask, dtype=np.float)
            cell_average_y_velocities[i] = np.mean(vel_masked, axis=1)

            for cell in range(NUM_CELLS):
                particles_in_cell = np.sum(mask[cell])
                v_c = vel[:, mask[cell]]

                # Number of Candidate Collisions as determined by kinetic theory
                NUM_CANDIDATES = np.ceil(
                    particles_in_cell ** 2 * np.pi * 6 * PARTICLES_PER_CELL * D_T / (2 * CELL_VOLUME)
                ).astype(int)

                # Calculate internal collisions

                for candidate in range(NUM_CANDIDATES):
                    v_i = v_c[:, np.random.randint(particles_in_cell)]
                    v_j = v_c[:, np.random.randint(particles_in_cell)]

                    v_rel2 = np.linalg.norm(v_i - v_j)

                    # Collide, with relative probabilities
                    if v_rel2 > 6 * np.random.random():
                        cos_theta = 2 * np.random.random() - 1
                        sin_theta = np.sqrt(1 - cos_theta ** 2)
                        phi = 2 * np.pi * np.random.random()

                        v_cm = 0.5 * (v_i + v_j)
                        v_p = v_rel2 * np.array([
                            sin_theta * np.cos(phi),
                            sin_theta * np.sin(phi),
                            cos_theta,
                            ])

                        v_i[:] = v_cm + 0.5 * v_p
                        v_j[:] = v_cm - 0.5 * v_p

                        num_collisions += 1

                vel[:, mask[cell]] = v_c

            # record system values
            energy[i] = np.linalg.norm(avg_velocity[i, :]) * 0.5  # 1/2 mv^2
            pressure[i] = SpecularWall.pressure
            # record v_y(z=0)
            y_velocity[sim, i] = np.mean(vel[1][(0 < pos[2]) & (pos[2] < D_Z)])

            add_to_plot(ax, pos, vel)

        SpecularWall.reset_pressure_parameter()

    plot_results(y_velocity)
    plot_against_time(energy)


if __name__ == "__main__":
    main()
