import argparse

from ems.algorithms.selection.dispatch_fastest import BestTravelTimeAlgorithm
from ems.analysis.analyze.summarize import Summarize
from ems.analysis.coverage.percent_coverage import PercentCoverage
from ems.datasets.case.dedatos_case_set import DeDatosCaseSet
from ems.datasets.case.jan2017_case_set import Jan2017CaseSet
from ems.datasets.location.tijuana_base_set import TijuanaBaseSet
from ems.datasets.location.tijuana_demand_set import TijuanaDemandSet
from ems.datasets.travel_times.tijuana_travel_times import TijuanaTravelTimes
from ems.filters import kmeans_select_bases
from ems.generators.event.travel_time_duration import TravelTimeDurationGenerator
from ems.models.ambulance import Ambulance
from ems.settings import Settings
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
travel_times = TijuanaTravelTimes(loc_set_1=base_set,
                                  loc_set_2=demand_set,
                                  filename=settings.travel_times_file)

# Initialize event duration generator
event_duration_generator=TravelTimeDurationGenerator(travel_times=travel_times)

# Initialize dataset for cases
# case_set = Jan2017CaseSet(filename=settings.cases_file)
case_set = DeDatosCaseSet(filename=settings.cases_file, duration_generator=event_duration_generator)

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
                                    case_set=case_set,
                                    ambulance_selector=ambulance_select)

# Start the whole thing
finished_cases, measured_coverage = sim.run()

print("Simulator has finished.")

summarize = Summarize(
    len(case_set),
    clargs.slices,
    len(ambulances)
)

# summarize.specific(measured_coverage, dataset.demands)
# summarize.overall(measured_coverage)
# summarize.duration(
#     [f.start_time for f in finished_cases],
#     [f.get_duration() for f in finished_cases])
