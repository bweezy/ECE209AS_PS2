import MdpRobot
import action
import policy
import state
import time
import pickle

robot = MdpRobot.MdpRobot(6,6)

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
# start_time = time.time()
# opt_policy_prob3, opt_value_prob3 = robot.policy_iteration(initial_policy, discount_factor)
# pickle.dump(opt_policy_prob3, open("opt_policy_prob3.p", "wb"))
# pickle.dump(opt_value_prob3, open("opt_value_prob3.p", "wb"))
# # opt_policy = pickle.load(open("opt_policy.p", "rb"))
# # opt_value = pickle.load(open("opt_value.p", "rb"))
# end_time = time.time()
# elapsed_time = end_time - start_time
# print "3(i): ", elapsed_time, "seconds"
# robot.plot_trajectory(opt_policy_prob3, initial_state, 0)

# prob 4(b) and 4(c)
# start_time = time.time()
# opt_policy_prob4, opt_value_prob4 = robot.value_iteration(discount_factor)
# pickle.dump(opt_policy_prob4, open("opt_policy_prob4.p", "wb"))
# pickle.dump(opt_value_prob4, open("opt_value_prob4.p", "wb"))
# end_time = time.time()
# elapsed_time = end_time - start_time
# print "4(c): ", elapsed_time, "seconds"
# robot.plot_trajectory(opt_policy_prob4, initial_state, 0)

# prob 5(a)
# robot.plot_trajectory(initial_policy, initial_state, 0.25)
error_prob = 0.25
opt_policy_prob5a, opt_value_prob5a = robot.value_iteration(discount_factor, error_prob)
pickle.dump(opt_policy_prob5a, open("opt_policy_prob5a.p", "wb"))
pickle.dump(opt_value_prob5a, open("opt_value_prob5a.p", "wb"))
# opt_policy_prob5a = pickle.load(open("opt_policy_prob5a.p", "rb"))
# opt_value_prob5a = pickle.load(open("opt_value_prob5a.p", "rb"))
robot.plot_trajectory(opt_policy_prob5a, initial_state, error_prob)

# prob 5(b)
error_prob = 0
opt_policy_prob5b_0, opt_value_prob5b_0 = robot.value_iteration_prob5b(discount_factor, error_prob)
pickle.dump(opt_policy_prob5b_0, open("opt_policy_prob5b_0.p", "wb"))
pickle.dump(opt_value_prob5b_0, open("opt_value_prob5b_0.p", "wb"))
# opt_policy_prob5b_0 = pickle.load(open("opt_policy_prob5b_0.p", "rb"))
# opt_value_prob5b_0 = pickle.load(open("opt_value_prob5b_0.p", "rb"))
robot.plot_trajectory(opt_policy_prob5b_0, initial_state, error_prob)

error_prob = 0.25
opt_policy_prob5b_25, opt_value_prob5b_25 = robot.value_iteration_prob5b(discount_factor, error_prob)
pickle.dump(opt_policy_prob5b_25, open("opt_policy_prob5b_25.p", "wb"))
pickle.dump(opt_value_prob5b_25, open("opt_value_prob5b_25.p", "wb"))
# opt_policy_prob5b_25 = pickle.load(open("opt_policy_prob5b_25.p", "rb"))
# opt_value_prob5b_25 = pickle.load(open("opt_value_prob5b_25.p", "rb"))
robot.plot_trajectory(opt_policy_prob5b_25, initial_state, error_prob)
import pdb; pdb.set_trace()