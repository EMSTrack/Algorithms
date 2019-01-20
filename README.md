# Ambulance Dispatch Simulation

A library to do ambulance dispatch simulation and analysis.

## Install and Run

### A virtual environment

Create a new environment: 

`virtualenv -p python3 venv`

Use the new environment:

`source venv/bin/activate`

### Libraries

Install the dependencies via the following command:

`pip install -r requirements.txt` 

In Ubuntu, Python 3.6 seems to be missing "tkinter". To install,

`sudo apt-get install python3.6-tk`

If all is well, the simulator library should be runnable now. 

`python run.py small.yaml`

`python run.py --help`

## Project UML

![](uml/ems_uml.png)

