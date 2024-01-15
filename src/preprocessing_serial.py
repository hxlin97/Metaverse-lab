# time-dependent serial prediction
import torch
import pickle
import os
import torch.nn as nn
import torch.nn.functional as F
import torch.utils
import torch.distributions
import torchvision
import numpy as np
import torch.utils.data as Data
import matplotlib.pyplot as plt
from D4R_vae import *
from D4R_serial import *
from utils import *
import config
file = open("../dataset/FB_reax/forcefield.reax")
text = file.readlines()
extracted_info = extract_feature_data_from_text(text, 'C')
parameters = config.parameters
T = config.T
num_nearest_atoms = config.num_nearest_atoms
device = config.device
sep = config.sep
batch_size = config.batch_size
last_frame = config.last_frame
interval_frame = config.interval_frame
path = config.path
ratio = config.ratio

# 记得要排序！！！
# sort_and_process_file(f"../dataset/CuCl2/dump.reax.cucl2", '../dataset/CuCl2.lammpstrj')
# sort_and_process_file('../dataset/FB_reax/dump.reax.mixture', '../datasset/FB_reax.lammpstrj')
# 一定记得要先运行这个程序
atom_coords, box_list = read_lammps_file(path, last_frame=last_frame, interval_frame=interval_frame,
                                         ratio=ratio, return_box_list=True)
I, J, K = IJK_from_box_list(box_list)
atom_coords = torch.tensor(atom_coords, dtype=torch.float).to(device)

atom_types = read_lammps_file_atom_type(path)
atom_types = torch.tensor(atom_types, dtype=torch.int).to(device)
# rdf_dict = compute_rdf_by_unique_types(atom_coords[0], atom_types, max_distance=10, num_bins=50, I=I, J=J, K=K)
# feature_inputs, targets = prepare_dataset_serial_periodic(atom_coords, parameters, atom_types, box_list, num_nearest_atoms)
feature_inputs, targets = prepare_dataset_serial_periodic_with_coords(atom_coords, parameters, atom_types, box_list, num_nearest_atoms)
# predict the coords, velocities, etc.
if not os.path.exists(f'../temp_data/{config.filename}'):
    os.mkdir(f'../temp_data/{config.filename}')
torch.save(feature_inputs, f'../temp_data/{config.filename}/feature_inputs.pt')
torch.save(targets, f'../temp_data/{config.filename}/targets.pt')
torch.save(atom_coords, f'../temp_data/{config.filename}/atom_coords.pt')
torch.save(atom_types, f'../temp_data/{config.filename}/atom_types.pt')
torch.save(box_list, f'../temp_data/{config.filename}/box_list.pt')