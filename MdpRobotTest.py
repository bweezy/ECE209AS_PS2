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

trajectory = robot.plot_trajectory(initial_policy, initial_state, 0)
print trajectory

#prob 3(e)
discount_factor = 0.9
# value = robot.eval_policy(initial_policy, discount_factor)
# pickle.dump(value, open("value.p", "wb"))
value = pickle.load(open("value.p", "rb"))
x, y, heading = initial_state.get_state()
print "3(d): ", value[heading][x][y] # the value matrix is indexed by heading, x, and y.

# prob 3(h) and (i)
start_time = time.time()
opt_policy_prob3, opt_value_prob3 = robot.policy_iteration(initial_policy, discount_factor)
# pickle.dump(opt_policy_prob3, open("opt_policy_prob3.p", "wb"))
# pickle.dump(opt_value_prob3, open("opt_value_prob3.p", "wb"))
# opt_policy_prob3 = pickle.load(open("opt_policy_prob3.p", "rb"))
# opt_value_prob3 = pickle.load(open("opt_value_prob3.p", "rb"))
end_time = time.time()
elapsed_time = end_time - start_time
print "3(i): ", elapsed_time, "seconds"
trajectory = robot.plot_trajectory(opt_policy_prob3, initial_state, 0)
print trajectory
print "Value of initial state = ", opt_value_prob3[heading][x][y]


# prob 4(b) and 4(c)
start_time = time.time()
opt_policy_prob4, opt_value_prob4 = robot.value_iteration(discount_factor)
# pickle.dump(opt_policy_prob4, open("opt_policy_prob4.p", "wb"))
# pickle.dump(opt_value_prob4, open("opt_value_prob4.p", "wb"))
# opt_policy_prob4 = pickle.load(open("opt_policy_prob4.p", "rb"))
# opt_value_prob4 = pickle.load(open("opt_value_prob4.p", "rb"))
end_time = time.time()
elapsed_time = end_time - start_time
print "4(c): ", elapsed_time, "seconds"
trajectory = robot.plot_trajectory(opt_policy_prob4, initial_state, 0)
print trajectory
print "Value of initial state = ", opt_value_prob4[heading][x][y]

# prob 5(a)
trajectory = robot.plot_trajectory(initial_policy, initial_state, 0.25)
value_prob5a = robot.eval_trajectory(discount_factor, trajectory)
print trajectory
print "5(a): Value of trajectory = ", value_prob5a

# prob 5(b)
error_prob = 0
trajectory = robot.plot_trajectory(initial_policy, initial_state, error_prob)
value_prob5b_0 = robot.eval_trajectory_prob5b(discount_factor, trajectory)
print trajectory
print "5(b): Value of trajectory (0%) = ", value_prob5b_0

error_prob = 0.25
trajectory = robot.plot_trajectory_prob5b(initial_policy, initial_state, error_prob)
value_prob5_25 = robot.eval_trajectory_prob5b(discount_factor, trajectory)
print trajectory
print "5(b) Value of trajectory (25%) = ", value_prob5_25

# import pdb; pdb.set_trace()
