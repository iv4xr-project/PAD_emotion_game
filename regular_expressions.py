import re

import glob

from trace_processor import get_pad_classes, transform_arrays_into_same_size

import string

import room_and_corridor_finder




def getRegularExpressionStringsFromFiles(file_path, slice_num, map_name = "Level1", map_granularity = 20):

	"""
	A function that turns trace data into expressions that can be validated using Regular Expressions
	"""

	_, groups, player_pos = room_and_corridor_finder.load(map_name)


	arousal_files_location = sorted(glob.glob(file_path + "/Arousal/Traces_Position*.txt"))
	arousal_files_pad =sorted(glob.glob(file_path + "/Arousal/Traces_Arousal*.txt"))

	# print(len(arousal_files_location))
	# print(len(arousal_files_pad))

	r_e_list = []

	for i in range(len(arousal_files_location)):
		print(arousal_files_location[i])
		f = open(arousal_files_location[i])
		locations = f.readlines()
		#locations = list(actions_to_string_translator(file_to_actions_translator(arousal_files_location[i])))
		pad_classes = get_pad_classes(arousal_files_pad[i], slice_number = slice_num)


		# print(len(locations))
		# print(len(pad_classes))


		pad_classes, locations = transform_arrays_into_same_size(pad_classes, locations)

		# print(len(pad_classes))
		# print(len(locations))

		

		r_e = ""

		#print(groups[0])

	

		for cat, loc in zip(pad_classes, locations):

			#print(cat)
			#print(loc)
			loc = loc.replace("\n","").split("_")

			#print("The moving locations: ", loc)
			#print("Them after the division: ",int(loc[1])//20, " and ", int(loc[0])//20 )
			

			#print("Test: ", (int(loc[0])//20) + player_pos[0])



			aux_loc = (int(loc[1])//20 + player_pos[0], int(loc[0])//20 + player_pos[1])

			room_num = None

			#print((aux_loc[0], aux_loc[1]))
			for group in groups:
				if (aux_loc[0], aux_loc[1]) in group:
					#print("Found it! It's in group ", groups.index(group))
					room_num = groups.index(group)
					break

			

			#room_num = groups.index((loc[1], loc[0]))

			#print(player_pos)

			if room_num == None:
				print("Can't find the room that corresponds to the position!")
				exit()

			#Debugging
			possible_characters = string.ascii_lowercase + string.ascii_uppercase
			# print(loc)
			# print(room_num)
			# print(possible_characters[room_num])


			if cat == 0:
				r_e += "R" + str(room_num) + "AdPn"
			else:
				r_e += "R" + str(room_num) + "AiPn"




		r_e_list.append(r_e)


		print("\n")
		print(r_e)
		print("\n")



	return r_e_list





def getRegularExpressionStringsFromPADClassesAndLocationFile(pad_classes_list, location_file_path, slice_num, map_name = "Level1", map_granularity = 20):

	"""
	A function that turns trace data into expressions that can be validated using Regular Expressions
	"""

	_, groups, player_pos = room_and_corridor_finder.load(map_name)


	files_location = sorted(glob.glob(location_file_path + "/Bot_Position*"))




	r_e_list = []

	for i in range(len(files_location)):
		#print(arousal_files_location[i])
		f = open(files_location[i])
		locations = f.readlines()


		# print(len(locations))
		# print(len(pad_classes))
		pad_classes = pad_classes_list[i]


		pad_classes, locations = transform_arrays_into_same_size(pad_classes, locations)

		# print(len(pad_classes))
		# print(len(locations))

		

		r_e = ""

		#print(groups[0])

	

		for cat, loc in zip(pad_classes, locations):

			#print(cat)
			#print(loc)
			loc = loc.replace("\n","").split("_")

			#print("The moving locations: ", loc)
			#print("Them after the division: ",int(loc[1])//20, " and ", int(loc[0])//20 )
			

			#print("Test: ", (int(loc[0])//20) + player_pos[0])



			aux_loc = (int(loc[1])//20 + player_pos[0], int(loc[0])//20 + player_pos[1])

			room_num = None

			#print((aux_loc[0], aux_loc[1]))
			for group in groups:
				if (aux_loc[0], aux_loc[1]) in group:
					#print("Found it! It's in group ", groups.index(group))
					room_num = groups.index(group)
					break

			

			#room_num = groups.index((loc[1], loc[0]))

			#print(player_pos)

			if room_num == None:
				room_num = "n"
				print("Can't find the room that corresponds to the position!")
				#exit()

			#Debugging
			possible_characters = string.ascii_lowercase + string.ascii_uppercase
			# print(loc)
			# print(room_num)
			# print(possible_characters[room_num])


			if cat == 0:
				r_e += "R" + str(room_num) + "AdPn"
			else:
				r_e += "R" + str(room_num) + "AiPn"




		r_e_list.append(r_e)



	return r_e_list




def satisfiesRegEx(string, reg_ex):

	return re.fullmatch(reg_ex, string)



def listSatisfiesRegEx(string_list, reg_ex):

	fail_accept_list = []


	for reggy in string_list:
		x = re.fullmatch(reg_ex, reggy)
		if x:
			fail_accept_list.append("A")
		else:
			fail_accept_list.append("F")


	return fail_accept_list




def main():


	#test_expression = "(R.AdP.)*(R.AiP.)*(R.AdP.)+(R.AiP.)+(R.AdP.)*"

	test_expression = ".*(R.AiP.){6}.*" # ".*(R4AiP.)+.*"

	print(satisfiesRegEx("R1AdPnR1AiPnR1AiPnR2AiPnR1AiPnR1AiPnR1AiPnR1AdPnR1AdPnR1AdPn", test_expression))

	exit()

	r_e_list = getRegularExpressionStringsFromFiles("./First_Study", slice_num = 3)


	fail_accept_list = []


	for reggy in r_e_list:
		x = re.fullmatch(test_expression, reggy)
		if x:
			fail_accept_list.append("A")
		else:
			fail_accept_list.append("F")

	print(fail_accept_list)

	print("Number of accepted: ", fail_accept_list.count("A"))
	print("Number of failures: ", fail_accept_list.count("F"))





if __name__=="__main__":
	main()

























