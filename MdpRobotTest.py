import MdpRobot
import action
import policy
import state

robot = MdpRobot.MdpRobot(6,6)

move_forward = action.Action(1, 0)

# print(robot.calc_next_state(.1, robot.state, move_forward).get_state())

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

#robot.plot_trajectory(initial_policy, initial_state, 0)

#prob 3(d)
value = robot.eval_policy(initial_policy, .9)

