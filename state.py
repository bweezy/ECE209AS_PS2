class State:
    
    def __init__(self, pos_x=0, pos_y=0, heading=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.heading = heading
        
    def get_state(self):
        return self.pos_x, self.pos_y, self.heading
        