import torch

import torch.nn as nn
import torch.nn.functional as F
import torch.utils
import torch.distributions
import torchvision
import numpy as np
import torch.utils.data as Data
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 200
from utils import *
import pickle


class VariationalEncoder(nn.Module):
    def __init__(self, latent_dims, pad_num_atoms, device):
        super(VariationalEncoder, self).__init__()
        self.device = device
        self.pad_num_atoms = pad_num_atoms
        self.linear1 = nn.Sequential(
            nn.Linear(self.pad_num_atoms * 3, 5120),
            nn.Tanh(),
            nn.Linear(5120, 2560),
            nn.Tanh(),
            nn.Linear(2560, 1280),
            nn.Tanh(),
        )
        self.linear2 = nn.Linear(1280, latent_dims)
        self.linear3 = nn.Linear(1280, latent_dims)

        self.N = torch.distributions.Normal(0, 1e-2)
        self.N.loc = self.N.loc  # hack to get sampling on the GPU
        self.N.scale = self.N.scale
        self.kl = 0


    def forward(self, x, training=True):
        x = torch.flatten(x, start_dim=1)
        x = self.linear1(x)
        mu = self.linear2(x)
        sigma = torch.exp(self.linear3(x))
        #         sigma = self.linear3(x)
        if training:
            z = mu + sigma * self.N.sample(mu.shape).to(self.device)
            # I do not know why I have to add "to(device)" here
        else:
            z = mu
        self.kl = (sigma ** 2 + mu ** 2 - torch.log(sigma) - 1 / 2).sum()
        return z


class Decoder(nn.Module):
    def __init__(self, latent_dims, pad_num_atoms, device):
        super(Decoder, self).__init__()
        self.pad_num_atoms = pad_num_atoms
        self.linear1 = nn.Sequential(
            nn.Linear(latent_dims, 1280),
            nn.Tanh(),
            nn.Linear(1280, 2560),
            nn.Tanh(),
            nn.Linear(2560, 5120),
            nn.Tanh(),
        )
        self.linear3 = nn.Linear(5120, self.pad_num_atoms * 3)
        self.device = device

    def forward(self, z):
        z = self.linear1(z)
        z = self.linear3(z)
        # last step have no activation function
        return z.reshape((-1, self.pad_num_atoms, 3))


class VariationalAutoencoder(nn.Module):
    def __init__(self, latent_dims, pad_num_atoms, device):
        super(VariationalAutoencoder, self).__init__()
        self.device = device
        self.pad_num_atoms = pad_num_atoms
        self.encoder = VariationalEncoder(latent_dims, self.pad_num_atoms, device=self.device)
        self.decoder = Decoder(latent_dims, self.pad_num_atoms, device=self.device)

    def forward(self, x, training=True):
        z = self.encoder(x, training)
        return self.decoder(z)


if __name__ == "__main__":
    # filename = 'dissolve_0810'
    filename = 'CuSO4_1'
    path = f"../dataset/{filename}_coords.pickle"
    # load the dataset to be learnt
    device = 'cuda:3' if torch.cuda.is_available() else 'cpu'
    latent_dims = 1000
    learning_rate = 1e-5
    batch_size = 32
    pad_num_atoms = 6000
    epochs = 10000
    print("loading dataset......")
    # data = read_lammps_file(path)
    file = open(path, 'rb')
    data = pickle.load(file)
    print("finished loading")
    num_atoms = data.shape[1]
    data = torch.tensor(data, dtype=torch.float)
    padder = nn.ZeroPad2d(padding=(0, 0, 0, pad_num_atoms - num_atoms))
    data = padder(data)
    # add a way to padding so that these systems are matching one given input shape
    split_num = int(0.8 * len(data))
    data, test_data = Data.random_split(data, lengths=[split_num, len(data) - split_num])
    # here all atoms are selected, or one may use other criteria to select atoms
    data = Data.DataLoader(dataset=data, batch_size=batch_size, shuffle=True)
    test_data = Data.DataLoader(dataset=test_data, batch_size=batch_size, shuffle=True)
    # try to split the entire dataset into a training part and a test part. How does it work in unknown system?
    import wandb

    wandb.init(project="D4R",
               name="D4R_vae",
               config={"learning_rate": learning_rate,
                       "latent_dims": latent_dims,
                       "epochs": epochs,
                       "batch_size": batch_size,
                       "num_atoms": num_atoms,
                       "pad_num_atoms": pad_num_atoms,
                       "dataset": filename},
               )
    vae = VariationalAutoencoder(latent_dims, pad_num_atoms, device=device).to(device)  # GPU
    opt = torch.optim.Adam(vae.parameters(), lr=learning_rate)
    # the training process
    for epoch in range(epochs):
        for x in data:
            x = x.to(device)
            opt.zero_grad()
            x_hat = vae(x)
            MAE_loss = ((x - x_hat) ** 2).sum()
            kl_loss = vae.encoder.kl
            loss = MAE_loss + kl_loss
            loss.backward()
            opt.step()
        wandb.log({"train_loss": loss,
                   "MAE_per_atom": ((x - x_hat) ** 2).mean(),
                   "KL_loss": kl_loss})
        # print(loss, MAE_loss, kl_loss)
        if epoch % 100 == 0:
            for x in test_data:
                x = x.to(device)
                x_hat = vae(x, training=False)
                MAE_loss = ((x - x_hat) ** 2).sum()
                kl_loss = vae.encoder.kl
                loss = MAE_loss + kl_loss
            wandb.log({"test_loss": loss,
                       "test_MAE_per_atom": ((x - x_hat) ** 2).mean(),
                       "test_KL_loss": kl_loss})
            print(epoch, loss.cpu().detach().numpy(), MAE_loss.cpu().detach().numpy(), kl_loss.cpu().detach().numpy())

    torch.save(vae, f"../output/vae_new_{filename}.pt")
