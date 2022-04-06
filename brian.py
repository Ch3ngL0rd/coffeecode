from datatime import datetime
import positions

# We are optimising for time
# Movements take time
# Waiting for operations takes time
# Forget about movement for first iteration

DUMMY = 7878
ZERO_TASK = -1

# This one talks with the robot - calls Brian once we are in position?
class BeepBoopBrain:
    def __init__(self):
        pass
    def speak():
        print("Beep Boop Brain.")

# Yes his name is Brian, don't ask
# Brian has knowledge of robot position and time of the world
# Will Brian be the one to commmunicate with the robot? Probably not
class Brian:
    def __init__(self):
        self.name = 'Brian'
        self.sequences = []

    def speak(self):
        print("I am {}.".format(self.name))

    def fart(self):
        return "Fart"

    # Spooky!
    def get_time(self):
        return datetime.now().timestamp()
    
    def next_action(self):
        self.fart()

# Functions like a stack
class Sequence:
    def __init__(self,task_list):
        self.task_list = task_list
        self.index = 0
    
    # Assumes index is ok :)
    def get_reward(self,current_time):
        return self.task_list[self.index].reward(current_time)
    
    # If we are chosen, then we get the action
    def get_action(self,current_time):
        self.index += 1
        return self.task_list[self.index-1].action(current_time)

# A task consists of two actions
# It allows for asynchronous tasks by integrating time
# Adjust the prize variable to prioritise it over other tasks
# Is not aware of robot position, time of the world
class Task:
    def __init__(self,alpha,omega,time_slept,prize,current_time):
        # First move
        self.alpha = alpha
        # Time started when alpha is started
        self.alpha_time = None
        # Second move
        self.omega = omega
        # Time waited between alpha & omega
        self.time_slept = time_slept
        # Reward for completing the task
        self.prize = prize
        # Time that the task was initiated
        self.time_start = current_time
        
    # Reward for completing the task
    # Does not account for robot position / distance
    # We square time expecting tasks that have been waiting longer to be prioritised
    def reward(self,current_time):
        # If we are waiting for the task, the reward is -1 and won't be chosen
        if self.__is_waiting():
            return ZERO_TASK
        return self.prize * (current_time-self.time_slept) ** 2
    
    # Returns action and updates as if choosing function
    # Could split into action + update if neccesary
    def action(self,current_time):
        if self.alpha.is_acted() == False:
            self.__start_alpha(current_time)
            return self.alpha
        
        if self.__finished_alpha(current_time):
            if self.omega.is_acted() == False:
                return self.omega
        return None

    # Checks if enough time has passed from starting action one
    def __finished_alpha(self,current_time):
        if self.alpha.is_acted() and (current_time-self.alpha_time) > self.time_slept:
            return True
        return False

    # Checks if the task is waiting
    def __is_waiting(self,current_time):
        if current_time-self.alpha_time < self.time_slept:
            return True
        return False

    # Signal when action is chosen
    def __start_alpha(self,current_time):
        self.alpha_time = current_time

    def is_completed(self):
        if self.alpha.is_completed() and self.omega.is_completed():
            return True
        return False

# Task notes
# If alpha | omega is None, assume that the Task is a one step task

# Action is the smallest unit of work
class Action:
    def __init__(self,position):
        self.position = position
        self.acted = False

    # Simple getter and setter functions
    def act(self):
        self.acted = True

    def is_acted(self):
        return self.acted

    def get_position(self):
        return self.position