from ems.algorithms.algorithm import DispatcherAlgorithm
from ems.data.tijuana import CSVTijuanaDataset
from ems.settings import Settings
from ems.simulator import DispatcherSimulator

# TODO read from settings file
file_path = '/Users/timothylam/Documents/school/ENG100L/data-cruz-roja/'
bases_filepath = file_path + 'bases.csv'
demands_filepath = file_path + 'demand_points.csv'
cases_filepath = file_path + 'calls.csv'
traveltimes_filepath = file_path + 'times.csv'

# Initialize settings
settings = Settings(debug=True,
                    demands_file=demands_filepath,
                    bases_file=bases_filepath,
                    cases_file=cases_filepath,
                    traveltimes_file=traveltimes_filepath)

# Initialize dataset
dataset = CSVTijuanaDataset(settings)

# Initialize algorithm
alg = DispatcherAlgorithm()

# Initialize and run the simulator
sim = DispatcherSimulator(settings, dataset, alg)
finished_cases = sim.run()
