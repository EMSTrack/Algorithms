import argparse

from ems.algorithms.analysis.demand_coverage import DemandCoverage
from ems.algorithms.selection.dispatch_fastest_ambulance import BestTravelTimeAlgorithm
from ems.data.filters import kmeans_select_bases
from ems.data.tijuana import CSVTijuanaDataset
from ems.models.ambulance import Ambulance
from ems.settings import Settings
from ems.simulators.dispatcher_simulator import DispatcherSimulator

# TODO allow command line arguments
parser = argparse.ArgumentParser(description="Load settings, data, preprocess models, run sim.")
parser.add_argument('--ambulances', help="Number of ambulances", type=int, required=False)
parser.add_argument('--bases',      help='Number of bases',     type=int,  required=False)
parser.add_argument('--settings', help="Location of settings yaml file", type=str, required=False)

clargs = parser.parse_args()

# TODO Fix this so that we can store these in a file :)
file_path = '/Users/timothylam/Documents/school/ENG100L/data-cruz-roja/'
# file_path = '../Data/'
# file_path = '~/tmp/data-cruz-roja/'

print (file_path)

bases_filepath = file_path + 'bases.csv'
demands_filepath = file_path + 'demand_points.csv'
cases_filepath = file_path + 'calls.csv'
travel_times_filepath = file_path + 'times.csv'
cd_mapping_filepath = file_path + 'calls_demand_amor.csv'

# Initialize settings
settings = Settings(debug=True,
                    demands_file=demands_filepath,
                    bases_file=bases_filepath,
                    cases_file=cases_filepath,
                    travel_times_file=travel_times_filepath,
                    args=clargs)

# Initialize dataset
dataset = CSVTijuanaDataset(demands_filepath=settings.demands_file,
                            bases_filepath=settings.bases_file,
                            cases_filepath=settings.cases_file,
                            travel_times_filepath=settings.travel_times_file)

# Initialize ambulance_selection
ambulance_select = BestTravelTimeAlgorithm(travel_times=dataset.travel_times)

# Initialize demand_coverage
determine_coverage = DemandCoverage(travel_times=dataset.travel_times)

# Select bases
chosen_bases = kmeans_select_bases(dataset.bases, dataset.travel_times)

# Generate ambulances - random base placement (may want to abstract into function)
ambulances = []
for index in range(settings.num_ambulances):
    ambulance = Ambulance(id=index,
                          base=chosen_bases[index],
                          location=chosen_bases[index].location)
    ambulances.append(ambulance)

# Initialize the simulator
sim = DispatcherSimulator(ambulances=ambulances,
                          cases=dataset.cases,
                          ambulance_selector=ambulance_select,
                          coverage_alg=determine_coverage)

# Start the whole thing
finished_cases = sim.run()





