import numpy as np
import random
import state as ss
import matplotlib.pyplot as plt
# import action

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
        self.state_space_size = length*width*self.num_headings

    # Returns the next state given current state, action, and error prob
    # For part 1(d)
    def calc_next_state(self, error_prob, current_state, action):

        next_states_error = []
        
        for i in np.arange(self.length):
            for j in np.arange(self.width):
                for k in np.arange(self.num_headings):
                    next_state = ss.State(i, j, k)
                    prob = self.transition_prob(error_prob, current_state, action, next_state)
                    if prob != 0:
                        # print(prob)
                        # print(next_state.get_state())
                        if prob == error_prob:
                            next_states_error.append(next_state)
                        else:
                            next_state_no_error = next_state

        chance = random.random()
        if chance < 2*error_prob:
            return random.choice(next_states_error)
        else:
            return next_state_no_error


    # Returns the probability of the next state given current state, action, and error probability
    # For part 1(c)
    def transition_prob(self, error_prob, current_state, action, next_state):
        move, rotate = action.get_action()
        if move == 0:
            return 1 if current_state.get_state() == next_state.get_state() else 0

        pos_x, pos_y, heading = current_state.get_state()

        if next_state.get_state() == self.next_logical_state(pos_x, pos_y, heading, action):
            #print(next_state.get_state())
            return 1 - (2 * error_prob)

        if next_state.get_state() == self.next_logical_state(pos_x, pos_y, (heading + 1) % 12, action):
            return error_prob

        if next_state.get_state() == self.next_logical_state(pos_x, pos_y, (heading - 1) % 12, action):
            return error_prob

        return 0

    # Returns what the next state would be given an action without any error.
    def next_logical_state(self, pos_x, pos_y, heading, action):
        move, rotate = action.get_action()

        if heading in self.right:
            # Move right if forwards, left if backwards
            next_x = pos_x + move
            next_y = pos_y
        elif heading in self.down :
            # Move down if forwards, up if backwards
            next_x = pos_x
            next_y = pos_y - move
        elif heading in self.left:
            # Move left if forwards, right if backwards
            next_x = pos_x - move
            next_y = pos_y
        else:
            # Move up if forwards, down if backwards
            next_x = pos_x
            next_y = pos_y + move

        # Check for bound violation
        if next_x < 0 or next_x >= self.width:
            next_x = pos_x

        if next_y < 0 or next_y >= self.length:
            next_y = pos_y

        next_heading = (heading + rotate) % 12

        return (next_x, next_y, next_heading)

    # Returns the reward R(s)
    # For part 2
    def get_reward(self, current_state):
        # L = W = 6 for this problem
        L = 6
        W = 6

        pos_x, pos_y, __ = current_state.get_state() # get the current state's x and y

        if pos_x == 0 or pos_x == L-1 or pos_y == 0 or pos_y == W-1:
            reward = -100
        elif (pos_x == 2 or pos_x == 4) and (pos_y >= 2 and pos_y <= 4):
            reward = -1
        elif pos_x == 3 and pos_y == 4:
            reward = 1
        else:
            reward = 0

        return reward

    # generate and plot trajectory of robot given pi, s0, and pe.
    # for part 3(b)
    def plot_trajectory(self, policy, initial_state, error_prob):
        trajectory = []

        curr_state = initial_state
        pos_x, pos_y, __ = curr_state.get_state()
        trajectory.append((pos_x,pos_y))

        while pos_x != 3 or pos_y != 4: # while the current state is not in the goal
            action = policy.get_policy_action(curr_state)
            next_state = self.calc_next_state(error_prob, curr_state, action) # get the next state
            pos_x, pos_y, __ = next_state.get_state()
            trajectory.append((pos_x,pos_y))
            curr_state = next_state

        print trajectory
        plt.xlim(-1, 6)
        plt.ylim(-1, 6)
        for i in xrange(len(trajectory)-1):
            curr_x = trajectory[i][0]
            curr_y = trajectory[i][1]
            next_x = trajectory[i+1][0]
            next_y = trajectory[i+1][1]
            dx = next_x - curr_x
            dy = next_y - curr_y
            plt.arrow(curr_x, curr_y, dx, dy, head_width=0.1, head_length=0.2, fc='r', ec='r', length_includes_head=True)

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Trajectory')
        plt.show()



    