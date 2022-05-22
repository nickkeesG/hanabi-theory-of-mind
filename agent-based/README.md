## Running MCTS
To build the models used by the theory of mind agents, you need to run the training script:
```
python3 mcts_training.py
```

Every 10k iterations the training accuracy and testing accuracy is evaluated. Training accuracy is how often MCTS explores a winning trajectory (this is not relevant for the results). Testing accuracy is how often two ToM0 agents win when playing together using the current model.

The models generated are recorded in:
```
trees_mcts.dict
```

The log file recording the training process:
```
log_training.dict
```
Note that current .dict files are more recent than the one used in the thesis and so the models and plot won't be exactly identical. They were produced in the same way, however, and so they should be mostly the same.

The log can be plotted with the following script:
```
plot_training.py
```

## Testing Theory of Mind
To test all combinations of theory of mind agents, run the testing script:
```
python3 theory_of_mind.py
```
Note that this takes a very long time to run.

If you want to simulate a single game with theory of mind agents, run the following code:
```
from theory_of_mind import *
dictionary = load_dictionary()
state_tree = dictionary['400']
test_simulation(state_tree, ['ToM0', 'ToM0'], verbose=True)
```

You can substitute '400' with any of the following:
'50', '100', '150', '200', '250', '300', '350', '400'
This represents at which iteration (in 10k) the model was logged at.

You can substitute 'ToM0' with any of the following:
'ToM0', 'ToM0+', 'ToM1', 'ToM2', 'ToM0+ToM1', 'ToM1+ToM2', 'ToM1+2'


