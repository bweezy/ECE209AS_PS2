
class Action:

    # Move can be {-1, 0, 1}, where -1 is backwards, 0 is nothing, and 1 is forwards
    # Rotate can be {-1, 0, 1}, where -1 is left, 0 is nothing, and 1 is right
    def __init__(move, rotate):
        self.move = move
        self.rotate = rotate

    def get_action():
        return move, rotate