import pygame
from screen_messages import TextInputBox
import os
from os.path import exists
import math

# --- constants --- (UPPER_CASE names)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLACK = (0,   0,   0)
BLUE = (0, 100, 200)
BRIGHT_BLUE = (0, 150, 255)
TEAL = (0,128,128)
BRIGHT_TEAL = (0,198,198)
PURPLE = (128,0,128)
BRIGHT_PURPLE = (198,0,198)
OLIVE = (128,128,0)
BRIGHT_OLIVE = (198,198,0)

GREEN = (0,230,0)

FPS = 100

# --- classses --- (CamelCase names)

# empty

# --- functions --- (lower_case names)

# empty

# --- main ---

# - init -

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen_rect = screen.get_rect()

pygame.display.set_caption("Experience Barcode Creation")

borders = 100 #pixels

num_rectangles = 20
rec_size = ((SCREEN_WIDTH - 2*borders)/num_rectangles)/3

POSSIBLE_NUM_SQUARES = [4,5,8,10,20,25,40,50]




# - objects -


pleasure_list = []

for i in range(num_rectangles):

	pleasure_list.append(pygame.rect.Rect(borders + i *(rec_size*3) + 0*rec_size, borders, rec_size, SCREEN_HEIGHT - borders*2 - rec_size))

arousal_list = []

for i in range(num_rectangles):

	arousal_list.append(pygame.rect.Rect(borders + i *(rec_size*3) + 1*rec_size, borders, rec_size, SCREEN_HEIGHT - borders*2 - rec_size))

dominance_list = []

for i in range(num_rectangles):

	dominance_list.append(pygame.rect.Rect(borders + i *(rec_size*3) + 2*rec_size, borders, rec_size, SCREEN_HEIGHT - borders*2 - rec_size))
	
# - mainloop -

clock = pygame.time.Clock()

running = True

dragging = False
dragging_gran_bar = False

drag_bar_for_granularity = pygame.rect.Rect(25, 300, 50, 30)
drag_bar_line = pygame.rect.Rect(45, borders + 50, 10, SCREEN_HEIGHT - borders*2 - 50*2)

save_button_height = 50
save_button_width = 100
save_button = pygame.rect.Rect(SCREEN_WIDTH - borders - save_button_width, SCREEN_HEIGHT - borders + (borders - save_button_height)/2, save_button_width, save_button_height)
save_button_colour = BRIGHT_BLUE

small_fontzy =  pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 24)
save_file_name_input = TextInputBox(100, 530, 400, small_fontzy)
text_group = pygame.sprite.Group(save_file_name_input )


pad_button_height = 50
pad_button_width = 150
P_button = pygame.rect.Rect(borders - 25, borders - pad_button_height - (borders - pad_button_height)/2, pad_button_width, pad_button_height)
P_button_colour = TEAL
A_button = pygame.rect.Rect(SCREEN_WIDTH/2 - pad_button_width/2 - 25, borders - pad_button_height - (borders - pad_button_height)/2, pad_button_width, pad_button_height)
A_button_colour = PURPLE
D_button = pygame.rect.Rect(SCREEN_WIDTH - borders - pad_button_width - 25, borders - pad_button_height - (borders - pad_button_height)/2, pad_button_width, pad_button_height)
D_button_colour = OLIVE


on_off_button_width = 50
on_off_button_height = save_button_height

P_on = True
P_on_off_button = pygame.rect.Rect(borders + pad_button_width - 25, borders - pad_button_height - (borders - pad_button_height)/2, on_off_button_width, on_off_button_height)

A_on = True
A_on_off_button = pygame.rect.Rect(SCREEN_WIDTH/2 - pad_button_width/2 + pad_button_width - 25, borders - pad_button_height - (borders - pad_button_height)/2, on_off_button_width, on_off_button_height)

D_on = True
D_on_off_button = pygame.rect.Rect(SCREEN_WIDTH - borders - pad_button_width + pad_button_width - 25, borders - pad_button_height - (borders - pad_button_height)/2, on_off_button_width, on_off_button_height)



P_active = True
A_active = False
D_active = False


no_file_name_error = False
file_name_already_in_use_error = False


while running:

	# - events -

	events = pygame.event.get()

	for event in events:
		if event.type == pygame.QUIT:
			running = False


		elif event.type == pygame.MOUSEBUTTONDOWN:
			dragging = True
			if event.button == 1:

				if save_button.collidepoint(event.pos):

					if save_file_name_input.text == "":
						no_file_name_error = True
						file_name_already_in_use_error = False
					else:
						file_path = "./Experience_Barcodes/" + save_file_name_input.text + ".txt"

						if exists(file_path):
							file_name_already_in_use_error = True
							no_file_name_error = False
							continue

						f = open(file_path, 'w+')


						binary_pleasure_list = []
						for square_line in pleasure_list:
							if square_line.height > rec_size:
								binary_pleasure_list.append(1)
							else:
								binary_pleasure_list.append(0)
						f.write("P: ")
						f.write(str(binary_pleasure_list))
						f.write("\n")

						binary_arousal_list = []
						for square_line in arousal_list:
							if square_line.height > rec_size:
								binary_arousal_list.append(1)
							else:
								binary_arousal_list.append(0)
						f.write("A: ")
						f.write(str(binary_arousal_list))
						f.write("\n")

						binary_dominance_list = []
						for square_line in dominance_list:
							if square_line.height > rec_size:
								binary_dominance_list.append(1)
							else:
								binary_dominance_list.append(0)
						f.write("D: ")
						f.write(str(binary_dominance_list))
						f.write("\n")
						running = False
						continue

				if P_button.collidepoint(event.pos):
					P_active = True
					A_active = False
					D_active = False
					P_button_colour = BRIGHT_TEAL
					A_button_colour = PURPLE
					D_button_colour = OLIVE
				elif A_button.collidepoint(event.pos):
					P_active = False
					A_active = True
					D_active = False
					P_button_colour = TEAL
					A_button_colour = BRIGHT_PURPLE
					D_button_colour = OLIVE
				elif D_button.collidepoint(event.pos):
					P_active = False
					A_active = False
					D_active = True
					P_button_colour = TEAL
					A_button_colour = PURPLE
					D_button_colour = BRIGHT_OLIVE

				if P_on_off_button.collidepoint(event.pos):
					P_on = not P_on
				if A_on_off_button.collidepoint(event.pos):
					A_on = not A_on
				if D_on_off_button.collidepoint(event.pos):
					D_on = not D_on


				mouse_x, mouse_y = event.pos

				if drag_bar_for_granularity.collidepoint(event.pos):
					dragging_gran_bar = True
					if mouse_y > borders + 50 and mouse_y < SCREEN_HEIGHT - borders - 50:
						drag_bar_for_granularity.y = mouse_y - drag_bar_for_granularity.height/2

				if mouse_y > borders and mouse_y < SCREEN_HEIGHT-borders:

					if P_active:
						pad_list = pleasure_list
					elif A_active:
						pad_list = arousal_list
					elif D_active:
						pad_list = dominance_list

					for square_line in pad_list:
						if mouse_x >= square_line.x and mouse_x < square_line.x + rec_size:
							if mouse_y > SCREEN_HEIGHT/2:
								square_line.y = SCREEN_HEIGHT - borders - rec_size
								square_line.height = rec_size
							else:
								square_line.y = borders
								square_line.height = SCREEN_HEIGHT - borders*2 - rec_size

		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:    
				dragging = False
				dragging_gran_bar = False

		elif event.type == pygame.MOUSEMOTION:
			
			if save_button.collidepoint(event.pos):
				save_button_colour = BLUE
			else:
				save_button_colour = BRIGHT_BLUE

			if P_button.collidepoint(event.pos):
				P_button_colour = BRIGHT_TEAL
			else:
				P_button_colour = TEAL
			if A_button.collidepoint(event.pos):
				A_button_colour = BRIGHT_PURPLE
			else:
				A_button_colour = PURPLE
			if D_button.collidepoint(event.pos):
				D_button_colour = BRIGHT_OLIVE
			else:
				D_button_colour = OLIVE

			mouse_x, mouse_y = event.pos

			if dragging_gran_bar:
				if mouse_y > borders + 50 and mouse_y < SCREEN_HEIGHT - borders - 50:
					drag_bar_for_granularity.y = mouse_y - drag_bar_for_granularity.height/2
					max_y = drag_bar_line.height + drag_bar_line.y
					min_y = drag_bar_line.y

					num_rectangles = min(POSSIBLE_NUM_SQUARES, key=lambda x: abs(x - (61 - math.ceil(abs(((drag_bar_for_granularity.y + drag_bar_for_granularity.height/2) - min_y)/(max_y - min_y))*60))))


			if dragging and not dragging_gran_bar:
				if mouse_y > borders and mouse_y < SCREEN_HEIGHT-borders:
					if P_active:
						pad_list = pleasure_list
					elif A_active:
						pad_list = arousal_list
					elif D_active:
						pad_list = dominance_list
					for square_line in pad_list:
						if mouse_x >= square_line.x and mouse_x < square_line.x + rec_size:
							if mouse_y > SCREEN_HEIGHT/2:
								square_line.y = SCREEN_HEIGHT - borders - rec_size
								square_line.height = rec_size
							else:
								square_line.y = borders
								square_line.height = SCREEN_HEIGHT - borders*2 - rec_size




	rec_size = ((SCREEN_WIDTH - 2*borders)/num_rectangles)/3




	if num_rectangles > len(pleasure_list):

		for k in range(len(pleasure_list)):
			pleasure_list[k].x = borders + k *(rec_size*3) + 0*rec_size
			if pleasure_list[k].y < SCREEN_HEIGHT/2:
				pleasure_list[k].height = SCREEN_HEIGHT - borders*2 - rec_size
				pleasure_list[k].y = borders
			else:
				pleasure_list[k].height = rec_size
				pleasure_list[k].y = SCREEN_HEIGHT - borders - rec_size
			pleasure_list[k].width = rec_size
		for j in range(len(pleasure_list), num_rectangles):
			pleasure_list.append(pygame.rect.Rect(borders + j *(rec_size*3) + 0*rec_size, borders, rec_size, SCREEN_HEIGHT - borders*2 - rec_size))

		for k in range(len(arousal_list)):
			arousal_list[k].x = borders + k *(rec_size*3) + 1*rec_size
			if arousal_list[k].y < SCREEN_HEIGHT/2:
				arousal_list[k].height = SCREEN_HEIGHT - borders*2 - rec_size
				arousal_list[k].y = borders
			else:
				arousal_list[k].height = rec_size
				arousal_list[k].y = SCREEN_HEIGHT - borders - rec_size
			arousal_list[k].width = rec_size
		for j in range(len(arousal_list), num_rectangles):
			arousal_list.append(pygame.rect.Rect(borders + j *(rec_size*3) + 1*rec_size, borders, rec_size, SCREEN_HEIGHT - borders*2 - rec_size))

		for k in range(len(dominance_list)):
			dominance_list[k].x = borders + k *(rec_size*3) + 2*rec_size
			if dominance_list[k].y < SCREEN_HEIGHT/2:
				dominance_list[k].height = SCREEN_HEIGHT - borders*2 - rec_size
				dominance_list[k].y = borders
			else:
				dominance_list[k].height = rec_size
				dominance_list[k].y = SCREEN_HEIGHT - borders - rec_size
			dominance_list[k].width = rec_size
		for j in range(len(dominance_list), num_rectangles):
			dominance_list.append(pygame.rect.Rect(borders + j *(rec_size*3) + 2*rec_size, borders, rec_size, SCREEN_HEIGHT - borders*2 - rec_size))

	elif num_rectangles < len(pleasure_list):
		for k in range(num_rectangles):
			pleasure_list[k].x = borders + k *(rec_size*3) + 0*rec_size
			if pleasure_list[k].y < SCREEN_HEIGHT/2:
				pleasure_list[k].height = SCREEN_HEIGHT - borders*2 - rec_size
				pleasure_list[k].y = borders
			else:
				pleasure_list[k].height = rec_size
				pleasure_list[k].y = SCREEN_HEIGHT - borders - rec_size
			pleasure_list[k].width = rec_size
		for k in range(num_rectangles):
			arousal_list[k].x = borders + k *(rec_size*3) + 1*rec_size
			if arousal_list[k].y < SCREEN_HEIGHT/2:
				arousal_list[k].height = SCREEN_HEIGHT - borders*2 - rec_size
				arousal_list[k].y = borders
			else:
				arousal_list[k].height = rec_size
				arousal_list[k].y = SCREEN_HEIGHT - borders - rec_size
			arousal_list[k].width = rec_size
		for k in range(num_rectangles):
			dominance_list[k].x = borders + k *(rec_size*3) + 2*rec_size
			if dominance_list[k].y < SCREEN_HEIGHT/2:
				dominance_list[k].height = SCREEN_HEIGHT - borders*2 - rec_size
				dominance_list[k].y = borders
			else:
				dominance_list[k].height = rec_size
				dominance_list[k].y = SCREEN_HEIGHT - borders - rec_size
			dominance_list[k].width = rec_size

		pleasure_list = pleasure_list[:num_rectangles]
		arousal_list = arousal_list[:num_rectangles]
		dominance_list = dominance_list[:num_rectangles]



	screen.fill(WHITE)

	rend = small_fontzy.render("File Name:", 1, (0,0,0))

	screen.blit(rend, (100, 500))


	if no_file_name_error:
		rend = small_fontzy.render("Please insert a name for the save file", 1, RED)
		screen.blit(rend, (int(SCREEN_WIDTH - small_fontzy.size("Please insert a name for the save file.") - borders), 500))

	if file_name_already_in_use_error:
		rend = small_fontzy.render("File name already in use", 1, RED)
		screen.blit(rend, (int(SCREEN_WIDTH - small_fontzy.size("File name already in use") - borders), 500))



	text_group.update(events)
							
	text_group.draw(screen)

	if P_on:
		for square_line in pleasure_list:
			if not A_on and not D_on:
				square_line.width = rec_size * 3
			else:
				square_line.width = rec_size
			pygame.draw.rect(screen, TEAL, square_line)

	if A_on:
		for square_line in arousal_list:
			if not P_on and not D_on:
				square_line.width = rec_size * 3
			else:
				square_line.width = rec_size
			pygame.draw.rect(screen, PURPLE, square_line)

	if D_on:
		for square_line in dominance_list:
			if not A_on and not P_on:
				square_line.width = rec_size * 3
			else:
				square_line.width = rec_size
			pygame.draw.rect(screen, OLIVE, square_line)

	pygame.draw.rect(screen, save_button_colour, save_button)


	if not P_on:
		P_active = False
	if not A_on:
		A_active = False
	if not D_on:
		D_active = False

	if P_on and not A_on and not D_on:
		P_active = True
		A_active = False
		D_active = False
	elif not P_on and A_on and not D_on:
		P_active = False
		A_active = True
		D_active = False
	elif not P_on and not A_on and D_on:
		P_active = False
		A_active = False
		D_active = True



	if P_active:
		P_button_colour = BRIGHT_TEAL
	elif A_active:
		A_button_colour = BRIGHT_PURPLE
	elif D_active:
		D_button_colour = BRIGHT_OLIVE




	pygame.draw.rect(screen, P_button_colour, P_button)
	rend = small_fontzy.render("Pleasure", 1, WHITE)
	screen.blit(rend, (borders + 35 - 25, borders - pad_button_height - (borders - pad_button_height)/2 +10))
	pygame.draw.rect(screen, A_button_colour, A_button)
	rend = small_fontzy.render("Arousal", 1, WHITE)
	screen.blit(rend, (SCREEN_WIDTH/2 - pad_button_width/2 + 35 - 25, borders - pad_button_height - (borders - pad_button_height)/2 + 10))
	pygame.draw.rect(screen, D_button_colour, D_button)
	rend = small_fontzy.render("Dominance", 1, WHITE)
	screen.blit(rend, (SCREEN_WIDTH - borders - pad_button_width + 20 - 25, borders - pad_button_height - (borders - pad_button_height)/2 + 10))




	if P_on:
		pygame.draw.rect(screen, GREEN, P_on_off_button)
		rend = small_fontzy.render("On", 1, WHITE)
		screen.blit(rend, (P_on_off_button.x + 5, borders - pad_button_height - (borders - pad_button_height)/2 +10))
	else:
		pygame.draw.rect(screen, BLACK, P_on_off_button)
		rend = small_fontzy.render("Off", 1, WHITE)
		screen.blit(rend, (P_on_off_button.x + 5, borders - pad_button_height - (borders - pad_button_height)/2 +10))

	if A_on:
		pygame.draw.rect(screen, GREEN, A_on_off_button)
		rend = small_fontzy.render("On", 1, WHITE)
		screen.blit(rend, (A_on_off_button.x + 5, borders - pad_button_height - (borders - pad_button_height)/2 +10))
	else:
		pygame.draw.rect(screen, BLACK, A_on_off_button)
		rend = small_fontzy.render("Off", 1, WHITE)
		screen.blit(rend, (A_on_off_button.x + 5, borders - pad_button_height - (borders - pad_button_height)/2 +10))

	if D_on:
		pygame.draw.rect(screen, GREEN, D_on_off_button)
		rend = small_fontzy.render("On", 1, WHITE)
		screen.blit(rend, (D_on_off_button.x + 5, borders - pad_button_height - (borders - pad_button_height)/2 +10))
	else:
		pygame.draw.rect(screen, BLACK, D_on_off_button)
		rend = small_fontzy.render("Off", 1, WHITE)
		screen.blit(rend, (D_on_off_button.x + 5, borders - pad_button_height - (borders - pad_button_height)/2 +10))

	pygame.draw.rect(screen, BLACK, drag_bar_for_granularity)

	pygame.draw.rect(screen, BLACK, drag_bar_line)

	rend = small_fontzy.render("Save", 1, WHITE)

	screen.blit(rend, (SCREEN_WIDTH - borders - save_button_width + 20, SCREEN_HEIGHT - borders + (borders - save_button_height)/2 + 10))

	pygame.display.flip()

	# - constant game speed / FPS -

	clock.tick(FPS)

# - end -

pygame.quit()