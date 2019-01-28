from ems.driver import read_user_input, Driver
from ems.models.events.event_type import EventType

# Initialize configurations
sim_args = read_user_input()
driver = Driver()
driver.create_objects(sim_args)
sim = driver.objects["simulator"]
case_record_set, metric_aggregator = sim.run()



polygon_coordinates = {
    'latitude': sim_args['simulator']['cases']['case_location_generator']['vertices_latitude'] ,
    'longitude': sim_args['simulator']['cases']['case_location_generator']['vertices_longitude']
}



events = [event for case_record in case_record_set.case_records for event in case_record.event_history]

# lat, lon
incident_dests = [event.destination for event in events if event.event_type == EventType.TO_INCIDENT]
incident_lats = [e.latitude for e in incident_dests]
incident_lons = [e.longitude for e in incident_dests]

incident_locations = {
    'latitude': incident_lats,
    'longitude': incident_lons,
}

# lat, lon
hospital_dests = [event.destination for event in events if event.event_type == EventType.TO_HOSPITAL]
hospital_lats = [e.latitude for e in hospital_dests]
hospital_lons = [e.longitude for e in hospital_dests]

hospital_locations = {
    'latitude': hospital_lats,
    'longitude': hospital_lons,
}

# lat, lon
base_dests = [event.destination for event in events if event.event_type == EventType.TO_BASE]
base_lats = [e.latitude for e in base_dests]
base_lons = [e.longitude for e in base_dests]

base_locations = {
    'latitude': base_lats,
    'longitude': base_lons,
}


sim_dests  = [event.sim_dest for event in events if event.sim_dest]
sim_lats = [e.latitude for e in sim_dests]
sim_lons = [e.longitude for e in sim_dests]

sim_locations = {
    'latitude': sim_lats,
    'longitude': sim_lons,
}

import yaml

info = {
    "polygon": polygon_coordinates ,
    "incident_locs": incident_locations ,
    "hospital_locs": hospital_locations,
    "sim_locs" : sim_locations,
    "base_locs": base_locations
}

with open ("./error-analysis/error-data.yaml", 'w') as error_file:
    info_yaml = yaml.dump(info)
    error_file.write(info_yaml)


















# # Initialize datasets
# demand_set = TijuanaDemandSet(filename=settings.demands_file)
# base_set = TijuanaBaseSet(filename=settings.bases_file)
# hospital_set = LocationSet(locations=[Point(longitude=-117.0097589492798,
#                                             latitude=32.52506901611384),
#                                       Point(longitude=-117.00371, latitude=32.5027),
#                                       Point(longitude=-117.0078, latitude=32.5180)])
# travel_times = TijuanaTravelTimes(origins=base_set,
#                                   destinations=demand_set,
#                                   filename=settings.travel_times_file)
# 
# 
# # Filter base_set
# np_travel_times = np.array(travel_times.times)
# chosen_bases = []
# demands_covered = 0
# required_travel_time = 600
# 
# for _ in range(settings.num_bases):
#     # Make a True/False table of the travel_times and then count how many covered.
#     covered = [[t < required_travel_time for t in row] for row in np_travel_times]
#     count_covered = [(index, covered[index].count(True)) for index in range(len(covered))]
#     d = [('index', int), ('covered', int)]
#     count_covered = np.array(count_covered, d)
# 
#     # Sort the table by row and grab the last element (the base with the most coverage)
#     (best_base, count) = np.sort(count_covered, order='covered', kind='mergesort')[-1]
#     chosen_bases.append(base_set.locations[best_base])
#     demands_covered += count
#     demand_coverage = covered[best_base]
# 
#     # Delete the covered columns
#     delete_cols = [d for d in range(len(demand_coverage)) if demand_coverage[d]]
#     np_travel_times = np.delete(np_travel_times, delete_cols, axis=1)
# 
# # Create new base set after filtering bases
# base_set = KDTreeLocationSet(chosen_bases)
# 
# # Initialize dataset for cases
# # case_set = Jan2017CaseSet(filename=configurations.cases_file)
# # case_set = DeDatosCaseSet(filename=configurations.cases_file, duration_generator=event_duration_generator)
# 
# # Define random case params
# # This example = 4 cases an hour
# 
# num_cases = 150
# timeframe = timedelta(hours=15)
# 
# initial_time = datetime.now() - timeframe
# end_time = datetime.now()
# minutes = timeframe.total_seconds() / 60
# 
# # Define a poisson case time generator with given lambda
# case_time_generator = PoissonCaseTimeGenerator(lmda=num_cases / minutes)
# 
# # Define a random location generator
# 
# center = Point(latitude=32.504876, longitude= -116.958774)
# radius = 0.5
# 
# # location_generator = RandomCircleLocationGenerator(center=center, radius=radius)
# 
# # p1 = [
# #     Point(32.536133, -117.046517),
# #     Point(32.524786, -117.048024),
# #     Point(32.516778, -117.033531),
# #     Point(32.523999, -117.011641),
# #     Point(32.540343, -117.012103)
# # ]
# #
# # p2 = [
# #     Point(32.517819, -117.056606),
# #     Point(32.514025, -117.076816),
# #     Point(32.496831, -117.068864),
# #     Point(32.492395, -117.052702),
# #     Point(32.503284, -117.052451)
# # ]
# #
# # p3 = [
# #     Point(32.507969, -117.040670),
# #     Point(32.493550, -117.030457),
# #     Point(32.497594, -117.003704),
# #     Point(32.516966, -117.008547)
# # ]
# #
# # polygons = [p1, p2, p3]
# 
# # case_location_generator = MultiPolygonLocationGenerator(polygons, densities=[0.65, 0.15, 0.2])
# 
# perimeter_latitudes = [32.533696, 32.554803, 32.469300, 32.439235, 32.530337]
# perimeter_longitudes = [-117.123506, -116.876454, -116.789148, -116.967181, -117.123475]
# 
# case_location_generator = PolygonLocationGenerator(perimeter_latitudes, perimeter_longitudes)
# 
# event_travel_duration_generator = TravelTimeDurationGenerator(travel_times=travel_times)
# event_incident_duration_generator = RandomDurationGenerator(lower_bound=5,
#                                                             upper_bound=10)
# event_hospital_duration_generator = RandomDurationGenerator(lower_bound=5,
#                                                             upper_bound=10)
# hospital_selector = FastestHospitalSelector(hospital_set=hospital_set,
#                                             travel_times=travel_times)
# 
# event_generator = EventGenerator(travel_duration_generator=event_travel_duration_generator,
#                                  incident_duration_generator=event_incident_duration_generator,
#                                  hospital_duration_generator=event_hospital_duration_generator,
#                                  hospital_selector=hospital_selector)
# 
# case_set = RandomCaseSet(quantity=num_cases,
#                          initial_time=initial_time,
#                          case_time_generator=case_time_generator,
#                          case_location_generator=case_location_generator,
#                          event_generator=event_generator,
#                          hospital_selector=hospital_selector)
# 
# # Initialize ambulance_selection algorithm
# ambulance_select = BestTravelTime(travel_times=travel_times)
# 
# # Initialize demand percentage coverage metric
# percent_coverage = PercentCoverage(demands=demand_set,
#                                    travel_times=travel_times,
#                                    r1=timedelta(seconds=600))
# 
# # Initialize demand radius coverage metric
# radius_coverage = RadiusCoverage(demands=demand_set,
#                                  travel_times=travel_times)
# 
# # Initialize other metrics
# total_delay = TotalDelay()
# count_pending = CountPending()
# 
# # Initialize metric aggregator
# metric_aggregator = MetricAggregator([percent_coverage, total_delay, count_pending])
# 
# # Generate ambulances - random base placement (may want to abstract into function)
# base_selector = RoundRobinBaseSelector(base_set=base_set)
# ambulance_set = CustomAmbulanceSet(count=settings.num_ambulances,
#                                    base_selector=base_selector)
# 
# # Initialize simulator
# sim = EventDispatcherSimulator(ambulances=ambulance_set,
#                                cases=case_set,
#                                ambulance_selector=ambulance_select,
#                                metric_aggregator=metric_aggregator)
# 
# # Start the simulation
# case_record_set, metric_aggregator = sim.run()
# 
# ambulance_set.write_to_file('./results/ambulances.csv')
# base_set.write_to_file('./results/bases.csv')
# hospital_set.write_to_file('./results/hospitals.csv')
# case_record_set.write_to_file('./results/processed_cases.csv')
# metric_aggregator.write_to_file('./results/metrics.csv')

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
