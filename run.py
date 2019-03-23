from ems.driver import read_user_input, Driver
from ems.models.events.event_type import EventType
import os

from IPython import embed


# Initialize configurations
sim_args = read_user_input()
driver = Driver()
driver.create_objects(sim_args)

# # Check if the figures folder exists, and then if the name of the output folder (name of simulator) exists.
output_dir = "./figures/" + driver.objects['name'] + "/"
current_dir = os.getcwd()
if 'Algorithms' != current_dir.split('/')[-1]:
    raise Exception("Run this simulator from the repository directory. ")

subdirs = [dirs for roots, dirs, _ in os.walk('.')]
subdirs = filter(lambda subdir: 'figures' in subdir, subdirs)

if not any(subdirs):
    os.mkdir('figures')

results_dir = [dirs for roots, dirs, _ in os.walk('./figures')]
results_dir = filter(lambda subdir: driver.objects['name'] in subdir, results_dir)

if not any(results_dir):
    os.mkdir(output_dir)


# # Check if the results folder exists, and then if the name of the output folder (name of simulator) exists.
output_dir = "./results/" + driver.objects['name'] + "/"
current_dir = os.getcwd()
if 'Algorithms' != current_dir.split('/')[-1]:
    raise Exception("Run this simulator from the repository directory. ")

subdirs = [dirs for roots, dirs, _ in os.walk('.')]
subdirs = filter(lambda subdir: 'results' in subdir, subdirs)

if not any(subdirs):
    os.mkdir('results')

results_dir = [dirs for roots, dirs, _ in os.walk('./results')]
results_dir = filter(lambda subdir: driver.objects['name'] in subdir, results_dir)

if not any(results_dir):
    os.mkdir(output_dir)


# # Save as much information as possible BEFORE the simulator runs in case it crashes.
driver.objects['simulation_bases'].write_to_file(output_dir + '/chosen_bases.csv')
driver.objects['ambulances'].write_to_file(output_dir +'/chosen_ambulances.csv')
driver.objects['hospitals'].write_to_file(output_dir +'/chosen_hospitals.csv')

# Run the simulator.
print("Begin simulator: ", driver.objects['name'])
sim = driver.objects["simulator"]
case_record_set, metric_aggregator = sim.run()

case_record_set.write_to_file('../processed_cases.csv')

# Save the finished simulator information

case_record_set.write_to_file(output_dir + '/processed_cases.csv')
metric_aggregator.write_to_file(output_dir + '/metrics.csv')

#
# polygon_coordinates = {
#     'latitude': sim_args['simulator']['cases']['case_location_generator']['vertices_latitude'] ,
#     'longitude': sim_args['simulator']['cases']['case_location_generator']['vertices_longitude']
# }

events = [event for case_record in case_record_set.case_records for event in case_record.event_history]

# import numpy as np
# errors = [event.error for event in events if event.error is not None]
#
#
# print("-- Error Summary -- ")
# print("Count:  {}".format(len(errors)))
# print("Mean:   {}".format(np.mean(errors)))
# print("Median: {}".format(np.median(errors)))
# print()
# print("Min:    {}".format(np.min(errors)))
# print("Max:    {}".format(np.max(errors)))

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



info = {
    # "polygon": polygon_coordinates ,
    "incident_locs": incident_locations ,
    "hospital_locs": hospital_locations,
    "sim_locs" : sim_locations,
    "base_locs": base_locations
}



# with open ("./error-analysis/error-coordinates.yaml", 'w') as error_file:
#     info_yaml = yaml.dump(info)
#     error_file.write(info_yaml)


print("Done: {}".format(driver.objects['name']))