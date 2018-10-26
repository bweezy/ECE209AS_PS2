import state
import numpy as np
import action

class StateSpace:

    num_headings = 12

    def __init__(self, length, width):
        state_list = []
        self.length = length
        self.width = width

        # Generate all possible states
        for x in np.arange(width):
            for y in np.arange(length):
                for h in np.arange(self.num_headings):
                    state_list.append(state.State(x, y, h))

        self.states = set(state_list)

        # Initialize an empty 3d array to hold lists of adjacent states
        self.adjacent_states = [[[None for y in xrange(self.length)] for x in xrange(self.width)] for h in xrange(self.num_headings)]

        # Pre-calculate adjacent states to save on computation time in iteration
        for s in self.states:
            x, y, h = s.get_state()
            self.adjacent_states[h][x][y] = self.calc_adjacent_states(s)

    
    # Given a state, returns all states that have a member with a difference of +/- 1 or 0 from the current state members
    def calc_adjacent_states(self, state_in):

        pos_x, pos_y, heading = state_in.get_state()
       
        # Possible headings include the current, a difference of 1 due to and error and no rotation, or a rotation and no error
        # Also include a difference of 2 that could result as the combination of an error and a rotation
        possible_headings = [heading, (heading + 1) % 12, (heading - 1) % 12, (heading - 2) % 12, (heading + 2) % 12]

        # Initialize the possible x and y matrices with the current position
        possible_x = [pos_x]
        possible_y = [pos_y]

        # Add neighboring x positions if they are on the grid
        if pos_x - 1 >= 0:
            possible_x.append(pos_x - 1)
        if pos_x + 1 < self.width:
            possible_x.append(pos_x + 1)

        # Add neighboring y positions if they are on the grid
        if pos_y - 1 >= 0:
            possible_y.append(pos_y - 1)
        if pos_y + 1 < self.length:
            possible_y.append(pos_y + 1)

        adjacent_states = []
        # Create the adjacent state list using all possible combinations. Though this includes many impossible transitions,
        # we felt the reduction of state space was good enough given the effort it would take to code an exact possible state list. 
        for x in possible_x:
            for y in possible_y:
                for h in possible_headings:
                    adjacent_states.append(state.State(x, y, h))

        return adjacent_states
        

    # Given a state, return all adjacent states
    def get_adjacent_states(self, state_in):
        x, y, h = state_in.get_state()
        return self.adjacent_states[h][x][y]