"""
This file contains position constants to move the robot arm to.
"""

import math3d as m3d
from dataclasses import dataclass


@dataclass(frozen=True)
class PoseConstant:
    """ Represents a pose constant and/or joint angles for the robot. """
    name: str = None  # Name of the Position
    method: str = None  # Method of Movement            - joint, move, linear
    repeat: str = None  # Secondary Method of Movement  - joint, move, linear

    joints: list = None  # List of 6 Joint Angles
    pose: m3d.Transform = None  # Rotational Matrix + Vector
    velocity: float = None  # Velocity - for fine tuning
    acceleration: float = None  # Acceleration - for fine tuning

    gripper: str = None  # Gripper open/close      - Applied after the movement
    delay: float = None  # Delay for this position - Applied after the movement

home = [
    PoseConstant(
        name="Home",
        method="joint",

        joints=[1.1710947751998901, -1.1096108595477503, -2.18372613588442, -3.0236452261554163, -1.9780052343951624,
                3.210230588912964],
        pose=m3d.Transform(
            [
                [0.99675205, -0.08027798, -0.00638785],
                [0.00377599, -0.03264491, 0.99945988],
                [-0.08044316, -0.9962378, -0.03223575]
            ],
            [0.17553, 0.49630, 0.30476]
        ),

        gripper="open",
        velocity=5,
        acceleration=1
    )
]