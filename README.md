# Python framework for Reinforcement Learning

This framework can be used to illustrate various principles in reinforcement learning. 
Due to the module-like design, you can easily introduce and test your own methods.

## Framework installation

For this installation, you have to download or clone the repository. Futhermore, a python-environment should be already installed.
* Navigate to the directory
* Activate your environment
* Issue the following command: 
```bash
% pip install -e .
```
(it will install all necessary packages into the current python environment)
* You are ready to use the framework!

## Generate Environment

A environment is simulated for training an agent. With the script **generate.py**, a simple grid with a start and end point (terminal nodes) can be created.
The layout and file path are specified as transfer parameters.

```bash
python generate.py 5 6 test/grid.pkl
```

This command will create a 5x6 grid and save the environment as .pkl file.

## Training

The file **train.py** is responsible for the preprocessing and management stuff between the learning algorithm and the previously created environment.
You can interact with this script as follows:


```bash
python train.py test/grid.pkl q_learning
```

It expects two transfer parameters: file path and learning method/algorithm. (Currently only Q-Learning is available.)
The script will save the trained model as .outcome file which can be used for further computation.

## Visualization

To see the resulting utility function, which is an approximation of the ideal policy, the file **view.py** creates a visual representation.

```bash
python view.py test/q_learning.outcome
```

The .outcome file is used as transfer parameter.

The following image shows an illustration of the interface:
![alt text](https://raw.githubusercontent.com/malex1106/rl_framework/main/images/view_interface.png "view.py visualization")

© Alexander Fichtinger, student, studies in Artificial Intelligence



