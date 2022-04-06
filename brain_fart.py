import positions
from datetime import datetime

# To add on - add on reward mechanism based on position

class Brain:
    def __init__(self):
        # Action Sequences
        self.sequences = []

        # Sets home / default position
        self.home = Action(positions.home,0,0)

        # Base time
        self.start_time = datetime.now().timestamp()
    
    # Gets the next action queued up with the highest reward
    def next_action(self):
        current_time = datetime.now().timestamp()-self.start_time

        #Sets our base action to the home position
        current_action = self.home
        highest_reward = self.home.reward(current_time)

        for action in self.actions:
            if action.reward(current_time) > highest_reward:
                current_action = action
                highest_reward = action.reward()

        current_action.completed = True

        return current_action

    # Find actions completed and get the next action
    # If the action sequence is completed, we remove it
    def update_actions(self):
        index = 0
        while index < len(self.sequences):
            sequence = self.sequences[index]
            if sequence.top_action().is_completed():
                if sequence.is_completed():
                    self.sequences.pop(index)
                else:
                    sequence.next_action()
            else:
                index += 1
        
    def add_sequence(self,action_sequence):
        self.sequences.append(action_sequence)
    

class ActionSequence:
    def __init__(self,positions,prizes):
        if len(positions) != len(prizes):
            raise Exception("Positions and Prizes lengths are different!")

        self.actions = []
        self.index = 0

        for i in range(len(positions)):
            self.actions.append(Action(
                positions[i],
                None,
                prizes[i]))

    def top_action(self):
        return self.actions[self.index-1]
    
    def next_action(self):
        self.index += 1

    def is_completed(self):
        return self.index == len(self.positions)
    

class Action:
    def __init__(self,position,time,prize):
        self.position = position
        self.time = time
        self.prize = prize
        self.completed = False
    
    # Priorities actions that have been waiting longer
    def reward(self,current_time):
        return self.prize * (current_time-self.time) ** 2
    
    def is_completed(self):
        return self.completed