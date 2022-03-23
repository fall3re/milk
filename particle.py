import numpy as np
from itertools import combinations


G = 6.67408E-11 # Newton's gravitational constant

class Particle:
    def __init__(
            self,
            pos=np.array([0, 0, 0], dtype=np.float64),
            vel=np.array([0, 0, 0], dtype=np.float64),
            name='Ball',
            mass=1.0
    ):
        self.pos = np.copy(pos).astype(np.float64)
        self.vel = np.copy(vel).astype(np.float64)
        self.prev_acc = np.zeros(3)
        self.name = name
        self.mass = mass

    def __str__(self):
        return "Particle: {0}, Mass: {1:.3e}, Position: {2}, Velocity: {3}".format(
            self.name, self.mass,self.pos, self.vel
        )

    def __sub__(self, other):
        return self.pos - other.pos

    def __repr__(self):
        return f"Hello, I am {self.name}, nice to meet you User!"

    @property
    def knrg(self): # kinetic energy of self
        return (np.linalg.norm(self.vel) ** 2) * 0.5 * self.mass

    @property
    def lmom(self): # linear momentum of self
        return self.mass * self.vel

    @property
    def amom(self): # angular momentum of self
        unit_vec = np.cross(self.pos, self.vel) / np.linalg.norm(np.cross(self.pos, self.vel))
        return np.linalg.norm(self.pos) * np.linalg.norm(self.vel) * self.mass * unit_vec

    def step(self, dt):
        """

        Parameters
        ----------
        dt - int - Timestep over which to run the chosen algorithm.

        Returns
        -------
        None
        Updates self.pos and self.vel in line with the chosen algorithm.
        """
        """
        if ALGORITHM == 1:
            self.pos += self.vel * dt
            self.vel += self.acc * dt
        elif ALGORITHM == 2:
            self.vel += self.acc * dt
            self.pos += self.vel * dt
        elif ALGORITHM == 3:
            self.update_acc(self.acc)
            self.pos += self.vel * dt + 0.5 * self.prev_acc * (dt ** 2)
            self.vel += 0.5 * (self.acc + self.prev_acc) * dt
        """


class System:
    def __init__(self):
        self.bodies = []

    def __iter__(self):
        return self.bodies.__iter__()

    @property
    def nrg(self): # Total energy in system
        kinetic_energy = sum(body.knrg for body in self)

        gravitational_energy = 0
        for body1, body2 in combinations(self, 2):
            gravitational_energy += -1 * G * body1.mass * body2.mass / np.linalg.norm(body1 - body2)

        return kinetic_energy + gravitational_energy # = total_energy

    @property
    def lmom(self): # Linear momentum in system
        return np.linalg.norm(sum(body.lmom for body in self))

    @property
    def amom(self): # Angular momentum in system
        return np.linalg.norm(sum(body.amom for body in self))

    def addbody(self, pos, vel, name, mass):   # Appends body to system by indexing in self.bodies
        body = Particle(pos, vel, name, mass)  # and creating a Particle object.
        self.bodies.append(body)
        body.acc = np.zeros(3)

    def step(self, dt): # The entire simulation logic, dependant on some other functions within Particle
        self._updategrav()
        for body in self:
            body.step(dt)

    def _updategrav(self):
        for body in self:
            body.acc = np.zeros_like(body.acc)

        for body1, body2 in combinations(self, 2):
            body1.do_gravity(body2)
            body2.do_gravity(body1)

