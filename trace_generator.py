import random






ACTION_LIST = ['w', 's', 'a', 'd', ' ']



def file_to_actions_translator(file_location):

	w_pressed = 0
	s_pressed = 0
	a_pressed = 0
	d_pressed = 0

	attack = 0

	new_actions = []

	f = open(file_location)
	lines = f.readlines()



	for line in lines:
		line_array = eval(line)
		new_line = []
		for i in range(0, len(line_array)):
			if i == 0:
				new_line.append(line_array[i])
			else:
				if line_array[i] == 'dd':
					if a_pressed == 2:
						a_pressed = 1
					d_pressed = 2
					
				if line_array[i] == 'du':
					if a_pressed == 1:
						a_pressed = 2
					d_pressed = 0


				if line_array[i] == 'ad':
					if d_pressed == 2:
						d_pressed = 1
					a_pressed = 2
					
				if line_array[i] == 'au':
					if d_pressed == 1:
						d_pressed = 2
					a_pressed = 0


				if line_array[i] == 'wd':
					if s_pressed == 2:
						s_pressed = 1
					w_pressed = 2
					
				if line_array[i] == 'wu':
					if s_pressed == 1:
						s_pressed = 2
					w_pressed = 0


				if line_array[i] == 'sd':
					if w_pressed == 2:
						w_pressed = 1
					s_pressed = 2
					
				if line_array[i] == 'su':
					if w_pressed == 1:
						w_pressed = 2
					s_pressed = 0

				if line_array[i] == ' ':
					attack = 1

		if w_pressed == 2:
			new_line.append('w')
		if s_pressed == 2:
			new_line.append('s')
		if a_pressed == 2:
			new_line.append('a')
		if d_pressed == 2:
			new_line.append('d')
		if attack:
			new_line.append(' ')
			attack = 0

		new_actions.append(new_line)


	return new_actions


def actions_to_file_translator(action_array, new_file_location = None):


	to_write = []

	w_pressed = 0
	s_pressed = 0
	a_pressed = 0
	d_pressed = 0

	attack = 0


	for actions in action_array:

		write_line = []

		if len(actions):
			write_line.append(actions[0])

		if w_pressed:

			w_found = 0
			for i in range(len(actions)):
				if actions[i] == 'w':
					w_found = 1
					break

			if w_found:
				pass
			else:
				write_line.append('wu')
				w_pressed = 0


		if s_pressed:

			s_found = 0
			for i in range(len(actions)):
				if actions[i] == 's':
					s_found = 1
					break

			if s_found:
				pass
			else:
				write_line.append('su')
				s_pressed = 0

		if a_pressed:

			a_found = 0
			for i in range(len(actions)):
				if actions[i] == 'a':
					a_found = 1
					break

			if a_found:
				pass
			else:
				write_line.append('au')
				a_pressed = 0


		if d_pressed:

			d_found = 0
			for i in range(len(actions)):
				if actions[i] == 'd':
					d_found = 1
					break

			if d_found:
				pass
			else:
				write_line.append('du')
				d_pressed = 0






		for i in range(len(actions)):


			if actions[i] == 'w':
				if w_pressed == 0:
					w_pressed = 1
					write_line.append('wd')

			if actions[i] == 's':
				if s_pressed == 0:
					s_pressed = 1
					write_line.append('sd')

			if actions[i] == 'a':
				if a_pressed == 0:
					a_pressed = 1
					write_line.append('ad')

			if actions[i] == 'd':
				if d_pressed == 0:
					d_pressed = 1
					write_line.append('dd')

			if actions[i] == ' ':
				write_line.append(' ')

		to_write.append(write_line)


	if new_file_location != None:

		writy = open(new_file_location, "w+")

		for line in to_write:
			writy.write(str(line) + '\n')

	return to_write





def random_trace_generator(trace_lenght, file_name):

	action_array = []

	action_array.append([])



	for i in range(trace_lenght):
		actions = []
		actions.append(i)
		actions.append(random.choice(ACTION_LIST))
		action_array.append(actions)



	actions_to_file_translator(action_array, "Generated_Traces/" + file_name)



def probability_trace_generator(trace_lenght, file_name, probability_list):

	action_array = []

	action_array.append([])



	for i in range(trace_lenght):
		actions = []
		actions.append(i)
		actions.append(random.choices(ACTION_LIST, weights=probability_list, k=1)[0])
		action_array.append(actions)



	actions_to_file_translator(action_array, "Generated_Traces/" + file_name)
















# action_array = file_to_actions_translator("First_Study/Arousal/Traces_Actions_Level3_26-04-2021_11-25-09_453.txt")

# actions_to_file_translator(action_array, "Generated_Traces/Test1.txt")





#random_trace_generator(500, "Gen1.txt")


#probability_trace_generator(2000, "ProbGen1.txt", [1,2,1,9,2])


















