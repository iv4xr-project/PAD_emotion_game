import numpy as np
import random
import math
import networkx as nx
import matplotlib.pyplot as plt





ACTION_LIST = ['n', ' ', 'w', 's', 'a', 'd', 'wa', 'wd', 'sa', 'sd', 'w ', 's ', 'a ', 'd ', 'wa ', 'wd ', 'sa ', 'sd ']

MOVE_LIST = ['n', 'w', 's', 'a', 'd', 'wa', 'wd', 'sa', 'sd']



class PositionError(Exception):
        def __init__(self, position):
            self.position = position


class WorldExploredError(Exception):
        def __init__(self, agent):
            agent.world_explored = 1



class BasicAgent:

	def __init__(self, world):
		self.world = world
		self.prefered_direction = 0
		self.previous_direction = 0
		self.previous_action = 'n'
		self.previous_pos_x = self.world.player.imagined_x
		self.previous_pos_y = self.world.player.imagined_y
		self.stuck_counter = 0

		self.world_explored = 0

		self.up_unknown = []
		self.down_unknown = []
		self.left_unknown = []
		self.right_unknown = []

		#self.visited_array = [0] * self.world.perceptor.num_directions


		# self.direction_array = [None] * self.world.perceptor.num_directions

		# for i in range(len(self.direction_array)):
		# 	direct = (i/self.world.perceptor.num_directions)*360 + 180
		# 	if direct >= 360:
		# 		direct -= 360
		# 	self.direction_array[i] = direct

		self.last_update_x = None
		self.last_update_y = None

		self.nav_graph = nx.Graph()

		self.collide_graph = nx.Graph()

		self.last_print = 0

		self.current_path = []

		self.chasing_enemy = False

		self.chasing_flower = False

		self.chasing_coin = False

		self.chasing_cake = False

		# self.nav_matrix_size = 30

		# self.nav_matrix = np.zeros((self.nav_matrix_size, self.nav_matrix_size))

	def flower_in_view(self):

		for flower in self.world.flower_group:
			if self.world.in_view(flower):
				return True
			


	def sprites_in_view(self, sprite_group):

		number_sprites_view = 0
		for spritty in sprite_group:
			if self.world.in_view(spritty):
				number_sprites_view += 1
		return number_sprites_view

	def enemies_in_view(self):

		return self.sprites_in_view(self.world.enemy_group)

	def coins_in_view(self):

		return self.sprites_in_view(self.world.money_group)

	def cakes_in_view(self):

		return self.sprites_in_view(self.world.food_group)


	def closest_manhattan_sprite(self, sprite_group):

		distance_closest = float('inf')
		sprite_closest = None

		player_x = self.world.player.imagined_x + self.world.screen_width/2
		player_y = self.world.player.imagined_y + self.world.screen_height/2

		for sprite in sprite_group:
			if self.world.in_view(sprite):
				try:
					distance = len(nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(player_x, player_y), target=self.get_closest_node_to_position(sprite.rect.x + self.world.player.imagined_x, sprite.rect.y + self.world.player.imagined_y)))
				except PositionError:
					continue
				except nx.NetworkXNoPath:
					continue
				if distance < distance_closest:
					distance_closest = distance
					sprite_closest = sprite
		return distance_closest, sprite_closest

 

	def closest_enemy(self):

		distance_closest_enemy = float('inf')

		for enemy in self.world.enemy_group:
			if self.world.in_view(enemy):
				distance = math.sqrt((self.world.player.rect.x - enemy.rect.x )**2 + (self.world.player.rect.y - enemy.rect.y)**2 )
				myradians = math.atan2(enemy.rect.y - self.world.player.rect.y, enemy.rect.x - self.world.player.rect.x)
				direction = math.degrees(myradians)

				while(direction > 360):
					direction -= 360

				while(direction < 0):
					direction += 360

				if distance < distance_closest_enemy:
					distance_closest_enemy = distance
					direction_closest_enemy = direction
					#print("Rect: ", enemy.rect.x, enemy.rect.y)
					position_closest_enemy = (enemy.rect.x, enemy.rect.y)


		return distance_closest_enemy, direction_closest_enemy, position_closest_enemy

	def avoid_closest_enemy(self):

		action = self.fight_closest()

		return self.negate_action(action)



	def fight_closest(self):


		distance_closest_enemy, direction_closest_enemy, position_closest_enemy = self.closest_enemy()

		#print(direction_closest_enemy)

		if distance_closest_enemy < float('inf'):

			if distance_closest_enemy < 70:
				self.chasing_enemy = False
				#move thowards while attacking

				self.current_path = []


				if (direction_closest_enemy < 22.5 and direction_closest_enemy >= 0) or (direction_closest_enemy <= 360 and direction_closest_enemy > 337.5):
					action = 'd '
				elif (direction_closest_enemy < 67.5 and direction_closest_enemy >= 22.5):
					action = 'sd '
				elif (direction_closest_enemy < 112.5 and direction_closest_enemy >= 67.5):
					action = 's '
				elif (direction_closest_enemy < 157.5 and direction_closest_enemy >= 112.5):
					action = 'sa '
				elif (direction_closest_enemy < 202.5 and direction_closest_enemy >= 157.5):
					action = 'a '
				elif (direction_closest_enemy < 247.5 and direction_closest_enemy >= 202.5):
					action = 'wa '
				elif (direction_closest_enemy < 292.5 and direction_closest_enemy >= 247.5):
					action = 'w '
				elif (direction_closest_enemy < 337.5 and direction_closest_enemy >= 292.5):
					action = 'wd '
				else:
					print("Error in directions!!!")
					exit()

			else:

				if self.previous_pos_x == self.world.player.imagined_x and self.previous_pos_y == self.world.player.imagined_y:
					self.stuck_counter += 1
				else:
					self.stuck_counter = 0

				if self.stuck_counter >= 3:
					self.stuck_counter = 0
					action = random.choice(MOVE_LIST)
				else:

					if self.chasing_enemy:

						if self.player_arrived_at_next_node():
							del[self.current_path[0]]

						if len(self.current_path) == 0:
							self.current_path = []
							self.chasing_enemy = False
							action = random.choice(MOVE_LIST)
						else:
							action = self.go_to_node(self.current_path[0])

					else:
						x = self.world.player.imagined_x + self.world.screen_width/2
						y = self.world.player.imagined_y + self.world.screen_height/2
						
						try:
							
							self.current_path = nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(x, y), target=self.get_closest_node_to_position(position_closest_enemy[0] + self.world.player.imagined_x, position_closest_enemy[1] + self.world.player.imagined_y))
							self.chasing_enemy = True
							self.chasing_coin = False
							self.chasing_flower = False
							self.chasing_cake = False

							action = self.go_to_node(self.current_path[0])
						except PositionError:
							action = random.choice(MOVE_LIST)
						except nx.NetworkXNoPath:
							action = random.choice(MOVE_LIST)
							# if self.world_explored:
							# 	return self.go_to_flower()
							# else:
							# 	try:
							# 		print("Exploring the world!")
							# 		self.chasing_enemy = False
							# 		self.current_path = []
							# 		return self.explore()
							# 	except WorldExploredError:
							# 		self.chasing_flower = False
							# 		return self.go_to_flower()
								

				# if (direction_closest_enemy < 22.5 and direction_closest_enemy >= 0) or (direction_closest_enemy <= 360 and direction_closest_enemy > 337.5):
				# 	action = 'd'
				# elif (direction_closest_enemy < 67.5 and direction_closest_enemy >= 22.5):
				# 	action = 'sd'
				# elif (direction_closest_enemy < 112.5 and direction_closest_enemy >= 67.5):
				# 	action = 's'
				# elif (direction_closest_enemy < 157.5 and direction_closest_enemy >= 112.5):
				# 	action = 'sa'
				# elif (direction_closest_enemy < 202.5 and direction_closest_enemy >= 157.5):
				# 	action = 'a'
				# elif (direction_closest_enemy < 247.5 and direction_closest_enemy >= 202.5):
				# 	action = 'wa'
				# elif (direction_closest_enemy < 292.5 and direction_closest_enemy >= 247.5):
				# 	action = 'w'
				# elif (direction_closest_enemy < 337.5 and direction_closest_enemy >= 292.5):
				# 	action = 'wd'
				# else:
				# 	print("Error in directions!!!")
				# 	exit()

		self.update_nav_graph()
		self.previous_pos_x = self.world.player.imagined_x
		self.previous_pos_y = self.world.player.imagined_y
		return action



	def go_to_flower(self):


		if self.previous_pos_x == self.world.player.imagined_x and self.previous_pos_y == self.world.player.imagined_y:
			self.stuck_counter += 1
		else:
			self.stuck_counter = 0

		if self.stuck_counter >= 3:
			self.stuck_counter = 0
			action = random.choice(MOVE_LIST)
			self.previous_action = action
			return action

		flower_x = self.world.flower_group.sprites()[0].rect.x
		flower_y = self.world.flower_group.sprites()[0].rect.y

		try:
			self.get_closest_node_to_position(flower_x + self.world.player.imagined_x, flower_y + self.world.player.imagined_y)
		except PositionError as er:
			#print("Couldn't find a node near position: ", er.position)
			return self.explore()

	
		

		if self.chasing_flower == False or len(self.current_path) == 0:
			self.chasing_flower = True
			self.chasing_coin = False
			self.chasing_enemy = False
			self.chasing_cake = False
			x = self.world.player.imagined_x + self.world.screen_width/2
			y = self.world.player.imagined_y + self.world.screen_height/2
			self.current_path = nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(x, y), target=self.get_closest_node_to_position(flower_x + self.world.player.imagined_x, flower_y + self.world.player.imagined_y))

		
		if self.player_arrived_at_next_node():
			del[self.current_path[0]]
			if len(self.current_path) == 0:
				self.chasing_flower = False
				return random.choice(MOVE_LIST)



		action = self.go_to_node(self.current_path[0])

		self.update_nav_graph()

		self.previous_pos_x = self.world.player.imagined_x
		self.previous_pos_y = self.world.player.imagined_y


		return action


	def get_closest_sprite_position_and_distance(self, sprite_group):

		distance = float('inf')
		position = None

		for spritty in sprite_group:
			prov_distance = math.sqrt((self.world.screen_width/2 - spritty.rect.x)**2 + (self.world.screen_height/2 - spritty.rect.y)**2)
			if prov_distance < distance:
				distance = prov_distance
				position = (self.world.player.imagined_x + spritty.rect.x, self.world.player.imagined_y + spritty.rect.y)

		return position, distance



	def go_to_closest_coin(self):

		#print("Going to coin!")

		if self.previous_pos_x == self.world.player.imagined_x and self.previous_pos_y == self.world.player.imagined_y:
			self.stuck_counter += 1
		else:
			self.stuck_counter = 0
		#print("Stuck counter: ", self.stuck_counter)
		if self.stuck_counter >= 3:
			self.stuck_counter = 0
			action = random.choice(MOVE_LIST)
			self.previous_action = action
			return action


		position, distance = self.get_closest_sprite_position_and_distance(self.world.money_group)

		try:
			self.get_closest_node_to_position(position[0], position[1])
		except PositionError as er:
			print("Couldn't find a node near position: ", er.position)
			return self.explore()

		# print("Current Position: ", self.world.player.imagined_x + self.world.screen_width/2, self.world.player.imagined_y + self.world.screen_height/2)
		
		# print("Closest Coin Position: ", position[0], position[1])
		if self.chasing_coin == False or len(self.current_path) == 0:
			self.chasing_coin = True
			self.chasing_flower = False
			self.chasing_enemy = False
			self.chasing_cake = False
			x = self.world.player.imagined_x + self.world.screen_width/2
			y = self.world.player.imagined_y + self.world.screen_height/2
			self.current_path = nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(x, y), target=self.get_closest_node_to_position(position[0], position[1]))

		
		if self.player_arrived_at_next_node():
			del[self.current_path[0]]
			if len(self.current_path) == 0:
				self.chasing_coin = False
				return random.choice(MOVE_LIST)



		action = self.go_to_node(self.current_path[0])


		self.update_nav_graph()

		self.previous_pos_x = self.world.player.imagined_x
		self.previous_pos_y = self.world.player.imagined_y


		return action

	def go_to_closest_cake(self):

		#print("Going to cake!")

		if self.previous_pos_x == self.world.player.imagined_x and self.previous_pos_y == self.world.player.imagined_y:
			self.stuck_counter += 1
		else:
			self.stuck_counter = 0
		if self.stuck_counter >= 3:
			self.stuck_counter = 0
			action = random.choice(MOVE_LIST)
			self.previous_action = action
			return action


		position, distance = self.get_closest_sprite_position_and_distance(self.world.food_group)

		try:
			self.get_closest_node_to_position(position[0], position[1])
		except PositionError as er:
			#print("Couldn't find a node near position: ", er.position)
			return self.explore()

		if self.chasing_coin == False or len(self.current_path) == 0:
			self.chasing_coin = True
			self.chasing_flower = False
			self.chasing_enemy = False
			self.chasing_cake = False
			x = self.world.player.imagined_x + self.world.screen_width/2
			y = self.world.player.imagined_y + self.world.screen_height/2

			self.current_path = nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(x, y), target=self.get_closest_node_to_position(position[0], position[1]))

		
		if self.player_arrived_at_next_node():
			del[self.current_path[0]]
			if len(self.current_path) == 0:
				self.chasing_coin = False
				return random.choice(MOVE_LIST)



		action = self.go_to_node(self.current_path[0])

		self.update_nav_graph()

		self.previous_pos_x = self.world.player.imagined_x
		self.previous_pos_y = self.world.player.imagined_y


		return action



	def get_free_directions(self):

		perc_vec = self.world.perceptor.get_perception_vec(self.world.collide_group)[0]

		if self.previous_action == 'n':
			self.visited_array = [0] * self.world.perceptor.num_directions
		elif self.previous_action == 'w':
			self.visited_array = [0] * int(self.world.perceptor.num_directions/2) + [1] * int(self.world.perceptor.num_directions/2)
		elif self.previous_action == 's':
			self.visited_array = [1] * int(self.world.perceptor.num_directions/2) + [0] * int(self.world.perceptor.num_directions/2)
		elif self.previous_action == 'a':
			self.visited_array = [0] * int(self.world.perceptor.num_directions/4) + [1] * int(self.world.perceptor.num_directions/2) + [0] * int(self.world.perceptor.num_directions/4)
		elif self.previous_action == 'd':
			self.visited_array = [1] * int(self.world.perceptor.num_directions/4) + [0] * int(self.world.perceptor.num_directions/2) + [1] * int(self.world.perceptor.num_directions/4)
		elif self.previous_action == 'wa':
			self.visited_array = [0] * int(self.world.perceptor.num_directions/8) + [0] * int(self.world.perceptor.num_directions/4) + [1] * int(self.world.perceptor.num_directions/2) + [0] * int(self.world.perceptor.num_directions/8)
		elif self.previous_action == 'wd':
			self.visited_array = [1] * int(self.world.perceptor.num_directions/8) + [0] * int(self.world.perceptor.num_directions/2) + [1] * int(self.world.perceptor.num_directions/4) + [1] * int(self.world.perceptor.num_directions/8)
		elif self.previous_action == 'sa':
			self.visited_array = [0] * int(self.world.perceptor.num_directions/8) + [1] * int(self.world.perceptor.num_directions/2) + [0] * int(self.world.perceptor.num_directions/4) + [0] * int(self.world.perceptor.num_directions/8)
		elif self.previous_action == 'sd':
			self.visited_array = [1] * int(self.world.perceptor.num_directions/8) + [1] * int(self.world.perceptor.num_directions/4) + [0] * int(self.world.perceptor.num_directions/2) + [1] * int(self.world.perceptor.num_directions/8)

		#print(self.previous_action)
		#print(len(self.visited_array))



		#print(perc_vec)

		empty_dir = []
		weights = []

		for i in range(len(perc_vec)):
			if perc_vec[i] < 300 and self.visited_array[i] == 0:

				empty_dir.append(self.direction_array[i])
				weights.append((self.world.perceptor.max_distance - perc_vec[i])**3)

		return empty_dir, weights


	def create_graphs(self):


		for xx in range(0, self.world.screen_width, self.world.iterator_square.granularity):

			for yy in range(0, self.world.screen_height, self.world.iterator_square.granularity):

				self.world.iterator_square.rect.x = xx
				self.world.iterator_square.rect.y = yy

				in_view = self.world.get_all_in_view(self.world.collide_group)

				collided = False

				for dude in in_view:
					if self.world.iterator_square.rect.colliderect(dude.rect):
						collided = True

				if not collided:
					self.nav_graph.add_node((self.world.player.imagined_x + xx, self.world.player.imagined_y + yy), pos=(self.world.player.imagined_x + xx, -(self.world.player.imagined_y + yy)))
					if self.nav_graph.has_node((self.world.player.imagined_x + xx - self.world.iterator_square.granularity, self.world.player.imagined_y + yy)):
						self.nav_graph.add_edge((self.world.player.imagined_x + xx - self.world.iterator_square.granularity, self.world.player.imagined_y + yy), (self.world.player.imagined_x + xx, self.world.player.imagined_y + yy))

					if self.nav_graph.has_node((self.world.player.imagined_x + xx, self.world.player.imagined_y + yy - self.world.iterator_square.granularity)):
						self.nav_graph.add_edge((self.world.player.imagined_x + xx , self.world.player.imagined_y + yy - self.world.iterator_square.granularity), (self.world.player.imagined_x + xx, self.world.player.imagined_y + yy))

				else:
					self.collide_graph.add_node((self.world.player.imagined_x + xx, self.world.player.imagined_y + yy), pos=(self.world.player.imagined_x + xx, -(self.world.player.imagined_y + yy)))
					if self.collide_graph.has_node((self.world.player.imagined_x + xx - self.world.iterator_square.granularity, self.world.player.imagined_y + yy)):
						self.collide_graph.add_edge((self.world.player.imagined_x + xx - self.world.iterator_square.granularity, self.world.player.imagined_y + yy), (self.world.player.imagined_x + xx, self.world.player.imagined_y + yy))

					if self.collide_graph.has_node((self.world.player.imagined_x + xx, self.world.player.imagined_y + yy - self.world.iterator_square.granularity)):
						self.collide_graph.add_edge((self.world.player.imagined_x + xx , self.world.player.imagined_y + yy - self.world.iterator_square.granularity), (self.world.player.imagined_x + xx, self.world.player.imagined_y + yy))

		self.last_update_x = self.world.player.imagined_x
		self.last_update_y = self.world.player.imagined_y


	def update_connections(self, graph, xx, yy):
		if not graph.has_node((self.world.player.imagined_x + xx, self.world.player.imagined_y + yy)):
			graph.add_node((self.world.player.imagined_x + xx, self.world.player.imagined_y + yy), pos=(self.world.player.imagined_x + xx, -(self.world.player.imagined_y + yy)))
		#Check for left connection
		if graph.has_node((self.world.player.imagined_x + xx - self.world.iterator_square.granularity, self.world.player.imagined_y + yy)):
			graph.add_edge((self.world.player.imagined_x + xx - self.world.iterator_square.granularity, self.world.player.imagined_y + yy), (self.world.player.imagined_x + xx, self.world.player.imagined_y + yy))
			if (self.world.player.imagined_x + xx - self.world.iterator_square.granularity, self.world.player.imagined_y + yy) in self.right_unknown:
				self.right_unknown.remove((self.world.player.imagined_x + xx - self.world.iterator_square.granularity, self.world.player.imagined_y + yy))
		#Check for up connection
		if graph.has_node((self.world.player.imagined_x + xx, self.world.player.imagined_y + yy - self.world.iterator_square.granularity)):
			graph.add_edge((self.world.player.imagined_x + xx , self.world.player.imagined_y + yy - self.world.iterator_square.granularity), (self.world.player.imagined_x + xx, self.world.player.imagined_y + yy))
			if (self.world.player.imagined_x + xx, self.world.player.imagined_y + yy - self.world.iterator_square.granularity) in self.down_unknown:
				self.down_unknown.remove((self.world.player.imagined_x + xx, self.world.player.imagined_y + yy - self.world.iterator_square.granularity))
		#Check for right connection
		if graph.has_node((self.world.player.imagined_x + xx + self.world.iterator_square.granularity, self.world.player.imagined_y + yy)):
			graph.add_edge((self.world.player.imagined_x + xx + self.world.iterator_square.granularity, self.world.player.imagined_y + yy), (self.world.player.imagined_x + xx, self.world.player.imagined_y + yy))
			if (self.world.player.imagined_x + xx + self.world.iterator_square.granularity, self.world.player.imagined_y + yy) in self.left_unknown:
				self.left_unknown.remove((self.world.player.imagined_x + xx + self.world.iterator_square.granularity, self.world.player.imagined_y + yy))
		#Check for down connection
		if graph.has_node((self.world.player.imagined_x + xx, self.world.player.imagined_y + yy + self.world.iterator_square.granularity)):
			graph.add_edge((self.world.player.imagined_x + xx , self.world.player.imagined_y + yy + self.world.iterator_square.granularity), (self.world.player.imagined_x + xx, self.world.player.imagined_y + yy))
			if (self.world.player.imagined_x + xx, self.world.player.imagined_y + yy + self.world.iterator_square.granularity) in self.up_unknown:
				self.up_unknown.remove((self.world.player.imagined_x + xx, self.world.player.imagined_y + yy + self.world.iterator_square.granularity))


	def update_nav_graph(self):


		#Update the RIGHT side of the screen
		if (self.world.player.imagined_x - self.last_update_x) >= self.world.iterator_square.granularity:
			x_remainder = self.world.player.imagined_x - self.last_update_x - self.world.iterator_square.granularity
			self.last_update_x = self.world.player.imagined_x - x_remainder

			yy_beginning = self.last_update_y - self.world.player.imagined_y
			
			xx = self.world.screen_width - self.world.iterator_square.granularity - x_remainder
			for yy in range(yy_beginning, self.world.screen_height + yy_beginning, self.world.iterator_square.granularity):
				self.world.iterator_square.rect.x = xx
				self.world.iterator_square.rect.y = yy

				in_view = self.world.get_all_in_view(self.world.collide_group)

				collided = False

				for dude in in_view:
					if self.world.iterator_square.rect.colliderect(dude.rect):
						collided = True

				if not collided:
					self.update_connections(self.nav_graph, xx, yy)
				else:
					self.update_connections(self.collide_graph, xx, yy)



		#Update the LEFT side of the screen
		if (self.world.player.imagined_x - self.last_update_x) <= -self.world.iterator_square.granularity:
			x_remainder = self.world.player.imagined_x - self.last_update_x + self.world.iterator_square.granularity
			self.last_update_x = self.world.player.imagined_x - x_remainder

			yy_beginning = self.last_update_y - self.world.player.imagined_y
			
			xx = 0 - x_remainder
			for yy in range(yy_beginning, self.world.screen_height + yy_beginning, self.world.iterator_square.granularity):
				self.world.iterator_square.rect.x = xx
				self.world.iterator_square.rect.y = yy

				in_view = self.world.get_all_in_view(self.world.collide_group)

				collided = False

				for dude in in_view:
					if self.world.iterator_square.rect.colliderect(dude.rect):
						collided = True

				if not collided:
					self.update_connections(self.nav_graph, xx, yy)

				else:
					self.update_connections(self.collide_graph, xx, yy)

		#Update the DOWN side of the screen
		if (self.world.player.imagined_y - self.last_update_y) >= self.world.iterator_square.granularity:
			y_remainder = self.world.player.imagined_y - self.last_update_y - self.world.iterator_square.granularity
			self.last_update_y = self.world.player.imagined_y - y_remainder

			xx_beginning = self.last_update_x - self.world.player.imagined_x
			
			yy = self.world.screen_height - self.world.iterator_square.granularity - y_remainder
			for xx in range(xx_beginning, self.world.screen_width + xx_beginning, self.world.iterator_square.granularity):
				self.world.iterator_square.rect.x = xx
				self.world.iterator_square.rect.y = yy

				in_view = self.world.get_all_in_view(self.world.collide_group)

				collided = False

				for dude in in_view:
					if self.world.iterator_square.rect.colliderect(dude.rect):
						collided = True

				if not collided:
					self.update_connections(self.nav_graph, xx, yy)
				else:
					self.update_connections(self.collide_graph, xx, yy)


		#Update the UP side of the screen
		if (self.world.player.imagined_y - self.last_update_y) <= -self.world.iterator_square.granularity:
			y_remainder = self.world.player.imagined_y - self.last_update_y + self.world.iterator_square.granularity
			self.last_update_y = self.world.player.imagined_y - y_remainder

			xx_beginning = self.last_update_x - self.world.player.imagined_x
			
			yy = 0 - y_remainder
			for xx in range(xx_beginning, self.world.screen_width + xx_beginning, self.world.iterator_square.granularity):
				self.world.iterator_square.rect.x = xx
				self.world.iterator_square.rect.y = yy

				in_view = self.world.get_all_in_view(self.world.collide_group)

				collided = False

				for dude in in_view:
					if self.world.iterator_square.rect.colliderect(dude.rect):
						collided = True

				if not collided:
					self.update_connections(self.nav_graph, xx, yy)
				else:
					self.update_connections(self.collide_graph, xx, yy)


		##### Uncoment these lines to print the navigational graphs being generated at fixed intervals

		# if (self.last_print == 0) or (self.last_print > 100):
		# 	self.last_print = 0
		# 	self.print_connected_components()
		# self.last_print += 1


	def negate_action(self, action):

		negated_actions = ['n', ' ', 's', 'w', 'd', 'a', 'sd', 'sa', 'wd', 'wa', 's', 'w', 'd', 'a', 'sd', 'sa', 'wd', 'wa']

		return negated_actions[ACTION_LIST.index(action)]




	def get_closest_node_to_position(self, x, y):

		


		possible_x = x - (x % self.world.iterator_square.granularity)
		possible_y = y - (y % self.world.iterator_square.granularity)

		if (possible_x, possible_y) in self.nav_graph:
			return (possible_x, possible_y)
		else:
			possible_x = x - (x % self.world.iterator_square.granularity) + self.world.iterator_square.granularity
			possible_y = y - (y % self.world.iterator_square.granularity)
			
			if (possible_x, possible_y) in self.nav_graph:
				return (possible_x, possible_y)
			else:
				possible_x = x - (x % self.world.iterator_square.granularity) + self.world.iterator_square.granularity
				possible_y = y - (y % self.world.iterator_square.granularity) + self.world.iterator_square.granularity
			
				if (possible_x, possible_y) in self.nav_graph:
					return (possible_x, possible_y)
				else:
					possible_x = x - (x % self.world.iterator_square.granularity)
					possible_y = y - (y % self.world.iterator_square.granularity) + self.world.iterator_square.granularity
				
					if (possible_x, possible_y) in self.nav_graph:
						return (possible_x, possible_y)
					else:
						raise PositionError((x,y))

						





	def get_collide_neighbors(self, node):

		collide_neighbors = []

		if (node[0] + self.world.iterator_square.granularity, node[1]) in self.collide_graph:
			collide_neighbors.append((node[0] + self.world.iterator_square.granularity, node[1]))
		if (node[0] - self.world.iterator_square.granularity, node[1]) in self.collide_graph:
			collide_neighbors.append((node[0] - self.world.iterator_square.granularity, node[1]))
		if (node[0], node[1] + self.world.iterator_square.granularity) in self.collide_graph:
			collide_neighbors.append((node[0], node[1] + self.world.iterator_square.granularity))
		if (node[0], node[1] - self.world.iterator_square.granularity) in self.collide_graph:
			collide_neighbors.append((node[0], node[1] - self.world.iterator_square.granularity))


		return collide_neighbors





	def get_unexplored_nodes(self):

		unexplored_nodes = []

		x = self.world.player.imagined_x + self.world.screen_width/2
		y = self.world.player.imagined_y + self.world.screen_height/2
		player_node = self.get_closest_node_to_position(x, y)

		components = nx.connected_components(self.nav_graph)

		player_component = None

		for component in components:
			if player_node in component:
				player_component = component


		for n in self.nav_graph:
			#print(n)
			
			if len(self.nav_graph[n]) >= 4:
				continue
			# print("Num Neighbors: ", len(self.nav_graph[n]))
			# print("Num Collidables: ", len(self.get_collide_neighbors(n)))
			if (len(self.get_collide_neighbors(n)) + len(self.nav_graph[n])) < 4:
				#if nx.has_path(self.nav_graph, n, player_node):
				if n in player_component:
					unexplored_nodes.append(n)


		#print("Unexplored nodes: ", unexplored_nodes)
		# for node in unexplored_nodes:
		# 	print("Node: ", node)
		# 	print("Path: ", nx.shortest_path(self.nav_graph, source=player_node, target=node))

		return unexplored_nodes




	def print_connected_components(self):

		print("--> Navigation Graphs:")
		print("Conected Components: ", nx.number_connected_components(self.nav_graph))

		pos = nx.get_node_attributes(self.nav_graph, 'pos')

		for h in [self.nav_graph.subgraph(c).copy() for c in nx.connected_components(self.nav_graph)]:
			nx.draw(h, pos, node_color='blue', node_size = 20)
			plt.show()

		print("--> Collision Graphs:")
		print("Conected Components: ", nx.number_connected_components(self.collide_graph))

		pos = nx.get_node_attributes(self.collide_graph, 'pos')

		for h in [self.collide_graph.subgraph(c).copy() for c in nx.connected_components(self.collide_graph)]:
			nx.draw(h, pos, node_color='red', node_size = 20)
			plt.show()




	def get_movement_from_direction(self, direction):

		if (direction < 22.5 and direction >= 0) or (direction <= 360 and direction > 337.5):
			action = 'd'
		elif (direction < 67.5 and direction >= 22.5):
			action = 'sd'
		elif (direction < 112.5 and direction >= 67.5):
			action = 's'
		elif (direction < 157.5 and direction >= 112.5):
			action = 'sa'
		elif (direction < 202.5 and direction >= 157.5):
			action = 'a'
		elif (direction < 247.5 and direction >= 202.5):
			action = 'wa'
		elif (direction < 292.5 and direction >= 247.5):
			action = 'w'
		elif (direction < 337.5 and direction >= 292.5):
			action = 'wd'
		else:
			print("Direction: ", direction)
			print("Error in directions!!!")
			exit()

		return action


	def go_to_node(self, node):

		x = self.world.player.imagined_x + self.world.screen_width/2
		y = self.world.player.imagined_y + self.world.screen_height/2
		player_node = self.get_closest_node_to_position(x, y)

		myradians = math.atan2(node[1] - player_node[1], node[0] - player_node[0])
		direction = math.degrees(myradians)

		while(direction > 360):
			direction -= 360

		while(direction < 0):
			direction += 360

		action = self.get_movement_from_direction(direction)

		# print("Going to Node!")
		# print("I'm here: ", player_node)
		# print("I want to go: ", node)
		# print("So I'm doing: ", action)

		return action

		

	def player_arrived_at_next_node(self):
		node = self.current_path[0]
		x = self.world.player.imagined_x + self.world.screen_width/2
		y = self.world.player.imagined_y + self.world.screen_height/2
		player_node = self.get_closest_node_to_position(x, y)
		distance = math.sqrt((player_node[0] - node[0])**2 + (player_node[1] - node[1])**2 )

		if distance < self.world.speed:
			return True
		else:
			return False




	def choose_node_to_explore(self, node_list):

		return random.choice(node_list)



	def explore(self):


		if self.previous_pos_x == self.world.player.imagined_x and self.previous_pos_y == self.world.player.imagined_y:
			self.stuck_counter += 1
		else:
			self.stuck_counter = 0

		if self.stuck_counter >= 3:
			self.stuck_counter = 0
			action = random.choice(MOVE_LIST)
			self.previous_action = action
			return action

		if self.last_update_x == None:
			self.create_graphs()
		else:
			self.update_nav_graph()

		if len(self.current_path) == 0:
			unknown_nodes = self.get_unexplored_nodes()

			if len(unknown_nodes) == 0:
				print("Nothing left to explore!")
				self.world_explored = 1
				return self.go_to_flower()
			else:
				chosen_node_to_explore = self.choose_node_to_explore(unknown_nodes)
				x = self.world.player.imagined_x + self.world.screen_width/2
				y = self.world.player.imagined_y + self.world.screen_height/2
				self.current_path = nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(x, y), target=chosen_node_to_explore)


		if self.player_arrived_at_next_node():
			del[self.current_path[0]]

			if len(self.current_path) == 0:
				unknown_nodes = self.get_unexplored_nodes()

				if len(unknown_nodes) == 0:
					print("Nothing left to explore!")
					self.world_explored = 1
					return self.go_to_flower()
				else:
					chosen_node_to_explore = self.choose_node_to_explore(unknown_nodes)
					x = self.world.player.imagined_x + self.world.screen_width/2
					y = self.world.player.imagined_y + self.world.screen_height/2
					self.current_path = nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(x, y), target=chosen_node_to_explore)

		action = self.go_to_node(self.current_path[0])


		self.previous_pos_x = self.world.player.imagined_x
		self.previous_pos_y = self.world.player.imagined_y

		
		return action




class RuleBasedAgent0(BasicAgent): #The Random
	
	
		
	def getAction(self):
		return random.choice(ACTION_LIST)



class RuleBasedAgent1(BasicAgent): #The Experimental

	def __init__(self, world):
		BasicAgent.__init__(self, world)
		
		
	def getAction(self):

		if self.enemies_in_view() > 0:
			return self.fight_closest()
		if self.flower_in_view():
			return self.explore()
		return self.explore()



class RuleBasedAgent2(BasicAgent): #Explores what is closest and goes to the flower when it is visible. Kills every enemy on sight

	def __init__(self, world):
		BasicAgent.__init__(self, world)

	def choose_node_to_explore(self, node_list):

		min_distance = float('inf')
		min_node = None

		for possible in node_list:
			player_x = self.world.player.imagined_x + self.world.screen_width/2
			player_y = self.world.player.imagined_y + self.world.screen_height/2
			distance = len(nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(player_x, player_y), target=possible))

			if distance < min_distance:
				min_distance = distance
				min_node = possible

		return min_node
		
		
	def getAction(self):
		

		if  self.enemies_in_view() > 0:
			distance, _, _ = self.closest_enemy()
			if distance < (self.world.screen_width/2 - 1.5*self.world.iterator_square.granularity):
				return self.fight_closest()
		if self.flower_in_view():
			return self.go_to_flower()

		return self.explore()







class RuleBasedAgent3(BasicAgent): #Explores everything first and then goes to the flower. Kills everyone on sight

	def __init__(self, world):
		BasicAgent.__init__(self, world)

	def choose_node_to_explore(self, node_list):

		min_distance = float('inf')
		min_node = None

		for possible in node_list:
			player_x = self.world.player.imagined_x + self.world.screen_width/2
			player_y = self.world.player.imagined_y + self.world.screen_height/2
			distance = len(nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(player_x, player_y), target=possible))

			if distance < min_distance:
				min_distance = distance
				min_node = possible

		return min_node
		
		
	def getAction(self):
		

		if  self.enemies_in_view() > 0:
			distance, _, _ = self.closest_enemy()
			if distance < (self.world.screen_width/2 - 1.5*self.world.iterator_square.granularity):
				#print("Fighting closest!")
				return self.fight_closest()

		if self.world_explored:
			return self.go_to_flower()

		try:
			return self.explore()
		except WorldExploredError as e:
			return self.go_to_flower()



class RuleBasedAgent4(BasicAgent): #Explores everything first and then goes to the flower. Kills everyone on sight. Collects all the coins

	def __init__(self, world):
		BasicAgent.__init__(self, world)

	def choose_node_to_explore(self, node_list):

		min_distance = float('inf')
		min_node = None

		for possible in node_list:
			player_x = self.world.player.imagined_x + self.world.screen_width/2
			player_y = self.world.player.imagined_y + self.world.screen_height/2
			distance = len(nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(player_x, player_y), target=possible))

			if distance < min_distance:
				min_distance = distance
				min_node = possible

		return min_node
		
		
	def getAction(self):
		

		if  self.enemies_in_view() > 0:
			distance, _, _ = self.closest_enemy()
			if distance < (self.world.screen_width/2 - 1.5*self.world.iterator_square.granularity):
				#print("Fighting closest!")
				return self.fight_closest()
		if self.coins_in_view() > 0:
			return self.go_to_closest_coin()
		if self.world_explored:
			return self.go_to_flower()

		try:
			return self.explore()
		except WorldExploredError as e:
			return self.go_to_flower()



class RuleBasedAgent5(BasicAgent): #Explores everything first and then goes to the flower. Kills everyone on sight. Collects all the coins. Gets cakes when under 100 health

	def __init__(self, world):
		BasicAgent.__init__(self, world)

	def choose_node_to_explore(self, node_list):

		min_distance = float('inf')
		min_node = None

		for possible in node_list:
			player_x = self.world.player.imagined_x + self.world.screen_width/2
			player_y = self.world.player.imagined_y + self.world.screen_height/2
			distance = len(nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(player_x, player_y), target=possible))

			if distance < min_distance:
				min_distance = distance
				min_node = possible

		return min_node
		
		
	def getAction(self):
		

		if  self.enemies_in_view() > 0:
			distance, _, _ = self.closest_enemy()
			if distance < (self.world.screen_width/2 - 1.5*self.world.iterator_square.granularity):
				#print("Fighting closest!")
				return self.fight_closest()
		if self.world.player.hp < self.world.player.max_hp and self.cakes_in_view() > 0:
			return self.go_to_closest_cake()
		if self.coins_in_view() > 0:
			return self.go_to_closest_coin()
		if self.world_explored:
			return self.go_to_flower()

		try:
			return self.explore()
		except WorldExploredError as e:
			return self.go_to_flower()


class RuleBasedAgent6(BasicAgent): #Goes to flower once found. Kills everyone on sight. Collects all the coins. Gets cakes when under 100 health

	def __init__(self, world):
		BasicAgent.__init__(self, world)

	def choose_node_to_explore(self, node_list):

		min_distance = float('inf')
		min_node = None

		for possible in node_list:
			player_x = self.world.player.imagined_x + self.world.screen_width/2
			player_y = self.world.player.imagined_y + self.world.screen_height/2
			distance = len(nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(player_x, player_y), target=possible))

			if distance < min_distance:
				min_distance = distance
				min_node = possible

		return min_node
		
		
	def getAction(self):
		

		if  self.enemies_in_view() > 0:
			distance, _, _ = self.closest_enemy()
			if distance < (self.world.screen_width/2 - 1.5*self.world.iterator_square.granularity):
				#print("Fighting closest!")
				return self.fight_closest()
		if self.flower_in_view():
			return self.go_to_flower()
		if self.world.player.hp < self.world.player.max_hp and self.cakes_in_view() > 0:
			return self.go_to_closest_cake()
		if self.coins_in_view() > 0:
			return self.go_to_closest_coin()
		try:
			return self.explore()
		except WorldExploredError as e:
			return self.go_to_flower()



class ParameterAgent(BasicAgent): #Behaviour depends on parameters


	def __init__(self, world, parameters):  #parameter_list
		BasicAgent.__init__(self, world)

		#####################
		#  PARAMETER LIST   #
		#####################
		
		# (explore_preference, flower_preference, kill_preference, coin_preference, cake_preference, randomness, cake_health_influence)

		self.parameter_list = parameters


	def choose_node_to_explore(self, node_list):

		min_distance = float('inf')
		min_node = None

		for possible in node_list:
			player_x = self.world.player.imagined_x + self.world.screen_width/2
			player_y = self.world.player.imagined_y + self.world.screen_height/2
			distance = len(nx.shortest_path(self.nav_graph, source = self.get_closest_node_to_position(player_x, player_y), target=possible))

			if distance < min_distance:
				min_distance = distance
				min_node = possible

		return min_node
		
		
	def getAction(self):

		explore_preference = self.parameter_list[0]/10 * (1 - self.world_explored)

		distance_closest_flower, closest_flower = self.closest_manhattan_sprite(self.world.flower_group)
		flower_preference = self.parameter_list[1] * (1/distance_closest_flower) + self.world_explored

		distance_closest_enemy, closest_enemy = self.closest_manhattan_sprite(self.world.enemy_group)
		kill_preference = self.parameter_list[2] * (1/distance_closest_enemy)

		distance_closest_coin, closest_coin = self.closest_manhattan_sprite(self.world.money_group)
		coin_preference = self.parameter_list[3] * (1/distance_closest_coin)

		distance_closest_cake, closest_cake = self.closest_manhattan_sprite(self.world.food_group)
		cake_preference = (self.parameter_list[4] * 1/distance_closest_cake) + (self.parameter_list[6]*((self.world.player.max_hp - self.world.player.hp) / self.world.player.max_hp)*(1/distance_closest_cake))

		randomness = self.parameter_list[5]/10

		pref_list = [explore_preference, flower_preference, kill_preference, coin_preference, cake_preference]

		index_max = pref_list.index(max(pref_list))

		is_max_list = np.zeros((len(pref_list), 1))

		is_max_list[index_max] = 1


		explore_probabiliy = (1 - randomness) * (explore_preference * (is_max_list[0] + randomness))  + 0.0000001 #this little value is added because the random.choices function can't deal with all probabilities being 0. When that happens, we decide that the agent should simply explore

		flower_probability = (1 - randomness) * (flower_preference * (is_max_list[1] + randomness))

		kill_probability = (1 - randomness) * (kill_preference * (is_max_list[2] + randomness))

		coin_probability = (1 - randomness) * (coin_preference * (is_max_list[3] + randomness))

		cake_probability = (1 - randomness) * (cake_preference * (is_max_list[4] + randomness))


		prob_list = [explore_probabiliy, flower_probability, kill_probability, coin_probability, cake_probability]


		function_list = [self.explore, self.go_to_flower, self.fight_closest, self.go_to_closest_coin, self.go_to_closest_cake]


		chosen_action = random.choices(function_list, weights = prob_list, k = 1)[0]

		#print(chosen_action)

		return chosen_action()







