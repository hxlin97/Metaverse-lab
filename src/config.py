from utils import *
T = 300

file = open("../ForceFieldParameters/FF_parameters1")
text = file.readlines()
parameters = {1: extract_feature_data_from_text(text, "H", T=T),
              2: extract_feature_data_from_text(text, "O", T=T),
              3: extract_feature_data_from_text(text, "Na", T=T),
              4: extract_feature_data_from_text(text, "Cl", T=T),}

# parameters = {1: extract_feature_data_from_text(text, "H", T=T),
#               2: extract_feature_data_from_text(text, "C", T=T),
#               3: extract_feature_data_from_text(text, "O", T=T),
#               4: extract_feature_data_from_text(text, "N", T=T),
#               5: extract_feature_data_from_text(text, "F", T=T),
#               6: extract_feature_data_from_text(text, "Na", T=T),
#               7: extract_feature_data_from_text(text, "Cl", T=T),
#               8: extract_feature_data_from_text(text, "Y", T=T),
#               9: extract_feature_data_from_text(text, "Yb", T=T),
#               10: extract_feature_data_from_text(text, "Tm", T=T),
#               11: extract_feature_data_from_text(text, "Er", T=T),
#               }
# 1H2O3Mg4N
# T = 400K

num_nearest_atoms = 4
device = 'cuda:2'
sep = 0.7
batch_size = 1
learning_rate = 1e-4
epochs = 10
print_interval = 5
last_frame = None
interval_frame = 8
filename = 'example'
path = f"../dataset/{filename}.lammpstrj"
# path = f"../dataset/{filename}/dump.reax.mixture"
ratio = True # whether the system is represented by ratio