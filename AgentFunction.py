import random
from Action import Action
from TransferPercept import TransferPercept


class AgentFunction:
    
    def __init__(self):
        self.agent_name = "Agent Popsicle"
        self.action_table = []
        self.action_table.append(Action.GO_FORWARD)
        self.action_table.append(Action.TURN_RIGHT)
        self.action_table.append(Action.GRAB)
        self.action_table.append(Action.SHOOT)
        self.action_table.append(Action.NO_OP)
    
    def process(self,tp):
        bump = tp.get_bump()
        glitter = tp.get_glitter()
        breeze = tp.get_breeze()
        stench = tp.get_stench()
        scream = tp.get_scream()

        prob = random.randint(0,100)

        if (glitter == True):
            return self.action_table[2]
	
        elif (breeze == True): 
            return self.action_table[4]
		
        elif (scream == True): 
            return self.action_table[0]

        elif (stench == True):
            if (prob<70): 
                return self.action_table[4]
            else: 
                return self.action_table[3]
		
		
        elif (bump == True): 
            return self.action_table[1]
		
        else: 
            return self.action_table[0]


    def get_agent_name(self):
        return self.agent_name