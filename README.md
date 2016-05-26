# Train a Smartcab How to Drive

Udacity Machine Learning - Reinforcement Learning Project
The goal of this project was to implement a Q-Learning algorithm so that a smartcab agent can learn to navigate to a destination within a predefined time in a grid-world.

The methodology for the implementation of this code is found in the report found in the main directory of this repository.  

## Install

This project requires Python 2.7 with the pygame library installed:

https://www.pygame.org/wiki/GettingStarted

## Code

Open `smartcab/agent.py` and implement `LearningAgent`. Follow `TODO`s for further instructions.

## Run

Make sure you are in the top-level project directory `smartcab/` (that contains this README). Then run:

```python smartcab/agent.py```

OR:

```python -m smartcab.agent
```

## Automated Data Collection

To run the automated data collection uncomment the script according to single scenario or iterative.

#### For iterative collection
- Comment out the Single Scenario Function call
- set the number of times for each iteration
- choose ranges and steps for Gamma, Epsilon and Epsilon Decay

```
  gamma_values = [(x / 100.0) for x in  range(30, 91, 10)]
  epsilon_values = [(x / 100.0) for x in range(50, 55, 10)]
  epsilon_decay_values = [(x / 100.0) for x in range(90, 100, 3)]

  number_of_times = 5
    for i in range(0, number_of_times):
    iterative_data_collection(gamma_values, epsilon_values, epsilon_decay_values, str(i))
```

- Run ```python automated_data_collection.py```

#### For Single Scenario
- Comment out the Iterative Data Collection Function Call
- Set the variables for Gamma, Epsilon, Epsilon Decay and the number of times

```
  single_scenario_repeat_data_collection(0.50, 0.50, 0.99, 10)
```

- Run ```python automated_data_collection.py```
