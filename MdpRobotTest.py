import MdpRobot
import action



robot = MdpRobot.MdpRobot(12,12)

move_forward = action.Action(1, 0)

print(robot.calc_next_state(.1, robot.state, move_forward).get_state())

