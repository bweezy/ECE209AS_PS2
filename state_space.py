import state
import numpy as np


class StateSpace:

    num_headings = 12

    def __init__(self, length, width):
        state_list = []
        self.length = length
        self.width = width

        for x in np.arange(length):
            for y in np.arange(width):
                for h in np.arange(self.num_headings):
                    state_list.append(state.State(x, y, h))

        self.states = set(state_list)
        self.adjacent_states = {}

        for s in self.states:
            self.adjacent_states[s] = self.calc_adjacent_states(s)

    
    def calc_adjacent_states(self, state_in):

        pos_x, pos_y, heading = state_in.get_state()

        possible_headings = [heading, (heading + 1) % 12, (heading - 1) % 12, (heading - 2) % 12, (heading + 2) % 12]
        possible_x = [pos_x]
        possible_y = [pos_y]

        if pos_x - 1 >= 0:
            possible_x.append(pos_x - 1)
        if pos_x + 1 < self.width:
            possible_x.append(pos_x + 1)

        if pos_y - 1 >= 0:
            possible_y.append(pos_y - 1)
        if pos_y + 1 < self.length:
            possible_y.append(pos_y + 1)

        adjacent_states = []
        for x in possible_x:
            for y in possible_y:
                for h in possible_headings:
                    adjacent_states.append(state.State(x, y, h))

        return adjacent_states


    def get_adjacent_states(self, state_in):
        return self.adjacent_states[state_in]