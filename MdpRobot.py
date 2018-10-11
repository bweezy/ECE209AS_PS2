import numpy as np
import random
import state
import state_space as ss
import matplotlib.pyplot as plt
import action as ac
import policy as pol

class MdpRobot:

    up = {11, 0, 1}
    right = {2, 3, 4}
    down = {5, 6, 7}
    left = {8, 9, 10}
    num_headings = 12

    def __init__(self, length, width):
        self.state = state.State()
        self.state_space = ss.StateSpace(length, width)
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
                    next_state = state.State(i, j, k)
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

        pos_x, pos_y, __ = current_state.get_state() # get the current state's x and y

        if pos_x == 0 or pos_x == self.length-1 or pos_y == 0 or pos_y == self.width-1:
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

        print(trajectory)
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


    # for part 3(d)
    def eval_policy(self, policy, discount):

        last_value = np.zeros((self.num_headings, self.width, self.length))

        error_prob = 0
        diff = -1
        
        while diff != 0:
        # diff = 10000 # TEMPORARY: For debugging
        # while diff > 100: # TEMPORARY: For debugging

            new_value = np.zeros((self.num_headings, self.width, self.length))

            for current_state in self.state_space.states:
                current_x, current_y, current_h = current_state.get_state()
                possible_states = self.state_space.get_adjacent_states(current_state)

                for next_state in possible_states:

                    action = policy.get_policy_action(current_state)
                    # Need an error probability?
                    prob = self.transition_prob(error_prob, current_state, action, next_state)
                    reward = self.get_reward(current_state)

                    next_x, next_y, next_h = next_state.get_state()
                    v_last = last_value[next_h][next_x][next_y]

                    new_value[current_h][current_x][current_y] += prob * (reward + discount * v_last)

            diff = np.sum(np.abs(new_value - last_value))
            last_value = new_value
            print diff

        return new_value

    # for part 3(f)
    def one_step_lookahead(self, value):

        new_policy_matrix = [[[None for y in xrange(self.length)] for x in xrange(self.width)] for h in xrange(self.num_headings)]
        for state in self.state_space.states:
            possible_states = self.state_space.get_adjacent_states(state)
            max_action_value = float("-inf")
            best_action = None
            for action_tuple in ac.action_space:
                action = ac.Action(action_tuple[0],action_tuple[1])
                for next_state in possible_states:
                    action_value = self.transition_prob(0, state, action, next_state)
                    if action_value > max_action_value:
                        max_action_value = action_value
                        best_action = action


            x, y, h = state.get_state()
            new_policy_matrix[h][x][y] = action
            new_policy = pol.Policy(new_policy_matrix)
        return new_policy

    # for part 3(g)
    def policy_iteration(self, initial_policy, discount):

        last_value = self.eval_policy(initial_policy, discount)
        last_policy = self.one_step_lookahead(last_value)

        while True:
            print '\npolicy iteration'
            new_value = self.eval_policy(last_policy, discount)
            new_policy = self.one_step_lookahead(new_value)

            # import pdb; pdb.set_trace()

            if np.array_equal(new_value, last_value) and new_policy == last_policy:
                break

        return new_policy, new_value # optimal policy and value


        

    