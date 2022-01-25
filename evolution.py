import random
import numpy as np
import trace_processor
import glob
import infinite_game
import Levenshtein as lv 

class Evo:
	def __init__(self, population_size, truncation_percentage, mutation_rate, max_generations, cluster_example, map_name):
		# Tuning parameters
		self.population_size = population_size
		self.truncation_selection = int(self.population_size * truncation_percentage)
		self.mutation_rate = mutation_rate

		self.current_generation = 0
		#list of lists of parameters
		self.population = []

		self.map_name = map_name

		self.cluster_example = cluster_example

		self.average_fitness_evolution = []
		self.best_agent_evolution = []
		self.best_fitness_evolution = []




	def get_initial_population(self):
		

		for _ in range(population_size):

			individual = random.choices(range(0, 11), k = 7)

			self.population.append(individual)

		print("Initial Population: ", self.population)
		return




	def get_fitness(self, agent_parameters):

		print("Agent Playing: ", agent_parameters)

		action_list = infinite_game.parameterized_agent_play(agent_parameters, self.map_name, False)

		action_string = trace_processor.actions_to_string_translator(action_list)

		fitness = - trace_processor.lev_distance(action_string, cluster_example)

		return fitness



	def get_next_generation(self):

		fitness_list = []
		summed_fitness = 0
		for agent in self.population:
			fitness = self.get_fitness(agent)
			summed_fitness += fitness
			fitness_list.append(fitness)

		average_fitness = summed_fitness/len(self.population)

		fitness_ordered_agents = [x for _,x in sorted(zip(fitness_list, self.population), reverse=True)]

		print("Ordered Fitness: ", sorted(fitness_list, reverse=True))

		best_fitness = max(fitness_list)
		best_agent = fitness_ordered_agents[0]

		survivors = fitness_ordered_agents[:self.truncation_selection]
		children = []

		while((len(survivors) + len(children)) < self.population_size ):

			#choose 2 prents from the survivors
			parents = random.sample(survivors, 2)

			#create a child that is a mixture of both with a sprinkle of mutation
			child = []
			for parameter_num in range(len(parents[0])):
				if random.uniform(0, 1) < self.mutation_rate:
					parameter = random.randint(0,10)
				else:
					parameter = random.choice([parents[0][parameter_num], parents[1][parameter_num]])
				child.append(parameter)
			children.append(child)

		new_population = survivors + children

		return new_population, average_fitness, best_agent, best_fitness





		

	def run_evolution(self):

		self.get_initial_population()

		for i in range(max_generations):
			print("Generation ", i + 1 )
			self.population, average_fitness, best_agent, best_fitness = self.get_next_generation()
			self.average_fitness_evolution.append(average_fitness)
			self.best_fitness_evolution.append(best_fitness)
			self.best_agent_evolution.append(best_agent)










if __name__ == '__main__':


	population_size = 10
	truncation_percentage = 0.5
	mutation_rate = 0.05
	max_generations = 10

	map_name = "Level2"

	cluster_example = trace_processor.actions_to_string_translator(trace_processor.file_to_actions_translator("./Saved_Clusters/Level2/2_____15/Traces_Actions_Level2_26-04-2021_11-25-09_453.txt"))
	#We need to get them from the trace_processor file and chose the one we are interested in



	evo = Evo(population_size, truncation_percentage, mutation_rate, max_generations, cluster_example, map_name)

	evo.run_evolution()

	print("\n\n\nFinal Population: ", evo.population)

	print("\n\n\nAverage Fitness Evolution: ", evo.average_fitness_evolution)

	print("\n\n\nBest Fitness Evolution: ", evo.best_fitness_evolution)

	print("\n\n\nBest Agent Evolution: ", evo.best_agent_evolution)







