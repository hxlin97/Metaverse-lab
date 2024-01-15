# time-dependent serial prediction
import torch
import pickle
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

# 1 H 2O 3Cu 4S
parameters = config.parameters
T = config.T
num_nearest_atoms = config.num_nearest_atoms
device = config.device
sep = config.sep
batch_size = config.batch_size
learning_rate = config.learning_rate
epochs = config.epochs
print_interval = config.print_interval
# set up the required parameters

feature_inputs = torch.load(f'../temp_data/{config.filename}/feature_inputs.pt').to(device)
targets = torch.load(f'../temp_data/{config.filename}/targets.pt').to(device)
atom_coords = torch.load(f'../temp_data/{config.filename}/atom_coords.pt').to(device)
atom_types = torch.load(f'../temp_data/{config.filename}/atom_types.pt').to(device)
box_list = torch.load(f'../temp_data/{config.filename}/box_list.pt')
I, J, K = IJK_from_box_list(box_list)
# training_data = D4R_serial_Dataset(training_inputs=feature_inputs[:sep], training_targets=targets[:sep])
sep = int(len(feature_inputs) * sep)
print(f"number of trainings:{sep}, number of test:{len(feature_inputs)-sep}")
training_data = D4R_serial_Dataset_coords(training_inputs=feature_inputs[:sep], atom_coords=atom_coords[:sep],
                                          atom_types=atom_types[:sep], training_targets=targets[:sep])
training_dataloader = Data.DataLoader(dataset=training_data, batch_size=batch_size, shuffle=True)
test_data = D4R_serial_Dataset_coords(training_inputs=feature_inputs[sep:], atom_coords=atom_coords[sep:],
                               atom_types=atom_types[sep:], training_targets=targets[sep:])
test_dataloader = Data.DataLoader(dataset=test_data, batch_size=batch_size, shuffle=True)
num_features = feature_inputs[0].shape[-1]
model = serial_model(num_features, num_nearest_atoms).to(device)
print(f'number of parameters: {sum([p.numel() for p in model.parameters()])}')
opt = torch.optim.Adam(model.parameters(), lr=learning_rate)
for epoch in range(epochs):
    for x_batch, y_batch, coords_batch, types_batch, in training_dataloader:
        model.train()
        y_batch = y_batch.to(device)
        y_predict = model(x_batch.to(device), coords_batch)
        target_coords = coords_batch + y_batch
        predicted_coords = coords_batch + y_predict
        rdf1 = compute_rdf_by_unique_types(target_coords[0], atom_types, max_distance=10, num_bins=50, I=I, J=J, K=K)
        rdf2 = compute_rdf_by_unique_types(predicted_coords[0], atom_types, max_distance=10, num_bins=50, I=I, J=J, K=K)
        train_loss = sum([torch.abs(r1 - r2).mean() for r1, r2 in zip(rdf1.values(), rdf2.values())])
        # train_loss = (torch.abs(y_predict - y_batch) ).mean()
        # change the error to the radial distribution functions
        # map y_predict and y_batch into the radical distributions?

        # the average displacement error
        opt.zero_grad()
        train_loss.backward()
        opt.step()

    if epoch % print_interval == 0:
        for x_batch, y_batch, coords_batch, types_batch, in training_dataloader:
            model.eval()
            y_batch = y_batch.to(device)
            y_predict = model(x_batch.to(device), coords_batch)
            target_coords = coords_batch + y_batch
            predicted_coords = coords_batch + y_predict
            rdf1 = compute_rdf_by_unique_types(target_coords[0], atom_types, max_distance=10, num_bins=50, I=I, J=J,
                                               K=K)
            rdf2 = compute_rdf_by_unique_types(predicted_coords[0], atom_types, max_distance=10, num_bins=50, I=I, J=J,
                                               K=K)
            test_loss = sum([torch.abs(r1 - r2).mean() for r1, r2 in zip(rdf1.values(), rdf2.values())])
        print(epoch, train_loss.cpu().detach().numpy(), test_loss.cpu().detach().numpy())
        # print(epoch, train_loss.cpu().detach().numpy(), test_loss.cpu().detach().numpy())
torch.save(model, f'../pretrained_model/serial_model_{config.filename}.pth')

