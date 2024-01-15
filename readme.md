代码文件在10.26.1.1 /xsdata1/diffusion/D4R_total/src
# 训练部分
1. 修改src/config.py中的参数信息
2. 运行src/preprocessing.serial.py，此函数会对原始的lammpstrj进行预处理，这项处理会输出预处理之后的输入文件与输出文件，分别为/temp_data/下的feature_inputs.pt与target.py文件
3. 运行src/D4R_AFA_training.py， 此函数会根据给定的feature_input.pt与target.py文件进行模型训练，训练的输出结果是一个对应的模型文件,为/pretrained_model下的serial_model.pth文件
# 使用部分
1. 在src/model_prediction.ipynb文件中举例了使用，对应的方法为先输入某一帧的系统信息文件，包括对应的atom_types与atom_coords，即原子类型与对应的原子坐标，该模型最终会输出下一帧的原子坐标。此处我们认为原子类型是保持不变的。