import random
from os.path import exists
import os
import numpy as np
import math
from collections import defaultdict

"""

Idea: make a map generator based on the concept of the turtle drawing library. 
We have a map generator that goes along the map, making corridors as it goes and sometimes expanding them into rooms of different sizes.
It also places coins and enemies along the way

"""

class MapGenerator(object):

	floor_char = '.'
	empty_char = '_'
	wall_char = 'x'
	player_char = 'p'
	enemy_char = 'f'
	health_char = 'r'
	coin_char = 'm'
	objective_char = '0'

	save_folder = "./Maps/Generated_Maps/"



	def print_map(self):

		print("--------MAP--------")

		for line in self.map:
			for char in line:
				print(char)
			print()



	def initialize_empty_map(self):

		for _ in range(self.canvas_size):
			line = ['_']*self.canvas_size
			self.map.append(line)






class TurtleGenerator(MapGenerator):

	directions = [(-1,0), (1,0), (0,1), (0,-1)]

	def __init__(self, canvas_size, total_lenght, rotation_frequency, room_frequency, num_rooms, corridor_min_width, corridor_max_width, room_min_size, room_max_size):

		self.map = []
		self.canvas_size = canvas_size
		self.total_lenght = total_lenght
		self.rotation_frequency = rotation_frequency
		self.room_frequency = room_frequency
		self.num_rooms = num_rooms
		self.corridor_min_width = corridor_min_width
		self.corridor_max_width = corridor_max_width
		self.room_min_size = room_min_size
		self.room_max_size = room_max_size
		self.initialize_empty_map()



	def make_a_map(self):

		turtle = [random.randint(2, self.canvas_size - 2 - self.corridor_max_width), random.randint(2, self.canvas_size - 2 - self.corridor_max_width)]
		new_direction = random.choice(self.directions)
		direction = new_direction
		corridor_width = random.randint(self.corridor_min_width, self.corridor_max_width)
		rooms_made = 0
		current_lenght = 0

		while((rooms_made < self.num_rooms) and current_lenght < self.total_lenght):

			if random.uniform(0.0, 1.0) < self.rotation_frequency:
				new_direction = random.choice(self.directions)
				corridor_width = random.randint(self.corridor_min_width, self.corridor_max_width)

			# if direction[0] == new_direction[0] and direction[1] == new_direction[1]:
			# 	 pass
			# else:

			direction = new_direction


			new_turtle_x = turtle[0] + direction[0]
			new_turtle_y = turtle[1] + direction[1]

			change_counter = 0
			while((new_turtle_x < 2) or (new_turtle_x >= self.canvas_size - 2 - self.corridor_max_width) or (new_turtle_y < 2) or (new_turtle_y >= self.canvas_size - 2 - self.corridor_max_width)):

				direction = random.choice(self.directions)

				new_turtle_x = turtle[0] + direction[0]
				new_turtle_y = turtle[1] + direction[1]

				change_counter +=1

				if change_counter > 100:
					print("Couldn't find a viable directional option!")
					exit()

			turtle[0] = new_turtle_x
			turtle[1] = new_turtle_y

			self.map[turtle[0]][turtle[1]] = self.floor_char

			if direction[0] == 0:
				for i in range(corridor_width):
					self.map[turtle[0] + 1 + i][turtle[1]] = self.floor_char
					if self.map[turtle[0] + corridor_width + 1][turtle[1]] == self.floor_char:
						pass
					else:
						self.map[turtle[0] + corridor_width + 1][turtle[1]]  = self.wall_char
					if self.map[turtle[0] - 1][turtle[1]]  == self.floor_char:
						pass
					else:
						self.map[turtle[0] - 1][turtle[1]] = self.wall_char
			elif direction[1] == 0:
				for i in range(corridor_width):
					self.map[turtle[0]][turtle[1] + 1 + i] = self.floor_char
					if self.map[turtle[0]][turtle[1] + corridor_width + 1] == self.floor_char:
						pass
					else:
						self.map[turtle[0]][turtle[1] + corridor_width + 1]  = self.wall_char
					if self.map[turtle[0]][turtle[1] - 1]  == self.floor_char:
						pass
					else:
						self.map[turtle[0]][turtle[1] - 1] = self.wall_char

			current_lenght += 1



		# Wall it up

		for i in range(1, len(self.map) - 1):
			for j in range(1, len(self.map[0]) - 1):

				if self.map[i][j] == self.empty_char:
					if self.map[i+1][j] == self.floor_char or self.map[i+1][j+1] == self.floor_char or self.map[i+1][j-1] == self.floor_char or self.map[i-1][j+1] == self.floor_char or self.map[i-1][j-1] == self.floor_char or self.map[i-1][j] == self.floor_char or self.map[i][j-1] == self.floor_char or self.map[i][j+1] == self.floor_char:
						self.map[i][j] = self.wall_char
















class TopDownGenerator(MapGenerator):
	pass


class BottomUpGenerator(MapGenerator):

	floor_char = '.'
	empty_char = '_'
	wall_char = 'x'
	player_char = 'p'
	enemy_char = 'f'
	health_char = 'r'
	coin_char = 'm'
	objective_char = '0'

	save_folder = "./Maps/Generated_Maps/"

	def __init__(self, canvas_size, dungeon_density, num_loops, neighbour_depth, neighbour_number_threshold, coin_density, health_density, enemy_density, minimum_tile_distance_player_flower):

		self.map = []
		self.canvas_size = canvas_size
		self.dungeon_density = dungeon_density
		self.num_loops = num_loops
		self.neighbour_depth = neighbour_depth
		self.neighbour_number_threshold = neighbour_number_threshold
		self.coin_density = coin_density
		self.health_density = health_density
		self.enemy_density = enemy_density
		self.minimum_distance_player_flower = minimum_tile_distance_player_flower
		self.small_col_matrix = None


	def make_a_map(self, verbose = False, name = None):

		path_between_player_and_flower = []

		tries = 0

		while len(path_between_player_and_flower) < self.minimum_distance_player_flower/2:

			tries += 1

			if tries > 500:
				print("Cannot find viable map for given parameters after 500 tries. Giving up...")
				return False

			self.map = []

			self.initialize_empty_map()

			if verbose:
				self.print_map()

			self.randomly_add_floor_tiles()

			if verbose:
				self.print_map()

			self.aglutinate_floor()

			self.wall_it_up()

			if verbose:
				self.print_map()

			np.set_printoptions(threshold=np.inf)
			self.makeCollisionMatrix()

			player_pos = self.place_player_randomly()

			if verbose:
				self.print_map()

			flower_pos = self.place_flower_randomly()

			if verbose:
				self.print_map()

			path_between_player_and_flower = self.AStar((int(player_pos[0]/2), int(player_pos[1]/2)), (int(flower_pos[0]/2), int(flower_pos[1]/2)))


		self.place_enemies_randomly()

		if verbose:
			self.print_map()

		self.place_coins_randomly()

		if verbose:
			self.print_map()

		self.place_health_randomly()

		if verbose:
			self.print_map()

		self.save_as_csv(name = name)



	def randomly_add_floor_tiles(self):
		for i in range(self.canvas_size):
			for j in range(self.canvas_size):
				if random.randint(0,100) < self.dungeon_density:
					self.map[i][j] = self.floor_char

	def get_position_empty_neighbours(self, i, j):

		neighbours = []

		if self.neighbour_depth <= 0:
			print("Depth variable needs to be greater than 0")
			exit()

		for n_i in range(i - 1, i + 1 + 1):
			for n_j in range(j - 1, j + 1 + 1):
				if n_i == i and n_j == j:
					continue
				if self.map[n_i][n_j] == self.empty_char:
					neighbours.append([n_i, n_j])

		return neighbours

	def get_position_floored_neighbours(self, i, j):

		neighbours = []
		bordering_edges = False

		if self.neighbour_depth <= 0:
			print("Depth variable needs to be greater than 0")
			exit()

		for n_i in range(i - self.neighbour_depth, i + self.neighbour_depth + 1):
			for n_j in range(j - self.neighbour_depth, j + self.neighbour_depth + 1):


				if n_i < 0 or n_i >= self.canvas_size or n_j < 0 or n_j >= self.canvas_size:
					bordering_edges = True
					continue
				if n_i == i and n_j == j:
					continue
				if self.map[n_i][n_j] == self.floor_char:
					neighbours.append([n_i, n_j])

		return neighbours, bordering_edges


	def aglutinate_floor(self):
		for run in range(self.num_loops):
			to_add = []
			to_remove = []
			for i in range(self.canvas_size):
				for j in range(self.canvas_size):
					neighbors, bordering = self.get_position_floored_neighbours(i, j)
					if (len(neighbors) >= self.neighbour_number_threshold) and not bordering:
						to_add.append([i, j])
					else:
						to_remove.append([i,j])
			for cord in to_add:
				self.map[cord[0]][cord[1]] = self.floor_char
			for cord in to_remove:
				self.map[cord[0]][cord[1]] = self.empty_char




	def wall_it_up(self):
		for i in range(self.canvas_size):
			for j in range(self.canvas_size):
				if self.map[i][j] == self.floor_char:
					empty_neighbours = self.get_position_empty_neighbours(i,j)
					for neighbour in empty_neighbours:
						self.map[neighbour[0]][neighbour[1]] = self.wall_char

	def place_player_randomly(self):

		for _ in range(10000):
			i = random.randint(1, self.canvas_size-2)
			j = random.randint(1, self.canvas_size-2)
			if self.map[i][j] == self.floor_char and len(self.get_position_floored_neighbours(i,j)[0]) == 8:
				self.map[i][j] = self.player_char
				return (i,j)

		print("Too many attempts at placing player. The map generator quit...")
		return False

	def place_flower_randomly(self):

		for _ in range(10000):
			i = random.randint(1, self.canvas_size-2)
			j = random.randint(1, self.canvas_size-2)
			if self.map[i][j] == self.floor_char and len(self.get_position_floored_neighbours(i,j)[0]) == 8:
				self.map[i][j] = self.objective_char
				return (i,j)

		print("Too many attempts at placing flower. The map generator quit...")
		return False

	def place_coins_randomly(self):

		for _ in range(self.canvas_size*self.canvas_size):
			i = random.randint(1, self.canvas_size-2)
			j = random.randint(1, self.canvas_size-2)
			if self.map[i][j] == self.floor_char and len(self.get_position_floored_neighbours(i,j)[0]) == 8:
				if random.uniform(0.0, 100.0) < self.coin_density:
					self.map[i][j] = self.coin_char


	def place_health_randomly(self):

		for _ in range(self.canvas_size*self.canvas_size):
			i = random.randint(1, self.canvas_size-2)
			j = random.randint(1, self.canvas_size-2)
			if self.map[i][j] == self.floor_char and len(self.get_position_floored_neighbours(i,j)[0]) == 8:
				if random.uniform(0.0, 100.0) < self.health_density:
					self.map[i][j] = self.health_char

	def place_enemies_randomly(self):

		for _ in range(self.canvas_size*self.canvas_size):
			i = random.randint(1, self.canvas_size-2)
			j = random.randint(1, self.canvas_size-2)
			if self.map[i][j] == self.floor_char and len(self.get_position_floored_neighbours(i,j)[0]) == 8:
				if random.uniform(0.0, 100.0) < self.enemy_density:
					self.map[i][j] = self.enemy_char


	def makeCollisionMatrix(self):
		self.small_col_matrix = np.zeros((int(self.canvas_size/2), int(self.canvas_size/2)))

		for i in range(int(self.canvas_size/2)):
			for j in range(int(self.canvas_size/2)):
				if self.map[i*2][j*2] == self.wall_char or self.map[i*2 + 1][j*2] == self.wall_char or self.map[i*2][j*2 + 1] == self.wall_char or self.map[i*2 + 1][j*2 + 1] == self.wall_char:
					self.small_col_matrix[i][j] = 1


	def reconstruct_path(self, cameFrom, current, start):
		total_path = [current]
		while current != start:
			current = cameFrom[current]
			total_path.insert(0, current)
		return total_path

	def AStarHeuristic(self, a, b):
		#Euclidian Distance
		return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5


	#Only returns diagonals when both adjacent horizontal and vertical tiles are also free as to avoid collisions.
	def getMixedNeighbors(self, node):
		neighbors = []
		
		if node[0]-1 > 0 and self.small_col_matrix[node[0]-1][node[1]] == 0:
			neighbors.append((node[0]-1, node[1]))
			if node[1]-1 > 0 and self.small_col_matrix[node[0]][node[1]-1] == 0:
				if self.small_col_matrix[node[0]-1][node[1]-1] == 0:
					neighbors.append((node[0]-1, node[1]-1))
			if node[1]+1 < len(self.small_col_matrix[0]) and self.small_col_matrix[node[0]][node[1]+1] == 0:
				if self.small_col_matrix[node[0]-1][node[1]+1] == 0:
					neighbors.append((node[0]-1, node[1]+1))
		if node[0]+1 < len(self.small_col_matrix) and self.small_col_matrix[node[0]+1][node[1]] == 0:
			neighbors.append((node[0] + 1, node[1]))
			if node[1]-1 > 0 and self.small_col_matrix[node[0]][node[1]-1] == 0:
				if self.small_col_matrix[node[0]+1][node[1]-1] == 0:
					neighbors.append((node[0]+1, node[1]-1))
			if node[1]+1 < len(self.small_col_matrix[0]) and self.small_col_matrix[node[0]][node[1]+1] == 0:
				if self.small_col_matrix[node[0]+1][node[1]+1] == 0:
					neighbors.append((node[0]+1, node[1]+1))
		if node[1]-1 > 0 and self.small_col_matrix[node[0]][node[1]-1] == 0:
			neighbors.append((node[0], node[1]-1))
		if node[1]+1 < len(self.small_col_matrix[0]) and self.small_col_matrix[node[0]][node[1]+1] == 0:
			neighbors.append((node[0], node[1] + 1))

		return neighbors

	# A* finds a path from start to goal.
	# h is the heuristic function. h(n) estimates the cost to reach goal from node n.
	def AStar(self, start, goal):
		# The set of discovered nodes that may need to be (re-)expanded.
		# Initially, only the start node is known.
		# This is usually implemented as a min-heap or priority queue rather than a hash-set.
		openSet = [start]

		# For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
		# to n currently known.
		cameFrom = {}

		# For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
		# I initialize every value as Infinite
		gScore = {}
		gScore = defaultdict(lambda: math.inf, gScore)
		gScore[start] = 0

		# For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
		# how short a path from start to finish can be if it goes through n.
		fScore = {}
		fScore = defaultdict(lambda: math.inf, fScore)
		fScore[start] = self.AStarHeuristic(start, goal)

		while len(openSet) > 0:
			# This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
			min_val = math.inf
			for node in openSet:
				if fScore[node] < min_val:
					min_val = fScore[node]
					current = node

			if current == goal:
				return self.reconstruct_path(cameFrom, current, start)

			openSet.remove(current)

			for neighbor in self.getMixedNeighbors(current):
				# d(current,neighbor) is the weight of the edge from current to neighbor
				# tentative_gScore is the distance from start to the neighbor through current
				tentative_gScore = gScore[current] + 1 #d(current, neighbor) --> for now, lets say all weights are 1
				if tentative_gScore < gScore[neighbor]:
					# This path to neighbor is better than any previous one. Record it!
					cameFrom[neighbor] = current
					gScore[neighbor] = tentative_gScore
					fScore[neighbor] = tentative_gScore + self.AStarHeuristic(neighbor, goal)
					if neighbor not in openSet:
						openSet.append(neighbor)

		# Open set is empty but goal was never reached
		return []




	def save_as_csv(self, name):

		rand_id = random.randint(1000000000, 9999999999)

		if name == None:
			file_path = self.save_folder + "BottomUpMap_" + str(self.canvas_size) + "_" + str(self.dungeon_density) + "_" + str(self.num_loops) + "_" + str(self.neighbour_depth) + "_" + str(self.neighbour_number_threshold) + "_" + str(self.coin_density) + "_" + str(self.health_density) + "_" + str(rand_id) +".csv"
		else:
			file_path = self.save_folder + "Map_" + str(name) +".csv"


		while exists(file_path):
			if name == None:
				print("File already exists")
				return
			else:
				rand_id = random.randint(1000000000, 9999999999)
				file_path = self.save_folder + "BottomUpMap_" + str(self.canvas_size) + "_" + str(self.dungeon_density) + "_" + str(self.num_loops) + "_" + str(self.neighbour_depth) + "_" + str(self.neighbour_number_threshold) + "_" + str(self.coin_density) + "_" + str(self.health_density) + "_" + str(rand_id) +".csv"

		f = open(file_path, 'w+')

		for line in self.map:
			for char in line:
				f.write(char)
				f.write(';')
			f.write("\n")



##############################################
###	Code to make celular automata maps
##############################################

# turly = BottomUpGenerator(32, 30, 3, 1, 3, 0.5, 0.5, 0.4, 10)

# for i in range(1):
# 	turly.make_a_map(name = i, verbose = True)


##############################################
###	Code to make room and corridors maps
##############################################


mappy_maker = TurtleGenerator(150, 800, 0.1, 0.1, 5, 3, 4, 6, 20)

mappy_maker.make_a_map()

mappy_maker.print_map()




















