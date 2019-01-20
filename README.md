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

In Ubuntu, "tkinter" seems to be missing for Python3.6. To install,

`sudo apt-get install python3.6-tk`


### Run the code! 

If all is well, the simulator library should be runnable now. 

`python run.py --help`

`python run.py small.yaml`


## Project UML

![](uml/ems_uml.png)

