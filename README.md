# Ambulance Dispatch Simulation

A library to do ambulance dispatch simulation and analysis.

## Installation

Highly suggested to use a UNIX-based operating system like Mac OS or Linux. 

#### Suggested operating systems: 

- Ubuntu 16 or higher or MacOS Sierra or higher

- Windows - use one of Microsoft's Linux subsystems. We are working on Docker containerizing
the simulator but there are no guarantees. 

#### Programming language: 
- Python 3. At least Python 3.5 should be good.
- Python 2 will not work. 
- Suggested: Python 3.7


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

`python3 run-simulation configurations/simple.yaml`  

### Custom Simulation

To run a custom simulation, create a new YAML file and specify the requirements for the simulation (look to the other YAMLs for an example). Additional extensions for the framework can also be specified here.
