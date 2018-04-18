# Ambulance Dispatch Simulation

A library to do ambulance dispatch simulation and analysis. 

To run, take a look at `test.py`. Notice the filepaths there. You will need to edit 
`file_path`, `demands_filepath`, and `bases_filepath` to point at the Cruz Roja datasets. 

You'll notice that an exception will be thrown. This is because the datasets will require
labels in the CSV files. Add a newline above the datasets, naming the latitudes and longitudes.

When it is correct, the test program will end up asking you to proceed when ready. (Press Enter.) 

# TODO 

- Define what algorithms are used by passing function pointers to the Algorithms class. 

- Read from files -- CSV files in the first line should contain the name of the data.

	- If the name deviates, throw an exception. e.g. base is a list of (lattitude, logitude)
		- GOT UP TO HERE. Reading demand points and base points from CSV now implemented.

	- In choosing the bases, use class Algorithm's instance variable base_init pointing to the 
	base chooser function.

		- Got this to work. KMeans base selector as default algorithm ported over. Two more to go.

- Run the simulation. It should return a list of lists (or the PANDAS 2D Array) of information.

- Run each column of data (list of a certain metric) into the each function in a list of analysis functions.