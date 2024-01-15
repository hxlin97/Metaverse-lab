import numpy as np
def to_array(str_list):
	for i in range(len(str_list)):
		str_list[i] = float(str_list[i])
	return np.array(str_list)
def to_str(float_list):
	for i in range(len(float_list)):
		float_list[i] = str(float_list[i])
	return float_list

df = open('./data_new.txt','r').readlines()
out = open('./1559.coo','w+')