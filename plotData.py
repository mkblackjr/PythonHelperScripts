# # plotData.py

import matplotlib
import matplotlib.pyplot as plt
import numpy
import time

def plotData(x_data=[[1,2,3],[7,8,9],[4,5,6],[10,11,12]],
			y_data=[[13, 14, 15],[1,2,3],[10,11,12],[4,5,6]],**kwargs):

	title = kwargs.get('title',"Title")
	x_label_array = kwargs.get('x_label',"X_Label")
	y_label_array = kwargs.get('y_label',"Y_label")
	legend_array = kwargs.get('legend',"Legend")
	image_name = kwargs.get('image_name',"image")
	subplots = kwargs.get('subplots',1)
	sub_cols = kwargs.get('subplot_columns',1)
	colors = kwargs.get('colors',['b','g','r'])
	save = kwargs.get('save',True)
	sync = kwargs.get('sync',False)

	# # Some parameters for debugging
	# x_data = [[1,2,3],[7,8,9],[4,5,6],[10,11,12]]
	# y_data = [[13, 14, 15],[1,2,3],[10,11,12],[4,5,6]]
	# title_array = ["title1","title2"]
	# x_label_array = ["x1","x2"]
	# y_label_array = ["y1","y2"]
	# subplots = 2
	# colors=['b','g','r']
	
	# Initializations
	one_plot = False
	legend = []
	k = 0

	# Determine configuration of 2D/1D array containing data
	if((type(x_data[0]) is float) | (type(x_data[0]) is numpy.float64)):
		subplot_1 = 1; subplot_2 = 1; subplot_3 = 1
		x_len = 1
		one_plot = True	
	else: 
		subplot_1 = 1*subplots/sub_cols
		subplot_2 = sub_cols
		subplot_3 = 1
		x_len = len(x_data)

	# Prepare figure for multiple plots
	plt.hold(True)
	font = {'size':5}
	matplotlib.rc('font',**font)
	fig = plt.figure(1)
	fig.subplots_adjust(hspace=1)
	fig.subplots_adjust(wspace=.17)
	fig.text(0.29, 0.04, x_label_array[0], ha='center', va='center')
	fig.text(0.72, 0.04, x_label_array[0], ha='center', va='center')
	fig.text(0.02, 0.5, y_label_array[0], ha='center', va='center', rotation='vertical')
	plt.suptitle(title)


	# Produce desired number of plots/subplots based on data formatting
	for i in range(subplots):
		print("subplot_val = " + str(subplot_1) + "," + str(subplot_2) + "," + str(subplot_3))
		plt.subplot(subplot_1,subplot_2,subplot_3)
		for j in range(int(x_len/subplots)):
			if not one_plot:
				plt.plot(x_data[k],y_data[k],colors[j])
				plt.title("Test " + str(k+1))
				if sync:
					axes = plt.gca()
					axes.set_xlim([0.035,0.16])
					axes.set_ylim([-2,-3.5])
			else:
				plt.plot(x_data,y_data,colors[j])
			k += 1
		subplot_3 += 1
		# try:
		# 	plt.xlabel(x_label_array[i])
		# 	plt.ylabel(y_label_array[i])
		# except:
		# 	plt.xlabel(x_label_array[-1])
		# 	plt.ylabel(y_label_array[-1])
		# plt.legend(legend_array)
	
	# Show and save plot to specified location
	if save:
		fig = plt.gcf()
		plt.ion()
		plt.show()
		plt.hold(False)
		fig.savefig(str(image_name))
		# plt.close('all')
	else:
		plt.ion()
		plt.show()
		plt.hold(False)
		# plt.close('all')
	
	return
