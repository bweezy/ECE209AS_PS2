import state
import numpy as np


class StateSpace:

    num_headings = 12

    def __init__(self, length, width):
        state_list = []

        for x in np.arange(length):
            for y in np.arange(width):
                for h in np.arange(self.num_headings):
                    state_list.append(state.State(x, y, h))

        self.states = set(state_list)


    '''
    def get_adjacent_states(self, state_in):

        pos_x, pos_y, heading = state_in.get_state()

        adjacent_states = []

        adjacent_states.append(pos_x)
    '''