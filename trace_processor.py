import random
import string
import Levenshtein as lv 
import glob
import numpy as np
from sklearn.cluster import AffinityPropagation
import os
import shutil




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


def actions_to_string_translator(action_list):
	
	possible_actions = ['n', ' ', 'w', 's', 'a', 'd', 'wa', 'wd', 'sa', 'sd', 'w ', 's ', 'a ', 'd ', 'wa ', 'wd ', 'sa ', 'sd ']

	action_encoding = list(string.ascii_lowercase)[:len(possible_actions)]

	action_string = ""

	for action in action_list:
		if len(action) == 0:
			pass
		if len(action) == 1:
			action_string += action_encoding[possible_actions.index('n')]
		if len(action) == 2:
			action_string += action_encoding[possible_actions.index(action[1])]
		if len(action) == 3:
			lil_string = str(action[1]) + str(action[2])
			action_string += action_encoding[possible_actions.index(lil_string)]
		if len(action) == 4:
			lil_string = str(action[1]) + str(action[2]) + str(action[3])
			action_string += action_encoding[possible_actions.index(lil_string)]

	return action_string




def levenshtein_distance_between_traces(trace_file_1, trace_file_2):

	actions1 = file_to_actions_translator(trace_file_1)
	actions2 = file_to_actions_translator(trace_file_2)

	string1 = actions_to_string_translator(actions1)
	string2 = actions_to_string_translator(actions2)

	distance = lv.distance(string1, string2)

	return distance




def levenshtein_afinity_clustering(glob_file_path):

	words = glob.glob(glob_file_path)

	#words = "YOUR WORDS HERE".split(" ") #Replace this line
	words = np.asarray(words) #So that indexing with a list will work
	lev_similarity = -1*np.array([[levenshtein_distance_between_traces(w1,w2) for w1 in words] for w2 in words])

	affprop = AffinityPropagation(affinity="precomputed", damping=0.5, max_iter = 200, convergence_iter = 15)
	affprop.fit(lev_similarity)
	counter = 1

	#Delete previous clustering
	folder = "./Clusters"
	for filename in os.listdir(folder):
	    file_path = os.path.join(folder, filename)
	    try:
	        if os.path.isfile(file_path) or os.path.islink(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path):
	            shutil.rmtree(file_path)
	    except Exception as e:
	        print('Failed to delete %s. Reason: %s' % (file_path, e))


	for cluster_id in np.unique(affprop.labels_):
		print("\n\nCluster Number: ", counter)
		exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
		cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
		folder_name = "./Clusters/" + str(counter) + "_____" + str(len(cluster))
		os.mkdir(folder_name)
		print("\n\nNumber of Traces in Cluster: ", len(cluster))
		for clusty in cluster:
			shutil.copy(clusty, folder_name)
			#Copying the images related to the traversal of the game. We need this to know what is going on
			clusty_id = clusty.split('/')[3][15:-4]
			print(clusty_id)
			images = glob.glob("./Figures/*/*/*"+clusty_id+"_DIMENSION_LOC.png")
			print("GLOB: ", images)
			for img in images:
				shutil.copy(img, folder_name)



		cluster_str = ", ".join(cluster)
		print("Example:   %s:\n Members:  %s" % (exemplar, cluster_str))
		counter += 1






if __name__ == '__main__':
	levenshtein_afinity_clustering("./First_Study/*/Traces_Actions_Level*.txt")



	# trace_file_1 = "./First_Study/Arousal/Traces_Actions_Level3_27-04-2021_11-56-47_926.txt"
	# trace_file_2 = "./First_Study/Arousal/Traces_Actions_Level3_26-04-2021_11-25-09_453.txt"


	# print(levenshtein_distance_between_traces(trace_file_1, trace_file_2))









