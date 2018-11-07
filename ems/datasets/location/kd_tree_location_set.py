from typing import List

from geopy import Point
from scipy.spatial import KDTree

from ems.datasets.location.location_set import LocationSet


class KDTreeLocationSet(LocationSet):

    def __init__(self, locations: List[Point]):
        super().__init__(locations)
        self.kd_tree = self._initialize_kd_tree()

    def _initialize_kd_tree(self):
        """
        Initialize the kd_tree.
        Helper Method.
        :return:
        """

        # Form a kd-tree with the given list of locations
        points = [(loc.longitude, loc.latitude) for loc in self.locations]
        kd_tree = KDTree(points)
        return kd_tree

    def closest(self, point: Point):
        """
        Finds the closest point in the corresponding generic list.
        For example, find the closest base given a GPS location.
        :param point:
        :return: The closest point and its index
        """

        # Query kd tree for nearest neighbor
        closest_point_data = self.kd_tree.query((point.longitude, point.latitude))

        # Retrieve closest point, its index, and the distance to it
        closest_point_ind = closest_point_data[1]
        closest_point = self.locations[closest_point_ind]
        closest_point_distance = closest_point_data[0]

        return closest_point, closest_point_ind, closest_point_distance