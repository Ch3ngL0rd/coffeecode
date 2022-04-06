"""
This file contains code for interacting with the robot.

Part of this code is just overriding the urx code to
fix bugs in it that we were running into.
"""

# from positions import loop_positions as positions
import math3d as m3d
import socket
from urx import Robot
from urx.ursecmon import TimeoutException, SecondaryMonitor
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper, RobotiqScript


def connect(host, *, use_rt=False, max_connection_attempts=10):
    """
    Attempts to connect to the robot repeatedly until it succeeds,
    or the maximum number of connection attempts is exceeded.
    """
    success = False
    attempts = 0
    while not success:
        attempts += 1
        try:
            return OurRobot(host, use_rt=use_rt)
        except (socket.timeout, TimeoutException) as e:
            if attempts >= max_connection_attempts:
                print(" .. Unable to connect to robot")
                raise e
            else:
                print(" .. Connection to robot failed... " + str(e))

class OurGripper(Robotiq_Two_Finger_Gripper):
    """
    The gripper code has the annoying feature of always
    opening the gripper before closing it as part of its
    initialisation. This stops the robot from doing that.
    """

    def __init__(self, robot, *, payload=0.85, speed=255, force=100):
        """
        Creates the grippper.
        """
        Robotiq_Two_Finger_Gripper.__init__(self, robot, payload=payload, speed=speed, force=force)
        self.activated = False

    def _get_new_urscript(self):
        """
        Set up a new URScript to communicate with gripper
        """
        script = RobotiqScript(socket_host=self.socket_host,
                               socket_port=self.socket_port,
                               socket_name=self.socket_name)

        # Set input and output voltage ranges
        script._set_analog_inputrange(0, 0)
        script._set_analog_inputrange(1, 0)
        script._set_analog_inputrange(2, 0)
        script._set_analog_inputrange(3, 0)
        script._set_analog_outputdomain(0, 0)
        script._set_analog_outputdomain(1, 0)
        script._set_tool_voltage(0)
        script._set_runstate_outputs()

        # Set payload, speed and force
        script._set_payload(self.payload)
        script._set_gripper_speed(self.speed)
        script._set_gripper_force(self.force)

        # # Initialize the gripper
        # if not self.activated:
        #     script._set_robot_activate()
        #     script._set_gripper_activate()
        #     self.activated = True
        """ Instead of Running the ABOVE Code to Activate the Gripper --> Just Activate the Gripper Once Manually after Robot has been Turned on """

        # Wait on activation to avoid USB conflicts
        script._sleep(0.1)
        return script


class OurSecondaryMonitor(SecondaryMonitor):
    """
    We subclass the secondary monitor to increase its default
    timeout duration, as we kept getting timeout errors.
    """

    def __init__(self, *args, **kwargs):
        SecondaryMonitor.__init__(self, *args, **kwargs)
        secondary_port = 30002  # Secondary client interface on Universal Robots
        self._s_secondary = socket.create_connection((self.host, secondary_port), timeout=5.0)

    def _get_data(self):
        """
        returns something that looks like a packet, nothing is guaranteed
        """
        while True:
            # self.logger.debug("data queue size is: {}".format(len(self._dataqueue)))
            ans = self._parser.find_first_packet(self._dataqueue[:])
            if ans:
                self._dataqueue = ans[1]
                # self.logger.debug("found packet of size {}".format(len(ans[0])))
                return ans[0]
            else:
                # self.logger.debug("Could not find packet in received data")
                try:
                    tmp = self._s_secondary.recv(1024)
                    self._dataqueue += tmp
                except socket.timeout:
                    print(" -- timed out")

    def wait(self, timeout=5.0):
        """ Wait with a more reasonable default timeout. """
        SecondaryMonitor.wait(self, timeout)


class OurRobot(Robot):
    """
    We subclass the API Robot class to fix its bug,
    and also to encapsulate some of our logic.
    """

    def __init__(self, host, *, use_rt=False):
        """
        Creates the robot and its gripper.
        """
        Robot.__init__(self, host, use_rt)
        self.gripper = OurGripper(self)
        """ Without Gripper """
        self.set_tcp(m3d.Transform())
        """ With Gripper ONLY """
        # self.set_payload(1, (-0.0007, 0.0012, 0.057))
        # self.set_tcp(m3d.Transform(
        #     [
        #         [1, 0, 0],
        #         [0, 1, 0],
        #         [0, 0, 1]
        #     ],
        #     [0, 0, 0.1755]
        # ))
        """ With Gripper + Handle """
        self.set_payload(2, (-0.0007, 0.0012, 0.265))
        self.set_tcp(m3d.Transform(
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ],
            [0, 0, 0.277]
        ))
        self.secmon = OurSecondaryMonitor(host)

    def is_running(self):
        """
        The Robot class incorrectly thinks that our robot
        is not running when it is. Therefore, we just override
        it and say that the robot is always running.
        :return: True
        """
        return True

    def open_gripper(self):
        """ Opens the gripper. """
        self.gripper.open_gripper()

    def close_gripper(self):
        """ Closes the gripper. """
        self.gripper.close_gripper()

