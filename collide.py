import numpy as np

def collide(v_i, v_j):
    """
    Function collide handling collisions between two candidates.

    Parameters
    ----------
    v_i: float
        Velocity along connecting axis of particle i.
    v_j: float
        Velocity along connecting axis of particle j.

    Returns
    -------
    Updates the two velocities as per collision protocol, conserving momentum and energy.
    Randomises directions.
    """
    relative_v = np.linalg.norm(v_i - v_j)

    cos_theta = 2 * np.random.random() - 1
    sin_theta = np.sqrt(1 - cos_theta ** 2)
    phi = 2 * np.pi * np.random.random()

    v_cm = 0.5 * (v_i + v_j)
    v_p = relative_v * np.array([
        sin_theta * np.cos(phi),
        sin_theta * np.sin(phi),
        cos_theta,
        ])

    v_i[:] = v_cm + 0.5 * v_p
    v_j[:] = v_cm - 0.5 * v_p
