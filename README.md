# Getting Started

- agent-based contains everything relating to the agent based theory of mind models
- machine-learning contains everything related to the reinforcement learning agents

I recommend making a python virtual environment for all dependencies.

## Shared Dependencies
```
pip install numpy
pip install matplotlib
```
## Running the RL experiments
```
sbatch rainbowZero.txt
sbatch rainbowToM.txt
```
## Collecting the character embeddings in a dictionary
```
sbatch collectChar.txt
```
## Analyze character embedings and produce plots
```
analyze_chars.py
```
