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

This command will create an 5x6 grid and save the environment as .pkl file.
