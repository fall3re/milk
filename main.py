import matplotlib.pyplot as plt
from CONFIG import *
import wall
import tqdm
from PLOTTING import add_to_plot, plot_results, plot_pressure


np.random.seed(31)
pressure = []

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


        NUM_COLLISIONS = 0
        for i in (pbar := tqdm.trange(NUM_TIMESTEPS, desc=f'Simulation {sim+1} of {NUM_SIMS}')):
            pbar.set_postfix(ordered_dict={'collisions': NUM_COLLISIONS})

            pos += D_T * vel
            NUM_COLLISIONS = 0

            SpecularWall.collide_with_specular_wall(pos[2], vel[2])
            ThermalWall.collide_with_thermal_wall(pos, vel)

            # Set Periodic Boundary conditions
            pos[:2] = np.mod(pos[:2], D_Z)


            for cell in range(NUM_CELLS):
                cell_bottom = cell * D_Z
                cell_top = cell_bottom + D_Z
                in_cell = (cell_bottom < pos[2]) & (pos[2] < cell_top)

                particles_in_cell = np.sum(in_cell)
                v_c = vel[:, in_cell]

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

                        NUM_COLLISIONS += 1

                vel[:, in_cell] = v_c

            # record pressure
            pressure.append(SpecularWall.pressure)

            # record v_y(z=0)
            y_velocity[sim, i] = np.mean(vel[1][(0 < pos[2]) & (pos[2] < D_Z)])

            add_to_plot(ax, pos, vel)


        SpecularWall.reset_pressure_parameter()

    plot_results(y_velocity)
    plot_pressure(pressure)

if __name__ == "__main__":
    main()