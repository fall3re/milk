from wall import ThermalWall
import numpy as np

t = 10
v = 5
subject = ThermalWall(wall_T=t,wall_v=v)

np.random.seed(42)

class particle:
    def __init__(
        self,
        pos = [0,0,-2],
        vel = [0,0,2]
        ):
        self.pos = pos
        self.vel = vel

collider = particle()

class TestThermalWall:

    #Test the functionality of the collision with Thermal wall.
    def test_collide(self):
        subject.collide_with_thermal_wall(collider.pos,collider.vel)
        actual = collider.pos

        assert actual > 0 and collider.vel > 2

