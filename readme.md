# Towards AI-embedded Metaverse Chemistry Laboratory

This README provides instructions for setting up and using the code for the AI-embedded Metaverse Chemistry Laboratory.
![image](https://github.com/hxlin97/Metaverse-lab/assets/58459755/a83c28c5-6967-4f5e-ad3f-a2dd0652c6fd)

## Requirements: 
PyTorch v1.11

streamlit

pandas

OR you may use `src/environment.yml`

## Part 1: the training of our proposed AI model

To train the model, follow these steps:

1. **Modify Configuration**: Edit `src/config.py` to update the parameter information as per your requirements.

2. **Preprocessing**: Run `src/preprocessing.serial.py`. This script preprocesses the original `lammpstrj` files. The preprocessing step will output the processed input and output files, which are `feature_inputs.pt` , `atom_coords.pt`, `atom_types.pt`, `box_list.pt` and `target.py`, located in the `/temp_data/` directory. These files are used in the future computaion.

3. **Model Training**: Execute `src/D4R_AFA_training.py`. This script uses the `feature_input.pt` and `target.py` files for model training. The output of the training process is a model file named `serial_model.pth`, which can be found in the `/pretrained_model` directory.

## Part 2: the implementation of our model

For using the trained model:

1. **Model Prediction Example**: Refer to `src/model_prediction.ipynb`. This notebook demonstrates how to use the model. You need to input the system information file of a specific frame, including `atom_types` and `atom_coords` (the types and coordinates of the atoms). The model will output the atomic coordinates for the next frame. Note that the atom types are assumed to remain constant.

For further assistance or queries, please refer to the documentation or contact the project maintainers.

2. **Web Presentation**: Refer to `src/web_utilize.py`. You may use the code `streamlit run src/web_utilize.py`. 
