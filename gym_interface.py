from flower_hunter import *
import time





class Env():

	action_space = ['n', ' ', 'w', 's', 'a', 'd', 'wa', 'wd', 'sa', 'sd', 'w ', 's ', 'a ', 'd ', 'wa ', 'wd ', 'sa ', 'sd ']

	def __init__(self, level, saving_data = False):

		pygame.init()

		logo = pygame.image.load("Images/30-30_samurai_ball_3.png")
		pygame.display.set_icon(logo)
		pygame.display.set_caption("Flower Hunter")

		self.map_height = 600
		self.map_width = 600

		self.saving_data = saving_data

		self.frame_rate = 0.0

		self.big_fontzy = pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 62)
		self.medium_fontzy = pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 32)
		self.small_fontzy =  pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 24)

		self.screeno = pygame.display.set_mode([self.map_width, self.map_height])

		self.map_name = level

		self.num_directions = 8 #Needs to be divisable by 8

	def reset(self):

		self.date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + "_" + str(random.randint(0, 1000))

		if self.saving_data:
			self.pos_file_path = "Traces/Gym_Bot_Position_" + self.map_name + "_" + self.date_time + ".txt"
			self.postextfile = open(self.pos_file_path, 'w')

		self.world = World(self.map_height, self.map_width, 20, self.map_name, self.small_fontzy)

		self.player = Player(self.world.screen_width/2 -15, self.world.screen_height/2 -15, self.world)
		self.world.player = self.player

		self.perceptor = Perceptor(self.world, math.inf, self.date_time, self.map_name, self.num_directions, saving_data = self.saving_data)
		self.world.perceptor = self.perceptor

		self.to_save_buffer = []

		self.last_sword_parameters = [12, -15, 0]

		self.world.timer = time.time()

		self.n_avoidance = 0

		self.action_list=[]

		self.counter = 0

		self.world.update()
		self.perceptor.update()

		self.last_score = 0
		self.last_kill = 0
		self.last_health = 100

		return self.perceptor.to_save_buffer[-1], None



	def step(self, action):

	

		self.last_update = time.time()

		self.world.pos_to_write.append(str(self.world.player.imagined_x) + "_" + str(self.world.player.imagined_y) + "\n")


		self.world.update()
		self.perceptor.update()

		#handle death
		if self.world.player.hp <= 0:
			
			self.world.player.hp = 0

			# save traces in file
			if self.saving_data:
				self.perceptor.write_to_file()
				for pos_to_write in self.world.pos_to_write:
					self.postextfile.write(pos_to_write)
				self.postextfile.close()

			return self.perceptor.to_save_buffer[-1], -10, True, None


		for flower in self.world.flower_group:

			if self.player.is_collided_with(flower):

				# save traces in file
				if self.saving_data:
					self.perceptor.write_to_file()
					for pos_to_write in self.world.pos_to_write:
						self.postextfile.write(pos_to_write)
					self.postextfile.close()

				return self.perceptor.to_save_buffer[-1], 10, True, None




		self.last_sword_parameters = set_sword_parameters(self.world, self.last_sword_parameters)	


		self.actions_to_save = [self.counter]

		if action == 'n':
			self.action_list.append(self.actions_to_save)
		else:
			for letter in action:
				self.actions_to_save.append(letter)
			self.action_list.append(self.actions_to_save)

		if action == 'n':
			self.world.shift_down = 0
			self.world.shift_up = 0
			self.world.shift_right = 0
			self.world.shift_left = 0


		elif action == ' ':

			self.world.shift_down = 0
			self.world.shift_up = 0
			self.world.shift_right = 0
			self.world.shift_left = 0
			swordy = Sword(self.world.player.rect.x + self.last_sword_parameters[0], self.world.player.rect.y + self.last_sword_parameters[1], self.world, self.last_sword_parameters[2])
			self.world.weapon_group.add(swordy)
			self.world.all_group.add(swordy)

		elif action == 'w':
			self.world.shift_down = 2
			self.world.shift_up = 0
			self.world.shift_right = 0
			self.world.shift_left = 0

		elif action == 's':
			self.world.shift_down = 0
			self.world.shift_up = 2
			self.world.shift_right = 0
			self.world.shift_left = 0

		elif action == 'a':
			self.world.shift_down = 0
			self.world.shift_up = 0
			self.world.shift_right = 2
			self.world.shift_left = 0

		elif action == 'd':
			self.world.shift_down = 0
			self.world.shift_up = 0
			self.world.shift_right = 0
			self.world.shift_left = 2

		elif action == 'wa':
			self.world.shift_down = 2
			self.world.shift_up = 0
			self.world.shift_right = 2
			self.world.shift_left = 0

		elif action == 'wd':
			self.world.shift_down = 2
			self.world.shift_up = 0
			self.world.shift_right = 0
			self.world.shift_left = 2

		elif action == 'sa':
			self.world.shift_down = 0
			self.world.shift_up = 2
			self.world.shift_right = 2
			self.world.shift_left = 0

		elif action == 'sd':
			self.world.shift_down = 0
			self.world.shift_up = 2
			self.world.shift_right = 0
			self.world.shift_left = 2

		elif action == 'w ':
			self.world.shift_down = 2
			self.world.shift_up = 0
			self.world.shift_right = 0
			self.world.shift_left = 0
			swordy = Sword(self.world.player.rect.x + self.last_sword_parameters[0], self.world.player.rect.y + self.last_sword_parameters[1], self.world, self.last_sword_parameters[2])
			self.world.weapon_group.add(swordy)
			self.world.all_group.add(swordy)

		elif action == 's ':
			self.world.shift_down = 0
			self.world.shift_up = 2
			self.world.shift_right = 0
			self.world.shift_left = 0
			swordy = Sword(self.world.player.rect.x + self.last_sword_parameters[0], self.world.player.rect.y + self.last_sword_parameters[1], self.world, self.last_sword_parameters[2])
			self.world.weapon_group.add(swordy)
			self.world.all_group.add(swordy)

		elif action == 'a ':
			self.world.shift_down = 0
			self.world.shift_up = 0
			self.world.shift_right = 2
			self.world.shift_left = 0
			swordy = Sword(self.world.player.rect.x + self.last_sword_parameters[0], self.world.player.rect.y + self.last_sword_parameters[1], self.world, self.last_sword_parameters[2])
			self.world.weapon_group.add(swordy)
			self.world.all_group.add(swordy)

		elif action == 'd ':
			self.world.shift_down = 0
			self.world.shift_up = 0
			self.world.shift_right = 0
			self.world.shift_left = 2
			swordy = Sword(self.world.player.rect.x + self.last_sword_parameters[0], self.world.player.rect.y + self.last_sword_parameters[1], self.world, self.last_sword_parameters[2])
			self.world.weapon_group.add(swordy)
			self.world.all_group.add(swordy)

		elif action == 'wa ':
			self.world.shift_down = 2
			self.world.shift_up = 0
			self.world.shift_right = 2
			self.world.shift_left = 0
			swordy = Sword(self.world.player.rect.x + self.last_sword_parameters[0], self.world.player.rect.y + self.last_sword_parameters[1], self.world, self.last_sword_parameters[2])
			self.world.weapon_group.add(swordy)
			self.world.all_group.add(swordy)

		elif action == 'wd ':
			self.world.shift_down = 2
			self.world.shift_up = 0
			self.world.shift_right = 0
			self.world.shift_left = 2
			swordy = Sword(self.world.player.rect.x + self.last_sword_parameters[0], self.world.player.rect.y + self.last_sword_parameters[1], self.world, self.last_sword_parameters[2])
			self.world.weapon_group.add(swordy)
			self.world.all_group.add(swordy)

		elif action == 'sa ':
			self.world.shift_down = 0
			self.world.shift_up = 2
			self.world.shift_right = 2
			self.world.shift_left = 0
			swordy = Sword(self.world.player.rect.x + self.last_sword_parameters[0], self.world.player.rect.y + self.last_sword_parameters[1], self.world, self.last_sword_parameters[2])
			self.world.weapon_group.add(swordy)
			self.world.all_group.add(swordy)

		elif action == 'sd ':
			self.world.shift_down = 0
			self.world.shift_up = 2
			self.world.shift_right = 0
			self.world.shift_left = 2
			swordy = Sword(self.world.player.rect.x + self.last_sword_parameters[0], self.world.player.rect.y + self.last_sword_parameters[1], self.world, self.last_sword_parameters[2])
			self.world.weapon_group.add(swordy)
			self.world.all_group.add(swordy)

		


		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				running = False

		

		while ((time.time() - self.last_update) < self.frame_rate):
			pass

		self.counter += 1

		reward = 0

		if self.last_score < int(self.perceptor.to_save_buffer[-1][17].replace('_','')):
			reward += 1
		if self.last_kill < int(self.perceptor.to_save_buffer[-1][18].replace('_','')):
			reward += 1
		if self.last_health > int(self.perceptor.to_save_buffer[-1][16].replace('_','')):
			reward -= 1
		elif self.last_health < int(self.perceptor.to_save_buffer[-1][16].replace('_','')):
			reward += 1

		self.last_score = int(self.perceptor.to_save_buffer[-1][17].replace('_',''))
		self.last_kill = int(self.perceptor.to_save_buffer[-1][18].replace('_',''))
		self.last_health = int(self.perceptor.to_save_buffer[-1][16].replace('_',''))


		return self.perceptor.to_save_buffer[-1], reward, False, None



	def render(self):
		self.world.render()
		pygame.display.flip()


	def close(self):
		pass



# The Main running function
def main():

	env = Env("Level3", saving_data = False)

	observation, info = env.reset()

	init_time = time.time()

	for i in range(20):
		#print(i)
		for j in range(100):

			#print(j)

			if random.randint(0,100)<30:
				observation, reward, done, info = env.step(random.choice(env.action_space))
			else:
				observation, reward, done, info = env.step("d")
			#env.render()
			if done:
				observation, info = env.reset()

		observation, info = env.reset()

	final_time = time.time() - init_time

	print("Done in: ", final_time)

	env.close()




# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	# call the main function
	main()








