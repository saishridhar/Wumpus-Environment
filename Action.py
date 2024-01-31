class Action:
    START_TRIAL = 0
    GO_FORWARD = 1
    TURN_RIGHT = 2
    TURN_LEFT = 3
    GRAB = 4
    SHOOT = 5
    NO_OP = 6
    END_TRIAL = 7

    @staticmethod
    def print_action(action):
      if (action == 0):
            return "START_TRIAL"
      elif (action == 1): 
            return "GO_FORWARD"
      elif (action == 2): 
            return "TURN_RIGHT"
      elif (action == 3): 
            return "TURN_LEFT"
      elif (action == 4): 
            return "GRAB"
      elif (action == 5): 
            return "SHOOT"
      elif (action == 6): 
            return "NO_OP"
      else: 
            return "END_TRIAL"
  


