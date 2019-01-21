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

In Ubuntu, "tkinter" seems to be missing for Python3.6. To install,

`sudo apt-get install python3.6-tk`


### Run the code! 

If all is well, the simulator library should be runnable now. 

`python run.py --help`

`python run.py example.yaml`

### yaml configuration files

We use yaml to read configurations from files into the simulator. Take a look 
at `configurations/example.yaml` for an example.

## Project UML

![](uml/ems_uml.png)

