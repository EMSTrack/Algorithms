import argparse
from datetime import timedelta, datetime

import numpy as np
from geopy import Point

from ems.algorithms.hospital_selectors.select_fastest import FastestHospitalSelector
from ems.algorithms.selection.dispatch_fastest import BestTravelTimeAlgorithm
from ems.analysis.metrics.count_pending import CountPending
from ems.analysis.metrics.coverage.percent_coverage import PercentCoverage
from ems.analysis.metrics.coverage.radius_coverage import RadiusCoverage
from ems.analysis.metrics.metric_aggregator import MetricAggregator
from ems.analysis.metrics.total_delay import TotalDelay
from ems.datasets.ambulance.custom_ambulance_set import CustomAmbulanceSet
from ems.datasets.case.random_case_set import RandomCaseSet
from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.datasets.location.location_set import LocationSet
from ems.datasets.location.base.tijuana_base_set import TijuanaBaseSet
from ems.datasets.location.demand.tijuana_demand_set import TijuanaDemandSet
from ems.datasets.travel_times.tijuana_travel_times import TijuanaTravelTimes
from ems.generators.case.location.multiple_polygon import MultiPolygonLocationGenerator
from ems.generators.case.location.polygon import PolygonLocationGenerator
from ems.generators.case.time.poisson_time import PoissonCaseTimeGenerator
from ems.generators.event.duration.random_duration import RandomDurationGenerator
from ems.generators.event.duration.travel_time_duration import TravelTimeDurationGenerator
from ems.algorithms.base_selectors.round_robin_selector import RoundRobinBaseSelector
from ems.generators.event.event_generator import EventGenerator
from ems.settings import Settings
from ems.simulators.event_simulator import EventDispatcherSimulator

parser = argparse.ArgumentParser(description="Load settings, data, preprocess models. Run simulator on "
                                             "ambulance dispatch. Decisions are made during the simulation, but "
                                             "the events are output to a csv file for replay.")

parser.add_argument('--settings', help="for example, '--settings hans'. Don't include '.json'", type=str, required=True)

parser.add_argument('--ambulances', help="Number of ambulances", type=int, required=False)
parser.add_argument('--bases', help='Number of bases', type=int, required=False)

parser.add_argument('--slices', help="Number of cases to simulate", type=int, required=False)
parser.add_argument('--output-file', help="Output filename for simulator info", type=str, required=False)

clargs = parser.parse_args()

# Initialize settings
settings = Settings(debug=True,
                    args=clargs)

# Initialize datasets
demand_set = TijuanaDemandSet(filename=settings.demands_file)
base_set = TijuanaBaseSet(filename=settings.bases_file)
hospital_set = LocationSet(locations=[Point(longitude=-117.0097589492798,
                                            latitude=32.52506901611384),
                                      Point(longitude=-117.00371, latitude=32.5027),
                                      Point(longitude=117.0078, latitude=32.5180)])
travel_times = TijuanaTravelTimes(loc_set_1=base_set,
                                  loc_set_2=demand_set,
                                  filename=settings.travel_times_file)


# Filter base_set
np_travel_times = np.array(travel_times.times)
chosen_bases = []
demands_covered = 0
required_travel_time = 600

for _ in range(settings.num_bases):
    # Make a True/False table of the travel_times and then count how many covered.
    covered = [[t < required_travel_time for t in row] for row in np_travel_times]
    count_covered = [(index, covered[index].count(True)) for index in range(len(covered))]
    d = [('index', int), ('covered', int)]
    count_covered = np.array(count_covered, d)

    # Sort the table by row and grab the last element (the base with the most coverage)
    (best_base, count) = np.sort(count_covered, order='covered', kind='mergesort')[-1]
    chosen_bases.append(base_set.locations[best_base])
    demands_covered += count
    demand_coverage = covered[best_base]

    # Delete the covered columns
    delete_cols = [d for d in range(len(demand_coverage)) if demand_coverage[d]]
    np_travel_times = np.delete(np_travel_times, delete_cols, axis=1)

# Create new base set after filtering bases
base_set = KDTreeLocationSet(chosen_bases)

# Initialize dataset for cases
# case_set = Jan2017CaseSet(filename=settings.cases_file)
# case_set = DeDatosCaseSet(filename=settings.cases_file, duration_generator=event_duration_generator)

# Define random case params
# This example = 4 cases an hour

num_cases = 3
timeframe = timedelta(hours=1)
# num_cases = 400
# timeframe = timedelta(hours=96)

initial_time = datetime.now() - timeframe
end_time = datetime.now()
minutes = timeframe.total_seconds() / 60

# Define a poisson case time generator with given lambda
case_time_generator = PoissonCaseTimeGenerator(lmda=num_cases / minutes)

# Define a random location generator

center = Point(latitude=32.504876, longitude= -116.958774)
radius = 0.5

# location_generator = RandomCircleLocationGenerator(center=center, radius=radius)

# p1 = [
#     Point(32.536133, -117.046517),
#     Point(32.524786, -117.048024),
#     Point(32.516778, -117.033531),
#     Point(32.523999, -117.011641),
#     Point(32.540343, -117.012103)
# ]
#
# p2 = [
#     Point(32.517819, -117.056606),
#     Point(32.514025, -117.076816),
#     Point(32.496831, -117.068864),
#     Point(32.492395, -117.052702),
#     Point(32.503284, -117.052451)
# ]
#
# p3 = [
#     Point(32.507969, -117.040670),
#     Point(32.493550, -117.030457),
#     Point(32.497594, -117.003704),
#     Point(32.516966, -117.008547)
# ]
#
# polygons = [p1, p2, p3]

# case_location_generator = MultiPolygonLocationGenerator(polygons, densities=[0.65, 0.15, 0.2])

perimeter_vertices = [
    Point(32.533696, -117.123506),
    Point(32.554803, -116.876454),
    Point(32.469300, -116.789148),
    Point(32.439235, -116.967181),
    Point(32.530337, -117.123475)
]

case_location_generator = PolygonLocationGenerator(perimeter_vertices)

event_travel_duration_generator = TravelTimeDurationGenerator(travel_times=travel_times)
event_incident_duration_generator = RandomDurationGenerator(lower_bound=timedelta(minutes=5),
                                                            upper_bound=timedelta(minutes=10))
event_hospital_duration_generator = RandomDurationGenerator(lower_bound=timedelta(minutes=5),
                                                            upper_bound=timedelta(minutes=10))
hospital_selector = FastestHospitalSelector(hospital_set=hospital_set,
                                            travel_times=travel_times)

event_generator = EventGenerator(travel_duration_generator=event_travel_duration_generator,
                                 incident_duration_generator=event_incident_duration_generator,
                                 hospital_duration_generator=event_hospital_duration_generator,
                                 hospital_selector=hospital_selector)

case_set = RandomCaseSet(num_cases=num_cases,
                         initial_time=initial_time,
                         case_time_generator=case_time_generator,
                         location_generator=case_location_generator,
                         event_generator=event_generator,
                         hospital_selector=hospital_selector)

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

# Generate ambulances - random base placement (may want to abstract into function)
base_selector = RoundRobinBaseSelector(base_set=base_set)
ambulance_set = CustomAmbulanceSet(ambulance_count=settings.num_ambulances,
                                   base_selector=base_selector)

# Initialize simulator
sim = EventDispatcherSimulator(ambulance_set=ambulance_set,
                               case_set=case_set,
                               ambulance_selector=ambulance_select,
                               metric_aggregator=metric_aggregator)

# Start the simulation
case_record_set, metric_aggregator = sim.run()

ambulance_set.write_to_file('./results/ambulances.csv')
base_set.write_to_file('./results/bases.csv')
hospital_set.write_to_file('./results/hospitals.csv')
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
