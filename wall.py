from CONFIG import WALL_VELOCITY, WALL_TEMPERATURE, HEIGHT
import numpy as np

class ThermalWall:
    def __init__(
        self,
        wall_T=WALL_TEMPERATURE,
        wall_v=WALL_VELOCITY
    ):
        self.T = wall_T
        self.v = wall_v

    def collide_with_thermal_wall(self, pos, vel):

        # Boolean Array Checker
        hit_thermal_wall = pos[2] < 0
        num_collisions = np.sum(hit_thermal_wall)

        # Correct position
        time_after_impact = pos[2, hit_thermal_wall] / vel[2, hit_thermal_wall]
        pos[:2, hit_thermal_wall] -= time_after_impact * vel[:2, hit_thermal_wall]

        # Reset velocity on collide
        vel[:, hit_thermal_wall] = np.sqrt(self.T)
        vel[:2, hit_thermal_wall] *= np.random.normal(size=(2, num_collisions))
        vel[2, hit_thermal_wall] *= np.sqrt(-2 * np.log(np.random.random(num_collisions)))

        vel[1, hit_thermal_wall] += self.v

        # Complete movement
        pos[:2, hit_thermal_wall] += time_after_impact * vel[:2, hit_thermal_wall]
        pos[2, hit_thermal_wall] = time_after_impact * vel[2, hit_thermal_wall]

    @property
    def knrg(self, particles): # kinetic energy of self
        knrg = 0
        for particle in particles:
            knrg += (np.linalg.norm(particle.vel) ** 2) * 0.5 * particle.mass
        return knrg

    @property
    def lmom(self, particles): # linear momentum of self
        lmom = 0
        for particle in particles:
            lmom += particle.mass * particle.vel
        return lmom


class SpecularWall:
    def __init__(
        self,
        boxHeight = HEIGHT,
        pressure = 0
    ):
        self.Height = boxHeight
        self.pressure = 0

    def reset_pressure_parameter(self):
        self.pressure = 0

    def collide_with_specular_wall(self, z, v_z):
        hit_specular_wall = z > self.Height

        # Correct position
        time_after_impact = (z[hit_specular_wall] - self.Height) / v_z[hit_specular_wall]
        z[hit_specular_wall] -= time_after_impact * v_z[hit_specular_wall]

        v_z[hit_specular_wall] *= -1  # Reverse normal component of velocity

        # Complete movement
        z[hit_specular_wall] += time_after_impact * v_z[hit_specular_wall]

        # Update Pressure Parameter
    """
        if hit_specular_wall:
            self.pressure += 2 * max(v_z, -1 * v_z)
    """

    @property
    def knrg(self, particles): # kinetic energy of self
        knrg = 0
        for particle in particles:
            knrg += (np.linalg.norm(particle.vel) ** 2) * 0.5 * particle.mass
        return knrg

    @property
    def lmom(self, particles): # linear momentum of self
        lmom = 0
        for particle in particles:
            lmom += particle.mass * particle.vel
        return lmom