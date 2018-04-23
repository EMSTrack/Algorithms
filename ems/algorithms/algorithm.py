# Framework for using algorithms and allowing for replacement

import copy
from datetime import timedelta

import geopy
import geopy.distance
import numpy as np

from ems.models.base import Base


# The following functions define default algorithms for the DispatchAlgorithm class.


def kmeans_init_bases(dataset):
    # This function happens to require the original Cruz Roja dataset. It doesn't necessarily need to.
    # For example, we could randomly choose bases.

    print("Default init_bases(): Kmeans init bases")

    # times[demand point][base] if using the pandas way
    # Using pandas dataframe
    chosen_base_indices, demands_covered = pick_starting_bases(dataset.traveltimes_df, 12, 600)

    # Returns object list
    chosen_bases = [dataset.bases[index] for index in chosen_base_indices]

    return chosen_bases


# Refactor TODO. I can't believe I just shoved this in and it worked.
def pick_starting_bases(traveltimes, num_bases, required_traveltime):
    traveltimes = copy.deepcopy(traveltimes)
    traveltimes = np.array(traveltimes)
    chosen_bases = []
    demands_covered = 0

    for _ in range(num_bases):
        # Make a True/False table of the times and then count how many covered.
        covered = [[t < required_traveltime for t in row] for row in traveltimes]
        count_covered = [(index, covered[index].count(True)) for index in range(len(covered))]
        d = [('index', int), ('covered', int)]
        count_covered = np.array(count_covered, d)

        # Sort the table by row and grab the last element (the base with the most coverage)
        (best_base, count) = np.sort(count_covered, order='covered', kind='mergesort')[-1]
        chosen_bases.append(best_base)
        demands_covered += count
        demand_coverage = covered[best_base]

        # Delete the covered columns 
        delete_cols = [d for d in range(len(demand_coverage)) if demand_coverage[d]]
        traveltimes = np.delete(traveltimes, delete_cols, axis=1)

    return chosen_bases, demands_covered


# "Bases" represents the chosen bases from init_bases
def random_ambulance_placements(bases, num_ambulances):
    print("Default init_ambulance_placements(): Random Ambulance Placements")

    ambulance_bases = []

    # Assign ambulances to bases
    for index in range(num_ambulances):
        ambulance_bases.append(bases[index % len(bases)])

    return ambulance_bases


def fastest_traveltime(dataset, ambulances, case):
    print("Default select_ambulance(): Fastest Traveltime")

    # Find the closest demand point to the given case
    closest_demand = closest_distance(dataset.demands, case.location)

    # Select an ambulance to attend to the given case and obtain the its duration of travel
    chosen_ambulance, ambulance_travel_time = find_available_ambulance(
        ambulances, dataset.traveltimes, closest_demand)

    return chosen_ambulance, ambulance_travel_time


def closest_distance(list_type, target_point):
    """
    Finds the closest point in the corresponding generic list.
    For example, find the closest base given a GPS location.
    :param list_type:
    :param target_point:
    :return: the position in that list
    """
    shortest_difference = 999999999
    position = -1

    for index in range(len(list_type)):
        # print(list_type)
        if list_type[index] is not None:

            difference = geopy.distance.vincenty(target_point, list_type[index].location).km
            if shortest_difference > difference:
                shortest_difference = difference
                position = index
                # print (type(difference), shortest_difference)
                if shortest_difference < 0.5:
                    return list_type[position]

    return list_type[position]


def find_available_ambulance(ambulances, traveltimes, demand):
    """
    Find an available ambulance if possible.
    :param ambulances: of type dictionary.
    :return: type int the ID of the ambulance, or None if all ambulances are busy.
    """
    amb_id = -1
    shortest_distance = 99999999999

    total_ambulances = len(ambulances)

    ambulance_bases = [a.base if not a.deployed else None for a in ambulances]
    # print('Length of ambulance locations:', len(ambulance_locations))
    # print('FA:', ambulance_locations)
    result, case_time = closest_time(ambulance_bases, traveltimes, demand)
    # print('Position:',result)
    if result > -1:
        return result, case_time

    # for amb in ambulances:
    #     if amb['deployed'] == False:
    #         distance =

    return None, None


def closest_time(list_type, traveltimes, demand):
    """
    Finds the ambulance, given a list of ambulances, that will reach the
    demand point the closest. The demand point must be in the list of demands.
    IF it is not, then use the above function `closest_distance` to find the
    closest demand point given a GPS coordinate.
    The parameter names are bad and the code needs to be refactored, probably
    :param list_type:
    :param bases:
    :param demands:
    :param traveltimes:
    :param target_point:
    :return:
    """
    shortest_difference = timedelta(hours=999999999)
    position = -1
    for index in range(len(list_type)):

        if list_type[index] is not None:

            difference = traveltime(traveltimes, list_type[index], demand)
            if shortest_difference > difference:
                shortest_difference = difference
                position = index

    return position, shortest_difference


def traveltime(times, base, demand):
    """
    Takes the travel time mapping, starting base, and ending demand to find time.
    :param base:
    :param demand:
    :return travel time: 
    """

    # base should be a base object
    # demand should be a demand object

    return times[(base.id, demand.id)].traveltime


# This class is used by the sim to run.
class DispatcherAlgorithm():

    # To instantiate this object, three function pointers must have been passed in.
    def __init__(self,
                 init_bases: callable = kmeans_init_bases,
                 init_ambulance_placements: callable = random_ambulance_placements,
                 select_ambulance: callable = fastest_traveltime):
        self.init_bases = init_bases
        self.init_ambulance_placements = init_ambulance_placements
        self.select_ambulance = select_ambulance

    # TODO -- maybe move assertions to tests.py
    def init_bases_typecheck(self, dataset):
        """ Runs init_bases, but makes sure the resulting dataset.chosen_bases is right type """
        self.init_bases(dataset)
        assert isinstance(dataset.chosen_bases, list)
        for element in dataset.chosen_bases:
            assert isinstance(element, Base)

    # TODO
    def init_ambulance_placements_typecheck(self, dataset):
        """ Runs init_ambulance_placements, but makes sure the resulting ___ is right type or state"""
        pass

        # TODO

    def select_ambulance_typecheck(self, dataset):
        """ Runs select_ambulance, but makes sure the resulting ___ is right type or state"""
        pass
