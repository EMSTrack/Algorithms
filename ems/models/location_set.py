from scipy.spatial import KDTree


class LocationSet:

    def __init__(self, locations):
        self.locations = locations
        self.kd_tree = self._initialize_kd_tree(locations)

    def _initialize_kd_tree(self):

        # Form a kd-tree
        points = [(demand.location.longitude, demand.location.latitude) for demand in self.locations]
        kd_tree = KDTree(points)
        return kd_tree

    def closest(self, point):
        """
        Finds the closest point in the corresponding generic list.
        For example, find the closest base given a GPS location.
        :param list_type:
        :param target_point:
        :return: the position in that list
        """

        # Query kd tree for nearest neighbor
        closest_point_ind = self.kd_tree.query((point.longitude, point.latitude))[1]

        return self.locations[closest_point_ind], closest_point_ind
