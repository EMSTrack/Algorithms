import argparse
from datetime import timedelta

from ems.algorithms.algorithm_set import AlgorithmSet
from ems.algorithms.times.constant_duration import ConstantDurationAlgorithm
from ems.algorithms.times.travel_time_lookup import TravelTimeLookupAlgorithm
from ems.analysis.coverage.percent_coverage import PercentCoverage
from ems.algorithms.selection.dispatch_fastest import BestTravelTimeAlgorithm
from ems.datasets.case.jan2017_case_set import Jan2017CaseSet
from ems.datasets.location.tijuana_base_set import TijuanaBaseSet
from ems.datasets.location.tijuana_demand_set import TijuanaDemandSet
from ems.datasets.travel_times.tijuana_travel_times import TijuanaTravelTimes
from ems.filters import kmeans_select_bases
from ems.models.ambulance import Ambulance
from ems.settings import Settings
from ems.analysis.analyze.summarize import Summarize

# TODO allow command line arguments
from ems.simulators.dispatcher_simulator_event import EventBasedDispatcherSimulator

parser = argparse.ArgumentParser(description="Load settings, data, preprocess models, run sim.")
parser.add_argument('--ambulances', help="Number of ambulances", type=int, required=False)
parser.add_argument('--bases', help='Number of bases', type=int, required=False)
parser.add_argument('--settings', help="for example, '--settings hans'. Don't include '.json'", type=str, required=True)
parser.add_argument('--slices', help="Number of cases to simulate", type=int, required=False)

clargs = parser.parse_args()

# Initialize settings
settings = Settings(debug=True,
                    args=clargs)

# Initialize datasets
demand_set = TijuanaDemandSet(filename=settings.demands_file)
base_set = TijuanaBaseSet(filename=settings.bases_file)
case_set = Jan2017CaseSet(filename=settings.cases_file)
travel_times = TijuanaTravelTimes(loc_set_1=base_set,
                                  loc_set_2=demand_set,
                                  filename=settings.travel_times_file)

# Initialize ambulance_selection algorithm
ambulance_select = BestTravelTimeAlgorithm(travel_times=travel_times)

# Initialize demand_coverage algorithm
determine_coverage = PercentCoverage(travel_times=travel_times)

# Select bases
chosen_base_locations = kmeans_select_bases(base_set, travel_times)

# Generate ambulances - random base placement (may want to abstract into function)
ambulances = []
for index in range(settings.num_ambulances):
    ambulance = Ambulance(id=index,
                          base=chosen_base_locations[index],
                          location=chosen_base_locations[index])
    ambulances.append(ambulance)

# Initialize simulator
sim = EventBasedDispatcherSimulator(ambulances=ambulances,
                                    cases=case_set,
                                    ambulance_selector=ambulance_select)

# Start the whole thing
finished_cases, measured_coverage = sim.run()

print("Simulator has finished.")

summarize = Summarize(
    len(dataset.get_cases()),
    clargs.slices,
    len(ambulances)
)

# summarize.specific(measured_coverage, dataset.demands)
# summarize.overall(measured_coverage)
# summarize.duration(
#     [f.start_time for f in finished_cases],
#     [f.get_duration() for f in finished_cases])
