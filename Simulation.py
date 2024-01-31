from TransferPercept import TransferPercept
from Agent import Agent
from Action import Action
from Environment import Environment


class Simulation:



    def __init__(self, env, maximum, out_writer, non_deterministic):

        self.curr_score = 0
        self.action_cost = -1
        self.death_cost = -1000
        self.shoot_cost = -10
        self.step_counter = 0
        self.last_action = 0        
        self.simulation_running = True;
        self.output_writer = out_writer
        self.environment = env
        self.max_steps = maximum
        self.transfer_percept = TransferPercept(self.environment)
        self.agent = Agent(self.environment,self.transfer_percept,non_deterministic)

        self.environment.place_agent(self.agent)

        #Thread
        self.environment.print_environment()
        self.print_current_percept_sequence()

        try:
            self.output_writer.write(f"Current score: {self.curr_score} \n");
            while (self.simulation_running == True and self.step_counter < self.max_steps):
                self.output_writer.write(f"Last action: {Action.print_action(self.last_action)}\n")
                self.output_writer.write(f"Time step: {self.step_counter}\n")
                self.handle_action(self.agent.choose_action())
                self.environment.place_agent(self.agent)
                self.environment.print_environment()								
                self.print_current_percept_sequence()
                self.output_writer.write(f"Current score: {self.curr_score}\n")

                self.step_counter += 1
                
                if (self.step_counter == self.max_steps or self.simulation_running == False):
                    self.output_writer.write(f"Last action: {Action.print_action(self.last_action)}\n");
                    self.output_writer.write(f"Time step: {self.step_counter}\n");
                    self.last_action = Action.END_TRIAL;
				
                if (self.agent.get_has_gold() == True):
                    self.output_writer.write(f"\n{self.agent.get_name()} found the GOLD!!\n");
				
                if (self.agent.get_is_dead() == True):
                    self.output_writer.write(f"\n{self.agent.get_name()} is DEAD!!\n");	
				
            
        
        except Exception as e:
            print(f'An exception was thrown: {e}')
            
        
        self.print_end_world()

    def print_end_world(self):
            try:
                self.environment.print_environment()
                self.output_writer.write(f"Final score: {self.curr_score}\n")
                self.output_writer.write(f"Last action: {Action.print_action(self.last_action)}\n")

            except Exception as e:
                print(f"An exception was thrown print_end_world: {e}")

    def print_current_percept_sequence(self):
            try:
                #print("Percept: <", end="")
                self.output_writer.write("Percept: <")

                if self.transfer_percept.get_bump():
                    #print("bump,", end="")
                    self.output_writer.write("bump,")
                elif not self.transfer_percept.get_bump():
                    #print("none,", end="")
                    self.output_writer.write("none,")

                if self.transfer_percept.get_glitter():
                    #print("glitter,", end="")
                    self.output_writer.write("glitter,")
                elif not self.transfer_percept.get_glitter():
                    #print("none,", end="")
                    self.output_writer.write("none,")

                if self.transfer_percept.get_breeze():
                    #print("breeze,", end="")
                    self.output_writer.write("breeze,")
                elif not self.transfer_percept.get_breeze():
                    #print("none,", end="")
                    self.output_writer.write("none,")

                if self.transfer_percept.get_stench():
                    #print("stench,", end="")
                    self.output_writer.write("stench,")
                elif not self.transfer_percept.get_stench():
                    #print("none,", end="")
                    self.output_writer.write("none,")

                if self.transfer_percept.get_scream():
                    #print("scream>\n", end="")
                    self.output_writer.write("scream>\n")
                elif not self.transfer_percept.get_scream():
                    #print("none>\n", end="")
                    self.output_writer.write("none>\n")

            except Exception as e:
                print(f"An exception was thrown in printPerceptSequence: {e}")
        
    def handle_action(self, action):
            try:
                if action == Action.GO_FORWARD:
                    if self.environment.get_bump():
                        self.environment.set_bump(False)

                    self.agent.go_forward()
                    self.environment.place_agent(self.agent)

                    if self.environment.check_death():
                        self.curr_score += self.death_cost
                        self.simulation_running = False
                        self.agent.set_is_dead(True)
                    else:
                        self.curr_score += self.action_cost

                    if self.environment.get_scream():
                        self.environment.set_scream(False)

                    self.last_action = Action.GO_FORWARD

                elif action == Action.TURN_RIGHT:
                    self.curr_score += self.action_cost
                    self.agent.turn_right()
                    self.environment.place_agent(self.agent)

                    if self.environment.get_bump():
                        self.environment.set_bump(False)
                    if self.environment.get_scream():
                        self.environment.set_scream(False)

                    self.last_action = Action.TURN_RIGHT

                elif action == Action.TURN_LEFT:
                    self.curr_score += self.action_cost
                    self.agent.turn_left()
                    self.environment.place_agent(self.agent)

                    if self.environment.get_bump():
                        self.environment.set_bump(False)
                    if self.environment.get_scream():
                        self.environment.set_scream(False)

                    self.last_action = Action.TURN_LEFT

                elif action == Action.GRAB:
                    if self.environment.grab_gold():
                        self.curr_score += 1000
                        self.simulation_running = False
                        self.agent.set_has_gold(True)
                    else:
                        self.curr_score += self.action_cost

                    self.environment.place_agent(self.agent)

                    if self.environment.get_bump():
                        self.environment.set_bump(False)
                    if self.environment.get_scream():
                        self.environment.set_scream(False)

                    self.last_action = Action.GRAB

                elif action == Action.SHOOT:
                    if self.agent.shoot_arrow():
                        if self.environment.shoot_arrow():
                            self.environment.set_scream(True)
                        self.curr_score += self.shoot_cost
                    else:
                        if self.environment.get_scream():
                            self.environment.set_scream(False)
                        self.curr_score += self.action_cost

                    self.environment.place_agent(self.agent)

                    if self.environment.get_bump():
                        self.environment.set_bump(False)

                    self.last_action = Action.SHOOT

                elif action == Action.NO_OP:
                    self.environment.place_agent(self.agent)

                    if self.environment.get_bump():
                        self.environment.set_bump(False)
                    if self.environment.get_scream():
                        self.environment.set_scream(False)

                    self.last_action = Action.NO_OP

            except Exception as e:
                print(f"An exception was thrown in handleAction: {e}")
        
    def get_score(self): 
		    return self.curr_score;
		
	
            


        
