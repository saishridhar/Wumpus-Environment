import argparse
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import random
import os
import tempfile
from Environment import Environment
from Simulation import Simulation
from tqdm import tqdm

class WorldApplication:

    VERSION = "v0.1"
    

    #seed,user_defined_seed, world_size,random_agent_loc,output_filename,max_steps,non_deterministic_mode,probability
    @staticmethod
    def simulate_trial(curr_trial, params):

        keep_file = random.random() < params[6]

        if params[1]:
            wumpus_world = WorldApplication.generate_random_wumpus_world(params[0] + curr_trial, params[2], params[3])
        else:
            rand = random.Random()
            wumpus_world = WorldApplication.generate_random_wumpus_world(rand.randint(0, 2**32 - 1), params[2], params[3])

        with tempfile.NamedTemporaryFile(delete=False, mode='w', dir='output/') as output_writer:
            wumpus_environment = Environment(size=params[2], world=wumpus_world, file=output_writer)
            trial = Simulation(env=wumpus_environment, maximum=params[4], out_writer=output_writer, non_deterministic=params[5])
            score = trial.get_score()
            output_writer.write("\n\n___________________________________________\n\n")
            temp_file_path = output_writer.name

        if keep_file == True:       
            return score,temp_file_path
        else:
            os.remove(temp_file_path)
            return score,None



    @staticmethod
    def main():

        parser = argparse.ArgumentParser(description="Wumpus World Application")
        
        parser.add_argument('-d', '--dimensions', type=int, help='World Size as an Integer')
        parser.add_argument('-s', '--steps', type=int, help='Maximum No. of steps')
        parser.add_argument('-t', '--trials', type=int, help='Number of Trials')
        parser.add_argument('-a', '--agentLoc', action='store_true', help='Randomize Agent Location')
        parser.add_argument('-r', '--randseed', type=int, help='Random Number Seed')
        parser.add_argument('-f', '--file', type=str, help='Output File Path')
        parser.add_argument('-n', '--nondeter', action='store_true', help='Non-determinism Flag')

        arg = parser.parse_args()

        world_size = 4
        num_trials = 100000
        max_steps = 50

        non_deterministic_mode = False
        random_agent_loc = False
        user_defined_seed = False

        out_filename = "output/wumpus_out.txt"

        rand = random.Random()
        seed = rand.randint(0, 2**32 - 1)

     
        # if the world dimension is specified
        if arg.dimensions is not None:
            if arg.d > 1:
                world_size = int(arg.dimensions)
           
        # if the maximum number of steps is specified
        if arg.steps is not None:
            max_steps = arg.steps
       
        # if the number of trials is specified
        if arg.trials is not None:
            num_trials = arg.trials
       
        # if the random agent location value is specified
        if arg.agentLoc is not None:
            random_agent_loc = arg.agentLoc
       
        # if the random number seed is specified
        if arg.randseed is not None:
            seed = arg.randseed
            user_defined_seed = True
       
        # if the output filename is specified
        if arg.file is not None:
            out_filename = arg.file
         
        # if the non-determinism is specified
        if arg.nondeter is not None:
            non_deterministic_mode = arg.nondeter
       

        try:
            with open(out_filename, 'w') as output_writer:
                print(f"\n\nWumpus-Python {WorldApplication.VERSION}\n")
                output_writer.write(f"Wumpus-Python {WorldApplication.VERSION}\n\n")

                print(f"Dimensions: {world_size}x{world_size}")
                output_writer.write(f"Dimensions: {world_size}x{world_size}\n")

                print(f"Maximum number of steps: {max_steps}")
                output_writer.write(f"Maximum number of steps: {max_steps}\n")

                print(f"Number of trials: {num_trials}")
                output_writer.write(f"Number of trials: {num_trials}\n")

                print(f"Random Agent Location: {random_agent_loc}")
                output_writer.write(f"Random Agent Location: {random_agent_loc}\n")

                print(f"Random number seed: {seed}")
                output_writer.write(f"Random number seed: {seed}\n")

                print(f"Output filename: {out_filename}")
                output_writer.write(f"Output filename: {out_filename}\n")

                print(f"Non-Deterministic Behavior: {non_deterministic_mode}\n")
                output_writer.write(f"Non-Deterministic Behavior: {non_deterministic_mode}\n\n")
                
            

            trial_scores = [0] * num_trials
            temp_files = []
            total_score = 0
            p = 10/num_trials
            params = [seed,user_defined_seed, world_size,random_agent_loc,max_steps,non_deterministic_mode,p]
            
            
            with ProcessPoolExecutor() as executor:
                futures = {executor.submit(WorldApplication.simulate_trial, curr_trial, params): curr_trial for curr_trial in range(num_trials)}
       
                for future in tqdm(concurrent.futures.as_completed(futures), total=num_trials, desc="Simulating"):
                    curr_trial = futures[future]
                    try:
                        score,temp = future.result()
                        trial_scores[curr_trial] = score
                        if temp is not None:
                            temp_files.append(temp)
                    except Exception as exc:
                        print(f'Trial {curr_trial} generated an exception: {exc}')
                    
            
            with open(out_filename, 'a') as output_writer:

                for temp_file_path in temp_files:
                    with open(temp_file_path, 'r') as file:
                        content = file.read()
                        output_writer.write(content)
                        output_writer.write('\n')  # Add a newline or some delimiter between files
        
                    os.remove(temp_file_path)

                for i in range(num_trials):
                    #print(f"Trial {i + 1} score: {trial_scores[i]}")
                    output_writer.write(f"Trial {i + 1} score: {trial_scores[i]}\n")
                    total_score += trial_scores[i]

                print(f"\nTotal Score: {total_score}")
                output_writer.write(f"\nTotal Score: {total_score}\n")

                print(f"Average Score: {total_score / num_trials}")
                output_writer.write(f"Average Score: {total_score / num_trials}\n")
            
         

        except Exception as e:
            print(f"An exception was thrown in World Application: {e}")

        print("\nFinished.")

    @staticmethod
    def generate_random_wumpus_world(seed, size, randomly_place_agent):
        new_world = [[[' ' for _ in range(4)] for _ in range(size)] for _ in range(size)]
        occupied = [[False for _ in range(size)] for _ in range(size)]

        rand_gen = random.Random(seed)
        pits = 2

        # default agent location and orientation
        agent_x_loc, agent_y_loc = 0, 0
        agent_icon = '^'

        # randomly generate agent location and orientation
        if randomly_place_agent:
            agent_x_loc, agent_y_loc = rand_gen.randint(0, size - 1), rand_gen.randint(0, size - 1)
            agent_icon = ['^', '>', 'V', '<'][rand_gen.randint(0, 3)]

        # place agent in the world
        new_world[agent_x_loc][agent_y_loc][3] = agent_icon

        # Pit generation
        for _ in range(pits):
            x, y = rand_gen.randint(0, size - 1), rand_gen.randint(0, size - 1)
            while (x == agent_x_loc and y == agent_y_loc) or occupied[x][y]:
                x, y = rand_gen.randint(0, size - 1), rand_gen.randint(0, size - 1)

            occupied[x][y] = True
            new_world[x][y][0] = 'P'

        # Wumpus Generation
        x, y = rand_gen.randint(0, size - 1), rand_gen.randint(0, size - 1)
        while x == agent_x_loc and y == agent_y_loc:
            x, y = rand_gen.randint(0, size - 1), rand_gen.randint(0, size - 1)

        occupied[x][y] = True
        new_world[x][y][1] = 'W'

        # Gold Generation
        x, y = rand_gen.randint(0, size - 1), rand_gen.randint(0, size - 1)
        occupied[x][y] = True
        new_world[x][y][2] = 'G'
        return new_world
    
    


if __name__ == "__main__":
    WorldApplication.main()






    
