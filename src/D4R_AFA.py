from D4R_vae import *
from utils import *
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