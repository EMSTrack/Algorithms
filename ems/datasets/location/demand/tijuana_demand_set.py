from geopy import Point

from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.utils import parse_unheadered_csv


class TijuanaDemandSet(KDTreeLocationSet):

    def __init__(self, filename):
        demands = self.read_demands(filename)
        super().__init__(demands)

    def read_demands(self, filename):
        # Read demands from an unheadered CSV into a pandas dataframe
        demand_col_positions = [0, 1]
        demand_headers = ["lat", "long"]
        demands_df = parse_unheadered_csv(filename, demand_col_positions, demand_headers)

        # Generate list of models from dataframe
        demands = []
        for index, row in demands_df.iterrows():
            demand = Point(row["lat"], row["long"])
            demands.append(demand)

        return demands
