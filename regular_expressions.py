import re

from trace_processor import *




def getRegularExpressionStrings(file_path, slice_num):

	"""
	A function that turns trace data into expressions that can be validated using Regular Expressions
	"""

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


		### Needs more things here, just a quick test

		r_e = ""

		for cat in pad_classes:
			if cat == 0:
				r_e += "R0AdPn"
			else:
				r_e += "R0AiPn"

		r_e_list.append(r_e)


		print("\n")
		print(r_e)
		print("\n")



	return r_e_list





def test():

	# "(R1AiPd)((R(2|3)AiP.)|(R4AdP.))*(R5A.Ps)"

	# R- Room

	# A- Arousal
	# P- Pleasure

	# i- Icrease
	# d- Decrease
	# s- Steady

	txt = "R1AiPdR3AiPdR4AdPiR5AiPs"



	x = re.fullmatch("(R1AiPd)((R(2|3)AiP.)|(R4AdP.))*(R5A.Ps)", txt)


	print(x)





test_expression = "(R.AdP.)*(R.AiP.)*(R.AdP.)+(R.AiP.)+(R.AdP.)*"

r_e_list = getRegularExpressionStrings("./First_Study", slice_num = 3)


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





























