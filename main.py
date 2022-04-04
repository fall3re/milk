import matplotlib.pyplot as plt
from CONFIG import *
from collide import collide
import wall
import tqdm
from PLOTTING import add_to_plot, plot_results, plot_against_time


np.random.seed(42)


def main():

    # Here are the parameters to be plotted!
    pressure = np.zeros(NUM_TIMESTEPS)
    energy = np.zeros(NUM_TIMESTEPS)
    avg_velocity = np.zeros((NUM_TIMESTEPS, 3))
    y_velocity = np.zeros((NUM_SIMS, NUM_TIMESTEPS))
    cell_average_y_velocities = np.zeros((NUM_TIMESTEPS, NUM_CELLS))
    axes = plt.gca()

    # Creating the walls!
    ThermalWall = wall.ThermalWall(WALL_TEMPERATURE, WALL_VELOCITY)
    SpecularWall = wall.SpecularWall(HEIGHT)

    # Main loop! This for loop is in charge of iterating over the number of simulations
    # that we will be running.
    for sim in range(NUM_SIMS):

        # Randomise initial parameters of the simulated particles
        pos = np.random.random(size=(3, NUM_PARTICLES)) * [[D_Z], [D_Z], [HEIGHT]]
        vel = np.random.normal(0, WALL_TEMPERATURE, size=(3, NUM_PARTICLES))

        # Record the number of collisions that are happening, for the purpose of making
        # the progress bar look pretty
        num_collisions = 0

        # This for loop iterates over the timesteps - it represents the march of time.
        # The tqdm package gives us a progress bar at this stage
        for i in (pbar := tqdm.trange(NUM_TIMESTEPS, desc=f'Simulation {sim+1} of {NUM_SIMS}')):
            pbar.set_postfix(ordered_dict={'collisions': num_collisions})

            # This is one of the parameters that we will plot, and this code is necessary
            # to prime the parameter to receive data
            avg_velocity[i, :] = np.mean(vel[:, :], axis=1)

            # This is the natural movement of the particles
            pos += D_T * vel # s = ut
            num_collisions = 0 # Reset progress bar parameter

            # Handles the collisions with the walls
            SpecularWall.collide_with_specular_wall(pos[2], vel[2])
            ThermalWall.collide_with_thermal_wall(pos, vel)


            # Determine cell parameters, and which particles are in each cell
            bottoms = np.arange(NUM_CELLS) * D_Z
            pos[:2] = np.mod(pos[:2], D_Z)
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

                    # Collide, with random determined probability
                    if np.linalg.norm(v_i - v_j) > 6 * np.random.random():
                        collide(v_i, v_j)

                        # Increment this variable to be reported on the progress bar
                        num_collisions += 1

                vel[:, mask[cell]] = v_c

            # Record system values
            energy[i] = np.linalg.norm(avg_velocity[i, :]) * 0.5  # 1/2 mv^2
            pressure[i] = SpecularWall.pressure
            SpecularWall.reset_pressure_parameter()
            # Record v_y(z=0)
            y_velocity[sim, i] = np.mean(vel[1][(0 < pos[2]) & (pos[2] < D_Z)])

            add_to_plot(axes, pos, vel)


    # MANUALLY DEFINED PLOTTING OPTIONS - comment out which ones you don't want
    # plot_results(y_velocity)
    plot_against_time(pressure)
    plot_against_time(energy)
    for i in range(20):
        plot_against_time(cell_average_y_velocities[100*i])


if __name__ == "__main__":
    main()
