import torch

import torch.nn as nn
import torch.nn.functional as F
import torch.utils
import torch.distributions
import torchvision
import numpy as np
import torch.utils.data as Data
from utils import *
import pickle


# the AFA model for Molecular Dynamics slide prediction
# 切片预测
# input: a given slides
# output: the displacement of each atom
# notice that here we only focus on the target atom, ignoring any other infection
# here we use a CuSO4 system as an example
# the water system are treating as a whole, while the atom Cu and SO4 are selected as input
# The input contains two things: the force field parameters of Cu and SO4
# and "environment displacement" from water.

class AFA_MD(nn.Module):
    def __init__(self):
        super(AFA_MD, self).__init__()

    def find_environment(self, input_system):
        return environment_vector

    def find_target_atoms(self, input_syste):
        return target_atoms

    def get_displacement(self, target_atoms):
        return displacement_target_atoms

    def forward(self, input_system):
        environment_vector = self.find_environment(input_system)
        target_atoms = self.find_target_atoms(input_system)
        # select the environment and the target atoms
        displacement_target_atoms = self.get_displacement(target_atoms)
        # calculate the displacement of the target atoms
        atom_displacement = self.cal_atom_displacement(displacement_target_atoms, environment_vector)
        return atom_displacement

AFA_MD(input_system)
# GER -> FF -> environment modification
# here the hydrogen bond information is included.
# one model for the environment atoms, and one model for the target atoms.
# parameters -> displacement