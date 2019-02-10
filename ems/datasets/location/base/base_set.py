from typing import List

from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.utils import parse_unheadered_csv


class BaseSet(KDTreeLocationSet):

    def __init__(self,
                 filename: str = None,
                 latitudes: List[float] = None,
                 longitudes: List[float] = None):
        self.filename = filename
        if filename is not None:
            latitudes, longitudes = self.read_bases(filename)
        super().__init__(latitudes, longitudes)

    def read_bases(self, filename):
        # Read bases from an unheadered CSV into a pandas dataframe
        base_col_positions = [4, 5]
        base_headers = ["lat", "long"]
        bases_df = parse_unheadered_csv(filename, base_col_positions, base_headers)

        # Generate list of models from dataframe
        latitudes = []
        longitudes = []
        for index, row in bases_df.iterrows():
            latitudes.append(row["lat"])
            longitudes.append(row["long"])

        return latitudes, longitudes
