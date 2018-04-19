from ems.algorithms.algorithm import DispatcherAlgorithm

from ems.settings import Settings
from ems.data import CSVTijuanaData

import matplotlib.pyplot as plt


# Hans Yuan

file_path = "/Users/vectflux/Documents/Data/"
demands_filepath = file_path + "demand_points.csv"
bases_filepath = file_path + "/bases.csv"

# Tim - we need to get started on the settings file pls

file_path = '/Users/timothylam/Documents/school/ENG100L/data-cruz-roja/'
bases_filepath = file_path + 'bases.csv'
demands_filepath = file_path + 'demand_points.csv'
cases_filepath = file_path + 'calls.csv'

# TODO cases_filepath


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

    set4 = Settings(debug=False, cases_file=cases_filepath)
    set4.set_demands_fd (str(demands_filepath))
    set4.set_bases_fd (str(bases_filepath))
    assert set4.cases_file is cases_filepath
    assert set4.demands_file is set3.demands_file
    assert set4.bases_file is set3.bases_file

    return set4


def testData(settings):
    assert isinstance (settings, Settings)

    data = CSVTijuanaData(settings)
    assert data.demands is not None
    assert data.bases   is not None
    assert data.cases   is not None

    return data


def printData(data):
    input ("\nWhen ready, press Enter to print the data: demands\n")
    print (data.demands)

    input ("\nWhen ready, press Enter to print the data: bases\n")
    print (data.bases)

    input ("\nWhen ready, press Enter to print the data: cases\n")
    print (data.cases)
    return


def testAlgorithms(data):
    da = DispatcherAlgorithm()

    da.init_bases_typecheck (data)
    da.init_ambulance_placements(data)
    da.select_ambulance(data)




def main():
    settings     = testSettings()
    data         = testData (settings)
    
    # printData (data) # Uncomment this to print out the data.

    testAlgorithms (data)
    
    print("\nFinished test.py \n")




if __name__ == "__main__": main()

