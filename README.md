# Ambulance Dispatch Simulation

A library to do ambulance dispatch simulation and analysis.

Try: `time python3 main.py --settings hans --ambulances 7 --bases 7 --slices 50`

python3 main.py --help

# Dependencies

- pandas
- scipy
- numpy
- geopy
- termcolor
- matplotlib

In Ubuntu, Python 3.6 seems to be missing "tkinter". To install,

`sudo apt-get install python3.6-tk`

# TODO

## Project UML

![](uml/ems_uml.png)


## TODO

- Introduce stochastic case and event generation

- Best coverage algorithm

- Best coverage/Fastest ambulance tension algorithm

- Coverage metrics

  - Given a desired radius, calculate the set covered

  - Given a desired set covered, calculate the radius
  
- Make a runnable animation of the simulation

- Introduce testing framework


## High-Level Overview

### Datasets (ems/data/*)

- CSVTijuanaDataset

- Jan2017Dataset

### Ambulance Selection Algorithms (ems/algorithms/selection/*)

- FastestAmbulanceSelection

- RandomAmbulanceSelection

### Simulators (ems/simulators/*)

- EventBasedDispatcherSimulator
