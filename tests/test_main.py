from main import main
import wall
import numpy as np

def as_expected(self):

    ThermalWall = wall.ThermalWall(1, 1)
    SpecularWall = wall.SpecularWall(1)

    pos = [0,0.5,0]
    vel = [0,1,0]

    pos += 1 * vel


    SpecularWall.collide_with_specular_wall(pos[2], vel[2])
    ThermalWall.collide_with_thermal_wall(pos, vel)

    pos[:2] = np.mod(pos[:2], 1)

    assert pos == [0,0.5,0] and vel == [0,-1,0]






