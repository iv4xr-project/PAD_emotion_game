import random
import numpy as np
import trace_processor
import glob

class Evo:
    def __init__(self, population_size, truncation_percentage, mutation_rate, max_generations, cluster_examples):
        # Tuning parameters
        self.population_size = population_size
        self.truncation_selection = int(self.population_size * truncation_percentage)
        self.mutation_rate = mutation_rate

        self.current_generation = 0
        #list of lists of parameters
        self.population = []




    def get_initial_population(self):
    	#TODO
    	pass


    def get_fitness(self, agent_parameters):

    	summed_fitness = 0

    	#TODO

    	for example in self.cluster_examples:

    		#TODO
    		pass


    	fitness = summed_fitness/len(self.cluster_examples)

    	#fitness is -(levenshtein distance)
    	#the level can be obtained from the cluster_examples name
    	#TODO
    	return fitness

    def get_next_generation(self):
    	pass







if __name__ == '__main__':


	population_size = 100
	truncation_percentage = 0.3
	mutation_rate = 0.05
	max_generations = 1000

	cluster_examples = #TODO
	#We need to get them from the trace_processor file and chose the one we are interested in



	evo = Evo(population_size, truncation_percentage, mutation_rate, max_generations, cluster_examples)







