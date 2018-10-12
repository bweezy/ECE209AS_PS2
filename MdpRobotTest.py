import MdpRobot
import action
import policy
import state
import time
import pickle

robot = MdpRobot.MdpRobot(6,6)

#move_forward = action.Action(1, 0)

#print(robot.calc_next_state(.1, robot.state, move_forward).get_state())

# a1 = action.Action(1, 3)
# a2 = action.Action(1, 0)
# a3 = action.Action(1, 8)
# print robot.state.get_state()
# new_state = robot.calc_next_state(0, robot.state, a1)
# print new_state.get_state()
# new_state = robot.calc_next_state(0, new_state, a2)
# print new_state.get_state()  
# new_state = robot.calc_next_state(0, new_state, a3)
# print new_state.get_state()
# new_state = robot.calc_next_state(0, new_state, a2)
# print new_state.get_state()
# print robot.get_reward(new_state)

# prob 3(c)
initial_policy = policy.Policy()
initial_state = state.State(1,4,6)

# robot.plot_trajectory(initial_policy, initial_state, 0)

#prob 3(d)
discount_factor = 0.9
# value = robot.eval_policy(initial_policy, discount_factor)

# print(value)

# #prob 3(e)
# print(value[6][4][1])

# print value

# # prob 3(e)
# x, y, heading = initial_state.get_state()
# print value[heading][x][y]

# prob 3(h) and (i)
#start_time = time.time()
#opt_policy, opt_value = robot.policy_iteration(initial_policy, discount_factor)
#pickle.dump(opt_policy, open("opt_policy.p", "wb"))
#pickle.dump(opt_value, open("opt_value.p", "wb"))
#opt_policy = pickle.load(open("opt_policy.p", "rb"))
#opt_value = pickle.load(open("opt_value.p", "rb"))
opt_policy = robot.value_iteration(discount_factor)
pickle.dump(opt_policy, open("opt_policy.p", "wb"))
robot.plot_trajectory(opt_policy, initial_state, 0)
#end_time = time.time()

#elapsed_time = end_time - start_time

import pdb; pdb.set_trace()