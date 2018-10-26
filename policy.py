import action

class Policy:

    # initial policy
    # for part 3(a)
    def __init__(self, input_policy=None):
        if input_policy == None: # if no input, create an initial policy
            up = {11, 0, 1}
            right = {2, 3, 4}
            down = {5, 6, 7}
            left = {8, 9, 10}

            # create empty matrices to store policy for each heading
            policy_matrix_up = [[None for y in xrange(6)] for x in xrange(6)]
            policy_matrix_right = [[None for y in xrange(6)] for x in xrange(6)]
            policy_matrix_down = [[None for y in xrange(6)] for x in xrange(6)]
            policy_matrix_left = [[None for y in xrange(6)] for x in xrange(6)]

            # store actions for the "up" policy matrix
            for x in xrange(6):
                for y in xrange(6):
                    if x <= 2: # if the current state is on the left of the goal 
                        rotate = 1 # turn right
                    elif x == 3: # if the current state is right above or below the goal
                        rotate = 0 # no turn
                    else: # if the current state is on the right of the goal
                        rotate = -1 # turn left

                    if y <= 4: # if the current state is below the goal or just to its left or right
                        move = 1 # move forward
                    else: # if the current state is above the goal
                        move = -1 # move backward

                    if x == 3 and y == 4:
                        rotate = 0
                        move = 0

                    a = action.Action(move,rotate)

                    policy_matrix_up[x][y] = a

            # store actions for the "right" policy matrix
            for x in xrange(6):
                for y in xrange(6):
                    if y == 5: # if the current state is on the left of the goal 
                        rotate = 1 # turn right
                    elif y == 4: # if the current state is right above or below the goal
                        rotate = 0 # no turn
                    else: # if the current state is on the right of the goal
                        rotate = -1 # turn left

                    if x <= 3: # if the current state is below the goal or just to its left or right
                        move = 1 # move forward
                    else: # if the current state is above the goal
                        move = -1 # move backward

                    if x == 3 and y == 4:
                        rotate = 0
                        move = 0

                    a = action.Action(move,rotate)

                    policy_matrix_right[x][y] = a

            # store actions for the "down" policy matrix
            for x in xrange(6):
                for y in xrange(6):
                    if x <= 2: # if the current state is on the right of the goal 
                        rotate = -1 # turn left
                    elif x == 3: # if the current state is right above or below the goal
                        rotate = 0 # no turn
                    else: # if the current state is on the left of the goal
                        rotate = 1 # turn right

                    if y >= 4: # if the current state is below the goal or just to its left or right
                        move = 1 # move forward
                    else: # if the current state is above the goal
                        move = -1 # move backward

                    if x == 3 and y == 4:
                        rotate = 0
                        move = 0

                    a = action.Action(move,rotate)

                    policy_matrix_down[x][y] = a

            # store actions for the "left" policy matrix
            for x in xrange(6):
                for y in xrange(6):
                    if y == 5: # if the current state is on the right of the goal 
                        rotate = -1 # turn left
                    elif y == 4: # if the current state is right above or below the goal
                        rotate = 0 # no turn
                    else: # if the current state is on the left of the goal
                        rotate = 1 # turn right

                    if x >= 3: # if the current state is below the goal or just to its left or right
                        move = 1 # move forward
                    else: # if the current state is above the goal
                        move = -1 # move backward

                    if x == 3 and y == 4:
                        rotate = 0
                        move = 0

                    a = action.Action(move,rotate)

                    policy_matrix_left[x][y] = a

            self.policy_matrix = [[]]*12
            for heading in xrange(12):
                if heading in up:
                    self.policy_matrix[heading] = policy_matrix_up
                elif heading in right:
                    self.policy_matrix[heading] = policy_matrix_right
                elif heading in down:
                    self.policy_matrix[heading] = policy_matrix_down
                else:
                    self.policy_matrix[heading] = policy_matrix_left

        else: # if there is input, create a policy object
            self.policy_matrix = input_policy

    def get_policy_action(self, current_state):
        pos_x, pos_y, heading = current_state.get_state()
        return self.policy_matrix[heading][pos_x][pos_y]

if __name__ == "__main__":
    pi = Policy()
    import pdb; pdb.set_trace()

