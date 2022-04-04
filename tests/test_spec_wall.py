from wall import SpecularWall
import numpy as np

h=5
subject = SpecularWall(boxHeight=h)

np.random.seed(42)

class particle:
    def __init__(
            self,
            pos = [0,0,2],
            vel = [0,0,2]
    ):
        self.pos = pos
        self.vel = vel

collider = particle()

class TestSpecularWall:

    # Test the functionality of the collision code.
    def test_collision(self):

        time_after_impact = (collider.pos - subject.Height) / collider.vel
        collider.pos -= time_after_impact * collider.vel
        collider.vel *= -1
        collider.pos += time_after_impact * collider.vel

        assert subject.collide_with_specular_wall(2,2) == [collider.pos, collider.vel], "Specular Wall collision failed."

    # Test the functionality of the pressure logging system.
    def test_pressure(self):

        subject.collide_with_specular_wall(collider.pos, collider.vel)

        assert subject.pressure == 4, "Pressure calculation failed."

    # Test the functionality of the pressure reset system.
    def test_reset_pressure(self):

        subject.pressure = 10
        subject.reset_pressure_parameter()

        assert subject.pressure == 0, "Pressure reset functionality failed."


