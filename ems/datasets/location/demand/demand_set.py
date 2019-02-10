from typing import List

from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.utils import parse_unheadered_csv


class DemandSet(KDTreeLocationSet):

    def __init__(self,
                 filename: str = None,
                 latitudes: List[float] = None,
                 longitudes: List[float] = None):
        if filename is not None:
            latitudes, longitudes = self.read_demands(filename)
        super().__init__(latitudes, longitudes)

    def read_demands(self, filename):
        # Read demands from an unheadered CSV into a pandas dataframe
        demand_col_positions = [0, 1]
        demand_headers = ["lat", "long"]
        demands_df = parse_unheadered_csv(filename, demand_col_positions, demand_headers)

        # Generate list of models from dataframe
        latitudes = []
        longitudes = []
        for index, row in demands_df.iterrows():
            latitudes.append(row["lat"])
            longitudes.append(row["long"])

        return latitudes, longitudes
