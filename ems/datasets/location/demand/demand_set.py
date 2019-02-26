from typing import List

from ems.datasets.location.location_set import LocationSet
from ems.utils import parse_headered_csv


class DemandSet(LocationSet):

    def __init__(self,
                 filename: str = None,
                 latitudes: List[float] = None,
                 longitudes: List[float] = None):
        if filename is not None:
            latitudes, longitudes = self.read_demands(filename)
        super().__init__(latitudes, longitudes)

    def read_demands(self, filename):
        # Read demands from a headered CSV into a pandas dataframe
        demand_headers = ["latitude", "longitude"]
        demands_df = parse_headered_csv(filename, demand_headers)

        # Generate list of models from dataframe
        latitudes = []
        longitudes = []
        for index, row in demands_df.iterrows():
            latitudes.append(row["latitude"])
            longitudes.append(row["longitude"])

        return latitudes, longitudes
