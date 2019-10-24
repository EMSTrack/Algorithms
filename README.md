# Ambulance Dispatch Simulation

A library to do ambulance dispatch simulation and analysis.

# Installation

There are many ways to get the simulator to work. See [The Installation Instructions](INSTALL.md).

# Learning how to run the simulator

`python3 run-simulation --help`

Among other things, you will see this:

`usage: run-simulation [-h] config_file` 

The program expects you to configure the specifications of the simulation and state where those specifications are. 

## YAML Configuration Files

The configuration file is in YAML format, and it contains user specifications for how the simulation runs. For specification details, an upcoming paper will detail that. For now, take a look 
at `configurations/example.yaml`. 

# Run an example simulation

#### The simulation currently must be run from the repository itself. 

`pwd` should return your directory and `/Algorithms/`. For example, here's mine: 

`/Users/vectflux/ReEMS/Algorithms`

#### Let's run the simulation.

`python3 run-simulation configurations/example.yaml`

If you got an error like `results does not exist`, make a new subdirectory:

`mkdir results`

Don't worry about accidentally pushing your own results. This folder is in the `.gitignore` file. 

#### On successful simulation, you will find the results saved under `./results/`

`ls ./results/`


# Run a simple simulation

`python3 run-simulation configurations/simple.yaml`  

#### You will find that this fails! 

That's because this particular configuration uses certain historical data files that do not exist **yet**. 

You will need to run one of our scripts to produce some synthetic input data. These inputs are examples of well-formatted CSV files that EMS organizations can export their historical data to. Alternatively, another data reader can be implemented that accepts data in a different way. 

`[Insert command for script here.]`

#### Now if you run the simulation again, the historical data is read into the simulation. 

`python3 run-simulation configurations/simple.yaml`  

#### On successful simulation, you will find the results saved under `./results/` under a different name.

`ls ./results/`

# Custom Simulation

- To run a custom simulation, create a new YAML file or copy an existing one. 

- Specify the requirements for the simulation (look to the other YAMLs for an example). Additional extensions for the framework can also be specified here.

`python run.py simple.yaml`

## Run on binder

Demo notebooks can be run online on [binder](https://mybinder.org). 

Just click on the binder logo:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EMSTrack/Algorithms/master-binder)
