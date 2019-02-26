from typing import List

from ems.datasets.location.location_set import LocationSet
from ems.utils import parse_headered_csv


class BaseSet(LocationSet):

    def __init__(self,
                 filename: str = None,
                 latitudes: List[float] = None,
                 longitudes: List[float] = None):
        self.filename = filename
        if filename is not None:
            latitudes, longitudes = self.read_bases(filename)
        super().__init__(latitudes, longitudes)

    def read_bases(self, filename):
        # Read bases from a headered CSV into a pandas dataframe
        base_headers = ["latitude", "longitude"]
        bases_df = parse_headered_csv(filename, base_headers)

        # Generate list of models from dataframe
        latitudes = []
        longitudes = []
        for index, row in bases_df.iterrows():
            latitudes.append(row["latitude"])
            longitudes.append(row["longitude"])

        return latitudes, longitudes
