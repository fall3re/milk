from wall import SpecularWall
import numpy as np

h=5
subject = SpecularWall(boxHeight=h)

np.random.seed(42)

class particle:
    def __init__(
            self,
            pos = 2,
            vel = 2
    ):
        self.pos = pos
        self.vel = vel

collider = particle()

class TestSpecularWall:
    def as_intended(self):

        time_after_impact = (collider.pos - subject.Height) / collider.vel
        collider.pos -= time_after_impact * collider.vel
        collider.vel *= -1
        collider.pos += time_after_impact * collider.vel

        assert SpecularWall.collide_with_specular_wall(2,2) == [collider.pos, collider.vel]

