# Ambulance Dispatch Simulation

A library to do ambulance dispatch simulation and analysis.

# Installation

There are many ways to get the simulator to work. See [The Installation Instructions](INSTALL.md).

# See the help message

`python3 run-simulation --help`

Among other things, you will see this:

`usage: run-simulation [-h] config_file` 

The program expects a configuration file with the simulation. 

# YAML Configuration Files

The configuration file is in YAML format, and it contains user specifications for how the simulation runs. For specification details, an upcoming paper will detail that. For now, take a look 
at `configurations/example.yaml`. 

# Run an example simulation

`python3 run-simulation configurations/example.yaml`

# Run a simple simulation

`python3 run-simulation configurations/simple.yaml`  

# Custom Simulation

To run a custom simulation, create a new YAML file and specify the requirements for the simulation (look to the other YAMLs for an example). Additional extensions for the framework can also be specified here.
