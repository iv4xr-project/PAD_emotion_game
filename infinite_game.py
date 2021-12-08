import pygame
import time
import math
import random
import numpy as np
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import screen_messages
import glob
import predictor
import rule_based_agents


def get_center(sprite):
	return (sprite.rect.x + sprite.rect.width/2, sprite.rect.y + sprite.rect.height/2)



class Follower(pygame.sprite.Sprite):

	hp_provided = -5

	perception_distance = 200

	value = 1

	hp = 50

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		image_name = "Images/Dark_ghost.png"
		self.image = pygame.image.load(image_name)
		x_size, y_size = self.image.get_rect().size
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.x_size = x_size
		self.y_size = y_size
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.mask = pygame.mask.from_surface(self.image)
		self.world = world

	def collided(self):
		self.kill()



	def update(self):

		distance = math.sqrt((self.world.player.rect.x - self.rect.x )**2 + (self.world.player.rect.y - self.rect.y)**2 )

		if distance <= self.perception_distance:

			self.x_pos += (self.world.player.rect.x - self.x_pos)/distance

			self.y_pos += (self.world.player.rect.y - self.y_pos)/distance

			image_name = "Images/Dark_ghost.png"
			self.image = pygame.image.load(image_name)
			x_size, y_size = self.image.get_rect().size
			self.rect = pygame.Rect(self.x_pos, self.y_pos, x_size, y_size)
			self.x_size = x_size
			self.y_size = y_size
			self.mask = pygame.mask.from_surface(self.image)

		else:
			image_name = "Images/Tent_ghost.png"
			self.image = pygame.image.load(image_name)
			x_size, y_size = self.image.get_rect().size
			self.rect = pygame.Rect(self.x_pos, self.y_pos, x_size, y_size)
			self.x_size = x_size
			self.y_size = y_size
			self.mask = pygame.mask.from_surface(self.image)

		self.rect.x = self.x_pos

		self.rect.y = self.y_pos

		if self.world.player.is_collided_with(self):

			self.x_pos -= 8*(self.world.player.rect.x - self.x_pos)/distance

			self.y_pos -= 8*(self.world.player.rect.y - self.y_pos)/distance

			self.rect.x = self.x_pos

			self.rect.y = self.y_pos

			self.world.player.hp += self.hp_provided

		for weapon in self.world.weapon_group:
			if weapon.is_collided_with(self):
				self.hp -= weapon.damage

				self.world.player.damage_done += weapon.damage

				self.x_pos -= weapon.throwback*(self.world.player.rect.x - self.x_pos)/distance

				self.y_pos -= weapon.throwback*(self.world.player.rect.y - self.y_pos)/distance

				self.rect.x = self.x_pos

				self.rect.y = self.y_pos

		if self.hp <= 0:
			self.kill()
			self.world.player.enemy_killed += 1


			## Uncomment to have enemies drop raice cakes with a certain probability

			# number = random.randint(0,7)

			# if number == 0:
			# 	ricy = RiceCake(self.rect.x + 5, self.rect.y + 5, self.world)
			# 	self.world.food_group.add(ricy)
			# 	self.world.all_group.add(ricy)




class Player(pygame.sprite.Sprite):

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world
		self.max_hp = 100

		self.enemy_killed = 0

		self.hp = 100

		self.money = 0

		self.damage_done = 0

		self.imagined_x = 0
		self.imagined_y = 0

		self.image = pygame.image.load("Images/30-30_samurai_ball_3.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		screen.blit(self.image, self.rect)

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)




class Sword(pygame.sprite.Sprite):

	def __init__(self, x_pos, y_pos, world, angle):

		pygame.sprite.Sprite.__init__(self)
		self.world = world
		self.lifetime = 3
		self.angle = angle
		self.damage = 10
		self.throwback = 20

		self.image = pygame.transform.rotate(pygame.image.load("Images/sword.png"), self.angle)
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		screen.blit(self.image, self.rect)

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)

	def update(self):
		self.lifetime -= 1

		if self.lifetime <= 0:
			self.kill()


class Flower(pygame.sprite.Sprite):

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world


		self.image = pygame.image.load("Images/Flower.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		pass

	def get_pos(self):
		return self.rect.x, self.rect.y


class Money(pygame.sprite.Sprite):

	value = 1

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world

		self.money_provided = 1


		self.image = pygame.image.load("Images/money.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.rect = pygame.Rect(x_pos + 4, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		
		if self.is_collided_with(self.world.player):
			self.world.player.money += self.money_provided

			self.kill()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)

	def get_pos(self):
		return self.rect.x, self.rect.y





class RiceCake(pygame.sprite.Sprite):

	value = 1

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world

		self.hp_provided = 10


		self.image = pygame.image.load("Images/Rice_cake_20_20.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		
		if self.is_collided_with(self.world.player):
			self.world.player.hp += self.hp_provided

			if self.world.player.hp > self.world.player.max_hp:
				self.world.player.hp = self.world.player.max_hp

			self.kill()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)

	def get_pos(self):
		return self.rect.x, self.rect.y



class Tile(pygame.sprite.Sprite):

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world


		self.image = pygame.image.load("Images/30-30_red_ball.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		pass

	def get_pos(self):
		return self.rect.x, self.rect.y



class GrassTile(Tile):

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world

		number = random.randint(0,3)
		image_name = "Images/20-20_grass_square" + str(number) + ".png"
		self.image = pygame.image.load(image_name)
		x_size, y_size = self.image.get_rect().size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.x_size = x_size
		self.y_size = y_size
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)



class RockWall(Tile):

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world

		number = random.randint(0,3)
		image_name = "Images/20-20_rock_wall" + str(number) + ".png"
		self.image = pygame.image.load(image_name).convert_alpha()
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		pass



class Polygon(pygame.sprite.Sprite):

	def __init__(self, world, points, number):

		pygame.sprite.Sprite.__init__(self)
		self.world = world
		self.rect = (0,0)

		self.number = number

		self.points = points

	
		self.image = pygame.Surface((self.world.screen_width, self.world.screen_height), pygame.SRCALPHA)

		#self.image.set_alpha(0)

		pygame.draw.polygon(self.image, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), points)

		self.image = self.image.convert_alpha()

		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		pass



	def draw(self, screen):
		screen.blit(self.image, (0,0))




class Iterator_Square(pygame.sprite.Sprite):

	def __init__(self, world, granularity):

		self.world = world
		self.granularity = granularity

		self.rect = pygame.Rect(0, 0, self.granularity, self.granularity)

		self.image = pygame.Surface((self.granularity, self.granularity), pygame.SRCALPHA)

		pygame.draw.rect(self.image, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), self.rect)

		self.image = self.image.convert_alpha()

		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		screen.blit(self.image, (self.rect.x, self.rect.y))






class Perceptor(object):

	def __init__(self, world, frequency, date_time, map_name, num_directions):

		self.world = world
		self.player = world.player
		self.frequency = frequency
		self.num_directions = num_directions

		self.fader_can_write = False

		self.polygon_group = pygame.sprite.Group()

		self.create_polygons()

		


		self.distance_closest_enemy = float('inf')
		self.distance_closest_food_item = float('inf')
		self.distance_closest_money = float('inf')
		self.distance_to_objective = float('inf')
		self.number_enemies_view = 0
		self.number_food_item_view = 0
		self.number_money_view = 0
		self.sum_enemy_values = 0   #How dangerous an enemy is. The highest, the more dangerous the enemy
		self.sum_food_item_values = 0    #How valuable an item is. The highest, the more valuable the item
		self.sum_money_values = 0
		self.sum_value_slash_distance_enemies = 0
		self.sum_value_slash_distance_food_item = 0
		self.sum_value_slash_distance_money = 0
		self.seconds_since_enemy = 0
		self.seconds_since_food_item = 0
		self.seconds_since_money = 0

		self.max_distance = abs(math.sqrt((self.world.screen_width/2) ** 2 + (self.world.screen_height/2) ** 2))

		self.hp = self.player.hp
		self.kills = 0
		self.money = 0
		self.damage_done = 0

		self.to_save_buffer = []
		self.current_perceptions = []


		self.last_enemy_time = time.time()
		self.last_food_item_time = time.time()
		self.last_money_time = time.time()

		self.last_update = time.time()

		file_name = "Traces/Perceptor_" + map_name + "_" + date_time + ".txt"
		self.save_file = open(file_name,"w+")


	def create_polygons(self):

		if self.num_directions % 4 != 0:
			print("The variable num_directions must be divisible by 4!")
			exit()

		#Draw top polygons
		for i in range(int(self.num_directions/4)):
			self.polygon_group.add(Polygon(self.world, ((i*(self.world.screen_width/(self.num_directions/4)),0), ((i+1)*(self.world.screen_width/(self.num_directions/4)),0), get_center(self.player)), ((self.num_directions/4)/2 + i) ))

		#Draw left polygons
		for i in range(int(self.num_directions/4)):

			if i < (self.num_directions/4)/2:
				self.polygon_group.add(Polygon(self.world, ((0, self.world.screen_height - i*(self.world.screen_height/(self.num_directions/4))), (0, self.world.screen_height - (i+1)*(self.world.screen_height/(self.num_directions/4))), get_center(self.player)), ( self.num_directions*3/4 + (self.num_directions/4)/2 + i) ) )
			else:
				self.polygon_group.add(Polygon(self.world, ((0, self.world.screen_height - i*(self.world.screen_height/(self.num_directions/4))), (0, self.world.screen_height - (i+1)*(self.world.screen_height/(self.num_directions/4))), get_center(self.player)), (i - (self.num_directions/4)/2 ) ))


		#Draw right polygons
		for i in range(int(self.num_directions/4)):
			self.polygon_group.add(Polygon(self.world, ((self.world.screen_width, i*(self.world.screen_height/(self.num_directions/4))), (self.world.screen_width, (i+1)*(self.world.screen_height/(self.num_directions/4))), get_center(self.player)), ( self.num_directions/4 + (self.num_directions/4)/2 + i)))

		#Draw bottom polygons
		for i in range(int(self.num_directions/4)):
			self.polygon_group.add(Polygon(self.world, ((self.world.screen_width - i*(self.world.screen_width/(self.num_directions/4)), self.world.screen_width), (self.world.screen_width - (i+1)*(self.world.screen_width/(self.num_directions/4)), self.world.screen_width), get_center(self.player)), ( (self.num_directions*2)/4 + (self.num_directions/4)/2 + i)))







	def update(self):

		self.current_perceptions = []

		if (time.time() - self.last_update) > 1/self.frequency:

			previous_distance_closest_enemy = self.distance_closest_enemy
			self.number_enemies_view = 0
			self.sum_enemy_values = 0
			self.distance_closest_enemy = float('inf')
			self.sum_value_slash_distance_enemies = 0
			for enemy in self.world.enemy_group:
				if self.world.in_view(enemy):
					self.last_enemy_time = time.time()
					self.number_enemies_view += 1
					self.sum_enemy_values += enemy.value
					distance = math.sqrt((self.player.rect.x - enemy.rect.x )**2 + (self.player.rect.y - enemy.rect.y)**2 )
					self.sum_value_slash_distance_enemies += enemy.value*10/distance
					if distance < self.distance_closest_enemy:
						self.distance_closest_enemy = distance

			self.seconds_since_enemy = int(time.time() - self.last_enemy_time)


			previous_distance_closest_money = self.distance_closest_money
			self.number_money_view = 0
			self.sum_money_values = 0
			self.distance_closest_money = float('inf')
			self.sum_value_slash_distance_money = 0
			for money in self.world.money_group:
				if self.world.in_view(money):
					self.last_money_time = time.time()
					self.number_money_view += 1
					self.sum_money_values += money.value
					distance = math.sqrt((self.player.rect.x - money.rect.x )**2 + (self.player.rect.y - money.rect.y)**2 )
					self.sum_value_slash_distance_money += money.value*10/distance
					if distance < self.distance_closest_money:
						self.distance_closest_money = distance

			self.seconds_since_money = int(time.time() - self.last_money_time)						



			#updating distance_closest_food
			previous_distance_closest_food_item = self.distance_closest_food_item
			self.number_food_item_view = 0
			self.sum_food_item_values = 0
			self.distance_closest_food_item = float('inf')
			self.sum_value_slash_distance_food_item = 0
			for food in self.world.food_group:
				if self.world.in_view(food):
					self.last_food_item_time = time.time()
					self.number_food_item_view += 1
					self.sum_food_item_values += food.value
					distance = math.sqrt((self.player.rect.x - food.rect.x )**2 + (self.player.rect.y - food.rect.y)**2 )
					self.sum_value_slash_distance_food_item += food.value*10/distance
					if distance < self.distance_closest_food_item:
						self.distance_closest_food_item = distance

			self.seconds_since_food_item = int(time.time() - self.last_food_item_time)

			
			previous_distance_to_objective = self.distance_to_objective 
			for flower in self.world.flower_group:
				if self.world.in_view(flower):
					distance = math.sqrt((self.player.rect.x - flower.rect.x )**2 + (self.player.rect.y - flower.rect.y)**2 )
					self.distance_to_objective = distance

			self.hp = self.player.hp

			self.kills = self.player.enemy_killed

			self.money = self.player.money


			self.damage_done = self.world.player.damage_done


			#save data

			self.current_perceptions.append(str(self.distance_closest_enemy) + "_")  #
			self.current_perceptions.append(str(self.distance_closest_food_item) + "_")  #
			self.current_perceptions.append(str(self.distance_closest_money) + "_")
			self.current_perceptions.append(str(self.number_enemies_view) + "_")  #
			self.current_perceptions.append(str(self.number_food_item_view) + "_")  #
			self.current_perceptions.append(str(self.number_money_view) + "_")  #
			self.current_perceptions.append(str(self.sum_enemy_values) + "_") 
			self.current_perceptions.append(str(self.sum_food_item_values) + "_") 
			self.current_perceptions.append(str(self.sum_money_values) + "_")  
			self.current_perceptions.append(str(self.sum_value_slash_distance_enemies) + "_")  #
			self.current_perceptions.append(str(self.sum_value_slash_distance_food_item) + "_")  #
			self.current_perceptions.append(str(self.sum_value_slash_distance_money) + "_")
			self.current_perceptions.append(str(self.seconds_since_enemy) + "_")  #
			self.current_perceptions.append(str(self.seconds_since_food_item) + "_")  #
			self.current_perceptions.append(str(self.seconds_since_money) + "_")  #
			self.current_perceptions.append(str(self.distance_to_objective) + "_")  #
			self.current_perceptions.append(str(self.hp) + "_")  #
			self.current_perceptions.append(str(self.money) + "_")  #
			self.current_perceptions.append(str(self.kills) + "_")  #
			self.current_perceptions.append(str(self.damage_done) + "_")  # 
			


			#Neutrals
			#print("Neutrals")
			neutral_vec = self.get_perception_vec(self.world.collide_group)
			self.current_perceptions.append(str(neutral_vec.tolist())+ "_")

			#Desirables
			#print("Desirables")
			desirable_vec = self.get_perception_vec(self.world.money_group)
			self.current_perceptions.append(str(desirable_vec.tolist()) + "_")

			#Conditionals 
			#print("Conditionals")
			conditional_vec = self.get_perception_vec(self.world.food_group)
			self.current_perceptions.append(str(conditional_vec.tolist()) + "_")

			#Enemies
			#print("Enemies")
			enemies_vec = self.get_perception_vec(self.world.enemy_group)
			self.current_perceptions.append(str(enemies_vec.tolist()) + "_")

			#Objective
			#print("Objectives")
			objective_vec = self.get_perception_vec(self.world.flower_group)
			self.current_perceptions.append(str(objective_vec.tolist()))

			self.current_perceptions.append("\n")


			self.last_update = time.time()


			self.fader_can_write = True

			self.to_save_buffer.extend(self.current_perceptions)

	def get_perception_vec(self, relevant_group):

		myX, myY = get_center(self.player)

		dist_q_array = np.full((1, self.num_directions), 0)

		for poppy in relevant_group:

			# Checking if inside screen
			if (poppy.rect.x > -poppy.x_size) and (poppy.rect.x < self.world.screen_width) and (poppy.rect.y > -poppy.y_size) and (poppy.rect.y < self.world.screen_height):

				targetX, targetY = get_center(poppy)


				collided = pygame.sprite.spritecollide(poppy, self.polygon_group, False, pygame.sprite.collide_mask)

				#print("Have collided with:")
				for polly in collided:
					#print(polly.number)
					distance = math.hypot(targetX - myX, targetY - myY)
					
					if abs(self.max_distance - distance) > dist_q_array[0][int(polly.number)]:

							dist_q_array[0][int(polly.number)] = abs(self.max_distance - distance)
						

				# myradians = math.atan2(targetY - myY, targetX - myX)
				# # print("My radians: ", myradians)
				# pos_radians = myradians + math.pi
				# quadrant = int(pos_radians // ((2 * math.pi) / self.num_directions))
				# if quadrant == self.num_directions:
				# 	quadrant -= 1
				# distance = math.hypot(targetX - myX, targetY - myY)
				# # print(distance)

				# if abs(distance) <= self.max_distance:

				# 	if abs(self.max_distance - distance) > dist_q_array[0][quadrant]:

				# 		dist_q_array[0][quadrant] = abs(self.max_distance - distance)
				
			# print(type(poppy).__name__)
		#print(dist_q_array)
		return dist_q_array



	def write_to_file(self):

		for savvy in self.to_save_buffer:
			self.save_file.write(savvy)

		self.save_file.close()




	def render(self):




		distance_closest_enemy_rend = self.world.font.render("Distance to closest enemy: " + str(self.distance_closest_enemy), 1, (0,0,0))
		self.world.screen.blit(distance_closest_enemy_rend, (10, 50))

		distance_closest_food_item_rend = self.world.font.render("Distance to closest food/item: " + str(self.distance_closest_food_item), 1, (0,0,0))
		self.world.screen.blit(distance_closest_food_item_rend, (10, 70))

		distance_closest_money_rend = self.world.font.render("Distance to closest coin: " + str(self.distance_closest_money), 1, (0,0,0))
		self.world.screen.blit(distance_closest_money_rend, (10, 90))

		distance_to_objective_rend = self.world.font.render("Distance to objective: " + str(self.distance_to_objective), 1, (0,0,0))
		self.world.screen.blit(distance_to_objective_rend, (10, 110))

		number_enemies_view_rend = self.world.font.render("Number of enemies in view: " + str(self.number_enemies_view), 1, (0,0,0))
		self.world.screen.blit(number_enemies_view_rend, (10, 130))

		number_food_item_view_rend = self.world.font.render("Number of food/items in view: " + str(self.number_food_item_view), 1, (0,0,0))
		self.world.screen.blit(number_food_item_view_rend, (10, 150))

		number_money_view_rend = self.world.font.render("Number of coins in view: " + str(self.number_money_view), 1, (0,0,0))
		self.world.screen.blit(number_money_view_rend, (10, 170))

		sum_enemy_values_rend = self.world.font.render("Sum of enemy values: " + str(self.sum_enemy_values), 1, (0,0,0))
		self.world.screen.blit(sum_enemy_values_rend, (10, 190))

		sum_food_item_values_rend = self.world.font.render("Sum of food/item values: " + str(self.sum_food_item_values), 1, (0,0,0))
		self.world.screen.blit(sum_food_item_values_rend, (10, 210))

		sum_money_values_rend = self.world.font.render("Sum of coin values: " + str(self.sum_money_values), 1, (0,0,0))
		self.world.screen.blit(sum_money_values_rend, (10, 230))

		sum_value_slash_distance_enemies_rend = self.world.font.render("Sum of value/distance for all enemies: " + str(self.sum_value_slash_distance_enemies), 1, (0,0,0))
		self.world.screen.blit(sum_value_slash_distance_enemies_rend, (10, 250))

		sum_value_slash_distance_food_item_rend = self.world.font.render("Sum of value/distance for all food/items: " + str(self.sum_value_slash_distance_food_item), 1, (0,0,0))
		self.world.screen.blit(sum_value_slash_distance_food_item_rend, (10, 270))

		sum_value_slash_distance_money_rend = self.world.font.render("Sum of value/distance for all coins: " + str(self.sum_value_slash_distance_money), 1, (0,0,0))
		self.world.screen.blit(sum_value_slash_distance_money_rend, (10, 290))

		seconds_since_enemy_rend = self.world.font.render("Seconds since new enemy spotted: " + str(self.seconds_since_enemy), 1, (0,0,0))
		self.world.screen.blit(seconds_since_enemy_rend, (10, 310))

		seconds_since_food_item_rend = self.world.font.render("Seconds since new food/item spotted: " + str(self.seconds_since_food_item), 1, (0,0,0))
		self.world.screen.blit(seconds_since_food_item_rend, (10, 330))

		seconds_since_money_rend = self.world.font.render("Seconds since new coins spotted: " + str(self.seconds_since_money), 1, (0,0,0))
		self.world.screen.blit(seconds_since_money_rend, (10, 350))
	
		hp_rend = self.world.font.render("HP: " + str(self.hp), 1, (0,0,0))
		self.world.screen.blit(hp_rend, (10, 370))

		money_rend = self.world.font.render("Coins: " + str(self.money), 1, (0,0,0))
		self.world.screen.blit(money_rend, (10, 390))

		kills_rend = self.world.font.render("Kills: " + str(self.kills), 1, (0,0,0))
		self.world.screen.blit(kills_rend, (10, 410))

		damage_done_rend = self.world.font.render("Damage Done: " + str(self.damage_done), 1, (0,0,0))
		self.world.screen.blit(damage_done_rend, (10, 430))


		pygame.display.flip()



class World(object):


# WORLD TYPES:
# infinite
# load
# load infinite


	def __init__(self, screen_width, screen_height, tile_size, world_type, small_fontzy):


		self.speed = 5


		self.x_pos = 0
		self.y_pos = 0

		self.world_type = world_type

		self.timer = time.time()
		

		#0 -> not shifting
		#1 -> key to shift is pressed but the opposite key was pressed afterwards and has priority
		#2 -> shifting
		self.shift_left = 0
		self.shift_right = 0
		self.shift_up = 0
		self.shift_down = 0

		self.ticker = 0

		self.key_press_list = []

		self.key_press_to_write = []
		self.pos_to_write = []


		self.tile_size = tile_size

		self.all_group = pygame.sprite.Group()
		self.tile_group = pygame.sprite.Group()
		self.collide_group = pygame.sprite.Group()
		self.enemy_group = pygame.sprite.Group()
		self.food_group = pygame.sprite.Group()
		self.money_group = pygame.sprite.Group()
		self.flower_group = pygame.sprite.Group()
		self.weapon_group = pygame.sprite.Group()
		self.player = None

		self.screen_width = screen_width
		self.screen_height = screen_height

		self.grass_surface = None

		if self.world_type == "infinite":
			pass
			#TODO
			#self.matrix =  Matrix(int(self.screen_height/tile_size), int(self.screen_width/tile_size), self)
		elif self.world_type == "load infinite":
			pass
			# TODO
		else:
			self.load(self.world_type)


		self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
		self.font = small_fontzy
		self.last_food = time.time()

		self.iterator_square = Iterator_Square(self, 20)

		



	def load(self, file_name):

		file_path = "Maps/" + file_name + ".csv"

		f = open(file_path, "r")
		lines = f.readlines()

		player_x = 0
		player_y = 0



		self.grass_surface = pygame.Surface((len(lines[0])*self.tile_size, len(lines)*self.tile_size))

		self.grass_surface.fill((255,255,255))


		line_count = 0
		for line in lines:
			column_count = 0
			line = line.replace('	', '')
			line = line.replace(';', '')

			for letter in line:

				if letter == '.':

					tilly = GrassTile(column_count*self.tile_size, line_count*self.tile_size, self)
					self.tile_group.add(tilly)

				elif letter == '0':
					tilly = Flower(column_count*self.tile_size, line_count*self.tile_size, self)
					self.flower_group.add(tilly)
					self.all_group.add(tilly)
				elif letter == '\n':
					pass
				elif letter == ' ':
					pass
				elif letter == '	':
					pass		
				elif letter == '_':
					pass		
				elif letter == "r":
					ricy = RiceCake(column_count*self.tile_size + 5, line_count*self.tile_size + 5, self)
					self.food_group.add(ricy)
					self.all_group.add(ricy)
					tilly = GrassTile(column_count*self.tile_size, line_count*self.tile_size, self)
					self.tile_group.add(tilly)

				elif letter == "m":
					muuney = Money(column_count*self.tile_size, line_count*self.tile_size, self)
					self.money_group.add(muuney)
					self.all_group.add(muuney)
					tilly = GrassTile(column_count*self.tile_size, line_count*self.tile_size, self)
					self.tile_group.add(tilly)

				elif letter == 'f':
					new_follower = Follower(column_count*self.tile_size, line_count*self.tile_size, self)
					self.enemy_group.add(new_follower)
					self.all_group.add(new_follower)
					tilly = GrassTile(column_count*self.tile_size, line_count*self.tile_size, self)
					self.tile_group.add(tilly)

				elif letter == 'x':
					wally = RockWall(column_count*self.tile_size, line_count*self.tile_size, self)
					self.collide_group.add(wally)
					self.all_group.add(wally)
				elif letter == "p":
					player_x = column_count*self.tile_size
					player_y = line_count*self.tile_size


					# #To Remove
					# self.playerx = column_count*self.tile_size
					# self.playery = line_count*self.tile_size


					tilly = GrassTile(column_count*self.tile_size, line_count*self.tile_size, self)
					self.tile_group.add(tilly)



				column_count += 1
			line_count += 1

		for dudette in self.all_group:
			dudette.rect.x += self.screen_height/2 -15 - player_x
			dudette.rect.y += self.screen_width/2 -15 - player_y

		for tillete in self.tile_group:
			tillete.rect.x += self.screen_height/2 -15 - player_x
			tillete.rect.y += self.screen_width/2 -15 - player_y

		for folly in self.enemy_group:
			folly.x_pos += self.screen_height/2 -15 - player_x
			folly.y_pos += self.screen_width/2 -15 - player_y



		for grasser in self.tile_group:
			self.grass_surface.blit(grasser.image, grasser.rect)


	def check_x_movement(self):



		if self.shift_left == 2:

			for pop in self.collide_group:
				pop.rect.x = pop.rect.x - self.speed

			self.player.imagined_x += self.speed

			for poppy in self.collide_group:
				if self.player.is_collided_with(poppy):
					for pop in self.collide_group:
						pop.rect.x = pop.rect.x + self.speed
					self.player.imagined_x -= self.speed
					return


			for flower in self.flower_group:
				flower.rect.x = flower.rect.x - self.speed

			for enem in self.enemy_group:
				enem.x_pos = enem.x_pos - self.speed

			for food in self.food_group:
				food.rect.x = food.rect.x - self.speed

			for money in self.money_group:
				money.rect.x = money.rect.x - self.speed
			
		elif self.shift_right == 2:

			for pop in self.collide_group:
				pop.rect.x = pop.rect.x + self.speed

			self.player.imagined_x -= self.speed

			for poppy in self.collide_group:
				if self.player.is_collided_with(poppy):
					for pop in self.collide_group:
						pop.rect.x = pop.rect.x - self.speed
					self.player.imagined_x += self.speed
					return

			for flower in self.flower_group:
				flower.rect.x = flower.rect.x + self.speed


			for enem in self.enemy_group:
				enem.x_pos = enem.x_pos + self.speed

			for food in self.food_group:
				food.rect.x = food.rect.x + self.speed

			for money in self.money_group:
				money.rect.x = money.rect.x + self.speed

			
	def check_y_movement(self):


		if self.shift_up == 2:

			for pop in self.collide_group:
				pop.rect.y = pop.rect.y - self.speed

			self.player.imagined_y += self.speed

			for poppy in self.collide_group:
				if self.player.is_collided_with(poppy):
					for pop in self.collide_group:
						pop.rect.y = pop.rect.y + self.speed
					self.player.imagined_y -= self.speed
					return


			for flower in self.flower_group:
				flower.rect.y = flower.rect.y - self.speed

			for enem in self.enemy_group:
				enem.y_pos = enem.y_pos - self.speed

			for food in self.food_group:
				food.rect.y = food.rect.y - self.speed

			for money in self.money_group:
				money.rect.y = money.rect.y - self.speed
			
		elif self.shift_down == 2:

			for pop in self.collide_group:
				pop.rect.y = pop.rect.y + self.speed

			self.player.imagined_y -= self.speed

			for poppy in self.collide_group:
				if self.player.is_collided_with(poppy):
					for pop in self.collide_group:
						pop.rect.y = pop.rect.y - self.speed
					self.player.imagined_y += self.speed
					return

			for flower in self.flower_group:
				flower.rect.y = flower.rect.y + self.speed


			for enem in self.enemy_group:
				enem.y_pos = enem.y_pos + self.speed

			for food in self.food_group:
				food.rect.y = food.rect.y + self.speed

			for money in self.money_group:
				money.rect.y = money.rect.y + self.speed
			
	def in_view(self, sprity):

		if sprity.rect.x >= (0 - sprity.x_size) and sprity.rect.x <= self.screen_width and sprity.rect.y >= (0 - sprity.y_size) and sprity.rect.y <= self.screen_height:
			return True
		else:
			return False


	def get_all_in_view(self, sprite_group):

		in_view = []

		for sprity in sprite_group:
			if self.in_view(sprity):
				in_view.append(sprity)

		return in_view


	def update(self):

		self.key_press_list = []
		self.key_press_list.append(self.ticker)

		self.check_x_movement()

		self.check_y_movement()

		self.all_group.update()
		self.player.update()

		self.ticker += 1


	def update_matrix(self):
		pass



	def render(self):

		self.screen.fill((255,255,255))


		self.screen.blit(self.grass_surface, (-self.player.imagined_x,-self.player.imagined_y))
		self.collide_group.draw(self.screen)
		self.flower_group.draw(self.screen)
		self.food_group.draw(self.screen)
		self.money_group.draw(self.screen)
		self.enemy_group.draw(self.screen)
		self.weapon_group.draw(self.screen)
		self.player.draw(self.screen)



		self.iterator_square.draw(self.screen)




		hp_rend = self.font.render("HP: " + str(self.player.hp), 1, (0,0,0))
		self.screen.blit(hp_rend, (10, 10))

		money_rend = self.font.render("Coins: " + str(self.player.money), 1, (0,0,0))
		self.screen.blit(money_rend, (200, 10))

		kill_rend = self.font.render("Kills: " + str(self.player.enemy_killed), 1, (0,0,0))
		self.screen.blit(kill_rend, (310, 10))

		time_rend = self.font.render("Time: " + str(int(time.time() - self.timer)), 1, (0,0,0))
		self.screen.blit(time_rend, (400, 10))


############To Remove

		# zoomed_screen = pygame.transform.smoothscale(self.screen, (1500, 1500))

		# self.screen.blit(zoomed_screen, (0,0))






class Value_Point(pygame.sprite.Sprite):

	def __init__(self, world, x_pos, y_pos):

		pygame.sprite.Sprite.__init__(self)
		self.world = world
		self.image = pygame.image.load("Images/black_square_4.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		screen.blit(self.image, self.rect)

	def render(self):
		screen = self.world.screen
		self.draw(screen)





class LimitlessFader(pygame.sprite.Sprite):


	def __init__(self, world):

		self.world = world
		self.value_points_group = pygame.sprite.Group()

		self.rising = 0
		self.lowering = 0

		self.value = 0


	def update(self):

		value = 0

		if self.rising == 2:
			value = 1

		elif self.lowering == 2:
			value = -1

		for vally in self.value_points_group:
			vally.rect.x -= 1
			vally.rect.y += 3*value

		self.value += value

		new_square = Value_Point(self.world, self.world.screen_width - 100, self.world.screen_height/2 - 2)
		self.value_points_group.add(new_square)

	def render(self):

		for vally in self.value_points_group:
			vally.render()



	def normalize(self, value):

		#To implement

		return value












def handle_key_down(world, event_key, last_sword_parameters):



	if event_key == ord(' '):

		world.key_press_list.append(' ')
		swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
		world.weapon_group.add(swordy)
		world.all_group.add(swordy)

	if event_key == pygame.K_LEFT or event_key == ord('a'):

		world.key_press_list.append('ad')
		if world.shift_left == 2:

			world.shift_left = 1
			world.shift_right = 2
		else:
			world.shift_right = 2

	if event_key == pygame.K_RIGHT or event_key == ord('d'):

		world.key_press_list.append('dd')
		if world.shift_right == 2:

			world.shift_right = 1
			world.shift_left = 2
		else:
			world.shift_left = 2

	if event_key == pygame.K_UP or event_key == ord('w'):

		world.key_press_list.append('wd')
		if world.shift_up == 2:

			world.shift_up = 1
			world.shift_down = 2
		else:
			world.shift_down = 2

	if event_key == pygame.K_DOWN or event_key == ord('s'):

		world.key_press_list.append('sd')
		if world.shift_down == 2:

			world.shift_down = 1
			world.shift_up = 2
		else:
			world.shift_up = 2



def handle_key_up(world, event_key, last_sword_parameters):



	if event_key == pygame.K_LEFT or event_key == ord('a'):

		world.key_press_list.append('au')
		if world.shift_left == 1:
			world.shift_right = 0
			world.shift_left = 2
		else:
			world.shift_right = 0

	if event_key == pygame.K_RIGHT or event_key == ord('d'):

		world.key_press_list.append('du')
		if world.shift_right == 1:
			world.shift_left = 0
			world.shift_right = 2
		else:
			world.shift_left = 0

	if event_key == pygame.K_UP or event_key == ord('w'):

		world.key_press_list.append('wu')
		if world.shift_up == 1:
			world.shift_down = 0
			world.shift_up = 2
		else:
			world.shift_down = 0

	if event_key == pygame.K_DOWN or event_key == ord('s'):

		world.key_press_list.append('su')
		if world.shift_down == 1:
			world.shift_up = 0
			world.shift_down = 2
		else:
			world.shift_up = 0




def set_sword_parameters(world, last_sword_parameters):

	if world.shift_down == 2 and world.shift_right == 2:
			last_sword_parameters = [-8, -8, 45]

	elif world.shift_down == 2 and world.shift_left == 2:
		last_sword_parameters = [22, -8, 315]

	elif world.shift_up == 2 and world.shift_right == 2:
		last_sword_parameters = [-8, 22, 135]

	elif world.shift_up == 2 and world.shift_left == 2:
		last_sword_parameters = [22, 22, 225]

	elif world.shift_down == 2:
		last_sword_parameters = [12, -15, 0]
	elif world.shift_up == 2:
		last_sword_parameters = [12, 30, 180]
	elif world.shift_right == 2:
		last_sword_parameters = [-15, 12, 90]
	elif world.shift_left == 2:
		last_sword_parameters = [30, 12, 270]	

	return last_sword_parameters








def playing_routine(frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, date_time, num_directions):


	#variable to control the main loop
	running = True


	world = World(map_height, map_width, 20, map_name, small_fontzy)


	player = Player(world.screen_width/2 -15, world.screen_height/2 -15, world)
	world.player = player



	world.render()
	pygame.display.flip()

	player_dead = False

	player_won = False

	
	
	perceptor = Perceptor(world, 8, date_time, map_name, num_directions)

	file_path = "Traces/Actions_" + map_name + "_" + date_time + ".txt"

	pos_file_path = "Traces/Position_" + map_name + "_" + date_time + ".txt"

	textfile = open(file_path, 'w')

	postextfile = open(pos_file_path, 'w')

	last_sword_parameters = [30, 12, 270]

	world.timer = time.time()



	# main loop
	while running:

		last_update = time.time()


		world.key_press_to_write.append(str(world.key_press_list) + "\n")

		world.pos_to_write.append(str(world.player.imagined_x) + "_" + str(world.player.imagined_y) + "\n")



		world.update()
		perceptor.update()
		#perceptor.polygon_group.draw(world.screen)
		world.render()
		
		pygame.display.flip()
		#perceptor.render()

		


		#handle death
		if world.player.hp <= 0:
			
			
			world.player.hp = 0

			if player_dead == False:
				death_time = time.time()

			player_dead = True

			s = pygame.Surface((world.screen_width, world.screen_height)) 
			s.set_alpha(155)              
			s.fill((255,255,255))           
			world.screen.blit(s, (0,0)) 

			rend = big_fontzy.render("Morreu...", 1, (0,0,0))

			center_dist = int((map_width - big_fontzy.size("Morreu...")[0])/2)


			if center_dist < 0:
				print("Text Outside Screen")
				exit()

			world.screen.blit(rend, (center_dist, 100))


			pygame.display.flip()



			while (time.time() - death_time) < 1.5:


				for event in pygame.event.get():

					if event.type == pygame.QUIT:

						for to_write in world.key_press_to_write:
							textfile.write(to_write)

						for pos_to_write in world.pos_to_write:
							postextfile.write(pos_to_write)

						running = False


			rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

			center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


			if center_dist < 0:
				print("Text Outside Screen")
				exit()

			world.screen.blit(rend, (center_dist, 400))

			pygame.display.flip()

			while player_dead:

				for event in pygame.event.get():
					#
					if event.type == pygame.QUIT:
						
						running = False

						for to_write in world.key_press_to_write:
							textfile.write(to_write)

						for pos_to_write in world.pos_to_write:
							postextfile.write(pos_to_write)

						exit()

					if event.type == pygame.KEYDOWN:

						if event.key == ord(' '):

							for to_write in world.key_press_to_write:
								textfile.write(to_write)

							for pos_to_write in world.pos_to_write:
								postextfile.write(pos_to_write)

							textfile.close()

							postextfile.close()

							return file_path, pos_file_path



		last_sword_parameters = set_sword_parameters(world, last_sword_parameters)	


		for flower in world.flower_group:

			if player.is_collided_with(flower):

				if player_won == False:
					won_time = time.time()

				player_won = True

				s = pygame.Surface((world.screen_width, world.screen_height))  
				s.set_alpha(155)              
				s.fill((255,255,255))           
				world.screen.blit(s, (0,0)) 

				rend = big_fontzy.render("Sucesso!", 1, (0,0,0))

				center_dist = int((map_width - big_fontzy.size("Sucesso!")[0])/2)


				if center_dist < 0:
					print("Text Outside Screen")
					exit()

				world.screen.blit(rend, (center_dist, 100))


				pygame.display.flip()
				
				while (time.time() - won_time) < 1.5:


					for event in pygame.event.get():
						if event.type == pygame.QUIT:

							for to_write in world.key_press_to_write:
								textfile.write(to_write)

							for pos_to_write in world.pos_to_write:
								postextfile.write(pos_to_write)

							running = False


				rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

				center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


				if center_dist < 0:
					print("Text Outside Screen")
					exit()

				world.screen.blit(rend, (center_dist, 400))

				pygame.display.flip()

				while player_won:

					for event in pygame.event.get():
						
						if event.type == pygame.QUIT:
							running = False
							for to_write in world.key_press_to_write:
								textfile.write(to_write)

							for pos_to_write in world.pos_to_write:
								postextfile.write(pos_to_write)

							exit()

						if event.type == pygame.KEYDOWN:

							if event.key == ord(' '):

								for to_write in world.key_press_to_write:
									textfile.write(to_write)

								for pos_to_write in world.pos_to_write:
									postextfile.write(pos_to_write)

								textfile.close()

								postextfile.close()

								return file_path, pos_file_path


		for event in pygame.event.get():
			if event.type == pygame.QUIT:

				for to_write in world.key_press_to_write:
					textfile.write(to_write)

				for pos_to_write in world.pos_to_write:
					postextfile.write(pos_to_write)

				running = False


			if event.type == pygame.KEYDOWN:

				handle_key_down(world, event.key, last_sword_parameters)


			if event.type == pygame.KEYUP:
				
				handle_key_up(world, event.key, last_sword_parameters)


		while ((time.time() - last_update) < frame_rate):
			pass

	for to_write in world.key_press_to_write:
		textfile.write(to_write)

	for pos_to_write in world.pos_to_write:
		postextfile.write(pos_to_write)

	textfile.close()

	postextfile.close()

	return file_path, pos_file_path



def fader_replay(date_time, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, chosen_dimension, num_directions):


	#variable to control the main loop
	running = True

	read_path = "Traces/Actions_" + map_name + "_" + date_time + ".txt"

	if chosen_dimension == "Pleasure":

		save_path = "Traces/Pleasure_" + map_name + "_" + date_time + ".txt"

	elif chosen_dimension == "Dominance":

		save_path = "Traces/Dominance_" + map_name + "_" + date_time + ".txt"


	elif chosen_dimension == "Arousal":

		save_path = "Traces/Arousal_" + map_name + "_" + date_time + ".txt"


	world = World(map_height, map_width, 20, map_name, small_fontzy)

	player = Player(world.screen_width/2 -15, world.screen_height/2 -15, world)
	world.player = player

	perceptor = Perceptor(world, 8, date_time, map_name, num_directions)


	to_save_buffer = []


	faddy = LimitlessFader(world)







	world.render()


	player_dead = False
	player_won = False

	textfile = open(read_path, 'r')

	save_file = open(save_path, 'w')

	waiting = True



	s = pygame.Surface((world.screen_width, world.screen_height)) 
	s.set_alpha(155)        
	s.fill((255,255,255))          
	world.screen.blit(s, (0,0)) 


	rend = big_fontzy.render("Nível de " + chosen_dimension, 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Nível de " + chosen_dimension)[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	world.screen.blit(rend, (center_dist, 100))


	rend = small_fontzy.render("Prepare-se para auto-reportar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Prepare-se para auto-reportar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	world.screen.blit(rend, (center_dist, 250))


	 

	rend = small_fontzy.render("o seu nível de " + chosen_dimension, 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("o seu nível de " + chosen_dimension)[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	world.screen.blit(rend, (center_dist, 280))

	rend = small_fontzy.render("ao longo da sua travessia do nível.", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("ao longo da sua travessia do nível.")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	world.screen.blit(rend, (center_dist, 310))



	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	world.screen.blit(rend, (center_dist, 400))




	pygame.display.flip()

	faddy.render()

	while waiting:

		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:
			
				if event.key == ord(' '):
					waiting = False


	last_sword_parameters = [12, -15, 0]

	world.timer = time.time()



	while running:

		key_press_list = textfile.readline()

		#Transformation into list
		key_press_list = key_press_list.replace(']', '')
		key_press_list = key_press_list.replace('[', '')
		key_press_list = key_press_list.replace('\'', '')
		key_press_list = key_press_list.replace('\n', '')
		key_press_list = key_press_list.split(", ")




		last_update = time.time()


		world.update()
		perceptor.update()
		faddy.update()

		world.render()
		faddy.render()

		pygame.display.flip()


		#handle death
		if world.player.hp <= 0:
			
			
			world.player.hp = 0

			if player_dead == False:
				death_time = time.time()

			player_dead = True

			s = pygame.Surface((world.screen_width, world.screen_height))
			s.set_alpha(155)         
			s.fill((255,255,255))        
			world.screen.blit(s, (0,0)) 

			rend = big_fontzy.render("Obrigado!", 1, (0,0,0))

			center_dist = int((map_width - big_fontzy.size("Obrigado!")[0])/2)


			if center_dist < 0:
				print("Text Outside Screen")
				exit()

			world.screen.blit(rend, (center_dist, 100))


			pygame.display.flip()
			

			while (time.time() - death_time) < 1.5:


				for event in pygame.event.get():
					if event.type == pygame.QUIT:

						for savy in to_save_buffer:
							save_file.write(savy)

						perceptor.write_to_file()
						running = False


			rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

			center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


			if center_dist < 0:
				print("Text Outside Screen")
				exit()

			world.screen.blit(rend, (center_dist, 400))

			pygame.display.flip()


			while player_dead:

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						running = False

						for savy in to_save_buffer:
							save_file.write(savy)
						perceptor.write_to_file()

						exit()

					if event.type == pygame.KEYDOWN:

						if event.key == ord(' '):

							for savy in to_save_buffer:
								save_file.write(savy)

							perceptor.write_to_file()
							textfile.close()

							return save_path


		for flower in world.flower_group:

			if player.is_collided_with(flower):

				if player_won == False:
					won_time = time.time()

				player_won = True

				s = pygame.Surface((world.screen_width, world.screen_height))  
				s.set_alpha(155)              
				s.fill((255,255,255))          
				world.screen.blit(s, (0,0)) 

				rend = big_fontzy.render("Obrigado!", 1, (0,0,0))

				center_dist = int((map_width - big_fontzy.size("Sucesso!")[0])/2)


				if center_dist < 0:
					print("Text Outside Screen")
					exit()

				world.screen.blit(rend, (center_dist, 100))


				pygame.display.flip()
				

				while (time.time() - won_time) < 1.5:


					for event in pygame.event.get():

						if event.type == pygame.QUIT:

							for savy in to_save_buffer:
								save_file.write(savy)

							perceptor.write_to_file()

							running = False


				rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

				center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


				if center_dist < 0:
					print("Text Outside Screen")
					exit()

				world.screen.blit(rend, (center_dist, 400))

				pygame.display.flip()

				while player_won:

					for event in pygame.event.get():
						
						if event.type == pygame.QUIT:
							
							running = False

							for savy in to_save_buffer:
								save_file.write(savy)

							perceptor.write_to_file()

							exit()

						if event.type == pygame.KEYDOWN:

							if event.key == ord(' '):

								for savy in to_save_buffer:
									save_file.write(savy)

								perceptor.write_to_file()

								return save_path



		last_sword_parameters = set_sword_parameters(world, last_sword_parameters)	

		if len(key_press_list) == 0:
			
			textfile.close()
			return save_path



		if len(key_press_list) > 1:

			del key_press_list[0]

			for event in key_press_list:

				if event == ' ':
					handle_key_down(world, ord(' '), last_sword_parameters)

				elif event == 'wd':
					handle_key_down(world, ord('w'), last_sword_parameters)

				elif event == 'sd':
					handle_key_down(world, ord('s'), last_sword_parameters)

				elif event == 'ad':
					handle_key_down(world, ord('a'), last_sword_parameters)

				elif event == 'dd':
					handle_key_down(world, ord('d'), last_sword_parameters)
				elif event == 'wu':
					handle_key_up(world, ord('w'), last_sword_parameters)

				elif event == 'su':
					handle_key_up(world, ord('s'), last_sword_parameters)

				elif event == 'au':
					handle_key_up(world, ord('a'), last_sword_parameters)

				elif event == 'du':
					handle_key_up(world, ord('d'), last_sword_parameters)


				#handle_key_down(world, event.key, last_sword_parameters)



		# event handling, gets all event from the event queue
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_DOWN:

					faddy.lowering = 2

					if faddy.rising == 2:
						faddy.rising = 1


				elif event.key == pygame.K_UP:

					faddy.rising = 2

					if faddy.lowering == 2:
						faddy.lowering = 1
					

			if event.type == pygame.KEYUP:
				
				if event.key == pygame.K_DOWN:

					faddy.lowering = 0

					if faddy.rising == 1:
						faddy.rising = 2
					

				elif event.key == pygame.K_UP:

					faddy.rising = 0

					if faddy.lowering == 1:
						faddy.lowering = 2

	


		#save position of fader
		if perceptor.fader_can_write:

			to_save_buffer.append(str(faddy.normalize(faddy.value)) + "\n")
			
			perceptor.fader_can_write = False




		while ((time.time() - last_update) < frame_rate):
			pass



	for savy in to_save_buffer:
		save_file.write(savy)

	perceptor.write_to_file()

	textfile.close()

	return save_path





def replay_from_trace(file_location, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, num_directions):


	#variable to control the main loop
	running = True


	date_time = file_location[41:(len(file_location)-4)]

	read_path = file_location

	world = World(map_height, map_width, 20, map_name, small_fontzy)

	player = Player(world.screen_width/2 -15, world.screen_height/2 -15, world)
	world.player = player

	perceptor = Perceptor(world, math.inf, date_time, map_name, num_directions)

	to_save_buffer = []

	world.render()


	player_dead = False
	player_won = False

	textfile = open(read_path, 'r')



	s = pygame.Surface((world.screen_width, world.screen_height)) 
	s.set_alpha(155)        
	s.fill((255,255,255))          
	world.screen.blit(s, (0,0)) 


	pygame.display.flip()


	last_sword_parameters = [12, -15, 0]

	world.timer = time.time()


	while running:

		key_press_list = textfile.readline()

		if len(key_press_list) == 0:
			
			running = False
			break

		#Transformation into list
		key_press_list = key_press_list.replace(']', '')
		key_press_list = key_press_list.replace('[', '')
		key_press_list = key_press_list.replace('\'', '')
		key_press_list = key_press_list.replace('\n', '')
		key_press_list = key_press_list.split(", ")




		last_update = time.time()


		world.update()
		perceptor.update()

		world.render()
		#perceptor.polygon_group.draw(world.screen)
		pygame.display.flip()


		#handle death
		if world.player.hp <= 0:
			
			
			world.player.hp = 0

			if player_dead == False:
				death_time = time.time()

			player_dead = True

			s = pygame.Surface((world.screen_width, world.screen_height))
			s.set_alpha(155)         
			s.fill((255,255,255))        
			world.screen.blit(s, (0,0)) 

			pygame.display.flip()

			running = False
			break

		for flower in world.flower_group:

			if player.is_collided_with(flower):

				player_won = True

				s = pygame.Surface((world.screen_width, world.screen_height))  
				s.set_alpha(155)              
				s.fill((255,255,255))          
				world.screen.blit(s, (0,0)) 

				pygame.display.flip()
				
				running = False
				break




		last_sword_parameters = set_sword_parameters(world, last_sword_parameters)	

		if len(key_press_list) == 0:
			
			running = False
			break


		if len(key_press_list) > 1:

			del key_press_list[0]

			for event in key_press_list:

				if event == ' ':
					handle_key_down(world, ord(' '), last_sword_parameters)

				elif event == 'wd':
					handle_key_down(world, ord('w'), last_sword_parameters)

				elif event == 'sd':
					handle_key_down(world, ord('s'), last_sword_parameters)

				elif event == 'ad':
					handle_key_down(world, ord('a'), last_sword_parameters)

				elif event == 'dd':
					handle_key_down(world, ord('d'), last_sword_parameters)
				elif event == 'wu':
					handle_key_up(world, ord('w'), last_sword_parameters)

				elif event == 'su':
					handle_key_up(world, ord('s'), last_sword_parameters)

				elif event == 'au':
					handle_key_up(world, ord('a'), last_sword_parameters)

				elif event == 'du':
					handle_key_up(world, ord('d'), last_sword_parameters)


				#handle_key_down(world, event.key, last_sword_parameters)



		# event handling, gets all event from the event queue
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				running = False

		

		while ((time.time() - last_update) < frame_rate):
			pass



	perceptor.write_to_file()

	textfile.close()

	return










def email_files(files_to_email, date_time):

	mail_content = '''Hello,
	In this mail we are sending some attachments.
	The mail is sent using Python SMTP library.
	Thank You
	'''
	#The mail addresses and password
	sender_address = 'ADD_THE_SENDER_ADDRESS_HERE'   #This is set to use with a gmail account
	sender_pass = 'ADD_YOUR_PASSWORD_HERE'
	receiver_address = 'ADD_RECEIVER_ADDRESS_HERE'
	#Setup the MIME
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = date_time




	for file_name in files_to_email:

		#The body and the attachments for the mail
		message.attach(MIMEText(mail_content, 'plain'))
		attach_file_name = file_name
		attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
		payload = MIMEBase('text', '*', Name=attach_file_name)
		payload.set_payload((attach_file).read())
		encoders.encode_base64(payload) #encode the attachment
		#add payload header with filename
		payload.add_header('Content-Decomposition', 'attachment', filename = "texty.txt")
		message.attach(payload)




	#Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()
	print('Mail Sent')




def play_with_pre_trained_model(trained_model_file, date_time, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, num_directions):


	#variable to control the main loop
	running = True

	trained_model = predictor.load(trained_model_file)


	world = World(map_height, map_width, 20, map_name, small_fontzy)

	player = Player(world.screen_width/2 -15, world.screen_height/2 -15, world)
	world.player = player

	perceptor = Perceptor(world, math.inf, date_time, map_name, num_directions)

	to_save_buffer = []

	world.render()


	player_dead = False
	player_won = False

	s = pygame.Surface((world.screen_width, world.screen_height)) 
	s.set_alpha(155)        
	s.fill((255,255,255))          
	world.screen.blit(s, (0,0)) 


	pygame.display.flip()


	last_sword_parameters = [12, -15, 0]

	world.timer = time.time()

	n_avoidance = 0


	while running:


		last_update = time.time()


		world.update()
		perceptor.update()

		world.render()
		#perceptor.polygon_group.draw(world.screen)
		pygame.display.flip()


		#handle death
		if world.player.hp <= 0:
			
			
			world.player.hp = 0

			if player_dead == False:
				death_time = time.time()

			player_dead = True

			s = pygame.Surface((world.screen_width, world.screen_height))
			s.set_alpha(155)         
			s.fill((255,255,255))        
			world.screen.blit(s, (0,0)) 

			pygame.display.flip()

			running = False
			break

		for flower in world.flower_group:

			if player.is_collided_with(flower):

				player_won = True

				s = pygame.Surface((world.screen_width, world.screen_height))  
				s.set_alpha(155)              
				s.fill((255,255,255))          
				world.screen.blit(s, (0,0)) 

				pygame.display.flip()
				
				running = False
				break




		last_sword_parameters = set_sword_parameters(world, last_sword_parameters)	




##########
###########
############  The model logic needs to be here
		
		perceptions = perceptor.current_perceptions

		string_ver = ""

		for percy_jackson in perceptions:
			string_ver += percy_jackson

		inputs = string_ver


		action = predictor.behaviour_predict(inputs, trained_model)



		print(string_ver)
		print(action)

		if action == 'n':
			n_avoidance += 1
		else:
			n_avoidance = 0

		if n_avoidance >= 30:
			action = 'd'



		if action == 'n':
			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 0


		elif action == ' ':

			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'w':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 0

		elif action == 's':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 0
			world.shift_left = 0

		elif action == 'a':
			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 2
			world.shift_left = 0

		elif action == 'd':
			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 2

		elif action == 'wa':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 2
			world.shift_left = 0

		elif action == 'wd':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 2

		elif action == 'sa':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 2
			world.shift_left = 0

		elif action == 'sd':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 0
			world.shift_left = 2

		elif action == 'w ':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 's ':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 0
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'a ':
			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 2
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'd ':
			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 2
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'wa ':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 2
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'wd ':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 2
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'sa ':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 2
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'sd ':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 0
			world.shift_left = 2
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		




		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				running = False

		

		while ((time.time() - last_update) < frame_rate):
			pass



	perceptor.write_to_file()


	return









def play_with_agent(agent_type, date_time, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, num_directions):


	#variable to control the main loop
	running = True


	world = World(map_height, map_width, 20, map_name, small_fontzy)

	player = Player(world.screen_width/2 -15, world.screen_height/2 -15, world)
	world.player = player

	perceptor = Perceptor(world, math.inf, date_time, map_name, num_directions)

	world.perceptor = perceptor

	agent = agent_type(world)

	to_save_buffer = []

	world.render()


	player_dead = False
	player_won = False

	s = pygame.Surface((world.screen_width, world.screen_height)) 
	s.set_alpha(155)        
	s.fill((255,255,255))          
	world.screen.blit(s, (0,0)) 


	pygame.display.flip()


	last_sword_parameters = [12, -15, 0]

	world.timer = time.time()

	n_avoidance = 0


	while running:


		last_update = time.time()


		world.update()
		perceptor.update()

		world.render()
		#perceptor.polygon_group.draw(world.screen)
		pygame.display.flip()


		#handle death
		if world.player.hp <= 0:
			
			
			world.player.hp = 0

			if player_dead == False:
				death_time = time.time()

			player_dead = True

			s = pygame.Surface((world.screen_width, world.screen_height))
			s.set_alpha(155)         
			s.fill((255,255,255))        
			world.screen.blit(s, (0,0)) 

			pygame.display.flip()

			running = False
			break

		for flower in world.flower_group:

			if player.is_collided_with(flower):

				player_won = True

				s = pygame.Surface((world.screen_width, world.screen_height))  
				s.set_alpha(155)              
				s.fill((255,255,255))          
				world.screen.blit(s, (0,0)) 

				pygame.display.flip()
				
				running = False
				break




		last_sword_parameters = set_sword_parameters(world, last_sword_parameters)	




##########
###########
############  The model logic needs to be here
		
		perceptions = perceptor.current_perceptions


		action = agent.getAction()

		if action == 'n':
			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 0


		elif action == ' ':

			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'w':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 0

		elif action == 's':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 0
			world.shift_left = 0

		elif action == 'a':
			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 2
			world.shift_left = 0

		elif action == 'd':
			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 2

		elif action == 'wa':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 2
			world.shift_left = 0

		elif action == 'wd':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 2

		elif action == 'sa':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 2
			world.shift_left = 0

		elif action == 'sd':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 0
			world.shift_left = 2

		elif action == 'w ':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 's ':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 0
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'a ':
			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 2
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'd ':
			world.shift_down = 0
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 2
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'wa ':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 2
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'wd ':
			world.shift_down = 2
			world.shift_up = 0
			world.shift_right = 0
			world.shift_left = 2
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'sa ':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 2
			world.shift_left = 0
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		elif action == 'sd ':
			world.shift_down = 0
			world.shift_up = 2
			world.shift_right = 0
			world.shift_left = 2
			swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
			world.weapon_group.add(swordy)
			world.all_group.add(swordy)

		




		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				running = False

		

		while ((time.time() - last_update) < frame_rate):
			pass



	perceptor.write_to_file()


	return













# The Main running function
def main():


	pygame.init()


	logo = pygame.image.load("Images/30-30_samurai_ball_3.png")
	pygame.display.set_icon(logo)
	pygame.display.set_caption("Flower Hunter")

	files_to_email = ['student_number.txt']
	

	map_height = 600
	map_width = 600

	frame_rate = 0.0

	big_fontzy = pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 62)
	medium_fontzy = pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 32)
	small_fontzy =  pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 24)

	screeno = pygame.display.set_mode([map_width, map_height])




	date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + "_" + str(random.randint(0, 1000))


	



################################################################################################
#																							   #
#  Uncomment the following lines to replay the original experience used to gather the traces   #
#																							   #
################################################################################################

	# questions_file_path = "Answers/Answers_" + date_time + ".txt"
	# files_to_email.append(questions_file_path)
	# questions_file = open(questions_file_path,"w+")


	# dimensions_list = ["prazer", "excitação", "dominância"]

	# random.shuffle(dimensions_list)

	# chosen_dimension = dimensions_list[0]

	
	# screen_messages.consentimento(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)

	# screen_messages.recolha_dados(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)

	# screen_messages.questao_idade(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.questao_sexo(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.questao_1(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.questao_2(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.questao_3(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)


	# screen_messages.hello_screen(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)

	# screen_messages.introducao_ao_tutorial(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)

	# map_name = "Tutorial"

	# file_path, pos_file_path = playing_routine(frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, date_time)

	# if chosen_dimension == "Pleasure":
	# 	screen_messages.introducao_as_anotacoes_pleasure(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)

	# elif chosen_dimension == "Arousal":
	# 	screen_messages.introducao_as_anotacoes_arousal(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)

	# elif chosen_dimension == "Dominance":
	# 	screen_messages.introducao_as_anotacoes_dominance(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)


	# screen_messages.introducao_as_anotacoes_geral(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, chosen_dimension)

	# save_path = fader_replay(date_time, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, chosen_dimension)

	# screen_messages.obrigado_tutorial(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, chosen_dimension)

	# map_list = ["Level1", "Level2", "Level3"]

	# random.shuffle(map_list)

	# order_path = "Answers/Order_" + date_time + ".txt"
	# files_to_email.append(order_path)

	# order_write = open(order_path,"w+")

	# order_write.write(str(map_list))





	# nivel_1(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)

	# map_name =  map_list[0] 

	# perceptor_file_path = "Traces/Perceptor_" + map_name + "_" + date_time + ".txt"

	# file_path, pos_file_path = playing_routine(frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, date_time)

	# save_path = fader_replay(date_time, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, chosen_dimension)


	# files_to_email.append(file_path)

	# files_to_email.append(pos_file_path)

	# files_to_email.append(perceptor_file_path)

	# files_to_email.append(save_path)


	# screen_messages.scale_question_intro(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, chosen_dimension)

	# screen_messages.scale_question_explanation(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, chosen_dimension)

	# screen_messages.scale_question_1(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_2(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_3(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_4(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_5(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_6(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)






	# nivel_2(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)

	# map_name = map_list[1]


	# perceptor_file_path = "Traces/Perceptor_" + map_name + "_" + date_time + ".txt"

	# file_path, pos_file_path = playing_routine(frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, date_time)

	# save_path = fader_replay(date_time, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, chosen_dimension)

	# files_to_email.append(file_path)

	# files_to_email.append(pos_file_path)

	# files_to_email.append(perceptor_file_path)

	# files_to_email.append(save_path)


	# screen_messages.scale_question_intro(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, chosen_dimension)

	# screen_messages.scale_question_1(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_2(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_3(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_4(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_5(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_6(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)





	# nivel_3(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)

	# map_name = map_list[2]

	# perceptor_file_path = "Traces/Perceptor_" + map_name + "_" + date_time + ".txt"

	# file_path, pos_file_path = playing_routine(frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, date_time)

	# save_path = fader_replay(date_time, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, chosen_dimension)

	# files_to_email.append(file_path)

	# files_to_email.append(pos_file_path)

	# files_to_email.append(perceptor_file_path)

	# files_to_email.append(save_path)


	# screen_messages.scale_question_intro(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, chosen_dimension)

	# screen_messages.scale_question_1(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_2(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_3(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_4(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_5(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)

	# screen_messages.scale_question_6(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file)


	# screen_messages.inserir_numero_aluno(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)

	# questions_file.close()
	# order_write.close()


	### To use email, set the email and password on the "email_files" function

	## email_files(files_to_email, date_time)

	# screen_messages.obrigado(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width)





#############################################################################
#										                                    #
#  Uncomment the following lines for playing and annotating a single level  #
#										                                    #
#############################################################################

	# num_directions = 100


	# map_name = "Level3"

	# chosen_dimension = "Arousal"


	# file_path, pos_file_path = playing_routine(frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, date_time, num_directions)

	# save_path = fader_replay(date_time, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, chosen_dimension, num_directions)






#################################################################################################################
#								                                   		                                        #
#        Uncomment the following lines for playing all generated traces in the "Generated_Traces" folder        #
#                     (This will generate the perception traces in the "Traces" folder)                         #
#										                                                                        #
#################################################################################################################



	# gen_traces = sorted(glob.glob("./Generated_Traces/*.txt"))

	# num_directions = 100

	# frame_rate = 0.0

	# for genny in gen_traces:

	# 	file_location = genny

	# 	map_name = genny[34:40]

	# 	replay_from_trace(file_location, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, num_directions)

#################################################################################################################
#								                                   		                                        #
#        Uncomment the following lines for playing with a previously trained behavioural model                  #
#                                                                                                               #
#										                                                                        #
#################################################################################################################



	# map_name = "Level1"

	# num_directions = 100

	# trained_model_file = 'trained_forest.pkl'


	# play_with_pre_trained_model(trained_model_file, date_time, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, num_directions)

#################################################################################################################
#								                                   		                                        #
#                     Uncomment the following lines for playing with an agent                                   #
#                                                                                                               #
#										                                                                        #
#################################################################################################################


	map_name = "Level2"

	num_directions = 200 #Needs to be divisable by 8

	agent_type = rule_based_agents.ParameterAgent



	play_with_agent(agent_type, date_time, frame_rate, map_name, map_height, map_width, small_fontzy, medium_fontzy, big_fontzy, num_directions)





			 
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	# call the main function
	main()















