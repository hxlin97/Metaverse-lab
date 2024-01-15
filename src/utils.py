import torch;

torch.manual_seed(0)
import torch.nn as nn
import torch.nn.functional as F
import torch.utils
import torch.distributions
import torchvision
import numpy as np
import torch.utils.data as Data
import matplotlib.pyplot as plt
import sys


def read_lammps_file_serials(traj_file_list, last_frame=None, interval_frame=1):
    # input is a serials of trajectory files
    def convey_to_xyz(ratio_list, box_list):
        x_range, y_range, z_range = box_list
        ratio_x, ratio_y, ratio_z = [np.round(float(i), 3) for i in ratio_list]
        assert ratio_x >= -0.1 and ratio_y >= -0.1 and ratio_z >= -0.1, f"{ratio_x},{ratio_y},{ratio_z} "
        x_left, x_right = [float(i) for i in x_range]
        x_scaled = x_left + (x_right - x_left) * ratio_x
        y_left, y_right = [float(i) for i in y_range]
        y_scaled = y_left + (y_right - y_left) * ratio_y
        z_left, z_right = [float(i) for i in z_range]
        z_scaled = z_left + (z_right - z_left) * ratio_z
        return [x_scaled, y_scaled, z_scaled]

    with open(traj_file_list[0]) as f:
        # load the number of atoms
        all_data = f.read().split('ITEM: TIMESTEP')[1]
        all_data = all_data.split('\n')
        natoms = int(all_data[3])

    coords = []
    for filename in traj_file_list:
        with open(filename) as f:
            # Read the number of atoms and number of timesteps from the header
            all_data = f.read().split('ITEM: TIMESTEP')
            times = []

            if last_frame:
                all_data = all_data[1:last_frame]
            else:
                all_data = all_data[1:]
            for nsteps, slide in enumerate(all_data[::interval_frame]):
                # if nsteps > 1000:
                #     break
                one_slide_coords = np.zeros((natoms, 3))
                print(f"\rReading: current step:{nsteps}/{len(all_data) // interval_frame}", end="")
                one_slide_data = slide.split('\n')
                natoms = int(one_slide_data[3])
                box_list = []
                for box_info in one_slide_data[5:8]:
                    left, right = box_info.split()
                    box_list.append([float(left), float(right)])
                for line in one_slide_data[9:-1]:
                    'ITEM: ATOMS id type xs ys zs'
                    atom_id, atom_type, xs, ys, zs = line.split()
                    atom_id = int(atom_id) - 1
                    x_scaled, y_scaled, z_scaled = (convey_to_xyz([xs, ys, zs], box_list))
                    one_slide_coords[atom_id][0] = x_scaled
                    one_slide_coords[atom_id][1] = y_scaled
                    one_slide_coords[atom_id][2] = z_scaled
                    # only xs ys zs are recorded, the term atoms and id always inherit
                coords.append(one_slide_coords)
    coords = np.asarray(coords)
    return coords


# prepare the data
def read_lammps_file(traj_file, last_frame=None, interval_frame=1, ratio=True, return_box_list=False):
    # this method have some difficulties, no more than 1000 frames can be loaded.
    def convey_to_xyz(ratio_list, box_list):
        x_range, y_range, z_range = box_list
        ratio_x, ratio_y, ratio_z = [np.round(float(i), 3) for i in ratio_list]
        assert ratio_x >= -0.1 and ratio_y >= -0.1 and ratio_z >= -0.1, f"{ratio_x},{ratio_y},{ratio_z} "
        x_left, x_right = [float(i) for i in x_range]
        x_scaled = x_left + (x_right - x_left) * ratio_x
        y_left, y_right = [float(i) for i in y_range]
        y_scaled = y_left + (y_right - y_left) * ratio_y
        z_left, z_right = [float(i) for i in z_range]
        z_scaled = z_left + (z_right - z_left) * ratio_z
        return [x_scaled, y_scaled, z_scaled]

    # Specify the path to the LAMMPS trajectory file
    #     traj_file = 'data/test_1.lammpstrj'
    # Open the trajectory file
    with open(traj_file) as f:
        # Read the number of atoms and number of timesteps from the header
        all_data = f.read().split('ITEM: TIMESTEP')
        times = []
        coords = []
        if last_frame:
            all_data = all_data[1:last_frame]
        else:
            all_data = all_data[1:]
        for nsteps, slide in enumerate(all_data[::interval_frame]):
            # if nsteps > 1000:
            #     break
            print(f"\rReading: current step:{nsteps}/{len(all_data) // interval_frame}", end="")
            one_slide_data = slide.split('\n')
            natoms = int(one_slide_data[3])
            one_slide_coords = []
            box_list = []
            for box_info in one_slide_data[5:8]:
                left, right = box_info.split()
                box_list.append([float(left), float(right)])
            for line in one_slide_data[9:-1]:
                'ITEM: ATOMS id type xs ys zs'
                atom_id, atom_type, xs, ys, zs = line.split()[:5]
                if ratio:
                    one_slide_coords.append(convey_to_xyz([xs, ys, zs], box_list))
                else:
                    one_slide_coords.append([float(i) for i in [xs, ys, zs]])
                # only xs ys zs are recorded, the term atoms and id always inherit
            if len(one_slide_coords) != natoms:
                print(f"slide {nsteps} failed")
                # now this slide is discarded
                continue
            coords.append(one_slide_coords)
    coords = np.asarray(coords)
    if return_box_list:
        return coords, box_list
    return coords


def read_lammps_file_atom_type(traj_file):
    with open(traj_file) as f:
        # load the number of atoms
        all_data = f.read().split('ITEM: TIMESTEP')[1]
        all_data = all_data.split('\n')
        natoms = int(all_data[3])

    with open(traj_file) as f:
        # Read the number of atoms and number of timesteps from the header
        atom_types = np.zeros(natoms)
        all_data = f.read().split('ITEM: TIMESTEP')[1]
        all_data = all_data.split('\n')
        for line in all_data[9:-1]:
            'ITEM: ATOMS id type xs ys zs'
            atom_id, atom_type, xs, ys, zs = line.split()[:5]
            atom_id = int(atom_id) - 1
            atom_type = int(atom_type)
            # only xs ys zs are recorded, the term atoms and id always inherit
            atom_types[atom_id] = atom_type
    atom_types = np.array(atom_types)
    return atom_types

# Given the provided content, I'll write a function to read and extract the data for a specified feature.

def extract_feature_data_from_text(text, feature, T=300):
    # Split the text into lines
    extracted_data = [T]
    feature_found = False
    # Iterate through each line
    for line in text:
        # Split each line into parts
        parts = line.split()
        # Iterate through the parts
        for part in parts:
            if feature_found:
                # If the part is a number, add it to the list, otherwise stop collecting
                if part.replace('.', '', 1).lstrip('-').isdigit():
                    extracted_data.append(float(part))
                else:
                    feature_found = False
                    break  # Break the inner loop, proceed to the next line
            if part == feature:
                # Mark that the feature is found, start collecting numbers from the next part
                feature_found = True
    return extracted_data


# separate into coord and type, only the coordinates can be changed.

def prepare_dataset(input_serial, min_lookback=10, max_lookback=30):
    # 实际上应该是只有第一帧和最后一帧作为输入，然后将所有的其余训练出来，训练的criteria可能需要进行一部分的修改
    # 再preprocessing 部分应该采用np来，而不是tensor.torch
    latent_dims = input_serial.shape[1]
    inputs, targets = [], []
    for lookback in range(min_lookback, max_lookback):
        for i in range(len(input_serial) - lookback):
            # from i to i+lookback
            input = torch.zeros(lookback, latent_dims, dtype=input_serial.dtype).to(input_serial.device)
            input[0] = input_serial[i].clone().detach()
            input[lookback - 1] = input_serial[lookback - 1]
            target = input_serial[i:i + lookback]  # open boundary for the right hand side
            inputs.append(input)
            targets.append(target)
    # input: several frames are exactly 0, while some frames are non-zero. These frames are used as reference
    # 这个训练数据集应该如何尝试？
    # target: all frames are given.
    return inputs, targets


class D4R_serial_Dataset(torch.utils.data.Dataset):
    def __init__(self, training_inputs, training_targets):
        self.training_inputs = training_inputs
        self.training_targets = training_targets

    def __len__(self):
        return len(self.training_inputs)

    def __getitem__(self, index):
        input_data = self.training_inputs[index]
        target_data = self.training_targets[index]
        return input_data, target_data

class D4R_serial_Dataset_coords(torch.utils.data.Dataset):
    def __init__(self, training_inputs, atom_coords, atom_types, training_targets):
        self.training_inputs = training_inputs
        self.training_targets = training_targets
        self.atom_coords = atom_coords
        self.atom_types = atom_types

    def __len__(self):
        return len(self.training_inputs)

    def __getitem__(self, index):
        input_data = self.training_inputs[index]
        target_data = self.training_targets[index]
        atom_coord = self.atom_coords[index]
        atom_type = self.atom_types[index]
        return input_data, target_data, atom_coord, atom_type

def atom_position2latent_space(atom_positions, VAE_model):
    latent_value = VAE_model.encoder(atom_positions.unsqueeze(0))
    # originally I use the batch processing, but here the encoding only takes for one
    return latent_value


def latent_space2atom_position(latent_value, VAE_model):
    atom_positions = VAE_model.decoder(latent_value.unsqueeze(0))
    # originally I use the batch processing, but here the decoding only takes for one
    return atom_positions

def sort_and_process_file(file_path, output_path):
    # example usage
    #sort_and_process_file('dump-8.reax.mgNO3', 'mgno3_8.lammpstrj')
    with open(file_path, 'r') as file, open(output_path, 'w') as output_file:
        current_section = []
        header_section = []
        processing_section = False
        line_count = 0

        for line in file:
            line_count += 1

            if "ITEM: ATOMS id type xs ys zs" in line:
                # 将 header_section 写入输出文件
                for header_line in header_section:
                    output_file.write(header_line)
                output_file.write(line)

                if current_section:
                    # 对当前片段进行排序并处理
                    process_section(current_section, output_file)
                    current_section = []
                processing_section = True
                header_section = []  # 清空 header_section 以备下次使用
            elif processing_section:
                if line.startswith("ITEM:"):
                    # 遇到新的片段开始，结束当前片段的处理
                    process_section(current_section, output_file)
                    current_section = []
                    processing_section = False
                    header_section.append(line)  # 开始收集新的 header_section
                else:
                    current_section.append(line)
            else:
                header_section.append(line)

            # 每读取一定数量的行，输出进度
            if line_count % 10000 == 0:
                print(f"Processed {line_count} lines.")

        # 确保最后一个片段也被处理
        if current_section:
            process_section(current_section, output_file)

def process_section(section, output_file):
    sorted_section = sorted(section, key=lambda x: int(x.split()[0]))
    for line in sorted_section:
        output_file.write(line)

def view_particular_slide(num_frame, serial, VAE_model):
    slide = serial[num_frame]
    atom_positions = latent_space2atom_position(slide, VAE_model)
    return atom_positions

def compute_rdf_by_unique_types(coordinates, types, max_distance, num_bins, I, J, K):
    """
    Compute the radial distribution function (RDF) for a set of points,
    separated by unique combinations of types.

    Args:
    - coordinates (torch.Tensor): A tensor of shape (n, 3) representing the coordinates of the points.
    - types (torch.Tensor): A tensor of shape (n,) representing the types of each point.
    - max_distance (float): The maximum distance to consider for the RDF.
    - num_bins (int): The number of bins to use in the RDF calculation.

    Returns:
    - dict: A dictionary where keys are tuples of types (in sorted order), and values are tensors representing the RDF.
    """
    unique_types = torch.unique(types)
    num_types = len(unique_types)
    n = coordinates.shape[0]
    # diff = coordinates.unsqueeze(1) - coordinates.unsqueeze(0)
    # dist = torch.sqrt(torch.sum(diff**2, dim=-1))
    unitcell_volumes = I*J*K # here we always assume orthogonal.
    dist = periodic_cdist_vectorized(coordinates, I, J, K)
    bins = torch.linspace(0, max_distance, steps=num_bins+1)
    rdf_dict = {}
    # here np.histc can not be used because it does not support backpropagation
    for i, type1 in enumerate(unique_types):
        for type2 in unique_types[i:]:
            rdf = torch.zeros(num_bins, requires_grad=True).to(coordinates.device)
            mask_type1 = types.unsqueeze(1) == type1
            mask_type2 = types.unsqueeze(0) == type2
            mask_type = mask_type1 & mask_type2

            for j in range(num_bins):
                mask_dist = (dist > bins[j]) & (dist <= bins[j+1])
                mask = mask_dist & mask_type
                rdf[j] = torch.sum(mask)
                shell_volume = 4 / 3 * torch.pi * (bins[j + 1] ** 3 - bins[j] ** 3)
                normalization_factor = shell_volume / unitcell_volumes * (1+num_types) * num_types/2
                # normalization_factor = torch.sum(mask_type) * (bins[1] - bins[0])
                rdf[j] /= normalization_factor

            rdf_dict[(type1.item(), type2.item())] = rdf/torch.sum(rdf)
            #这地方normalization设置的有问题，不知道啥情况
    # r = 0.5 * (edges[1:] + edges[:-1])
    return rdf_dict


def periodic_cdist_vectorized(points, I, J, K):
    points_expanded = points.unsqueeze(1)
    delta = points_expanded - points_expanded.transpose(0, 1)
    delta[..., 0] -= I * torch.round(delta[..., 0] / I)
    delta[..., 1] -= J * torch.round(delta[..., 1] / J)
    delta[..., 2] -= K * torch.round(delta[..., 2] / K)
    distances = torch.norm(delta, dim=2)
    return distances


def find_nearest_atoms_torch_periodic(coordinates, I, J, K, num_nearest_atoms: int = 8):
    """
    Finds the 8 nearest atoms for each atom in the given set of coordinates using PyTorch.

    Parameters:
    coordinates (torch.Tensor): An n x 3 matrix representing the coordinates of n atoms.

    Returns:
    torch.Tensor: An n x 8 matrix representing the indices of the 8 nearest atoms for each atom.
    """
    # Calculate the pairwise distance matrix
    dist_matrix = periodic_cdist_vectorized(coordinates, I, J, K)
    assert num_nearest_atoms > 2, 'min number of nearest atoms must be larger than 8'
    # For each atom, find the indices of the 8 nearest atoms
    # We use topk and take indices 1 to 9 (excluding the first one, which is the atom itself)
    _, nearest_indices = torch.topk(dist_matrix, num_nearest_atoms + 1, largest=False)
    nearest_indices = nearest_indices[:, :]  # Exclude the atom itself (which is always the closest)

    return nearest_indices


def find_nearest_atoms_torch(coordinates, num_nearest_atoms: int = 8):
    """
    Finds the 8 nearest atoms for each atom in the given set of coordinates using PyTorch.

    Parameters:
    coordinates (torch.Tensor): An n x 3 matrix representing the coordinates of n atoms.

    Returns:
    torch.Tensor: An n x 8 matrix representing the indices of the 8 nearest atoms for each atom.
    """
    # Calculate the pairwise distance matrix
    dist_matrix = torch.cdist(coordinates, coordinates, p=2)
    assert num_nearest_atoms > 2, 'min number of nearest atoms must be larger than 8'
    # For each atom, find the indices of the 8 nearest atoms
    # We use topk and take indices 1 to 9 (excluding the first one, which is the atom itself)
    _, nearest_indices = torch.topk(dist_matrix, num_nearest_atoms + 1, largest=False)
    nearest_indices = nearest_indices[:, :]  # Exclude the atom itself (which is always the closest)

    return nearest_indices


def prepare_dataset_serial(atom_coords, parameters, atom_types, num_nearest_atoms: int = 8):
    num_features = 3 + len(parameters[1])  # 1 must be in the key of parameters.
    targets = (atom_coords[1:] - atom_coords[:-1])  # output the displacements
    num_atoms = atom_coords.shape[1]
    feature_inputs = []
    nsteps = 0
    for one_frame_coords in atom_coords[:-1]:
        nsteps += 1
        print(f"\rcalculating: current step:{nsteps}/{len(atom_coords)}", end="")
        feature_input = preprocess_one_frame(one_frame_coords, num_nearest_atoms, num_atoms, num_features, atom_types,
                                             parameters)

        feature_inputs.append(feature_input)
    return torch.stack(feature_inputs), targets

def IJK_from_box_list(box_list):
    I = box_list[0][1] - box_list[0][0]
    J = box_list[1][1] - box_list[1][0]
    K = box_list[2][1] - box_list[2][0]
    return I,J, K

def prepare_dataset_serial_periodic(atom_coords, parameters, atom_types, box_list, num_nearest_atoms: int = 8):
    num_features = 3 + len(parameters[1])  # 1 must be in the key of parameters.
    I, J, K = IJK_from_box_list(box_list)
    targets = periodic_distance(atom_coords[1:], atom_coords[:-1], I, J, K)  # output the displacements
    num_atoms = atom_coords.shape[1]
    feature_inputs = []
    nsteps = 0
    for one_frame_coords in atom_coords[:-1]:
        nsteps += 1
        print(f"\rcalculating: current step:{nsteps}/{len(atom_coords)}", end="")
        feature_input = preprocess_one_frame_periodic(one_frame_coords, num_nearest_atoms, num_atoms, num_features,
                                                      atom_types,
                                                      parameters, I, J, K)

        feature_inputs.append(feature_input)
    return torch.stack(feature_inputs), targets

def prepare_dataset_serial_periodic_with_coords(atom_coords, parameters, atom_types, box_list, num_nearest_atoms: int = 8):
    num_features = 3 + len(parameters[1])  # 1 must be in the key of parameters.
    I, J, K = IJK_from_box_list(box_list)
    targets = periodic_distance(atom_coords[1:], atom_coords[:-1], I, J, K)  # output the displacements
    num_atoms = atom_coords.shape[1]
    feature_inputs = []
    nsteps = 0
    for one_frame_coords in atom_coords[:-1]:
        nsteps += 1
        print(f"\rcalculating: current step:{nsteps}/{len(atom_coords)}", end="")
        feature_input = preprocess_one_frame_periodic_with_coords(one_frame_coords, num_nearest_atoms, num_atoms, num_features,
                                                      atom_types,
                                                      parameters, I, J, K)

        feature_inputs.append(feature_input)
    return torch.stack(feature_inputs), targets
    # return feature_input, targets

def preprocess_one_frame_periodic(one_frame_coords, num_nearest_atoms, num_atoms, num_features, atom_types, parameters,
                                  I, J, K):
    nearest_atoms_indices_torch = find_nearest_atoms_torch_periodic(one_frame_coords,
                                                                    I=I,
                                                                    J=J,
                                                                    K=K, num_nearest_atoms = num_nearest_atoms)

    def cal_dist(i):
        nearest_index = nearest_atoms_indices_torch[i]
        # first_parameter: the distance between each
        distance = periodic_distance(one_frame_coords[nearest_index], one_frame_coords[i], I, J, K)
        return distance

    def read_params(i):
        nearest_index = nearest_atoms_indices_torch[i]
        types = atom_types[nearest_index]
        temp = list(map(lambda x: parameters[int(x)], types))
        return torch.tensor(temp)

    feature_input = torch.zeros(num_atoms, num_nearest_atoms + 1, num_features)
    feature_input[:, :, :3] = torch.stack(list(map(lambda x: cal_dist(x), range(num_atoms))))
    # making mapping for each element
    feature_input[:, :, 3:] = torch.stack(list(map(lambda x: read_params(x), range(num_atoms))))
    return feature_input

def preprocess_one_frame_periodic_with_coords(one_frame_coords, num_nearest_atoms, num_atoms, num_features, atom_types, parameters,
                                  I, J, K):
    nearest_atoms_indices_torch = find_nearest_atoms_torch_periodic(one_frame_coords,
                                                                    I=I,
                                                                    J=J,
                                                                    K=K, num_nearest_atoms = num_nearest_atoms)

    def cal_dist(i):
        nearest_index = nearest_atoms_indices_torch[i]
        # first_parameter: the distance between each
        distance = periodic_distance(one_frame_coords[nearest_index], one_frame_coords[i], I, J, K)
        return distance

    def read_params(i):
        nearest_index = nearest_atoms_indices_torch[i]
        types = atom_types[nearest_index]
        temp = list(map(lambda x: parameters[int(x)], types))
        return torch.tensor(temp)

    feature_input = torch.zeros(num_atoms, num_nearest_atoms + 1, num_features)
    feature_input[:, :, :3] = torch.stack(list(map(lambda x: cal_dist(x), range(num_atoms))))
    # making mapping for each element
    feature_input[:, :, 3:] = torch.stack(list(map(lambda x: read_params(x), range(num_atoms))))
    return feature_input#, one_frame_coords

def preprocess_one_frame(one_frame_coords, num_nearest_atoms, num_atoms, num_features, atom_types, parameters):
    nearest_atoms_indices_torch = find_nearest_atoms_torch(one_frame_coords, num_nearest_atoms)

    def cal_dist(i):
        nearest_index = nearest_atoms_indices_torch[i]
        # first_parameter: the distance between each
        distance = one_frame_coords[nearest_index] - one_frame_coords[i]  # 8*3 matrix
        return distance

    def read_params(i):
        nearest_index = nearest_atoms_indices_torch[i]
        types = atom_types[nearest_index]
        temp = list(map(lambda x: parameters[int(x)], types))
        return torch.tensor(temp)

    feature_input = torch.zeros(num_atoms, num_nearest_atoms + 1, num_features)
    feature_input[:, :, :3] = torch.stack(list(map(lambda x: cal_dist(x), range(num_atoms))))
    # making mapping for each element
    feature_input[:, :, 3:] = torch.stack(list(map(lambda x: read_params(x), range(num_atoms))))
    return feature_input


def periodic_distance(A, B, I, J, K):
    # A: n*3 matrix
    # B: n*3 matrix
    # I, J, K: periodicity in x,y,z dimension
    # 计算A和B之间的差异
    delta = A - B
    # 考虑周期性边界条件
    # 对于每个维度，计算最近的周期性距离
    delta[..., 0] = delta[..., 0] - I * torch.round(delta[..., 0] / I)
    delta[..., 1] = delta[..., 1] - J * torch.round(delta[..., 1] / J)
    delta[..., 2] = delta[..., 2] - K * torch.round(delta[..., 2] / K)
    # round: 四舍五入
    return delta
