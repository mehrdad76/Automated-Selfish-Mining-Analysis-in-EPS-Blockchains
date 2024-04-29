This repository contains the codebase of the paper titled "Fully Automated Selfish Mining Analysis in Efficient Proof
Systems Blockchains".

1. Dependencies:

In order to run the code the following dependencies must be met:

    - Python 3 should be installed. We used Python 3.10 for obtaining the results in the paper. 
    - `Stormpy` library should be installed. (https://moves-rwth.github.io/stormpy/installation.html)
    - `matplotlib` library should be installed. 

2. Structure and How to run:

There are followings in the repository:

    - Storm models in `storm_models` folder.
    - A Python file `EPS_experiments.py` for binary search.
    - `results` folder 
To run each of the experiments, simply execute: 
`python3 EPS_experiments.py [gamma]` 
where `[gamma]` is one of 0, 0.25, 0.5, 0.75, and 1.
Example: `python3 EPS_experiments.py 0`

After finishing executing, you can find the diagram and log of times in the `results` folder.
