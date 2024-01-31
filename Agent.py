import random
from AgentFunction import AgentFunction


class Agent:

    num_arrows = 1
    
    def __init__(self, world, percept_trans, non_deterministic):
        
        self.non_deterministic_mode = non_deterministic
        self.is_dead = False
        self.has_gold = False
        self.wumpus_world = world
        self.agent_function = AgentFunction()
        self.percept = percept_trans
        self.agent_icon = ""

        self.world_size = self.wumpus_world.get_world_size()
        self.location = self.wumpus_world.get_agent_location()
        self.direction = self.wumpus_world.get_agent_direction()
        self.set_direction(self.direction)
    
    def set_is_dead(self, dead):
        self.is_dead = dead

    def get_is_dead(self):
        return self.is_dead

    def set_has_gold(self, possessGold):
        self.has_gold = possessGold

    def get_has_gold(self):
        return self.has_gold

    def get_name(self):
        return self.agent_function.get_agent_name()

    def choose_action(self):
        return self.agent_function.process(self.percept)

    def get_agent_icon(self):
        return self.agent_icon

    def go_forward(self):
        if not self.non_deterministic_mode:
            if self.direction == 'N':
                if self.location[0] + 1 < self.world_size:
                    self.location[0] += 1
                else:
                    self.wumpus_world.set_bump(True)
            elif self.direction == 'E':
                if self.location[1] + 1 < self.world_size:
                    self.location[1] += 1
                else:
                    self.wumpus_world.set_bump(True)
            elif self.direction == 'S':
                if self.location[0] - 1 >= 0:
                    self.location[0] -= 1
                else:
                    self.wumpus_world.set_bump(True)
            elif self.direction == 'W':
                if self.location[1] - 1 >= 0:
                    self.location[1] -= 1
                else:
                    self.wumpus_world.set_bump(True)
        else:
            move_direction = self.non_deterministic_move()

            if self.direction == 'N':
                if move_direction == 'F':
                    if self.location[0] + 1 < self.world_size:
                        self.location[0] += 1
                    else:
                        self.wumpus_world.set_bump(True)
                elif move_direction == 'L':
                    if self.location[1] - 1 >= 0:
                        self.location[1] -= 1
                    else:
                        self.wumpus_world.set_bump(True)
                elif move_direction == 'R':
                    if self.location[1] + 1 < self.world_size:
                        self.location[1] += 1
                    else:
                        self.wumpus_world.set_bump(True)

            elif self.direction == 'E':
                if move_direction == 'F':
                    if self.location[1] + 1 < self.world_size:
                        self.location[1] += 1
                    else:
                        self.wumpus_world.set_bump(True)
                elif move_direction == 'L':
                    if self.location[0] + 1 < self.world_size:
                        self.location[0] += 1
                    else:
                        self.wumpus_world.set_bump(True)
                elif move_direction == 'R':
                    if self.location[0] - 1 >= 0:
                        self.location[0] -= 1
                    else:
                        self.wumpus_world.set_bump(True)

            elif self.direction == 'S':
                if move_direction == 'F':
                    if self.location[0] - 1 >= 0:
                        self.location[0] -= 1
                    else:
                        self.wumpus_world.set_bump(True)
                elif move_direction == 'L':
                    if self.location[1] + 1 < self.world_size:
                        self.location[1] += 1
                    else:
                        self.wumpus_world.set_bump(True)
                elif move_direction == 'R':
                    if self.location[1] - 1 >= 0:
                        self.location[1] -= 1
                    else:
                        self.wumpus_world.set_bump(True)

            elif self.direction == 'W':
                if move_direction == 'F':
                    if self.location[1] - 1 >= 0:
                        self.location[1] -= 1
                    else:
                        self.wumpus_world.set_bump(True)
                elif move_direction == 'L':
                    if self.location[0] - 1 >= 0:
                        self.location[0] -= 1
                    else:
                        self.wumpus_world.set_bump(True)
                elif move_direction == 'R':
                    if self.location[0] + 1 < self.world_size:
                        self.location[0] += 1
                    else:
                        self.wumpus_world.set_bump(True)

    def non_deterministic_move():
        move_dir = 'F'
        rand = random.randint(0, 9)
        if rand_choice < 8:
            move_dir = 'F'
        elif rand_choice == 8:
            move_dir = 'L'
        elif rand_choice == 9:
            move_dir = 'R'
        return move_dir
    
    def shoot_arrow(self):
        if self.num_arrows == 1:
            self.num_arrows -= 1
            return True
        else:
            return False

    def turn_right(self):
        if self.direction == 'N':
            self.set_direction('E')
        elif self.direction == 'E':
            self.set_direction('S')
        elif self.direction == 'S':
            self.set_direction('W')
        elif self.direction == 'W':
            self.set_direction('N')

    def turn_left(self):
        if self.direction == 'N':
            self.set_direction('W')
        elif self.direction == 'E':
            self.set_direction('N')
        elif self.direction == 'S':
            self.set_direction('E')
        elif self.direction == 'W':
            self.set_direction('S')

    def set_direction(self, newDirection):
        self.direction = newDirection

        if self.direction == 'N':
            self.agent_icon = '^'
        elif self.direction == 'E':
            self.agent_icon = '>'
        elif self.direction == 'S':
            self.agent_icon = 'V'
        elif self.direction == 'W':
            self.agent_icon = '<'

    def get_direction(self):
        return self.direction

    def set_location(self, newLocation):
        self.location[0] = newLocation[0]
        self.location[1] = newLocation[1]

    def get_location(self):
        return self.location
