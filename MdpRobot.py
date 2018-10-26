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
        #Initial state of (0,0,0)
        self.state = state.State()
        #Generate a state space given the input parameters
        self.state_space = ss.StateSpace(length, width)
        self.length = length
        self.width = width
        #Calculate the size of the state space
        self.state_space_size = length*width*self.num_headings

    # Returns the next state given current state, action, and error prob
    # For part 1(d)
    def calc_next_state(self, error_prob, current_state, action):

        next_states = []
        next_states_prob = []

        #Shortcut function so that only adjacent states are iterated over, rather than the entire state space each timer
        adjacent_states = self.state_space.get_adjacent_states(current_state)

        # Iterate through all possible next states
        for next_possible_state in possible_states:
            
            # Retrieve the transition probability
            prob = self.transition_prob(error_prob, current_state, action, next_possible_state)
            
            # If possible, add the state to an array of next states, along with its probability
            if prob != 0:
                next_states.append(next_possible_state)
                next_states_prob.append(prob)


        # Sample the next state distribution
        next_state = np.random.choice(next_states, p=next_states_prob)
        return next_state


    # Returns the probability of the next state given current state, action, and error probability
    # For part 1(c)
    def transition_prob(self, error_prob, current_state, action, next_state):
        move, rotate = action.get_action()

        # If no movement, then no rotation and no error chance. Only possible next state is same one.
        if move == 0:
            return 1 if current_state.get_state() == next_state.get_state() else 0

        pos_x, pos_y, heading = current_state.get_state()

        probability = 0

        # If the next state is what the action without error would result in, add 1 minus two times the error probability to the transition probability.
        if next_state.get_state() == self.next_logical_state(pos_x, pos_y, heading, action):
            probability += 1 - (2 * error_prob)

        # If the next state is what the action with a prerotation error right would result in, add the error probability.
        if next_state.get_state() == self.next_logical_state(pos_x, pos_y, (heading + 1) % 12, action):
            probability += error_prob

        # If the next state is what the action with a prerotation error left would result in, add the error probability.
        if next_state.get_state() == self.next_logical_state(pos_x, pos_y, (heading - 1) % 12, action):
            probability += error_prob

        return probability

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

        # Add rotation to heading, make sure to wrap around 0.
        next_heading = (heading + rotate) % 12

        return (next_x, next_y, next_heading)

    # Returns the reward R(s)
    # For part 2
    def get_reward(self, current_state):

        pos_x, pos_y, __ = current_state.get_state() # get the current state's x and y

        if pos_x == 0 or pos_x == self.length-1 or pos_y == 0 or pos_y == self.width-1: # Edge tiles
            reward = -100
        elif (pos_x == 2 or pos_x == 4) and (pos_y >= 2 and pos_y <= 4): # Lane tiles
            reward = -10
        elif pos_x == 3 and pos_y == 4: #Goal square
            reward = 1
        else: # All other squares
            reward = 0

        return reward

    # For part 5(b)
    def get_reward_prob5(self, current_state):

        pos_x, pos_y, heading = current_state.get_state() # get the current state's x, y, 

        if pos_x == 0 or pos_x == self.length-1 or pos_y == 0 or pos_y == self.width-1: #Edge tiles
            reward = -100
        elif (pos_x == 2 or pos_x == 4) and (pos_y >= 2 and pos_y <= 4): # Lane tiles
            reward = -10
        elif pos_x == 3 and pos_y == 4 and (heading == 5 or heading == 6 or heading == 7): #Goal Square/Heading
            reward = 1
        else:
            reward = 0 #All other squares

        return reward

    # generate and plot trajectory of robot given pi, s0, and pe.
    # for part 3(b)
    def plot_trajectory(self, policy, initial_state, error_prob):
        trajectory = []

        curr_state = initial_state
        pos_x, pos_y, __ = curr_state.get_state()
        trajectory.append((pos_x,pos_y))

        while pos_x != 3 or pos_y != 4: # while the current state is not in the goal
            # Get the policy action for the current state
            action = policy.get_policy_action(curr_state) 
            
            # Calculate the next state with the current state action pair and error probability
            next_state = self.calc_next_state(error_prob, curr_state, action)

            # Add the x and y to the trajectory
            pos_x, pos_y, __ = next_state.get_state()
            trajectory.append((pos_x,pos_y))

            # Update the current state
            curr_state = next_state
            

        print(trajectory)
        plt.xlim(-1, 6)
        plt.ylim(-1, 6)

        #Plot the trajectory
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
        return trajectory

    # for part 5(b)
    # Same as previous function but takes heading into account 
    def plot_trajectory_prob5b(self, policy, initial_state, error_prob):
        trajectory = []

        curr_state = initial_state
        pos_x, pos_y, heading = curr_state.get_state()
        trajectory.append((pos_x,pos_y, heading))

        while pos_x != 3 or pos_y != 4 or heading < 5 or heading > 7 : # while the current state is not in the goal
            action = policy.get_policy_action(curr_state)
            #import pdb; pdb.set_trace()
            next_state = self.calc_next_state(error_prob, curr_state, action) # get the next state
            pos_x, pos_y, heading = next_state.get_state()
            trajectory.append((pos_x,pos_y, heading))
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
        return trajectory


    # for part 3(d)
    def eval_policy(self, policy, discount, error_prob=0):

        # Initialize V matrix to 0
        last_value = np.zeros((self.num_headings, self.width, self.length))

        diff = -1
        
        # While the value is still changing per iteration
        while diff != 0:

            # Create a new matrix to hold updated values
            new_value = np.zeros((self.num_headings, self.width, self.length))

            # Iterate through all states in state space
            for current_state in self.state_space.states:
                current_x, current_y, current_h = current_state.get_state()

                # Get adjacent states for transition probability calculation
                possible_states = self.state_space.get_adjacent_states(current_state)

                # Iterate through possible next states
                for next_state in possible_states:

                    # Get the action for the current state from the given policy
                    action = policy.get_policy_action(current_state)
                    
                    # Get the transition probability for the s, a, s' triplet
                    prob = self.transition_prob(error_prob, current_state, action, next_state)

                    # Get the reward for the current state 
                    reward = self.get_reward(current_state)

                    # Get the value of the next state from the previous iteration
                    next_x, next_y, next_h = next_state.get_state()
                    v_last = last_value[next_h][next_x][next_y]

                    # Update the value of the current state
                    new_value[current_h][current_x][current_y] += prob * (reward + discount * v_last)

            # Calculate the difference between iterations
            diff = np.sum(np.abs(new_value - last_value))

            # Update the value matrix
            last_value = new_value
        
        # Return the most updated value matrix
        return new_value

    # for part 3(f)
    def one_step_lookahead(self, value, error_prob=0):

        new_policy_matrix = [[[None for y in xrange(self.length)] for x in xrange(self.width)] for h in xrange(self.num_headings)]
        for state in self.state_space.states:
            possible_states = self.state_space.get_adjacent_states(state)
            max_action_value = float("-inf")
            best_action = None
            for action_tuple in ac.action_space:
                action = ac.Action(action_tuple[0],action_tuple[1])
                action_value = 0
                for next_state in possible_states:
                    x, y, h = next_state.get_state()
                    action_value += self.transition_prob(error_prob, state, action, next_state) * value[h][x][y] # add all Psa(s')V(s')
                if action_value > max_action_value:
                    max_action_value = action_value
                    best_action = action

            x, y, h = state.get_state()
            new_policy_matrix[h][x][y] = best_action

        new_policy = pol.Policy(new_policy_matrix)
        return new_policy

    # for part 3(g)
    def policy_iteration(self, initial_policy, discount, error_prob=0):

        last_value = self.eval_policy(initial_policy, discount, error_prob)
        last_policy = self.one_step_lookahead(last_value, error_prob)

        while True:
            print '\npolicy iteration'
            new_value = self.eval_policy(last_policy, discount, error_prob)
            new_policy = self.one_step_lookahead(new_value, error_prob)

            print np.sum(np.abs(new_value - last_value))

            if np.array_equal(new_value, last_value): # if new_value = last_value, then new_policy = last_policy
                #import pdb; pdb.set_trace()
                break

            last_value = new_value
            last_policy = new_policy

        return new_policy, new_value # optimal policy and value

    def value_iteration(self, discount, error_prob=0):

        # Initialize the value matrix to 0
        last_value = np.zeros((self.num_headings, self.width, self.length))

        # Create a policy matrix to update
        new_policy_matrix = [[[None for y in xrange(self.length)] for x in xrange(self.width)] for h in xrange(self.num_headings)]

        diff = -1
        
        # While the value is changing between iterations
        while diff != 0:

            # Initialize a new matrix to hold the updated state values
            new_value = np.zeros((self.num_headings, self.width, self.length))

            # Iterate through all states in state space
            for current_state in self.state_space.states:
                current_x, current_y, current_h = current_state.get_state()

                # Get the adjacent states so you don't need to iterate through entire state space twice
                possible_states = self.state_space.get_adjacent_states(current_state)

                # Initialize the best action and best action value to None and negative infinity
                best_action = None
                max_action_value = float("-inf")

                # Iterate through all possible actions
                for action_tuple in ac.action_space: 
                    action = ac.Action(action_tuple[0],action_tuple[1])
                    action_value = 0

                    # Update the action value with all possible rewards and transition probabilities
                    for next_state in possible_states:
                        x,y,h = next_state.get_state()
                        action_value += self.transition_prob(error_prob, current_state, action, next_state) * (self.get_reward(current_state) + discount*last_value[h][x][y])
                    
                    # If this action has the best expected reward for this state, update the max value and best action
                    if action_value > max_action_value:
                        best_action = action 
                        max_action_value = action_value

                # Set the policy matrix to the best action for this state
                new_policy_matrix[current_h][current_x][current_y] = best_action

                # Set the value of this state to the best expected action reward
                new_value[current_h][current_x][current_y] = max_action_value

            # If the value matrix is the same as the last iteration, break
            if np.array_equal(new_value, last_value):
                break
            last_value = new_value

        # Return the calculated policy and value matrices
        new_policy = pol.Policy(new_policy_matrix)
        return new_policy, new_value


    # Evaluates a trajectory given the (x,y) positions and discount factor
    def eval_trajectory(self, discount, trajectory):

        # Initialize value of trajectory to 0
        value = 0

        # Iterate through trajectory
        for i in xrange(len(trajectory)):
            x, y = trajectory[i]

            # Apply compounding discount to rewards and sum
            value += discount**i + self.get_reward(state.State(pos_x=x, pos_y=y))

        # Return the computed value
        return value

    # Evaluates a trajectory given the (x,y,h) positions and discount factor
    def eval_trajectory_prob5b(self, discount, trajectory):

        # Initialize value of trajectory to 0
        value = 0

        # Iterate through trajectory
        for i in xrange(len(trajectory)):
            x, y, h = trajectory[i]

            # Apply compounding discount to rewards and sum
            value += discount**i + self.get_reward(state.State(pos_x=x, pos_y=y, heading=h))

        # Return the computed value
        return value

