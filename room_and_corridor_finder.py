import os
from copy import copy, deepcopy
import string


def printMapMatrix(map_matrix, file_name):

	found_numbers = []
	possible_characters = string.ascii_lowercase + string.ascii_uppercase
	nothing_char = "_"

	if os.path.exists(file_name):
		os.remove(file_name)
	f = open(file_name, "a+")

	for line in map_matrix:
		for num in line:
			if num == 0:
				chari = nothing_char
			else:
				if num not in found_numbers:
					found_numbers.append(num)

				chari = possible_characters[found_numbers.index(num)]

			f.write(chari)
		f.write("\n")
	f.close()



def csv_to_zero_and_ones_matrix(file_name):
	file_path = "Maps/" + file_name + ".csv"

	f = open(file_path, "r")
	lines = f.readlines()


	map_matrix = []

	line_count = 0

	for line in lines:
		line_array = []
		column_count = 0
		line = line.replace('	', '')
		line = line.replace(';', '')

		for letter in line:

			if letter == '.':

				line_array.append(1)

			elif letter == '0':
				line_array.append(1)
			elif letter == '\n':
				pass
			elif letter == ' ':
				line_array.append(0)
			elif letter == '	':
				line_array.append(0)	
			elif letter == '_':
				line_array.append(0)	
			elif letter == "r":
				line_array.append(1)
			elif letter == "m":
				line_array.append(1)
			elif letter == 'f':
				line_array.append(1)
			elif letter == 'x':
				line_array.append(0)
			elif letter == "p":
				player_pos = (line_count, column_count)
				line_array.append(1)

			column_count += 1
		map_matrix.append(line_array)
		line_count += 1

	return map_matrix, player_pos



def load(file_name):

	# To read different file formats, just implement a different csv_to_zero_and_ones_matrix function and change it here!
	map_matrix, player_pos = csv_to_zero_and_ones_matrix(file_name)


	aux_vertical_matrix = deepcopy(map_matrix)


	# Find the vertical lenght of each verticl segment that is bounded by walls by summing the left position plus one.
	for line in range(len(aux_vertical_matrix)):
		for pos in range(len(aux_vertical_matrix[0])):
			if line == 0:
				pass
			else:
				if aux_vertical_matrix[line-1][pos] and aux_vertical_matrix[line][pos]:
					aux_vertical_matrix[line][pos] = aux_vertical_matrix[line-1][pos] + 1

	# Now go from bot to top and assign each position the number of it's connected rightmost neighbour
	for line in range(len(aux_vertical_matrix), 0, -1):
		for pos in range(len(aux_vertical_matrix[0])):
			if line == 0:
				pass
			else:
				if aux_vertical_matrix[line-1][pos] and aux_vertical_matrix[line][pos]:
					aux_vertical_matrix[line-1][pos] = aux_vertical_matrix[line][pos]	


	join_matrix = deepcopy(aux_vertical_matrix)

	# #Now let's clean this a bit

	for line in range(len(aux_vertical_matrix)):
		for pos in range(len(aux_vertical_matrix[0])-1):

			if aux_vertical_matrix[line][pos] == aux_vertical_matrix[line][pos+1]:
				continue
			else:
				for aux_pos in range(pos, len(aux_vertical_matrix[0])-1):
					if aux_vertical_matrix[line][aux_pos] == 0:
						break
					if aux_vertical_matrix[line][aux_pos] == aux_vertical_matrix[line][pos]:
						for second_aux_pos in range(aux_pos, pos, -1):
							join_matrix[line][second_aux_pos] = aux_vertical_matrix[line][pos]



	# Finally, we need to ensure all groups have unique identifiers and get their members on a nice list of lists
	visited_positions = []

	groups = []
	for line in range(len(join_matrix)):
		for pos in range(len(join_matrix[0])):

			if join_matrix[line][pos] == 0:
				continue
			else:
				if (line,pos) not in visited_positions:
					new_group = []
					for aux_line in range(line, len(join_matrix)):
						if join_matrix[aux_line][pos] != join_matrix[line][pos]:
							break
						for aux_pos in range(pos, len(join_matrix[0])):
							if join_matrix[line][pos] == join_matrix[aux_line][aux_pos]:
								visited_positions.append((aux_line, aux_pos))
								new_group.append((aux_line, aux_pos))
							else:
								break

					groups.append(new_group)
				else:
					continue

	for group in groups:
		for member in group:
			join_matrix[member[0]][member[1]] = groups.index(group) + 1


	printMapMatrix(join_matrix, "map_room_identification_testing.txt")

	return join_matrix, groups, player_pos





#load("Level18")



















