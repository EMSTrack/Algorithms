# Ambulance Dispatch Simulation

A library to do ambulance dispatch simulation and analysis.

# Installation

There are many ways to get the simulator to work. See [The Installation Instructions](INSTALL.md).

## Run

If all is well, the simulator library should be runnable now. 

`python3 run-simulation --help`

### YAML Configuration Files

We use yaml to read configurations from files into the simulator. Take a look 
at `configurations/example.yaml` for an example. To run it:

`python3 run-simulation configurations/example.yaml`

### Simple Example

`python3 run-simulation configurations/simple.yaml`  

### Custom Simulation

To run a custom simulation, create a new YAML file and specify the requirements for the simulation (look to the other YAMLs for an example). Additional extensions for the framework can also be specified here.
