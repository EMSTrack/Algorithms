# The following functions define default algorithms for the DispatchAlgorithm class.
from datetime import timedelta
from typing import List

import geopy
import geopy.distance
import numpy as np

from copy import deepcopy

from scipy.spatial import KDTree

from ems.algorithms.algorithm import Algorithm
from ems.data.traveltimes import TravelTimes
from ems.models.ambulance import Ambulance
from ems.models.base import Base
from ems.models.case import Case
from ems.models.demand import Demand


# An implementation of a "fastest travel time" algorithm from a base to
# the demand point closest to a case

class DispatcherAlgorithm(Algorithm):

    def __init__(self,
                 bases: List[Base] = None,
                 demands: List[Demand] = None,
                 traveltimes: TravelTimes = None):
        self.bases = bases
        self.demands = demands
        self.traveltimes = traveltimes

        self.kd_tree = self.initialize_kd_tree(demands)

    def select_ambulance(self,
                         ambulances: List[Ambulance],
                         case: Case):

        # Compute the closest demand point to the case location
        closest_demand = self.closest_distance(self.demands, case.location)

        # Select an ambulance to attend to the given case and obtain the its duration of travel
        chosen_ambulance, ambulance_travel_time = self.find_fastest_ambulance(
            ambulances, self.traveltimes, closest_demand)

        return chosen_ambulance, ambulance_travel_time

    def closest_distance(self, list_type, target_point):
        """
        Finds the closest point in the corresponding generic list.
        For example, find the closest base given a GPS location.
        :param list_type:
        :param target_point:
        :return: the position in that list
        """

        # Query kd tree for nearest neighbor
        closest_point_ind = self.kd_tree.query((target_point.longitude, target_point.latitude))[1]

        return list_type[closest_point_ind]

    def find_fastest_ambulance(self, ambulances, traveltimes, demand):
        """
        Finds the ambulance with the shortest one way travel time from its base to the
        demand point
        :param ambulances:
        :param traveltimes:
        :param demand:
        :return: The ambulance and the travel time
        """

        shortest_time = timedelta(hours=9999999)
        fastest_amb = None

        for amb in ambulances:
            if not amb.deployed:
                time = self.find_traveltime(traveltimes, amb.base, demand)
                if shortest_time > time:
                    shortest_time = time
                    fastest_amb = amb

        if fastest_amb is not None:
            return fastest_amb, shortest_time

        return None, None

    def find_traveltime(self, traveltimes, base, demand):
        """
        Takes the travel time mapping, starting base, and ending demand to find time.
        :param base:
        :param demand:
        :return travel time:
        """

        return traveltimes.get_time(base, demand)

    def initialize_kd_tree(self, demands):

        # Form a kd-tree
        points = [(demand.location.longitude, demand.location.latitude) for demand in demands]
        kd_tree = KDTree(points)
        return kd_tree




    def find_partial_coverage (self, base, demands_to_cover):

        print("Length of demands: ", len(demands_to_cover))
        # find the traveltime from the base to each demand, if it is less than 600 then it is covered
        for i in range(len(demands_to_cover)):
            
            time = self.traveltimes.get_time(base, demands_to_cover[i])
            covered = time.total_seconds() < 600
            if covered:
                demands_to_cover[i] = None
                

        return list(filter(None.__ne__, demands_to_cover))

    def determine_coverage (self, ambulances:List[Ambulance], case):
        # Given a set of ambulances, for each available ambulance, find its base and calculate how 
        # many demands are covered. For each covered demand, delete it from the demand. 

        # Continue until no more available ambulances, and then count remaining demand as 
        # uncovered demands. 

        checked_bases = []
        active_bases = list([amb.base for amb in ambulances if not amb.deployed])
        demands_covered = [0 for _ in self.demands]

        for index in range(len(demands_covered)):
            if not demands_covered[index]:
                for base in active_bases:
                    if self.traveltimes.get_time(base, self.demands[index]).total_seconds() < 600:
                        demands_covered[index] = 1
                        break
        print("Coverage: ",sum(demands_covered))
        return sum(demands_covered) 




        # demands_to_cover = deepcopy(self.demands)
        # covered = [0 for _ in demands_to_cover]

        # active_bases = list([amb.base for amb in ambulances if not amb.deployed])

        # print("Active bases: ", len(active_bases))
        # for base in active_bases:
        #     demands_to_cover = self.find_partial_coverage(base, demands_to_cover)



        # print ("Coverage: " ,sum(covered))



        # uncovered = sum([1 for u in demands_to_cover])
        # print("Coverage: ", 100 - uncovered )
        # return 100 - uncovered




