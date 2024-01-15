import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils
import torch.distributions
import torchvision
import numpy as np
import torch.utils.data as Data
import matplotlib.pyplot as plt
import os
from D4R_vae import *
from utils import *


class D4R_serial(nn.Module):
    def __init__(self, latent_dims=1000, hidden_size=50, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(latent_dims, hidden_size, num_layers)
        self.label = nn.Linear(hidden_size, latent_dims)

    def forward(self, input_serial):
        # perhaps the hidden variable need to be a input?
        out, _ = self.lstm(input_serial)
        out = self.label(out)
        return out

class serial_model(nn.Module):
    def __init__(self, num_features, num_nearest_atoms):
        super().__init__()
        self.num_nearest_atoms = num_nearest_atoms
        latent = 10
        self.parameter_process = nn.Sequential(nn.Linear(num_features, 1280),
                                               nn.Tanh(),
                                               nn.Linear(1280, 256),
                                               nn.Tanh(),
                                               nn.Linear(256, latent))
        self.coords_embedding = nn.Sequential(nn.Linear(3, 128),
                                              nn.Tanh(),
                                              nn.Linear(128, 210),
                                              )
        self.displacement_prediction = nn.Sequential(nn.Linear(latent*(num_nearest_atoms+1), 1280),
                                                     nn.Linear(1280,256),
                                                     nn.Linear(256,3))
    def forward(self, feature_inputs, coords_batch):
        # output the displacement
        # TODO: try to think about how to insert the coords?
        current_shape = feature_inputs.shape
        x = feature_inputs.reshape(-1, current_shape[2], current_shape[3])
        x = self.parameter_process(x)
        # num_atoms = coords_batch.shape[1]
        # y = coords_batch.reshape(-1, num_atoms, 3)
        # y = self.coords_embedding(y)
        x = x.view(x.size(0), -1)
        # y = y.view(y.size(0), -1) # think carefully how it can be encoded?
        x = self.displacement_prediction(x)
        return x.reshape(current_shape[0], current_shape[1], 3)
        # merge the first two dimension, batch * number of atoms


# estimate the target
if __name__ == "__main__":
    # os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
    device = 'cuda:1' if torch.cuda.is_available() else 'cpu'
    # num_atoms = 2208
    num_atoms = 4928
    latent_dims = 1000
    learning_rate = 1e-4
    epochs = 1000
    batch_size = 4
    filename = 'dissolve_0810'
    # path = "../dataset/cool.lammpstrj"
    # path = "../dataset/NaCl_solute.lammpstrj"
    path = f"../dataset/{filename}_coords.pickle"
    # VAE = torch.load("../output/vae_2208test.pt", map_location=device)
    VAE = torch.load(f"../output/vae_{filename}.pt", map_location=device)

    with open(path) as file:
        data = pickle.load(file)
        data = torch.tensor(data).to(device)
    data = VAE.encoder(data)
    training_inputs, training_targets = prepare_dataset(data.detach(), lookback=10)
    # test_inputs, test_targets = prepare_dataset(encoded_data[division:])
    sep = -3
    training_data = D4R_serial_Dataset(training_inputs=training_inputs[:sep],
                                       training_targets=training_targets[:sep])
    training_dataloader = Data.DataLoader(dataset=training_data, batch_size=batch_size, shuffle=True)
    test_data = D4R_serial_Dataset(training_inputs=training_inputs[sep:],
                                   training_targets=training_targets[sep:])
    test_dataloader = Data.DataLoader(dataset=test_data, batch_size=batch_size, shuffle=True)
    import wandb

    wandb.init(project="D4R",
               name="D4R_serial",
               config={"learning_rate": learning_rate,
                       "epochs": epochs,
                       "num_atoms": num_atoms})

    model = D4R_serial(latent_dims=latent_dims, hidden_size=5000).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=learning_rate)
    # here the optimizer only acting on the D4R serial model, without any effect on VAE model
    loss_fn = nn.MSELoss()
    for epoch in range(epochs):
        for x_batch, y_batch in training_dataloader:
            model.train()
            y_batch = y_batch.to(device)
            y_predict = model(x_batch.to(device))
            loss = ((y_predict - y_batch) ** 2).sum()
            # loss = ((VAE.decoder(y_predict) - VAE.decoder(y_batch))**2).sum()
            # 感觉不应该采用如此simple的损失函数，不过也能接受吧。可能不是在latent space上进行误差运算，估计是添加到system上
            opt.zero_grad()
            loss.backward()
            opt.step()
            # 测试一下预测结果？
        wandb.log({"training_loss": loss})
        if epoch % 100 == 0:
            print(epoch, loss)
        for x_batch, y_batch in test_dataloader:
            model.eval()
            y_batch = y_batch.to(device)
            y_predict = model(x_batch.to(device))
            loss = ((y_predict - y_batch) ** 2).sum()
        wandb.log({"test_loss": loss})
    torch.save(model, f"../output/D4R_serial_fill_cool.pt")
