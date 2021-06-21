import time
import numpy as np
import math
import random
import glob
from datetime import datetime
import tensorflow as tf
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.callbacks import EarlyStopping
from numpy.random import seed
from tensorflow.random import set_seed
import matplotlib.pyplot as plt
from sklearn.preprocessing import MultiLabelBinarizer
from imblearn.over_sampling import SMOTE 
from imblearn.over_sampling import SVMSMOTE
from imblearn.over_sampling import BorderlineSMOTE
from imblearn.over_sampling import KMeansSMOTE
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import ADASYN
from imblearn.over_sampling import SMOTENC
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from collections import Counter



def new_get_processed_data(input_path, output_file, slice_number):

	my_data = np.genfromtxt(input_path, delimiter='_')
	my_output = np.genfromtxt(output_file)
	if len(my_data) > len(my_output):
		my_data = my_data[:-1]
	seconds_since = my_data[:, [12, 13, 14]]
	my_data = my_data[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]

	my_output = my_output[..., None]



	new_data = np.zeros((int(len(my_data) - slice_number), len(my_data[0])))

	for i in range(0, len(my_data) - slice_number):

		for j in range(len(my_data[0])):

			if (my_data[i + slice_number][j] > 99999 or my_data[i + slice_number][j] < -99999 or my_data[i][j] > 99999 or my_data[i][j] < -99999):
				new_data[int(i/slice_number)][j] = 0

			else:
				new_data[i][j] = my_data[i + slice_number][j] - my_data[i][j]

	new_seconds =np.zeros((int(len(seconds_since) - slice_number), len(seconds_since[0])))

	for i in range(0, len(seconds_since) - slice_number):

		for j in range(len(seconds_since[0])):

			new_seconds[i][j] = seconds_since[i + slice_number][j]


	new_data = np.concatenate((new_data, new_seconds), axis=1)


	
	forest_output = np.zeros((int(len(my_output) - slice_number), 1))

	for i in range(0, len(my_output) - slice_number):

		if (my_output[i + slice_number][0] - my_output[i][0]) > 0:

			forest_output[i] = 2


		elif (my_output[i + slice_number][0] - my_output[i][0]) < 0:

			forest_output[i] = 0

		else:

			forest_output[i] = 1




	return new_data, forest_output





def predict_traces_on_folder():


	my_data_list = sorted(glob.glob("./Traces/Trainers/Perceptor*.txt"))

	my_output_list = sorted(glob.glob("./Traces/Trainers/Fader*.txt"))



	model = Sequential([
		InputLayer(input_shape = (20,)),
		Dense(30, activation='tanh'),
		Dense(30, activation='tanh'),
		Dense(1)
		])

	model.compile(optimizer = "adam", loss = "mse", metrics=[tf.keras.metrics.MeanSquaredError()])

	es = EarlyStopping(patience=7)




	#Training 


	# for i in range(len(my_data_list)):
	# 	my_data, my_output = get_processed_data(my_data_list[i], my_output_list[i])



	# 	model.fit(my_data, my_output, epochs = 1000, batch_size = 128, validation_split = 0.2, callbacks=[es], shuffle=True)

	my_data, my_output = get_processed_data(my_data_list[0], my_output_list[0])

	for i in range(1, len(my_data_list)):

		prov_data, prov_out = get_processed_data(my_data_list[i], my_output_list[i])
		my_data = np.concatenate((my_data, prov_data), axis=0)
		my_output = np.concatenate((my_output, prov_out), axis=0)



	model.fit(my_data, my_output, epochs = 1000, batch_size = 128, validation_split = 0.1, callbacks=[es], shuffle=True)




	#Predicting


	my_data_list = sorted(glob.glob("./Traces/To_Predict/Perceptor*.txt"))

	print(my_data_list)


	my_output_list = sorted(glob.glob("./Traces/To_Predict/Fader*.txt"))



	for i in range(len(my_data_list)):
		# my_data = np.genfromtxt(my_data_list[i], delimiter='_')
		# #my_data = my_data[:-1]
		# my_output = np.genfromtxt(my_output_list[i])
		# my_output = my_output[..., None]

		my_data, my_output = get_processed_data(my_data_list[i], my_output_list[i])


		prediction = model.predict(my_data)


		total_number = 0
		right_polarity_number = 0
		positive_number = 0
		negative_number = 0

		for j in range(len(prediction)):
			print(str(j) + ": " + str(prediction[j]) + "->" + str(my_output[j]))
			total_number += 1
			if ((prediction[j] <= 0) and (my_output[j] <= 0)) or ((prediction[j] > 0) and (my_output[j] > 0)):
				right_polarity_number += 1
			if my_output[j] <= 0:
				negative_number += 1
			if my_output[j] > 0:
				positive_number += 1
		
		
		print("MEAN SQUARED ERROR OF PREDICTION:")
		mse = tf.keras.losses.MeanSquaredError()
		print(mse(my_output, prediction).numpy())
		print("PERCENTAGE OF ALL NEGATIVE:")
		print(negative_number/total_number * 100)
		print("PERCENTAGE OF ALL POSITIVE:")
		print(positive_number/total_number * 100)
		print("PERCENTAGE OF CORRECT GRADIENT RESULTS:")
		print(right_polarity_number/total_number * 100)


def remove_outliers(my_data_list, my_output_list):

	to_remove = []

	for i in range(len(my_output_list)):

		my_output = np.genfromtxt(my_output_list[i])
		remove = True
		for j in my_output:
			if j != 0.0:
				remove = False
		if remove:
			to_remove.append(i)


	inversy = to_remove[::-1]

	for remo in inversy:
		del my_data_list[remo]
		del my_output_list[remo]

	return my_data_list, my_output_list





def new_leave_one_out(slice_number, balance_data):

	dimensions = ["Arousal", "Pleasure", "Dominance"]


	print_list = [[], [], []]

	print_counter = 0


	#sm = SMOTE(random_state=42)
	#sm = SVMSMOTE(random_state=42)
	#sm = BorderlineSMOTE(random_state=42)
	#sm = KMeansSMOTE(random_state=42)
	#sm = RandomOverSampler(random_state=42)
	#sm = ADASYN(random_state=42)
	sm = RandomUnderSampler(random_state=42)




	print("Slice Number: ", slice_number)

	print("Balancing: ", balance_data)





	print_list = [[], [], []]

	print_counter = 0



	for dim in dimensions:

		print("\n\n\n\n\n\n\n\n\n\nDimension: " + dim)


		dirty_data_list = sorted(glob.glob("./First_Study/" + dim + "/Traces_Perceptor*.txt"))

		dirty_output_list = sorted(glob.glob("./First_Study/" + dim + "/Traces_" + dim + "*.txt"))

		my_data_list, my_output_list = remove_outliers(dirty_data_list, dirty_output_list)

		dim_accuracy = 0

		forest_accuracy = 0

		rangy = len(my_data_list)

		mse_sum = 0 
		negative_per_sum = 0
		positive_per_sum = 0
		correct_pol_sum = 0
		forgiving_pol_sum = 0
		sum_confusion_matrix = np.zeros((3,3))


		

		for k in range(rangy):



			clf = RandomForestClassifier(n_estimators = 300, random_state=42, criterion = "gini")  #class_weight = "balanced"

			print(my_output_list[k])

			prediction_data_list = [my_data_list[k]]
			prediction_output_list = [my_output_list[k]]



			my_data, forest_output = new_get_processed_data(my_data_list[0], my_output_list[0], slice_number)



			for i in range(1, len(my_data_list)):

				prov_data, prov_forest = new_get_processed_data(my_data_list[i], my_output_list[i],slice_number)
				my_data = np.concatenate((my_data, prov_data), axis=0)
				forest_output = np.concatenate((forest_output, prov_forest), axis=0)



			######################################
			###### To Balance or not to Balance...
			######################################


			######### TO BALANCE

			if balance_data:


				balanced_my_data_forest, balanced_my_output_forest = sm.fit_resample(my_data, forest_output)
			
			#print(np.bincount(np.ravel(balanced_my_output_forest).astype(int)))

			#################################################





			######### NOT TO BALANCE

			else:

				balanced_my_data_forest = my_data

				balanced_my_output_forest = forest_output

			##################################################


			clf.fit(balanced_my_data_forest, balanced_my_output_forest)



			my_data, forest_output = new_get_processed_data(prediction_data_list[0], prediction_output_list[0], slice_number)




			forest_predict = clf.predict(my_data)


			for_acc = accuracy_score(forest_output, forest_predict)

			conf_mat = confusion_matrix(forest_output, forest_predict, labels = [0., 1., 2.])



			print(clf.feature_importances_)

			print("Accuracy: ", for_acc)

			print(conf_mat)




			forest_accuracy += for_acc

			sum_confusion_matrix = sum_confusion_matrix + conf_mat

			dirty_data_list = sorted(glob.glob("./First_Study/" + dim + "/Traces_Perceptor*.txt"))

			dirty_output_list = sorted(glob.glob("./First_Study/" + dim + "/Traces_" + dim + "*.txt"))

			my_data_list, my_output_list = remove_outliers(dirty_data_list, dirty_output_list)

			
			




		print_list[print_counter].append("\n\n\n\n-----> " + dim)


		print_list[print_counter].append("\n\n Random Forest Accuracy:")


		print_list[print_counter].append(forest_accuracy/rangy)


		print_list[print_counter].append("\n\n Random Forest Confusion Matrix:")


		print_list[print_counter].append(sum_confusion_matrix/rangy)
		


		print_counter += 1


	#The final printing

	for i in range(3):
		for text in print_list[i]:
			print(text)








def save_dimension_over_time(file_name):

	#data, output = get_processed_data(input_path, output_file)

	output = np.genfromtxt(file_name)

	fig4 = plt.figure()
	ax4 = fig4.add_subplot(111)

	numbering = range(len(output))

	ax4.plot(numbering, output)


	plt.xlabel("Ticks")
	plt.ylabel("Level")
	fig_name = "Figures/" + file_name.replace('.txt','')
	fig4.savefig(fig_name)



def save_location_over_time(file_name):

	#data, output = get_processed_data(input_path, output_file)

	f = open(file_name)

	output = f.readlines()


	x_list = []
	y_list = []

	for inpy in output:
		x_y = inpy.split("_")
		x_list.append(int(x_y[0]))
		y_list.append(-int(x_y[1].replace('\n','')))




	fig4 = plt.figure()
	ax4 = fig4.add_subplot(111)

	numbering = range(len(output))

	ax4.plot(x_list, y_list)


	plt.xlabel("Level")
	plt.ylabel("Ticks")
	plt.axis('equal')
	fig_name = "Figures/" + file_name.replace('.txt','')
	fig4.savefig(fig_name)



def save_dimension_over_location(location_file, dimension_file, slice_number):


	f = open(location_file)

	output = f.readlines()


	x_list = []
	y_list = []

	for inpy in output:
		x_y = inpy.split("_")
		x_list.append(int(x_y[0]))
		y_list.append(-int(x_y[1].replace('\n','')))


	dimension = np.genfromtxt(dimension_file)

	dimension = dimension[..., None]

	new_output = np.zeros((int(len(dimension)/slice_number),1))

	for i in range(0, len(dimension) - slice_number, slice_number):

		new_output[int(i/slice_number)][0] = dimension[i + slice_number][0] - dimension[i][0]


	#data, output = get_processed_data(input_path, output_file)

	colour_list = []

	for i in range(len(new_output)):

		colour_code = 'k'

		if new_output[i][0] <= -1:
			colour_code = 'r'

		elif new_output[i][0] >= 1:
			colour_code = 'g'

		for j in range(24):
			colour_list.append(colour_code)



	while(len(x_list) > len(colour_list)):
		colour_list.append(colour_list[len(colour_list)-1])




	fig4 = plt.figure()
	ax4 = fig4.add_subplot(111)
	img = plt.imread("try.png")

	ax4.imshow(img, extent=[-190, 2230, -960, 260])



	for i in range(len(x_list)):
		ax4.scatter(x_list[i], y_list[i], c = colour_list[i], alpha=0.1)

	plt.xlabel("Level")
	plt.ylabel("Ticks")
	plt.axis('equal')


	plt.xlim([-200, 2200])
	plt.ylim([-1000, 200])
	fig_name = "Figures/" + dimension_file.replace('.txt','') + "_DIMENSION_LOC"
	fig4.savefig(fig_name)



	#idea: use this but with for loops to create a lot of tiny sections (1 or 3 seconds?).
	#Colour each either black (neutral), red (decreasing) or green (rising)

	# x = np.linspace(-10, 10, 1000)
	# y = np.sin(x)

	# # 4 segments defined according to some x properties
	# segment1 = (x<-5)
	# segment2 = (x>=-5) & (x<0)
	# segment3 = (x>=0) & (x<5)
	# segment4 = (x>=5)

	# plt.plot(x[segment1], y[segment1], '-k', lw=2)
	# plt.plot(x[segment2], y[segment2], '-g', lw=2)
	# plt.plot(x[segment3], y[segment3], '-r', lw=2)
	# plt.plot(x[segment4], y[segment4], '-b', lw=2)

	# plt.show()


def print_images_folder(folder_name, slice_number):


	position_arousal_traces_list = glob.glob(folder_name + "/Arousal/Traces_Position*.txt")
	position_pleasure_traces_list = glob.glob(folder_name + "/Pleasure/Traces_Position*.txt")
	position_dominance_traces_list = glob.glob(folder_name + "/Dominance/Traces_Position*.txt")

	position_traces_list = sorted(position_arousal_traces_list + position_pleasure_traces_list + position_dominance_traces_list)


 #We need to solve this folder thingy things! Doesn't work like this

	arousal_traces_list = glob.glob(folder_name + "/Arousal/Traces_Arousal*.txt")
	pleasure_traces_list = glob.glob(folder_name + "/Pleasure/Traces_Pleasure*.txt")
	dominance_traces_list = glob.glob(folder_name + "/Dominance/Traces_Dominance*.txt")

	dimension_traces_list = sorted(arousal_traces_list + pleasure_traces_list + dominance_traces_list)

	for i in range(len(position_traces_list)):
		save_dimension_over_time(dimension_traces_list[i])
		save_dimension_over_location(position_traces_list[i], dimension_traces_list[i], slice_number)





def number_crawlwer():
	number_list = glob.glob("First_Study/Student_Number/*.txt")

	writy = open("number_file.txt", "w")

	for numb in number_list:
		f = open(numb)
		number = f.readlines()

		writy.write(number[0])

		# for n in number:
		# 	print(n)





seed(7)
set_seed(7)

slice_number = 24
balance_data = True

#number_crawlwer()


new_leave_one_out(slice_number, balance_data)


# print_images_folder("First_Study", slice_number)















