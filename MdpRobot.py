import numpy as np
import random
import state as ss
import action

class MdpRobot:

    up = {11, 0, 1}
    right = {2, 3, 4}
    down = {5, 6, 7}
    left = {8, 9, 10}
    num_headings = 12

    def __init__(self, length, width):
        self.state = ss.State()
        self.length = length
        self.width = width
        self.state_space_size = length*width*num_headings

    # Returns the next state given current state, action, and error prob
    # For part 1(d)
    def calc_next_state(self, error_prob, current_state, action):

        possible_states = {}
        for i in np.arange(length):
            for j in np.arange(width):
                for k in np.arange(num_headings):
                    next_state = ss.State(i, j, k)
                    prob = transition_prob(error_prob, current_state, action, next_state)
                    if prob != 0:
                        possible_states[next_state] = prob

        return random.choice(possible_states.keys(), possible_states.values())


    # Returns the probability of the next state given current state, action, and error probability
    # For part 1(c)
    def transition_prob(self, error_prob, current_state, action, next_state):
        move, rotate = action.get_action()
        if move == 0:
            return 1 if current_state.get_state() == next_state.get_state() else 0

        pos_x, pos_y, heading = current_state.get_state()

        if next_state.get_state() == calc_next_state(pos_x, pos_y, heading, action):
            return 1 - (2 * error_prob)

        if next_state.get_state() == calc_next_state(pos_x, pos_y, (heading + 1) % 12, action):
            return error_prob

        if next_state.get_state() == calc_next_state(pos_x, pos_y, (heading - 1) % 12, action):
            return error_prob

    # Returns what the next state would be given an action without any error.
    def next_logical_state(self, pos_x, pos_y, heading, action):
        move, rotate = action.get_action()

        if heading in self.right:
            # Move right if forwards, left if backwards
            next_x = pos_x + move
        elif heading in self.down :
            # Move down if forwards, up if backwards
            next_y = pos_y - move
        elif heading in self.left:
            # Move left if forwards, right if backwards
            next_x = pos_x - move
        else:
            # Move up if forwards, down if backwards
            next_y = pos_y + move

        # Check for bound violation
        if next_x < 0 or next_x >= self.width:
            next_x = pos_x

        if next_y < 0 or next_y >= self.length:
            next_y = pos_y

        next_heading = (heading + rotate) % 12

        return (next_x, next_y, next_heading)


    