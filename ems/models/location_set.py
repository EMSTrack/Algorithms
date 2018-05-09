from typing import List

from scipy.spatial import KDTree

from ems.models.location import Location


class LocationSet:

    def __init__(self, locations: List[Location]):
        self.locations = locations
        self.kd_tree = self._initialize_kd_tree()

    def _initialize_kd_tree(self):
        """
        Initialize the kd_tree.
        Helper Method.
        :return:
        """

        # Form a kd-tree
        points = [(loc.location.longitude, loc.location.latitude) for loc in self.locations]
        kd_tree = KDTree(points)
        return kd_tree

    def closest(self, point):
        """
        Finds the closest point in the corresponding generic list.
        For example, find the closest base given a GPS location.
        :param point:
        :return: The closest point and its index
        """

        # Query kd tree for nearest neighbor
        closest_point_ind = self.kd_tree.query((point.longitude, point.latitude))[1]

        return self.locations[closest_point_ind], closest_point_ind
