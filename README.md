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

- Incorporate the amortized file to speed up the process of finding the closest demand point to a case

- Port over the "coverage" function from the old repo

- Define a format for a configuration file and read it into Settings

- For kmeans_init_bases, remove dependency on the pandas dataframe and instead rely on list of objects

- Write tests for the datasets, algorithms, and settings

	- Move type checks in DispatcherAlgorithm to testing file
	
- Finish typing in function signatures for many functions

## Comments

- It may be too much to define both the default algos and the algos class in one file. 

- Need more thought about separation/combination of settings and data. 

- See order.pdf


