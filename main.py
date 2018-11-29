import argparse
from datetime import timedelta, datetime

from geopy import Point

from ems.algorithms.selection.dispatch_fastest import BestTravelTimeAlgorithm
from ems.analysis.metrics.count_pending import CountPending
from ems.analysis.metrics.coverage.percent_coverage import PercentCoverage
from ems.analysis.metrics.coverage.radius_coverage import RadiusCoverage
from ems.analysis.metrics.metric_aggregator import MetricAggregator
from ems.analysis.metrics.total_delay import TotalDelay
from ems.datasets.case.random_case_set import RandomCaseSet
from ems.datasets.location.tijuana_base_set import TijuanaBaseSet
from ems.datasets.location.tijuana_demand_set import TijuanaDemandSet
from ems.datasets.travel_times.tijuana_travel_times import TijuanaTravelTimes
from ems.filters import kmeans_select_bases
from ems.generators.case.location.random_circle import RandomCircleLocationGenerator
from ems.generators.case.time.poisson_time import PoissonCaseTimeGenerator
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

# Initialize dataset for cases
# case_set = Jan2017CaseSet(filename=settings.cases_file)
# case_set = DeDatosCaseSet(filename=settings.cases_file, duration_generator=event_duration_generator)

# Define random case params
# This example = 4 cases an hour
num_cases = 200

timeframe = timedelta(hours=48)
initial_time = datetime.now() - timeframe
end_time = datetime.now()
minutes = timeframe.total_seconds() / 60

# Define a poisson case time generator with given lambda
case_time_generator = PoissonCaseTimeGenerator(lmda=num_cases/minutes)

# Define a random location generator
center = Point(latitude=32.504876, longitude= -116.958774)
radius = 0.5
location_generator = RandomCircleLocationGenerator(center=center, radius=radius)

event_duration_generator = TravelTimeDurationGenerator(travel_times=travel_times)

case_set = RandomCaseSet(num_cases=num_cases,
                         initial_time=initial_time,
                         case_time_generator=case_time_generator,
                         location_generator=location_generator,
                         event_duration_generator=event_duration_generator)

# Initialize ambulance_selection algorithm
ambulance_select = BestTravelTimeAlgorithm(travel_times=travel_times)

# Initialize demand percentage coverage metric
percent_coverage = PercentCoverage(demands=demand_set,
                                   travel_times=travel_times,
                                   r1=timedelta(seconds=600))

# Initialize demand radius coverage metric
radius_coverage = RadiusCoverage(demands=demand_set,
                                 travel_times=travel_times)

# Initialize other metrics
total_delay = TotalDelay()
count_pending = CountPending()

# Initialize metric aggregator
metric_aggregator = MetricAggregator([percent_coverage, total_delay, count_pending])

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
                                    ambulance_selector=ambulance_select,
                                    metric_aggregator=metric_aggregator)

# Start the simulation
case_record_set, metric_aggregator = sim.run()

case_record_set.write_to_file('./results/processed_cases.csv')
metric_aggregator.write_to_file('./results/metrics.csv')

# print("Simulator has finished.")
#
# summarize = Summarize(
#     len(case_set),
#     clargs.slices,
#     len(ambulances)
# )

# summarize.specific(measured_coverage, dataset.demands)
# summarize.overall(measured_coverage)
# summarize.duration(
#     [f.start_time for f in finished_cases],
#     [f.get_duration() for f in finished_cases])
