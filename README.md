# Python framework for Artificial Intelligence algorithms

This framework can be used to illustrate various ai-principles. 
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

## Generate Environment/Sample data

With the script **generate.py**, a simple grid/board or sample data can be created. Depending on the learning method, the generated output file is stored as .pkl or .json file which offer different structures. For further information, you can take a closer look in the appropriate help monitor.

**Sample commands:**

* Grid
```bash
python generate.py grid test_data/grid.pkl -width 5 -height 5
```

This command will create a 5x5 grid and save the environment as *.pkl* file. (for q_learning)

* Board

```bash
python generate.py board test_data/board.pkl -width 5 -height 5
```

This command will create a 5x5 board and save the environment as *.pkl* file. (for logical_reasoning)

* Random data

```bash
python generate.py data test_data/data.json -features 2 -samples 10
```

This command will create a random categorized data with 2 features and 10 samples. (for id3)
The visualisation currently only works with 2 features.


## Training

The file **train.py** is responsible for the preprocessing and management stuff between the learning algorithm and the previously created environment/data.
You can interact with this script as follows:


```bash
python train.py test_data/grid.pkl q_learning
```

It expects two transfer parameters: file path and learning method/algorithm. (q_learning, logical_reasoning, id3)
The script will save the trained model as *.out* file which can be used for further computation.

## Visualization

To see the resulting utility function, which is an approximation of the ideal policy, the file **view.py** creates a visual representation.

```bash
python view.py test_data/q_learning.out
```

The *.out* file is used as transfer parameter.
The following images show an illustration of the interface:

### Q-learning
![alt text](https://github.com/malex1106/ai_framework/blob/development/images/q_learning_view.png "view.py visualization - q_learning")


### Logical Reasoning
![alt text](https://github.com/malex1106/ai_framework/blob/development/images/logical_reasoning_view.png "view.py visualization - logical_reasoning")


### ID3 - Decision Tree
![alt text](https://github.com/malex1106/ai_framework/blob/development/images/id3_view.png "view.py visualization")

© Alexander Fichtinger, student, studies in Artificial Intelligence



