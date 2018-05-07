from ems.algorithms.ambulance_selection import DispatcherAlgorithm
from ems.data.tijuana import CSVTijuanaDataset
from ems.models.base import Base
from ems.settings import Settings

# Hans Yuan

file_path = "/Users/vectflux/Documents/Data/"
demands_filepath = file_path + "demand_points.csv"
bases_filepath = file_path + "/bases.csv"

# Tim

file_path = '/Users/timothylam/Documents/school/ENG100L/data-cruz-roja/'
bases_filepath = file_path + 'bases.csv'
demands_filepath = file_path + 'demand_points.csv'
cases_filepath = file_path + 'calls.csv'
traveltimes_filepath = file_path + 'times.csv'


# TODO cases_filepath


def testSettings():
    set1 = Settings(debug=False)
    assert set1.demands_file is None

    set2 = Settings(debug=True, demands_file=demands_filepath)
    assert set2.demands_file is demands_filepath
    assert set2.demands_file == demands_filepath

    set3 = Settings(debug=False, bases_file=bases_filepath)
    set3.demands_file = str(demands_filepath)
    assert set3.demands_file == set2.demands_file
    assert set3.demands_file is set2.demands_file

    set4 = Settings(debug=False, cases_file=cases_filepath)
    set4.demands_file = str(demands_filepath)
    set4.bases_file = str(bases_filepath)
    set4.traveltimes_file = str(traveltimes_filepath)
    assert set4.cases_file is cases_filepath
    assert set4.demands_file is set3.demands_file
    assert set4.bases_file is set3.bases_file
    assert set4.traveltimes_file is traveltimes_filepath

    return set4


def testData(settings):
    assert isinstance(settings, Settings)

    data = CSVTijuanaDataset(settings)
    assert data.demands is not None
    assert data.bases is not None
    assert data.cases is not None

    return data


def printData(data):
    input("\nWhen ready, press Enter to print the data: demands\n")
    print(data.demands)

    input("\nWhen ready, press Enter to print the data: bases\n")
    print(data.bases)

    input("\nWhen ready, press Enter to print the data: cases\n")
    print(data.cases)
    return


# TODO -- move assertions to tests.py
def init_bases_typecheck(algorithm, dataset):
    """ Runs init_bases, but makes sure the resulting dataset.chosen_bases is right type """
    algorithm.init_bases(dataset)
    assert isinstance(dataset.chosen_bases, list)
    for element in dataset.chosen_bases:
        assert isinstance(element, Base)


# TODO
def init_ambulance_placements_typecheck(algorithm, dataset):
    """ Runs init_ambulance_placements, but makes sure the resulting ___ is right type or state"""
    pass

    # TODO


def select_ambulance_typecheck(algorithm, dataset):
    """ Runs select_ambulance, but makes sure the resulting ___ is right type or state"""
    pass


def testAlgorithms(data, settings):
    da = DispatcherAlgorithm()

    init_bases_typecheck(da, data)
    init_ambulance_placements_typecheck(da, data)
    select_ambulance_typecheck(da, data)


def main():
    settings = testSettings()
    data = testData(settings)

    # printData (data) # Uncomment this to print out the data.

    testAlgorithms(data, settings)

    print("\nFinished test.py \n")


if __name__ == "__main__": main()
