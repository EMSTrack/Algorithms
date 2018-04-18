from ems.algorithms.algorithm import DispatcherAlgorithm

from ems.settings import Settings
from ems.data import Data 

import matplotlib.pyplot as plt


# Hans Yuan


file_path = "/Users/vectflux/Documents/Data/"
demands_filepath = file_path + "demand_points.csv"
bases_filepath = file_path + "/bases.csv"




def testSettings():
	set1 = Settings (debug=False)
	assert set1.demands_file is None

	set2 = Settings (debug=True, demands_file=demands_filepath)
	assert set2.demands_file is demands_filepath
	assert set2.demands_file == demands_filepath

	set3 = Settings (debug=False, bases_file=bases_filepath)
	set3.set_demands_fd (str(demands_filepath))
	assert set3.demands_file == set2.demands_file
	assert set3.demands_file is set2.demands_file

	return set3




def testData(settings):
	assert isinstance (settings, Settings)

	data = Data(settings)
	assert data.demands is not None
	assert data.bases   is not None


	return data





def main():
	settings     = testSettings()
	data         = testData(settings)

	input ("\nWhen ready, press Enter to print the data: demands\n")
	print (data.demands)

	input ("\nWhen ready, press Enter to print the data: bases\n")
	print (data.bases)

	print("\nFinished test.py \n")




if __name__ == "__main__": main()

