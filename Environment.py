class Environment:


    def __init__(self, size, world, file):
        
        self.world_size = size
        self.output_writer = file
        self.bump = False
        self.scream = False 

        self.wumpus_world = [[[world[i][j][k] for k in range(4)] for j in range(self.world_size)] for i in range(self.world_size)]
        self.percepts = [[[' ' for _ in range(4)] for _ in range(self.world_size)] for _ in range(self.world_size)]
        self.prev_agent_position = self.get_agent_location()
        self.set_percept_map()

        self.bar = ""
        for i in range((self.world_size * 5) + self.world_size - 1):
            self.bar += "-"
    
    def get_world_size(self):
        return self.world_size
    
    def get_agent_direction(self):
        for i in range(self.world_size):
            for j in range(self.world_size):
                if self.wumpus_world[i][j][3] == '^':
                    return 'N'
                if self.wumpus_world[i][j][3] == '>':
                    return 'E'
                if self.wumpus_world[i][j][3] == 'V':
                    return 'S'
                if self.wumpus_world[i][j][3] == '<':
                    return 'W'

        return '@'

    def get_agent_location(self):
        agent_pos = [None, None]

        for i in range(self.world_size):
            for j in range(self.world_size):
                if self.wumpus_world[i][j][3] != ' ':
                    agent_pos[0] = i
                    agent_pos[1] = j

        return agent_pos
    
    def place_agent(self, the_agent):
        self.wumpus_world[self.prev_agent_position[0]][self.prev_agent_position[1]][3] = ' '

        self.agent = the_agent
        self.wumpus_world[self.agent.get_location()[0]][self.agent.get_location()[1]][3] = self.agent.get_agent_icon()

        self.prev_agent_position[0] = self.agent.get_location()[0]
        self.prev_agent_position[1] = self.agent.get_location()[1]
    
    def set_bump(self, bumped):
        self.bump = bumped

    def get_bump(self):
        return self.bump

    def set_scream(self, screamed):
        self.scream = screamed

    def get_scream(self):
        return self.scream

    def get_breeze(self):
        if self.percepts[self.agent.get_location()[0]][self.agent.get_location()[1]][0] == 'B':
            return True
        else:
            return False

    def get_stench(self):
        if self.percepts[self.agent.get_location()[0]][self.agent.get_location()[1]][1] == 'S':
            return True
        else:
            return False

    def get_glitter(self):
        if self.percepts[self.agent.get_location()[0]][self.agent.get_location()[1]][2] == 'G':
            return True
        else:
            return False
    
    def grab_gold(self):
        if self.percepts[self.agent.get_location()[0]][self.agent.get_location()[1]][2] == 'G':
            self.percepts[self.agent.get_location()[0]][self.agent.get_location()[1]][2] = ' '
            self.wumpus_world[self.agent.get_location()[0]][self.agent.get_location()[1]][2] = ' '
            return True
        return False

    def check_death(self):
        if self.wumpus_world[self.agent.get_location()[0]][self.agent.get_location()[1]][0] == 'P':
            return True
        elif self.wumpus_world[self.agent.get_location()[0]][self.agent.get_location()[1]][1] == 'W':
            return True

        return False
    
    def shoot_arrow(self):
        if self.agent.get_direction() == 'N':
            for i in range(self.agent.get_location()[0], self.world_size):
                if self.wumpus_world[i][self.agent.get_location()[1]][1] == 'W':
                    self.wumpus_world[i][self.agent.get_location()[1]][1] = '*'

                    x = i
                    y = self.agent.get_location()[1]

                    if x - 1 >= 0: self.percepts[x - 1][y][1] = ' '
                    if x + 1 < self.world_size: self.percepts[x + 1][y][1] = ' '
                    if y - 1 >= 0: self.percepts[x][y - 1][1] = ' '
                    if y + 1 < self.world_size: self.percepts[x][y + 1][1] = ' '

                    # self.printPercepts()
                    return True

        elif self.agent.get_direction() == 'E':
            for i in range(self.agent.get_location()[1], self.world_size):
                if self.wumpus_world[self.agent.get_location()[0]][i][1] == 'W':
                    self.wumpus_world[self.agent.get_location()[0]][i][1] = '*'

                    x = self.agent.get_location()[0]
                    y = i

                    if x - 1 >= 0: self.percepts[x - 1][y][1] = ' '
                    if x + 1 < self.world_size: self.percepts[x + 1][y][1] = ' '
                    if y - 1 >= 0: self.percepts[x][y - 1][1] = ' '
                    if y + 1 < self.world_size: self.percepts[x][y + 1][1] = ' '

                    # self.printPercepts()

                    return True

        elif self.agent.get_direction() == 'S':
            for i in range(self.agent.get_location()[0], -1, -1):
                if self.wumpus_world[i][self.agent.get_location()[1]][1] == 'W':
                    self.wumpus_world[i][self.agent.get_location()[1]][1] = '*'

                    x = i
                    y = self.agent.get_location()[1]

                    if x - 1 >= 0: self.percepts[x - 1][y][1] = ' '
                    if x + 1 < self.world_size: self.percepts[x + 1][y][1] = ' '
                    if y - 1 >= 0: self.percepts[x][y - 1][1] = ' '
                    if y + 1 < self.world_size: self.percepts[x][y + 1][1] = ' '

                    # self.printPercepts()

                    return True

        elif self.agent.get_direction() == 'W':
            for i in range(self.agent.get_location()[1], -1, -1):
                if self.wumpus_world[self.agent.get_location()[0]][i][1] == 'W':
                    self.wumpus_world[self.agent.get_location()[0]][i][1] = '*'

                    x = self.agent.get_location()[0]
                    y = i

                    if x - 1 >= 0: self.percepts[x - 1][y][1] = ' '
                    if x + 1 < self.world_size: self.percepts[x + 1][y][1] = ' '
                    if y - 1 >= 0: self.percepts[x][y - 1][1] = ' '
                    if y + 1 < self.world_size: self.percepts[x][y + 1][1] = ' '

                    # self.printPercepts()

                    return True

        return False

    def set_percept_map(self):
        # World: Pit, Wumpus, Gold, Agent
        # Percepts: Breeze, Stench, Glitter, Scream

        for i in range(self.world_size):
            for j in range(self.world_size):
                for k in range(4):
                    if self.wumpus_world[i][j][k] == 'P':
                        if j - 1 >= 0: self.percepts[i][j - 1][k] = 'B'
                        if i + 1 < self.world_size: self.percepts[i + 1][j][k] = 'B'
                        if j + 1 < self.world_size: self.percepts[i][j + 1][k] = 'B'
                        if i - 1 >= 0: self.percepts[i - 1][j][k] = 'B'
                    elif self.wumpus_world[i][j][k] == 'W':
                        if j - 1 >= 0: self.percepts[i][j - 1][k] = 'S'
                        if i + 1 < self.world_size: self.percepts[i + 1][j][k] = 'S'
                        if j + 1 < self.world_size: self.percepts[i][j + 1][k] = 'S'
                        if i - 1 >= 0: self.percepts[i - 1][j][k] = 'S'
                    elif self.wumpus_world[i][j][k] == 'G':
                        self.percepts[i][j][k] = 'G'
    
     

    def print_environment(self):
        #   -----------------------
		#  | P W | P W | P W | P W |
 		#  | G A | G A | G A | G A |
		#   -----------------------
		#  | P W | P W | P W | P W |
 		#  | G A | G A | G A | G A |
		#   -----------------------
		#  | P W | P W | P W | P W |
 		#  | G A | G A | G A | G A |
		#   ----------------------- 23
		#  | P W | P W | P W | P W | A A |
 		#  | G A | G A | G A | G A | A A |
		#   ----------------------------- 29
		#
		# P,W,G,A
        
        try:
          
            #print("\n " + self.bar)
            
            self.output_writer.write("\n " + self.bar + "\n")
            for i in range(self.world_size - 1, -1, -1):
                for j in range(2):
                    for k in range(self.world_size):
                        if j == 0:
                            content = "| {} {} ".format(self.wumpus_world[i][k][0], self.wumpus_world[i][k][1])
                        else:
                            content = "| {} {} ".format(self.wumpus_world[i][k][2], self.wumpus_world[i][k][3])
                        #print(content, end='')
                        self.output_writer.write(content)
                        if k == self.world_size - 1:
                            #print("|", end='')
                            self.output_writer.write("|")
                    #print()
                    self.output_writer.write("\n")

                    # print(" -----------------------")
                    # outputWriter.write(" -----------------------\n")

                #print(" " + self.bar)
                self.output_writer.write(" " + self.bar + "\n")
            #print()
            self.output_writer.write("\n")

        except Exception as e:
            print("An exception was thrown: " + str(e))
    