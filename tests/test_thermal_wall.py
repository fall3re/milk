from wall import ThermalWall
import numpy as np

t = 10
v = 5
subject = ThermalWall(wall_T=t,wall_v=v)

np.random.seed(42)

class particle:
    def __init__(
        self,
        pos = -2,
        vel = 2
        ):
        self.pos = pos
        self.vel = vel

collider = particle()

class TestThermalWall:
    def as_intended(self):
        subject.collide_with_thermal_wall(collider.pos,collider.vel)
        actual = collider.pos

        assert actual > 0 and collider.vel > 2

