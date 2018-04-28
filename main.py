from ems.algorithms.dispatcher_algorithm import DispatcherAlgorithm
from ems.data.filters import kmeans_select_bases
from ems.data.tijuana import CSVTijuanaDataset
from ems.models.ambulance import Ambulance
from ems.settings import Settings
from ems.simulators.dispatcher_simulator import DispatcherSimulator


# TODO read from settings file
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
alg = DispatcherAlgorithm(traveltimes=dataset.traveltimes)

# Select bases
chosen_bases = kmeans_select_bases(dataset.bases, dataset.traveltimes)

# Generate ambulances - random base placement (may want to abstract into function)
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
                          algorithm=alg)
finished_cases = sim.run()
