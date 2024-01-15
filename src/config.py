from utils import *
T = 400

file = open("../dataset/FB_reax/forcefield.reax")
text = file.readlines()
# extracted_info = extract_feature_data_from_text(text, 'C')
parameters = {1: extract_feature_data_from_text(text, "H", T=T),
              2: extract_feature_data_from_text(text, "C", T=T),
              3: extract_feature_data_from_text(text, "O", T=T),
              4: extract_feature_data_from_text(text, "N", T=T),
              5: extract_feature_data_from_text(text, "F", T=T),
              6: extract_feature_data_from_text(text, "Na", T=T),
              7: extract_feature_data_from_text(text, "Cl", T=T),
              8: extract_feature_data_from_text(text, "Y", T=T),
              9: extract_feature_data_from_text(text, "Yb", T=T),
              10: extract_feature_data_from_text(text, "Tm", T=T),
              11: extract_feature_data_from_text(text, "Er", T=T),
              }

# parameters = {1:[T, 0.03,  0.50, 0,      0,      0, 0,          0 ,0,            450.0, 0.9572],
#               2:[T, 0,     0,    0.1852, 3.1589, 0.096, 2.18,   0.3474, 3.3545,  773.49, 1.59],
#               3:[T, 0,     0,    0.096,  2.18,   0.05, 1.2,     0.1118, 1.875,   0,0],
#               4:[T, 0,     0,    0.3474, 3.3545, 0.1118, 1.875, 0.25, 3.55,      0, 0]}
#
# parameters = {1:[T, 1.9853832, 4.48, 0.09552, 3.74],
#               2:[T, 0.09552, 3.74, 0.5955672, 3.0],
#               }

# parameters = {1:[T, 0.8930,1.0000, 1.0080, 1.3550, 0.0930, 0.8203, -0.1000, 1.0000,
#                  8.2230, 33.2894, 1.0000, 0.0000, 121.1250, 3.7248, 9.6093, 1.0000,
#                  -0.1000, 0.0000, 55.1878, 3.0408, 2.4197, 0.0003, 1.0698, 0.0000,
#                  -19.4571, 4.2733, 1.0338, 1.0000, 2.8793, 0.0000, 0.0000, 0.0000],
#               2:[T,1.2450, 2.0000, 15.9990, 2.3890, 0.1000, 1.0898, 1.0548, 6.0000,
#                  9.7300, 13.8449, 4.0000, 37.5000, 116.0768, 8.5000, 8.3122, 2.0000,
#                  0.9049, 0.4056, 68.0152, 3.5027, 0.7640, 0.0021, 0.9745, 0.0000,
#                  -3.5500, 2.9000, 1.0493, 4.0000, 2.9225, 0.0000, 0.0000, 0.0000,],
#               3:[T,1.8315, 2.0000, 24.3050, 2.2464, 0.1806, 0.5020, 1.0000, 2.0000,
#                  10.9186, 27.1205, 3.0000, 38.0000, 0.0000, 0.9499, 5.6130, 0.0000,
#                  -1.3000 ,0.0000 ,220.0000, 49.9248 ,0.3370 ,0.0000, 0.0000, 0.0000,
#                  -1.0823, 2.3663, 1.0564, 6.0000, 2.9663, 0.0000, 0.0000, 0.0000],
#               4:[T,1.2333, 3.0000, 14.0000, 2.1263, 0.1207, 1.0000, 1.1748, 5.0000,
#                  9.9865, 13.2428, 4.0000, 26.4087, 100.0000, 6.3619, 6.9188, 2.0000,
#                  1.0433, 3.9512, 119.9837, 0.7170, 7.4321, 2.3377, 0.9745, 0.0000,
#                  -3.5800, 4.0000, 1.0183, 4.0000, 2.8793, 0.0000, 0.0000, 0.0000,],
#               }
# 1H2O3Mg4N
# T = 400K
'''
1.8315 2.0000 24.3050 2.2464 0.1806 0.5020 1.0000 2.0000
 10.9186 27.1205 3.0000 38.0000 0.0000 0.9499 5.6130 0.0000
 -1.3000 0.0000 220.0000 49.9248 0.3370 0.0000 0.0000 0.0000
 -1.0823 2.3663 1.0564 6.0000 2.9663 0.0000 0.0000 0.0000
'''

num_nearest_atoms = 10
device = 'cuda:2'
sep = 0.7
batch_size = 1
learning_rate = 1e-4
epochs = 100
print_interval = 5
last_frame = 100
interval_frame = 1
filename = 'FB_reax'
path = f"../dataset/{filename}.lammpstrj"
# path = f"../dataset/{filename}/dump.reax.mixture"
ratio = True # whether the system is represented by ratio