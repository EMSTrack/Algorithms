# Ambulance Dispatch Simulation

A library to do ambulance dispatch simulation and analysis.

## Installation

### A virtual environment

Create a new environment with Python 3: 

`virtualenv -p python3 venv`

Use the new environment:

`source venv/bin/activate`


### Libraries

Install the dependencies via the following command:

`pip3 install -r requirements.txt` 


## Run

If all is well, the simulator library should be runnable now. 

`chmod +x run-simulator`

`python3 run-simulation --help`

### YAML Configuration Files

We use yaml to read configurations from files into the simulator. Take a look 
at `configurations/example.yaml` for an example. To run it:

`python3 run-simulation configurations/example.yaml`

### Simple Example

`python3 run-simulation configurations/example.yaml`  

### Custom Simulation

To run a custom simulation, create a new YAML file and specify the requirements for the simulation (look to the other YAMLs for an example). Additional extensions for the framework can also be specified here.
