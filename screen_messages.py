import pygame
import time

def hello_screen(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):



	screeno.fill((255,255,255))

	rend = big_fontzy.render("Flower Hunter", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Flower Hunter")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 100))



	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 450))



	image = pygame.image.load("Images/samurai2.png")

	x_size, y_size = image.get_rect().size

	screeno.blit(image, ((map_width-y_size)/2, 225))




	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == ord(' '):

					return


def consentimento(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):



	while True:


		screeno.fill((255,255,255))


		rend = big_fontzy.render("Consentimento", 1, (0,0,0))

		center_dist = int((map_width - big_fontzy.size("Consentimento")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 100))




		rend = small_fontzy.render("Leu com atenção as intruções na página anterior", 1, (0,0,0))


		screeno.blit(rend, (50, 250))

		rend = small_fontzy.render("e aceita fazer parte deste estudo?", 1, (0,0,0))

		screeno.blit(rend, (50, 300))

	


		posx, posy = pygame.mouse.get_pos()

		if (posy > 500) and (posy < 550):

			if (posx < 250) and (posx > 100):
				pygame.draw.rect(screeno, (255,0,0), pygame.Rect(100, 500, 150, 50))

			if (posx < 500) and (posx > 350):
				pygame.draw.rect(screeno, (0,255,0), pygame.Rect(350, 500, 150, 50))





		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(100, 500, 150, 50), 3)

		rend = small_fontzy.render("Não", 1, (0,0,0))
		screeno.blit(rend, (150, 510))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(350, 500, 150, 50), 3)

		rend = small_fontzy.render("Sim", 1, (0,0,0))
		screeno.blit(rend, (400, 510))




		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()

					if (posy > 500) and (posy < 550):

						if (posx < 250) and (posx > 100):
							exit()

						if (posx < 500) and (posx > 350):
							return


def recolha_dados(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):




	screeno.fill((255,255,255))

	rend = big_fontzy.render("Recolha de Dados", 1, (0,0,0))
	screeno.blit(rend, (50, 100))

	rend = small_fontzy.render("Obrigada por aceitar participar neste estudo.", 1, (0,0,0))
	screeno.blit(rend, (50, 250))

	rend = small_fontzy.render("Para efeitos de caracterização da amostra, pedimos", 1, (0,0,0))
	screeno.blit(rend, (50, 300))

	rend = small_fontzy.render("que responda de seguida a alguma questões.", 1, (0,0,0))
	screeno.blit(rend, (50, 325))


	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))


	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == ord(' '):

					return


def introducao_ao_tutorial(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):



	screeno.fill((255,255,255))

	rend = big_fontzy.render("Tutorial", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Tutorial")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 50))


	rend = small_fontzy.render("Irá agora jogar um tutorial do jogo.", 1, (0,0,0))


	screeno.blit(rend, (50, 200))


	rend = small_fontzy.render("Use as setas ou as teclas W A S e D para se mover.", 1, (0,0,0))

	screeno.blit(rend, (50, 225))


	rend = small_fontzy.render("Use a barra de espaços para atacar.", 1, (0,0,0))

	screeno.blit(rend, (50, 250))


	flower_image = pygame.image.load("Images/Flower.png")
	
	x_size, y_size = flower_image.get_rect().size
	screeno.blit(flower_image, pygame.Rect((450,305),(x_size, y_size)))

	rend = small_fontzy.render("O objetivo do jogo é encontrar uma flor     no mapa.", 1, (0,0,0))

	screeno.blit(rend, (50, 300))


	rend = small_fontzy.render("Ao tocar nessa flor, completou o nível.", 1, (0,0,0))

	screeno.blit(rend, (50, 325))

	rend = small_fontzy.render("Pelo caminho encontrará: fantasmas, que o atacam", 1, (0,0,0))

	screeno.blit(rend, (50, 350))

	rend = small_fontzy.render("se se aproximar demasiado e os quais pode matar", 1, (0,0,0))

	screeno.blit(rend, (50, 375))

	rend = small_fontzy.render("usando a sua espada (barra de espaços); moedas,", 1, (0,0,0))

	screeno.blit(rend, (50, 400))

	rend = small_fontzy.render("as quais pode colecionar; e bolinhos de arroz, que", 1, (0,0,0))

	screeno.blit(rend, (50, 425))

	rend = small_fontzy.render("o ajudam a recuperar vida.", 1, (0,0,0))

	screeno.blit(rend, (50, 450))




	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))






	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == ord(' '):

					return






def nivel_1(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):




	screeno.fill((255,255,255))

	rend = big_fontzy.render("Nível 1", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Nível 1")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 100))




	rend = small_fontzy.render("Prepare-se para jogar o primeiro nível", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Prepare-se para jogar o primeiro nível")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 300))


	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))



	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:

				if event.key == ord(' '):

					return


def nivel_2(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):



	screeno.fill((255,255,255))

	rend = big_fontzy.render("Nível 2", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Nível 2")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 100))




	rend = small_fontzy.render("Prepare-se para jogar o segundo nível", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Prepare-se para jogar o segundo nível")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 300))


	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))



	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:

				if event.key == ord(' '):

					return






def nivel_3(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):



	screeno.fill((255,255,255))

	rend = big_fontzy.render("Nível 3", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Nível 3")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 100))




	rend = small_fontzy.render("Prepare-se para jogar o terceiro e último nível", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Prepare-se para jogar o terceiro e último nível")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 300))


	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))



	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:

				if event.key == ord(' '):

					return






def questao_idade(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):


	clock = pygame.time.Clock()

	text_input_box = TextInputBox(100, 300, 400, small_fontzy)
	group = pygame.sprite.Group(text_input_box)

	run = True
	while run:


		clock.tick(60)
		event_list = pygame.event.get()
		for event in event_list:
			if event.type == pygame.QUIT:
				run = False 

			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()

					if (posy > 500) and (posy < 550):

						if (posx < 375) and (posx > 225):
							#save_number
							questions_file.write(str(text_input_box.text) + "\n")

							return


		group.update(event_list)

		screeno.fill((255,255,255))

		rend = big_fontzy.render("Idade", 1, (0,0,0))

		center_dist = int((map_width - big_fontzy.size("Idade")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 100))




		rend = small_fontzy.render("Qual é a sua idade?", 1, (0,0,0))

		center_dist = int((map_width - small_fontzy.size("Qual é a sua idade?")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 250))


		group.draw(screeno)




		posx, posy = pygame.mouse.get_pos()

		if (posy > 500) and (posy < 550):

			if (posx < 375) and (posx > 225):
				pygame.draw.rect(screeno, (0,255,255), pygame.Rect(225, 500, 150, 50))




		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(225, 500, 150, 50), 3)

		rend = small_fontzy.render("Submeter", 1, (0,0,0))
		screeno.blit(rend, (250, 510))




		pygame.display.flip()

		
		timerino = time.time()



		pygame.display.flip()







def inserir_numero_aluno(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):


	clock = pygame.time.Clock()

	text_input_box = TextInputBox(100, 300, 400, small_fontzy)
	group = pygame.sprite.Group(text_input_box)

	run = True
	while run:


		clock.tick(60)
		event_list = pygame.event.get()
		for event in event_list:
			if event.type == pygame.QUIT:
				run = False 

			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()

					if (posy > 500) and (posy < 550):

						if (posx < 375) and (posx > 225):
							#save_number
							questions_file = open("student_number.txt","a")
							questions_file.write(str(text_input_box.text) + "\n")
							questions_file.close()

							return


		group.update(event_list)

		screeno.fill((255,255,255))

		rend = big_fontzy.render("Número de Aluno", 1, (0,0,0))

		center_dist = int((map_width - big_fontzy.size("Número de Aluno")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 100))




		rend = small_fontzy.render("Por favor insira o seu número de aluno", 1, (0,0,0))

		center_dist = int((map_width - small_fontzy.size("Por favor insira o seu número de aluno")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 250))


		group.draw(screeno)




		posx, posy = pygame.mouse.get_pos()

		if (posy > 500) and (posy < 550):

			if (posx < 375) and (posx > 225):
				pygame.draw.rect(screeno, (0,255,255), pygame.Rect(225, 500, 150, 50))




		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(225, 500, 150, 50), 3)

		rend = small_fontzy.render("Submeter", 1, (0,0,0))
		screeno.blit(rend, (250, 510))




		pygame.display.flip()

		
		timerino = time.time()



		pygame.display.flip()






def obrigado(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):



	screeno.fill((255,255,255))

	rend = big_fontzy.render("Obrigado!", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Obrigado!")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 100))




	rend = small_fontzy.render("Muito obrigado por participar nesta experiência!", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Muito obrigado por participar nesta experiência!")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 250))


	rend = small_fontzy.render("A experiência terminou.", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("A experiência terminou.")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 350))


	rend = small_fontzy.render("Pode fechar este separador", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Pode fechar este separador")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 400))



	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:

				if event.key == ord(' '):

					return




def obrigado_tutorial(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, chosen_dimension):


	screeno.fill((255,255,255))

	rend = big_fontzy.render("Obrigado!", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Obrigado!")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 100))




	rend = small_fontzy.render("Completou agora o tutorial.", 1, (0,0,0))

	screeno.blit(rend, (50, 250))

	rend = small_fontzy.render("Irá de seguida jogar 3 níveis diferentes", 1, (0,0,0))

	screeno.blit(rend, (50, 275))

	rend = small_fontzy.render("do mesmo jogo e reportar o seu nível de " + chosen_dimension + ".", 1, (0,0,0))

	screeno.blit(rend, (50, 300))

	rend = small_fontzy.render("É muito importante para o nosso estudo que", 1, (0,0,0))

	screeno.blit(rend, (50, 350))

	rend = small_fontzy.render("seja o mais preciso que conseguir ao reportar", 1, (0,0,0))

	screeno.blit(rend, (50, 375))

	rend = small_fontzy.render("o seu nível de " + chosen_dimension + ".", 1, (0,0,0))

	screeno.blit(rend, (50, 400))





	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))





	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:

				if event.key == ord(' '):

					return


def scale_question_intro(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, chosen_dimension):


	screeno.fill((255,255,255))

	rend = big_fontzy.render("Obrigado!", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Obrigado!")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 100))




	rend = small_fontzy.render("Irá de seguida responder a 6 questões", 1, (0,0,0))

	screeno.blit(rend, (50, 250))

	rend = small_fontzy.render("relativas ao seu esforço ao jogar este nível.", 1, (0,0,0))

	screeno.blit(rend, (50, 275))

	rend = small_fontzy.render("Por favor responda às questões tendo em conta", 1, (0,0,0))

	screeno.blit(rend, (50, 325))

	rend = small_fontzy.render("o seu esforço ao jogar o nível em si", 1, (0,0,0))

	screeno.blit(rend, (50, 350))

	rend = small_fontzy.render("e não o esforço do processo de anotação.", 1, (0,0,0))

	screeno.blit(rend, (50, 375))




	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))





	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:

				if event.key == ord(' '):

					return





def scale_question_explanation(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, chosen_dimension):



	screeno.fill((255,255,255))

	rend = big_fontzy.render("Esforço Cognitivo", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Esforço Cognitivo")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 50))



	rend = small_fontzy.render("O esforço cognitivo é difícil de definir mas ", 1, (0,0,0))

	screeno.blit(rend, (50, 150))

	rend = small_fontzy.render("geralmente simples de compreender. Pode ser", 1, (0,0,0))

	screeno.blit(rend, (50, 175))

	rend = small_fontzy.render("influenciado pela tarefa, por sentimentos sobre ", 1, (0,0,0))

	screeno.blit(rend, (50, 200))

	rend = small_fontzy.render("a própria performance ou sentimentos de stress", 1, (0,0,0))

	screeno.blit(rend, (50, 225))

	rend = small_fontzy.render("e frustração. O esforço cognitivo pode ter origens", 1, (0,0,0))

	screeno.blit(rend, (50, 250))

	rend = small_fontzy.render("diversas, vamos pedir-lhe que avalie 6 factores", 1, (0,0,0))

	screeno.blit(rend, (50, 275))

	rend = small_fontzy.render("individualmente. Por favor leia atentamente as ", 1, (0,0,0))

	screeno.blit(rend, (50, 300))

	rend = small_fontzy.render("descrições de cada factor e em seguida indique", 1, (0,0,0))

	screeno.blit(rend, (50, 325))

	rend = small_fontzy.render("na escala de 0 a 10 qual o valor que melhor", 1, (0,0,0))

	screeno.blit(rend, (50, 350))

	rend = small_fontzy.render("corresponde ao esforço cognitivo sentido durante o", 1, (0,0,0))

	screeno.blit(rend, (50, 375))

	rend = small_fontzy.render("nível que acabou de jogar. O esforço cognitivo é uma", 1, (0,0,0))

	screeno.blit(rend, (50, 400))

	rend = small_fontzy.render("experiência individual, não há respostas certas ou", 1, (0,0,0))

	screeno.blit(rend, (50, 425))

	rend = small_fontzy.render("erradas. Note que nem todos os factores terão", 1, (0,0,0))

	screeno.blit(rend, (50, 450))

	rend = small_fontzy.render("a mesma importância.", 1, (0,0,0))

	screeno.blit(rend, (50, 475))




	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 525))





	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:

				if event.key == ord(' '):

					return





def introducao_as_anotacoes_pleasure(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):


	screeno.fill((255,255,255))

	rend = big_fontzy.render("Anotação: Prazer", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Anotação: Prazer")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 50))


	rend = small_fontzy.render("Leia atentamente a descrição que se segue:", 1, (0,0,0))

	screeno.blit(rend, (50, 200))



	rend = small_fontzy.render("O prazer está relacionado com afectos positivos", 1, (0,0,0))

	screeno.blit(rend, (50, 250))

	rend = small_fontzy.render("e negativos.", 1, (0,0,0))

	screeno.blit(rend, (50, 275))

	rend = small_fontzy.render("Por exemplo, elevado prazer envolve satisfação", 1, (0,0,0))

	screeno.blit(rend, (50, 325))

	rend = small_fontzy.render("e felicidade enquanto que baixo prazer envolve", 1, (0,0,0))

	screeno.blit(rend, (50, 350))

	rend = small_fontzy.render("sentimentos negativos e irritação.", 1, (0,0,0))

	screeno.blit(rend, (50, 375))

 

	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))



	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:

				if event.key == ord(' '):

					return


def introducao_as_anotacoes_arousal(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):



	screeno.fill((255,255,255))

	rend = big_fontzy.render("Anotação: Excitação", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Anotação: Excitação")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 50))


	rend = small_fontzy.render("Leia atentamente a descrição que se segue:", 1, (0,0,0))

	screeno.blit(rend, (50, 150))



	rend = small_fontzy.render("Excitação é um estado fisiológico e psicológico", 1, (0,0,0))

	screeno.blit(rend, (50, 200))

	rend = small_fontzy.render("de activação.", 1, (0,0,0))

	screeno.blit(rend, (50, 225))

	rend = small_fontzy.render("Está ligado à intensidade da reação e não", 1, (0,0,0))

	screeno.blit(rend, (50, 250))

	rend = small_fontzy.render("ao facto do estímulo ser bom ou mau.", 1, (0,0,0))

	screeno.blit(rend, (50, 275))

	rend = small_fontzy.render("Por exemplo, elevada excitação pode ser sentida", 1, (0,0,0))

	screeno.blit(rend, (50, 300))

	rend = small_fontzy.render("quando alguém que tem medo de um bicho, vê", 1, (0,0,0))

	screeno.blit(rend, (50, 325))

	rend = small_fontzy.render("esse bicho; ou quando alguém que adora", 1, (0,0,0))

	screeno.blit(rend, (50, 350))

	rend = small_fontzy.render("montanhas russas está prestes a andar numa.", 1, (0,0,0))

	screeno.blit(rend, (50, 375))


	rend = small_fontzy.render("Elevada excitação envolve sentimentos de prontidão,", 1, (0,0,0))

	screeno.blit(rend, (50, 400))

	rend = small_fontzy.render("tensão, entusiasmo ou euforia. Baixa excitação", 1, (0,0,0))

	screeno.blit(rend, (50, 425))

	rend = small_fontzy.render("envolve cansaço, estar aborrecido, calmo, ou relaxado.", 1, (0,0,0))

	screeno.blit(rend, (50, 450))


	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))



	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:

				if event.key == ord(' '):

					return



def introducao_as_anotacoes_dominance(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width):



	#blit relevant things
	# fontzy = pygame.font.SysFont('macondoswashcapsregularttf', 60)


	screeno.fill((255,255,255))

	rend = big_fontzy.render("Anotação: Dominância", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Anotação: Dominância")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 50))


	rend = small_fontzy.render("Leia atentamente a descrição que se segue:", 1, (0,0,0))

	screeno.blit(rend, (50, 200))



	rend = small_fontzy.render("A dominância está relacionada com o controlo", 1, (0,0,0))

	screeno.blit(rend, (50, 250))

	rend = small_fontzy.render("e influência.", 1, (0,0,0))

	screeno.blit(rend, (50, 275))

	rend = small_fontzy.render("Está relacionado com sentimentos de que as minhas", 1, (0,0,0))

	screeno.blit(rend, (50, 300))

	rend = small_fontzy.render("acções provocam a reacção desejada no mundo.", 1, (0,0,0))

	screeno.blit(rend, (50, 325))

	rend = small_fontzy.render("Elevada dominância pode ser por exemplo sentir que", 1, (0,0,0))

	screeno.blit(rend, (50, 350))

	rend = small_fontzy.render("controla o jogo e consegue fazer aquilo que quer.", 1, (0,0,0))

	screeno.blit(rend, (50, 375))

	rend = small_fontzy.render("Baixa dominância pode ser a sensação de que faça", 1, (0,0,0))

	screeno.blit(rend, (50, 400))

	rend = small_fontzy.render("o que fizer as coisas não correm como quer. ", 1, (0,0,0))

	screeno.blit(rend, (50, 425))

 

	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))



	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:

				if event.key == ord(' '):

					return


def introducao_as_anotacoes_geral(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, chosen_dimension):



	#blit relevant things
	# fontzy = pygame.font.SysFont('macondoswashcapsregularttf', 60)


	screeno.fill((255,255,255))

	rend = big_fontzy.render("Anotação: Instruções", 1, (0,0,0))

	center_dist = int((map_width - big_fontzy.size("Anotação: Instruções")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 75))





	rend = small_fontzy.render("De seguida vai ver um vídeo do jogo que acabou", 1, (0,0,0))

	screeno.blit(rend, (50, 200))

	rend = small_fontzy.render("de realizar. A meio do ecrã verá uma linha", 1, (0,0,0))

	screeno.blit(rend, (50, 225))

	rend = small_fontzy.render("a aparecer do lado direito.", 1, (0,0,0))

	screeno.blit(rend, (50, 250))

	rend = small_fontzy.render(("Essa linha representa o seu nível de " + chosen_dimension), 1, (0,0,0))

	screeno.blit(rend, (50, 275))

	rend = small_fontzy.render("durante a sua travessia do jogo.", 1, (0,0,0))

	screeno.blit(rend, (50, 300))

	rend = small_fontzy.render("Utilize as setas 'cima' e 'baixo' para indicar", 1, (0,0,0))

	screeno.blit(rend, (50, 325))

	rend = small_fontzy.render("como variou o seu nível de " + chosen_dimension, 1, (0,0,0))

	screeno.blit(rend, (50, 350))

	rend = small_fontzy.render("ao longo do jogo.", 1, (0,0,0))

	screeno.blit(rend, (50, 375))

	rend = small_fontzy.render("Esta anotação é para treino e não será gravada.", 1, (0,0,0))

	screeno.blit(rend, (50, 425))

	rend = small_fontzy.render("Experimente à vontade controlar a linha.", 1, (0,0,0))

	screeno.blit(rend, (50, 450))

 

	rend = small_fontzy.render("Carregue na barra de espaços para continuar", 1, (0,0,0))

	center_dist = int((map_width - small_fontzy.size("Carregue na barra de espaços para continuar")[0])/2)


	if center_dist < 0:
		print("Text Outside Screen")
		exit()

	screeno.blit(rend, (center_dist, 500))



	pygame.display.flip()

	
	timerino = time.time()

	while (time.time() - timerino) < 1.5:


		for event in pygame.event.get():
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				exit()

	while True:

		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == ord(' '):

					return


def questao_sexo(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):



	#blit relevant things
	# fontzy = pygame.font.SysFont('macondoswashcapsregularttf', 60)

	while True:

		screeno.fill((255,255,255))

		rend = big_fontzy.render("Género", 1, (0,0,0))

		center_dist = int((map_width - big_fontzy.size("Género")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 100))



		rend = medium_fontzy.render("Com que género se identifica?", 1, (0,0,0))


		screeno.blit(rend, (50, 250))


		
		posx, posy = pygame.mouse.get_pos()

		if (posx > 70) and (posx < 520):

			if (posy < 350) and (posy > 295):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 295, 510, 45))

			if (posy < 390) and (posy > 345):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 345, 510, 45))

			if (posy < 440) and (posy > 395):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 395, 510, 45))

			if (posy < 490) and (posy > 445):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 445, 510, 45))



		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 295, 510, 45), 3)

		rend = small_fontzy.render("Feminino", 1, (0,0,0))
		screeno.blit(rend, (45, 300))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 345, 510, 45), 3)

		rend = small_fontzy.render("Masculino", 1, (0,0,0))
		screeno.blit(rend, (45, 350))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 395, 510, 45), 3)

		rend = small_fontzy.render("Outro", 1, (0,0,0))
		screeno.blit(rend, (45, 400))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 445, 510, 45), 3)

		rend = small_fontzy.render("Prefiro não responder", 1, (0,0,0))
		screeno.blit(rend, (45, 450))



		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()

					if (posx > 70) and (posx < 520):


						if (posy < 340) and (posy > 295):
							questions_file.write("Feminino\n")
							return

						if (posy < 390) and (posy > 345):
							questions_file.write("Masculino\n")
							return

						if (posy < 440) and (posy > 395):
							questions_file.write("Outro\n")
							return

						if (posy < 490) and (posy > 445):
							questions_file.write("Prefiro não responder\n")
							return




def questao_1(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):



	#blit relevant things
	# fontzy = pygame.font.SysFont('macondoswashcapsregularttf', 60)

	while True:

		screeno.fill((255,255,255))

		# rend = big_fontzy.render("Questão 1", 1, (0,0,0))

		# center_dist = int((map_width - big_fontzy.size("Questão 1")[0])/2)


		# if center_dist < 0:
		# 	print("Text Outside Screen")
		# 	exit()

		# screeno.blit(rend, (center_dist, 100))



		rend = medium_fontzy.render("Com que frequência joga videojogos?", 1, (0,0,0))


		screeno.blit(rend, (50, 250))


		
		posx, posy = pygame.mouse.get_pos()

		if (posx > 70) and (posx < 520):

			if (posy < 390) and (posy > 345):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(70, 345, 450, 45))

			if (posy < 440) and (posy > 395):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(70, 395, 450, 45))

			if (posy < 490) and (posy > 445):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(70, 445, 450, 45))




		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(70, 345, 450, 45), 3)

		rend = small_fontzy.render("Guardo tempo no meu horário para jogar", 1, (0,0,0))
		screeno.blit(rend, (75, 350))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(70, 395, 450, 45), 3)

		rend = small_fontzy.render("Jogo ocasionalmente ", 1, (0,0,0))
		screeno.blit(rend, (75, 400))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(70, 445, 450, 45), 3)

		rend = small_fontzy.render("Raramente jogo", 1, (0,0,0))
		screeno.blit(rend, (75, 450))



		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()

					if (posx > 70) and (posx < 520):

						if (posy < 390) and (posy > 345):
							questions_file.write("1\n")
							return

						if (posy < 440) and (posy > 395):
							questions_file.write("2\n")
							return

						if (posy < 490) and (posy > 445):
							questions_file.write("3\n")
							return

					

def questao_2(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):



	#blit relevant things
	# fontzy = pygame.font.SysFont('macondoswashcapsregularttf', 60)

	while True:

		screeno.fill((255,255,255))

		# rend = big_fontzy.render("Questão 2", 1, (0,0,0))

		# center_dist = int((map_width - big_fontzy.size("Questão 2")[0])/2)


		# if center_dist < 0:
		# 	print("Text Outside Screen")
		# 	exit()

		# screeno.blit(rend, (center_dist, 50))



		rend = medium_fontzy.render("Quão familiarizado está com jogos", 1, (0,0,0))

		screeno.blit(rend, (50, 150))

		rend = medium_fontzy.render("do tipo aventura 2D, como por exemplo", 1, (0,0,0))

		screeno.blit(rend, (50, 200))

		rend = medium_fontzy.render("os antigos jogos Zelda ou Pokemon?", 1, (0,0,0))

		screeno.blit(rend, (50, 250))



		
		posx, posy = pygame.mouse.get_pos()

		if (posx > 70) and (posx < 520):

			if (posy < 390) and (posy > 345):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 345, 510, 45))

			if (posy < 440) and (posy > 395):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 395, 510, 45))

			if (posy < 490) and (posy > 445):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 445, 510, 45))




		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 345, 510, 45), 3)

		rend = small_fontzy.render("Gosto e já joguei / vi outros jogarem muitas vezes", 1, (0,0,0))
		screeno.blit(rend, (45, 350))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 395, 510, 45), 3)

		rend = small_fontzy.render("Não me é familiar ou não tenho opinião formada", 1, (0,0,0))
		screeno.blit(rend, (45, 400))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 445, 510, 45), 3)

		rend = small_fontzy.render("Não gosto desse tipo de jogo", 1, (0,0,0))
		screeno.blit(rend, (45, 450))



		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()

					if (posx > 70) and (posx < 520):

						if (posy < 390) and (posy > 345):
							questions_file.write("1\n")
							return

						if (posy < 440) and (posy > 395):
							questions_file.write("2\n")
							return

						if (posy < 490) and (posy > 445):
							questions_file.write("3\n")
							return

					
def questao_3(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):



# Ao jogar um jogo de aventura, o que é mais importante para si?

# Chegar ao objectivo final o mais rápido possível
# Explorar novos locais
# Coletar itens e dinheiro de modo a melhorar a minha personagem
# Derrotar todos os inimigos que encontro




	#blit relevant things
	# fontzy = pygame.font.SysFont('macondoswashcapsregularttf', 60)

	while True:

		screeno.fill((255,255,255))

		# rend = big_fontzy.render("Questão 3", 1, (0,0,0))

		# center_dist = int((map_width - big_fontzy.size("Questão 3")[0])/2)


		# if center_dist < 0:
		# 	print("Text Outside Screen")
		# 	exit()

		# screeno.blit(rend, (center_dist, 50))



		rend = medium_fontzy.render("Ao jogar um jogo de aventura,", 1, (0,0,0))

		screeno.blit(rend, (50, 150))

		rend = medium_fontzy.render("o que é mais importante para si?", 1, (0,0,0))

		screeno.blit(rend, (50, 200))



		
		posx, posy = pygame.mouse.get_pos()

		if (posx > 70) and (posx < 520):

			if (posy < 350) and (posy > 295):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 295, 510, 45))

			if (posy < 390) and (posy > 345):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 345, 510, 45))

			if (posy < 440) and (posy > 395):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 395, 510, 45))

			if (posy < 490) and (posy > 445):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(40, 445, 510, 45))



		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 295, 510, 45), 3)

		rend = small_fontzy.render("Derrotar todos os inimigos que encontro", 1, (0,0,0))
		screeno.blit(rend, (45, 300))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 345, 510, 45), 3)

		rend = small_fontzy.render("Chegar ao objectivo final o mais rápido possível", 1, (0,0,0))
		screeno.blit(rend, (45, 350))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 395, 510, 45), 3)

		rend = small_fontzy.render("Explorar novos locais", 1, (0,0,0))
		screeno.blit(rend, (45, 400))

		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(40, 445, 510, 45), 3)

		rend = small_fontzy.render("Melhorar o equipamento da minha personagem", 1, (0,0,0))
		screeno.blit(rend, (45, 450))



		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()

					if (posx > 70) and (posx < 520):


						if (posy < 340) and (posy > 295):
							questions_file.write("1\n")
							return

						if (posy < 390) and (posy > 345):
							questions_file.write("2\n")
							return

						if (posy < 440) and (posy > 395):
							questions_file.write("3\n")
							return

						if (posy < 490) and (posy > 445):
							questions_file.write("4\n")
							return



def scale_question_1(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):



	while True:

		screeno.fill((255,255,255))

		rend = big_fontzy.render("Esforço mental", 1, (0,0,0))

		center_dist = int((map_width - big_fontzy.size("Esforço mental")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 50))




		posx, posy = pygame.mouse.get_pos()

		if (posy > 450) and (posy < 500):

			if (posx < 75) and (posx > 25):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(25, 450, 50, 50))
			if (posx < 125) and (posx > 75):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(75, 450, 50, 50))
			if (posx < 175) and (posx > 125):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(125, 450, 50, 50))
			if (posx < 225) and (posx > 175):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(175, 450, 50, 50))
			if (posx < 275) and (posx > 225):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(225, 450, 50, 50))
			if (posx < 325) and (posx > 275):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(275, 450, 50, 50))
			if (posx < 375) and (posx > 325):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(325, 450, 50, 50))
			if (posx < 425) and (posx > 375):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(375, 450, 50, 50))
			if (posx < 475) and (posx > 425):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(425, 450, 50, 50))
			if (posx < 525) and (posx > 475):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(475, 450, 50, 50))
			if (posx < 575) and (posx > 525):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(525, 450, 50, 50))



		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(25, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(75, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(125, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(175, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(225, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(275, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(325, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(375, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(425, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(475, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(525, 450, 50, 50), 3)



		rend = small_fontzy.render("0", 1, (0,0,0))
		screeno.blit(rend, (42, 460))

		rend = small_fontzy.render("1", 1, (0,0,0))
		screeno.blit(rend, (92, 460))

		rend = small_fontzy.render("2", 1, (0,0,0))
		screeno.blit(rend, (142, 460))

		rend = small_fontzy.render("3", 1, (0,0,0))
		screeno.blit(rend, (192, 460))

		rend = small_fontzy.render("4", 1, (0,0,0))
		screeno.blit(rend, (242, 460))

		rend = small_fontzy.render("5", 1, (0,0,0))
		screeno.blit(rend, (292, 460))

		rend = small_fontzy.render("6", 1, (0,0,0))
		screeno.blit(rend, (342, 460))

		rend = small_fontzy.render("7", 1, (0,0,0))
		screeno.blit(rend, (392, 460))

		rend = small_fontzy.render("8", 1, (0,0,0))
		screeno.blit(rend, (442, 460))

		rend = small_fontzy.render("9", 1, (0,0,0))
		screeno.blit(rend, (492, 460))

		rend = small_fontzy.render("10", 1, (0,0,0))
		screeno.blit(rend, (538, 460))




		rend = medium_fontzy.render("Baixo", 1, (0,0,0))

		screeno.blit(rend, (25, 510))

		rend = medium_fontzy.render("Alto", 1, (0,0,0))

		screeno.blit(rend, (515, 510))








		rend = medium_fontzy.render("Definição:", 1, (0,0,0))

		screeno.blit(rend, (25, 150))


		rend = small_fontzy.render("Quanta actividade mental e perceptual foi necessária?", 1, (0,0,0))

		screeno.blit(rend, (25, 200))

		rend = small_fontzy.render("(e.g., pensar, decidir, calcular, lembrar procurar, etc.)", 1, (0,0,0))

		screeno.blit(rend, (25, 250))

		rend = small_fontzy.render("A tarefa foi fácil ou exigente?", 1, (0,0,0))

		screeno.blit(rend, (25, 300))

		rend = small_fontzy.render("Simples ou complexa?", 1, (0,0,0))

		screeno.blit(rend, (25, 350))


		rend = medium_fontzy.render("Nível de esforço mental:", 1, (0,0,0))

		screeno.blit(rend, (25, 400))



		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()


					if (posy > 450) and (posy < 500):

						if (posx < 75) and (posx > 25):
							questions_file.write("0\n")
							return
						if (posx < 125) and (posx > 75):
							questions_file.write("1\n")
							return
						if (posx < 175) and (posx > 125):
							questions_file.write("2\n")
							return
						if (posx < 225) and (posx > 175):
							questions_file.write("3\n")
							return
						if (posx < 275) and (posx > 225):
							questions_file.write("4\n")
							return
						if (posx < 325) and (posx > 275):
							questions_file.write("5\n")
							return
						if (posx < 375) and (posx > 325):
							questions_file.write("6\n")
							return
						if (posx < 425) and (posx > 375):
							questions_file.write("7\n")
							return
						if (posx < 475) and (posx > 425):
							questions_file.write("8\n")
							return
						if (posx < 525) and (posx > 475):
							questions_file.write("9\n")
							return
						if (posx < 575) and (posx > 525):
							questions_file.write("10\n")
							return





def scale_question_2(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):



	while True:

		screeno.fill((255,255,255))

		rend = big_fontzy.render("Esforço físico", 1, (0,0,0))

		center_dist = int((map_width - big_fontzy.size("Esforço físico")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 50))




		posx, posy = pygame.mouse.get_pos()

		if (posy > 450) and (posy < 500):

			if (posx < 75) and (posx > 25):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(25, 450, 50, 50))
			if (posx < 125) and (posx > 75):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(75, 450, 50, 50))
			if (posx < 175) and (posx > 125):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(125, 450, 50, 50))
			if (posx < 225) and (posx > 175):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(175, 450, 50, 50))
			if (posx < 275) and (posx > 225):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(225, 450, 50, 50))
			if (posx < 325) and (posx > 275):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(275, 450, 50, 50))
			if (posx < 375) and (posx > 325):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(325, 450, 50, 50))
			if (posx < 425) and (posx > 375):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(375, 450, 50, 50))
			if (posx < 475) and (posx > 425):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(425, 450, 50, 50))
			if (posx < 525) and (posx > 475):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(475, 450, 50, 50))
			if (posx < 575) and (posx > 525):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(525, 450, 50, 50))



		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(25, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(75, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(125, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(175, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(225, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(275, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(325, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(375, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(425, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(475, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(525, 450, 50, 50), 3)



		rend = small_fontzy.render("0", 1, (0,0,0))
		screeno.blit(rend, (42, 460))

		rend = small_fontzy.render("1", 1, (0,0,0))
		screeno.blit(rend, (92, 460))

		rend = small_fontzy.render("2", 1, (0,0,0))
		screeno.blit(rend, (142, 460))

		rend = small_fontzy.render("3", 1, (0,0,0))
		screeno.blit(rend, (192, 460))

		rend = small_fontzy.render("4", 1, (0,0,0))
		screeno.blit(rend, (242, 460))

		rend = small_fontzy.render("5", 1, (0,0,0))
		screeno.blit(rend, (292, 460))

		rend = small_fontzy.render("6", 1, (0,0,0))
		screeno.blit(rend, (342, 460))

		rend = small_fontzy.render("7", 1, (0,0,0))
		screeno.blit(rend, (392, 460))

		rend = small_fontzy.render("8", 1, (0,0,0))
		screeno.blit(rend, (442, 460))

		rend = small_fontzy.render("9", 1, (0,0,0))
		screeno.blit(rend, (492, 460))

		rend = small_fontzy.render("10", 1, (0,0,0))
		screeno.blit(rend, (538, 460))




		rend = medium_fontzy.render("Baixo", 1, (0,0,0))

		screeno.blit(rend, (25, 510))

		rend = medium_fontzy.render("Alto", 1, (0,0,0))

		screeno.blit(rend, (515, 510))








		rend = medium_fontzy.render("Definição:", 1, (0,0,0))

		screeno.blit(rend, (25, 150))


		rend = small_fontzy.render("Quanta actividade física foi necessária?", 1, (0,0,0))

		screeno.blit(rend, (25, 200))

		rend = small_fontzy.render("(eg., puxar, pular, virar, controlar, activar)", 1, (0,0,0))

		screeno.blit(rend, (25, 250))

		rend = small_fontzy.render("A tarefa foi fácil ou exigente? Foi lenta ou animada?", 1, (0,0,0))

		screeno.blit(rend, (25, 300))

		rend = small_fontzy.render("Folgada ou extenuante? Relaxante ou trabalhosa?", 1, (0,0,0))

		screeno.blit(rend, (25, 350))

		rend = medium_fontzy.render("Nível de esforço físico:", 1, (0,0,0))

		screeno.blit(rend, (25, 400))




		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()


					if (posy > 450) and (posy < 500):

						if (posx < 75) and (posx > 25):
							questions_file.write("0\n")
							return
						if (posx < 125) and (posx > 75):
							questions_file.write("1\n")
							return
						if (posx < 175) and (posx > 125):
							questions_file.write("2\n")
							return
						if (posx < 225) and (posx > 175):
							questions_file.write("3\n")
							return
						if (posx < 275) and (posx > 225):
							questions_file.write("4\n")
							return
						if (posx < 325) and (posx > 275):
							questions_file.write("5\n")
							return
						if (posx < 375) and (posx > 325):
							questions_file.write("6\n")
							return
						if (posx < 425) and (posx > 375):
							questions_file.write("7\n")
							return
						if (posx < 475) and (posx > 425):
							questions_file.write("8\n")
							return
						if (posx < 525) and (posx > 475):
							questions_file.write("9\n")
							return
						if (posx < 575) and (posx > 525):
							questions_file.write("10\n")
							return






def scale_question_3(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):



	while True:

		screeno.fill((255,255,255))

		rend = big_fontzy.render("Esforço temporal", 1, (0,0,0))

		center_dist = int((map_width - big_fontzy.size("Esforço temporal")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 50))




		posx, posy = pygame.mouse.get_pos()

		if (posy > 450) and (posy < 500):

			if (posx < 75) and (posx > 25):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(25, 450, 50, 50))
			if (posx < 125) and (posx > 75):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(75, 450, 50, 50))
			if (posx < 175) and (posx > 125):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(125, 450, 50, 50))
			if (posx < 225) and (posx > 175):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(175, 450, 50, 50))
			if (posx < 275) and (posx > 225):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(225, 450, 50, 50))
			if (posx < 325) and (posx > 275):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(275, 450, 50, 50))
			if (posx < 375) and (posx > 325):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(325, 450, 50, 50))
			if (posx < 425) and (posx > 375):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(375, 450, 50, 50))
			if (posx < 475) and (posx > 425):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(425, 450, 50, 50))
			if (posx < 525) and (posx > 475):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(475, 450, 50, 50))
			if (posx < 575) and (posx > 525):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(525, 450, 50, 50))



		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(25, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(75, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(125, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(175, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(225, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(275, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(325, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(375, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(425, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(475, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(525, 450, 50, 50), 3)



		rend = small_fontzy.render("0", 1, (0,0,0))
		screeno.blit(rend, (42, 460))

		rend = small_fontzy.render("1", 1, (0,0,0))
		screeno.blit(rend, (92, 460))

		rend = small_fontzy.render("2", 1, (0,0,0))
		screeno.blit(rend, (142, 460))

		rend = small_fontzy.render("3", 1, (0,0,0))
		screeno.blit(rend, (192, 460))

		rend = small_fontzy.render("4", 1, (0,0,0))
		screeno.blit(rend, (242, 460))

		rend = small_fontzy.render("5", 1, (0,0,0))
		screeno.blit(rend, (292, 460))

		rend = small_fontzy.render("6", 1, (0,0,0))
		screeno.blit(rend, (342, 460))

		rend = small_fontzy.render("7", 1, (0,0,0))
		screeno.blit(rend, (392, 460))

		rend = small_fontzy.render("8", 1, (0,0,0))
		screeno.blit(rend, (442, 460))

		rend = small_fontzy.render("9", 1, (0,0,0))
		screeno.blit(rend, (492, 460))

		rend = small_fontzy.render("10", 1, (0,0,0))
		screeno.blit(rend, (538, 460))




		rend = medium_fontzy.render("Baixo", 1, (0,0,0))

		screeno.blit(rend, (25, 510))

		rend = medium_fontzy.render("Alto", 1, (0,0,0))

		screeno.blit(rend, (515, 510))








		rend = medium_fontzy.render("Definição:", 1, (0,0,0))

		screeno.blit(rend, (25, 150))


		rend = small_fontzy.render("Sentiu pressão temporal devido ao ritmo da", 1, (0,0,0))

		screeno.blit(rend, (25, 200))

		rend = small_fontzy.render("tarefa ou dos elementos da tarefa?", 1, (0,0,0))

		screeno.blit(rend, (25, 250))

		rend = small_fontzy.render("O ritmo era lento e vagaroso ou rápido e frenético?", 1, (0,0,0))

		screeno.blit(rend, (25, 300))

		rend = small_fontzy.render("", 1, (0,0,0))

		screeno.blit(rend, (25, 350))

		rend = medium_fontzy.render("Nível de esforço temporal:", 1, (0,0,0))

		screeno.blit(rend, (25, 400))



		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()


					if (posy > 450) and (posy < 500):

						if (posx < 75) and (posx > 25):
							questions_file.write("0\n")
							return
						if (posx < 125) and (posx > 75):
							questions_file.write("1\n")
							return
						if (posx < 175) and (posx > 125):
							questions_file.write("2\n")
							return
						if (posx < 225) and (posx > 175):
							questions_file.write("3\n")
							return
						if (posx < 275) and (posx > 225):
							questions_file.write("4\n")
							return
						if (posx < 325) and (posx > 275):
							questions_file.write("5\n")
							return
						if (posx < 375) and (posx > 325):
							questions_file.write("6\n")
							return
						if (posx < 425) and (posx > 375):
							questions_file.write("7\n")
							return
						if (posx < 475) and (posx > 425):
							questions_file.write("8\n")
							return
						if (posx < 525) and (posx > 475):
							questions_file.write("9\n")
							return
						if (posx < 575) and (posx > 525):
							questions_file.write("10\n")
							return





def scale_question_4(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):



	while True:

		screeno.fill((255,255,255))

		rend = big_fontzy.render("Performance", 1, (0,0,0))

		center_dist = int((map_width - big_fontzy.size("Performance")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 50))




		posx, posy = pygame.mouse.get_pos()

		if (posy > 450) and (posy < 500):

			if (posx < 75) and (posx > 25):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(25, 450, 50, 50))
			if (posx < 125) and (posx > 75):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(75, 450, 50, 50))
			if (posx < 175) and (posx > 125):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(125, 450, 50, 50))
			if (posx < 225) and (posx > 175):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(175, 450, 50, 50))
			if (posx < 275) and (posx > 225):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(225, 450, 50, 50))
			if (posx < 325) and (posx > 275):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(275, 450, 50, 50))
			if (posx < 375) and (posx > 325):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(325, 450, 50, 50))
			if (posx < 425) and (posx > 375):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(375, 450, 50, 50))
			if (posx < 475) and (posx > 425):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(425, 450, 50, 50))
			if (posx < 525) and (posx > 475):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(475, 450, 50, 50))
			if (posx < 575) and (posx > 525):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(525, 450, 50, 50))



		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(25, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(75, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(125, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(175, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(225, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(275, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(325, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(375, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(425, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(475, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(525, 450, 50, 50), 3)



		rend = small_fontzy.render("0", 1, (0,0,0))
		screeno.blit(rend, (42, 460))

		rend = small_fontzy.render("1", 1, (0,0,0))
		screeno.blit(rend, (92, 460))

		rend = small_fontzy.render("2", 1, (0,0,0))
		screeno.blit(rend, (142, 460))

		rend = small_fontzy.render("3", 1, (0,0,0))
		screeno.blit(rend, (192, 460))

		rend = small_fontzy.render("4", 1, (0,0,0))
		screeno.blit(rend, (242, 460))

		rend = small_fontzy.render("5", 1, (0,0,0))
		screeno.blit(rend, (292, 460))

		rend = small_fontzy.render("6", 1, (0,0,0))
		screeno.blit(rend, (342, 460))

		rend = small_fontzy.render("7", 1, (0,0,0))
		screeno.blit(rend, (392, 460))

		rend = small_fontzy.render("8", 1, (0,0,0))
		screeno.blit(rend, (442, 460))

		rend = small_fontzy.render("9", 1, (0,0,0))
		screeno.blit(rend, (492, 460))

		rend = small_fontzy.render("10", 1, (0,0,0))
		screeno.blit(rend, (538, 460))




		rend = medium_fontzy.render("Baixo", 1, (0,0,0))

		screeno.blit(rend, (25, 510))

		rend = medium_fontzy.render("Alto", 1, (0,0,0))

		screeno.blit(rend, (515, 510))









		rend = medium_fontzy.render("Definição:", 1, (0,0,0))

		screeno.blit(rend, (25, 150))

		rend = small_fontzy.render("Quão bem sucedido pensa ter sido no alcance dos", 1, (0,0,0))

		screeno.blit(rend, (25, 200))

		rend = small_fontzy.render("objectivos da tarefa?", 1, (0,0,0))

		screeno.blit(rend, (25, 250))

		rend = small_fontzy.render("O quão satisfeito está com a sua prestação e", 1, (0,0,0))

		screeno.blit(rend, (25, 300))

		rend = small_fontzy.render("capacidade de atingir os objectivos?", 1, (0,0,0))

		screeno.blit(rend, (25, 350))


		rend = medium_fontzy.render("Nível de performance:", 1, (0,0,0))

		screeno.blit(rend, (25, 400))


		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()


					if (posy > 450) and (posy < 500):

						if (posx < 75) and (posx > 25):
							questions_file.write("0\n")
							return
						if (posx < 125) and (posx > 75):
							questions_file.write("1\n")
							return
						if (posx < 175) and (posx > 125):
							questions_file.write("2\n")
							return
						if (posx < 225) and (posx > 175):
							questions_file.write("3\n")
							return
						if (posx < 275) and (posx > 225):
							questions_file.write("4\n")
							return
						if (posx < 325) and (posx > 275):
							questions_file.write("5\n")
							return
						if (posx < 375) and (posx > 325):
							questions_file.write("6\n")
							return
						if (posx < 425) and (posx > 375):
							questions_file.write("7\n")
							return
						if (posx < 475) and (posx > 425):
							questions_file.write("8\n")
							return
						if (posx < 525) and (posx > 475):
							questions_file.write("9\n")
							return
						if (posx < 575) and (posx > 525):
							questions_file.write("10\n")
							return




def scale_question_5(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):



	while True:

		screeno.fill((255,255,255))

		rend = big_fontzy.render("Esforço", 1, (0,0,0))

		center_dist = int((map_width - big_fontzy.size("Esforço")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 50))




		posx, posy = pygame.mouse.get_pos()

		if (posy > 450) and (posy < 500):

			if (posx < 75) and (posx > 25):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(25, 450, 50, 50))
			if (posx < 125) and (posx > 75):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(75, 450, 50, 50))
			if (posx < 175) and (posx > 125):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(125, 450, 50, 50))
			if (posx < 225) and (posx > 175):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(175, 450, 50, 50))
			if (posx < 275) and (posx > 225):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(225, 450, 50, 50))
			if (posx < 325) and (posx > 275):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(275, 450, 50, 50))
			if (posx < 375) and (posx > 325):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(325, 450, 50, 50))
			if (posx < 425) and (posx > 375):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(375, 450, 50, 50))
			if (posx < 475) and (posx > 425):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(425, 450, 50, 50))
			if (posx < 525) and (posx > 475):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(475, 450, 50, 50))
			if (posx < 575) and (posx > 525):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(525, 450, 50, 50))



		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(25, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(75, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(125, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(175, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(225, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(275, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(325, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(375, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(425, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(475, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(525, 450, 50, 50), 3)



		rend = small_fontzy.render("0", 1, (0,0,0))
		screeno.blit(rend, (42, 460))

		rend = small_fontzy.render("1", 1, (0,0,0))
		screeno.blit(rend, (92, 460))

		rend = small_fontzy.render("2", 1, (0,0,0))
		screeno.blit(rend, (142, 460))

		rend = small_fontzy.render("3", 1, (0,0,0))
		screeno.blit(rend, (192, 460))

		rend = small_fontzy.render("4", 1, (0,0,0))
		screeno.blit(rend, (242, 460))

		rend = small_fontzy.render("5", 1, (0,0,0))
		screeno.blit(rend, (292, 460))

		rend = small_fontzy.render("6", 1, (0,0,0))
		screeno.blit(rend, (342, 460))

		rend = small_fontzy.render("7", 1, (0,0,0))
		screeno.blit(rend, (392, 460))

		rend = small_fontzy.render("8", 1, (0,0,0))
		screeno.blit(rend, (442, 460))

		rend = small_fontzy.render("9", 1, (0,0,0))
		screeno.blit(rend, (492, 460))

		rend = small_fontzy.render("10", 1, (0,0,0))
		screeno.blit(rend, (538, 460))




		rend = medium_fontzy.render("Baixo", 1, (0,0,0))

		screeno.blit(rend, (25, 510))

		rend = medium_fontzy.render("Alto", 1, (0,0,0))

		screeno.blit(rend, (515, 510))







		rend = medium_fontzy.render("Definição:", 1, (0,0,0))

		screeno.blit(rend, (25, 150))



		rend = small_fontzy.render("Quanto teve que trabalhar (mental e fisicamente)", 1, (0,0,0))

		screeno.blit(rend, (25, 200))

		rend = small_fontzy.render("para conseguir o seu nível de prestação?", 1, (0,0,0))

		screeno.blit(rend, (25, 250))

		rend = small_fontzy.render("", 1, (0,0,0))

		screeno.blit(rend, (25, 300))

		rend = small_fontzy.render("", 1, (0,0,0))

		screeno.blit(rend, (25, 350))

		rend = medium_fontzy.render("Nível de esforço:", 1, (0,0,0))

		screeno.blit(rend, (25, 400))



		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()


					if (posy > 450) and (posy < 500):

						if (posx < 75) and (posx > 25):
							questions_file.write("0\n")
							return
						if (posx < 125) and (posx > 75):
							questions_file.write("1\n")
							return
						if (posx < 175) and (posx > 125):
							questions_file.write("2\n")
							return
						if (posx < 225) and (posx > 175):
							questions_file.write("3\n")
							return
						if (posx < 275) and (posx > 225):
							questions_file.write("4\n")
							return
						if (posx < 325) and (posx > 275):
							questions_file.write("5\n")
							return
						if (posx < 375) and (posx > 325):
							questions_file.write("6\n")
							return
						if (posx < 425) and (posx > 375):
							questions_file.write("7\n")
							return
						if (posx < 475) and (posx > 425):
							questions_file.write("8\n")
							return
						if (posx < 525) and (posx > 475):
							questions_file.write("9\n")
							return
						if (posx < 575) and (posx > 525):
							questions_file.write("10\n")
							return




def scale_question_6(small_fontzy, medium_fontzy, big_fontzy, screeno, map_height, map_width, questions_file):



	while True:

		screeno.fill((255,255,255))

		rend = big_fontzy.render("Frustração", 1, (0,0,0))

		center_dist = int((map_width - big_fontzy.size("Frustração")[0])/2)


		if center_dist < 0:
			print("Text Outside Screen")
			exit()

		screeno.blit(rend, (center_dist, 50))




		posx, posy = pygame.mouse.get_pos()

		if (posy > 450) and (posy < 500):

			if (posx < 75) and (posx > 25):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(25, 450, 50, 50))
			if (posx < 125) and (posx > 75):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(75, 450, 50, 50))
			if (posx < 175) and (posx > 125):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(125, 450, 50, 50))
			if (posx < 225) and (posx > 175):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(175, 450, 50, 50))
			if (posx < 275) and (posx > 225):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(225, 450, 50, 50))
			if (posx < 325) and (posx > 275):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(275, 450, 50, 50))
			if (posx < 375) and (posx > 325):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(325, 450, 50, 50))
			if (posx < 425) and (posx > 375):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(375, 450, 50, 50))
			if (posx < 475) and (posx > 425):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(425, 450, 50, 50))
			if (posx < 525) and (posx > 475):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(475, 450, 50, 50))
			if (posx < 575) and (posx > 525):
				pygame.draw.rect(screeno, (0,150,255), pygame.Rect(525, 450, 50, 50))



		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(25, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(75, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(125, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(175, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(225, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(275, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(325, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(375, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(425, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(475, 450, 50, 50), 3)
		pygame.draw.rect(screeno, (0,0,0), pygame.Rect(525, 450, 50, 50), 3)



		rend = small_fontzy.render("0", 1, (0,0,0))
		screeno.blit(rend, (42, 460))

		rend = small_fontzy.render("1", 1, (0,0,0))
		screeno.blit(rend, (92, 460))

		rend = small_fontzy.render("2", 1, (0,0,0))
		screeno.blit(rend, (142, 460))

		rend = small_fontzy.render("3", 1, (0,0,0))
		screeno.blit(rend, (192, 460))

		rend = small_fontzy.render("4", 1, (0,0,0))
		screeno.blit(rend, (242, 460))

		rend = small_fontzy.render("5", 1, (0,0,0))
		screeno.blit(rend, (292, 460))

		rend = small_fontzy.render("6", 1, (0,0,0))
		screeno.blit(rend, (342, 460))

		rend = small_fontzy.render("7", 1, (0,0,0))
		screeno.blit(rend, (392, 460))

		rend = small_fontzy.render("8", 1, (0,0,0))
		screeno.blit(rend, (442, 460))

		rend = small_fontzy.render("9", 1, (0,0,0))
		screeno.blit(rend, (492, 460))

		rend = small_fontzy.render("10", 1, (0,0,0))
		screeno.blit(rend, (538, 460))




		rend = medium_fontzy.render("Baixo", 1, (0,0,0))

		screeno.blit(rend, (25, 510))

		rend = medium_fontzy.render("Alto", 1, (0,0,0))

		screeno.blit(rend, (515, 510))








		rend = medium_fontzy.render("Definição:", 1, (0,0,0))

		screeno.blit(rend, (25, 150))


		rend = small_fontzy.render("Quão inseguro, stressado, irritado e aborrecido", 1, (0,0,0))

		screeno.blit(rend, (25, 200))

		rend = small_fontzy.render("se sentiu durante a tarefa vs seguro,", 1, (0,0,0))

		screeno.blit(rend, (25, 250))

		rend = small_fontzy.render("gratificado, relaxado e complacente?", 1, (0,0,0))

		screeno.blit(rend, (25, 300))

		rend = small_fontzy.render("", 1, (0,0,0))

		screeno.blit(rend, (25, 350))


		rend = medium_fontzy.render("Nível de frustração:", 1, (0,0,0))

		screeno.blit(rend, (25, 400))


		pygame.display.flip()

		
		timerino = time.time()


		for event in pygame.event.get():
			#
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					posx, posy = pygame.mouse.get_pos()


					if (posy > 450) and (posy < 500):

						if (posx < 75) and (posx > 25):
							questions_file.write("0\n")
							return
						if (posx < 125) and (posx > 75):
							questions_file.write("1\n")
							return
						if (posx < 175) and (posx > 125):
							questions_file.write("2\n")
							return
						if (posx < 225) and (posx > 175):
							questions_file.write("3\n")
							return
						if (posx < 275) and (posx > 225):
							questions_file.write("4\n")
							return
						if (posx < 325) and (posx > 275):
							questions_file.write("5\n")
							return
						if (posx < 375) and (posx > 325):
							questions_file.write("6\n")
							return
						if (posx < 425) and (posx > 375):
							questions_file.write("7\n")
							return
						if (posx < 475) and (posx > 425):
							questions_file.write("8\n")
							return
						if (posx < 525) and (posx > 475):
							questions_file.write("9\n")
							return
						if (posx < 575) and (posx > 525):
							questions_file.write("10\n")
							return











class TextInputBox(pygame.sprite.Sprite):
	def __init__(self, x, y, w, font):
		super().__init__()
		self.color = (0, 0, 0)
		self.backcolor = None
		self.pos = (x, y) 
		self.width = w
		self.font = font
		self.active = False
		self.text = ""
		self.render_text()

	def render_text(self):
		t_surf = self.font.render(self.text, True, self.color, self.backcolor)
		self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
		if self.backcolor:
			self.image.fill(self.backcolor)
		self.image.blit(t_surf, (5, 5))
		pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
		self.rect = self.image.get_rect(topleft = self.pos)

	def update(self, event_list):
		for event in event_list:
			if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
				self.active = self.rect.collidepoint(event.pos)
			if event.type == pygame.KEYDOWN and self.active:
				if event.key == pygame.K_RETURN:
					self.active = False
				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
				self.render_text()


