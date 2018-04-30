from ems.algorithms.dispatcher_algorithm import DispatcherAlgorithm
from ems.data.filters import kmeans_select_bases
from ems.data.tijuana import CSVTijuanaDataset
from ems.models.ambulance import Ambulance
from ems.settings import Settings
from ems.simulators.dispatcher_simulator import DispatcherSimulator
from ems.utils import generate_amor_filename


# TODO read from settings file

file_path = '/Users/timothylam/Documents/school/ENG100L/data-cruz-roja/'
# file_path = '~/tmp/data-cruz-roja/'
bases_filepath = file_path + 'bases.csv'
demands_filepath = file_path + 'demand_points.csv'
cases_filepath = file_path + 'calls.csv'
traveltimes_filepath = file_path + 'times.csv'

cd_mapping_filepath = generate_amor_filename(cases_filepath)

# Initialize settings
settings = Settings(debug=True,
                    demands_file=demands_filepath,
                    bases_file=bases_filepath,
                    cases_file=cases_filepath,
                    traveltimes_file=traveltimes_filepath,
                    cd_mapping_file=cd_mapping_filepath)

# Initialize dataset
dataset = CSVTijuanaDataset(demands_filepath=settings.demands_file,
                            bases_filepath=settings.bases_file,
                            cases_filepath=settings.cases_file,
                            traveltimes_filepath=settings.traveltimes_file,
                            cd_mapping_filepath=settings.cd_mapping_file)

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
