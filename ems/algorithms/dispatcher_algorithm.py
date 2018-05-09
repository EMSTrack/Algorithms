# The following functions define default algorithms for the DispatchAlgorithm class.
from datetime import timedelta
from typing import List

import geopy
import geopy.distance
import numpy as np

from copy import deepcopy

from scipy.spatial import KDTree

from ems.algorithms.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.data.traveltimes import TravelTimes
from ems.models.ambulance import Ambulance
from ems.models.base import Base
from ems.models.case import Case
from ems.models.demand import Demand


# An implementation of a "fastest travel time" algorithm from a base to
# the demand point closest to a case

class BestTravelTimeAlgorithm(AmbulanceSelectionAlgorithm):

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

        # Determine the overall coverage, and each ambulance's disruption to the cost. TODO 
        # current_coverage = self.determine_coverage(ambulances, case)

        return {'choice': chosen_ambulance,
                'travel_time': ambulance_travel_time}

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







