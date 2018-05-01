# Ambulance Dispatch Simulation

A library to do ambulance dispatch simulation and analysis. 

To run the simulation, take a look at `main.py`. Notice the filepaths there. You will need to edit 
`file_path`, `demands_filepath`, and `bases_filepath` to point at the Cruz Roja datasets. 

To test, take a look at `test.py`. Similar to main.py, you will need to edit 
`file_path`, `demands_filepath`, and `bases_filepath` to point at the Cruz Roja datasets. 

You'll notice that an exception will be thrown. This is because the datasets will require
labels in the CSV files. Add a newline above the datasets, naming the latitudes and longitudes.

To see this, you may need to uncomment `printData()`. The test program will end up asking you 
to proceed when ready. (Press Enter.) 

## TODO 

- Port over the "coverage" function from the old repo

- Begin brainstorming and implementing additional simulation evaluation metrics (e.g. coverage, etc.)

- Expand the current testing framework to test the new project infrastructure
