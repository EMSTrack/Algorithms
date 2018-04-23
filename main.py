from ems.simulator import DispatcherSimulator
from ems.algorithms.algorithm import DispatcherAlgorithm
from ems.settings import Settings
from ems.data.dataset import CSVTijuanaDataset
from ems.simulator import DispatcherSimulator

# TODO read from settings file
file_path = '/Users/timothylam/Documents/school/ENG100L/data-cruz-roja/'
bases_filepath = file_path + 'bases.csv'
demands_filepath = file_path + 'demand_points.csv'
cases_filepath = file_path + 'calls.csv'
traveltimes_filepath = file_path + 'times.csv'

settings = Settings (debug=True, 
                demands_file=demands_filepath,
                bases_file=bases_filepath,
                cases_file=cases_filepath,
                traveltimes_file=traveltimes_filepath)

dataset = CSVTijuanaDataset(settings)

alg = DispatcherAlgorithm()

sim = DispatcherSimulator(settings, dataset, alg)
finished_cases = sim.run()