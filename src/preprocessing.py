# this file is to conduct the preprocessing of lammps trajectory files.
import torch
import numpy as np
from utils import *
import pickle
from D4R_vae import *

def preprocess_vae():
    # filename = 'dissolve_0810'
    filename = 'CuSO4_1'
    path = f"../dataset/{filename}.lammpstrj"

    output_file = open(f"../dataset/{filename}_type.pickle", 'wb')
    types = read_lammps_file_atom_type(path)
    pickle.dump(types, output_file)

    print("loading dataset......")
    traj_file_list = [f"../dataset/CuSO4_1.lammpstrj",
                      f"../dataset/CuSO4_2.lammpstrj",
                      f"../dataset/CuSO4_3.lammpstrj",
                      f"../dataset/CuSO4_4.lammpstrj",
                      f"../dataset/CuSO4_5.lammpstrj",
                      ]
    data = read_lammps_file_serials(traj_file_list)
    print("finished loading")
    output_file = open(f"../dataset/{filename}_coords.pickle", 'wb')
    pickle.dump(data, output_file)


def preprocess_serial():
    device = 'cuda:1' if torch.cuda.is_available() else 'cpu'
    filename = 'dissolve_0810'
    vae_name = "dissolve_0810"

    VAE = torch.load(f"../output/vae_{vae_name}.pt", map_location=device)
    data = pickle.load(open(f"../dataset/{filename}_coords.pickle",'rb'))
    data = torch.tensor(data, dtype=torch.float).to(device)
    data = VAE.encoder(data)
    training_inputs, training_targets = prepare_dataset(data.detach(), min_lookback=10, max_lookback=10)

    output_file = open(f"../dataset/{filename}_vae_{vae_name}.pickle", 'wb')
    pickle.dump([training_inputs, training_targets], output_file)


if __name__ == "__main__":
    preprocess_vae()
    # preprocess_serial()
