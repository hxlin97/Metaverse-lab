# Towards AI-embedded Metaverse Chemistry Laboratory

This README provides instructions for setting up and using the code for the AI-embedded Metaverse Chemistry Laboratory.


## Requirements: 
For Physics-endorsed slice generation model:
PyTorch v1.11
streamlit
pandas
OR you may use `src/environment.yml`

For Unity Interface:
Unity version: 2022.3.5f1c1
Python: 3.8.8
Visual Studio 2022 with Unity development package: Visual Studio Tools for Unity, C# and Visual Basic

## Physics-endorsed slice generation model
**Part 1: the training of our proposed AI model**

Before running the training of this code, please first place the trajectory file in `dataset` folder. The exact trajectory file is too large and we cannot upload it to github. Current files can only serve as an example. To train the model, follow these steps:

1. **Modify Configuration**: Edit `src/config.py` to update the parameter information as per your requirements.

2. **Preprocessing**: First, open the python file `dataset/sort_atoms.py`, then revise the last line. Currently it is `sort_and_process_file('dump-8.reax.mgNO3', 'mgno3_8.lammpstrj')`, please revise the first parameter as the input trajectory file, and the second parameter as the output filename. This output filename should match the description in `src/config.py`. Run `src/preprocessing.serial.py`. This script preprocesses the original `lammpstrj` files. The preprocessing step will output the processed input and output files, which are `feature_inputs.pt` , `atom_coords.pt`, `atom_types.pt`, `box_list.pt` and `target.py`, located in the `/temp_data/` directory. These files are used in the future computaion.

3. **Model Training**: Execute `src/D4R_AFA_training.py`. This script uses the `feature_input.pt` and `target.py` files for model training. The output of the training process is a model file named `serial_model.pth`, which can be found in the `/pretrained_model` directory.

**Part 2: the implementation of our model**

For using the trained model:

1. **Model Prediction Example**: Refer to `src/model_prediction.ipynb`. This notebook demonstrates how to use the model. You need to input the system information file of a specific frame, including `atom_types` and `atom_coords` (the types and coordinates of the atoms). The model will output the atomic coordinates for the next frame. Note that the atom types are assumed to remain constant.

For further assistance or queries, please refer to the documentation or contact the project maintainers.

2. **Web Presentation**: Refer to `src/web_utilize.py`. You may use the code `streamlit run src/web_utilize.py`. The expected output is:
![image](https://github.com/hxlin97/Metaverse-lab/assets/58459755/e1941cfc-1828-4065-b715-dfb3c40ae95a)
You may follow the instruction on this figure to how to manipulate.

## Unity Interface
**Hardware**:
HTC-VIVE with a pair of joysticks
Beitong Asura2: BTP-2175S2 LB1

![image](https://github.com/hxlin97/Metaverse-lab/assets/114046154/0e948aca-e433-4a43-a4f3-5fb54d81fc30)

Figure 1. View of Beitong Asura2 Joysticks.

**Operation Manual**
You can refer to the supplementary materials S3 of the article for details.
1.**AI-Supervisor Plugin**: We have added the AI-supervisor plugin as well as the atomic slice generation module. The AI-supervisor region lies at the left-hand side of the of interface. Users can interact with AI-supervisor with their own OpenAI-API key. The user will first search the experiment data through AI-supervisor. The user can input research field, paper title of DOI to find the information of the article.

2.**Forcefield Optimization**: In the middle part, the users adjusted the forcefield Tensor, where the system properties are calculated on the black panel compared to the experiment value. The demonstration described the optimization process of water system. In the liquid properties interface, there are mainly three regions: the Forcefield matrix region; the Option region; and the Benchmark region. The Forcefield matrix region contains a 12×12 matrix, including 144 boxes. Each box represents a matrix element, which value can be arbitrary set through joystick Beitong Asura2, where the left panel is responsible for the value of matrix indices, and the right panel is responsible for shifting between different matrix indices. Adjacent to the forcefield matrix, there is a “Setting” region, which controls the temperature and pressure of the simulation system. This is also controlled by the Beitong Asura2. 

After setting the forcefield matrix and the simulation environment, players can send the modified forcefield to the backend slice generation module by clicking the “COMPLETE” button using VIVE joystick. The forcefield matrix will be firstly diagonalized, and the eigenvalues are sent to modify the forcefield parameters. The trajectory of atoms and calculated properties will be read from the output files and shown in the interface by clicking “View Trajectory” with VIVE joystick. The right-hand side of the scene is the benchmark region. After prediction of model, the properties will be sent back to the interface and shown in this region. The upper part summarizes the current properties of the system, compared to the corresponding experiment value. The lowest part is the option region. Firstly, the atomic trajectory file will be generated after each simulation. Each frame of the trajectory can be visualized in the interface by clicking “View Trajectory” repeatedly. Secondly, player can interact with the trajectory. Each atom of the trajectory is grabbable (press the side button of VIVE joystick) and removable (press the trigger button of VIVE joystick). In this way, the player can analyze the trajectory to find the current setback of forcefield model. Then, he can save the modified trajectory to a new file, which can be used for the next round optimization. 

The right-hand side shows the bulk and the microscopic state of the solvation process. The bulk state is described as a flask with color-variable solution. The solid is implemented with the particle system in unity. The size and lifetime of the particle system is accurately mapped from the real scenario. The microscopic state is the visualization of atomic trajectory of the physics-endorsed diffusion-like model. The digitalized state is compared to the real experiment observation in the real timeline. In the initial state, the solid diffuses into the water. During the solvation process, the solids gradually turned small and vanished in the solution, while the color of the solution is commensurate with the real experiments. 

3.**View of perspective**: The view of perspective is changed by the touchpad on the VIVE joystick. The player will move forward/backward/left/right in the game scene through the touchpad control. 

