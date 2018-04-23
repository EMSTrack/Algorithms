from ems.algorithms.algorithm import DispatcherAlgorithm
from ems.data.tijuana import CSVTijuanaDataset
from ems.models.ambulance import Ambulance
from ems.settings import Settings

# TODO read from settings file
from ems.simulators.dispatcher_simulator import DispatcherSimulator

file_path = '/Users/timothylam/Documents/school/ENG100L/data-cruz-roja/'
# file_path = '~/tmp/data-cruz-roja/'
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

# Select bases
chosen_bases = alg.init_bases(dataset.bases, dataset.traveltimes_df)

# Generate ambulances
ambulances = []
for index in range(settings.num_ambulances):
    ambulance = Ambulance(id=index,
                          base=chosen_bases[index])
    ambulances.append(ambulance)

# Initialize and run the simulator
sim = DispatcherSimulator(ambulances=ambulances,
                          bases=chosen_bases,
                          cases=dataset.cases,
                          demands=dataset.demands,
                          algorithm=alg,
                          traveltimes=dataset.traveltimes)
finished_cases = sim.run()
