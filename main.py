import argparse

from ems.algorithms.coverage.percent_coverage import PercentCoverage
from ems.algorithms.selection.dispatch_fastest_ambulance import BestTravelTimeAlgorithm
from ems.data.filters import kmeans_select_bases
from ems.data.tijuana import CSVTijuanaDataset
from ems.models.ambulance import Ambulance
from ems.settings import Settings
from ems.simulators.dispatcher_simulator import DispatcherSimulator
from ems.algorithms.analyze.summarize import Summarize

# TODO allow command line arguments
parser = argparse.ArgumentParser(description="Load settings, data, preprocess models, run sim.")
parser.add_argument('--ambulances', help="Number of ambulances", type=int, required=False)
parser.add_argument('--bases',      help='Number of bases',     type=int,  required=False)
parser.add_argument('--settings',   help="for example, '--settings hans'. Don't include '.json'", type=str, required=True)
parser.add_argument('--slices',     help="Number of cases to simulate", type=int, required=False)

clargs = parser.parse_args()

# Initialize settings
settings = Settings(debug=True,
                    args=clargs)

# Initialize dataset
dataset = CSVTijuanaDataset(demands_file_path=settings.demands_file,
                            bases_file_path=settings.bases_file,
                            cases_file_path=settings.cases_file,
                            travel_times_file_path=settings.travel_times_file,
                            slices=clargs.slices
                            )

# Initialize ambulance_selection
ambulance_select = BestTravelTimeAlgorithm(travel_times=dataset.travel_times)

# Initialize demand_coverage
determine_coverage = PercentCoverage(travel_times=dataset.travel_times)

# Select bases
chosen_base_locations = kmeans_select_bases(dataset.bases, dataset.travel_times)

# Generate ambulances - random base placement (may want to abstract into function)
ambulances = []
for index in range(settings.num_ambulances):
    ambulance = Ambulance(id=index,
                          base=chosen_base_locations[index],
                          location=chosen_base_locations[index])
    ambulances.append(ambulance)

# Initialize the simulator
sim = DispatcherSimulator(ambulances=ambulances,
                          cases=dataset.cases,
                          ambulance_selector=ambulance_select,
                          coverage_alg=determine_coverage,
                          plot=settings.plot
                          )

# Start the whole thing
finished_cases, measured_coverage = sim.run()

print("Simulator has finished.")

summarize = Summarize()

# summarize.specific(measured_coverage, dataset.demands)
summarize.overall(measured_coverage)
summarize.duration([f.get_duration() for f in finished_cases])

# import IPython; IPython.embed()
