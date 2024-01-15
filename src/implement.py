import torch
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


def atom_position2latent_space(atom_positions, VAE_model):
    latent_value = VAE_model.encoder(atom_positions.unsqueeze(0))
    # originally I use the batch processing, but here the encoding only takes for one
    return latent_value


def latent_space2atom_position(latent_value, VAE_model):
    atom_positions = VAE_model.decoder(latent_value.unsqueeze(0))
    # originally I use the batch processing, but here the decoding only takes for one
    return atom_positions


def criteria(serial, reference_frames):
    return 1


# 1. load the model and related parameters
num_slides = 100
FF_parameters = load_FF_parameters()
device = 'cuda:1' if torch.cuda.is_available() else 'cpu'
D4R_VAE = torch.load("../output/vae.pt", map_location=device)
D4R_serial = torch.load("../output/D4R_serial_epochs1000.pt", map_location=device)
path = "../dataset/cool.lammpstrj"
data = read_lammps_file(path)
data = torch.tensor(data, dtype=torch.float).to(device)
initial_slide = atom_position2latent_space(data[0], D4R_VAE)
final_slide = atom_position2latent_space(data[-1], D4R_VAE)
# 2. load the initial state and the final state, here we set the initial and final state as the reference slides
reference_slides = [initial_slide, final_slide]
# 3. training to obtain the intermedia states
# use D4R_serial to iteratively predict the following frame, and then compare the final frame with the target
all_slides = [initial_slide]
for i in range(num_slides):
    D4R_serial.eval()
    new_slides = D4R_serial(all_slides)
    all_slides.append(new_slides)

loss = criteria(all_slides, reference_slides)
# 4. select the intermedia states and then change it
select_frame = 10

# 5. re-training to obtain the intermedia states

# 6. store the corresponding data
