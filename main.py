import robot
import positions
import time
import constants

IP_ADDRESS = "192.168.0.10"

def get_positions():
    print("Joint Angles:")
    print(rob.getj())

    print("Pose Values:")
    print(rob.get_pose())


def move2joints(rob):
    rob.movej(positions.table_home_position[0].joints, acc=constants.ACCELERATION, vel=constants.VELOCITY)

def move2pose(rob):
    rob.movep(positions.table_home_position[0].pose, acc=constants.ACCELERATION, vel=constants.VELOCITY)

def move2linear(rob):
    rob.movel(positions.table_home_position[0].pose, acc=constants.ACCELERATION, vel=constants.VELOCITY)

""" Robot Connection """
rob = robot.connect(IP_ADDRESS)
get_positions()