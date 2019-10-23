# Ambulance Dispatch Simulation

A library to do ambulance dispatch simulation and analysis.

## Install and Run

### A virtual environment

Create a new environment with Python 3: 

`virtualenv -p python3 venv`

Use the new environment:

`source venv/bin/activate`


### Libraries

Install the dependencies via the following command:

`pip install -r requirements.txt` 



### Run the code! 

If all is well, the simulator library should be runnable now. 

`python run.py --help`

`python run.py example.yaml`

### yaml configuration files

We use yaml to read configurations from files into the simulator. Take a look 
at `configurations/example.yaml` for an example.


### Generating bases and demands

You can generate data by going to `./examples`. Run: 

`python synthesize_data.py` 

It will produce sample bases, demand points, and the times 
between them. 

To use these, go up one directory. 

`python run.py simple.yaml`


## Run on binder

# notebooks
A variety of demo notebooks

These notebooks can be run online on [binder](https://mybinder.org). Just click on the binder logo:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EMSTrack/Algorithms/master)
